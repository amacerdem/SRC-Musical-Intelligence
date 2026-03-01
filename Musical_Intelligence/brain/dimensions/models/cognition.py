"""12D Cognition tier — informed-listener dimensions.

A casual musician or avid music listener can validate these with some thought.
Each function: (beliefs) → (B, T) scalar in [0, 1].

Dimensions:
    0  melodic_hook   — "Is the melody catchy/memorable?"
    1  harmonic_depth — "Simple chords or rich/complex?"
    2  rhythmic_drive — "Basic beat or layered/syncopated?"
    3  timbral_color  — "Warm/organic or cold/electronic?"
    4  emotional_arc  — "Which specific emotion? Joy? Awe? Nostalgia?"
    5  surprise       — "Did something unexpected happen?"
    6  momentum       — "Building to somewhere or going in circles?"
    7  narrative      — "Is this a journey with chapters, or a loop?"
    8  familiarity    — "Do I recognize these patterns/style?"
    9  pleasure       — "Am I enjoying this? Do I want more?"
    10 space          — "Intimate whisper or cathedral vastness?"
    11 repetition     — "Same loop over and over, or always changing?"
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Tuple

import torch

if TYPE_CHECKING:
    from torch import Tensor

# Belief indices (from 0-130 registry)
# F1 Sensory
_HARMONIC_STABILITY = 4
_HARMONIC_TEMPLATE_MATCH = 5
_INTERVAL_QUALITY = 6
_PITCH_PROMINENCE = 8
_PITCH_IDENTITY = 10
_AESTHETIC_QUALITY = 11
_SPECTRAL_TEMPORAL_SYNERGY = 13
_TIMBRAL_CHARACTER = 15
_SPECTRAL_COMPLEXITY = 16
# F2 Prediction
_ABSTRACT_FUTURE = 17
_PREDICTION_ACCURACY = 20
_PREDICTION_HIERARCHY = 21
_INFORMATION_CONTENT = 25
_SEQUENCE_MATCH = 31
# F3 Attention
_SENSORY_LOAD = 35
_ATTENTION_CAPTURE = 36
_BEAT_ENTRAINMENT = 42
_METER_HIERARCHY = 44
# F4 Memory
_MELODIC_RECOGNITION = 47
_MEMORY_PRESERVATION = 48
_EMOTIONAL_COLORING = 51
_RETRIEVAL_PROBABILITY = 54
_EPISODIC_BOUNDARY = 58
# F5 Emotion
_ANS_DOMINANCE = 60
_EMOTIONAL_AROUSAL = 63
_EMOTION_CERTAINTY = 64
_PERCEIVED_HAPPY = 67
_PERCEIVED_SAD = 68
_NOSTALGIA_AFFECT = 70
# F6 Reward
_DA_CAUDATE = 74
_DA_NACC = 75
_WANTING_RAMP = 78
_CHILLS_PROXIMITY = 79
_HARMONIC_TENSION = 80
_LIKING = 81
_PEAK_DETECTION = 82
_PLEASURE = 83
_PREDICTION_ERROR = 84
_PREDICTION_MATCH = 85
_TENSION = 88
_WANTING = 89
# F7 Motor
_AUDITORY_MOTOR_COUPLING = 90
_GROOVE_QUALITY = 92
_METER_STRUCTURE = 94
_CONTEXT_DEPTH = 101
_PHRASE_BOUNDARY_PRED = 104
_STRUCTURE_PRED = 106
# F8 Learning
_STATISTICAL_MODEL = 109
_TRAINED_TIMBRE_RECOGNITION = 111


def compute_melodic_hook(beliefs: Tensor) -> Tensor:
    """Melody — is the melody catchy and memorable?

    "Can you hum it afterwards? Does it grab your ear?"

    Combines pitch salience (how prominent the melodic line is), pattern
    recognition (how well-formed the contour), memorability (stickiness),
    melodic recognition, and spectral-temporal synergy (temporal auditory
    integration, replaces STG region).

    Sources: Zatorre 2012 (pitch processing in STG/HG), Jakubowski 2017 (earworms).
    """
    pitch = beliefs[:, :, _PITCH_PROMINENCE]
    identity = beliefs[:, :, _PITCH_IDENTITY]
    memory = beliefs[:, :, _MEMORY_PRESERVATION]
    recognition = beliefs[:, :, _MELODIC_RECOGNITION]
    synergy = beliefs[:, :, _SPECTRAL_TEMPORAL_SYNERGY]

    return (
        0.25 * pitch + 0.20 * identity + 0.25 * memory
        + 0.15 * recognition + 0.15 * synergy
    ).clamp(0, 1)


def compute_harmonic_depth(beliefs: Tensor) -> Tensor:
    """Harmony — are the chords simple or rich/complex?

    "Three-chord pop or jazz-level voicings?"

    Uses harmonic stability inversely (low stability = complex/adventurous),
    template match (how standard the progressions are), interval quality
    (consonance/dissonance balance), and prediction hierarchy (harmonic
    syntax processing, replaces IFG region).

    Sources: Koelsch 2005 (ERAN in IFG), Lerdahl 2001 (tonal tension model).
    """
    stability = beliefs[:, :, _HARMONIC_STABILITY]
    template = beliefs[:, :, _HARMONIC_TEMPLATE_MATCH]
    interval = beliefs[:, :, _INTERVAL_QUALITY]
    h_tension = beliefs[:, :, _HARMONIC_TENSION]
    hierarchy = beliefs[:, :, _PREDICTION_HIERARCHY]

    # Invert stability: low stability = more harmonic depth
    depth = (
        0.25 * (1.0 - stability) + 0.20 * (1.0 - template) + 0.20 * interval
        + 0.15 * h_tension + 0.20 * hierarchy
    )
    return depth.clamp(0, 1)


def compute_rhythmic_drive(beliefs: Tensor) -> Tensor:
    """Rhythm — basic beat or layered and syncopated?

    "Simple four-on-the-floor or polyrhythmic complexity?"

    Combines beat clarity, meter sophistication, and motor coupling.
    High beat + high meter complexity = driving syncopated rhythm.

    Sources: London 2012 (metric well-formedness), Witek 2014 (syncopation inverted-U).
    """
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    meter = beliefs[:, :, _METER_HIERARCHY]
    structure = beliefs[:, :, _METER_STRUCTURE]
    motor = beliefs[:, :, _AUDITORY_MOTOR_COUPLING]
    groove = beliefs[:, :, _GROOVE_QUALITY]

    return (
        0.25 * beat + 0.20 * meter + 0.20 * structure
        + 0.20 * motor + 0.15 * groove
    ).clamp(0, 1)


def compute_timbral_color(beliefs: Tensor) -> Tensor:
    """Timbre — warm/organic or cold/electronic?

    "Acoustic guitar warmth or synthesizer crispness?"

    Timbral character directly measures the spectral identity.
    Spectral complexity adds density of overtones. Spectral-temporal
    synergy captures primary auditory encoding (replaces A1_HG region).

    Sources: Menon 2002 (timbre in A1), McAdams 1999 (timbre space dimensions).
    """
    timbre = beliefs[:, :, _TIMBRAL_CHARACTER]
    complexity = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    aesthetic = beliefs[:, :, _AESTHETIC_QUALITY]
    trained = beliefs[:, :, _TRAINED_TIMBRE_RECOGNITION]
    synergy = beliefs[:, :, _SPECTRAL_TEMPORAL_SYNERGY]

    return (
        0.30 * timbre + 0.20 * complexity + 0.15 * aesthetic
        + 0.15 * trained + 0.20 * synergy
    ).clamp(0, 1)


def compute_emotional_arc(beliefs: Tensor) -> Tensor:
    """Emotion — which specific emotion dominates? How clear is it?

    "Joy? Awe? Nostalgia? Or a confusing mix?"

    Combines emotional arousal magnitude, valence clarity, nostalgia,
    and emotion certainty (emotional salience/clarity, replaces amygdala).
    High emotion_arc = strong, clear emotional character.

    Sources: GEMS (Zentner 2008), Eerola & Vuoskoski 2011.
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    nostalgia = beliefs[:, :, _NOSTALGIA_AFFECT]
    certainty = beliefs[:, :, _EMOTION_CERTAINTY]

    # Emotional clarity = max of (happy, sad, nostalgia) * arousal strength
    emo_max = torch.max(torch.max(happy, sad), nostalgia)
    return (
        0.30 * emo_max + 0.25 * arousal + 0.20 * certainty + 0.25 * nostalgia
    ).clamp(0, 1)


