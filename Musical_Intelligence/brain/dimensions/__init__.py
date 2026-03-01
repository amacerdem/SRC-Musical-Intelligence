"""3-Tier Falsifiability Dimension System — independent 6D + 12D + 24D.

Three independent tiers (NOT hierarchically derived):

    Psychology   (6D)  — gut-level, zero training  (free tier)
    Cognition    (12D) — informed listener          (basic tier)
    Neuroscience (24D) — expert, neuroscience       (premium tier)

Each tier is independently computed from (beliefs, ram, neuro).

Usage::

    from Musical_Intelligence.brain.dimensions import DimensionInterpreter
    interpreter = DimensionInterpreter()
    state = interpreter.interpret(beliefs, ram, neuro)  # → DimensionState
"""

from ._dimension import Dimension
from .interpreter import DimensionInterpreter
from .registry import (
    ALL_COGNITION,
    ALL_NEUROSCIENCE,
    ALL_PSYCHOLOGY,
    COGNITION_NAMES,
    COGNITION_NAMES_TR,
    DIM_BY_KEY,
    NEUROSCIENCE_NAMES,
    NEUROSCIENCE_NAMES_TR,
    NUM_COGNITION,
    NUM_NEUROSCIENCE,
    NUM_PSYCHOLOGY,
    PSYCHOLOGY_NAMES,
    PSYCHOLOGY_NAMES_TR,
)

__all__ = [
    "Dimension",
    "DimensionInterpreter",
    "ALL_PSYCHOLOGY",
    "ALL_COGNITION",
    "ALL_NEUROSCIENCE",
    "DIM_BY_KEY",
    "NUM_PSYCHOLOGY",
    "NUM_COGNITION",
    "NUM_NEUROSCIENCE",
    "PSYCHOLOGY_NAMES",
    "PSYCHOLOGY_NAMES_TR",
    "COGNITION_NAMES",
    "COGNITION_NAMES_TR",
    "NEUROSCIENCE_NAMES",
    "NEUROSCIENCE_NAMES_TR",
]
