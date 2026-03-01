"""24D Neuroscience tier — expert-level dimensions.

Requires music cognition or neuroscience knowledge to validate.
Each function: (beliefs, ram, neuro) → (B, T) scalar in [0, 1].

6 domains × 4 parameters:
    Predictive Processing (0-3)
    Sensorimotor          (4-7)
    Emotion Circuitry     (8-11)
    Reward System         (12-15)
    Memory & Learning     (16-19)
    Social Cognition      (20-23)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Tuple

import torch

from Musical_Intelligence.brain.neurochemicals import DA, NE, OPI, _5HT
from Musical_Intelligence.brain.regions import region_index

if TYPE_CHECKING:
    from torch import Tensor

# Pre-resolve region indices
_A1_HG = region_index("A1_HG")
_STG = region_index("STG")
_STS = region_index("STS")
_IFG = region_index("IFG")
_dlPFC = region_index("dlPFC")
_vmPFC = region_index("vmPFC")
_OFC = region_index("OFC")
_ACC = region_index("ACC")
_SMA = region_index("SMA")
_PMC = region_index("PMC")
_VTA = region_index("VTA")
_NAcc = region_index("NAcc")
_CAUDATE = region_index("caudate")
_AMYGDALA = region_index("amygdala")
_HIPPOCAMPUS = region_index("hippocampus")
_PUTAMEN = region_index("putamen")
_HYPOTHALAMUS = region_index("hypothalamus")
_INSULA = region_index("insula")
_PAG = region_index("PAG")

# Belief indices (0-130)
# F1
_HARMONIC_STABILITY = 4
# F2
_PREDICTION_ACCURACY = 20
_PREDICTION_HIERARCHY = 21
_INFORMATION_CONTENT = 25
_SEQUENCE_MATCH = 31
# F3
_SENSORY_LOAD = 35
_ATTENTION_CAPTURE = 36
_PRECISION_WEIGHTING = 39
_BEAT_ENTRAINMENT = 42
_METER_HIERARCHY = 44
_SELECTIVE_GAIN = 46
# F4
_AUTOBIOGRAPHICAL_RETRIEVAL = 50
_NOSTALGIA_INTENSITY = 53
_SELF_RELEVANCE = 55
_CONSOLIDATION_STRENGTH = 57
_EPISODIC_ENCODING = 59
# F5
_ANS_DOMINANCE = 60
_CHILLS_INTENSITY = 61
_EMOTIONAL_AROUSAL = 63
_MODE_DETECTION = 66
_PERCEIVED_HAPPY = 67
_PERCEIVED_SAD = 68
_NOSTALGIA_AFFECT = 70
# F6
_DA_CAUDATE = 74
_DA_NACC = 75
_DISSOCIATION_INDEX = 76
_WANTING_RAMP = 78
_LIKING = 81
_PLEASURE = 83
_PREDICTION_ERROR = 84
_PREDICTION_MATCH = 85
_WANTING = 89
# F7
_AUDITORY_MOTOR_COUPLING = 90
_KINEMATIC_EFFICIENCY = 96
_PERIOD_ENTRAINMENT = 98
_TIMING_PRECISION = 100
# F8
_STATISTICAL_MODEL = 109
_TRAINED_TIMBRE = 111
_EXPERTISE_ENHANCEMENT = 114
_NETWORK_SPECIALIZATION = 119
_WITHIN_CONNECTIVITY = 120
# F9
_COLLECTIVE_PLEASURE = 121
_ENTRAINMENT_QUALITY = 122
_GROUP_FLOW = 123
_SOCIAL_BONDING = 124
_SOCIAL_PREDICTION_ERROR = 125
_SYNCHRONY_REWARD = 126
_NEURAL_SYNCHRONY = 128
_SOCIAL_COORDINATION = 130


# ======================================================================
# PREDICTIVE PROCESSING (0-3)
# ======================================================================

def compute_prediction_error(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Prediction Error — average unsigned PE across Core beliefs.

    Measures the brain's surprise signal: how much reality deviates from
    internal model predictions. Central to predictive coding (Friston 2005).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    info = beliefs[:, :, _INFORMATION_CONTENT]
    acc = ram[:, :, _ACC]  # Anterior cingulate tracks PE

    return (0.45 * pe + 0.30 * info + 0.25 * acc).clamp(0, 1)


def compute_precision(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Precision — confidence of predictions (π_eff).

    Precision weighting determines how much prediction errors update beliefs.
    High precision = confident predictions. Insula tracks precision (Feldman 2010).
    """
    pw = beliefs[:, :, _PRECISION_WEIGHTING]
    pred_acc = beliefs[:, :, _PREDICTION_ACCURACY]
    insula = ram[:, :, _INSULA]

    return (0.40 * pw + 0.35 * pred_acc + 0.25 * insula).clamp(0, 1)


