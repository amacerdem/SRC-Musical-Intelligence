"""Spotify → MI Feature Bridge.

Maps Spotify audio features + artist genres to MI-compatible format:
  signal(8D) → genes(5D) → dimensions(6D/12D/24D) → persona

When Spotify audio_features endpoint is unavailable (403), falls back to
genre-based heuristic signal profiles calibrated from the 138-track MI dataset.
"""
from __future__ import annotations

import math
from typing import Any

# ── Genre → MI Signal heuristic profiles ────────────────────────────
# Calibrated from 138-track MI dataset v4.0 ground truth.
# Keys: signal fields (energy, valence, tempo, danceability, acousticness,
#        harmonicComplexity, timbralBrightness)

GENRE_SIGNAL_PROFILES: dict[str, dict[str, float]] = {
    "electronic":   {"energy": 0.78, "valence": 0.55, "tempo": 0.65, "danceability": 0.82, "acousticness": 0.12, "harmonicComplexity": 0.45, "timbralBrightness": 0.72},
    "dance":        {"energy": 0.80, "valence": 0.62, "tempo": 0.62, "danceability": 0.88, "acousticness": 0.08, "harmonicComplexity": 0.35, "timbralBrightness": 0.75},
    "edm":          {"energy": 0.85, "valence": 0.58, "tempo": 0.65, "danceability": 0.85, "acousticness": 0.05, "harmonicComplexity": 0.40, "timbralBrightness": 0.80},
    "house":        {"energy": 0.75, "valence": 0.60, "tempo": 0.62, "danceability": 0.85, "acousticness": 0.10, "harmonicComplexity": 0.38, "timbralBrightness": 0.70},
    "techno":       {"energy": 0.82, "valence": 0.42, "tempo": 0.65, "danceability": 0.78, "acousticness": 0.05, "harmonicComplexity": 0.42, "timbralBrightness": 0.78},
    "classical":    {"energy": 0.35, "valence": 0.42, "tempo": 0.40, "danceability": 0.18, "acousticness": 0.85, "harmonicComplexity": 0.75, "timbralBrightness": 0.30},
    "jazz":         {"energy": 0.42, "valence": 0.58, "tempo": 0.45, "danceability": 0.55, "acousticness": 0.70, "harmonicComplexity": 0.80, "timbralBrightness": 0.35},
    "rock":         {"energy": 0.72, "valence": 0.48, "tempo": 0.55, "danceability": 0.52, "acousticness": 0.25, "harmonicComplexity": 0.45, "timbralBrightness": 0.65},
    "metal":        {"energy": 0.88, "valence": 0.30, "tempo": 0.60, "danceability": 0.35, "acousticness": 0.08, "harmonicComplexity": 0.55, "timbralBrightness": 0.85},
    "pop":          {"energy": 0.65, "valence": 0.68, "tempo": 0.55, "danceability": 0.72, "acousticness": 0.30, "harmonicComplexity": 0.30, "timbralBrightness": 0.55},
    "hip-hop":      {"energy": 0.70, "valence": 0.50, "tempo": 0.50, "danceability": 0.78, "acousticness": 0.15, "harmonicComplexity": 0.35, "timbralBrightness": 0.60},
    "rap":          {"energy": 0.72, "valence": 0.48, "tempo": 0.52, "danceability": 0.75, "acousticness": 0.12, "harmonicComplexity": 0.30, "timbralBrightness": 0.62},
    "r&b":          {"energy": 0.55, "valence": 0.62, "tempo": 0.48, "danceability": 0.70, "acousticness": 0.35, "harmonicComplexity": 0.50, "timbralBrightness": 0.45},
    "soul":         {"energy": 0.50, "valence": 0.65, "tempo": 0.45, "danceability": 0.62, "acousticness": 0.45, "harmonicComplexity": 0.55, "timbralBrightness": 0.40},
    "folk":         {"energy": 0.38, "valence": 0.55, "tempo": 0.42, "danceability": 0.45, "acousticness": 0.82, "harmonicComplexity": 0.40, "timbralBrightness": 0.28},
    "ambient":      {"energy": 0.20, "valence": 0.45, "tempo": 0.30, "danceability": 0.15, "acousticness": 0.75, "harmonicComplexity": 0.50, "timbralBrightness": 0.20},
    "experimental": {"energy": 0.55, "valence": 0.40, "tempo": 0.50, "danceability": 0.30, "acousticness": 0.40, "harmonicComplexity": 0.70, "timbralBrightness": 0.55},
    "indie":        {"energy": 0.55, "valence": 0.52, "tempo": 0.50, "danceability": 0.55, "acousticness": 0.40, "harmonicComplexity": 0.45, "timbralBrightness": 0.50},
    "punk":         {"energy": 0.82, "valence": 0.45, "tempo": 0.62, "danceability": 0.48, "acousticness": 0.10, "harmonicComplexity": 0.25, "timbralBrightness": 0.78},
    "blues":        {"energy": 0.45, "valence": 0.42, "tempo": 0.42, "danceability": 0.50, "acousticness": 0.60, "harmonicComplexity": 0.55, "timbralBrightness": 0.38},
    "country":      {"energy": 0.55, "valence": 0.62, "tempo": 0.48, "danceability": 0.58, "acousticness": 0.55, "harmonicComplexity": 0.35, "timbralBrightness": 0.45},
    "latin":        {"energy": 0.72, "valence": 0.70, "tempo": 0.55, "danceability": 0.80, "acousticness": 0.30, "harmonicComplexity": 0.40, "timbralBrightness": 0.55},
    "reggae":       {"energy": 0.55, "valence": 0.65, "tempo": 0.45, "danceability": 0.72, "acousticness": 0.35, "harmonicComplexity": 0.35, "timbralBrightness": 0.42},
    "world":        {"energy": 0.50, "valence": 0.55, "tempo": 0.48, "danceability": 0.55, "acousticness": 0.50, "harmonicComplexity": 0.55, "timbralBrightness": 0.45},
    "singer-songwriter": {"energy": 0.38, "valence": 0.52, "tempo": 0.42, "danceability": 0.42, "acousticness": 0.78, "harmonicComplexity": 0.42, "timbralBrightness": 0.30},
}

