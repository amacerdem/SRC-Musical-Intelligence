"""Hierarchical Dimension Tree — 6D → 12D → 24D → 131 beliefs.

Binary tree structure:
    6 Psychology nodes  (experiential, free tier)
    12 Cognition nodes  (music cognition, basic tier)
    24 Neuroscience nodes (neuroscience, premium tier)

Each 6D splits into 2×12D, each 12D splits into 2×24D.
Each 24D maps to a disjoint subset of the 131 C³ beliefs.
All 131 beliefs (indices 0-130) appear exactly once.

Belief index source: Lab/frontend/src/data/beliefs.ts
"""
from __future__ import annotations

from ._dimension import Dimension

# ======================================================================
# 24D — NEUROSCIENCE LAYER (leaf nodes, each maps to belief indices)
# ======================================================================

# --- Discovery / Expectancy ---
PREDICTIVE_PROCESSING = Dimension(
    index=0, key="predictive_processing",
    name="Pattern Sense", name_tr="Örüntü Algısı",
    layer="neuroscience", parent_key="expectancy",
    belief_indices=(20, 21, 28, 84, 85),
)
INFORMATION_ENTROPY = Dimension(
    index=1, key="information_entropy",
    name="Wonder", name_tr="Hayret",
    layer="neuroscience", parent_key="expectancy",
    belief_indices=(3, 7, 17, 19, 30),
)

# --- Discovery / Information Rate ---
SEQUENCE_LEARNING = Dimension(
    index=2, key="sequence_learning",
    name="Learning", name_tr="Öğrenme",
    layer="neuroscience", parent_key="information_rate",
    belief_indices=(18, 24, 25, 29, 31),
)
SENSORY_ENCODING = Dimension(
    index=3, key="sensory_encoding",
    name="Sound Awareness", name_tr="Ses Farkındalığı",
    layer="neuroscience", parent_key="information_rate",
    belief_indices=(0, 13, 16, 33, 35, 39),
)

# --- Intensity / Tension Arc ---
HARMONIC_TENSION = Dimension(
    index=4, key="harmonic_tension",
    name="Harmonic Pull", name_tr="Harmonik Çekim",
    layer="neuroscience", parent_key="tension_arc",
    belief_indices=(4, 5, 6, 80, 82, 88),
)
AUTONOMIC_AROUSAL = Dimension(
    index=5, key="autonomic_arousal",
    name="Chills", name_tr="Tüyler Diken",
    layer="neuroscience", parent_key="tension_arc",
    belief_indices=(22, 23, 26, 60, 62, 63),
)

# --- Intensity / Sonic Impact ---
SENSORY_SALIENCE = Dimension(
    index=6, key="sensory_salience",
    name="Attention Grab", name_tr="Dikkat Çekme",
    layer="neuroscience", parent_key="sonic_impact",
    belief_indices=(15, 34, 36, 37, 38, 61),
)
AESTHETIC_APPRAISAL = Dimension(
    index=7, key="aesthetic_appraisal",
    name="Beauty Sense", name_tr="Güzellik Hissi",
    layer="neuroscience", parent_key="sonic_impact",
    belief_indices=(11, 12, 14, 27, 40, 41),
)

# --- Flow / Entrainment ---
OSCILLATION_COUPLING = Dimension(
    index=8, key="oscillation_coupling",
    name="Beat Lock", name_tr="Ritim Kilidi",
    layer="neuroscience", parent_key="entrainment",
    belief_indices=(42, 43, 44, 45, 46),
)
MOTOR_PERIOD_LOCKING = Dimension(
    index=9, key="motor_period_locking",
    name="Body Pulse", name_tr="Beden Nabzı",
    layer="neuroscience", parent_key="entrainment",
    belief_indices=(96, 97, 98, 99, 100),
)

# --- Flow / Groove ---
AUDITORY_MOTOR = Dimension(
    index=10, key="auditory_motor",
    name="Movement Urge", name_tr="Hareket Dürtüsü",
    layer="neuroscience", parent_key="groove",
    belief_indices=(90, 91, 92, 93, 95),
)
HIERARCHICAL_CONTEXT = Dimension(
    index=11, key="hierarchical_context",
    name="Musical Story", name_tr="Müzikal Hikaye",
    layer="neuroscience", parent_key="groove",
    belief_indices=(94, 101, 102, 103, 105),
)