def compute_surprise(beliefs: Tensor) -> Tensor:
    """Surprise — degree of expectation violation.

    "Did something unexpected just happen? That chord change was wild!"

    Prediction error is THE core signal. Information content measures
    how unlikely the event was. DA NAcc captures phasic surprise response
    (replaces DA neurochemical). Prediction hierarchy captures syntactic
    violation processing (replaces IFG region).

    Sources: Huron 2006 (ITPRA), Koelsch 2006 (harmonic expectancy violations).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    info = beliefs[:, :, _INFORMATION_CONTENT]
    da = beliefs[:, :, _DA_NACC]
    hierarchy = beliefs[:, :, _PREDICTION_HIERARCHY]

    return (
        0.30 * pe + 0.25 * info + 0.20 * da + 0.25 * hierarchy
    ).clamp(0, 1)


def compute_momentum(beliefs: Tensor) -> Tensor:
    """Momentum — forward motion and directionality.

    "Building toward a climax, or going in circles?"

    Rising tension + approaching peak + wanting ramp = forward momentum.
    Chills proximity signals approaching peak experience.
    Wanting ramp captures the anticipatory DA ramp (replaces DA neurochemical).

    Sources: Huron 2006 (sweet anticipation), Salimpoor 2011 (DA ramp).
    """
    tension = beliefs[:, :, _TENSION]
    peak = beliefs[:, :, _PEAK_DETECTION]
    chills_prox = beliefs[:, :, _CHILLS_PROXIMITY]
    wanting = beliefs[:, :, _WANTING]
    wanting_ramp = beliefs[:, :, _WANTING_RAMP]

    return (
        0.25 * tension + 0.20 * peak + 0.20 * chills_prox
        + 0.15 * wanting + 0.20 * wanting_ramp
    ).clamp(0, 1)


def compute_narrative(beliefs: Tensor) -> Tensor:
    """Story — does the music tell a story with chapters?

    "An epic journey with twists and turns, or a static ambient loop?"

    Context depth measures nested structural layers (phrase > section > piece).
    Phrase and structure predictions indicate hierarchical form awareness.
    Episodic boundary detection marks "chapter breaks."
    Abstract future prediction captures executive planning (replaces dlPFC region).

    Sources: Lerdahl & Jackendoff 1983 (GTTM), Sridharan 2007 (event segmentation).
    """
    depth = beliefs[:, :, _CONTEXT_DEPTH]
    phrase = beliefs[:, :, _PHRASE_BOUNDARY_PRED]
    structure = beliefs[:, :, _STRUCTURE_PRED]
    boundary = beliefs[:, :, _EPISODIC_BOUNDARY]
    abstract = beliefs[:, :, _ABSTRACT_FUTURE]

    return (
        0.25 * depth + 0.20 * structure + 0.20 * phrase
        + 0.15 * boundary + 0.20 * abstract
    ).clamp(0, 1)


def compute_familiarity(beliefs: Tensor) -> Tensor:
    """Familiarity — do I recognize these patterns and style?

    "I've heard this kind of music before. This sounds familiar."

    Sequence match indicates pattern recognition. Prediction accuracy rises
    with familiarity. Statistical model captures learned regularities.
    Emotional coloring captures hippocampal memory associations
    (replaces hippocampus region).

    Sources: Janata 2009 (familiarity in hippocampus), Berlyne 1971 (inverted-U).
    """
    seq_match = beliefs[:, :, _SEQUENCE_MATCH]
    pred_acc = beliefs[:, :, _PREDICTION_ACCURACY]
    stat_model = beliefs[:, :, _STATISTICAL_MODEL]
    retrieval = beliefs[:, :, _RETRIEVAL_PROBABILITY]
    coloring = beliefs[:, :, _EMOTIONAL_COLORING]

    return (
        0.25 * seq_match + 0.25 * pred_acc + 0.20 * stat_model
        + 0.15 * retrieval + 0.15 * coloring
    ).clamp(0, 1)


def compute_pleasure(beliefs: Tensor) -> Tensor:
    """Pleasure — hedonic enjoyment and wanting more.

    "Am I enjoying this? Do I want it to continue?"

    Wanting (anticipatory) + liking (consummatory) + pleasure integration.
    DA NAcc captures reward circuit activation (replaces NAcc region).
    DA caudate captures anticipatory reward (replaces DA neurochemical).

    Sources: Berridge 2003 (wanting vs liking), Salimpoor 2011 (DA and music).
    """
    wanting = beliefs[:, :, _WANTING]
    liking = beliefs[:, :, _LIKING]
    pleasure = beliefs[:, :, _PLEASURE]
    da_nacc = beliefs[:, :, _DA_NACC]
    da_caudate = beliefs[:, :, _DA_CAUDATE]

    return (
        0.20 * wanting + 0.20 * liking + 0.20 * pleasure
        + 0.20 * da_nacc + 0.20 * da_caudate
    ).clamp(0, 1)


def compute_space(beliefs: Tensor) -> Tensor:
    """Space — perceived spatial extent and immersion.

    "Intimate close-mic whisper or vast cathedral reverb?"

    Spectral complexity correlates with perceived spaciousness (more frequencies
    = richer reverberant field). Sensory load increases with spatial complexity.
    Spectral-temporal synergy captures temporal auditory processing
    (replaces STG region). ANS dominance captures interoceptive immersion
    (replaces insula region).

    Sources: Bregman 1990 (auditory scene analysis), Craig 2009 (insula interoception).
    """
    complexity = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    load = beliefs[:, :, _SENSORY_LOAD]
    attention = beliefs[:, :, _ATTENTION_CAPTURE]
    synergy = beliefs[:, :, _SPECTRAL_TEMPORAL_SYNERGY]
    ans = beliefs[:, :, _ANS_DOMINANCE]

    return (
        0.25 * complexity + 0.20 * load + 0.15 * attention
        + 0.20 * synergy + 0.20 * ans
    ).clamp(0, 1)


def compute_repetition(beliefs: Tensor) -> Tensor:
    """Repetition — structural repetition level.

    "Same loop over and over, or always changing?"

    High sequence match + high prediction accuracy + low information content
    = high repetition. Prediction match signals "as expected" (no surprise).

    Sources: Margulis 2014 (repetition in music), IDyOM (Pearce 2018).
    """
    match = beliefs[:, :, _PREDICTION_MATCH]
    pred_acc = beliefs[:, :, _PREDICTION_ACCURACY]
    seq = beliefs[:, :, _SEQUENCE_MATCH]
    # Low information = high predictability = repetitive
    info_inv = 1.0 - beliefs[:, :, _INFORMATION_CONTENT]

    return (0.30 * match + 0.25 * pred_acc + 0.25 * seq + 0.20 * info_inv).clamp(0, 1)


# ======================================================================
# Ordered model list — canonical order matching 12D tensor indices
# ======================================================================

COGNITION_MODELS: Tuple[Callable[..., Tensor], ...] = (
    compute_melodic_hook,     # 0
    compute_harmonic_depth,   # 1
    compute_rhythmic_drive,   # 2
    compute_timbral_color,    # 3
    compute_emotional_arc,    # 4
    compute_surprise,         # 5
    compute_momentum,         # 6
    compute_narrative,        # 7
    compute_familiarity,      # 8
    compute_pleasure,         # 9
    compute_space,            # 10
    compute_repetition,       # 11
)