_DEFAULT_SIGNAL = {"energy": 0.50, "valence": 0.50, "tempo": 0.50, "danceability": 0.50, "acousticness": 0.50, "harmonicComplexity": 0.45, "timbralBrightness": 0.50}

# ── 24 Persona definitions (gene profiles) ─────────────────────────
# Frozen v1.0 — matches My Musical Mind (Monetizing)/src/data/personas.ts

PERSONAS: list[dict[str, Any]] = [
    {"id": 1,  "name": "Dopamine Seeker",     "family": "Alchemists",  "genes": {"entropy": 0.30, "resolution": 0.25, "tension": 0.85, "resonance": 0.45, "plasticity": 0.35}},
    {"id": 6,  "name": "Tension Architect",    "family": "Alchemists",  "genes": {"entropy": 0.35, "resolution": 0.50, "tension": 0.92, "resonance": 0.20, "plasticity": 0.25}},
    {"id": 7,  "name": "Contrast Addict",      "family": "Alchemists",  "genes": {"entropy": 0.50, "resolution": 0.25, "tension": 0.75, "resonance": 0.30, "plasticity": 0.40}},
    {"id": 18, "name": "Dramatic Arc",          "family": "Alchemists",  "genes": {"entropy": 0.25, "resolution": 0.45, "tension": 0.85, "resonance": 0.55, "plasticity": 0.20}},
    {"id": 2,  "name": "Harmonic Purist",       "family": "Architects",  "genes": {"entropy": 0.10, "resolution": 0.90, "tension": 0.15, "resonance": 0.40, "plasticity": 0.15}},
    {"id": 4,  "name": "Minimal Zen",           "family": "Architects",  "genes": {"entropy": 0.10, "resolution": 0.70, "tension": 0.10, "resonance": 0.50, "plasticity": 0.20}},
    {"id": 5,  "name": "Resolution Junkie",     "family": "Architects",  "genes": {"entropy": 0.15, "resolution": 0.95, "tension": 0.40, "resonance": 0.30, "plasticity": 0.15}},
    {"id": 9,  "name": "Pattern Hunter",        "family": "Architects",  "genes": {"entropy": 0.30, "resolution": 0.80, "tension": 0.20, "resonance": 0.20, "plasticity": 0.25}},
    {"id": 20, "name": "Precision Mind",         "family": "Architects",  "genes": {"entropy": 0.10, "resolution": 0.85, "tension": 0.20, "resonance": 0.15, "plasticity": 0.35}},
    {"id": 3,  "name": "Chaos Explorer",         "family": "Explorers",   "genes": {"entropy": 0.92, "resolution": 0.10, "tension": 0.45, "resonance": 0.10, "plasticity": 0.30}},
    {"id": 10, "name": "Sonic Nomad",            "family": "Explorers",   "genes": {"entropy": 0.85, "resolution": 0.10, "tension": 0.35, "resonance": 0.15, "plasticity": 0.40}},
    {"id": 19, "name": "Curious Wanderer",       "family": "Explorers",   "genes": {"entropy": 0.70, "resolution": 0.25, "tension": 0.25, "resonance": 0.35, "plasticity": 0.30}},
    {"id": 23, "name": "Edge Runner",            "family": "Explorers",   "genes": {"entropy": 0.88, "resolution": 0.08, "tension": 0.50, "resonance": 0.10, "plasticity": 0.25}},
    {"id": 24, "name": "Renaissance Mind",       "family": "Explorers",   "genes": {"entropy": 0.65, "resolution": 0.50, "tension": 0.45, "resonance": 0.45, "plasticity": 0.45}},
    {"id": 8,  "name": "Structural Romantic",    "family": "Anchors",     "genes": {"entropy": 0.15, "resolution": 0.45, "tension": 0.35, "resonance": 0.80, "plasticity": 0.20}},
    {"id": 11, "name": "Emotional Anchor",       "family": "Anchors",     "genes": {"entropy": 0.15, "resolution": 0.25, "tension": 0.30, "resonance": 0.90, "plasticity": 0.20}},
    {"id": 13, "name": "Tonal Dreamer",          "family": "Anchors",     "genes": {"entropy": 0.15, "resolution": 0.30, "tension": 0.10, "resonance": 0.75, "plasticity": 0.15}},
    {"id": 15, "name": "Quiet Observer",          "family": "Anchors",     "genes": {"entropy": 0.15, "resolution": 0.35, "tension": 0.12, "resonance": 0.72, "plasticity": 0.15}},
    {"id": 17, "name": "Ambient Flow",            "family": "Anchors",     "genes": {"entropy": 0.15, "resolution": 0.10, "tension": 0.08, "resonance": 0.80, "plasticity": 0.20}},
    {"id": 22, "name": "Nostalgic Soul",           "family": "Anchors",     "genes": {"entropy": 0.10, "resolution": 0.35, "tension": 0.10, "resonance": 0.85, "plasticity": 0.20}},
    {"id": 12, "name": "Rhythmic Pulse",           "family": "Kineticists", "genes": {"entropy": 0.30, "resolution": 0.20, "tension": 0.25, "resonance": 0.25, "plasticity": 0.85}},
    {"id": 14, "name": "Dynamic Storm",            "family": "Kineticists", "genes": {"entropy": 0.55, "resolution": 0.30, "tension": 0.60, "resonance": 0.15, "plasticity": 0.80}},
    {"id": 16, "name": "Groove Mechanic",           "family": "Kineticists", "genes": {"entropy": 0.20, "resolution": 0.40, "tension": 0.20, "resonance": 0.20, "plasticity": 0.88}},
    {"id": 21, "name": "Raw Energy",                "family": "Kineticists", "genes": {"entropy": 0.45, "resolution": 0.10, "tension": 0.40, "resonance": 0.15, "plasticity": 0.78}},
]