# --- Depth / Contagion ---
VALENCE_MODE = Dimension(
    index=12, key="valence_mode",
    name="Mood Color", name_tr="Duygu Rengi",
    layer="neuroscience", parent_key="contagion",
    belief_indices=(64, 65, 66, 67, 68),
)
NOSTALGIA_CIRCUITRY = Dimension(
    index=13, key="nostalgia_circuitry",
    name="Time Travel", name_tr="Zaman Yolculuğu",
    layer="neuroscience", parent_key="contagion",
    belief_indices=(69, 70, 71, 72, 73),
)

# --- Depth / Reward ---
DOPAMINERGIC_DRIVE = Dimension(
    index=14, key="dopaminergic_drive",
    name="Craving", name_tr="Özlem",
    layer="neuroscience", parent_key="reward",
    belief_indices=(74, 75, 76, 77, 78),
)
HEDONIC_VALUATION = Dimension(
    index=15, key="hedonic_valuation",
    name="Bliss", name_tr="Keyif",
    layer="neuroscience", parent_key="reward",
    belief_indices=(79, 81, 83, 86, 87, 89),
)

# --- Trace / Episodic Resonance ---
HIPPOCAMPAL_BINDING = Dimension(
    index=16, key="hippocampal_binding",
    name="Déjà Vu", name_tr="Déjà Vu",
    layer="neuroscience", parent_key="episodic_resonance",
    belief_indices=(47, 48, 49, 54, 57, 58, 59),
)
AUTOBIOGRAPHICAL = Dimension(
    index=17, key="autobiographical",
    name="Life Story", name_tr="Yaşam Öyküsü",
    layer="neuroscience", parent_key="episodic_resonance",
    belief_indices=(50, 51, 52, 53, 55, 56),
)

# --- Trace / Recognition ---
PITCH_MELODY = Dimension(
    index=18, key="pitch_melody",
    name="Melodic Ear", name_tr="Melodik Kulak",
    layer="neuroscience", parent_key="recognition",
    belief_indices=(1, 2, 8, 9, 10, 32),
)
PERCEPTUAL_LEARNING = Dimension(
    index=19, key="perceptual_learning",
    name="Trained Ear", name_tr="Eğitimli Kulak",
    layer="neuroscience", parent_key="recognition",
    belief_indices=(107, 108, 109, 110, 111, 112, 113),
)

# --- Sharing / Synchrony ---
STRUCTURAL_PREDICTION = Dimension(
    index=20, key="structural_prediction",
    name="Musical Intuition", name_tr="Müzikal Sezgi",
    layer="neuroscience", parent_key="synchrony",
    belief_indices=(104, 106, 114, 115),
)
EXPERTISE_NETWORK = Dimension(
    index=21, key="expertise_network",
    name="Mastery", name_tr="Ustalık",
    layer="neuroscience", parent_key="synchrony",
    belief_indices=(116, 117, 118, 119, 120),
)

# --- Sharing / Bonding ---
INTERPERSONAL_SYNC = Dimension(
    index=22, key="interpersonal_sync",
    name="Shared Pulse", name_tr="Ortak Nabız",
    layer="neuroscience", parent_key="bonding",
    belief_indices=(122, 123, 124, 128, 130),
)
SOCIAL_REWARD = Dimension(
    index=23, key="social_reward",
    name="Together Joy", name_tr="Birlikte Neşe",
    layer="neuroscience", parent_key="bonding",
    belief_indices=(121, 125, 126, 127, 129),
)


# ======================================================================
# 12D — MUSIC COGNITION LAYER (each aggregates 2 neuroscience children)
# ======================================================================

EXPECTANCY = Dimension(
    index=0, key="expectancy",
    name="Anticipation", name_tr="Önsezi",
    layer="cognition", parent_key="discovery",
    belief_indices=PREDICTIVE_PROCESSING.belief_indices + INFORMATION_ENTROPY.belief_indices,
)
INFORMATION_RATE = Dimension(
    index=1, key="information_rate",
    name="Surprise", name_tr="Sürpriz",
    layer="cognition", parent_key="discovery",
    belief_indices=SEQUENCE_LEARNING.belief_indices + SENSORY_ENCODING.belief_indices,
)

