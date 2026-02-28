"""Smart Router — selects the model for agent requests.

Currently all traffic routes to Haiku 4.5 for cost efficiency.

Usage:
    from Musical_Intelligence.brain.llm.agent.router import route_message
    model = route_message(message, user_tier="basic", turn_count=2)
"""

from __future__ import annotations

from Musical_Intelligence.brain.llm.config import MODELS


# ── Router ──────────────────────────────────────────────────────────


def route_message(
    message: str,
    user_tier: str = "free",
    turn_count: int = 0,
    has_analysis_data: bool = False,
) -> str:
    """Select the model for a user message.

    All tiers use Haiku 4.5 — no Sonnet routing.

    Args:
        message: User's message text.
        user_tier: Subscription tier (free/basic/premium/research).
        turn_count: Number of turns in current conversation.
        has_analysis_data: Whether real-time MI data is available.

    Returns:
        Model identifier string (always Haiku).
    """
    return MODELS["primary"]


def estimate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
) -> float:
    """Estimate API call cost in USD.

    Prices as of 2026 (approximate):
      Sonnet 4.5: $3/$15 per 1M tokens (input/output)
      Haiku 4.5:  $0.80/$4 per 1M tokens (input/output)
    """
    prices = {
        "claude-sonnet-4-5-20250929": (3.0, 15.0),
        "claude-haiku-4-5-20251001": (0.80, 4.0),
    }
    input_price, output_price = prices.get(model, (0.80, 4.0))
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000