GENE_NAMES = ("entropy", "resolution", "tension", "resonance", "plasticity")

GENE_TO_FAMILY: dict[str, str] = {
    "entropy": "Explorers",
    "resolution": "Architects",
    "tension": "Alchemists",
    "resonance": "Anchors",
    "plasticity": "Kineticists",
}

FAMILY_TO_GENE: dict[str, str] = {v: k for k, v in GENE_TO_FAMILY.items()}


# ── Helpers ─────────────────────────────────────────────────────────

def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _shannon_entropy(distribution: dict[str, int]) -> float:
    """Normalized Shannon entropy of a count distribution."""
    total = sum(distribution.values())
    if total == 0:
        return 0.0
    probs = [c / total for c in distribution.values() if c > 0]
    h = -sum(p * math.log2(p) for p in probs)
    max_h = math.log2(len(probs)) if len(probs) > 1 else 1.0
    return h / max_h if max_h > 0 else 0.0


# ── A) Spotify Audio Features → MI Signal ───────────────────────────

def spotify_features_to_signal(
    sp: dict[str, float],
    duration_ms: float,
) -> dict[str, float]:
    """Map Spotify audio_features to MI signal (8D)."""
    return {
        "energy": _clamp(sp.get("energy", 0.5)),
        "valence": _clamp(sp.get("valence", 0.5)),
        "tempo": _clamp(sp.get("tempo", 120) / 200),
        "danceability": _clamp(sp.get("danceability", 0.5)),
        "acousticness": _clamp(sp.get("acousticness", 0.5)),
        "harmonicComplexity": _clamp(
            sp.get("instrumentalness", 0.5) * 0.7
            + (1 - sp.get("speechiness", 0.5)) * 0.3
        ),
        "timbralBrightness": _clamp(
            sp.get("energy", 0.5) * 0.5
            + (1 - sp.get("acousticness", 0.5)) * 0.5
        ),
        "duration": _clamp(duration_ms / 600_000),
    }


