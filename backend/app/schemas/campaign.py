"""Campaign request/response schemas."""

from datetime import datetime

from pydantic import BaseModel


class CampaignResponse(BaseModel):
    id: str
    brief_id: str
    client_id: str
    name: str
    status: str
    platform_data: dict
    impressions: int
    clicks: int
    conversions: int
    spend: float
    roas: float
    strategy_output: dict
    creative_output: dict
    created_at: datetime
    launched_at: datetime | None

    model_config = {"from_attributes": True}


class CampaignListItem(BaseModel):
    id: str
    name: str
    status: str
    spend: float
    impressions: int
    clicks: int
    roas: float
    created_at: datetime

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    id: str
    campaign_id: str
    assigned_to_pod: str
    assigned_to_agent: str
    task_type: str
    status: str
    output_data: dict
    error: str | None
    created_at: datetime
    completed_at: datetime | None

    model_config = {"from_attributes": True}
