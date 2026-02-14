"""Brain regions sub-package -- cortical, subcortical, brainstem regions and registry."""
from __future__ import annotations

from .brainstem import BRAINSTEM_REGIONS
from .cortical import CORTICAL_REGIONS
from .registry import BrainRegionRegistry
from .subcortical import SUBCORTICAL_REGIONS

__all__ = [
    "BRAINSTEM_REGIONS",
    "BrainRegionRegistry",
    "CORTICAL_REGIONS",
    "SUBCORTICAL_REGIONS",
]