# ── B) Genre → MI Signal (fallback heuristic) ──────────────────────

def genres_to_signal(genres: list[str], duration_ms: float) -> dict[str, float]:
    """Blend genre-based signal profiles for a track when audio features unavailable."""
    if not genres:
        return {**_DEFAULT_SIGNAL, "duration": _clamp(duration_ms / 600_000)}

    matched: list[dict[str, float]] = []
    for genre in genres:
        g_lower = genre.lower()
        for key, profile in GENRE_SIGNAL_PROFILES.items():
            if key in g_lower:
                matched.append(profile)
                break

    if not matched:
        return {**_DEFAULT_SIGNAL, "duration": _clamp(duration_ms / 600_000)}

    n = len(matched)
    blended = {}
    for field in ("energy", "valence", "tempo", "danceability", "acousticness", "harmonicComplexity", "timbralBrightness"):
        blended[field] = sum(p[field] for p in matched) / n
    blended["duration"] = _clamp(duration_ms / 600_000)
    return blended


# ── C) Signal → Genes ───────────────────────────────────────────────

def signal_to_genes(
    signal: dict[str, float],
    genre_novelty: float = 0.5,
    familiarity: float = 0.5,
    rhythmic_variety: float = 0.5,
    harmonic_indicator: float = 0.5,
) -> dict[str, float]:
    """Derive 5 mind genes from MI signal + contextual indicators."""
    e = signal.get("energy", 0.5)
    v = signal.get("valence", 0.5)
    d = signal.get("danceability", 0.5)
    a = signal.get("acousticness", 0.5)
    hc = signal.get("harmonicComplexity", 0.5)
    tb = signal.get("timbralBrightness", 0.5)
    t = signal.get("tempo", 0.5)

    return {
        "entropy":     _clamp(e * 0.30 + (1 - a) * 0.30 + tb * 0.20 + genre_novelty * 0.20),
        "resolution":  _clamp(a * 0.30 + hc * 0.30 + (1 - e) * 0.20 + harmonic_indicator * 0.20),
        "tension":     _clamp(e * 0.35 + (1 - v) * 0.35 + (1 - d) * 0.15 + tb * 0.15),
        "resonance":   _clamp(v * 0.35 + a * 0.25 + (1 - e) * 0.20 + familiarity * 0.20),
        "plasticity":  _clamp(d * 0.35 + t * 0.25 + e * 0.20 + rhythmic_variety * 0.20),
    }


# ── D) Genes → Dimensions ──────────────────────────────────────────

