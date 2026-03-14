"""Radar 2 — "How It Feels" (Emotional Feel, 5D).

Each function computes one dimension from beliefs → (B, T).
Based on Russell's Circumplex, GEMS-9, Apple/Spotify moods,
and 2025 streaming engagement data.

Dimensions:
    0  mood           — Sad ↔ Happy
    1  energy         — Chill ↔ Hyped
    2  hardness       — Soft ↔ Hard
    3  predictability — Surprising ↔ Predictable
    4  focus          — Dreamy ↔ Focused
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Tuple

if TYPE_CHECKING:
    from torch import Tensor

# ── Belief index constants ──────────────────────────────────────────

# F1 Sensory
_HARMONIC_STABILITY = 4         # consonance / stability
_SPECTRAL_COMPLEXITY = 16       # acoustic density

# F2 Prediction
_PREDICTION_ACCURACY = 20       # how well model predicts
_INFORMATION_CONTENT = 25       # Shannon surprise / unexpectedness

# F3 Attention
_SALIENCE_NETWORK = 34          # attention-grabbing intensity
_SENSORY_LOAD = 35              # cognitive resource demand
_SELECTIVE_GAIN = 46            # selective attention focusing

# F5 Emotion
_ANS_DOMINANCE = 60             # autonomic arousal
_EMOTIONAL_AROUSAL = 63         # felt activation
_PERCEIVED_HAPPY = 67           # perceived happiness
_PERCEIVED_SAD = 68             # perceived sadness

# F6 Reward
_HARMONIC_TENSION = 80          # harmonic dissonance
_LIKING = 81                    # hedonic tone
_PREDICTION_ERROR = 84          # prediction error (F6/SRP)
_TENSION = 88                   # felt tension
_WANTING = 89                   # reward anticipation

# F8 Learning
_STATISTICAL_MODEL = 109        # statistical learning model (F8/SLEE)


def compute_mood(beliefs: Tensor) -> Tensor:
    """Mood — Sad ↔ Happy.

    Russell's #1 dimension. Apple, Spotify, GEMS all validate.
    >85% within-culture agreement, >70% cross-cultural (Fritz 2009).

    Sources:
        - b67 perceived_happy / b68 perceived_sad: direct percepts
        - b4 harmonic_stability: consonance → positive valence
        - b89 wanting: reward tone
        - b81 liking: hedonic tone
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    stability = beliefs[:, :, _HARMONIC_STABILITY]
    wanting = beliefs[:, :, _WANTING]
    liking = beliefs[:, :, _LIKING]

    mood = 0.30 * happy - 0.20 * sad + 0.15 * stability + 0.15 * wanting + 0.10 * liking
    return (mood + 0.20).clamp(0, 1)


def compute_energy(beliefs: Tensor) -> Tensor:
    """Energy — Chill ↔ Hyped.

    Russell's #2 dimension (arousal). Maps to activity:
    study, workout, party, sleep.

    Sources:
        - b63 emotional_arousal: felt activation level
        - b60 ans_dominance: autonomic nervous system arousal
        - b34 salience_network_activation: alerting / attention demand
    """
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    ans = beliefs[:, :, _ANS_DOMINANCE]
    salience = beliefs[:, :, _SALIENCE_NETWORK]

    return (0.40 * arousal + 0.35 * ans + 0.25 * salience).clamp(0, 1)


def compute_hardness(beliefs: Tensor) -> Tensor:
    """Hardness — Soft ↔ Hard.

    #1 streaming engagement mood (20% romantic/tender).
    Soft rock vs hard rock — a 5-year-old understands.
    GEMS "tenderness" dimension maps here.

    Sources:
        - b88 tension: felt tension / aggression
        - b80 harmonic_tension: harmonic dissonance (hard = dissonant)
        - b63 emotional_arousal: arousal amplifies hardness
        - b60 ans_dominance: bodily tension response
    """
    tension = beliefs[:, :, _TENSION]
    h_tension = beliefs[:, :, _HARMONIC_TENSION]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    ans = beliefs[:, :, _ANS_DOMINANCE]

    return (0.30 * tension + 0.25 * h_tension + 0.25 * arousal + 0.20 * ans).clamp(0, 1)


def compute_predictability(beliefs: Tensor) -> Tensor:
    """Predictability — Surprising ↔ Predictable.

    Objective, computable from audio (entropy, prediction error).
    "Did that chord change catch me off guard?"

    Sources:
        - b20 prediction_accuracy: model confidence in next event
        - b109 statistical_model: learned pattern model (F8/SLEE)
        - b25 information_content: Shannon surprise (INVERTED)
        - b84 prediction_error: prediction error (INVERTED, F6/SRP)
    """
    accuracy = beliefs[:, :, _PREDICTION_ACCURACY]
    stat_model = beliefs[:, :, _STATISTICAL_MODEL]
    surprise = beliefs[:, :, _INFORMATION_CONTENT]
    pred_error = beliefs[:, :, _PREDICTION_ERROR]

    # High accuracy + stat_model = predictable; high surprise = unpredictable
    return (0.30 * accuracy + 0.30 * stat_model - 0.20 * surprise - 0.10 * pred_error + 0.30).clamp(0, 1)


def compute_focus(beliefs: Tensor) -> Tensor:
    """Focus — Dreamy ↔ Focused.

    Apple Music top-5 mood. Fastest growing category (lofi/ambient).
    Practical daily use: study vs daydream.

    Sources:
        - b46 selective_gain: attentional sharpness
        - b35 sensory_load: cognitive engagement (focused = loaded)
        - b16 spectral_complexity: sparse = dreamy, dense = focused
    """
    gain = beliefs[:, :, _SELECTIVE_GAIN]
    load = beliefs[:, :, _SENSORY_LOAD]
    spectral = beliefs[:, :, _SPECTRAL_COMPLEXITY]

    return (0.40 * gain + 0.35 * load + 0.25 * spectral).clamp(0, 1)


# ======================================================================
# Ordered model list — canonical order matching 5D tensor indices
# ======================================================================

EMOTIONAL_MODELS: Tuple[Callable[..., Tensor], ...] = (
    compute_mood,           # 0
    compute_energy,         # 1
    compute_hardness,       # 2
    compute_predictability, # 3
    compute_focus,          # 4
)

EMOTIONAL_NAMES = ("mood", "energy", "hardness", "predictability", "focus")
EMOTIONAL_LABELS = {
    "mood":           {"low": "Sad",       "high": "Happy"},
    "energy":         {"low": "Chill",     "high": "Hyped"},
    "hardness":       {"low": "Soft",      "high": "Hard"},
    "predictability": {"low": "Surprising","high": "Predictable"},
    "focus":          {"low": "Dreamy",    "high": "Focused"},
}
