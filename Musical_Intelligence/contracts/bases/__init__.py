"""Abstract base classes for the MI contracts layer.

Re-exports ABC types used as interface contracts throughout Musical Intelligence.
"""
from __future__ import annotations

from .base_model import BaseModel
from .base_semantic_group import BaseSemanticGroup
from .base_spectral_group import BaseSpectralGroup
from .base_unit import BaseCognitiveUnit
from .belief import AnticipationBelief, AppraisalBelief, Belief, CoreBelief
from .nucleus import Associator, Encoder, Hub, Integrator, Nucleus, Relay

__all__ = [
    # Legacy
    "BaseCognitiveUnit",
    "BaseModel",
    "BaseSemanticGroup",
    "BaseSpectralGroup",
    # Nucleus hierarchy
    "Associator",
    "Encoder",
    "Hub",
    "Integrator",
    "Nucleus",
    "Relay",
    # Belief hierarchy
    "AnticipationBelief",
    "AppraisalBelief",
    "Belief",
    "CoreBelief",
]
