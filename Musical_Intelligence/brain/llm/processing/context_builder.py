"""Context Builder — Assembles Layers 0–2 of the LLM system prompt.

Layer 0: Persona (system identity, guardrails, tone)
Layer 1: User Profile (persona, genes, level, tier, dimension snapshot)
Layer 2: Vocabulary (M3-LOGOS term rules, tier-gated names)

Usage:
    from Musical_Intelligence.brain.llm.processing.context_builder import build_context
    ctx = build_context(user_profile=profile, language="tr")
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Musical_Intelligence.brain.llm.config import (
    CONTEXT_BUDGET,
    KNOWLEDGE_DIR,
    PROMPTS_DIR,
    TIERS,
)

# ── Prompt file cache ───────────────────────────────────────────────

_prompt_cache: dict[str, str] = {}


def _load_prompt(name: str) -> str:
    """Load a markdown prompt file, cached after first read."""
    if name not in _prompt_cache:
        path = PROMPTS_DIR / name
        _prompt_cache[name] = path.read_text(encoding="utf-8")
    return _prompt_cache[name]


# ── Knowledge card cache ────────────────────────────────────────────

_knowledge_cache: dict[str, list[dict]] = {}


def _load_jsonl(name: str) -> list[dict]:
    """Load a JSONL knowledge file, cached after first read."""
    if name not in _knowledge_cache:
        path = KNOWLEDGE_DIR / name
        cards: list[dict] = []
        for line in path.read_text(encoding="utf-8").strip().splitlines():
            if line.strip():
                cards.append(json.loads(line))
        _knowledge_cache[name] = cards
    return _knowledge_cache[name]


# ── Layer 0: Persona ────────────────────────────────────────────────


def build_layer0(language: str = "tr") -> str:
    """Assemble Layer 0: persona + guardrails.

    Args:
        language: "tr" or "en"

    Returns:
        System prompt string for identity and rules.
    """
    persona_file = f"persona_{language}.md"
    persona = _load_prompt(persona_file)
    guardrails = _load_prompt("guardrails.md")
    return f"{persona}\n\n{guardrails}"


# ── Layer 1: User Profile ──────────────────────────────────────────


def build_layer1(user_profile: dict[str, Any], language: str = "tr") -> str:
    """Assemble Layer 1: user-specific context injection.

    Args:
        user_profile: Dict with keys:
            - name: str
            - persona_id: int (1-24)
            - persona_name: str
            - family: str (Alchemists/Architects/Explorers/Anchors/Kineticists)
            - level: int (1-12)
            - tier: str (free/basic/premium/research)
            - genes: dict[str, float] (entropy/resolution/tension/resonance/plasticity)
            - dimensions_6d: dict[str, float] (current snapshot, optional)
            - listening_hours: float (optional)
        language: "tr" or "en"

    Returns:
        User profile block for system prompt injection.
    """
    name = user_profile.get("name", "Kullanıcı" if language == "tr" else "User")
    persona_name = user_profile.get("persona_name", "Unknown")
    family = user_profile.get("family", "Unknown")
    level = user_profile.get("level", 1)
    tier = user_profile.get("tier", "free")
    tier_info = TIERS.get(tier, TIERS["free"])

    # Look up persona card for conversation guidance
    personas = _load_jsonl("personas.jsonl")
    persona_id = user_profile.get("persona_id", 1)
    persona_card = next((p for p in personas if p["id"] == persona_id), None)

    lines: list[str] = []

    if language == "tr":
        lines.append("## Kullanıcı Profili")
        lines.append(f"- **İsim**: {name}")
        lines.append(f"- **Persona**: {persona_name} ({family})")
        lines.append(f"- **Seviye**: L{level}")
        lines.append(f"- **Katman**: {tier_info['label']} ({tier_info['domain']})")
        lines.append(f"- **Maksimum boyut derinliği**: {tier_info['max_dim']}D")
    else:
        lines.append("## User Profile")
        lines.append(f"- **Name**: {name}")
        lines.append(f"- **Persona**: {persona_name} ({family})")
        lines.append(f"- **Level**: L{level}")
        lines.append(f"- **Tier**: {tier_info['label']} ({tier_info['domain']})")
        lines.append(f"- **Max dimension depth**: {tier_info['max_dim']}D")

    # Genes
    genes = user_profile.get("genes")
    if genes:
        gene_str = ", ".join(f"{k}={v:.2f}" for k, v in genes.items())
        if language == "tr":
            lines.append(f"- **Genler**: {gene_str}")
        else:
            lines.append(f"- **Genes**: {gene_str}")

    # Current 6D snapshot (if available from recent analysis)
    dims_6d = user_profile.get("dimensions_6d")
    if dims_6d:
        dim_str = ", ".join(f"{k}={v:.2f}" for k, v in dims_6d.items())
        if language == "tr":
            lines.append(f"- **Güncel 6D**: {dim_str}")
        else:
            lines.append(f"- **Current 6D**: {dim_str}")

    # Spotify listening profile (if available)
    sp = user_profile.get("spotify_profile")
    if sp:
        lines.append("")
        if language == "tr":
            lines.append("### Dinleme Profili (Spotify)")
            lines.append(f"- **Kütüphane**: {sp.get('total_tracks', 0)} parça, {round(sp.get('total_minutes', 0) / 60, 1)} saat")
            top_genres = sp.get("top_genres", [])
            if top_genres:
                lines.append(f"- **Favori türler**: {', '.join(top_genres[:8])}")
            lines.append(f"- **Tür çeşitliliği**: {sp.get('genre_diversity', 0):.2f}")
            lines.append(f"- **Sanatçı sayısı**: {sp.get('artist_count', 0)}")
            fd = sp.get("family_distribution", {})
            if fd:
                fd_str = ", ".join(f"{k} %{round(v / max(sum(fd.values()), 1) * 100)}" for k, v in sorted(fd.items(), key=lambda x: -x[1]))
                lines.append(f"- **Aile dağılımı**: {fd_str}")
            ts = sp.get("taste_shift", 0)
            if ts > 0.05:
                lines.append(f"- **Zevk evrimi**: {ts:+.2f} (kısa vs uzun dönem farkı)")
        else:
            lines.append("### Listening Profile (Spotify)")
            lines.append(f"- **Library**: {sp.get('total_tracks', 0)} tracks, {round(sp.get('total_minutes', 0) / 60, 1)} hours")
            top_genres = sp.get("top_genres", [])
            if top_genres:
                lines.append(f"- **Top genres**: {', '.join(top_genres[:8])}")
            lines.append(f"- **Genre diversity**: {sp.get('genre_diversity', 0):.2f}")
            lines.append(f"- **Unique artists**: {sp.get('artist_count', 0)}")
            fd = sp.get("family_distribution", {})
            if fd:
                fd_str = ", ".join(f"{k} {round(v / max(sum(fd.values()), 1) * 100)}%" for k, v in sorted(fd.items(), key=lambda x: -x[1]))
                lines.append(f"- **Family distribution**: {fd_str}")
            ts = sp.get("taste_shift", 0)
            if ts > 0.05:
                lines.append(f"- **Taste evolution**: {ts:+.2f} (short vs long term shift)")

    # Persona-specific conversation guidance
    if persona_card:
        lines.append("")
        if language == "tr":
            lines.append("### Konuşma Rehberi")
            lines.append(f"- **Ton**: {persona_card.get('conversation_tone', '')}")
            lines.append(f"- **Metafor stili**: {persona_card.get('metaphor_style', '')}")
            lines.append(f"- **Tercih ettiği konular**: {', '.join(persona_card.get('preferred_topics', []))}")
            shadow = persona_card.get("shadow", "")
            if shadow:
                lines.append(f"- **Gölge (gelişim alanı)**: {shadow}")
        else:
            lines.append("### Conversation Guide")
            lines.append(f"- **Tone**: {persona_card.get('conversation_tone', '')}")
            lines.append(f"- **Metaphor style**: {persona_card.get('metaphor_style', '')}")
            lines.append(f"- **Preferred topics**: {', '.join(persona_card.get('preferred_topics', []))}")
            shadow = persona_card.get("shadow", "")
            if shadow:
                lines.append(f"- **Shadow (growth area)**: {shadow}")

    return "\n".join(lines)


# ── Layer 2: Vocabulary ─────────────────────────────────────────────


def build_layer2(tier: str = "free", language: str = "tr") -> str:
    """Assemble Layer 2: tier-gated vocabulary and dimension names.

    Args:
        tier: User's subscription tier (free/basic/premium/research)
        language: "tr" or "en"

    Returns:
        Vocabulary rules + relevant dimension cards for the tier.
    """
    vocabulary = _load_prompt("vocabulary.md")
    tier_rules = _load_prompt("tier_rules.md")

    # Load dimension cards gated by tier
    max_dim = TIERS.get(tier, TIERS["free"])["max_dim"]
    suffix = "tr" if language == "tr" else "en"

    lines: list[str] = [vocabulary, "", tier_rules, ""]

    # Always include 6D
    dims_6d = _load_jsonl("dimensions_6d.jsonl")
    if language == "tr":
        lines.append("### Aktif Boyutlar (6D)")
    else:
        lines.append("### Active Dimensions (6D)")
    for d in dims_6d:
        name = d.get(f"name_{suffix}", d.get("name_en"))
        what = d.get(f"what_{suffix}", d.get("what_en"))
        lines.append(f"- **{name}**: {what}")

    # 12D for basic+
    if max_dim >= 12:
        dims_12d = _load_jsonl("dimensions_12d.jsonl")
        lines.append("")
        if language == "tr":
            lines.append("### Aktif Boyutlar (12D)")
        else:
            lines.append("### Active Dimensions (12D)")
        for d in dims_12d:
            name = d.get(f"name_{suffix}", d.get("name_en"))
            what = d.get(f"what_{suffix}", d.get("what_en"))
            lines.append(f"- **{name}**: {what}")

    # 24D for premium+
    if max_dim >= 24:
        dims_24d = _load_jsonl("dimensions_24d.jsonl")
        lines.append("")
        if language == "tr":
            lines.append("### Aktif Boyutlar (24D)")
        else:
            lines.append("### Active Dimensions (24D)")
        for d in dims_24d:
            name = d.get(f"name_{suffix}", d.get("name_en"))
            what = d.get(f"what_{suffix}", d.get("what_en"))
            lines.append(f"- **{name}**: {what}")

    return "\n".join(lines)


# ── Full Context Assembly ───────────────────────────────────────────


def build_context(
    user_profile: dict[str, Any],
    language: str = "tr",
) -> str:
    """Build the complete Layer 0-2 system prompt.

    Args:
        user_profile: User profile dict (see build_layer1 for schema).
        language: "tr" or "en".

    Returns:
        Assembled system prompt string (Layers 0 + 1 + 2).
    """
    tier = user_profile.get("tier", "free")

    layer0 = build_layer0(language)
    layer1 = build_layer1(user_profile, language)
    layer2 = build_layer2(tier, language)

    return f"{layer0}\n\n---\n\n{layer1}\n\n---\n\n{layer2}"


def estimate_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token for mixed TR/EN text)."""
    return len(text) // 4


def build_context_with_budget(
    user_profile: dict[str, Any],
    language: str = "tr",
) -> dict[str, Any]:
    """Build context and return with token estimates per layer.

    Returns:
        Dict with keys: context, layer0_tokens, layer1_tokens,
        layer2_tokens, total_tokens, budget.
    """
    tier = user_profile.get("tier", "free")

    layer0 = build_layer0(language)
    layer1 = build_layer1(user_profile, language)
    layer2 = build_layer2(tier, language)

    context = f"{layer0}\n\n---\n\n{layer1}\n\n---\n\n{layer2}"

    l0_tok = estimate_tokens(layer0)
    l1_tok = estimate_tokens(layer1)
    l2_tok = estimate_tokens(layer2)
    total = l0_tok + l1_tok + l2_tok

    budget_total = (
        CONTEXT_BUDGET["persona"]
        + CONTEXT_BUDGET["user_profile"]
        + CONTEXT_BUDGET["vocabulary"]
    )

    return {
        "context": context,
        "layer0_tokens": l0_tok,
        "layer1_tokens": l1_tok,
        "layer2_tokens": l2_tok,
        "total_tokens": total,
        "budget": budget_total,
        "within_budget": total <= budget_total,
    }