TENSION_ARC = Dimension(
    index=2, key="tension_arc",
    name="Tension", name_tr="Gerilim",
    layer="cognition", parent_key="intensity",
    belief_indices=HARMONIC_TENSION.belief_indices + AUTONOMIC_AROUSAL.belief_indices,
)
SONIC_IMPACT = Dimension(
    index=3, key="sonic_impact",
    name="Impact", name_tr="Etki",
    layer="cognition", parent_key="intensity",
    belief_indices=SENSORY_SALIENCE.belief_indices + AESTHETIC_APPRAISAL.belief_indices,
)

ENTRAINMENT = Dimension(
    index=4, key="entrainment",
    name="Sync", name_tr="Senkron",
    layer="cognition", parent_key="flow",
    belief_indices=OSCILLATION_COUPLING.belief_indices + MOTOR_PERIOD_LOCKING.belief_indices,
)
GROOVE = Dimension(
    index=5, key="groove",
    name="Groove", name_tr="Groove",
    layer="cognition", parent_key="flow",
    belief_indices=AUDITORY_MOTOR.belief_indices + HIERARCHICAL_CONTEXT.belief_indices,
)

CONTAGION = Dimension(
    index=6, key="contagion",
    name="Empathy", name_tr="Empati",
    layer="cognition", parent_key="depth",
    belief_indices=VALENCE_MODE.belief_indices + NOSTALGIA_CIRCUITRY.belief_indices,
)
REWARD = Dimension(
    index=7, key="reward",
    name="Pleasure", name_tr="Haz",
    layer="cognition", parent_key="depth",
    belief_indices=DOPAMINERGIC_DRIVE.belief_indices + HEDONIC_VALUATION.belief_indices,
)

EPISODIC_RESONANCE = Dimension(
    index=8, key="episodic_resonance",
    name="Nostalgia", name_tr="Nostalji",
    layer="cognition", parent_key="trace",
    belief_indices=HIPPOCAMPAL_BINDING.belief_indices + AUTOBIOGRAPHICAL.belief_indices,
)
RECOGNITION = Dimension(
    index=9, key="recognition",
    name="Familiarity", name_tr="Tanıdıklık",
    layer="cognition", parent_key="trace",
    belief_indices=PITCH_MELODY.belief_indices + PERCEPTUAL_LEARNING.belief_indices,
)

SYNCHRONY = Dimension(
    index=10, key="synchrony",
    name="Togetherness", name_tr="Birliktelik",
    layer="cognition", parent_key="sharing",
    belief_indices=STRUCTURAL_PREDICTION.belief_indices + EXPERTISE_NETWORK.belief_indices,
)
BONDING = Dimension(
    index=11, key="bonding",
    name="Bonding", name_tr="Bağlanma",
    layer="cognition", parent_key="sharing",
    belief_indices=INTERPERSONAL_SYNC.belief_indices + SOCIAL_REWARD.belief_indices,
)


# ======================================================================
# 6D — PSYCHOLOGY LAYER (experiential, each aggregates 2 cognition children)
# ======================================================================

DISCOVERY = Dimension(
    index=0, key="discovery",
    name="Curiosity", name_tr="Merak",
    layer="psychology", parent_key=None,
    belief_indices=EXPECTANCY.belief_indices + INFORMATION_RATE.belief_indices,
)
INTENSITY = Dimension(
    index=1, key="intensity",
    name="Energy", name_tr="Enerji",
    layer="psychology", parent_key=None,
    belief_indices=TENSION_ARC.belief_indices + SONIC_IMPACT.belief_indices,
)
FLOW = Dimension(
    index=2, key="flow",
    name="Rhythm", name_tr="Ritim",
    layer="psychology", parent_key=None,
    belief_indices=ENTRAINMENT.belief_indices + GROOVE.belief_indices,
)
DEPTH = Dimension(
    index=3, key="depth",
    name="Emotion", name_tr="Duygu",
    layer="psychology", parent_key=None,
    belief_indices=CONTAGION.belief_indices + REWARD.belief_indices,
)
TRACE = Dimension(
    index=4, key="trace",
    name="Memory", name_tr="Hafıza",
    layer="psychology", parent_key=None,
    belief_indices=EPISODIC_RESONANCE.belief_indices + RECOGNITION.belief_indices,
)
SHARING = Dimension(
    index=5, key="sharing",
    name="Connection", name_tr="Bağ",
    layer="psychology", parent_key=None,
    belief_indices=SYNCHRONY.belief_indices + BONDING.belief_indices,
)
