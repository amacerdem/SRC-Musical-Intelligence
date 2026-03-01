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
_SALIENCE_NETWORK = 34          # F3 salience_network_activation
_EMOTIONAL_AROUSAL = 63         # F5 emotional_arousal
_PERCEIVED_HAPPY = 67           # F5 perceived_happy
_PERCEIVED_SAD = 68             # F5 perceived_sad
_HARMONIC_STABILITY = 4         # F1 harmonic_stability
_TENSION = 88                   # F6 tension
_GROOVE_QUALITY = 92            # F7 groove_quality
_BEAT_ENTRAINMENT = 42          # F3 beat_entrainment
_PERIOD_ENTRAINMENT = 98        # F7 period_entrainment
_SPECTRAL_COMPLEXITY = 16       # F1 spectral_complexity
_CONTEXT_DEPTH = 101            # F7 context_depth
_SENSORY_LOAD = 35              # F3 sensory_load
_ATTENTION_CAPTURE = 36         # F3 attention_capture


def compute_energy(beliefs: Tensor) -> Tensor:
    """Energy — perceived intensity/activation level.

    "Is this loud/intense or quiet/gentle?"

    Agreement: ICC > 0.95 (Schafer 2024). 82% variance explained by
    tempo, pulse clarity, brightness (N=1,513 participants, 750 excerpts).
    Neonates show startle/calming responses — pre-verbal, pre-cultural.

    Sources:
        - b34 salience_network_activation: attention-grabbing intensity
        - b63 emotional_arousal: felt activation (ANS coupling)
    """
    salience = beliefs[:, :, _SALIENCE_NETWORK]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]

    return (0.50 * salience + 0.50 * arousal).clamp(0, 1)


def compute_valence(beliefs: Tensor) -> Tensor:
    """Valence — positive-to-negative emotional coloring.

    "Does this sound happy or sad?"

    Agreement: >85% within-culture, >70% cross-cultural (Fritz 2009).
    Newborns discriminate consonance from dissonance within hours (Perani 2010).

    Sources:
        - b67 perceived_happy / b68 perceived_sad: direct emotion percepts
        - b4 harmonic_stability: consonance → positive valence
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    stability = beliefs[:, :, _HARMONIC_STABILITY]

    # Happy-sad differential + consonance bias
    mood = 0.45 * happy - 0.30 * sad + 0.25 * stability
    # Shift and scale: raw range ~ [-0.30, 0.70] → [0, 1]
    return (mood + 0.30).clamp(0, 1)


def compute_tempo(beliefs: Tensor) -> Tensor:
    """Tempo — perceived speed of musical events.

    "Is this fast or slow?"

    Agreement: alpha 0.83-0.98 (Eerola 2020). Universal structural cue —
    beat perception is innate, newborns detect it (Winkler 2009, PNAS).
    Cross-cultural rhythm priors converge at ~120 BPM (Nature Human Behav 2024).

    Sources:
        - b98 period_entrainment: motor system's locked tempo estimate
        - b42 beat_entrainment: oscillatory coupling strength (fast = strong)
    """
    period = beliefs[:, :, _PERIOD_ENTRAINMENT]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]

    return (0.55 * period + 0.45 * beat).clamp(0, 1)


def compute_tension(beliefs: Tensor) -> Tensor:
    """Tension — felt strain, suspense, unresolved expectation vs. release.

    "Do I feel strain or release?"

    Agreement: r = 0.71-0.95 between musicians and non-musicians
    (Madsen & Fredrickson 1993). Somatic — felt in body (muscle, breath).

    Sources:
        - b88 tension: F6 direct tension belief (harmonics + PE)
        - b63 emotional_arousal: arousal amplifies felt tension
        - b34 salience_network_activation: threat/salience detection
    """
    tension_belief = beliefs[:, :, _TENSION]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    salience = beliefs[:, :, _SALIENCE_NETWORK]

    return (0.50 * tension_belief + 0.30 * arousal + 0.20 * salience).clamp(0, 1)


def compute_groove(beliefs: Tensor) -> Tensor:
    """Groove — the urge to move rhythmically.

    "Do I want to move my body?"

    Agreement: >85%. No musician/non-musician differences in groove
    susceptibility (Senn 2021). Toddlers spontaneously bounce to groovy music
    (Zentner & Eerola 2010). Medium syncopation = peak groove (Witek 2014).

    Sources:
        - b92 groove_quality: direct groove assessment from F7
        - b42 beat_entrainment: entrainment enables groove
    """
    groove = beliefs[:, :, _GROOVE_QUALITY]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]

    return (0.55 * groove + 0.45 * beat).clamp(0, 1)


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
