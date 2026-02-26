"""Registry — collects all 42 dimensions into lookup structures.

This is the single source of truth for the hierarchical dimension tree.
Three layers: Psychology (6D), Cognition (12D), Neuroscience (24D).

Pattern follows: Musical_Intelligence/brain/regions/registry.py
"""
from __future__ import annotations

from typing import Dict, Tuple

from ._dimension import Dimension

# --- 24D Neuroscience (leaf nodes) ---
from .tree import (
    PREDICTIVE_PROCESSING,
    INFORMATION_ENTROPY,
    SEQUENCE_LEARNING,
    SENSORY_ENCODING,
    HARMONIC_TENSION,
    AUTONOMIC_AROUSAL,
    SENSORY_SALIENCE,
    AESTHETIC_APPRAISAL,
    OSCILLATION_COUPLING,
    MOTOR_PERIOD_LOCKING,
    AUDITORY_MOTOR,
    HIERARCHICAL_CONTEXT,
    VALENCE_MODE,
    NOSTALGIA_CIRCUITRY,
    DOPAMINERGIC_DRIVE,
    HEDONIC_VALUATION,
    HIPPOCAMPAL_BINDING,
    AUTOBIOGRAPHICAL,
    PITCH_MELODY,
    PERCEPTUAL_LEARNING,
    STRUCTURAL_PREDICTION,
    EXPERTISE_NETWORK,
    INTERPERSONAL_SYNC,
    SOCIAL_REWARD,
)

# --- 12D Cognition ---
from .tree import (
    EXPECTANCY,
    INFORMATION_RATE,
    TENSION_ARC,
    SONIC_IMPACT,
    ENTRAINMENT,
    GROOVE,
    CONTAGION,
    REWARD,
    EPISODIC_RESONANCE,
    RECOGNITION,
    SYNCHRONY,
    BONDING,
)

# --- 6D Psychology ---
from .tree import (
    DISCOVERY,
    INTENSITY,
    FLOW,
    DEPTH,
    TRACE,
    SHARING,
)

# ======================================================================
# Ordered tuples — canonical order by index
# ======================================================================

ALL_PSYCHOLOGY: Tuple[Dimension, ...] = (
    DISCOVERY, INTENSITY, FLOW, DEPTH, TRACE, SHARING,
)

ALL_COGNITION: Tuple[Dimension, ...] = (
    EXPECTANCY, INFORMATION_RATE, TENSION_ARC, SONIC_IMPACT,
    ENTRAINMENT, GROOVE, CONTAGION, REWARD,
    EPISODIC_RESONANCE, RECOGNITION, SYNCHRONY, BONDING,
)

ALL_NEUROSCIENCE: Tuple[Dimension, ...] = (
    PREDICTIVE_PROCESSING, INFORMATION_ENTROPY,
    SEQUENCE_LEARNING, SENSORY_ENCODING,
    HARMONIC_TENSION, AUTONOMIC_AROUSAL,
    SENSORY_SALIENCE, AESTHETIC_APPRAISAL,
    OSCILLATION_COUPLING, MOTOR_PERIOD_LOCKING,
    AUDITORY_MOTOR, HIERARCHICAL_CONTEXT,
    VALENCE_MODE, NOSTALGIA_CIRCUITRY,
    DOPAMINERGIC_DRIVE, HEDONIC_VALUATION,
    HIPPOCAMPAL_BINDING, AUTOBIOGRAPHICAL,
    PITCH_MELODY, PERCEPTUAL_LEARNING,
    STRUCTURAL_PREDICTION, EXPERTISE_NETWORK,
    INTERPERSONAL_SYNC, SOCIAL_REWARD,
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
NEUROSCIENCE_NAMES: Tuple[str, ...] = tuple(d.name for d in ALL_NEUROSCIENCE)

# ======================================================================
# Integrity check — all 131 beliefs must appear exactly once
# ======================================================================

_all_leaf_indices: set = set()
for _d in ALL_NEUROSCIENCE:
    for _idx in _d.belief_indices:
        assert _idx not in _all_leaf_indices, (
            f"Belief {_idx} appears in multiple 24D nodes"
        )
        _all_leaf_indices.add(_idx)

assert _all_leaf_indices == set(range(131)), (
    f"Belief coverage mismatch. "
    f"Missing: {set(range(131)) - _all_leaf_indices}, "
    f"Extra: {_all_leaf_indices - set(range(131))}"
)
