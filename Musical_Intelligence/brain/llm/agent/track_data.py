"""Track Analysis Data Service — loads pre-computed MI analysis for 138 tracks.

Provides lookup, search, and LLM-friendly formatting of track analysis data
produced by the MI Pipeline v4.0 (R³→H³→C³, 88 mechanisms, 131 beliefs).
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Musical_Intelligence.brain.llm.config import KNOWLEDGE_DIR, PROJECT_ROOT

# ── Paths ──────────────────────────────────────────────────────────

DATASET_DIR = (
    PROJECT_ROOT
    / "My Musical Mind (Monetizing)"
    / "public"
    / "data"
    / "mi-dataset"
)
TRACKS_DIR = DATASET_DIR / "tracks"

# ── Dimension Key Names ────────────────────────────────────────────

DIM_6D = ["discovery", "intensity", "flow", "depth", "trace", "sharing"]

DIM_12D = [
    "expectancy", "information_rate", "tension_arc", "sonic_impact",
    "entrainment", "groove", "contagion", "reward",
    "episodic_resonance", "recognition", "synchrony", "bonding",
]

DIM_24D = [
    "predictive_processing", "information_entropy", "sequence_learning",
    "sensory_encoding", "harmonic_tension", "autonomic_arousal",
    "sensory_salience", "aesthetic_appraisal", "oscillation_coupling",
    "motor_period_locking", "auditory_motor", "hierarchical_context",
    "valence_mode", "nostalgia_circuitry", "dopaminergic_drive",
    "hedonic_valuation", "hippocampal_binding", "autobiographical",
    "pitch_melody", "perceptual_learning", "structural_prediction",
    "expertise_network", "interpersonal_sync", "social_reward",
]

FUNCTION_NAMES = {
    "F1": "Sensory Processing",
    "F2": "Prediction & Pattern Recognition",
    "F3": "Attention & Salience",
    "F4": "Memory Systems",
    "F5": "Emotion & Valence",
    "F6": "Reward & Motivation",
    "F7": "Motor & Timing",
    "F8": "Learning & Plasticity",
    "F9": "Social Cognition",
}

NEURO_NAMES = {
    "DA": "Dopamine (anticipation, reward prediction)",
    "NE": "Norepinephrine (attention, arousal)",
    "OPI": "Opioid (hedonic pleasure, liking)",
    "5HT": "Serotonin (mood, temporal discounting)",
}

# ── Belief Key Mapping ─────────────────────────────────────────────

_belief_keys: list[str] = []
_belief_meta: dict[str, dict] = {}


def _ensure_belief_keys() -> None:
    """Load belief key mapping from beliefs.jsonl (lazy, once)."""
    global _belief_keys, _belief_meta
    if _belief_keys:
        return
    path = KNOWLEDGE_DIR / "beliefs.jsonl"
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        card = json.loads(line)
        _belief_keys.append(card["key"])
        _belief_meta[card["key"]] = {
            "index": card["index"],
            "function": card["function"],
            "type": card["type"],
            "mechanism": card.get("mechanism", ""),
            "parent_6d": card.get("parent_6d", ""),
            "parent_12d": card.get("parent_12d", ""),
            "parent_24d": card.get("parent_24d", ""),
            "what_en": card.get("what_en", ""),
            "what_tr": card.get("what_tr", ""),
            "analogy_en": card.get("analogy_en", ""),
            "analogy_tr": card.get("analogy_tr", ""),
        }


def belief_index_to_key(idx: int) -> str:
    """Map belief index to key name."""
    _ensure_belief_keys()
    if 0 <= idx < len(_belief_keys):
        return _belief_keys[idx]
    return f"belief_{idx}"


def get_belief_meta(key: str) -> dict:
    """Get metadata for a belief key."""
    _ensure_belief_keys()
    return _belief_meta.get(key, {})


# ── Catalog ────────────────────────────────────────────────────────

_catalog: dict | None = None


def load_catalog() -> dict:
    """Load the track catalog (cached)."""
    global _catalog
    if _catalog is not None:
        return _catalog
    path = DATASET_DIR / "catalog.json"
    if not path.exists():
        _catalog = {"tracks": [], "total_tracks": 0}
        return _catalog
    _catalog = json.loads(path.read_text(encoding="utf-8"))
    return _catalog


# ── Track Loading ──────────────────────────────────────────────────

_track_cache: dict[str, dict] = {}


def load_track(track_id: str) -> dict | None:
    """Load a single track analysis JSON by ID."""
    if track_id in _track_cache:
        return _track_cache[track_id]

    path = TRACKS_DIR / f"{track_id}.json"
    if not path.exists():
        return None

    data = json.loads(path.read_text(encoding="utf-8"))
    _track_cache[track_id] = data
    return data


def list_tracks() -> list[dict]:
    """List all available tracks (basic info only)."""
    catalog = load_catalog()
    return [
        {
            "id": t["id"],
            "artist": t["artist"],
            "title": t["title"],
            "categories": t.get("categories", []),
            "duration_s": t.get("duration_s", 0),
        }
        for t in catalog.get("tracks", [])
    ]


def search_tracks(query: str, limit: int = 10) -> list[dict]:
    """Search tracks by artist, title, or ID. Case-insensitive fuzzy match."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    catalog = load_catalog()
    results = []

    for t in catalog.get("tracks", []):
        score = 0
        artist = t.get("artist", "").lower()
        title = t.get("title", "").lower()
        tid = t.get("id", "").lower()

        # Exact matches score highest
        if query_lower == artist or query_lower == title:
            score = 100
        elif query_lower in artist:
            score = 80
        elif query_lower in title:
            score = 70
        elif query_lower in tid:
            score = 60
        else:
            # Check individual words
            words = query_lower.split()
            for w in words:
                if w in artist:
                    score += 30
                if w in title:
                    score += 25
                if w in tid:
                    score += 15

        if score > 0:
            results.append((score, t))

    results.sort(key=lambda x: -x[0])
    return [
        {
            "id": t["id"],
            "artist": t["artist"],
            "title": t["title"],
            "categories": t.get("categories", []),
            "duration_s": t.get("duration_s", 0),
            "match_score": score,
        }
        for score, t in results[:limit]
    ]


