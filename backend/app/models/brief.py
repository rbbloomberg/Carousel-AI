"""Campaign brief model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, ForeignKey, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Brief(Base):
    __tablename__ = "briefs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False, index=True)

    # Core brief info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    campaign_objective: Mapped[str] = mapped_column(Text, nullable=False)
    target_audience: Mapped[dict] = mapped_column(JSONB, default=dict)
    budget_total: Mapped[float] = mapped_column(Float, default=0.0)
    budget_duration_days: Mapped[int] = mapped_column(Integer, default=30)
    platforms: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    kpis: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    brand_voice: Mapped[str] = mapped_column(Text, nullable=True)
    reference_examples: Mapped[dict] = mapped_column(JSONB, default=dict)
    constraints: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Status
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)  # draft|submitted|in_progress|completed

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    client: Mapped["Client"] = relationship(back_populates="briefs")
    campaign: Mapped["Campaign | None"] = relationship(back_populates="brief")
