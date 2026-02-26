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
    name="Predictive Processing", name_tr="Tahminsel İşleme",
    layer="neuroscience", parent_key="expectancy",
    belief_indices=(20, 21, 28, 84, 85),
)
INFORMATION_ENTROPY = Dimension(
    index=1, key="information_entropy",
    name="Information Entropy", name_tr="Bilgi Entropisi",
    layer="neuroscience", parent_key="expectancy",
    belief_indices=(3, 7, 17, 19, 30),
)

# --- Discovery / Information Rate ---
SEQUENCE_LEARNING = Dimension(
    index=2, key="sequence_learning",
    name="Sequence Learning", name_tr="Dizi Öğrenme",
    layer="neuroscience", parent_key="information_rate",
    belief_indices=(18, 24, 25, 29, 31),
)
SENSORY_ENCODING = Dimension(
    index=3, key="sensory_encoding",
    name="Sensory Encoding", name_tr="Duyusal Kodlama",
    layer="neuroscience", parent_key="information_rate",
    belief_indices=(0, 13, 16, 33, 35, 39),
)

# --- Intensity / Tension Arc ---
HARMONIC_TENSION = Dimension(
    index=4, key="harmonic_tension",
    name="Harmonic Tension", name_tr="Harmonik Gerilim",
    layer="neuroscience", parent_key="tension_arc",
    belief_indices=(4, 5, 6, 80, 82, 88),
)
AUTONOMIC_AROUSAL = Dimension(
    index=5, key="autonomic_arousal",
    name="Autonomic Arousal", name_tr="Otonom Uyarılma",
    layer="neuroscience", parent_key="tension_arc",
    belief_indices=(22, 23, 26, 60, 62, 63),
)

# --- Intensity / Sonic Impact ---
SENSORY_SALIENCE = Dimension(
    index=6, key="sensory_salience",
    name="Sensory Salience", name_tr="Duyusal Belirginlik",
    layer="neuroscience", parent_key="sonic_impact",
    belief_indices=(15, 34, 36, 37, 38, 61),
)
AESTHETIC_APPRAISAL = Dimension(
    index=7, key="aesthetic_appraisal",
    name="Aesthetic Appraisal", name_tr="Estetik Değerlendirme",
    layer="neuroscience", parent_key="sonic_impact",
    belief_indices=(11, 12, 14, 27, 40, 41),
)

# --- Flow / Entrainment ---
OSCILLATION_COUPLING = Dimension(
    index=8, key="oscillation_coupling",
    name="Oscillation Coupling", name_tr="Osilasyon Eşleşmesi",
    layer="neuroscience", parent_key="entrainment",
    belief_indices=(42, 43, 44, 45, 46),
)
MOTOR_PERIOD_LOCKING = Dimension(
    index=9, key="motor_period_locking",
    name="Motor Period-Locking", name_tr="Motor Periyot Kilidi",
    layer="neuroscience", parent_key="entrainment",
    belief_indices=(96, 97, 98, 99, 100),
)

# --- Flow / Groove ---
AUDITORY_MOTOR = Dimension(
    index=10, key="auditory_motor",
    name="Auditory-Motor Integration", name_tr="İşitsel-Motor Entegrasyon",
    layer="neuroscience", parent_key="groove",
    belief_indices=(90, 91, 92, 93, 95),
)
HIERARCHICAL_CONTEXT = Dimension(
    index=11, key="hierarchical_context",
    name="Hierarchical Context", name_tr="Hiyerarşik Bağlam",
    layer="neuroscience", parent_key="groove",
    belief_indices=(94, 101, 102, 103, 105),
)

# --- Depth / Contagion ---
VALENCE_MODE = Dimension(
    index=12, key="valence_mode",
    name="Valence-Mode Circuitry", name_tr="Valans-Mod Devresi",
    layer="neuroscience", parent_key="contagion",
    belief_indices=(64, 65, 66, 67, 68),
)
NOSTALGIA_CIRCUITRY = Dimension(
    index=13, key="nostalgia_circuitry",
    name="Nostalgia Circuitry", name_tr="Nostalji Devresi",
    layer="neuroscience", parent_key="contagion",
    belief_indices=(69, 70, 71, 72, 73),
)

# --- Depth / Reward ---
DOPAMINERGIC_DRIVE = Dimension(
    index=14, key="dopaminergic_drive",
    name="Dopaminergic Drive", name_tr="Dopaminerjik Dürtü",
    layer="neuroscience", parent_key="reward",
    belief_indices=(74, 75, 76, 77, 78),
)
HEDONIC_VALUATION = Dimension(
    index=15, key="hedonic_valuation",
    name="Hedonic Valuation", name_tr="Hedonik Değerleme",
    layer="neuroscience", parent_key="reward",
    belief_indices=(79, 81, 83, 86, 87, 89),
)

# --- Trace / Episodic Resonance ---
HIPPOCAMPAL_BINDING = Dimension(
    index=16, key="hippocampal_binding",
    name="Hippocampal Binding", name_tr="Hipokampal Bağlama",
    layer="neuroscience", parent_key="episodic_resonance",
    belief_indices=(47, 48, 49, 54, 57, 58, 59),
)
AUTOBIOGRAPHICAL = Dimension(
    index=17, key="autobiographical",
    name="Autobiographical Network", name_tr="Otobiyografik Ağ",
    layer="neuroscience", parent_key="episodic_resonance",
    belief_indices=(50, 51, 52, 53, 55, 56),
)

