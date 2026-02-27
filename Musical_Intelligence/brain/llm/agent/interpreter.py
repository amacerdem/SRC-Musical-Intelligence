"""Dimension & Belief Interpreter — converts numerical states to natural language.

Takes raw belief values, dimension scores, and neurochemical levels and
produces human-readable observations following M3-LOGOS vocabulary.

Usage:
    from Musical_Intelligence.brain.llm.agent.interpreter import interpret_dimensions

    text = interpret_dimensions(
        dimensions_6d={"discovery": 0.82, "intensity": 0.15, ...},
        tier="basic",
        language="tr",
    )
"""

from __future__ import annotations

import json
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR, TIERS

# ── Dimension Card Cache ────────────────────────────────────────────

_dim_cards: dict[str, list[dict]] = {}


def _load_dim_cards(level: str) -> list[dict]:
    """Load dimension cards for a given level (6d, 12d, 24d)."""
    if level not in _dim_cards:
        path = KNOWLEDGE_DIR / f"dimensions_{level}.jsonl"
        cards: list[dict] = []
        for line in path.read_text(encoding="utf-8").strip().splitlines():
            if line.strip():
                cards.append(json.loads(line))
        _dim_cards[level] = cards
    return _dim_cards[level]


def _load_neurochemicals() -> list[dict]:
    """Load neurochemical cards."""
    if "neuro" not in _dim_cards:
        path = KNOWLEDGE_DIR / "neurochemicals.jsonl"
        cards: list[dict] = []
        for line in path.read_text(encoding="utf-8").strip().splitlines():
            if line.strip():
                cards.append(json.loads(line))
        _dim_cards["neuro"] = cards
    return _dim_cards["neuro"]


# ── Polarity Classification ────────────────────────────────────────


def _classify_value(value: float) -> str:
    """Classify a 0-1 value into polarity."""
    if value >= 0.7:
        return "high"
    elif value <= 0.3:
        return "low"
    else:
        return "moderate"


def _classify_delta(current: float, previous: float | None) -> str | None:
    """Classify change direction."""
    if previous is None:
        return None
    delta = current - previous
    if delta > 0.1:
        return "rising"
    elif delta < -0.1:
        return "falling"
    return None


# ── 6D Interpretation ──────────────────────────────────────────────


def interpret_6d(
    values: dict[str, float],
    language: str = "tr",
    previous: dict[str, float] | None = None,
) -> list[dict[str, str]]:
    """Interpret 6D psychology dimensions.

    Args:
        values: Dict of {dim_key: float_value} (0-1 scale).
        language: "tr" or "en".
        previous: Optional previous values for delta detection.

    Returns:
        List of observation dicts with "dimension", "polarity", "text".
    """
    cards = _load_dim_cards("6d")
    card_map = {c["key"]: c for c in cards}
    suffix = "tr" if language == "tr" else "en"

    observations: list[dict[str, str]] = []

    for key, value in values.items():
        card = card_map.get(key)
        if not card:
            continue

        polarity = _classify_value(value)
        delta = _classify_delta(value, previous.get(key) if previous else None)

        # Choose the best descriptor
        if delta in ("rising", "falling"):
            text = card.get(f"{delta}_{suffix}", card.get(f"{polarity}_{suffix}", ""))
        else:
            text = card.get(f"{polarity}_{suffix}", "")

        name = card.get(f"name_{suffix}", card.get("name_en", key))

        observations.append({
            "dimension": name,
            "key": key,
            "value": f"{value:.2f}",
            "polarity": delta or polarity,
            "text": text,
        })

    return observations


# ── Neurochemical Interpretation ────────────────────────────────────


def interpret_neurochemicals(
    levels: dict[str, float],
    language: str = "tr",
) -> list[dict[str, str]]:
    """Interpret neurochemical levels.

    Args:
        levels: Dict of {DA/NE/OPI/5HT: float_value} (0-1 scale).
        language: "tr" or "en".

    Returns:
        List of observation dicts.
    """
    cards = _load_neurochemicals()
    card_map = {c["key"]: c for c in cards}
    suffix = "tr" if language == "tr" else "en"

    observations: list[dict[str, str]] = []

    for key, value in levels.items():
        card = card_map.get(key)
        if not card:
            continue

        polarity = _classify_value(value)
        name = card.get(f"name_{suffix}", card.get("name_en", key))
        role = card.get(f"role_{suffix}", card.get("role_en", ""))

        observations.append({
            "neurochemical": name,
            "key": key,
            "symbol": card.get("symbol", key),
            "value": f"{value:.2f}",
            "polarity": polarity,
            "role": role,
        })

    return observations


