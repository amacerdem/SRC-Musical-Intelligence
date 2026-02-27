"""Full 5-Layer Context Builder — assembles the complete system prompt.

Combines all layers:
  Layer 0: Persona (identity, guardrails)
  Layer 1: User Profile (persona, genes, tier)
  Layer 2: Vocabulary (M3-LOGOS terms, tier gates)
  Layer 3: Knowledge RAG (retrieved cards)
  Layer 4: Literature RAG (retrieved papers)
  Layer 5: Live Data (injected via tool results, not built here)

Usage:
    from Musical_Intelligence.brain.llm.agent.context_builder import build_full_context

    system_prompt, messages = build_full_context(
        user_message="Neden bazı şarkılar ürperti veriyor?",
        user_profile=profile,
        language="tr",
    )
"""

from __future__ import annotations

from typing import Any

from Musical_Intelligence.brain.llm.config import CONTEXT_BUDGET, TIERS
from Musical_Intelligence.brain.llm.processing.context_builder import (
    build_layer0,
    build_layer1,
    build_layer2,
    estimate_tokens,
)

# ── Layer 3: Knowledge RAG ──────────────────────────────────────────


def build_layer3(
    query: str,
    user_tier: str = "free",
    max_tokens: int | None = None,
    use_local_embeddings: bool = False,
) -> str:
    """Retrieve relevant knowledge cards for the user's query.

    Args:
        query: User's message text.
        user_tier: Subscription tier for filtering.
        max_tokens: Token budget for this layer.
        use_local_embeddings: Use hash-based embeddings (dev).

    Returns:
        Formatted knowledge context string.
    """
    if max_tokens is None:
        max_tokens = CONTEXT_BUDGET["knowledge_rag"]

    try:
        from Musical_Intelligence.brain.llm.rag.retriever import (
            format_results_for_prompt,
            retrieve_knowledge,
        )

        results = retrieve_knowledge(
            query=query,
            user_tier=user_tier,
            top_k=5,
            use_local_embeddings=use_local_embeddings,
        )
        if results:
            return format_results_for_prompt(results, max_tokens=max_tokens)
    except Exception:
        pass  # RAG not initialized yet

    return ""


# ── Layer 4: Literature RAG ─────────────────────────────────────────


def build_layer4(
    query: str,
    user_tier: str = "premium",
    max_tokens: int | None = None,
    use_local_embeddings: bool = False,
) -> str:
    """Retrieve relevant literature for deep questions.

    Only activated for premium+ users.

    Args:
        query: User's message text.
        user_tier: Must be "premium" or "research".
        max_tokens: Token budget for this layer.
        use_local_embeddings: Use hash-based embeddings (dev).

    Returns:
        Formatted literature context string.
    """
    if max_tokens is None:
        max_tokens = CONTEXT_BUDGET["literature_rag"]

    tier_level = {"free": 0, "basic": 1, "premium": 2, "research": 3}
    if tier_level.get(user_tier, 0) < 2:
        return ""

    try:
        from Musical_Intelligence.brain.llm.rag.retriever import (
            format_results_for_prompt,
            retrieve_literature,
        )

        results = retrieve_literature(
            query=query,
            user_tier=user_tier,
            top_k=3,
            use_local_embeddings=use_local_embeddings,
        )
        if results:
            return format_results_for_prompt(results, max_tokens=max_tokens)
    except Exception:
        pass

    return ""


# ── Full Context Assembly ───────────────────────────────────────────


def build_full_context(
    user_message: str,
    user_profile: dict[str, Any],
    language: str = "tr",
    conversation_history: list[dict[str, str]] | None = None,
    use_local_embeddings: bool = False,
) -> tuple[str, list[dict[str, str]]]:
    """Build the complete system prompt and message array.

    Args:
        user_message: The current user message.
        user_profile: User profile dict (see processing.context_builder).
        language: "tr" or "en".
        conversation_history: Previous messages in API format.
        use_local_embeddings: Use hash-based embeddings (dev).

    Returns:
        Tuple of (system_prompt, messages) ready for Claude API call.
    """
    tier = user_profile.get("tier", "free")

    # Layer 0-2: Static context (cached by API via prompt caching)
    layer0 = build_layer0(language)
    layer1 = build_layer1(user_profile, language)
    layer2 = build_layer2(tier, language)

    static_context = f"{layer0}\n\n---\n\n{layer1}\n\n---\n\n{layer2}"

    # Layer 3: Knowledge RAG (dynamic, per-query)
    layer3 = build_layer3(
        query=user_message,
        user_tier=tier,
        use_local_embeddings=use_local_embeddings,
    )

    # Layer 4: Literature RAG (premium+ only)
    layer4 = build_layer4(
        query=user_message,
        user_tier=tier,
        use_local_embeddings=use_local_embeddings,
    )

    # Assemble system prompt
    parts = [static_context]
    if layer3:
        header = "## Relevant Knowledge" if language == "en" else "## İlgili Bilgi"
        parts.append(f"\n\n---\n\n{header}\n\n{layer3}")
    if layer4:
        header = "## Literature" if language == "en" else "## Literatür"
        parts.append(f"\n\n---\n\n{header}\n\n{layer4}")

    system_prompt = "".join(parts)

    # Build messages array
    messages: list[dict[str, str]] = []
    if conversation_history:
        # Trim to budget
        max_conv_tokens = CONTEXT_BUDGET["conversation"]
        total = 0
        trimmed: list[dict[str, str]] = []
        for msg in reversed(conversation_history):
            msg_tokens = estimate_tokens(msg["content"])
            if total + msg_tokens > max_conv_tokens:
                break
            trimmed.insert(0, msg)
            total += msg_tokens
        messages.extend(trimmed)

    messages.append({"role": "user", "content": user_message})

    return system_prompt, messages


def build_api_request(
    user_message: str,
    user_profile: dict[str, Any],
    language: str = "tr",
    conversation_history: list[dict[str, str]] | None = None,
    model: str | None = None,
    use_local_embeddings: bool = False,
) -> dict[str, Any]:
    """Build a complete Claude API request body.

    Args:
        user_message: Current user message.
        user_profile: User profile dict.
        language: "tr" or "en".
        conversation_history: Previous messages.
        model: Model override (or auto-route).
        use_local_embeddings: Dev mode flag.

    Returns:
        Dict ready for anthropic.Anthropic().messages.create(**request).
    """
    from Musical_Intelligence.brain.llm.agent.router import route_message
    from Musical_Intelligence.brain.llm.agent.tools import TOOLS

    system_prompt, messages = build_full_context(
        user_message=user_message,
        user_profile=user_profile,
        language=language,
        conversation_history=conversation_history,
        use_local_embeddings=use_local_embeddings,
    )

    if model is None:
        tier = user_profile.get("tier", "free")
        turn_count = len(conversation_history) if conversation_history else 0
        model = route_message(user_message, tier, turn_count)

    return {
        "model": model,
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": messages,
        "tools": TOOLS,
    }
