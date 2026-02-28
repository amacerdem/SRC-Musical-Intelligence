"""Dimension Interpreter — tier-gated 6D/12D/24D narrative generation.

Reads dimension cards from knowledge/ and produces rich, persona-aware
natural language descriptions of a listener's dimensional state.
"""

from __future__ import annotations

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR, TIERS
from .polarity import classify_value, classify_delta, polarity_label, delta_label

# ── Dimension Card Cache ─────────────────────────────────────────

_dim_cards: dict[str, list[dict]] = {}


def _load_cards(level: str) -> list[dict]:
    """Load dimension cards for a given level (6d, 12d, 24d)."""
    if level not in _dim_cards:
        path = KNOWLEDGE_DIR / f"dimensions_{level}.jsonl"
        cards: list[dict] = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").strip().splitlines():
                if line.strip():
                    cards.append(json.loads(line))
        _dim_cards[level] = cards
    return _dim_cards[level]


# ── Persona-Family Metaphor Prefixes ─────────────────────────────

_FAMILY_TONE: dict[str, dict[str, str]] = {
    "Alchemists": {
        "en": "Through the lens of transformation",
        "tr": "Dönüşüm merceğinden",
    },
    "Architects": {
        "en": "From a structural perspective",
        "tr": "Yapısal bir perspektiften",
    },
    "Explorers": {
        "en": "On the frontier of discovery",
        "tr": "Keşfin sınırında",
    },
    "Anchors": {
        "en": "In the depth of feeling",
        "tr": "Duygunun derinliğinde",
    },
    "Kineticists": {
        "en": "In the pulse of movement",
        "tr": "Hareketin nabzında",
    },
}


# ── 6D Interpretation ────────────────────────────────────────────


def interpret_6d(
    values: dict[str, float],
    language: str = "tr",
    previous: dict[str, float] | None = None,
    persona_family: str | None = None,
) -> dict[str, Any]:
    """Interpret 6D psychology dimensions with rich narrative.

    Returns:
        Dict with "narrative", "highlights", "observations".
    """
    cards = _load_cards("6d")
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    observations: list[dict] = []
    highlights: list[str] = []

    # Sort by extremity (distance from 0.5) for narrative priority
    sorted_keys = sorted(
        values.keys(),
        key=lambda k: abs(values[k] - 0.5),
        reverse=True,
    )

    for key in sorted_keys:
        value = values[key]
        card = card_map.get(key)
        if not card:
            continue

        pol = classify_value(value)
        dlt = classify_delta(value, previous.get(key) if previous else None)

        # Choose the best descriptor from the card
        if dlt in ("rising", "rising_fast"):
            text = card.get(f"rising_{sfx}", card.get(f"high_{sfx}", ""))
        elif dlt in ("falling", "falling_fast"):
            text = card.get(f"falling_{sfx}", card.get(f"low_{sfx}", ""))
        elif pol in ("very_high", "high"):
            text = card.get(f"high_{sfx}", "")
        elif pol in ("very_low", "low"):
            text = card.get(f"low_{sfx}", "")
        else:
            text = card.get(f"moderate_{sfx}", card.get(f"what_{sfx}", ""))

        name = card.get(f"name_{sfx}", card.get("name_en", key))

        obs = {
            "dimension": name,
            "key": key,
            "value": round(value, 3),
            "polarity": polarity_label(value, language),
            "delta": delta_label(value, previous.get(key) if previous else None, language),
            "text": text,
        }
        observations.append(obs)

        # Build highlights from the most extreme
        if abs(value - 0.5) > 0.15:
            highlights.append(f"{name}: {text}")

    # Build narrative
    narrative_parts: list[str] = []

    # Persona-family tone prefix
    if persona_family and persona_family in _FAMILY_TONE:
        narrative_parts.append(_FAMILY_TONE[persona_family][sfx] + ":")

    # Top 2 most extreme dimensions
    top_2 = observations[:2]
    for obs in top_2:
        if obs["delta"]:
            narrative_parts.append(f"**{obs['dimension']}** ({obs['delta']}): {obs['text']}")
        else:
            narrative_parts.append(f"**{obs['dimension']}** ({obs['polarity']}): {obs['text']}")

    # Contrast note if present
    if len(observations) >= 4:
        hi = observations[0]
        lo = next((o for o in observations if o["value"] < 0.4), None)
        if lo and hi["value"] > 0.6:
            if language == "tr":
                narrative_parts.append(
                    f"Dikkat çekici kontrast: {hi['dimension']} yüksekken "
                    f"{lo['dimension']} düşük — bu deneyim seçici bir odak gösteriyor."
                )
            else:
                narrative_parts.append(
                    f"Notable contrast: {hi['dimension']} is high while "
                    f"{lo['dimension']} is low — this experience shows selective focus."
                )

    return {
        "narrative": "\n".join(narrative_parts),
        "highlights": highlights[:4],
        "observations": observations,
        "tier_used": "6d",
    }


# ── 12D Interpretation ───────────────────────────────────────────


