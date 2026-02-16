"""Initial schema – all core MVP tables.

Revision ID: 001
Revises: None
Create Date: 2026-02-16
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── clients ───────────────────────────────────────────────────────
    op.create_table(
        "clients",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("company_name", sa.String(255), nullable=False),
        sa.Column("industry", sa.String(128), nullable=True),
        sa.Column("subscription_tier", sa.String(32), server_default="starter"),
        sa.Column("active_assets_limit", sa.Integer, server_default="10"),
        sa.Column("current_active_assets", sa.Integer, server_default="0"),
        sa.Column("brand_guidelines", JSONB, server_default="{}"),
        sa.Column("connected_platforms", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── users ─────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("client_id", UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

    # ── briefs ────────────────────────────────────────────────────────
    op.create_table(
        "briefs",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("client_id", UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("campaign_objective", sa.Text, nullable=False),
        sa.Column("target_audience", JSONB, server_default="{}"),
        sa.Column("budget_total", sa.Float, server_default="0"),
        sa.Column("budget_duration_days", sa.Integer, server_default="30"),
        sa.Column("platforms", ARRAY(sa.String), server_default="{}"),
        sa.Column("kpis", ARRAY(sa.String), server_default="{}"),
        sa.Column("brand_voice", sa.Text, nullable=True),
        sa.Column("reference_examples", JSONB, server_default="{}"),
        sa.Column("constraints", JSONB, server_default="{}"),
        sa.Column("status", sa.String(32), server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_briefs_client_id", "briefs", ["client_id"])
    op.create_index("ix_briefs_status", "briefs", ["status"])

    # ── campaigns ─────────────────────────────────────────────────────
    op.create_table(
        "campaigns",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("brief_id", UUID(as_uuid=True), sa.ForeignKey("briefs.id"), nullable=False, unique=True),
        sa.Column("client_id", UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("status", sa.String(32), server_default="planning"),
        sa.Column("platform_data", JSONB, server_default="{}"),
        sa.Column("impressions", sa.Integer, server_default="0"),
        sa.Column("clicks", sa.Integer, server_default="0"),
        sa.Column("conversions", sa.Integer, server_default="0"),
        sa.Column("spend", sa.Float, server_default="0"),
        sa.Column("roas", sa.Float, server_default="0"),
        sa.Column("strategy_output", JSONB, server_default="{}"),
        sa.Column("creative_output", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("launched_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_campaigns_client_id", "campaigns", ["client_id"])
    op.create_index("ix_campaigns_status", "campaigns", ["status"])

    # ── assets ────────────────────────────────────────────────────────
    op.create_table(
        "assets",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("campaign_id", UUID(as_uuid=True), sa.ForeignKey("campaigns.id"), nullable=False),
        sa.Column("asset_type", sa.String(32), nullable=False),
        sa.Column("file_url", sa.String(1024), nullable=True),
        sa.Column("content", JSONB, server_default="{}"),
        sa.Column("metadata", JSONB, server_default="{}"),
        sa.Column("generated_by_agent", sa.String(128), nullable=True),
        sa.Column("status", sa.String(32), server_default="draft"),
        sa.Column("performance_metrics", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_assets_campaign_id", "assets", ["campaign_id"])
    op.create_index("ix_assets_status", "assets", ["status"])

    # ── agent_tasks ───────────────────────────────────────────────────
    op.create_table(
        "agent_tasks",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("campaign_id", UUID(as_uuid=True), sa.ForeignKey("campaigns.id"), nullable=False),
        sa.Column("assigned_to_pod", sa.String(64), nullable=False),
        sa.Column("assigned_to_agent", sa.String(128), nullable=False),
        sa.Column("task_type", sa.String(64), nullable=False),
        sa.Column("input_data", JSONB, server_default="{}"),
        sa.Column("output_data", JSONB, server_default="{}"),
        sa.Column("error", sa.Text, nullable=True),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("dependencies", ARRAY(UUID(as_uuid=True)), server_default="{}"),
        sa.Column("priority", sa.Integer, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_agent_tasks_campaign_id", "agent_tasks", ["campaign_id"])
    op.create_index("ix_agent_tasks_status", "agent_tasks", ["status"])

    # ── agent_messages ────────────────────────────────────────────────
    op.create_table(
        "agent_messages",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("campaign_id", UUID(as_uuid=True), nullable=False),
        sa.Column("from_agent", sa.String(128), nullable=False),
        sa.Column("to_agent", sa.String(128), nullable=False),
        sa.Column("to_pod", sa.String(64), nullable=False),
        sa.Column("message_type", sa.String(32), nullable=False),
        sa.Column("payload", JSONB, server_default="{}"),
        sa.Column("context", JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_agent_messages_campaign_id", "agent_messages", ["campaign_id"])

    # ── platform_credentials ──────────────────────────────────────────
    op.create_table(
        "platform_credentials",
        sa.Column("id", UUID(as_uuid=True), primary_key=True),
        sa.Column("client_id", UUID(as_uuid=True), sa.ForeignKey("clients.id"), nullable=False),
        sa.Column("platform", sa.String(32), nullable=False),
        sa.Column("access_token_encrypted", sa.Text, nullable=False),
        sa.Column("refresh_token_encrypted", sa.Text, nullable=True),
        sa.Column("token_expires_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("account_id", sa.String(128), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_platform_credentials_client_id", "platform_credentials", ["client_id"])


def downgrade() -> None:
    op.drop_table("platform_credentials")
    op.drop_table("agent_messages")
    op.drop_table("agent_tasks")
    op.drop_table("assets")
    op.drop_table("campaigns")
    op.drop_table("briefs")
    op.drop_table("users")
    op.drop_table("clients")
