"""Dual-Radar Dimension System — 5+5 intuitive bipolar axes.

Two independent radars, each with 5 bipolar dimensions:

Radar 1: "What You Hear" (Musical Character)
    Slow↔Fast, Quiet↔Loud, Light↔Heavy, Smooth↔Rough, Thin↔Deep

Radar 2: "How It Feels" (Emotional Feel)
    Sad↔Happy, Chill↔Hyped, Soft↔Hard, Surprising↔Predictable, Dreamy↔Focused

Each dimension is independently computed from beliefs only.

Usage::

    from Musical_Intelligence.brain.dimensions import DimensionInterpreter
    interpreter = DimensionInterpreter()
    result = interpreter.interpret_numpy(beliefs)  # → dict of numpy arrays
"""

from .interpreter import DimensionInterpreter
from .models.musical import MUSICAL_NAMES, MUSICAL_LABELS
from .models.emotional import EMOTIONAL_NAMES, EMOTIONAL_LABELS

__all__ = [
    "DimensionInterpreter",
    "MUSICAL_NAMES",
    "MUSICAL_LABELS",
    "EMOTIONAL_NAMES",
    "EMOTIONAL_LABELS",
]
