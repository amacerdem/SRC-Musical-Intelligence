"""24D Neuroscience tier — expert-level dimensions.

Requires music cognition or neuroscience knowledge to validate.
Each function: (beliefs) → (B, T) scalar in [0, 1].

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

if TYPE_CHECKING:
    from torch import Tensor

# Belief indices (0-130)
# F2
_PREDICTION_ACCURACY = 20
_INFORMATION_CONTENT = 25
_SEQUENCE_MATCH = 31
# F3
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
_WANTING_RAMP = 78
_CHILLS_PROXIMITY = 79
_LIKING = 81
_PLEASURE = 83
_PREDICTION_ERROR = 84
_PREDICTION_MATCH = 85
_WANTING = 89
# F7
_AUDITORY_MOTOR_COUPLING = 90
_GROOVE_QUALITY = 92
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

def compute_prediction_error(beliefs: Tensor) -> Tensor:
    """Prediction Error — average unsigned PE across Core beliefs.

    Measures the brain's surprise signal: how much reality deviates from
    internal model predictions. Central to predictive coding (Friston 2005).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    info = beliefs[:, :, _INFORMATION_CONTENT]

    return (0.60 * pe + 0.40 * info).clamp(0, 1)


def compute_precision(beliefs: Tensor) -> Tensor:
    """Precision — confidence of predictions (π_eff).

    Precision weighting determines how much prediction errors update beliefs.
    High precision = confident predictions. (Feldman 2010).
    """
    pw = beliefs[:, :, _PRECISION_WEIGHTING]
    pred_acc = beliefs[:, :, _PREDICTION_ACCURACY]

    return (0.55 * pw + 0.45 * pred_acc).clamp(0, 1)


def compute_information_content(beliefs: Tensor) -> Tensor:
    """Information Content — Shannon information per musical event.

    -log₂(P) of current event under learned model. High = surprising event.
    IDyOM explains up to 83% of variance in pitch expectations (Pearce 2018).
    """
    info = beliefs[:, :, _INFORMATION_CONTENT]
    return info.clamp(0, 1)


def compute_model_uncertainty(beliefs: Tensor) -> Tensor:
    """Model Uncertainty — epistemic uncertainty about the musical model.

    Inverse of prediction accuracy: high uncertainty = the internal model
    doesn't fit the current music well (novel genre, unusual structure).
    """
    inv_acc = 1.0 - beliefs[:, :, _PREDICTION_ACCURACY]
    inv_match = 1.0 - beliefs[:, :, _SEQUENCE_MATCH]
    inv_gain = 1.0 - beliefs[:, :, _SELECTIVE_GAIN]

    return (0.40 * inv_acc + 0.35 * inv_match + 0.25 * inv_gain).clamp(0, 1)


# ======================================================================
# SENSORIMOTOR (4-7)
# ======================================================================

def compute_oscillation_coupling(beliefs: Tensor) -> Tensor:
    """Beat Coupling — neural oscillation entrainment to musical beat.

    Phase-locking of endogenous oscillations to exogenous rhythm.
    Measured via EEG frequency-tagging (Nozaradan 2011).
    """
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    meter = beliefs[:, :, _METER_HIERARCHY]

    return (0.55 * beat + 0.45 * meter).clamp(0, 1)


def compute_motor_period_lock(beliefs: Tensor) -> Tensor:
    """Period Lock — motor system convergence to auditory period.

    Motor period adaptation (Thaut 2015). When locked, movement
    becomes effortless and automatic.
    """
    period = beliefs[:, :, _PERIOD_ENTRAINMENT]
    kinematic = beliefs[:, :, _KINEMATIC_EFFICIENCY]

    return (0.55 * period + 0.45 * kinematic).clamp(0, 1)


def compute_auditory_motor_bind(beliefs: Tensor) -> Tensor:
    """Motor Binding — strength of auditory-motor coupling.

    The dorsal auditory stream that transforms hearing into movement
    (Zatorre 2007, dual-stream model).
    """
    coupling = beliefs[:, :, _AUDITORY_MOTOR_COUPLING]
    beat = beliefs[:, :, _BEAT_ENTRAINMENT]
    kinematic = beliefs[:, :, _KINEMATIC_EFFICIENCY]

    return (0.50 * coupling + 0.25 * beat + 0.25 * kinematic).clamp(0, 1)