# ── LLM-Friendly Formatting ───────────────────────────────────────


def _named_dims(values: list[float], keys: list[str]) -> dict[str, float]:
    """Map dimension values to named keys."""
    return {k: round(v, 3) for k, v in zip(keys, values) if v is not None}


def _polarity(value: float) -> str:
    """Describe a 0-1 value."""
    if value >= 0.75:
        return "very high"
    if value >= 0.6:
        return "high"
    if value >= 0.4:
        return "moderate"
    if value >= 0.25:
        return "low"
    return "very low"


def _top_beliefs(
    means: list[float],
    stds: list[float],
    n: int = 15,
) -> list[dict]:
    """Find the most notable beliefs (extreme values + high variance)."""
    _ensure_belief_keys()
    scored = []
    for i, (m, s) in enumerate(zip(means, stds)):
        key = belief_index_to_key(i)
        meta = get_belief_meta(key)
        # Score: distance from 0.5 (how extreme) + std (how dynamic)
        extremity = abs(m - 0.5) * 2
        notability = extremity * 0.6 + min(s * 10, 1.0) * 0.4
        scored.append({
            "key": key,
            "value": round(m, 3),
            "std": round(s, 3),
            "polarity": _polarity(m),
            "function": meta.get("function", ""),
            "type": meta.get("type", ""),
            "mechanism": meta.get("mechanism", ""),
            "what": meta.get("what_en", ""),
        })
    scored.sort(key=lambda x: -(abs(x["value"] - 0.5) * 0.6 + x["std"] * 4))
    return scored[:n]


def _temporal_arc(
    segments: list[list[float]],
    belief_idx: int,
) -> list[float]:
    """Extract a single belief's trajectory across temporal segments."""
    return [round(seg[belief_idx], 3) for seg in segments if len(seg) > belief_idx]


