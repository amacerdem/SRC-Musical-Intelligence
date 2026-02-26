"""Hierarchical Dimension System — 131 beliefs → 24D → 12D → 6D.

Three-layer binary tree mapping C³ beliefs to user-facing dimensions:

    Psychology  (6D)  — experiential terms  (free tier)
    Cognition   (12D) — music cognition     (basic tier)
    Neuroscience (24D) — neuroscience terms  (premium tier)

Usage::

    from Musical_Intelligence.brain.dimensions import DimensionInterpreter
    interpreter = DimensionInterpreter()
    state = interpreter.interpret(beliefs_tensor)  # (B, T, 131) → DimensionState
"""

from ._dimension import Dimension
from .interpreter import DimensionInterpreter
from .registry import (
    ALL_COGNITION,
    ALL_NEUROSCIENCE,
    ALL_PSYCHOLOGY,
    COGNITION_NAMES,
    DIM_BY_KEY,
    NEUROSCIENCE_NAMES,
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
    "NEUROSCIENCE_NAMES",
]
