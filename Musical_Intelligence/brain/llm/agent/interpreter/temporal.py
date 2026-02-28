"""Temporal Arc Interpreter — 8-segment journey narrative.

Reads temporal_profile data (belief_means_per_segment) and produces
a narrative of how the musical experience evolves across the piece:
- Where tension builds
- Where climaxes occur
- Where resolution happens
- Turning points (tension→resolution, DA→OPI transitions)
"""

from __future__ import annotations

from typing import Any

from Musical_Intelligence.brain.llm.agent.track_data import (
    belief_index_to_key,
    get_belief_meta,
    _ensure_belief_keys,
)
from .polarity import classify_value

# ── Segment Labels ──────────────────────────────────────────────

_SEGMENT_LABELS = {
    "en": ["Opening", "Early", "Build-up", "Development", "Peak zone", "Transition", "Late", "Closing"],
    "tr": ["Açılış", "Erken", "Birikim", "Gelişme", "Doruk bölgesi", "Geçiş", "Geç", "Kapanış"],
}


def _segment_label(idx: int, total: int, language: str = "en") -> str:
    """Get a meaningful label for a segment position."""
    labels = _SEGMENT_LABELS.get(language, _SEGMENT_LABELS["en"])
    if total <= len(labels):
        return labels[idx] if idx < len(labels) else f"Segment {idx + 1}"
    return f"Segment {idx + 1}/{total}"


# ── Turning Point Detection ─────────────────────────────────────

def _detect_turning_points(
    segments: list[list[float]],
    belief_idx: int,
    min_delta: float = 0.08,
) -> list[dict]:
    """Find significant direction changes for a single belief across segments."""
    points: list[dict] = []
    for i in range(1, len(segments) - 1):
        if len(segments[i]) <= belief_idx:
            continue
        prev = segments[i - 1][belief_idx]
        curr = segments[i][belief_idx]
        nxt = segments[i + 1][belief_idx]

        rising_then_falling = (curr - prev > min_delta) and (nxt - curr < -min_delta)
        falling_then_rising = (prev - curr > min_delta) and (curr - nxt < -min_delta)

        if rising_then_falling:
            points.append({"segment": i, "type": "peak", "value": round(curr, 3)})
        elif falling_then_rising:
            points.append({"segment": i, "type": "trough", "value": round(curr, 3)})

    return points


# ── Segment Mood Detection ──────────────────────────────────────

def _segment_mood(
    segment_means: list[float],
    language: str = "en",
) -> str:
    """Determine overall mood label for a segment from key belief indices."""
    _ensure_belief_keys()

    # Key belief indices for mood detection (use safe defaults)
    key_beliefs = {}
    for name in ("wanting", "pleasure", "prediction_accuracy", "beat_entrainment",
                 "autobiographical_retrieval", "emotional_arousal"):
        meta = get_belief_meta(name)
        if meta and "index" in meta:
            idx = meta["index"]
            if idx < len(segment_means):
                key_beliefs[name] = segment_means[idx]

    wanting = key_beliefs.get("wanting", 0.5)
    pleasure = key_beliefs.get("pleasure", 0.5)
    pred_acc = key_beliefs.get("prediction_accuracy", 0.5)
    beat = key_beliefs.get("beat_entrainment", 0.5)
    memory = key_beliefs.get("autobiographical_retrieval", 0.5)
    arousal = key_beliefs.get("emotional_arousal", 0.5)

    moods = {
        "en": {
            "building": "Building tension",
            "climax": "Climax / Peak reward",
            "resolution": "Resolution / Satisfaction",
            "groove": "Groove lock",
            "nostalgia": "Memory / Nostalgia",
            "exploration": "Exploration",
            "calm": "Calm / Ambient",
            "neutral": "Steady state",
        },
        "tr": {
            "building": "Gerilim inşası",
            "climax": "Doruk / Zirve ödül",
            "resolution": "Çözüm / Tatmin",
            "groove": "Groove kilidi",
            "nostalgia": "Hafıza / Nostalji",
            "exploration": "Keşif",
            "calm": "Sakin / Ambient",
            "neutral": "Kararlı durum",
        },
    }
    labels = moods.get(language, moods["en"])

    if wanting > 0.65 and pleasure < 0.5:
        return labels["building"]
    if pleasure > 0.65 and wanting > 0.5:
        return labels["climax"]
    if pleasure > 0.6 and wanting < 0.4:
        return labels["resolution"]
    if beat > 0.65:
        return labels["groove"]
    if memory > 0.6:
        return labels["nostalgia"]
    if arousal > 0.6 and pred_acc < 0.4:
        return labels["exploration"]
    if arousal < 0.35:
        return labels["calm"]
    return labels["neutral"]


# ── Main Interpreter ─────────────────────────────────────────────


