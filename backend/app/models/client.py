"""Client (company/account) model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str] = mapped_column(String(128), nullable=True)
    subscription_tier: Mapped[str] = mapped_column(String(32), default="starter")  # starter|professional|enterprise
    active_assets_limit: Mapped[int] = mapped_column(Integer, default=10)
    current_active_assets: Mapped[int] = mapped_column(Integer, default=0)
    brand_guidelines: Mapped[dict] = mapped_column(JSONB, default=dict)
    connected_platforms: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[list["User"]] = relationship(back_populates="client")
    briefs: Mapped[list["Brief"]] = relationship(back_populates="client")
    campaigns: Mapped[list["Campaign"]] = relationship(back_populates="client")
