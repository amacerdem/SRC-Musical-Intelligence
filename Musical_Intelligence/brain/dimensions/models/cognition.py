"""12D Cognition tier — informed-listener dimensions.

A casual musician or avid music listener can validate these with some thought.
Each function: (beliefs, ram, neuro) → (B, T) scalar in [0, 1].

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

from Musical_Intelligence.brain.neurochemicals import DA, NE, OPI, _5HT
from Musical_Intelligence.brain.regions import region_index

if TYPE_CHECKING:
    from torch import Tensor

# Pre-resolve region indices
_STG = region_index("STG")
_IFG = region_index("IFG")
_A1_HG = region_index("A1_HG")
_NAcc = region_index("NAcc")
_VTA = region_index("VTA")
_HIPPOCAMPUS = region_index("hippocampus")
_vmPFC = region_index("vmPFC")
_dlPFC = region_index("dlPFC")
_ACC = region_index("ACC")
_OFC = region_index("OFC")
_AMYGDALA = region_index("amygdala")
_SMA = region_index("SMA")
_PUTAMEN = region_index("putamen")
_INSULA = region_index("insula")
_AG = region_index("AG")

# Belief indices (from 0-130 registry)
# F1 Sensory
_HARMONIC_STABILITY = 4
_HARMONIC_TEMPLATE_MATCH = 5
_INTERVAL_QUALITY = 6
_PITCH_PROMINENCE = 8
_PITCH_IDENTITY = 10
_AESTHETIC_QUALITY = 11
_TIMBRAL_CHARACTER = 15
_SPECTRAL_COMPLEXITY = 16
# F2 Prediction
_PREDICTION_ACCURACY = 20
_PREDICTION_HIERARCHY = 21
_INFORMATION_CONTENT = 25
_SEQUENCE_MATCH = 31
# F3 Attention
_SENSORY_LOAD = 35
_ATTENTION_CAPTURE = 36
_BEAT_ENTRAINMENT = 42
_METER_HIERARCHY = 44
_SELECTIVE_GAIN = 46
# F4 Memory
_MELODIC_RECOGNITION = 47
_MEMORY_PRESERVATION = 48
_AUTOBIOGRAPHICAL_RETRIEVAL = 50
_NOSTALGIA_INTENSITY = 53
_RETRIEVAL_PROBABILITY = 54
_EPISODIC_BOUNDARY = 58
# F5 Emotion
_EMOTIONAL_AROUSAL = 63
_PERCEIVED_HAPPY = 67
_PERCEIVED_SAD = 68
_NOSTALGIA_AFFECT = 70
# F6 Reward
_CHILLS_PROXIMITY = 79
_HARMONIC_TENSION = 80
_LIKING = 81
_PEAK_DETECTION = 82
_PLEASURE = 83
_PREDICTION_ERROR = 84
_PREDICTION_MATCH = 85
_RESOLUTION_EXPECTATION = 86
_TENSION = 88
_WANTING = 89
# F7 Motor
_AUDITORY_MOTOR_COUPLING = 90
_GROOVE_QUALITY = 92
_GROOVE_TRAJECTORY = 93
_METER_STRUCTURE = 94
_PERIOD_ENTRAINMENT = 98
_CONTEXT_DEPTH = 101
_PHRASE_BOUNDARY_PRED = 104
_STRUCTURE_PRED = 106
# F8 Learning
_STATISTICAL_MODEL = 109
_TRAINED_TIMBRE_RECOGNITION = 111


def compute_melodic_hook(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Melody — is the melody catchy and memorable?

    "Can you hum it afterwards? Does it grab your ear?"

    Combines pitch salience (how prominent the melodic line is), pattern
    recognition (how well-formed the contour), memorability (stickiness),
    and STG activation (temporal auditory processing hub for melody).

    Sources: Zatorre 2012 (pitch processing in STG/HG), Jakubowski 2017 (earworms).
    """
    pitch = beliefs[:, :, _PITCH_PROMINENCE]
    identity = beliefs[:, :, _PITCH_IDENTITY]
    memory = beliefs[:, :, _MEMORY_PRESERVATION]
    recognition = beliefs[:, :, _MELODIC_RECOGNITION]
    stg = ram[:, :, _STG]

    return (
        0.25 * pitch + 0.20 * identity + 0.25 * memory
        + 0.15 * recognition + 0.15 * stg
    ).clamp(0, 1)


