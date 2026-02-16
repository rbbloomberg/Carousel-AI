"""LLM client – wraps Anthropic Claude with a mock fallback for keyless dev."""

from __future__ import annotations

import json
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Unified interface to Claude. Falls back to mock responses when no API key is set."""

    def __init__(self):
        self._client = None
        if settings.has_anthropic_key:
            import anthropic
            self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
            logger.info("Using live Anthropic Claude API")
        else:
            logger.warning("ANTHROPIC_API_KEY not set – using mock LLM responses")

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        *,
        model: str = "claude-sonnet-4-5-20250929",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> str:
        """Generate a completion from Claude (or mock)."""
        if self._client:
            message = self._client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
            )
            return message.content[0].text

        # --- Mock fallback ---
        return self._mock_response(system_prompt, user_prompt)

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs,
    ) -> dict:
        """Generate and parse a JSON response."""
        raw = await self.generate(
            system_prompt + "\n\nRespond ONLY with valid JSON, no markdown.",
            user_prompt,
            **kwargs,
        )
        # Strip markdown fences if present
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]
            text = text.rsplit("```", 1)[0]
        return json.loads(text)

    def _mock_response(self, system_prompt: str, user_prompt: str) -> str:
        """Return deterministic mock output for development without API keys."""
        if "market research" in system_prompt.lower():
            return json.dumps({
                "market_analysis": {
                    "market_size": "$50B digital advertising market",
                    "growth_rate": "12% YoY",
                    "key_trends": [
                        "Short-form video dominance",
                        "AI-powered personalization",
                        "Privacy-first targeting",
                    ],
                    "competitor_landscape": [
                        {"name": "Competitor A", "strength": "Brand awareness", "weakness": "High CPM"},
                        {"name": "Competitor B", "strength": "Low cost", "weakness": "Poor creative"},
                    ],
                },
                "opportunities": [
                    "Underserved mobile-first audience segment",
                    "Emerging short-form video ad formats",
                ],
                "recommendations": "Focus on video-first creative with mobile optimization.",
            })

        if "brand strategy" in system_prompt.lower():
            return json.dumps({
                "positioning": "The intelligent advertising partner for growth-focused brands",
                "messaging_framework": {
                    "primary_message": "Smarter ads, faster results",
                    "supporting_messages": [
                        "AI-powered campaign optimization",
                        "From brief to live in hours, not weeks",
                    ],
                },
                "tone_of_voice": "Professional yet approachable, data-driven, confident",
                "target_personas": [
                    {"name": "Growth Marketer", "pain_points": ["Time to launch", "Budget waste"]},
                ],
            })

        if "copywriting" in system_prompt.lower():
            return json.dumps({
                "headlines": [
                    {"text": "Grow Faster with AI Ads", "platform": "meta", "character_count": 25},
                    {"text": "Your Ads, Supercharged", "platform": "meta", "character_count": 23},
                    {"text": "Stop Guessing, Start Growing", "platform": "meta", "character_count": 29},
                    {"text": "Smart Ads for Smart Brands", "platform": "meta", "character_count": 26},
                    {"text": "Results You Can See", "platform": "meta", "character_count": 19},
                ],
                "primary_text": [
                    {"text": "Launch high-performing ad campaigns in hours. AI-powered strategy and creative that delivers.", "platform": "meta"},
                    {"text": "Tired of ads that don't convert? Let AI optimize every detail for maximum ROAS.", "platform": "meta"},
                    {"text": "From brief to live campaign in under 4 hours. The future of advertising is here.", "platform": "meta"},
                ],
                "ctas": ["Learn More", "Get Started", "See Results"],
                "reasoning": "Focused on speed-to-market and results, matching growth marketer persona.",
            })

        if "visual creative" in system_prompt.lower():
            return json.dumps({
                "creative_concepts": [
                    {
                        "concept_name": "Speed & Growth",
                        "description": "Rocket/growth imagery with clean modern design",
                        "image_prompt": "Modern minimalist ad design with upward trending graph, brand colors, clean typography",
                        "format": "1080x1080",
                        "platform": "meta_feed",
                    },
                    {
                        "concept_name": "AI Intelligence",
                        "description": "Neural network / brain imagery conveying smart automation",
                        "image_prompt": "Abstract AI brain visualization with connecting nodes, professional blue tones",
                        "format": "1080x1920",
                        "platform": "meta_stories",
                    },
                ],
                "reasoning": "Two distinct concepts for A/B testing visual approaches.",
            })

        return json.dumps({
            "response": "Mock agent response — set ANTHROPIC_API_KEY for live output.",
            "note": "This is placeholder data for development.",
        })


# Singleton
llm_client = LLMClient()
