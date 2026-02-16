"""Campaign model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brief_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("briefs.id"), unique=True, nullable=False)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="planning", index=True)
    # status: planning|strategy|creative|approval|live|paused|completed

    # Platform-specific data
    platform_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    # e.g. {"meta": {"campaign_id": "...", "status": "...", "spend": 0.0}}

    # Aggregated metrics
    impressions: Mapped[int] = mapped_column(Integer, default=0)
    clicks: Mapped[int] = mapped_column(Integer, default=0)
    conversions: Mapped[int] = mapped_column(Integer, default=0)
    spend: Mapped[float] = mapped_column(Float, default=0.0)
    roas: Mapped[float] = mapped_column(Float, default=0.0)

    # Strategy & creative outputs from agents
    strategy_output: Mapped[dict] = mapped_column(JSONB, default=dict)
    creative_output: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    launched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    brief: Mapped["Brief"] = relationship(back_populates="campaign")
    client: Mapped["Client"] = relationship(back_populates="campaigns")
    assets: Mapped[list["Asset"]] = relationship(back_populates="campaign")
    tasks: Mapped[list["AgentTask"]] = relationship(back_populates="campaign")