# ── Full Interpretation ─────────────────────────────────────────────


def interpret_dimensions(
    dimensions_6d: dict[str, float],
    tier: str = "free",
    language: str = "tr",
    dimensions_12d: dict[str, float] | None = None,
    dimensions_24d: dict[str, float] | None = None,
    neurochemicals: dict[str, float] | None = None,
    previous_6d: dict[str, float] | None = None,
) -> str:
    """Generate a full natural-language interpretation.

    Respects tier gating — only includes dimensions the user's tier allows.

    Args:
        dimensions_6d: 6D values (always required).
        tier: User's subscription tier.
        language: "tr" or "en".
        dimensions_12d: 12D values (basic+ only).
        dimensions_24d: 24D values (premium+ only).
        neurochemicals: Neurochemical levels (any tier).
        previous_6d: Previous session 6D for delta detection.

    Returns:
        Formatted natural-language interpretation string.
    """
    max_dim = TIERS.get(tier, TIERS["free"])["max_dim"]
    suffix = "tr" if language == "tr" else "en"
    lines: list[str] = []

    # 6D — always
    obs_6d = interpret_6d(dimensions_6d, language, previous_6d)

    # Find the most prominent dimensions (highest and lowest)
    sorted_dims = sorted(obs_6d, key=lambda o: float(o["value"]), reverse=True)
    top = sorted_dims[:2]  # highest 2
    bottom = [d for d in sorted_dims[-2:] if float(d["value"]) < 0.4]  # lowest if notable

    if language == "tr":
        lines.append("**Şu anki durumun:**")
    else:
        lines.append("**Your current state:**")

    for obs in top:
        lines.append(f"- {obs['dimension']}: {obs['text']}")

    if bottom:
        for obs in bottom:
            lines.append(f"- {obs['dimension']}: {obs['text']}")

    # Neurochemicals — any tier
    if neurochemicals:
        neuro_obs = interpret_neurochemicals(neurochemicals, language)
        active = [n for n in neuro_obs if float(n["value"]) > 0.6]
        if active:
            lines.append("")
            if language == "tr":
                lines.append("**Aktif nörokimyasallar:**")
            else:
                lines.append("**Active neurochemicals:**")
            for n in active:
                lines.append(f"- {n['symbol']} ({n['role']})")

    # 12D — basic+
    if max_dim >= 12 and dimensions_12d:
        cards_12d = _load_dim_cards("12d")
        card_map_12d = {c["key"]: c for c in cards_12d}
        notable = [(k, v) for k, v in dimensions_12d.items() if v > 0.7 or v < 0.3]
        if notable:
            lines.append("")
            if language == "tr":
                lines.append("**Bilişsel kanallar:**")
            else:
                lines.append("**Cognitive channels:**")
            for key, value in sorted(notable, key=lambda x: x[1], reverse=True)[:4]:
                card = card_map_12d.get(key, {})
                name = card.get(f"name_{suffix}", key)
                pol = _classify_value(value)
                desc = card.get(f"{pol}_{suffix}", "")
                lines.append(f"- {name}: {desc}")

    # 24D — premium+
    if max_dim >= 24 and dimensions_24d:
        cards_24d = _load_dim_cards("24d")
        card_map_24d = {c["key"]: c for c in cards_24d}
        notable = [(k, v) for k, v in dimensions_24d.items() if v > 0.7 or v < 0.3]
        if notable:
            lines.append("")
            if language == "tr":
                lines.append("**Nörobilimsel katman:**")
            else:
                lines.append("**Neuroscience layer:**")
            for key, value in sorted(notable, key=lambda x: x[1], reverse=True)[:4]:
                card = card_map_24d.get(key, {})
                name = card.get(f"name_{suffix}", key)
                correlate = card.get("neural_correlate", "")
                lines.append(f"- {name} ({correlate})")

    return "\n".join(lines)