def genes_to_dim_6d(genes: dict[str, float]) -> list[float]:
    """Map genes to 6D psychology dimensions."""
    en = genes["entropy"]
    re = genes["resolution"]
    te = genes["tension"]
    rs = genes["resonance"]
    pl = genes["plasticity"]
    return [
        _clamp(te * 0.5 + en * 0.3 + pl * 0.2),         # energy
        _clamp(rs * 0.5 + re * 0.3 + (1 - te) * 0.2),   # valence
        _clamp(pl * 0.5 + en * 0.3 + te * 0.2),          # tempo
        _clamp(te * 0.5 + en * 0.3 + (1 - re) * 0.2),   # tension
        _clamp(pl * 0.5 + rs * 0.2 + en * 0.3),          # groove
        _clamp(en * 0.4 + re * 0.3 + te * 0.3),          # complexity
    ]


def genes_to_dim_12d(genes: dict[str, float]) -> list[float]:
    """Map genes to 12D cognition dimensions."""
    en = genes["entropy"]
    re = genes["resolution"]
    te = genes["tension"]
    rs = genes["resonance"]
    pl = genes["plasticity"]
    return [
        _clamp(rs * 0.4 + re * 0.4 + (1 - en) * 0.2),   # melodic_hook
        _clamp(re * 0.5 + rs * 0.3 + (1 - en) * 0.2),   # harmonic_depth
        _clamp(pl * 0.5 + en * 0.3 + te * 0.2),          # rhythmic_drive
        _clamp(en * 0.4 + te * 0.3 + pl * 0.3),          # timbral_color
        _clamp(rs * 0.5 + te * 0.3 + (1 - en) * 0.2),   # emotional_arc
        _clamp(en * 0.5 + te * 0.3 + (1 - re) * 0.2),   # surprise
        _clamp(pl * 0.4 + te * 0.3 + en * 0.3),          # momentum
        _clamp(te * 0.4 + rs * 0.3 + re * 0.3),          # narrative
        _clamp(rs * 0.4 + (1 - en) * 0.4 + re * 0.2),   # familiarity
        _clamp(rs * 0.4 + re * 0.3 + pl * 0.3),          # pleasure
        _clamp(en * 0.4 + (1 - pl) * 0.3 + re * 0.3),   # space
        _clamp((1 - en) * 0.5 + pl * 0.3 + rs * 0.2),   # repetition
    ]


def genes_to_dim_24d(genes: dict[str, float]) -> list[float]:
    """Map genes to 24D neuroscience dimensions."""
    en = genes["entropy"]
    re = genes["resolution"]
    te = genes["tension"]
    rs = genes["resonance"]
    pl = genes["plasticity"]
    return [
        _clamp(en * 0.5 + te * 0.3 + (1 - re) * 0.2),   # prediction_error
        _clamp(re * 0.5 + (1 - en) * 0.3 + rs * 0.2),   # precision
        _clamp(en * 0.4 + re * 0.3 + te * 0.3),          # information_content
        _clamp(en * 0.5 + (1 - re) * 0.3 + te * 0.2),   # model_uncertainty
        _clamp(pl * 0.4 + re * 0.3 + rs * 0.3),          # oscillation_coupling
        _clamp(pl * 0.5 + (1 - en) * 0.3 + re * 0.2),   # motor_period_lock
        _clamp(pl * 0.4 + rs * 0.3 + re * 0.3),          # auditory_motor_bind
        _clamp(pl * 0.4 + re * 0.4 + (1 - en) * 0.2),   # timing_precision
        _clamp(rs * 0.5 + (1 - te) * 0.3 + re * 0.2),   # valence_mode
        _clamp(te * 0.4 + en * 0.3 + pl * 0.3),          # autonomic_arousal
        _clamp(rs * 0.5 + (1 - en) * 0.3 + re * 0.2),   # nostalgia_circuit
        _clamp(rs * 0.3 + te * 0.3 + en * 0.2 + re * 0.2),  # chills_pathway
        _clamp(en * 0.4 + te * 0.3 + pl * 0.3),          # da_anticipation
        _clamp(re * 0.4 + rs * 0.3 + (1 - te) * 0.3),   # da_consummation
        _clamp(rs * 0.5 + re * 0.3 + (1 - te) * 0.2),   # hedonic_tone
        _clamp(en * 0.4 + te * 0.3 + (1 - re) * 0.3),   # reward_pe
        _clamp(rs * 0.4 + en * 0.3 + re * 0.3),          # episodic_encoding
        _clamp(rs * 0.5 + (1 - en) * 0.3 + re * 0.2),   # autobiographical
        _clamp(re * 0.4 + (1 - en) * 0.3 + pl * 0.3),   # statistical_learning
        _clamp(re * 0.4 + pl * 0.3 + (1 - en) * 0.3),   # expertise_effect
        _clamp(pl * 0.4 + rs * 0.3 + re * 0.3),          # neural_synchrony
        _clamp(rs * 0.5 + pl * 0.3 + (1 - te) * 0.2),   # social_bonding
        _clamp(re * 0.4 + rs * 0.3 + en * 0.3),          # social_prediction
        _clamp(rs * 0.4 + pl * 0.3 + re * 0.3),          # collective_reward
    ]


