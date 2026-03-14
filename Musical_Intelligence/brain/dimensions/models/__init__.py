"""Dimension computation models — 10 independent functions across 2 radars.

Radar 1: "What You Hear" (Musical Character, 5D)
    speed, volume, weight, texture, depth

Radar 2: "How It Feels" (Emotional Feel, 5D)
    mood, energy, hardness, predictability, focus
"""
from .emotional import EMOTIONAL_MODELS
from .musical import MUSICAL_MODELS

__all__ = [
    "MUSICAL_MODELS",
    "EMOTIONAL_MODELS",
]