def compute_harmonic_depth(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Harmony — are the chords simple or rich/complex?

    "Three-chord pop or jazz-level voicings?"

    Uses harmonic stability inversely (low stability = complex/adventurous),
    template match (how standard the progressions are), and interval quality
    (consonance/dissonance balance). IFG processes harmonic syntax (Koelsch 2005).

    Sources: Koelsch 2005 (ERAN in IFG), Lerdahl 2001 (tonal tension model).
    """
    stability = beliefs[:, :, _HARMONIC_STABILITY]
    template = beliefs[:, :, _HARMONIC_TEMPLATE_MATCH]
    interval = beliefs[:, :, _INTERVAL_QUALITY]
    ifg = ram[:, :, _IFG]
    h_tension = beliefs[:, :, _HARMONIC_TENSION]

    # Invert stability: low stability = more harmonic depth
    depth = 0.30 * (1.0 - stability) + 0.20 * (1.0 - template) + 0.20 * interval
    depth = depth + 0.15 * h_tension + 0.15 * ifg
    return depth.clamp(0, 1)


def compute_rhythmic_drive(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
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


def compute_timbral_color(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Timbre — warm/organic or cold/electronic?

    "Acoustic guitar warmth or synthesizer crispness?"

    Timbral character directly measures the spectral identity.
    Spectral complexity adds density of overtones. A1_HG is primary
    auditory cortex where timbral features are first encoded.

    Sources: Menon 2002 (timbre in A1), McAdams 1999 (timbre space dimensions).
    """
    timbre = beliefs[:, :, _TIMBRAL_CHARACTER]
    complexity = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    aesthetic = beliefs[:, :, _AESTHETIC_QUALITY]
    trained = beliefs[:, :, _TRAINED_TIMBRE_RECOGNITION]
    a1 = ram[:, :, _A1_HG]

    return (
        0.35 * timbre + 0.20 * complexity + 0.15 * aesthetic
        + 0.15 * trained + 0.15 * a1
    ).clamp(0, 1)


def compute_emotional_arc(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Emotion — which specific emotion dominates? How clear is it?

    "Joy? Awe? Nostalgia? Or a confusing mix?"

    Combines emotional arousal magnitude, valence clarity, and nostalgia.
    High emotion_arc = strong, clear emotional character.

    Sources: GEMS (Zentner 2008), Eerola & Vuoskoski 2011.
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    nostalgia = beliefs[:, :, _NOSTALGIA_AFFECT]
    amyg = ram[:, :, _AMYGDALA]

    # Emotional clarity = max of (happy, sad, nostalgia) * arousal strength
    emo_max = torch.max(torch.max(happy, sad), nostalgia)
    return (0.35 * emo_max + 0.30 * arousal + 0.20 * amyg + 0.15 * nostalgia).clamp(0, 1)


def compute_surprise(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Surprise — degree of expectation violation.

    "Did something unexpected just happen? That chord change was wild!"

    Prediction error is THE core signal. Above-baseline DA indicates
    phasic surprise response. IFG activates for syntactic violations.

    Sources: Huron 2006 (ITPRA), Koelsch 2006 (harmonic expectancy violations).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    info = beliefs[:, :, _INFORMATION_CONTENT]
    da_phasic = torch.relu(neuro[:, :, DA] - 0.6)  # Phasic burst above threshold
    ifg = ram[:, :, _IFG]

    return (0.35 * pe + 0.25 * info + 0.20 * da_phasic * 2.5 + 0.20 * ifg).clamp(0, 1)


def compute_momentum(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Momentum — forward motion and directionality.

    "Building toward a climax, or going in circles?"

    Rising tension + approaching peak + wanting ramp = forward momentum.
    Chills proximity signals approaching peak experience.

    Sources: Huron 2006 (sweet anticipation), Salimpoor 2011 (DA ramp).
    """
    tension = beliefs[:, :, _TENSION]
    peak = beliefs[:, :, _PEAK_DETECTION]
    chills_prox = beliefs[:, :, _CHILLS_PROXIMITY]
    wanting = beliefs[:, :, _WANTING]
    da_ramp = torch.relu(neuro[:, :, DA] - 0.5) * 2.0  # Anticipatory DA

    return (
        0.25 * tension + 0.20 * peak + 0.20 * chills_prox
        + 0.15 * wanting + 0.20 * da_ramp
    ).clamp(0, 1)


def compute_narrative(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Story — does the music tell a story with chapters?

    "An epic journey with twists and turns, or a static ambient loop?"

    Context depth measures nested structural layers (phrase > section > piece).
    Phrase and structure predictions indicate hierarchical form awareness.
    Episodic boundary detection marks "chapter breaks."

    Sources: Lerdahl & Jackendoff 1983 (GTTM), Sridharan 2007 (event segmentation).
    """
    depth = beliefs[:, :, _CONTEXT_DEPTH]
    phrase = beliefs[:, :, _PHRASE_BOUNDARY_PRED]
    structure = beliefs[:, :, _STRUCTURE_PRED]
    boundary = beliefs[:, :, _EPISODIC_BOUNDARY]
    dlpfc = ram[:, :, _dlPFC]

    return (
        0.25 * depth + 0.25 * structure + 0.20 * phrase
        + 0.15 * boundary + 0.15 * dlpfc
    ).clamp(0, 1)


def compute_familiarity(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Familiarity — do I recognize these patterns and style?

    "I've heard this kind of music before. This sounds familiar."

    Hippocampus is the memory hub. Sequence match indicates pattern recognition.
    Prediction accuracy rises with familiarity. Statistical model captures
    learned regularities.

    Sources: Janata 2009 (familiarity in hippocampus), Berlyne 1971 (inverted-U).
    """
    seq_match = beliefs[:, :, _SEQUENCE_MATCH]
    pred_acc = beliefs[:, :, _PREDICTION_ACCURACY]
    stat_model = beliefs[:, :, _STATISTICAL_MODEL]
    retrieval = beliefs[:, :, _RETRIEVAL_PROBABILITY]
    hippo = ram[:, :, _HIPPOCAMPUS]

    return (
        0.25 * seq_match + 0.25 * pred_acc + 0.20 * stat_model
        + 0.15 * retrieval + 0.15 * hippo
    ).clamp(0, 1)


def compute_pleasure(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Pleasure — hedonic enjoyment and wanting more.

    "Am I enjoying this? Do I want it to continue?"

    Wanting (DA caudate) + liking (OPI NAcc) + pleasure integration.
    Inverted-U familiarity modulation: too novel or too familiar reduces pleasure.

    Sources: Berridge 2003 (wanting vs liking), Salimpoor 2011 (DA and music).
    """
    wanting = beliefs[:, :, _WANTING]
    liking = beliefs[:, :, _LIKING]
    pleasure = beliefs[:, :, _PLEASURE]
    nacc = ram[:, :, _NAcc]
    da = neuro[:, :, DA]
    opi = neuro[:, :, OPI]

    return (
        0.20 * wanting + 0.20 * liking + 0.20 * pleasure
        + 0.15 * nacc + 0.15 * da + 0.10 * opi
    ).clamp(0, 1)


def compute_space(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Space — perceived spatial extent and immersion.

    "Intimate close-mic whisper or vast cathedral reverb?"

    Spectral complexity correlates with perceived spaciousness (more frequencies
    = richer reverberant field). Sensory load increases with spatial complexity.
    Insula integrates interoceptive awareness of immersion.

    Sources: Bregman 1990 (auditory scene analysis), Craig 2009 (insula interoception).
    """
    complexity = beliefs[:, :, _SPECTRAL_COMPLEXITY]
    load = beliefs[:, :, _SENSORY_LOAD]
    attention = beliefs[:, :, _ATTENTION_CAPTURE]
    insula = ram[:, :, _INSULA]
    stg = ram[:, :, _STG]

    return (
        0.30 * complexity + 0.20 * load + 0.15 * attention
        + 0.15 * insula + 0.20 * stg
    ).clamp(0, 1)


def compute_repetition(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
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
