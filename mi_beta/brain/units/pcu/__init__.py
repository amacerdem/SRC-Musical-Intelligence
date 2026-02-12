"""
PCU -- Predictive Coding Unit.

Re-exports the unit definition and all model classes for convenient access:

    from mi_beta.brain.units.pcu import PCUUnit
    from mi_beta.brain.units.pcu import HTP, SPH, ICEM  # individual models
"""

from ._unit import PCUUnit
from .models import (
    ALL_PCU_MODELS,
    HTP,
    ICEM,
    IGFE,
    MAA,
    PSH,
    PWUP,
    SPH,
    UDP,
    WMED,
)

__all__ = [
    "PCUUnit",
    # Alpha
    "HTP",
    "SPH",
    "ICEM",
    # Beta
    "PWUP",
    "WMED",
    "UDP",
    # Gamma
    "IGFE",
    "MAA",
    "PSH",
    # Registry
    "ALL_PCU_MODELS",
]