# ── E) Genes → Dominant family/gene ─────────────────────────────────

def get_dominant(genes: dict[str, float]) -> tuple[str, str]:
    """Return (dominant_family, dominant_gene) from gene dict."""
    best_gene = max(GENE_NAMES, key=lambda g: genes.get(g, 0))
    return GENE_TO_FAMILY[best_gene], best_gene


# ── F) Genes → Persona matching ─────────────────────────────────────

def derive_persona(genes: dict[str, float]) -> dict[str, Any]:
    """Find best-matching persona from genes (same algo as frontend)."""
    best_id = 1
    best_score = -float("inf")
    best_persona: dict[str, Any] = PERSONAS[0]

    for p in PERSONAS:
        d_sq = sum((genes.get(g, 0.5) - p["genes"].get(g, 0.5)) ** 2 for g in GENE_NAMES)
        gene_sim = 1 - math.sqrt(d_sq) / math.sqrt(5)
        family_gene = FAMILY_TO_GENE.get(p["family"], "entropy")
        family_bonus = genes.get(family_gene, 0.5)
        score = gene_sim * 0.85 + family_bonus * 0.15
        if score > best_score:
            best_score = score
            best_id = p["id"]
            best_persona = p

    return best_persona


# ── G) Full profile computation ─────────────────────────────────────

