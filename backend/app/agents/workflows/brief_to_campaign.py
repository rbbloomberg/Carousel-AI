"""LangGraph workflow: Brief → Strategy → Creative → Approval.

This is the core MVP pipeline that takes a submitted brief through
the Strategy & Insights pod and CX & Creative pod, producing a
campaign ready for client approval and Meta Ads launch.
"""

from __future__ import annotations

import logging
from typing import TypedDict

from langgraph.graph import END, StateGraph

from app.agents.strategy.market_research import MarketResearchAgent
from app.agents.strategy.brand_strategy import BrandStrategyAgent
from app.agents.creative.copywriting import CopywritingAgent
from app.agents.creative.visual_creative import VisualCreativeAgent

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# State schema – flows through every node
# ---------------------------------------------------------------------------

class CampaignState(TypedDict, total=False):
    # Inputs
    brief: dict
    brand_guidelines: dict
    campaign_id: str

    # Strategy outputs
    market_research: dict
    brand_strategy: dict

    # Creative outputs
    ad_copy: dict
    visual_creative: dict

    # Status tracking
    current_stage: str
    error: str | None


# ---------------------------------------------------------------------------
# Node functions
# ---------------------------------------------------------------------------

async def run_market_research(state: CampaignState) -> dict:
    logger.info("Running market research agent")
    agent = MarketResearchAgent()
    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_started", {"agent": agent.name})

    result = await agent.run(
        input_data=state["brief"],
        context={"brand_guidelines": state.get("brand_guidelines", {})},
    )

    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_completed", {"agent": agent.name})

    return {"market_research": result, "current_stage": "market_research_complete"}


async def run_brand_strategy(state: CampaignState) -> dict:
    logger.info("Running brand strategy agent")
    agent = BrandStrategyAgent()
    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_started", {"agent": agent.name})

    result = await agent.run(
        input_data=state["brief"],
        context={
            "market_research": state.get("market_research", {}),
            "brand_guidelines": state.get("brand_guidelines", {}),
        },
    )

    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_completed", {"agent": agent.name})

    return {"brand_strategy": result, "current_stage": "brand_strategy_complete"}


async def run_copywriting(state: CampaignState) -> dict:
    logger.info("Running copywriting agent")
    agent = CopywritingAgent()
    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_started", {"agent": agent.name})

    result = await agent.run(
        input_data=state["brief"],
        context={
            "brand_strategy": state.get("brand_strategy", {}),
            "brand_guidelines": state.get("brand_guidelines", {}),
        },
    )

    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_completed", {"agent": agent.name})

    return {"ad_copy": result, "current_stage": "copywriting_complete"}


async def run_visual_creative(state: CampaignState) -> dict:
    logger.info("Running visual creative agent")
    agent = VisualCreativeAgent()
    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_started", {"agent": agent.name})

    result = await agent.run(
        input_data=state["brief"],
        context={
            "brand_strategy": state.get("brand_strategy", {}),
            "ad_copy": state.get("ad_copy", {}),
            "brand_guidelines": state.get("brand_guidelines", {}),
        },
    )

    if state.get("campaign_id"):
        await agent.emit_event(state["campaign_id"], "agent_completed", {"agent": agent.name})

    return {"visual_creative": result, "current_stage": "visual_creative_complete"}


# ---------------------------------------------------------------------------
# Build the graph
# ---------------------------------------------------------------------------

def build_campaign_graph() -> StateGraph:
    """Construct the LangGraph DAG for brief-to-campaign pipeline.

    Flow:
        market_research → brand_strategy → copywriting → visual_creative → END
    """
    graph = StateGraph(CampaignState)

    # Add nodes
    graph.add_node("market_research", run_market_research)
    graph.add_node("brand_strategy", run_brand_strategy)
    graph.add_node("copywriting", run_copywriting)
    graph.add_node("visual_creative", run_visual_creative)

    # Define edges (linear MVP pipeline)
    graph.set_entry_point("market_research")
    graph.add_edge("market_research", "brand_strategy")
    graph.add_edge("brand_strategy", "copywriting")
    graph.add_edge("copywriting", "visual_creative")
    graph.add_edge("visual_creative", END)

    return graph


# Pre-compiled graph ready for invocation
campaign_graph = build_campaign_graph().compile()
