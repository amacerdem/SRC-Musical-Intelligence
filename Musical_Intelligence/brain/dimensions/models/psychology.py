"""6D Psychology tier — gut-level dimensions, zero training needed.

Each function computes one dimension from beliefs → (B, T).
A listener with NO musical training can validate these in 2 seconds.

Dimensions:
    0  energy     — "Is this loud/intense or quiet/gentle?"
    1  valence    — "Does this sound happy or sad?"
    2  tempo      — "Is this fast or slow?"
    3  tension    — "Do I feel strain or release?"
    4  groove     — "Do I want to move my body?"
    5  complexity — "How much stuff is going on?"

Inter-rater agreement (non-musicians): all >80%.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Tuple

if TYPE_CHECKING:
    from torch import Tensor

# Belief index constants (from beliefs.jsonl registry)
# F1 Sensory
_HARMONIC_STABILITY = 4         # F1 harmonic_stability
_SPECTRAL_COMPLEXITY = 16       # F1 spectral_complexity
# F3 Attention
_SALIENCE_NETWORK = 34          # F3 salience_network_activation
_SENSORY_LOAD = 35              # F3 sensory_load
_ATTENTION_CAPTURE = 36         # F3 attention_capture
_BEAT_ENTRAINMENT = 42          # F3 beat_entrainment
# F5 Emotion
_ANS_DOMINANCE = 60             # F5 ans_dominance
_EMOTIONAL_AROUSAL = 63         # F5 emotional_arousal
_PERCEIVED_HAPPY = 67           # F5 perceived_happy
_PERCEIVED_SAD = 68             # F5 perceived_sad
# F6 Reward
_HARMONIC_TENSION = 80          # F6 harmonic_tension
_LIKING = 81                    # F6 liking
_WANTING = 89                   # F6 wanting
_TENSION = 88                   # F6 tension
# F7 Motor
_AUDITORY_MOTOR_COUPLING = 90   # F7 auditory_motor_coupling
_GROOVE_QUALITY = 92            # F7 groove_quality
_MOTOR_PREPARATION = 95         # F7 motor_preparation
_PERIOD_ENTRAINMENT = 98        # F7 period_entrainment
_PERIOD_LOCK_STRENGTH = 99      # F7 period_lock_strength
_CONTEXT_DEPTH = 101            # F7 context_depth


def compute_energy(beliefs: Tensor) -> Tensor:
    """Energy — perceived intensity/activation level.

    "Is this loud/intense or quiet/gentle?"

    Agreement: ICC > 0.95 (Schafer 2024). 82% variance explained by
    tempo, pulse clarity, brightness (N=1,513 participants, 750 excerpts).
    Neonates show startle/calming responses — pre-verbal, pre-cultural.

    Sources:
        - b34 salience_network_activation: attention-grabbing intensity
        - b63 emotional_arousal: felt activation (ANS coupling)
        - b35 sensory_load: cognitive resource demand (replaces NE arousal)
        - b16 spectral_complexity: acoustic density (replaces A1_HG)
    """
    salience = beliefs[:, :, _SALIENCE_NETWORK]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    load = beliefs[:, :, _SENSORY_LOAD]
    spectral = beliefs[:, :, _SPECTRAL_COMPLEXITY]

    return (
        0.25 * salience + 0.25 * arousal + 0.25 * load + 0.25 * spectral
    ).clamp(0, 1)


def compute_valence(beliefs: Tensor) -> Tensor:
    """Valence — positive-to-negative emotional coloring.

    "Does this sound happy or sad?"

    Agreement: >85% within-culture, >70% cross-cultural (Fritz 2009).
    Newborns discriminate consonance from dissonance within hours (Perani 2010).

    Sources:
        - b67 perceived_happy / b68 perceived_sad: direct emotion percepts
        - b4 harmonic_stability: consonance → positive valence
        - b89 wanting: reward tone (replaces DA)
        - b81 liking: hedonic tone (replaces OPI)
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    stability = beliefs[:, :, _HARMONIC_STABILITY]
    wanting = beliefs[:, :, _WANTING]
    liking = beliefs[:, :, _LIKING]

    # Happy-sad differential + consonance bias + reward tone
    mood = 0.30 * happy - 0.20 * sad + 0.15 * stability + 0.15 * wanting + 0.10 * liking
    # Shift and scale: raw range ~ [-0.20, 0.70] → [0, 1]
    return (mood + 0.20).clamp(0, 1)