def compute_information_content(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Information Content — Shannon information per musical event.

    -log₂(P) of current event under learned model. High = surprising event.
    IDyOM explains up to 83% of variance in pitch expectations (Pearce 2018).
    """
    info = beliefs[:, :, _INFORMATION_CONTENT]
    return info.clamp(0, 1)


def compute_model_uncertainty(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Model Uncertainty — epistemic uncertainty about the musical model.

    Inverse of prediction accuracy: high uncertainty = the internal model
    doesn't fit the current music well (novel genre, unusual structure).
    """
    inv_acc = 1.0 - beliefs[:, :, _PREDICTION_ACCURACY]
    inv_match = 1.0 - beliefs[:, :, _SEQUENCE_MATCH]
    # Low selective gain = uncertain about where to focus
    inv_gain = 1.0 - beliefs[:, :, _SELECTIVE_GAIN]

    return (0.40 * inv_acc + 0.35 * inv_match + 0.25 * inv_gain).clamp(0, 1)


# ======================================================================
# SENSORIMOTOR (4-7)
# ======================================================================

def compute_oscillation_coupling(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Beat Coupling — neural oscillation entrainment to musical beat.

    Phase-locking of endogenous oscillations to exogenous rhythm.
    Measured via EEG frequency-tagging (Nozaradan 2011).
    """
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    meter = beliefs[:, :, _METER_HIERARCHY]

    return (0.55 * beat + 0.45 * meter).clamp(0, 1)


def compute_motor_period_lock(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Period Lock — motor system convergence to auditory period.

    SMA+putamen period adaptation (Thaut 2015). When locked, movement
    becomes effortless and automatic.
    """
    period = beliefs[:, :, _PERIOD_ENTRAINMENT]
    kinematic = beliefs[:, :, _KINEMATIC_EFFICIENCY]
    sma = ram[:, :, _SMA]

    return (0.40 * period + 0.30 * kinematic + 0.30 * sma).clamp(0, 1)


def compute_auditory_motor_bind(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Motor Binding — strength of auditory-motor coupling.

    The dorsal auditory stream connecting A1→SMA→PMC that transforms
    hearing into movement (Zatorre 2007, dual-stream model).
    """
    coupling = beliefs[:, :, _AUDITORY_MOTOR_COUPLING]
    putamen = ram[:, :, _PUTAMEN]
    pmc = ram[:, :, _PMC]

    return (0.45 * coupling + 0.30 * putamen + 0.25 * pmc).clamp(0, 1)


def compute_timing_precision(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Timing Precision — temporal accuracy of rhythmic processing.

    How precisely the motor system tracks musical timing (Grahn & Brett 2007).
    """
    precision = beliefs[:, :, _TIMING_PRECISION]
    return precision.clamp(0, 1)


# ======================================================================
# EMOTION CIRCUITRY (8-11)
# ======================================================================

def compute_valence_mode(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Valence Mode — emotional color from mode/consonance/tempo interaction.

    The classic major=happy, minor=sad mapping, modulated by tempo and
    spectral features (Eerola & Vuoskoski 2011).
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    mode = beliefs[:, :, _MODE_DETECTION]

    return (0.35 * happy + 0.30 * sad + 0.35 * mode).clamp(0, 1)


def compute_autonomic_arousal(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """ANS Arousal — autonomic nervous system activation.

    Heart rate, skin conductance, pupil dilation. Driven by NE (locus coeruleus)
    and sympathetic/parasympathetic balance (Koelsch 2014).
    """
    ans = beliefs[:, :, _ANS_DOMINANCE]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]
    ne = neuro[:, :, NE]

    return (0.35 * ans + 0.30 * arousal + 0.35 * ne).clamp(0, 1)


def compute_nostalgia_circuit(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Nostalgia Circuit — hippocampus-mPFC-reward nostalgia network.

    Music-evoked autobiographical memory activates hippocampus→vmPFC→NAcc
    (Janata 2009). Nostalgia increases self-esteem and social connectedness.
    """
    nostalgia_int = beliefs[:, :, _NOSTALGIA_INTENSITY]
    nostalgia_aff = beliefs[:, :, _NOSTALGIA_AFFECT]
    hippo = ram[:, :, _HIPPOCAMPUS]
    vmpfc = ram[:, :, _vmPFC]

    return (
        0.30 * nostalgia_int + 0.25 * nostalgia_aff + 0.25 * hippo + 0.20 * vmpfc
    ).clamp(0, 1)


def compute_chills_pathway(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Chills Pathway — frisson/chills via PAG-hypothalamus-opioid circuit.

    Peak emotional response: piloerection, skin conductance spike, shivers.
    PAG + hypothalamus + mu-opioid receptor activation (Blood & Zatorre 2001).
    """
    chills = beliefs[:, :, _CHILLS_INTENSITY]
    pag = ram[:, :, _PAG]
    hypo = ram[:, :, _HYPOTHALAMUS]
    opi = neuro[:, :, OPI]

    return (0.30 * chills + 0.25 * pag + 0.20 * hypo + 0.25 * opi).clamp(0, 1)


# ======================================================================
# REWARD SYSTEM (12-15)
# ======================================================================

def compute_da_anticipation(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """DA Anticipation — caudate dopamine ramp before peak experience.

    Wanting signal: caudate DA ramps 10-15s before pleasure peak.
    Anatomically distinct from consummation (Salimpoor 2011).
    """
    caudate_da = beliefs[:, :, _DA_CAUDATE]
    wanting_ramp = beliefs[:, :, _WANTING_RAMP]
    caudate_ram = ram[:, :, _CAUDATE]

    return (0.40 * caudate_da + 0.30 * wanting_ramp + 0.30 * caudate_ram).clamp(0, 1)


def compute_da_consummation(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """DA Consummation — NAcc dopamine burst at peak pleasure.

    Liking signal: NAcc DA fires at the moment of musical pleasure.
    Correlates with chills and willingness to pay (Salimpoor 2013).
    """
    nacc_da = beliefs[:, :, _DA_NACC]
    wanting = beliefs[:, :, _WANTING]
    nacc_ram = ram[:, :, _NAcc]
    da = neuro[:, :, DA]

    return (0.30 * nacc_da + 0.25 * wanting + 0.25 * nacc_ram + 0.20 * da).clamp(0, 1)


def compute_hedonic_tone(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Hedonic Tone — mu-opioid-mediated pleasure.

    Consummatory pleasure distinct from wanting. Liking = OPI in NAcc shell.
    Blocked by naltrexone, enhanced by music (Ferreri 2019, PNAS).
    """
    liking = beliefs[:, :, _LIKING]
    pleasure = beliefs[:, :, _PLEASURE]
    opi = neuro[:, :, OPI]
    ofc = ram[:, :, _OFC]

    return (0.30 * liking + 0.25 * pleasure + 0.25 * opi + 0.20 * ofc).clamp(0, 1)


def compute_reward_pe(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Reward PE — reward prediction error (better/worse than expected).

    TD error: δ = R + γV' − V. Positive RPE → DA burst → reinforcement.
    Negative RPE → DA dip → aversion (Schultz 1997).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    match = beliefs[:, :, _PREDICTION_MATCH]
    vta = ram[:, :, _VTA]

    # PE * (1 - match): high PE AND low match = large RPE
    rpe = pe * (1.0 - match)
    return (0.50 * rpe + 0.25 * pe + 0.25 * vta).clamp(0, 1)


# ======================================================================
# MEMORY & LEARNING (16-19)
# ======================================================================

def compute_episodic_encoding(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Episodic Encoding — strength of new memory formation.

    Hippocampal binding of sensory, emotional, and contextual features into
    a single episodic trace (Squire 2004). Consolidation during encoding.
    """
    encoding = beliefs[:, :, _EPISODIC_ENCODING]
    consolidation = beliefs[:, :, _CONSOLIDATION_STRENGTH]
    hippo = ram[:, :, _HIPPOCAMPUS]

    return (0.40 * encoding + 0.30 * consolidation + 0.30 * hippo).clamp(0, 1)


def compute_autobiographical(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Autobiographical — connection to personal life story.

    Music-evoked autobiographical memories (MEAMs) occur ~once per day.
    Hippocampus→vmPFC→default mode network (Janata 2009).
    """
    autobio = beliefs[:, :, _AUTOBIOGRAPHICAL_RETRIEVAL]
    self_rel = beliefs[:, :, _SELF_RELEVANCE]
    vmpfc = ram[:, :, _vmPFC]

    return (0.40 * autobio + 0.30 * self_rel + 0.30 * vmpfc).clamp(0, 1)


def compute_statistical_learning(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Statistical Learning — implicit learning of musical regularities.

    Tracking transitional probabilities of melodic/harmonic sequences.
    The brain's internal generative model (Saffran 1999, Pearce 2018).
    """
    stat = beliefs[:, :, _STATISTICAL_MODEL]
    seq = beliefs[:, :, _SEQUENCE_MATCH]
    stg = ram[:, :, _STG]

    return (0.40 * stat + 0.35 * seq + 0.25 * stg).clamp(0, 1)


def compute_expertise_effect(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Expertise Effect — neural reorganization from musical training.

    Musicians show enhanced MMN, larger planum temporale, stronger
    auditory-motor connections (Munte 2002, Schlaug 2005).
    """
    expertise = beliefs[:, :, _EXPERTISE_ENHANCEMENT]
    network = beliefs[:, :, _NETWORK_SPECIALIZATION]
    connectivity = beliefs[:, :, _WITHIN_CONNECTIVITY]
    trained = beliefs[:, :, _TRAINED_TIMBRE]

    return (
        0.30 * expertise + 0.25 * network + 0.25 * connectivity + 0.20 * trained
    ).clamp(0, 1)


# ======================================================================
# SOCIAL COGNITION (20-23)
# ======================================================================

def compute_neural_synchrony(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Neural Sync — inter-brain phase synchronization during shared listening.

    Hyperscanning studies show phase-locking between listeners' EEG/fMRI
    signals during shared musical experience (Hasson 2012).
    """
    sync = beliefs[:, :, _NEURAL_SYNCHRONY]
    sts = ram[:, :, _STS]

    return (0.60 * sync + 0.40 * sts).clamp(0, 1)


def compute_social_bonding(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Social Bond — music-mediated social cohesion.

    Synchronized music-making releases endorphins and oxytocin,
    promoting "self-other merging" (Tarr 2014, Savage 2021).
    """
    bonding = beliefs[:, :, _SOCIAL_BONDING]
    flow = beliefs[:, :, _GROUP_FLOW]
    vmpfc = ram[:, :, _vmPFC]
    opi = neuro[:, :, OPI]

    return (0.30 * bonding + 0.25 * flow + 0.25 * vmpfc + 0.20 * opi).clamp(0, 1)


def compute_social_prediction(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Social Prediction — predicting others' musical intentions.

    Theory of mind applied to music: anticipating a co-performer's next move.
    TPJ/STS activation during joint music-making (Novembre 2016).
    """
    spe = beliefs[:, :, _SOCIAL_PREDICTION_ERROR]
    coord = beliefs[:, :, _SOCIAL_COORDINATION]
    sts = ram[:, :, _STS]

    return (0.35 * spe + 0.35 * coord + 0.30 * sts).clamp(0, 1)


def compute_collective_reward(beliefs: Tensor, ram: Tensor, neuro: Tensor) -> Tensor:
    """Collective Reward — shared pleasure amplification.

    Music heard together is rated as more pleasurable than alone.
    Shared reward circuits (NAcc) + social reward (Tarr 2014).
    """
    sync_rew = beliefs[:, :, _SYNCHRONY_REWARD]
    collective = beliefs[:, :, _COLLECTIVE_PLEASURE]
    nacc = ram[:, :, _NAcc]

    return (0.35 * sync_rew + 0.35 * collective + 0.30 * nacc).clamp(0, 1)


# ======================================================================
# Ordered model list — canonical order matching 24D tensor indices
# ======================================================================

NEUROSCIENCE_MODELS: Tuple[Callable[..., Tensor], ...] = (
    # Predictive Processing (0-3)
    compute_prediction_error,       # 0
    compute_precision,              # 1
    compute_information_content,    # 2
    compute_model_uncertainty,      # 3
    # Sensorimotor (4-7)
    compute_oscillation_coupling,   # 4
    compute_motor_period_lock,      # 5
    compute_auditory_motor_bind,    # 6
    compute_timing_precision,       # 7
    # Emotion Circuitry (8-11)
    compute_valence_mode,           # 8
    compute_autonomic_arousal,      # 9
    compute_nostalgia_circuit,      # 10
    compute_chills_pathway,         # 11
    # Reward System (12-15)
    compute_da_anticipation,        # 12
    compute_da_consummation,        # 13
    compute_hedonic_tone,           # 14
    compute_reward_pe,              # 15
    # Memory & Learning (16-19)
    compute_episodic_encoding,      # 16
    compute_autobiographical,       # 17
    compute_statistical_learning,   # 18
    compute_expertise_effect,       # 19
    # Social Cognition (20-23)
    compute_neural_synchrony,       # 20
    compute_social_bonding,         # 21
    compute_social_prediction,      # 22
    compute_collective_reward,      # 23
)
