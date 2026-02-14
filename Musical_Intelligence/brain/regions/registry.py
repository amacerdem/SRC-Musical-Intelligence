"""BrainRegionRegistry -- lookup by name, abbreviation, and MNI proximity."""
from __future__ import annotations

import math
from typing import Dict, List, Optional, Tuple

from ...contracts.dataclasses import BrainRegion
from .cortical import CORTICAL_REGIONS
from .subcortical import SUBCORTICAL_REGIONS
from .brainstem import BRAINSTEM_REGIONS


class BrainRegionRegistry:
    """Lookup brain regions by name, abbreviation, or MNI proximity.

    Indexes all cortical, subcortical, and brainstem regions on construction.
    """

    def __init__(self) -> None:
        all_regions = CORTICAL_REGIONS + SUBCORTICAL_REGIONS + BRAINSTEM_REGIONS
        self._by_name: Dict[str, BrainRegion] = {r.name: r for r in all_regions}
        self._by_abbr: Dict[str, BrainRegion] = {
            r.abbreviation: r for r in all_regions
        }
        self._all: Tuple[BrainRegion, ...] = all_regions

    # ── Lookups ──────────────────────────────────────────────────────

    def get_by_name(self, name: str) -> Optional[BrainRegion]:
        """Return the region with the given full name, or ``None``."""
        return self._by_name.get(name)

    def get_by_abbreviation(self, abbr: str) -> Optional[BrainRegion]:
        """Return the region with the given abbreviation, or ``None``."""
        return self._by_abbr.get(abbr)

    def get_nearest_mni(
        self, x: int, y: int, z: int, k: int = 1
    ) -> List[BrainRegion]:
        """Find the *k* nearest regions to the given MNI coordinates."""

        def _dist(r: BrainRegion) -> float:
            rx, ry, rz = r.mni_coords
            return math.sqrt((x - rx) ** 2 + (y - ry) ** 2 + (z - rz) ** 2)

        return sorted(self._all, key=_dist)[:k]

    # ── Properties ───────────────────────────────────────────────────

    @property
    def all_regions(self) -> Tuple[BrainRegion, ...]:
        """All registered brain regions."""
        return self._all

    # ── Dunder ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"BrainRegionRegistry(regions={len(self._all)})"
