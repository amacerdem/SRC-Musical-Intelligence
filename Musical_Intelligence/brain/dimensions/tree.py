"""Dimension definitions — 6D + 12D + 24D independent tiers.

Three tiers selected for falsifiability (listener validation ability):
    6D  Psychology   — gut-level, zero training needed
    12D Cognition    — informed listener, some music knowledge
    24D Neuroscience — expert, requires neuroscience / music cognition

Each tier is independently computed from beliefs only.
NO tier derives from another tier's output.
Computation models: ``dimensions/models/{psychology,cognition,neuroscience}.py``
"""
from __future__ import annotations

from ._dimension import Dimension

# ======================================================================
# 6D — PSYCHOLOGY (gut-level, free tier)
# ======================================================================

ENERGY = Dimension(
    index=0, key="energy",
    name="Energy", name_tr="Enerji",
    layer="psychology",
    description="Is this loud/intense or quiet/gentle?",
    agreement="very_high",
    belief_indices=(16, 34, 35, 63),  # spectral_complexity, salience, sensory_load, emotional_arousal
)
VALENCE = Dimension(
    index=1, key="valence",
    name="Valence", name_tr="Duygu Tonu",
    layer="psychology",
    description="Does this sound happy or sad?",
    agreement="high",
    belief_indices=(4, 67, 68, 81, 89),  # harmonic_stability, happy, sad, liking, wanting
)
TEMPO = Dimension(
    index=2, key="tempo",
    name="Tempo", name_tr="Hız",
    layer="psychology",
    description="Is this fast or slow?",
    agreement="very_high",
    belief_indices=(42, 95, 98),  # beat_entrainment, motor_preparation, period_entrainment
)
TENSION = Dimension(
    index=3, key="tension",
    name="Tension", name_tr="Gerilim",
    layer="psychology",
    description="Do I feel strain or release?",
    agreement="high",
    belief_indices=(34, 60, 63, 80, 88),  # salience, ans_dominance, emotional_arousal, harmonic_tension, tension
)
GROOVE = Dimension(
    index=4, key="groove",
    name="Groove", name_tr="Hareket",
    layer="psychology",
    description="Do I want to move my body?",
    agreement="high",
    belief_indices=(42, 90, 92, 95, 99),  # beat_entrainment, aud_motor_coupling, groove_quality, motor_prep, period_lock
)
COMPLEXITY = Dimension(
    index=5, key="complexity",
    name="Density", name_tr="Yoğunluk",
    layer="psychology",
    description="How much stuff is going on?",
    agreement="high",
    belief_indices=(16, 35, 36, 101),  # spectral_complexity, sensory_load, attention_capture, context_depth
)


# ======================================================================
# 12D — COGNITION (informed listener, basic tier)
# ======================================================================

