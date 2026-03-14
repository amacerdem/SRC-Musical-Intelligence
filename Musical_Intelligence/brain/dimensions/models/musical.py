"""Radar 1 — "What You Hear" (Musical Character, 5D).

Each function computes one dimension from beliefs → (B, T).
Every label passes the "would my mom say this?" test.

Dimensions:
    0  speed    — Slow ↔ Fast
    1  volume   — Quiet ↔ Loud
    2  weight   — Light ↔ Heavy
    3  texture  — Smooth ↔ Rough
    4  depth    — Thin ↔ Deep
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Tuple

if TYPE_CHECKING:
    from torch import Tensor

# ── Belief index constants ──────────────────────────────────────────

# F1 Sensory
_CONSONANCE_SALIENCE_GRADIENT = 0  # consonance gradient (smooth ↔ rough proxy)
_HARMONIC_STABILITY = 4            # consonance / stability
_SPECTRAL_COMPLEXITY = 16          # spectral density / acoustic richness
_TIMBRAL_CHARACTER = 15            # timbral brightness / character (F1/MIAA)

# F3 Attention
_SALIENCE_NETWORK = 34          # salience / intensity
_SENSORY_LOAD = 35              # cognitive resource demand
_ATTENTION_CAPTURE = 36         # involuntary attention from complexity

# F3 Rhythm
_BEAT_ENTRAINMENT = 42          # beat coupling strength

# F5 Emotion
_EMOTIONAL_AROUSAL = 63         # arousal / activation

# F6 Reward
_HARMONIC_TENSION = 80          # harmonic dissonance

# F7 Motor
_AUDITORY_MOTOR_COUPLING = 90   # hearing-to-movement link
_GROOVE_QUALITY = 92            # groove assessment
_MOTOR_PREPARATION = 95         # motor readiness
_PERIOD_ENTRAINMENT = 98        # locked tempo estimate
_CONTEXT_DEPTH = 101            # hierarchical structure layers


def compute_speed(beliefs: Tensor) -> Tensor:
    """Speed — Slow ↔ Fast.

    Perceived tempo / rate of musical events.
    Strongest discriminator across 131 classical pieces (std=11.1 BPM).

    Sources:
        - b98 period_entrainment: motor system's locked tempo estimate
        - b42 beat_entrainment: oscillatory coupling strength
        - b95 motor_preparation: motor readiness
    """
    period = beliefs[:, :, _PERIOD_ENTRAINMENT]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    motor = beliefs[:, :, _MOTOR_PREPARATION]

    return (0.40 * period + 0.30 * beat + 0.30 * motor).clamp(0, 1)


def compute_volume(beliefs: Tensor) -> Tensor:
    """Volume — Quiet ↔ Loud.

    Physical loudness / sound intensity level.
    The first thing anyone notices about music.

    Sources:
        - b35 sensory_load: cognitive resource demand from volume
        - b63 emotional_arousal: arousal tracks loudness closely
        - b34 salience_network_activation: attention-grabbing intensity
    """
    load = beliefs[:, :, _SENSORY_LOAD]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    salience = beliefs[:, :, _SALIENCE_NETWORK]

    return (0.40 * load + 0.35 * arousal + 0.25 * salience).clamp(0, 1)


def compute_weight(beliefs: Tensor) -> Tensor:
    """Weight — Light ↔ Heavy.

    Perceptual heaviness: spectral density, bass energy, layering.
    "Heavy metal" vs "light jazz" — everyone says this.

    Sources:
        - b16 spectral_complexity: acoustic density / spectral richness
        - b35 sensory_load: cognitive load from dense sound
        - b36 attention_capture: multiple competing streams = heavy
    """
    spectral = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    load = beliefs[:, :, _SENSORY_LOAD]
    capture = beliefs[:, :, _ATTENTION_CAPTURE]

    return (0.40 * spectral + 0.35 * load + 0.25 * capture).clamp(0, 1)


def compute_texture(beliefs: Tensor) -> Tensor:
    """Texture — Smooth ↔ Rough.

    Surface quality of sound: polished/clean vs gritty/distorted.
    "Smooth jazz" vs "rough vocals" — natural language.

    Sources:
        - b80 harmonic_tension: harmonic dissonance = rougher texture
        - b0  consonance_salience_gradient: low consonance = rough
        - b15 timbral_character: timbral edge / brightness
        - b34 salience_network_activation: salience from jagged transients
    """
    h_tension = beliefs[:, :, _HARMONIC_TENSION]
    consonance = beliefs[:, :, _CONSONANCE_SALIENCE_GRADIENT]
    timbral = beliefs[:, :, _TIMBRAL_CHARACTER]
    salience = beliefs[:, :, _SALIENCE_NETWORK]

    # High tension + low consonance + high timbral edge = rough
    return (0.30 * h_tension - 0.20 * consonance + 0.25 * timbral + 0.25 * salience + 0.20).clamp(0, 1)


def compute_depth(beliefs: Tensor) -> Tensor:
    """Depth — Thin ↔ Deep.

    Perceived depth: bass energy, layering, structural complexity.
    "Deep bass", "thin sound" — everyone understands.

    Sources:
        - b101 context_depth: hierarchical structural layers
        - b16 spectral_complexity: spectral richness / fullness
        - b90 auditory_motor_coupling: bass-driven body resonance
    """
    context = beliefs[:, :, _CONTEXT_DEPTH]
    spectral = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    motor = beliefs[:, :, _AUDITORY_MOTOR_COUPLING]

    return (0.40 * context + 0.35 * spectral + 0.25 * motor).clamp(0, 1)


# ======================================================================
# Ordered model list — canonical order matching 5D tensor indices
# ======================================================================

MUSICAL_MODELS: Tuple[Callable[..., Tensor], ...] = (
    compute_speed,    # 0
    compute_volume,   # 1
    compute_weight,   # 2
    compute_texture,  # 3
    compute_depth,    # 4
)

MUSICAL_NAMES = ("speed", "volume", "weight", "texture", "depth")
MUSICAL_LABELS = {
    "speed":   {"low": "Slow",   "high": "Fast"},
    "volume":  {"low": "Quiet",  "high": "Loud"},
    "weight":  {"low": "Light",  "high": "Heavy"},
    "texture": {"low": "Smooth", "high": "Rough"},
    "depth":   {"low": "Thin",   "high": "Deep"},
}
