"""
ASU (Auditory Salience Unit) -- All cognitive models.

9 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        SNEM -- Salience Network Engagement Model       (12D)
        IACM -- Interaural Attention Capture Model       (11D)
        CSG  -- Cortical Salience Gating                 (11D)

    Beta (correlational, 5 <= k < 10):
        BARM -- Bottom-up Attention Reflex Model         (10D)
        STANM-- Spectro-Temporal Attention Network Model (10D)
        AACM -- Auditory Attention Control Model         (10D)

    Gamma (exploratory, k < 5):
        PWSM -- Pop-out Warning Salience Model           (10D)
        DGTP -- Deviance-Gated Temporal Processing       (10D)
        SDL  -- Stimulus-Driven Listening                (10D)

Total ASU output: 94D per frame.
"""

from .aacm import AACM
from .barm import BARM
from .csg import CSG
from .dgtp import DGTP
from .iacm import IACM
from .pwsm import PWSM
from .sdl import SDL
from .snem import SNEM
from .stanm import STANM

__all__ = [
    # Alpha
    "SNEM",
    "IACM",
    "CSG",
    # Beta
    "BARM",
    "STANM",
    "AACM",
    # Gamma
    "PWSM",
    "DGTP",
    "SDL",
]

ALL_ASU_MODELS = (SNEM, IACM, CSG, BARM, STANM, AACM, PWSM, DGTP, SDL)
"""Ordered tuple of all ASU model classes for registry auto-discovery."""