# --- Trace / Recognition ---
PITCH_MELODY = Dimension(
    index=18, key="pitch_melody",
    name="Pitch-Melody Processing", name_tr="Perde-Melodi İşleme",
    layer="neuroscience", parent_key="recognition",
    belief_indices=(1, 2, 8, 9, 10, 32),
)
PERCEPTUAL_LEARNING = Dimension(
    index=19, key="perceptual_learning",
    name="Perceptual Learning", name_tr="Algısal Öğrenme",
    layer="neuroscience", parent_key="recognition",
    belief_indices=(107, 108, 109, 110, 111, 112, 113),
)

# --- Sharing / Synchrony ---
STRUCTURAL_PREDICTION = Dimension(
    index=20, key="structural_prediction",
    name="Structural Prediction", name_tr="Yapısal Tahmin",
    layer="neuroscience", parent_key="synchrony",
    belief_indices=(104, 106, 114, 115),
)
EXPERTISE_NETWORK = Dimension(
    index=21, key="expertise_network",
    name="Expertise Network", name_tr="Uzmanlık Ağı",
    layer="neuroscience", parent_key="synchrony",
    belief_indices=(116, 117, 118, 119, 120),
)

# --- Sharing / Bonding ---
INTERPERSONAL_SYNC = Dimension(
    index=22, key="interpersonal_sync",
    name="Interpersonal Synchrony", name_tr="Kişilerarası Senkronizasyon",
    layer="neuroscience", parent_key="bonding",
    belief_indices=(122, 123, 124, 128, 130),
)
SOCIAL_REWARD = Dimension(
    index=23, key="social_reward",
    name="Social Reward", name_tr="Sosyal Ödül",
    layer="neuroscience", parent_key="bonding",
    belief_indices=(121, 125, 126, 127, 129),
)


# ======================================================================
# 12D — MUSIC COGNITION LAYER (each aggregates 2 neuroscience children)
# ======================================================================

EXPECTANCY = Dimension(
    index=0, key="expectancy",
    name="Expectancy", name_tr="Beklenti",
    layer="cognition", parent_key="discovery",
    belief_indices=PREDICTIVE_PROCESSING.belief_indices + INFORMATION_ENTROPY.belief_indices,
)
INFORMATION_RATE = Dimension(
    index=1, key="information_rate",
    name="Information Rate", name_tr="Bilgi Hızı",
    layer="cognition", parent_key="discovery",
    belief_indices=SEQUENCE_LEARNING.belief_indices + SENSORY_ENCODING.belief_indices,
)

TENSION_ARC = Dimension(
    index=2, key="tension_arc",
    name="Tension Arc", name_tr="Gerilim Yayı",
    layer="cognition", parent_key="intensity",
    belief_indices=HARMONIC_TENSION.belief_indices + AUTONOMIC_AROUSAL.belief_indices,
)
SONIC_IMPACT = Dimension(
    index=3, key="sonic_impact",
    name="Sonic Impact", name_tr="Sonik Etki",
    layer="cognition", parent_key="intensity",
    belief_indices=SENSORY_SALIENCE.belief_indices + AESTHETIC_APPRAISAL.belief_indices,
)

ENTRAINMENT = Dimension(
    index=4, key="entrainment",
    name="Entrainment", name_tr="Senkronizasyon",
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
    name="Emotional Contagion", name_tr="Duygusal Bulaşma",
    layer="cognition", parent_key="depth",
    belief_indices=VALENCE_MODE.belief_indices + NOSTALGIA_CIRCUITRY.belief_indices,
)
REWARD = Dimension(
    index=7, key="reward",
    name="Reward", name_tr="Ödül",
    layer="cognition", parent_key="depth",
    belief_indices=DOPAMINERGIC_DRIVE.belief_indices + HEDONIC_VALUATION.belief_indices,
)

EPISODIC_RESONANCE = Dimension(
    index=8, key="episodic_resonance",
    name="Episodic Resonance", name_tr="Epizodik Rezonans",
    layer="cognition", parent_key="trace",
    belief_indices=HIPPOCAMPAL_BINDING.belief_indices + AUTOBIOGRAPHICAL.belief_indices,
)
RECOGNITION = Dimension(
    index=9, key="recognition",
    name="Recognition", name_tr="Tanıma",
    layer="cognition", parent_key="trace",
    belief_indices=PITCH_MELODY.belief_indices + PERCEPTUAL_LEARNING.belief_indices,
)

SYNCHRONY = Dimension(
    index=10, key="synchrony",
    name="Synchrony", name_tr="Senkroni",
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
    name="Discovery", name_tr="Keşif",
    layer="psychology", parent_key=None,
    belief_indices=EXPECTANCY.belief_indices + INFORMATION_RATE.belief_indices,
)
INTENSITY = Dimension(
    index=1, key="intensity",
    name="Intensity", name_tr="Yoğunluk",
    layer="psychology", parent_key=None,
    belief_indices=TENSION_ARC.belief_indices + SONIC_IMPACT.belief_indices,
)
FLOW = Dimension(
    index=2, key="flow",
    name="Flow", name_tr="Akış",
    layer="psychology", parent_key=None,
    belief_indices=ENTRAINMENT.belief_indices + GROOVE.belief_indices,
)
DEPTH = Dimension(
    index=3, key="depth",
    name="Depth", name_tr="Derinlik",
    layer="psychology", parent_key=None,
    belief_indices=CONTAGION.belief_indices + REWARD.belief_indices,
)
TRACE = Dimension(
    index=4, key="trace",
    name="Trace", name_tr="İz",
    layer="psychology", parent_key=None,
    belief_indices=EPISODIC_RESONANCE.belief_indices + RECOGNITION.belief_indices,
)
SHARING = Dimension(
    index=5, key="sharing",
    name="Sharing", name_tr="Paylaşım",
    layer="psychology", parent_key=None,
    belief_indices=SYNCHRONY.belief_indices + BONDING.belief_indices,
)
