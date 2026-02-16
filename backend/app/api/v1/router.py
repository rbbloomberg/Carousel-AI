"""V1 API router – aggregates all sub-routers."""

from fastapi import APIRouter

from app.api.v1 import auth, briefs, campaigns, agents

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(briefs.router, prefix="/briefs", tags=["briefs"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(agents.router, prefix="/agents", tags=["agents"])
