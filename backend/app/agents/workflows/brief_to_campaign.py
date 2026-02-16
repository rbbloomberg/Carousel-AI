"""LangGraph workflow: Brief → Strategy → Creative → Approval.

Pipeline DAG:
    market_research → brand_strategy → [copywriting, visual_creative] → END
                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                        These two run in PARALLEL since
                                        visual_creative doesn't need ad_copy
                                        to generate image concepts.
"""

from __future__ import annotations

import logging
from typing import Annotated, TypedDict

from langgraph.graph import END, StateGraph

from app.agents.strategy.market_research import MarketResearchAgent
from app.agents.strategy.brand_strategy import BrandStrategyAgent
from app.agents.creative.copywriting import CopywritingAgent
from app.agents.creative.visual_creative import VisualCreativeAgent
from app.services.events import EventPublisher, EventType, event_publisher

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Merge helper for parallel node outputs
# ---------------------------------------------------------------------------

def _merge_dicts(left: dict, right: dict) -> dict:
    """Merge two dicts, preferring right-side values."""
    merged = {**left}
    for key, value in right.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


# ---------------------------------------------------------------------------
# State schema – flows through every node
# ---------------------------------------------------------------------------

class CampaignState(TypedDict, total=False):
    # Inputs
    brief: dict
    brand_guidelines: dict
    campaign_id: str

    # Strategy outputs
    market_research: dict
    brand_strategy: dict

    # Creative outputs (written by parallel nodes)
    ad_copy: dict
    visual_creative: dict

    # Tracking
    current_stage: str
    stages_completed: list[str]
    error: str | None


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

async def run_market_research(state: CampaignState) -> dict:
    agent = MarketResearchAgent()
    campaign_id = state.get("campaign_id")

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_STARTED,
            agent=agent.name, pod=agent.pod, stage="market_research",
        )

    try:
        result = await agent.run(
            input_data=state["brief"],
            context={"brand_guidelines": state.get("brand_guidelines", {})},
        )
    except Exception as e:
        logger.error(f"Market research agent failed: {e}")
        if campaign_id:
            await event_publisher.publish(
                campaign_id, EventType.AGENT_FAILED,
                agent=agent.name, pod=agent.pod, stage="market_research",
                data={"error": str(e)},
            )
        return {"error": str(e)}

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_COMPLETED,
            agent=agent.name, pod=agent.pod, stage="market_research",
            data={"summary": result.get("recommendations", "")[:200]},
        )

    return {
        "market_research": result,
        "current_stage": "market_research",
        "stages_completed": ["market_research"],
    }


async def run_brand_strategy(state: CampaignState) -> dict:
    agent = BrandStrategyAgent()
    campaign_id = state.get("campaign_id")

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_STARTED,
            agent=agent.name, pod=agent.pod, stage="brand_strategy",
        )

    try:
        result = await agent.run(
            input_data=state["brief"],
            context={
                "market_research": state.get("market_research", {}),
                "brand_guidelines": state.get("brand_guidelines", {}),
            },
        )
    except Exception as e:
        logger.error(f"Brand strategy agent failed: {e}")
        if campaign_id:
            await event_publisher.publish(
                campaign_id, EventType.AGENT_FAILED,
                agent=agent.name, pod=agent.pod, stage="brand_strategy",
                data={"error": str(e)},
            )
        return {"error": str(e)}

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_COMPLETED,
            agent=agent.name, pod=agent.pod, stage="brand_strategy",
            data={"positioning": result.get("positioning", "")[:200]},
        )

    completed = list(state.get("stages_completed", []))
    completed.append("brand_strategy")

    return {
        "brand_strategy": result,
        "current_stage": "brand_strategy",
        "stages_completed": completed,
    }


