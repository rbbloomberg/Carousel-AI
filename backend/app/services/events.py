"""Real-time event publishing service for campaign pipeline tracking."""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from enum import Enum

import redis.asyncio as aioredis

from app.config import settings

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    PIPELINE_STARTED = "pipeline_started"
    PIPELINE_COMPLETED = "pipeline_completed"
    PIPELINE_FAILED = "pipeline_failed"
    STAGE_STARTED = "stage_started"
    STAGE_COMPLETED = "stage_completed"
    AGENT_STARTED = "agent_started"
    AGENT_PROGRESS = "agent_progress"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    APPROVAL_REQUESTED = "approval_requested"
    CAMPAIGN_LAUNCHED = "campaign_launched"


# Stage definitions for progress tracking
PIPELINE_STAGES = [
    {"key": "market_research", "label": "Market Research", "pod": "strategy_insights"},
    {"key": "brand_strategy", "label": "Brand Strategy", "pod": "strategy_insights"},
    {"key": "copywriting", "label": "Ad Copywriting", "pod": "cx_creative"},
    {"key": "visual_creative", "label": "Visual Creative", "pod": "cx_creative"},
]


class EventPublisher:
    """Publishes real-time events to Redis pub/sub for SSE consumption."""

    async def publish(
        self,
        campaign_id: str,
        event_type: EventType,
        *,
        agent: str | None = None,
        pod: str | None = None,
        stage: str | None = None,
        data: dict | None = None,
        progress: float | None = None,
    ) -> None:
        event = {
            "event_type": event_type.value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "campaign_id": campaign_id,
        }
        if agent:
            event["agent"] = agent
        if pod:
            event["pod"] = pod
        if stage:
            event["stage"] = stage
            # Calculate overall progress percentage
            stage_keys = [s["key"] for s in PIPELINE_STAGES]
            if stage in stage_keys:
                idx = stage_keys.index(stage)
                if event_type in (EventType.STAGE_COMPLETED, EventType.AGENT_COMPLETED):
                    event["progress"] = round((idx + 1) / len(stage_keys) * 100)
                else:
                    event["progress"] = round(idx / len(stage_keys) * 100)
        if progress is not None:
            event["progress"] = progress
        if data:
            event["data"] = data

        channel = f"campaign:{campaign_id}:events"
        r = aioredis.from_url(settings.redis_url)
        try:
            await r.publish(channel, json.dumps(event))
            # Also store in a list for clients that connect after events fire
            await r.rpush(f"campaign:{campaign_id}:event_log", json.dumps(event))
            await r.expire(f"campaign:{campaign_id}:event_log", 86400)  # 24h TTL
        finally:
            await r.aclose()

    async def get_event_log(self, campaign_id: str) -> list[dict]:
        """Retrieve stored events for a campaign (for late-joining clients)."""
        r = aioredis.from_url(settings.redis_url)
        try:
            raw = await r.lrange(f"campaign:{campaign_id}:event_log", 0, -1)
            return [json.loads(item) for item in raw]
        finally:
            await r.aclose()


event_publisher = EventPublisher()
