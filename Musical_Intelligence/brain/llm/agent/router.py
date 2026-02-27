"""Smart Router — selects the optimal model based on query complexity.

Routes between fast (Haiku) and deep (Sonnet) models to optimize
cost vs quality tradeoff.

Usage:
    from Musical_Intelligence.brain.llm.agent.router import route_message
    model = route_message(message, user_tier="basic", turn_count=2)
"""

from __future__ import annotations

import re

from Musical_Intelligence.brain.llm.config import MODELS

# ── Classification Patterns ─────────────────────────────────────────

# Simple greetings and short queries → Haiku
SIMPLE_PATTERNS = [
    r"^(merhaba|selam|hey|hi|hello|günaydın|iyi\s*(akşam|gece)lar?)[\s!.]*$",
    r"^(nasılsın|naber|ne\s*var\s*ne\s*yok)[\s?!.]*$",
    r"^(teşekkür|sağ\s*ol|thanks?|thank\s*you)[\s!.]*$",
    r"^(evet|hayır|yes|no|ok|tamam|anladım)[\s!.]*$",
    r"^(göster|listele|show|list)\s+\w+$",
]

# Deep science / analysis queries → Sonnet always
DEEP_PATTERNS = [
    r"(nörobilim|neuroscience|beyin|brain|korteks|cortex)",
    r"(dopamin|serotonin|norepinefrin|opioid|nörokimya)",
    r"(tahmin\s*hatası|prediction\s*error|bayesian|bayes)",
    r"(belief|inanç|model|mechanism|mekanizma)",
    r"(analiz|analysis|karşılaştır|compare|trajektori|trajectory)",
    r"(neden|niye|nasıl|why|how\s+does|how\s+come|explain)",
    r"(brecvema|gems|itpra|idyom|pepam|mmn)",
    r"(F[1-9]|relay|kernel|C³|R³|H³)",
    r"(chills?|ürpert|frisson|groove|entrainment)",
]

# Tool use indicators → Sonnet (tool calling is better on larger models)
TOOL_PATTERNS = [
    r"(şu\s*an|right\s*now|current|mevcut)\s*(belief|boyut|dimension|durum|state)",
    r"(analiz\s*et|analyze|yorumla|interpret)",
    r"(son\s*seans|last\s*session|önceki|previous|karşılaştır|compare)",
    r"(öner|recommend|tavsiye|suggest)",
]


def _matches_any(text: str, patterns: list[str]) -> bool:
    """Check if text matches any pattern (case-insensitive)."""
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


# ── Router ──────────────────────────────────────────────────────────


def route_message(
    message: str,
    user_tier: str = "free",
    turn_count: int = 0,
    has_analysis_data: bool = False,
) -> str:
    """Select the optimal model for a user message.

    Routing logic:
      1. Simple greetings in early turns → Haiku (fast, cheap)
      2. Premium/Research tier → always Sonnet (quality matters)
      3. Deep science questions → Sonnet
      4. Tool use needed → Sonnet (better tool calling)
      5. Default for short messages → Haiku
      6. Default for longer messages → Sonnet

    Args:
        message: User's message text.
        user_tier: Subscription tier (free/basic/premium/research).
        turn_count: Number of turns in current conversation.
        has_analysis_data: Whether real-time MI data is available.

    Returns:
        Model identifier string.
    """
    text = message.strip()

    # 1. Premium/Research users always get Sonnet (quality matters)
    if user_tier in ("premium", "research"):
        return MODELS["deep"]

    # 2. Simple greetings in early conversation → Haiku
    if turn_count < 3 and _matches_any(text, SIMPLE_PATTERNS):
        return MODELS["fast"]

    # 3. Deep science questions → Sonnet
    if _matches_any(text, DEEP_PATTERNS):
        return MODELS["deep"]

    # 4. Tool use indicators → Sonnet
    if _matches_any(text, TOOL_PATTERNS) or has_analysis_data:
        return MODELS["deep"]

    # 5. Short messages (< 20 chars) → Haiku
    if len(text) < 20:
        return MODELS["fast"]

    # 6. Medium-length messages → depends on turn depth
    if turn_count < 5:
        return MODELS["fast"]

    # 7. Deep conversation (many turns) → Sonnet
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
        MODELS["primary"]: (3.0, 15.0),
        MODELS["deep"]: (3.0, 15.0),
        MODELS["fast"]: (0.80, 4.0),
    }
    input_price, output_price = prices.get(model, (3.0, 15.0))
    return (input_tokens * input_price + output_tokens * output_price) / 1_000_000
