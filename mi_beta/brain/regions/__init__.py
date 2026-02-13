"""Brain region atlas: 26 regions in MNI152 space."""
from __future__ import annotations
from typing import Tuple
from ...contracts.brain_region import BrainRegion
from .subcortical import SUBCORTICAL_REGIONS
from .cortical import CORTICAL_REGIONS
from .brainstem import BRAINSTEM_REGIONS

class RegionAtlas:
    def __init__(self):
        self.subcortical = SUBCORTICAL_REGIONS
        self.cortical = CORTICAL_REGIONS
        self.brainstem = BRAINSTEM_REGIONS
    @property
    def all(self) -> Tuple[BrainRegion, ...]:
        return self.subcortical + self.cortical + self.brainstem

ATLAS = RegionAtlas()
