"""Agent unit tests – mock LLM responses."""

import pytest

from app.agents.strategy.market_research import MarketResearchAgent
from app.agents.strategy.brand_strategy import BrandStrategyAgent
from app.agents.creative.copywriting import CopywritingAgent
from app.agents.creative.visual_creative import VisualCreativeAgent


@pytest.mark.asyncio
async def test_market_research_agent():
    agent = MarketResearchAgent()
    result = await agent.run(
        input_data={
            "title": "Test Campaign",
            "campaign_objective": "Brand Awareness",
            "target_audience": {"interests": ["technology"]},
            "budget_total": 5000,
        }
    )
    # Mock LLM returns structured data
    assert "market_analysis" in result or "response" in result


@pytest.mark.asyncio
async def test_brand_strategy_agent():
    agent = BrandStrategyAgent()
    result = await agent.run(
        input_data={"title": "Test", "campaign_objective": "Sales"},
        context={"market_research": {"recommendations": "Focus on video"}},
    )
    assert "positioning" in result or "response" in result


@pytest.mark.asyncio
async def test_copywriting_agent():
    agent = CopywritingAgent()
    result = await agent.run(
        input_data={"title": "Test", "campaign_objective": "Traffic"},
        context={"brand_strategy": {"tone_of_voice": "Professional"}},
    )
    assert "headlines" in result or "response" in result


@pytest.mark.asyncio
async def test_visual_creative_agent():
    agent = VisualCreativeAgent()
    result = await agent.run(
        input_data={"title": "Test", "campaign_objective": "Awareness"},
        context={"brand_strategy": {"creative_direction": {"visual_style": "Modern"}}},
    )
    assert "creative_concepts" in result or "response" in result
