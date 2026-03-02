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

DIM_6D = ["energy", "valence", "tempo", "tension", "groove", "complexity"]

DIM_12D = [
    "melodic_hook", "harmonic_depth", "rhythmic_drive", "timbral_color",
    "emotional_arc", "surprise", "momentum", "narrative",
    "familiarity", "pleasure", "space", "repetition",
]

DIM_24D = [
    "prediction_error", "precision", "information_content", "model_uncertainty",
    "oscillation_coupling", "motor_period_lock", "auditory_motor_bind", "timing_precision",
    "valence_mode", "autonomic_arousal", "nostalgia_circuit", "chills_pathway",
    "da_anticipation", "da_consummation", "hedonic_tone", "reward_pe",
    "episodic_encoding", "autobiographical", "statistical_learning", "expertise_effect",
    "neural_synchrony", "social_bonding", "social_prediction", "collective_reward",
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


def get_listening_profile() -> dict[str, Any]:
    """Build user's listening profile from catalog categories.

    Returns summary of: recently played, saved/liked, top tracks,
    genre/family distribution, and overall gene centroid.
    """
    catalog = load_catalog()
    tracks = catalog.get("tracks", [])

    recently_played: list[dict] = []
    saved_tracks: list[dict] = []
    top_tracks: list[dict] = []

    family_counts: dict[str, int] = {}
    gene_sums: dict[str, float] = {
        "entropy": 0, "resolution": 0, "tension": 0,
        "resonance": 0, "plasticity": 0,
    }
    n = 0

    for t in tracks:
        cats = t.get("categories", [])
        entry = {
            "id": t["id"],
            "artist": t.get("artist", ""),
            "title": t.get("title", ""),
            "dominant_family": t.get("dominant_family", ""),
            "dominant_gene": t.get("dominant_gene", ""),
        }

        if "Recently Played" in cats:
            recently_played.append(entry)
        if "Saved Tracks" in cats:
            saved_tracks.append(entry)
        if "Top Tracks" in cats:
            top_tracks.append(entry)

        fam = t.get("dominant_family", "")
        if fam:
            family_counts[fam] = family_counts.get(fam, 0) + 1

        genes = t.get("genes", {})
        if genes:
            for g in gene_sums:
                gene_sums[g] += genes.get(g, 0.5)
            n += 1

    # Compute average gene profile
    avg_genes = {g: round(v / max(n, 1), 3) for g, v in gene_sums.items()}

    # Sort families by count
    top_families = sorted(family_counts.items(), key=lambda x: -x[1])

    return {
        "total_tracks": len(tracks),
        "recently_played": recently_played[:20],
        "recently_played_count": len(recently_played),
        "saved_tracks": saved_tracks[:20],
        "saved_count": len(saved_tracks),
        "top_tracks": top_tracks[:20],
        "top_count": len(top_tracks),
        "family_distribution": dict(top_families),
        "average_gene_profile": avg_genes,
    }


def load_beliefs_full(track_id: str) -> dict | None:
    """Load frame-level beliefs_full JSON for a track."""
    path = TRACKS_DIR / f"{track_id}_beliefs_full.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def get_belief_timeline(
    track_id: str,
    belief_keys: list[str] | None = None,
    n_points: int = 16,
) -> dict[str, Any]:
    """Downsample beliefs_full into compact LLM-friendly trajectories.

    Returns per-belief: n_points values, peak/valley with timestamps.
    """
    _ensure_belief_keys()
    bf = load_beliefs_full(track_id)
    if not bf:
        return {"error": f"No beliefs_full data for '{track_id}'."}

    duration = bf.get("duration_s", 30.0)

    # Flatten all beliefs across F1-F9
    all_b: dict[str, dict] = {}
    for fdata in bf.get("functions", {}).values():
        for bk, bv in fdata.get("beliefs", {}).items():
            all_b[bk] = bv

    # Pick belief keys: explicit or top-10 notable
    if not belief_keys:
        track = load_track(track_id)
        if track:
            means = track.get("beliefs", {}).get("means", [])
            stds = track.get("beliefs", {}).get("stds", [])
            if means and stds:
                scored = sorted(
                    range(len(means)),
                    key=lambda i: -(abs(means[i] - 0.5) * 0.6 + min(stds[i] * 10, 1.0) * 0.4),
                )
                belief_keys = [belief_index_to_key(i) for i in scored[:10]]
        if not belief_keys:
            belief_keys = list(all_b.keys())[:10]

    time_labels = [round(i * duration / n_points, 1) for i in range(n_points)]
    result: dict[str, Any] = {
        "track_id": track_id, "duration_s": duration,
        "n_points": n_points, "time_labels_s": time_labels, "beliefs": {},
    }

    for bk in belief_keys:
        bd = all_b.get(bk)
        if not bd:
            result["beliefs"][bk] = {"error": "not found"}
            continue
        frames = bd.get("frames", [])
        if not frames:
            continue
        nf = len(frames)
        bs = max(1, nf // n_points)
        traj = []
        for i in range(n_points):
            chunk = frames[i * bs: min((i + 1) * bs, nf)]
            traj.append(round(sum(chunk) / len(chunk), 4) if chunk else 0.0)

        peak_i = max(range(nf), key=lambda j: frames[j])
        valley_i = min(range(nf), key=lambda j: frames[j])
        meta = get_belief_meta(bk)
        result["beliefs"][bk] = {
            "trajectory": traj,
            "mean": round(sum(frames) / nf, 4),
            "peak": {"time_s": round(peak_i * duration / nf, 1), "value": round(frames[peak_i], 4)},
            "valley": {"time_s": round(valley_i * duration / nf, 1), "value": round(frames[valley_i], 4)},
            "function": meta.get("function", ""),
            "type": bd.get("type", meta.get("type", "")),
            "mechanism": bd.get("mechanism", meta.get("mechanism", "")),
        }

    return result


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
        n_segs = tp.get("segments", len(segs))
        duration = track.get("duration_s", 0)
        seg_dur = round(duration / max(n_segs, 1), 1) if duration else 0

        # Top notable beliefs → temporal arcs (top 15 instead of just 5)
        _ensure_belief_keys()
        notable = _top_beliefs(means, stds, n=15)
        arcs = {}
        for b in notable:
            meta = get_belief_meta(b["key"])
            idx = meta.get("index", -1) if meta else -1
            if 0 <= idx < len(means):
                arcs[b["key"]] = _temporal_arc(segs, idx)
        result["temporal_arcs"] = arcs
        result["temporal_segments"] = n_segs
        result["segment_duration_s"] = seg_dur

        # Neurochemical temporal arcs
        neuro_segs = tp.get("neuro_per_segment", [])
        if neuro_segs:
            result["neuro_temporal"] = {
                "DA": [round(s[0], 3) for s in neuro_segs],
                "NE": [round(s[1], 3) for s in neuro_segs],
                "OPI": [round(s[2], 3) for s in neuro_segs],
                "5HT": [round(s[3], 3) for s in neuro_segs],
            }

        # Reward temporal arc
        rew_segs = tp.get("reward_per_segment", [])
        if rew_segs:
            result["reward_temporal"] = [round(r, 3) for r in rew_segs]

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