def compute_tempo(beliefs: Tensor) -> Tensor:
    """Tempo — perceived speed of musical events.

    "Is this fast or slow?"

    Agreement: alpha 0.83-0.98 (Eerola 2020). Universal structural cue —
    beat perception is innate, newborns detect it (Winkler 2009, PNAS).
    Cross-cultural rhythm priors converge at ~120 BPM (Nature Human Behav 2024).

    Sources:
        - b98 period_entrainment: motor system's locked tempo estimate
        - b42 beat_entrainment: oscillatory coupling strength (fast = strong)
        - b95 motor_preparation: motor system readiness (replaces SMA)
    """
    period = beliefs[:, :, _PERIOD_ENTRAINMENT]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    motor = beliefs[:, :, _MOTOR_PREPARATION]

    return (0.40 * period + 0.30 * beat + 0.30 * motor).clamp(0, 1)


def compute_tension(beliefs: Tensor) -> Tensor:
    """Tension — felt strain, suspense, unresolved expectation vs. release.

    "Do I feel strain or release?"

    Agreement: r = 0.71-0.95 between musicians and non-musicians
    (Madsen & Fredrickson 1993). Somatic — felt in body (muscle, breath).

    Sources:
        - b88 tension: F6 direct tension belief (harmonics + PE)
        - b63 emotional_arousal: arousal amplifies felt tension (replaces amygdala)
        - b80 harmonic_tension: harmonic dissonance tension
        - b60 ans_dominance: autonomic arousal (replaces NE)
        - b34 salience_network_activation: threat/salience (replaces 5HT inverse)
    """
    tension_belief = beliefs[:, :, _TENSION]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    h_tension = beliefs[:, :, _HARMONIC_TENSION]
    ans = beliefs[:, :, _ANS_DOMINANCE]
    salience = beliefs[:, :, _SALIENCE_NETWORK]

    return (
        0.30 * tension_belief + 0.20 * arousal + 0.20 * h_tension
        + 0.15 * ans + 0.15 * salience
    ).clamp(0, 1)


def compute_groove(beliefs: Tensor) -> Tensor:
    """Groove — the urge to move rhythmically.

    "Do I want to move my body?"

    Agreement: >85%. No musician/non-musician differences in groove
    susceptibility (Senn 2021). Toddlers spontaneously bounce to groovy music
    (Zentner & Eerola 2010). Medium syncopation = peak groove (Witek 2014).

    Sources:
        - b92 groove_quality: direct groove assessment from F7
        - b42 beat_entrainment: entrainment enables groove
        - b90 auditory_motor_coupling: hearing-to-movement link (replaces putamen)
        - b95 motor_preparation: motor readiness (replaces SMA)
        - b99 period_lock_strength: period tracking quality
    """
    groove = beliefs[:, :, _GROOVE_QUALITY]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    motor_coupling = beliefs[:, :, _AUDITORY_MOTOR_COUPLING]
    motor_prep = beliefs[:, :, _MOTOR_PREPARATION]
    lock = beliefs[:, :, _PERIOD_LOCK_STRENGTH]

    return (
        0.30 * groove + 0.20 * beat + 0.20 * motor_coupling
        + 0.15 * motor_prep + 0.15 * lock
    ).clamp(0, 1)


def compute_complexity(beliefs: Tensor) -> Tensor:
    """Complexity — perceived density of simultaneous musical events.

    "How much stuff is going on?"

    Agreement: alpha 0.83-0.98 for relative judgments (Eerola 2020).
    Auditory scene analysis is pre-attentive and universal (Bregman 1990).
    Inverted-U preference: too simple = boring, too complex = aversive (Berlyne 1971).

    Sources:
        - b16 spectral_complexity: acoustic richness / spectral density
        - b101 context_depth: hierarchical layers of musical structure
        - b35 sensory_load: cognitive resource demand from sensory input
        - b36 attention_capture: involuntary attention = many competing streams
    """
    spec = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    depth = beliefs[:, :, _CONTEXT_DEPTH]
    load = beliefs[:, :, _SENSORY_LOAD]
    capture = beliefs[:, :, _ATTENTION_CAPTURE]

    return (0.30 * spec + 0.25 * depth + 0.25 * load + 0.20 * capture).clamp(0, 1)


# ======================================================================
# Ordered model list — canonical order matching 6D tensor indices
# ======================================================================

PSYCHOLOGY_MODELS: Tuple[Callable[..., Tensor], ...] = (
    compute_energy,       # 0
    compute_valence,      # 1
    compute_tempo,        # 2
    compute_tension,      # 3
    compute_groove,       # 4
    compute_complexity,   # 5
)
