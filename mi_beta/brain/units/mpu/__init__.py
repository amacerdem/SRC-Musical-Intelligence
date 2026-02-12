"""
MPU -- Motor Planning Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.mpu import MPUUnit
    from mi_beta.brain.units.mpu import PEOM, MSR, GSSM  # individual models
"""

from ._unit import MPUUnit
from .models import (
    ALL_MPU_MODELS,
    ASAP,
    CTBB,
    DDSMI,
    GSSM,
    MSR,
    NSCP,
    PEOM,
    SPMC,
    STC,
    VRMSME,
)

__all__ = [
    "MPUUnit",
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
    # Registry
    "ALL_MPU_MODELS",
]
