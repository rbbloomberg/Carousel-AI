"""Creative asset model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, ForeignKey, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False, index=True)

    asset_type: Mapped[str] = mapped_column(String(32), nullable=False)  # image|video|copy|landing_page
    file_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    content: Mapped[dict] = mapped_column(JSONB, default=dict)  # For copy assets: {"headline": "...", "body": "..."}
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict)  # dimensions, format, platform, variation
    generated_by_agent: Mapped[str] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="draft", index=True)  # draft|approved|live|archived
    performance_metrics: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    campaign: Mapped["Campaign"] = relationship(back_populates="assets")