def compute_user_profile(
    tracks: list[dict[str, Any]],
    artists: list[dict[str, Any]],
    spotify_user: dict[str, Any],
) -> dict[str, Any]:
    """Compute full MI profile from Spotify data.

    Parameters
    ----------
    tracks : list of track dicts with keys:
        id, name, artist, album_art, duration_ms, genres (from artist),
        audio_features (dict or None)
    artists : list of artist dicts with keys:
        id, name, genres, popularity
    spotify_user : dict with keys:
        id, display_name, product
    """
    if not tracks:
        default_genes = {g: 0.2 for g in GENE_NAMES}
        persona = derive_persona(default_genes)
        return {
            "spotify_user": spotify_user,
            "stats": {"total_tracks": 0, "total_minutes": 0, "unique_artists": 0, "unique_genres": 0},
            "genes": default_genes,
            "dominant_family": "Explorers",
            "dominant_gene": "entropy",
            "persona_id": persona["id"],
            "persona_name": persona["name"],
            "dimensions_6d": genes_to_dim_6d(default_genes),
            "dimensions_12d": genes_to_dim_12d(default_genes),
            "dimensions_24d": genes_to_dim_24d(default_genes),
            "family_distribution": {},
            "genre_distribution": {},
            "tracks": [],
            "listening_diversity": {"genre_entropy": 0, "artist_entropy": 0, "tempo_range": 0, "taste_shift": 0},
        }

    # Build artist genre lookup
    artist_genres: dict[str, list[str]] = {}
    for a in artists:
        artist_genres[a.get("name", "").lower()] = a.get("genres", [])

    # Compute genre/artist/family distributions
    genre_counts: dict[str, int] = {}
    artist_counts: dict[str, int] = {}
    family_counts: dict[str, int] = {}
    total_duration_ms = 0.0
    all_tempos: list[float] = []

    mi_tracks: list[dict[str, Any]] = []

    for t in tracks:
        dur_ms = t.get("duration_ms", 0)
        total_duration_ms += dur_ms
        artist_name = t.get("artist", "")
        genres = t.get("genres", []) or artist_genres.get(artist_name.lower(), [])

        # Count distributions
        artist_counts[artist_name] = artist_counts.get(artist_name, 0) + 1
        for g in genres:
            genre_counts[g] = genre_counts.get(g, 0) + 1

        # Signal
        af = t.get("audio_features")
        if af and af.get("energy") is not None:
            signal = spotify_features_to_signal(af, dur_ms)
            source = "spotify_audio_features"
        else:
            signal = genres_to_signal(genres, dur_ms)
            source = "genre_heuristic"

        if af and af.get("tempo"):
            all_tempos.append(af["tempo"])

        # Genre novelty = how uncommon this artist's genres are
        genre_novelty = 0.5
        if genres and genre_counts:
            max_count = max(genre_counts.values()) if genre_counts else 1
            avg_rarity = sum(1 - genre_counts.get(g, 0) / max(max_count, 1) for g in genres) / len(genres)
            genre_novelty = _clamp(avg_rarity)

        genes = signal_to_genes(signal, genre_novelty=genre_novelty)
        dom_family, dom_gene = get_dominant(genes)
        family_counts[dom_family] = family_counts.get(dom_family, 0) + 1

        mi_track = {
            "id": t.get("id", ""),
            "title": t.get("name", ""),
            "artist": artist_name,
            "album_art": t.get("album_art", ""),
            "duration_s": round(dur_ms / 1000, 1),
            "genres": genres,
            "signal": {k: round(v, 4) for k, v in signal.items()},
            "genes": {k: round(v, 4) for k, v in genes.items()},
            "dominant_family": dom_family,
            "dominant_gene": dom_gene,
            "dimensions_6d": [round(d, 4) for d in genes_to_dim_6d(genes)],
            "source": source,
        }
        mi_tracks.append(mi_track)

    # Duration-weighted aggregate genes
    agg_genes = {g: 0.0 for g in GENE_NAMES}
    if total_duration_ms > 0:
        for mt in mi_tracks:
            w = (mt["duration_s"] * 1000) / total_duration_ms
            for g in GENE_NAMES:
                agg_genes[g] += mt["genes"][g] * w
    else:
        for g in GENE_NAMES:
            agg_genes[g] = sum(mt["genes"][g] for mt in mi_tracks) / len(mi_tracks)

    agg_genes = {g: round(_clamp(v), 4) for g, v in agg_genes.items()}

    # Listening diversity metrics
    genre_entropy = _shannon_entropy(genre_counts)
    artist_entropy = _shannon_entropy(artist_counts)
    tempo_range = (max(all_tempos) - min(all_tempos)) / 200 if len(all_tempos) >= 2 else 0.0

    # Taste shift: how different are short-term vs long-term genes?
    # (Computed externally from time-range-tagged tracks — passed as 0 here, set by caller)
    taste_shift = 0.0

    dom_family, dom_gene = get_dominant(agg_genes)
    persona = derive_persona(agg_genes)

    unique_genres = set()
    for g_list in artist_genres.values():
        unique_genres.update(g_list)

    return {
        "spotify_user": spotify_user,
        "stats": {
            "total_tracks": len(mi_tracks),
            "total_minutes": round(total_duration_ms / 60_000, 1),
            "unique_artists": len(artist_counts),
            "unique_genres": len(unique_genres) or len(genre_counts),
        },
        "genes": agg_genes,
        "dominant_family": dom_family,
        "dominant_gene": dom_gene,
        "persona_id": persona["id"],
        "persona_name": persona["name"],
        "dimensions_6d": [round(d, 4) for d in genes_to_dim_6d(agg_genes)],
        "dimensions_12d": [round(d, 4) for d in genes_to_dim_12d(agg_genes)],
        "dimensions_24d": [round(d, 4) for d in genes_to_dim_24d(agg_genes)],
        "family_distribution": dict(sorted(family_counts.items(), key=lambda x: -x[1])),
        "genre_distribution": dict(sorted(genre_counts.items(), key=lambda x: -x[1])[:20]),
        "tracks": mi_tracks,
        "listening_diversity": {
            "genre_entropy": round(genre_entropy, 3),
            "artist_entropy": round(artist_entropy, 3),
            "tempo_range": round(tempo_range, 3),
            "taste_shift": round(taste_shift, 3),
        },
    }