def compute_timing_precision(beliefs: Tensor) -> Tensor:
    """Timing Precision — temporal accuracy of rhythmic processing.

    How precisely the motor system tracks musical timing (Grahn & Brett 2007).
    """
    precision = beliefs[:, :, _TIMING_PRECISION]
    return precision.clamp(0, 1)


# ======================================================================
# EMOTION CIRCUITRY (8-11)
# ======================================================================

def compute_valence_mode(beliefs: Tensor) -> Tensor:
    """Valence Mode — emotional color from mode/consonance/tempo interaction.

    The classic major=happy, minor=sad mapping, modulated by tempo and
    spectral features (Eerola & Vuoskoski 2011).
    """
    happy = beliefs[:, :, _PERCEIVED_HAPPY]
    sad = beliefs[:, :, _PERCEIVED_SAD]
    mode = beliefs[:, :, _MODE_DETECTION]

    return (0.35 * happy + 0.30 * sad + 0.35 * mode).clamp(0, 1)


def compute_autonomic_arousal(beliefs: Tensor) -> Tensor:
    """ANS Arousal — autonomic nervous system activation.

    Heart rate, skin conductance, pupil dilation. Driven by ANS dominance
    and emotional arousal (Koelsch 2014).
    """
    ans = beliefs[:, :, _ANS_DOMINANCE]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]

    return (0.55 * ans + 0.45 * arousal).clamp(0, 1)


def compute_nostalgia_circuit(beliefs: Tensor) -> Tensor:
    """Nostalgia Circuit — nostalgia network activation.

    Music-evoked autobiographical memory activates hippocampus→vmPFC→NAcc
    (Janata 2009). Nostalgia increases self-esteem and social connectedness.
    """
    nostalgia_int = beliefs[:, :, _NOSTALGIA_INTENSITY]
    nostalgia_aff = beliefs[:, :, _NOSTALGIA_AFFECT]

    return (0.55 * nostalgia_int + 0.45 * nostalgia_aff).clamp(0, 1)


def compute_chills_pathway(beliefs: Tensor) -> Tensor:
    """Chills Pathway — frisson/chills response.

    Peak emotional response: piloerection, skin conductance spike, shivers.
    (Blood & Zatorre 2001).
    """
    chills = beliefs[:, :, _CHILLS_INTENSITY]
    chills_prox = beliefs[:, :, _CHILLS_PROXIMITY]
    arousal = beliefs[:, :, _EMOTIONAL_AROUSAL]

    return (0.40 * chills + 0.30 * chills_prox + 0.30 * arousal).clamp(0, 1)


# ======================================================================
# REWARD SYSTEM (12-15)
# ======================================================================

def compute_da_anticipation(beliefs: Tensor) -> Tensor:
    """DA Anticipation — caudate dopamine ramp before peak experience.

    Wanting signal: caudate DA ramps 10-15s before pleasure peak.
    Anatomically distinct from consummation (Salimpoor 2011).
    """
    caudate_da = beliefs[:, :, _DA_CAUDATE]
    wanting_ramp = beliefs[:, :, _WANTING_RAMP]

    return (0.55 * caudate_da + 0.45 * wanting_ramp).clamp(0, 1)


def compute_da_consummation(beliefs: Tensor) -> Tensor:
    """DA Consummation — NAcc dopamine burst at peak pleasure.

    Liking signal: NAcc DA fires at the moment of musical pleasure.
    Correlates with chills and willingness to pay (Salimpoor 2013).
    """
    nacc_da = beliefs[:, :, _DA_NACC]
    wanting = beliefs[:, :, _WANTING]

    return (0.55 * nacc_da + 0.45 * wanting).clamp(0, 1)


def compute_hedonic_tone(beliefs: Tensor) -> Tensor:
    """Hedonic Tone — consummatory pleasure.

    Consummatory pleasure distinct from wanting. Liking = OPI in NAcc shell.
    Blocked by naltrexone, enhanced by music (Ferreri 2019, PNAS).
    """
    liking = beliefs[:, :, _LIKING]
    pleasure = beliefs[:, :, _PLEASURE]

    return (0.55 * liking + 0.45 * pleasure).clamp(0, 1)


