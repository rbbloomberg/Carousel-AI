"""Campaign endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.campaign import Campaign
from app.models.task import AgentTask
from app.api.deps import get_current_user
from app.schemas.campaign import CampaignResponse, CampaignListItem, TaskResponse

router = APIRouter()


@router.get("", response_model=list[CampaignListItem])
async def list_campaigns(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.client_id == user.client_id).order_by(Campaign.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{campaign_id}", response_model=CampaignResponse)
async def get_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.client_id == user.client_id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign


@router.post("/{campaign_id}/approve", response_model=CampaignResponse)
async def approve_campaign(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Client approves creative, triggering media buying."""
    result = await db.execute(
        select(Campaign).where(Campaign.id == campaign_id, Campaign.client_id == user.client_id)
    )
    campaign = result.scalar_one_or_none()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign.status != "approval":
        raise HTTPException(status_code=400, detail=f"Campaign is in '{campaign.status}' state, not awaiting approval")

    campaign.status = "live"
    await db.commit()
    await db.refresh(campaign)

    # Trigger Meta Ads campaign creation via Celery
    from app.agents.tasks import launch_campaign
    launch_campaign.delay(str(campaign.id))

    return campaign


@router.get("/{campaign_id}/tasks", response_model=list[TaskResponse])
async def get_campaign_tasks(
    campaign_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(AgentTask).where(AgentTask.campaign_id == campaign_id).order_by(AgentTask.created_at)
    )
    return result.scalars().all()