def interpret_12d(
    values: dict[str, float],
    language: str = "tr",
) -> dict[str, Any]:
    """Interpret 12D cognition dimensions."""
    cards = _load_cards("12d")
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    # Find notable dimensions (extreme values)
    notable: list[dict] = []
    for key, value in sorted(values.items(), key=lambda x: abs(x[1] - 0.5), reverse=True):
        card = card_map.get(key, {})
        pol = classify_value(value)
        if pol in ("very_high", "high"):
            desc = card.get(f"high_{sfx}", "")
        elif pol in ("very_low", "low"):
            desc = card.get(f"low_{sfx}", "")
        else:
            desc = card.get(f"what_{sfx}", "")

        name = card.get(f"name_{sfx}", card.get("name_en", key))
        parent = card.get("parent_6d", "")

        notable.append({
            "dimension": name,
            "key": key,
            "value": round(value, 3),
            "polarity": polarity_label(value, language),
            "parent_6d": parent,
            "text": desc,
        })

    # Top 4 for narrative
    top = [d for d in notable if abs(d["value"] - 0.5) > 0.15][:4]

    parts: list[str] = []
    if language == "tr":
        parts.append("**Bilişsel kanallar:**")
    else:
        parts.append("**Cognitive channels:**")
    for d in top:
        parts.append(f"- {d['dimension']}: {d['text']}")

    return {
        "narrative": "\n".join(parts),
        "highlights": [f"{d['dimension']}: {d['text']}" for d in top],
        "observations": notable,
        "tier_used": "12d",
    }


# ── 24D Interpretation ───────────────────────────────────────────


def interpret_24d(
    values: dict[str, float],
    language: str = "tr",
) -> dict[str, Any]:
    """Interpret 24D neuroscience dimensions."""
    cards = _load_cards("24d")
    card_map = {c["key"]: c for c in cards}
    sfx = "tr" if language == "tr" else "en"

    notable: list[dict] = []
    for key, value in sorted(values.items(), key=lambda x: abs(x[1] - 0.5), reverse=True):
        card = card_map.get(key, {})
        pol = classify_value(value)
        if pol in ("very_high", "high"):
            desc = card.get(f"high_{sfx}", "")
        elif pol in ("very_low", "low"):
            desc = card.get(f"low_{sfx}", "")
        else:
            desc = card.get(f"what_{sfx}", "")

        name = card.get(f"name_{sfx}", card.get("name_en", key))
        correlate = card.get("neural_correlate", "")

        notable.append({
            "dimension": name,
            "key": key,
            "value": round(value, 3),
            "polarity": polarity_label(value, language),
            "neural_correlate": correlate,
            "text": desc,
        })

    top = [d for d in notable if abs(d["value"] - 0.5) > 0.15][:4]

    parts: list[str] = []
    if language == "tr":
        parts.append("**Nörobilimsel katman:**")
    else:
        parts.append("**Neuroscience layer:**")
    for d in top:
        if d["neural_correlate"]:
            parts.append(f"- {d['dimension']} [{d['neural_correlate']}]: {d['text']}")
        else:
            parts.append(f"- {d['dimension']}: {d['text']}")

    return {
        "narrative": "\n".join(parts),
        "highlights": [f"{d['dimension']}: {d['text']}" for d in top],
        "observations": notable,
        "tier_used": "24d",
    }


# ── Full Tier-Gated Dimension Interpretation ─────────────────────


def interpret_dimensions(
    dimensions_6d: dict[str, float],
    tier: str = "free",
    language: str = "tr",
    dimensions_12d: dict[str, float] | None = None,
    dimensions_24d: dict[str, float] | None = None,
    previous_6d: dict[str, float] | None = None,
    persona_family: str | None = None,
) -> dict[str, Any]:
    """Generate full tier-gated dimension interpretation.

    Returns:
        Dict with "narrative" (str), "highlights" (list), "layers" (dict).
    """
    max_dim = TIERS.get(tier, TIERS["free"])["max_dim"]

    layers: dict[str, Any] = {}
    all_highlights: list[str] = []
    narrative_parts: list[str] = []

    # 6D — always
    result_6d = interpret_6d(dimensions_6d, language, previous_6d, persona_family)
    layers["6d"] = result_6d
    narrative_parts.append(result_6d["narrative"])
    all_highlights.extend(result_6d["highlights"])

    # 12D — basic+
    if max_dim >= 12 and dimensions_12d:
        result_12d = interpret_12d(dimensions_12d, language)
        layers["12d"] = result_12d
        narrative_parts.append("")
        narrative_parts.append(result_12d["narrative"])
        all_highlights.extend(result_12d["highlights"])

    # 24D — premium+
    if max_dim >= 24 and dimensions_24d:
        result_24d = interpret_24d(dimensions_24d, language)
        layers["24d"] = result_24d
        narrative_parts.append("")
        narrative_parts.append(result_24d["narrative"])
        all_highlights.extend(result_24d["highlights"])

    return {
        "narrative": "\n".join(narrative_parts),
        "highlights": all_highlights[:8],
        "layers": layers,
        "tier_used": tier,
    }