def compute_reward_pe(beliefs: Tensor) -> Tensor:
    """Reward PE — reward prediction error (better/worse than expected).

    TD error: δ = R + γV' − V. Positive RPE → DA burst → reinforcement.
    Negative RPE → DA dip → aversion (Schultz 1997).
    """
    pe = beliefs[:, :, _PREDICTION_ERROR]
    match = beliefs[:, :, _PREDICTION_MATCH]

    # PE * (1 - match): high PE AND low match = large RPE
    rpe = pe * (1.0 - match)
    return (0.65 * rpe + 0.35 * pe).clamp(0, 1)


# ======================================================================
# MEMORY & LEARNING (16-19)
# ======================================================================

def compute_episodic_encoding(beliefs: Tensor) -> Tensor:
    """Episodic Encoding — strength of new memory formation.

    Hippocampal binding of sensory, emotional, and contextual features into
    a single episodic trace (Squire 2004). Consolidation during encoding.
    """
    encoding = beliefs[:, :, _EPISODIC_ENCODING]
    consolidation = beliefs[:, :, _CONSOLIDATION_STRENGTH]

    return (0.55 * encoding + 0.45 * consolidation).clamp(0, 1)


def compute_autobiographical(beliefs: Tensor) -> Tensor:
    """Autobiographical — connection to personal life story.

    Music-evoked autobiographical memories (MEAMs) occur ~once per day.
    Hippocampus→vmPFC→default mode network (Janata 2009).
    """
    autobio = beliefs[:, :, _AUTOBIOGRAPHICAL_RETRIEVAL]
    self_rel = beliefs[:, :, _SELF_RELEVANCE]

    return (0.55 * autobio + 0.45 * self_rel).clamp(0, 1)


def compute_statistical_learning(beliefs: Tensor) -> Tensor:
    """Statistical Learning — implicit learning of musical regularities.

    Tracking transitional probabilities of melodic/harmonic sequences.
    The brain's internal generative model (Saffran 1999, Pearce 2018).
    """
    stat = beliefs[:, :, _STATISTICAL_MODEL]
    seq = beliefs[:, :, _SEQUENCE_MATCH]

    return (0.55 * stat + 0.45 * seq).clamp(0, 1)


def compute_expertise_effect(beliefs: Tensor) -> Tensor:
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

def compute_neural_synchrony(beliefs: Tensor) -> Tensor:
    """Neural Sync — inter-brain phase synchronization during shared listening.

    Hyperscanning studies show phase-locking between listeners' EEG/fMRI
    signals during shared musical experience (Hasson 2012).
    """
    sync = beliefs[:, :, _NEURAL_SYNCHRONY]
    entrainment = beliefs[:, :, _ENTRAINMENT_QUALITY]

    return (0.60 * sync + 0.40 * entrainment).clamp(0, 1)


def compute_social_bonding(beliefs: Tensor) -> Tensor:
    """Social Bond — music-mediated social cohesion.

    Synchronized music-making releases endorphins and oxytocin,
    promoting "self-other merging" (Tarr 2014, Savage 2021).
    """
    bonding = beliefs[:, :, _SOCIAL_BONDING]
    flow = beliefs[:, :, _GROUP_FLOW]

    return (0.55 * bonding + 0.45 * flow).clamp(0, 1)


def compute_social_prediction(beliefs: Tensor) -> Tensor:
    """Social Prediction — predicting others' musical intentions.

    Theory of mind applied to music: anticipating a co-performer's next move.
    TPJ/STS activation during joint music-making (Novembre 2016).
    """
    spe = beliefs[:, :, _SOCIAL_PREDICTION_ERROR]
    coord = beliefs[:, :, _SOCIAL_COORDINATION]

    return (0.50 * spe + 0.50 * coord).clamp(0, 1)


def compute_collective_reward(beliefs: Tensor) -> Tensor:
    """Collective Reward — shared pleasure amplification.

    Music heard together is rated as more pleasurable than alone.
    Shared reward circuits + social reward (Tarr 2014).
    """
    sync_rew = beliefs[:, :, _SYNCHRONY_REWARD]
    collective = beliefs[:, :, _COLLECTIVE_PLEASURE]

    return (0.50 * sync_rew + 0.50 * collective).clamp(0, 1)


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
