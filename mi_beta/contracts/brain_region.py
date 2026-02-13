"""BrainRegion: anatomical region specification in MNI152 space."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class BrainRegion:
    name: str                    # "Nucleus Accumbens"
    abbreviation: str            # "NAcc"
    hemisphere: str              # "L", "R", "bilateral"
    mni_coords: Tuple[int, int, int]  # (x, y, z) MNI152 space
    brodmann_area: Optional[int] = None
    function: str = ""
    evidence_count: int = 0

    @property
    def is_cortical(self) -> bool:
        _, _, z = self.mni_coords
        return z > 0

    @property
    def is_subcortical(self) -> bool:
        return not self.is_cortical
