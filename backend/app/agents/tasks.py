"""Celery tasks – bridges the async agent pipeline with the task queue."""

from __future__ import annotations

import asyncio
import logging
import uuid
from datetime import datetime, timezone

from app.worker import celery_app

logger = logging.getLogger(__name__)


def _run_async(coro):
    """Run an async function from synchronous Celery task context."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def run_campaign_pipeline(self, brief_id: str):
    """Run the full brief-to-campaign LangGraph pipeline.

    Called when a client submits a brief.
    """
    logger.info(f"Starting campaign pipeline for brief {brief_id}")

    async def _execute():
        # Import here to avoid circular imports at module level
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.brief import Brief
        from app.models.campaign import Campaign
        from app.models.task import AgentTask
        from app.agents.workflows.brief_to_campaign import campaign_graph

        engine = create_async_engine(settings.database_url)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with session_factory() as db:
            # Load the brief
            result = await db.execute(select(Brief).where(Brief.id == uuid.UUID(brief_id)))
            brief = result.scalar_one_or_none()
            if not brief:
                raise ValueError(f"Brief {brief_id} not found")

            # Create campaign record
            campaign = Campaign(
                brief_id=brief.id,
                client_id=brief.client_id,
                name=f"Campaign: {brief.title}",
                status="strategy",
            )
            db.add(campaign)
            await db.flush()

            # Update brief status
            brief.status = "in_progress"
            await db.commit()

            campaign_id = str(campaign.id)

            # Record task start
            task_record = AgentTask(
                campaign_id=campaign.id,
                assigned_to_pod="orchestrator",
                assigned_to_agent="campaign_pipeline",
                task_type="brief_to_campaign",
                input_data={"brief_id": brief_id},
                status="in_progress",
                started_at=datetime.now(timezone.utc),
            )
            db.add(task_record)
            await db.commit()

            # Build state and run the LangGraph pipeline
            initial_state = {
                "brief": {
                    "title": brief.title,
                    "campaign_objective": brief.campaign_objective,
                    "target_audience": brief.target_audience,
                    "budget_total": brief.budget_total,
                    "budget_duration_days": brief.budget_duration_days,
                    "platforms": brief.platforms,
                    "kpis": brief.kpis,
                    "brand_voice": brief.brand_voice,
                },
                "brand_guidelines": {},  # TODO: load from client
                "campaign_id": campaign_id,
            }

            try:
                final_state = await campaign_graph.ainvoke(initial_state)

                # Save outputs to campaign
                campaign.strategy_output = {
                    "market_research": final_state.get("market_research", {}),
                    "brand_strategy": final_state.get("brand_strategy", {}),
                }
                campaign.creative_output = {
                    "ad_copy": final_state.get("ad_copy", {}),
                    "visual_creative": final_state.get("visual_creative", {}),
                }
                campaign.status = "approval"

                # Mark task complete
                task_record.status = "completed"
                task_record.output_data = {"final_stage": final_state.get("current_stage")}
                task_record.completed_at = datetime.now(timezone.utc)

                # Mark brief as completed
                brief.status = "completed"

                await db.commit()
                logger.info(f"Campaign pipeline completed for {campaign_id}")

            except Exception as e:
                logger.error(f"Pipeline failed for brief {brief_id}: {e}")
                campaign.status = "planning"  # Reset to allow retry
                task_record.status = "failed"
                task_record.error = str(e)
                task_record.completed_at = datetime.now(timezone.utc)
                await db.commit()
                raise

        await engine.dispose()

    _run_async(_execute())


@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def launch_campaign(self, campaign_id: str):
    """Create the campaign on Meta Ads after client approval."""
    logger.info(f"Launching campaign {campaign_id} on Meta Ads")

    async def _execute():
        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
        from app.config import settings
        from app.models.campaign import Campaign
        from app.integrations.meta_ads import meta_ads_client

        engine = create_async_engine(settings.database_url)
        session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        async with session_factory() as db:
            result = await db.execute(select(Campaign).where(Campaign.id == uuid.UUID(campaign_id)))
            campaign = result.scalar_one_or_none()
            if not campaign:
                raise ValueError(f"Campaign {campaign_id} not found")

            # Create campaign on Meta
            meta_result = await meta_ads_client.create_campaign(
                ad_account_id="placeholder",
                name=campaign.name,
                daily_budget=int(campaign.brief.budget_total / campaign.brief.budget_duration_days * 100) if campaign.brief else 1000,
            )

            campaign.platform_data = {"meta": meta_result}
            campaign.status = "live"
            campaign.launched_at = datetime.now(timezone.utc)
            await db.commit()

            logger.info(f"Campaign {campaign_id} launched on Meta: {meta_result}")

        await engine.dispose()

    _run_async(_execute())