async def run_copywriting(state: CampaignState) -> dict:
    agent = CopywritingAgent()
    campaign_id = state.get("campaign_id")

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_STARTED,
            agent=agent.name, pod=agent.pod, stage="copywriting",
        )

    try:
        result = await agent.run(
            input_data=state["brief"],
            context={
                "brand_strategy": state.get("brand_strategy", {}),
                "brand_guidelines": state.get("brand_guidelines", {}),
            },
        )
    except Exception as e:
        logger.error(f"Copywriting agent failed: {e}")
        if campaign_id:
            await event_publisher.publish(
                campaign_id, EventType.AGENT_FAILED,
                agent=agent.name, pod=agent.pod, stage="copywriting",
                data={"error": str(e)},
            )
        return {"error": str(e)}

    if campaign_id:
        headline_count = len(result.get("headlines", []))
        await event_publisher.publish(
            campaign_id, EventType.AGENT_COMPLETED,
            agent=agent.name, pod=agent.pod, stage="copywriting",
            data={"headlines_generated": headline_count},
        )

    return {"ad_copy": result, "current_stage": "copywriting"}


async def run_visual_creative(state: CampaignState) -> dict:
    agent = VisualCreativeAgent()
    campaign_id = state.get("campaign_id")

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.AGENT_STARTED,
            agent=agent.name, pod=agent.pod, stage="visual_creative",
        )

    try:
        result = await agent.run(
            input_data=state["brief"],
            context={
                "brand_strategy": state.get("brand_strategy", {}),
                "ad_copy": state.get("ad_copy", {}),
                "brand_guidelines": state.get("brand_guidelines", {}),
            },
        )
    except Exception as e:
        logger.error(f"Visual creative agent failed: {e}")
        if campaign_id:
            await event_publisher.publish(
                campaign_id, EventType.AGENT_FAILED,
                agent=agent.name, pod=agent.pod, stage="visual_creative",
                data={"error": str(e)},
            )
        return {"error": str(e)}

    if campaign_id:
        concept_count = len(result.get("creative_concepts", []))
        await event_publisher.publish(
            campaign_id, EventType.AGENT_COMPLETED,
            agent=agent.name, pod=agent.pod, stage="visual_creative",
            data={"concepts_generated": concept_count},
        )

    return {"visual_creative": result, "current_stage": "visual_creative"}


async def merge_creative_outputs(state: CampaignState) -> dict:
    """Merge node after parallel creative agents. Marks creative stage done."""
    campaign_id = state.get("campaign_id")
    completed = list(state.get("stages_completed", []))
    completed.extend(["copywriting", "visual_creative"])

    if campaign_id:
        await event_publisher.publish(
            campaign_id, EventType.STAGE_COMPLETED,
            stage="creative", progress=100,
            data={"message": "All creative assets generated"},
        )

    return {"stages_completed": completed, "current_stage": "creative_complete"}


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def build_campaign_graph() -> StateGraph:
    """Construct the LangGraph DAG for brief-to-campaign pipeline.

    Flow:
        market_research → brand_strategy ─┬─ copywriting ──────┬─ merge → END
                                          └─ visual_creative ──┘
    """
    graph = StateGraph(CampaignState)

    # Add nodes
    graph.add_node("market_research", run_market_research)
    graph.add_node("brand_strategy", run_brand_strategy)
    graph.add_node("copywriting", run_copywriting)
    graph.add_node("visual_creative", run_visual_creative)
    graph.add_node("merge_creative", merge_creative_outputs)

    # Sequential: strategy phase
    graph.set_entry_point("market_research")
    graph.add_edge("market_research", "brand_strategy")

    # Parallel: creative phase — both fan out from brand_strategy
    graph.add_edge("brand_strategy", "copywriting")
    graph.add_edge("brand_strategy", "visual_creative")

    # Fan-in: both creative nodes merge
    graph.add_edge("copywriting", "merge_creative")
    graph.add_edge("visual_creative", "merge_creative")

    # Done
    graph.add_edge("merge_creative", END)

    return graph


# Pre-compiled graph ready for invocation
campaign_graph = build_campaign_graph().compile()
