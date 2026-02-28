"""Interpreter Package — rich, tier-gated, persona-aware interpretation engine.

Public API:
    interpret_dimensions(...)  — backward-compat string output for /interpret
    interpret_track(...)       — full track analysis with all layers
    interpret_comparison(...)  — rich two-track comparison

Usage:
    from Musical_Intelligence.brain.llm.agent.interpreter import interpret_dimensions
    from Musical_Intelligence.brain.llm.agent.interpreter import interpret_track
"""

from __future__ import annotations

from typing import Any

from Musical_Intelligence.brain.llm.config import TIERS

from .dimensions import (
    interpret_dimensions as _interpret_dims_full,
    interpret_6d,
    interpret_12d,
    interpret_24d,
)
from .neurochemicals import interpret_neurochemicals
from .functions import interpret_functions
from .temporal import interpret_temporal
from .reward import interpret_reward
from .beliefs import interpret_beliefs
from .brain_regions import interpret_brain_regions
from .genes import interpret_genes
from .comparison import interpret_comparison
from .observation import get_available_observations, get_observation_type
from .polarity import classify_value, classify_delta, polarity_label, delta_label

__all__ = [
    # Backward-compat
    "interpret_dimensions",
    # Full track
    "interpret_track",
    # Comparison
    "interpret_comparison",
    # Individual modules
    "interpret_6d",
    "interpret_12d",
    "interpret_24d",
    "interpret_neurochemicals",
    "interpret_functions",
    "interpret_temporal",
    "interpret_reward",
    "interpret_beliefs",
    "interpret_brain_regions",
    "interpret_genes",
    # Observation
    "get_available_observations",
    "get_observation_type",
    # Polarity utils
    "classify_value",
    "classify_delta",
    "polarity_label",
    "delta_label",
]


# ── Backward-Compatible String API ──────────────────────────────


def interpret_dimensions(
    dimensions_6d: dict[str, float],
    tier: str = "free",
    language: str = "tr",
    dimensions_12d: dict[str, float] | None = None,
    dimensions_24d: dict[str, float] | None = None,
    neurochemicals: dict[str, float] | None = None,
    previous_6d: dict[str, float] | None = None,
    persona_family: str | None = None,
) -> str:
    """Generate full natural-language interpretation (backward-compatible).

    Returns a formatted string, compatible with the old interpreter API.
    """
    result = _interpret_dims_full(
        dimensions_6d=dimensions_6d,
        tier=tier,
        language=language,
        dimensions_12d=dimensions_12d,
        dimensions_24d=dimensions_24d,
        previous_6d=previous_6d,
        persona_family=persona_family,
    )

    parts: list[str] = [result["narrative"]]

    # Add neurochemicals if provided
    if neurochemicals:
        neuro_result = interpret_neurochemicals(neurochemicals, language, tier)
        parts.append("")
        parts.append(neuro_result["narrative"])

    return "\n".join(parts)


# ── Full Track Interpretation ───────────────────────────────────