MELODIC_HOOK = Dimension(
    index=0, key="melodic_hook",
    name="Melody", name_tr="Melodi",
    layer="cognition",
    description="Is the melody catchy/memorable?",
    agreement="high",
    belief_indices=(8, 10, 13, 47, 48),  # pitch_prominence, pitch_identity, spectral_temporal_synergy, melodic_recognition, memory_preservation
)
HARMONIC_DEPTH = Dimension(
    index=1, key="harmonic_depth",
    name="Harmony", name_tr="Armoni",
    layer="cognition",
    description="Simple chords or rich/complex?",
    agreement="medium",
    belief_indices=(4, 5, 6, 21, 80),  # harmonic_stability, template_match, interval_quality, prediction_hierarchy, harmonic_tension
)
RHYTHMIC_DRIVE = Dimension(
    index=2, key="rhythmic_drive",
    name="Rhythm", name_tr="Ritim",
    layer="cognition",
    description="Basic beat or layered/syncopated?",
    agreement="high",
    belief_indices=(42, 44, 90, 92, 94),  # beat_entrainment, meter_hierarchy, aud_motor, groove, meter_structure
)
TIMBRAL_COLOR = Dimension(
    index=3, key="timbral_color",
    name="Timbre", name_tr="Tını",
    layer="cognition",
    description="Warm/organic or cold/electronic?",
    agreement="medium",
    belief_indices=(11, 13, 15, 16, 111),  # aesthetic_quality, spectral_temporal_synergy, timbral_character, spectral_complexity, trained_timbre
)
EMOTIONAL_ARC = Dimension(
    index=4, key="emotional_arc",
    name="Emotion", name_tr="Duygu",
    layer="cognition",
    description="Which specific emotion? Joy? Awe? Nostalgia?",
    agreement="high",
    belief_indices=(63, 64, 67, 68, 70),  # emotional_arousal, emotion_certainty, happy, sad, nostalgia_affect
)
SURPRISE = Dimension(
    index=5, key="surprise",
    name="Surprise", name_tr="Sürpriz",
    layer="cognition",
    description="Did something unexpected happen?",
    agreement="medium",
    belief_indices=(21, 25, 75, 84),  # prediction_hierarchy, information_content, da_nacc, prediction_error
)
MOMENTUM = Dimension(
    index=6, key="momentum",
    name="Momentum", name_tr="İvme",
    layer="cognition",
    description="Building to somewhere or going in circles?",
    agreement="high",
    belief_indices=(78, 79, 82, 88, 89),  # wanting_ramp, chills_proximity, peak_detection, tension, wanting
)
NARRATIVE = Dimension(
    index=7, key="narrative",
    name="Story", name_tr="Hikaye",
    layer="cognition",
    description="Is this a journey with chapters, or a loop?",
    agreement="medium",
    belief_indices=(17, 58, 101, 104, 106),  # abstract_future, episodic_boundary, context_depth, phrase_boundary, structure_pred
)
FAMILIARITY = Dimension(
    index=8, key="familiarity",
    name="Familiarity", name_tr="Tanıdıklık",
    layer="cognition",
    description="Do I recognize these patterns/style?",
    agreement="medium",
    belief_indices=(20, 31, 51, 54, 109),  # prediction_accuracy, sequence_match, emotional_coloring, retrieval_prob, statistical_model
)
PLEASURE = Dimension(
    index=9, key="pleasure",
    name="Pleasure", name_tr="Haz",
    layer="cognition",
    description="Am I enjoying this? Do I want more?",
    agreement="high",
    belief_indices=(74, 75, 81, 83, 89),  # da_caudate, da_nacc, liking, pleasure, wanting
)
SPACE = Dimension(
    index=10, key="space",
    name="Space", name_tr="Mekan",
    layer="cognition",
    description="Intimate whisper or cathedral vastness?",
    agreement="medium",
    belief_indices=(13, 16, 35, 36, 60),  # spectral_temporal_synergy, spectral_complexity, sensory_load, attention_capture, ans_dominance
)
REPETITION = Dimension(
    index=11, key="repetition",
    name="Repetition", name_tr="Tekrar",
    layer="cognition",
    description="Same loop over and over, or always changing?",
    agreement="high",
    belief_indices=(20, 25, 31, 85),  # prediction_accuracy, information_content, sequence_match, prediction_match
)


# ======================================================================
# 24D — NEUROSCIENCE (expert, premium tier)
# Organized into 6 domains × 4 parameters
# ======================================================================

# --- Predictive Processing (0-3) ---
PREDICTION_ERROR = Dimension(
    index=0, key="prediction_error",
    name="Prediction Error", name_tr="Tahmin Hatası",
    layer="neuroscience", parent_key="predictive",
    belief_indices=(25, 34, 84),  # information_content, salience, prediction_error
)
PRECISION = Dimension(
    index=1, key="precision",
    name="Precision", name_tr="Hassasiyet",
    layer="neuroscience", parent_key="predictive",
    belief_indices=(20, 39, 46),  # prediction_accuracy, precision_weighting, selective_gain
)
INFORMATION_CONTENT = Dimension(
    index=2, key="information_content",
    name="Information Content", name_tr="Bilgi İçeriği",
    layer="neuroscience", parent_key="predictive",
    belief_indices=(25,),
)
MODEL_UNCERTAINTY = Dimension(
    index=3, key="model_uncertainty",
    name="Model Uncertainty", name_tr="Model Belirsizliği",
    layer="neuroscience", parent_key="predictive",
    belief_indices=(20, 31, 46),
)

# --- Sensorimotor (4-7) ---
OSCILLATION_COUPLING = Dimension(
    index=4, key="oscillation_coupling",
    name="Beat Coupling", name_tr="Ritim Bağı",
    layer="neuroscience", parent_key="sensorimotor",
    belief_indices=(42, 44),
)
MOTOR_PERIOD_LOCK = Dimension(
    index=5, key="motor_period_lock",
    name="Period Lock", name_tr="Periyot Kilidi",
    layer="neuroscience", parent_key="sensorimotor",
    belief_indices=(96, 98, 99),  # kinematic_efficiency, period_entrainment, period_lock_strength
)
AUDITORY_MOTOR_BIND = Dimension(
    index=6, key="auditory_motor_bind",
    name="Motor Binding", name_tr="Motor Bağlama",
    layer="neuroscience", parent_key="sensorimotor",
    belief_indices=(90, 92, 95, 99),  # auditory_motor_coupling, groove_quality, motor_preparation, period_lock_strength
)
TIMING_PRECISION = Dimension(
    index=7, key="timing_precision",
    name="Timing Precision", name_tr="Zamanlama Hassasiyeti",
    layer="neuroscience", parent_key="sensorimotor",
    belief_indices=(100,),
)

