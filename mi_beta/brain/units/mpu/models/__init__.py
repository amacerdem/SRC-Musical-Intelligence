"""
MPU (Motor Planning Unit) -- All cognitive models.

10 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        PEOM  -- Predictive Error Optimization Model     (12D)
        MSR   -- Motor Sequence Representation           (11D)
        GSSM  -- Groove-State Sensorimotor Model         (11D)

    Beta (correlational, 5 <= k < 10):
        ASAP  -- Anticipatory Sequence Action Planning   (10D)
        DDSMI -- Dynamic Dual-Stream Motor Integration   (10D)
        VRMSME-- VR Motor Skill Music Enhancement        (10D)
        SPMC  -- Sensory-Predictive Motor Coupling       (10D)

    Gamma (exploratory, k < 5):
        NSCP  -- Neural Substrate Choreographic Planning (10D)
        CTBB  -- Cerebello-Thalamic Beat Binding         (10D)
        STC   -- Sensorimotor Timing Calibration         (10D)

Total MPU output: 104D per frame.
"""

from .asap import ASAP
from .ctbb import CTBB
from .ddsmi import DDSMI
from .gssm import GSSM
from .msr import MSR
from .nscp import NSCP
from .peom import PEOM
from .spmc import SPMC
from .stc import STC
from .vrmsme import VRMSME

__all__ = [
    # Alpha
    "PEOM",
    "MSR",
    "GSSM",
    # Beta
    "ASAP",
    "DDSMI",
    "VRMSME",
    "SPMC",
    # Gamma
    "NSCP",
    "CTBB",
    "STC",
]

ALL_MPU_MODELS = (PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC)
"""Ordered tuple of all MPU model classes for registry auto-discovery."""