def interpret_track(
    track: dict[str, Any],
    tier: str = "free",
    language: str = "tr",
    persona_family: str | None = None,
    level: int = 1,
    user_genes: dict[str, float] | None = None,
    previous_6d: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Generate comprehensive track interpretation with all available layers.

    Args:
        track: Full track analysis dict (from format_track_for_llm or raw).
        tier: User's subscription tier.
        language: "tr" or "en".
        persona_family: User's persona family (for metaphor tone).
        level: User's level (for observation gating).
        user_genes: User's gene profile (for matching).
        previous_6d: Previous session 6D (for delta detection).

    Returns:
        Dict with all interpretation layers:
        - dimensions: tier-gated 6D/12D/24D narrative
        - neurochemicals: combination narrative
        - functions: F1-F9 comparative
        - reward_insight: reward decomposition
        - temporal_summary: temporal arc (if available)
        - beliefs: cross-function patterns (basic+)
        - brain_regions: RAM 26D narrative (premium+)
        - gene_match: gene profile + user matching
        - observation_type: level-gated observation
        - narrative: combined human-readable summary
        - highlights: bullet-point highlights
    """
    max_dim = TIERS.get(tier, TIERS["free"])["max_dim"]
    sfx = "tr" if language == "tr" else "en"

    result: dict[str, Any] = {
        "track_id": track.get("id", track.get("track", {}).get("id", "")),
        "artist": track.get("artist", track.get("track", {}).get("artist", "")),
        "title": track.get("title", track.get("track", {}).get("title", "")),
    }

    all_highlights: list[str] = []
    narrative_parts: list[str] = []

    # ── Dimensions ──────────────────────────────────────────────
    dims = track.get("dimensions", {})
    dims_6d = track.get("psychology_6d", dims.get("psychology_6d", {}))
    dims_12d = track.get("cognition_12d", dims.get("cognition_12d", None))
    dims_24d = track.get("neuroscience_24d", dims.get("neuroscience_24d", None))

    # Handle list format
    if isinstance(dims_6d, list):
        from Musical_Intelligence.brain.llm.agent.track_data import DIM_6D
        dims_6d = {k: v for k, v in zip(DIM_6D, dims_6d)}
    if isinstance(dims_12d, list):
        from Musical_Intelligence.brain.llm.agent.track_data import DIM_12D
        dims_12d = {k: v for k, v in zip(DIM_12D, dims_12d)}
    if isinstance(dims_24d, list):
        from Musical_Intelligence.brain.llm.agent.track_data import DIM_24D
        dims_24d = {k: v for k, v in zip(DIM_24D, dims_24d)}

    if dims_6d:
        dim_result = _interpret_dims_full(
            dimensions_6d=dims_6d,
            tier=tier,
            language=language,
            dimensions_12d=dims_12d if max_dim >= 12 else None,
            dimensions_24d=dims_24d if max_dim >= 24 else None,
            previous_6d=previous_6d,
            persona_family=persona_family,
        )
        result["dimensions"] = dim_result
        narrative_parts.append(dim_result["narrative"])
        all_highlights.extend(dim_result["highlights"][:3])

    # ── Neurochemicals ──────────────────────────────────────────
    neuro = track.get("neurochemicals", track.get("neuro_4d", {}))
    if neuro:
        neuro_result = interpret_neurochemicals(neuro, language, tier)
        result["neurochemicals"] = neuro_result
        narrative_parts.append("")
        narrative_parts.append(neuro_result["narrative"])
        all_highlights.extend(neuro_result["highlights"][:2])

    # ── Functions ───────────────────────────────────────────────
    functions = track.get("functions", {})
    if functions:
        fn_result = interpret_functions(functions, language, tier)
        result["functions"] = fn_result
        narrative_parts.append("")
        narrative_parts.append(fn_result["narrative"])
        all_highlights.extend(fn_result["highlights"][:2])

    # ── Reward ──────────────────────────────────────────────────
    signal = track.get("signal", {})
    if signal:
        reward_data = {
            "total": signal.get("reward", signal.get("total_reward", 0.5)),
            "surprise": signal.get("surprise", 0.5),
            "resolution": signal.get("resolution", 0.5),
            "exploration": signal.get("exploration", 0.5),
            "monotony": signal.get("monotony", 0.0),
            "familiarity": signal.get("familiarity", None),
        }
        reward_result = interpret_reward(reward_data, language, tier)
        result["reward_insight"] = reward_result
        narrative_parts.append("")
        narrative_parts.append(reward_result["narrative"])
        all_highlights.extend(reward_result["highlights"][:2])

    # ── Beliefs (basic+) ────────────────────────────────────────
    beliefs = track.get("beliefs", {})
    means = beliefs.get("means", [])
    stds = beliefs.get("stds", [])

    if tier in ("basic", "premium", "research") and means and stds:
        beliefs_result = interpret_beliefs(means, stds, language, tier)
        result["beliefs"] = beliefs_result
        narrative_parts.append("")
        narrative_parts.append(beliefs_result["narrative"])
        all_highlights.extend(beliefs_result["highlights"][:2])

    # ── Brain Regions (premium+) ────────────────────────────────
    ram = track.get("ram_26d", {})
    if tier in ("premium", "research") and ram:
        ram_values = ram if isinstance(ram, (dict, list)) else {}
        if ram_values:
            ram_result = interpret_brain_regions(ram_values, language, tier)
            result["brain_regions"] = ram_result
            narrative_parts.append("")
            narrative_parts.append(ram_result["narrative"])
            all_highlights.extend(ram_result["highlights"][:2])

    # ── Temporal (premium+) ─────────────────────────────────────
    tp = track.get("temporal_profile", {})
    if tier in ("premium", "research") and tp.get("belief_means_per_segment"):
        temporal_result = interpret_temporal(tp, means, stds, language, tier)
        result["temporal_summary"] = temporal_result
        narrative_parts.append("")
        narrative_parts.append(temporal_result["narrative"])
        all_highlights.extend(temporal_result["highlights"][:2])

    # ── Genes ───────────────────────────────────────────────────
    genes = track.get("genes", {})
    if genes:
        gene_result = interpret_genes(genes, language, user_genes, persona_family)
        result["gene_match"] = gene_result
        narrative_parts.append("")
        narrative_parts.append(gene_result["narrative"])
        if gene_result.get("match_note"):
            all_highlights.append(gene_result["match_note"][:80])

    # ── Observation Type ────────────────────────────────────────
    available_data = []
    if dims_6d:
        available_data.append("dimensions_6d")
    if dims_12d:
        available_data.append("dimensions_12d")
    if neuro:
        available_data.append("neurochemicals")
    if functions:
        available_data.append("functions")
    if means:
        available_data.append("beliefs")
    if ram:
        available_data.append("ram_26d")
    if tp.get("belief_means_per_segment"):
        available_data.append("temporal")
    if genes:
        available_data.append("genes")
    if previous_6d:
        available_data.append("previous_6d")

    obs_type = get_observation_type(level, available_data, language)
    if obs_type:
        result["observation_type"] = obs_type

    # ── Assemble ────────────────────────────────────────────────
    result["narrative"] = "\n".join(narrative_parts)
    result["highlights"] = all_highlights[:10]

    return result