# --- Emotion Circuitry (8-11) ---
VALENCE_MODE = Dimension(
    index=8, key="valence_mode",
    name="Valence Mode", name_tr="Duygu Modu",
    layer="neuroscience", parent_key="emotion",
    belief_indices=(66, 67, 68),
)
AUTONOMIC_AROUSAL = Dimension(
    index=9, key="autonomic_arousal",
    name="ANS Arousal", name_tr="Otonom Uyarılma",
    layer="neuroscience", parent_key="emotion",
    belief_indices=(35, 60, 63),  # sensory_load, ans_dominance, emotional_arousal
)
NOSTALGIA_CIRCUIT = Dimension(
    index=10, key="nostalgia_circuit",
    name="Nostalgia Circuit", name_tr="Nostalji Devresi",
    layer="neuroscience", parent_key="emotion",
    belief_indices=(50, 53, 55, 70),  # autobiographical_retrieval, nostalgia_intensity, self_relevance, nostalgia_affect
)
CHILLS_PATHWAY = Dimension(
    index=11, key="chills_pathway",
    name="Chills Pathway", name_tr="Tüylenme Yolu",
    layer="neuroscience", parent_key="emotion",
    belief_indices=(60, 61, 62, 79, 83),  # ans_dominance, chills_intensity, driving_signal, chills_proximity, pleasure
)

# --- Reward System (12-15) ---
DA_ANTICIPATION = Dimension(
    index=12, key="da_anticipation",
    name="DA Anticipation", name_tr="DA Beklenti",
    layer="neuroscience", parent_key="reward",
    belief_indices=(74, 77, 78),  # da_caudate, temporal_phase, wanting_ramp
)
DA_CONSUMMATION = Dimension(
    index=13, key="da_consummation",
    name="DA Consummation", name_tr="DA Tüketim",
    layer="neuroscience", parent_key="reward",
    belief_indices=(74, 75, 83, 89),  # da_caudate, da_nacc, pleasure, wanting
)
HEDONIC_TONE = Dimension(
    index=14, key="hedonic_tone",
    name="Hedonic Tone", name_tr="Hedonik Ton",
    layer="neuroscience", parent_key="reward",
    belief_indices=(40, 61, 81, 83),  # aesthetic_engagement, chills_intensity, liking, pleasure
)
REWARD_PE = Dimension(
    index=15, key="reward_pe",
    name="Reward PE", name_tr="Ödül TH",
    layer="neuroscience", parent_key="reward",
    belief_indices=(75, 84, 85),  # da_nacc, prediction_error, prediction_match
)

# --- Memory & Learning (16-19) ---
EPISODIC_ENCODING = Dimension(
    index=16, key="episodic_encoding",
    name="Episodic Encoding", name_tr="Epizodik Kodlama",
    layer="neuroscience", parent_key="memory",
    belief_indices=(51, 57, 59),  # emotional_coloring, consolidation_strength, episodic_encoding
)
AUTOBIOGRAPHICAL = Dimension(
    index=17, key="autobiographical",
    name="Autobiographical", name_tr="Otobiyografik",
    layer="neuroscience", parent_key="memory",
    belief_indices=(50, 51, 55),  # autobiographical_retrieval, emotional_coloring, self_relevance
)
STATISTICAL_LEARNING = Dimension(
    index=18, key="statistical_learning",
    name="Statistical Learning", name_tr="İstatistiksel Öğrenme",
    layer="neuroscience", parent_key="memory",
    belief_indices=(20, 31, 109),  # prediction_accuracy, sequence_match, statistical_model
)
EXPERTISE_EFFECT = Dimension(
    index=19, key="expertise_effect",
    name="Expertise Effect", name_tr="Uzmanlık Etkisi",
    layer="neuroscience", parent_key="memory",
    belief_indices=(111, 114, 119, 120),
)

# --- Social Cognition (20-23) ---
NEURAL_SYNCHRONY = Dimension(
    index=20, key="neural_synchrony",
    name="Neural Sync", name_tr="Nöral Senkron",
    layer="neuroscience", parent_key="social",
    belief_indices=(122, 128),  # entrainment_quality, neural_synchrony
)
SOCIAL_BONDING = Dimension(
    index=21, key="social_bonding",
    name="Social Bond", name_tr="Sosyal Bağ",
    layer="neuroscience", parent_key="social",
    belief_indices=(55, 123, 124, 126),  # self_relevance, group_flow, social_bonding, synchrony_reward
)
SOCIAL_PREDICTION = Dimension(
    index=22, key="social_prediction",
    name="Social Prediction", name_tr="Sosyal Tahmin",
    layer="neuroscience", parent_key="social",
    belief_indices=(122, 125, 130),  # entrainment_quality, social_prediction_error, social_coordination
)
COLLECTIVE_REWARD = Dimension(
    index=23, key="collective_reward",
    name="Collective Reward", name_tr="Kolektif Ödül",
    layer="neuroscience", parent_key="social",
    belief_indices=(83, 121, 126),  # pleasure, collective_pleasure, synchrony_reward
)
