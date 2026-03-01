"""Registry — collects all 42 dimensions into lookup structures.

Three independent tiers (NOT hierarchically derived):
    Psychology   (6D)  — gut-level, free tier
    Cognition    (12D) — informed listener, basic tier
    Neuroscience (24D) — expert, premium tier

Pattern follows: Musical_Intelligence/brain/regions/registry.py
"""
from __future__ import annotations

from typing import Dict, Tuple

from ._dimension import Dimension

# --- 6D Psychology ---
from .tree import (
    COMPLEXITY,
    ENERGY,
    GROOVE,
    TEMPO,
    TENSION,
    VALENCE,
)

# --- 12D Cognition ---
from .tree import (
    EMOTIONAL_ARC,
    FAMILIARITY,
    HARMONIC_DEPTH,
    MELODIC_HOOK,
    MOMENTUM,
    NARRATIVE,
    PLEASURE,
    REPETITION,
    RHYTHMIC_DRIVE,
    SPACE,
    SURPRISE,
    TIMBRAL_COLOR,
)

# --- 24D Neuroscience ---
from .tree import (
    AUDITORY_MOTOR_BIND,
    AUTOBIOGRAPHICAL,
    AUTONOMIC_AROUSAL,
    CHILLS_PATHWAY,
    COLLECTIVE_REWARD,
    DA_ANTICIPATION,
    DA_CONSUMMATION,
    EPISODIC_ENCODING,
    EXPERTISE_EFFECT,
    HEDONIC_TONE,
    INFORMATION_CONTENT,
    MODEL_UNCERTAINTY,
    MOTOR_PERIOD_LOCK,
    NEURAL_SYNCHRONY,
    NOSTALGIA_CIRCUIT,
    OSCILLATION_COUPLING,
    PRECISION,
    PREDICTION_ERROR,
    REWARD_PE,
    SOCIAL_BONDING,
    SOCIAL_PREDICTION,
    STATISTICAL_LEARNING,
    TIMING_PRECISION,
    VALENCE_MODE,
)

# ======================================================================
# Ordered tuples — canonical order by index
# ======================================================================

ALL_PSYCHOLOGY: Tuple[Dimension, ...] = (
    ENERGY, VALENCE, TEMPO, TENSION, GROOVE, COMPLEXITY,
)

ALL_COGNITION: Tuple[Dimension, ...] = (
    MELODIC_HOOK, HARMONIC_DEPTH, RHYTHMIC_DRIVE, TIMBRAL_COLOR,
    EMOTIONAL_ARC, SURPRISE, MOMENTUM, NARRATIVE,
    FAMILIARITY, PLEASURE, SPACE, REPETITION,
)

ALL_NEUROSCIENCE: Tuple[Dimension, ...] = (
    # Predictive Processing (0-3)
    PREDICTION_ERROR, PRECISION, INFORMATION_CONTENT, MODEL_UNCERTAINTY,
    # Sensorimotor (4-7)
    OSCILLATION_COUPLING, MOTOR_PERIOD_LOCK, AUDITORY_MOTOR_BIND, TIMING_PRECISION,
    # Emotion Circuitry (8-11)
    VALENCE_MODE, AUTONOMIC_AROUSAL, NOSTALGIA_CIRCUIT, CHILLS_PATHWAY,
    # Reward System (12-15)
    DA_ANTICIPATION, DA_CONSUMMATION, HEDONIC_TONE, REWARD_PE,
    # Memory & Learning (16-19)
    EPISODIC_ENCODING, AUTOBIOGRAPHICAL, STATISTICAL_LEARNING, EXPERTISE_EFFECT,
    # Social Cognition (20-23)
    NEURAL_SYNCHRONY, SOCIAL_BONDING, SOCIAL_PREDICTION, COLLECTIVE_REWARD,
)

# ======================================================================
# Counts
# ======================================================================

NUM_PSYCHOLOGY: int = len(ALL_PSYCHOLOGY)
NUM_COGNITION: int = len(ALL_COGNITION)
NUM_NEUROSCIENCE: int = len(ALL_NEUROSCIENCE)

assert NUM_PSYCHOLOGY == 6, f"Expected 6 psychology dims, got {NUM_PSYCHOLOGY}"
assert NUM_COGNITION == 12, f"Expected 12 cognition dims, got {NUM_COGNITION}"
assert NUM_NEUROSCIENCE == 24, f"Expected 24 neuroscience dims, got {NUM_NEUROSCIENCE}"

# ======================================================================
# Lookup dicts
# ======================================================================

DIM_BY_KEY: Dict[str, Dimension] = {}
for _dim in ALL_PSYCHOLOGY + ALL_COGNITION + ALL_NEUROSCIENCE:
    DIM_BY_KEY[_dim.key] = _dim

# ======================================================================
# Ordered name tuples (for axis labels, charts, etc.)
# ======================================================================

PSYCHOLOGY_NAMES: Tuple[str, ...] = tuple(d.name for d in ALL_PSYCHOLOGY)
PSYCHOLOGY_NAMES_TR: Tuple[str, ...] = tuple(d.name_tr for d in ALL_PSYCHOLOGY)
COGNITION_NAMES: Tuple[str, ...] = tuple(d.name for d in ALL_COGNITION)
COGNITION_NAMES_TR: Tuple[str, ...] = tuple(d.name_tr for d in ALL_COGNITION)
NEUROSCIENCE_NAMES: Tuple[str, ...] = tuple(d.name for d in ALL_NEUROSCIENCE)
NEUROSCIENCE_NAMES_TR: Tuple[str, ...] = tuple(d.name_tr for d in ALL_NEUROSCIENCE)