def interpret_temporal(
    temporal_profile: dict[str, Any],
    beliefs_means: list[float] | None = None,
    beliefs_stds: list[float] | None = None,
    language: str = "tr",
    tier: str = "free",
    focus_beliefs: list[str] | None = None,
) -> dict[str, Any]:
    """Interpret temporal arc across 8 segments.

    Args:
        temporal_profile: Dict with "belief_means_per_segment" and "segments".
        beliefs_means: Track-level belief means (for context).
        beliefs_stds: Track-level belief stds (for dynamics detection).
        language: "tr" or "en"
        tier: user tier
        focus_beliefs: Optional list of specific belief keys to track.

    Returns:
        Dict with "narrative", "highlights", "segments", "turning_points".
    """
    sfx = "tr" if language == "tr" else "en"
    segments_data = temporal_profile.get("belief_means_per_segment", [])
    n_segments = temporal_profile.get("segments", len(segments_data))

    if not segments_data or n_segments < 2:
        if language == "tr":
            return {"narrative": "Zamansal veri yetersiz — tek anlık analiz.", "highlights": [], "segments": [], "turning_points": []}
        return {"narrative": "Insufficient temporal data — single-moment analysis.", "highlights": [], "segments": [], "turning_points": []}

    _ensure_belief_keys()

    # Key belief indices to track
    tracked_beliefs: dict[str, int] = {}
    default_track = [
        "wanting", "pleasure", "harmonic_stability",
        "prediction_accuracy", "beat_entrainment", "autobiographical_retrieval",
    ]

    track_list = focus_beliefs or default_track
    for name in track_list:
        meta = get_belief_meta(name)
        if meta and "index" in meta:
            tracked_beliefs[name] = meta["index"]

    # Analyze each segment
    segment_info: list[dict] = []
    for i, seg in enumerate(segments_data):
        label = _segment_label(i, n_segments, language)
        mood = _segment_mood(seg, language)

        # Top rising and falling beliefs in this segment vs previous
        changes: list[dict] = []
        if i > 0:
            prev_seg = segments_data[i - 1]
            for name, idx in tracked_beliefs.items():
                if idx < len(seg) and idx < len(prev_seg):
                    delta = seg[idx] - prev_seg[idx]
                    if abs(delta) > 0.05:
                        meta = get_belief_meta(name)
                        changes.append({
                            "belief": name,
                            "delta": round(delta, 3),
                            "direction": "rising" if delta > 0 else "falling",
                            "function": meta.get("function", ""),
                        })
            changes.sort(key=lambda x: abs(x["delta"]), reverse=True)

        segment_info.append({
            "index": i,
            "label": label,
            "mood": mood,
            "top_changes": changes[:3],
        })

    # Detect turning points for key beliefs
    turning_points: list[dict] = []
    for name, idx in tracked_beliefs.items():
        points = _detect_turning_points(segments_data, idx)
        for pt in points:
            pt["belief"] = name
            meta = get_belief_meta(name)
            pt["function"] = meta.get("function", "")
            turning_points.append(pt)

    # Check for flat profile
    total_dynamics = sum(
        abs(c["delta"])
        for seg in segment_info
        for c in seg.get("top_changes", [])
    )

    # Build narrative
    parts: list[str] = []

    if total_dynamics < 0.3:
        # Flat profile
        if language == "tr":
            parts.append("**Zamansal profil**: Tutarlı bir deneyim — inançlar parça boyunca oldukça sabit kalıyor. Büyük gerilim-çözüm döngüleri yerine kararlı bir durum.")
        else:
            parts.append("**Temporal profile**: A consistent experience — beliefs remain fairly stable across the piece. A steady state rather than dramatic tension-resolution cycles.")
    else:
        # Dynamic profile — tell the journey
        if language == "tr":
            parts.append("**Zamansal yolculuk:**")
        else:
            parts.append("**Temporal journey:**")

        for seg in segment_info:
            mood_str = seg["mood"]
            changes = seg["top_changes"]
            if changes:
                change_str = ", ".join(
                    f"{c['belief']} {'↑' if c['direction'] == 'rising' else '↓'}"
                    for c in changes[:2]
                )
                parts.append(f"- **{seg['label']}**: {mood_str} ({change_str})")
            else:
                parts.append(f"- **{seg['label']}**: {mood_str}")

        # Turning points summary
        if turning_points:
            parts.append("")
            if language == "tr":
                parts.append("**Dönüm noktaları:**")
            else:
                parts.append("**Turning points:**")
            for tp in turning_points[:3]:
                seg_label = _segment_label(tp["segment"], n_segments, language)
                if language == "tr":
                    tp_type = "doruk" if tp["type"] == "peak" else "çukur"
                else:
                    tp_type = tp["type"]
                parts.append(f"- {tp['belief']} {tp_type} @ {seg_label}")

    # Highlights
    highlights: list[str] = []
    mood_sequence = [s["mood"] for s in segment_info]
    if len(set(mood_sequence)) > 3:
        if language == "tr":
            highlights.append("Çeşitli zamansal yolculuk — birden fazla mod geçişi")
        else:
            highlights.append("Diverse temporal journey — multiple mood transitions")
    if turning_points:
        if language == "tr":
            highlights.append(f"{len(turning_points)} dönüm noktası tespit edildi")
        else:
            highlights.append(f"{len(turning_points)} turning points detected")

    return {
        "narrative": "\n".join(parts),
        "highlights": highlights,
        "segments": segment_info,
        "turning_points": turning_points,
    }
