"""Agent orchestration & SSE streaming endpoints."""

import asyncio
import json

from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse
import redis.asyncio as aioredis

from app.config import settings
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()


async def _event_generator(request: Request, channel: str):
    """Yield SSE events from a Redis pub/sub channel."""
    r = aioredis.from_url(settings.redis_url)
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)
    try:
        while True:
            if await request.is_disconnected():
                break
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
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
    """SSE endpoint – streams real-time agent updates for a campaign."""
    channel = f"campaign:{campaign_id}:events"
    return EventSourceResponse(_event_generator(request, channel))
