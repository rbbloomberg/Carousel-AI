"""Agent orchestration & SSE streaming endpoints."""

import asyncio
import json
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
import redis.asyncio as aioredis

from app.config import settings
from app.models.user import User
from app.api.deps import get_current_user
from app.services.events import event_publisher, PIPELINE_STAGES

router = APIRouter()


async def _event_generator(
    request: Request, campaign_id: str
) -> AsyncGenerator[dict, None]:
    """Yield SSE events: first replay stored log, then stream live."""
    channel = f"campaign:{campaign_id}:events"

    # 1. Replay stored events so late-joining clients see full history
    stored = await event_publisher.get_event_log(campaign_id)
    for event in stored:
        yield {"event": "agent_update", "data": json.dumps(event)}

    # 2. Stream live events from Redis pub/sub
    r = aioredis.from_url(settings.redis_url)
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)
    try:
        while True:
            if await request.is_disconnected():
                break
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message and message["type"] == "message":
                yield {"event": "agent_update", "data": message["data"].decode()}
            await asyncio.sleep(0.1)
    finally:
        await pubsub.unsubscribe(channel)
        await r.aclose()


@router.get("/stream/{campaign_id}")
async def stream_campaign_events(
    campaign_id: str,
    request: Request,
    user: User = Depends(get_current_user),
):
    """SSE endpoint – streams real-time agent updates for a campaign.

    Late-joining clients receive the full event log first, then live updates.
    """
    return EventSourceResponse(_event_generator(request, campaign_id))


@router.get("/stages")
async def get_pipeline_stages(user: User = Depends(get_current_user)):
    """Return the pipeline stage definitions (for progress UI)."""
    return {"stages": PIPELINE_STAGES}
