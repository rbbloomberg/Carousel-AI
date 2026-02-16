"""Base agent class – all pod agents inherit from this."""

from __future__ import annotations

import json
import logging
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timezone

import redis.asyncio as aioredis

from app.config import settings
from app.integrations.llm import llm_client

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """Abstract base for every agent in the platform.

    Subclasses must implement:
      - name: human-readable agent name
      - pod: which pod this agent belongs to
      - system_prompt: the system prompt defining agent role
      - run(): the core execution logic
    """

    name: str = "base_agent"
    pod: str = "unknown"
    system_prompt: str = ""

    def __init__(self):
        self.llm = llm_client

    async def run(self, input_data: dict, context: dict | None = None) -> dict:
        """Execute the agent's task. Override in subclasses for custom logic."""
        user_prompt = self._build_user_prompt(input_data, context)
        result = await self.llm.generate_json(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )
        return result

    def _build_user_prompt(self, input_data: dict, context: dict | None = None) -> str:
        """Build the user message from input data and context."""
        parts = []
        if context:
            parts.append(f"CONTEXT:\n{json.dumps(context, indent=2)}")
        parts.append(f"INPUT:\n{json.dumps(input_data, indent=2)}")
        return "\n\n".join(parts)

    async def emit_event(self, campaign_id: str, event_type: str, data: dict) -> None:
        """Publish a real-time event to the campaign's SSE channel."""
        r = aioredis.from_url(settings.redis_url)
        event = json.dumps({
            "event_type": event_type,
            "agent": self.name,
            "pod": self.pod,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        })
        await r.publish(f"campaign:{campaign_id}:events", event)
        await r.aclose()
