"""Meta Marketing API integration – campaign creation."""

from __future__ import annotations

import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)

META_API_BASE = "https://graph.facebook.com/v19.0"


class MetaAdsClient:
    """Thin wrapper around Meta Marketing API. Falls back to mock in dev."""

    def __init__(self):
        self.live = settings.has_meta_credentials
        if not self.live:
            logger.warning("Meta Ads credentials not set – using mock client")

    async def create_campaign(
        self,
        *,
        ad_account_id: str,
        name: str,
        objective: str = "OUTCOME_TRAFFIC",
        status: str = "PAUSED",
        daily_budget: int = 1000,  # in cents
    ) -> dict:
        if not self.live:
            return self._mock_create_campaign(name)

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{META_API_BASE}/act_{ad_account_id}/campaigns",
                params={"access_token": settings.meta_access_token},
                json={
                    "name": name,
                    "objective": objective,
                    "status": status,
                    "special_ad_categories": [],
                    "daily_budget": daily_budget,
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def create_ad_set(
        self,
        *,
        ad_account_id: str,
        campaign_id: str,
        name: str,
        targeting: dict,
        daily_budget: int = 1000,
        billing_event: str = "IMPRESSIONS",
        optimization_goal: str = "LINK_CLICKS",
    ) -> dict:
        if not self.live:
            return {"id": "mock_adset_123", "name": name}

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{META_API_BASE}/act_{ad_account_id}/adsets",
                params={"access_token": settings.meta_access_token},
                json={
                    "campaign_id": campaign_id,
                    "name": name,
                    "targeting": targeting,
                    "daily_budget": daily_budget,
                    "billing_event": billing_event,
                    "optimization_goal": optimization_goal,
                    "status": "PAUSED",
                },
            )
            resp.raise_for_status()
            return resp.json()

    async def create_ad_creative(
        self,
        *,
        ad_account_id: str,
        name: str,
        page_id: str,
        headline: str,
        body: str,
        link_url: str,
        image_url: str | None = None,
    ) -> dict:
        if not self.live:
            return {"id": "mock_creative_123", "name": name}

        object_story_spec = {
            "page_id": page_id,
            "link_data": {
                "message": body,
                "link": link_url,
                "name": headline,
            },
        }
        if image_url:
            object_story_spec["link_data"]["picture"] = image_url

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{META_API_BASE}/act_{ad_account_id}/adcreatives",
                params={"access_token": settings.meta_access_token},
                json={"name": name, "object_story_spec": object_story_spec},
            )
            resp.raise_for_status()
            return resp.json()

    def _mock_create_campaign(self, name: str) -> dict:
        return {
            "id": "mock_campaign_456",
            "name": name,
            "status": "PAUSED",
            "objective": "OUTCOME_TRAFFIC",
            "_mock": True,
        }


meta_ads_client = MetaAdsClient()