def format_track_for_llm(
    track: dict,
    tier: str = "free",
    language: str = "en",
) -> dict[str, Any]:
    """Format track analysis data for LLM consumption.

    Returns a structured summary appropriate for the user's tier:
    - free: signal, genes, 6D, functions, neurochemicals
    - basic: + 12D, top beliefs summary
    - premium: + 24D, detailed beliefs, temporal profile
    - research: + all 131 beliefs, full temporal data
    """
    result: dict[str, Any] = {
        "track": {
            "id": track.get("id", ""),
            "artist": track.get("artist", ""),
            "title": track.get("title", ""),
            "duration_s": track.get("duration_s", 0),
            "categories": track.get("categories", []),
        },
        "signal": track.get("signal", {}),
        "genes": track.get("genes", {}),
        "dominant_gene": track.get("dominant_gene", ""),
        "dominant_family": track.get("dominant_family", ""),
    }

    # 6D — always included
    dims = track.get("dimensions", {})
    if "psychology_6d" in dims:
        result["psychology_6d"] = _named_dims(dims["psychology_6d"], DIM_6D)

    # Functions — always included
    result["functions"] = track.get("functions", {})

    # Neurochemicals — always included
    result["neurochemicals"] = track.get("neuro_4d", {})

    # 12D — basic+ tier
    if tier in ("basic", "premium", "research") and "cognition_12d" in dims:
        result["cognition_12d"] = _named_dims(dims["cognition_12d"], DIM_12D)

    # Notable beliefs summary — basic+ tier
    beliefs = track.get("beliefs", {})
    means = beliefs.get("means", [])
    stds = beliefs.get("stds", [])

    if tier in ("basic", "premium", "research") and means:
        result["notable_beliefs"] = _top_beliefs(means, stds, n=15)

    # 24D — premium+ tier
    if tier in ("premium", "research") and "neuroscience_24d" in dims:
        result["neuroscience_24d"] = _named_dims(dims["neuroscience_24d"], DIM_24D)

    # RAM — premium+ tier
    if tier in ("premium", "research") and "ram_26d" in track:
        result["ram_26d"] = track["ram_26d"]

    # Temporal profile — premium+ tier
    tp = track.get("temporal_profile", {})
    if tier in ("premium", "research") and tp.get("belief_means_per_segment"):
        segs = tp["belief_means_per_segment"]
        # Summarize temporal arc for key beliefs
        _ensure_belief_keys()
        key_indices = {
            "harmonic_stability": 4,
            "prediction_accuracy": 20 if len(_belief_keys) > 20 else -1,
            "beat_entrainment": 36 if len(_belief_keys) > 36 else -1,
            "wanting": 65 if len(_belief_keys) > 65 else -1,
            "pleasure": 67 if len(_belief_keys) > 67 else -1,
        }
        # Use actual indices from belief metadata
        for key in list(key_indices):
            meta = get_belief_meta(key)
            if meta and "index" in meta:
                key_indices[key] = meta["index"]

        arcs = {}
        for key, idx in key_indices.items():
            if 0 <= idx < len(means):
                arcs[key] = _temporal_arc(segs, idx)
        result["temporal_arcs"] = arcs
        result["temporal_segments"] = tp.get("segments", 8)

    # Full belief data — research tier only
    if tier == "research" and means:
        _ensure_belief_keys()
        result["all_beliefs"] = {
            belief_index_to_key(i): {"mean": round(m, 4), "std": round(s, 4)}
            for i, (m, s) in enumerate(zip(means, stds))
        }

    return result


def format_dimensions_for_llm(
    track: dict,
    layer: str = "6d",
    tier: str = "free",
) -> dict[str, Any]:
    """Extract dimension values for a specific layer."""
    dims = track.get("dimensions", {})
    result: dict[str, Any] = {
        "track_id": track.get("id", ""),
        "artist": track.get("artist", ""),
        "title": track.get("title", ""),
    }

    if layer == "6d" and "psychology_6d" in dims:
        result["dimensions"] = _named_dims(dims["psychology_6d"], DIM_6D)
    elif layer == "12d" and "cognition_12d" in dims:
        result["dimensions"] = _named_dims(dims["cognition_12d"], DIM_12D)
    elif layer == "24d" and "neuroscience_24d" in dims:
        result["dimensions"] = _named_dims(dims["neuroscience_24d"], DIM_24D)
    else:
        result["dimensions"] = {}

    return result


def format_beliefs_for_llm(
    track: dict,
    belief_keys: list[str] | None = None,
    tier: str = "free",
) -> dict[str, Any]:
    """Extract specific belief values with metadata."""
    _ensure_belief_keys()
    beliefs = track.get("beliefs", {})
    means = beliefs.get("means", [])
    stds = beliefs.get("stds", [])

    if not means:
        return {"error": "No belief data available for this track."}

    # If no specific keys requested, return top notable beliefs
    if not belief_keys:
        return {
            "track_id": track.get("id", ""),
            "notable_beliefs": _top_beliefs(means, stds, n=15),
        }

    result_beliefs = {}
    for key in belief_keys:
        meta = get_belief_meta(key)
        if not meta:
            result_beliefs[key] = {"error": f"Unknown belief key: {key}"}
            continue
        idx = meta["index"]
        if idx >= len(means):
            result_beliefs[key] = {"error": f"Index {idx} out of range"}
            continue
        result_beliefs[key] = {
            "value": round(means[idx], 4),
            "std": round(stds[idx], 4),
            "polarity": _polarity(means[idx]),
            "function": meta["function"],
            "type": meta["type"],
            "mechanism": meta["mechanism"],
            "what": meta.get("what_en", ""),
            "analogy": meta.get("analogy_en", ""),
        }

    return {
        "track_id": track.get("id", ""),
        "beliefs": result_beliefs,
    }
