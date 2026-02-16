"""Brief CRUD and submission endpoints."""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.models.brief import Brief
from app.api.deps import get_current_user
from app.schemas.brief import BriefCreate, BriefUpdate, BriefResponse

router = APIRouter()


@router.post("", response_model=BriefResponse, status_code=status.HTTP_201_CREATED)
async def create_brief(
    body: BriefCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    brief = Brief(
        client_id=user.client_id,
        title=body.title,
        campaign_objective=body.campaign_objective,
        target_audience=body.target_audience.model_dump(),
        budget_total=body.budget_total,
        budget_duration_days=body.budget_duration_days,
        platforms=body.platforms,
        kpis=body.kpis,
        brand_voice=body.brand_voice,
        reference_examples=body.reference_examples,
        constraints=body.constraints,
    )
    db.add(brief)
    await db.commit()
    await db.refresh(brief)
    return brief


@router.get("", response_model=list[BriefResponse])
async def list_briefs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Brief).where(Brief.client_id == user.client_id).order_by(Brief.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{brief_id}", response_model=BriefResponse)
async def get_brief(
    brief_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Brief).where(Brief.id == brief_id, Brief.client_id == user.client_id)
    )
    brief = result.scalar_one_or_none()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return brief


@router.put("/{brief_id}", response_model=BriefResponse)
async def update_brief(
    brief_id: str,
    body: BriefUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Brief).where(Brief.id == brief_id, Brief.client_id == user.client_id)
    )
    brief = result.scalar_one_or_none()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")

    update_data = body.model_dump(exclude_unset=True)
    if "target_audience" in update_data and update_data["target_audience"] is not None:
        update_data["target_audience"] = update_data["target_audience"].model_dump()

    for field, value in update_data.items():
        setattr(brief, field, value)

    await db.commit()
    await db.refresh(brief)
    return brief


@router.post("/{brief_id}/submit", response_model=BriefResponse)
async def submit_brief(
    brief_id: str,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Submit a brief to kick off the agent orchestration pipeline."""
    result = await db.execute(
        select(Brief).where(Brief.id == brief_id, Brief.client_id == user.client_id)
    )
    brief = result.scalar_one_or_none()
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    if brief.status != "draft":
        raise HTTPException(status_code=400, detail="Brief already submitted")

    brief.status = "submitted"
    brief.submitted_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(brief)

    # Trigger orchestration pipeline via Celery
    from app.agents.tasks import run_campaign_pipeline
    run_campaign_pipeline.delay(str(brief.id))

    return brief
