"""
SPU (Spectral Processing Unit) -- All cognitive models.

9 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        BCH  -- Brainstem Consonance Hierarchy        (12D)
        PSCL -- Pitch-Space Cortical Lateralization    (12D)
        PCCR -- Pitch Chroma Cortical Representation   (11D)

    Beta (correlational, 5 <= k < 10):
        STAI -- Spectral-Temporal Auditory Integration  (12D)
        TSCP -- Timbre-Specific Cortical Plasticity     (10D)
        MIAA -- Musical Imagery Auditory Activation     (11D)

    Gamma (exploratory, k < 5):
        SDNPS-- Stimulus-Dependent Neural Pitch Scaling (10D)
        ESME -- Expertise-Specific MMN Enhancement      (11D)
        SDED -- Sensory Dissonance Early Detection      (10D)

Total SPU output: 99D per frame.
"""

from .bch import BCH
from .esme import ESME
from .miaa import MIAA
from .pccr import PCCR
from .pscl import PSCL
from .sdnps import SDNPS
from .sded import SDED
from .stai import STAI
from .tscp import TSCP

__all__ = [
    # Alpha
    "BCH",
    "PSCL",
    "PCCR",
    # Beta
    "STAI",
    "TSCP",
    "MIAA",
    # Gamma
    "SDNPS",
    "ESME",
    "SDED",
]

ALL_SPU_MODELS = (BCH, PSCL, PCCR, STAI, TSCP, MIAA, SDNPS, ESME, SDED)
"""Ordered tuple of all SPU model classes for registry auto-discovery."""
