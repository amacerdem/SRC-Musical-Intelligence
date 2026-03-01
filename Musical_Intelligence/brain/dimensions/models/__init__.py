"""Dimension computation models — 42 independent functions across 3 tiers.

Each tier's models compute independently from (beliefs, ram, neuro).
No tier derives from another tier's output.

Tiers:
    Psychology   (6D)  — gut-level, zero training needed to validate.
    Cognition    (12D) — informed listener, some music knowledge.
    Neuroscience (24D) — expert, requires music cognition / neuroscience.
"""
from .cognition import COGNITION_MODELS
from .neuroscience import NEUROSCIENCE_MODELS
from .psychology import PSYCHOLOGY_MODELS

__all__ = [
    "PSYCHOLOGY_MODELS",
    "COGNITION_MODELS",
    "NEUROSCIENCE_MODELS",
]
