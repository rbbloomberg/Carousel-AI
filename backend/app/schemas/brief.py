"""Brief request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class TargetAudience(BaseModel):
    demographics: dict = {}
    interests: list[str] = []
    behaviors: list[str] = []


class BriefCreate(BaseModel):
    title: str
    campaign_objective: str
    target_audience: TargetAudience = TargetAudience()
    budget_total: float = 0.0
    budget_duration_days: int = 30
    platforms: list[str] = ["meta"]
    kpis: list[str] = []
    brand_voice: str | None = None
    reference_examples: dict = {}
    constraints: dict = {}


class BriefUpdate(BaseModel):
    title: str | None = None
    campaign_objective: str | None = None
    target_audience: TargetAudience | None = None
    budget_total: float | None = None
    budget_duration_days: int | None = None
    platforms: list[str] | None = None
    kpis: list[str] | None = None
    brand_voice: str | None = None
    status: str | None = None


class BriefResponse(BaseModel):
    id: str
    client_id: str
    title: str
    campaign_objective: str
    target_audience: dict
    budget_total: float
    budget_duration_days: int
    platforms: list[str]
    kpis: list[str]
    brand_voice: str | None
    status: str
    created_at: datetime
    submitted_at: datetime | None

    model_config = {"from_attributes": True}
