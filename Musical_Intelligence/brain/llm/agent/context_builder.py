"""Full 6-Layer Context Builder — assembles the complete system prompt.

Combines all layers:
  Layer 0: Persona (identity, guardrails)
  Layer 1: User Profile (persona, genes, tier)
  Layer 2: Vocabulary (M3-LOGOS terms, tier gates)
  Layer 2.5: Interpretation Guide (always-on analysis framework)
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

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import CONTEXT_BUDGET, KNOWLEDGE_DIR, TIERS
from Musical_Intelligence.brain.llm.processing.context_builder import (
    build_layer0,
    build_layer1,
    build_layer2,
    estimate_tokens,
)


# ── Layer 2.5 Cache ──────────────────────────────────────────────

_GUIDE_CACHE: dict[str, dict[str, str]] | None = None

_GUIDE_KEYS = [
    "system_identity",
    "scientific_methodology",
    "key_references",
    "interpreting_6d",
    "interpreting_functions",
    "interpreting_notable_beliefs",
    "neurochemicals_meaning",
    "reward_formula",
]


def _load_guide_entries() -> dict[str, dict[str, str]]:
    """Load the 5 critical interpretation guide entries from analysis_guide.jsonl."""
    global _GUIDE_CACHE
    if _GUIDE_CACHE is not None:
        return _GUIDE_CACHE

    entries: dict[str, dict[str, str]] = {}
    guide_path = KNOWLEDGE_DIR / "analysis_guide.jsonl"
    if guide_path.exists():
        for line in guide_path.read_text(encoding="utf-8").strip().splitlines():
            if not line.strip():
                continue
            entry = json.loads(line)
            key = entry.get("key", "")
            if key in _GUIDE_KEYS:
                entries[key] = entry

    _GUIDE_CACHE = entries
    return entries

# ── Layer 2.5: Interpretation Guide ──────────────────────────────────


def build_layer2_5(language: str = "tr") -> str:
    """Build the always-on interpretation guide layer.

    Embeds 5 critical analysis framework entries directly in the system
    prompt so the agent always has interpretation context — independent
    of RAG retrieval quality.

    Entries:
        - interpreting_6d: How to read the 6 psychology dimensions
        - interpreting_functions: How to compare F1-F9 activations
        - interpreting_notable_beliefs: Cross-function belief patterns
        - neurochemicals_meaning: DA/NE/OPI/5HT channels
        - reward_formula: Reward decomposition (surprise/resolution/exploration/monotony)

    Returns:
        Formatted interpretation guide string.
    """
    entries = _load_guide_entries()
    if not entries:
        return ""

    sfx = "tr" if language == "tr" else "en"
    header = "## Yorum Rehberi" if language == "tr" else "## Interpretation Guide"

    section_titles = {
        "system_identity": ("Sistem Kimliği", "System Identity"),
        "scientific_methodology": ("Bilimsel Metodoloji", "Scientific Methodology"),
        "key_references": ("Temel Kaynaklar", "Key References"),
        "interpreting_6d": ("6D Boyutları Okuma", "Reading 6D Dimensions"),
        "interpreting_functions": ("F1-F9 Fonksiyon Karşılaştırma", "Comparing F1-F9 Functions"),
        "interpreting_notable_beliefs": ("İnanç Örüntüleri", "Belief Patterns"),
        "neurochemicals_meaning": ("Nörokimyasallar", "Neurochemicals"),
        "reward_formula": ("Ödül Formülü", "Reward Formula"),
    }

    parts = [header]
    budget = CONTEXT_BUDGET.get("interpretation_guide", 1200)
    total_tokens = 0

    for key in _GUIDE_KEYS:
        entry = entries.get(key)
        if not entry:
            continue

        text = entry.get(f"what_{sfx}", entry.get("what_en", ""))
        if not text:
            continue

        tokens = estimate_tokens(text)
        if total_tokens + tokens > budget:
            break

        title_tr, title_en = section_titles.get(key, (key, key))
        title = title_tr if language == "tr" else title_en
        parts.append(f"\n### {title}\n{text}")
        total_tokens += tokens

    return "\n".join(parts) if len(parts) > 1 else ""


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

    Layers assembled:
        0: Persona identity + guardrails
        1: User profile (persona, genes, tier)
        2: M3-LOGOS vocabulary + tier gates
        2.5: Interpretation guide (always-on analysis framework)
        3: Knowledge RAG (dynamic, per-query)
        4: Literature RAG (premium+ only)

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

    # Layer 2.5: Interpretation guide (always-on, not RAG-dependent)
    layer2_5 = build_layer2_5(language)
    if layer2_5:
        static_context += f"\n\n---\n\n{layer2_5}"

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
