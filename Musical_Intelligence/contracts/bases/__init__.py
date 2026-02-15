"""Abstract base classes for the MI contracts layer.

Re-exports all 4 ABC types used as interface contracts throughout
Musical Intelligence.
"""
from __future__ import annotations

from .base_model import BaseModel
from .base_semantic_group import BaseSemanticGroup
from .base_spectral_group import BaseSpectralGroup
from .base_unit import BaseCognitiveUnit

__all__ = [
    "BaseCognitiveUnit",
    "BaseModel",
    "BaseSemanticGroup",
    "BaseSpectralGroup",
]
