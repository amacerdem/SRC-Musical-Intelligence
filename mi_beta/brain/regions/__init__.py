"""
Brain Region Atlas -- Unified registry of all anatomical regions.

RegionAtlas collects all BrainRegion instances from subcortical, cortical,
and brainstem submodules into a single queryable atlas.  Models declare
their associated regions via BrainRegion references; the atlas enables
lookup by abbreviation and category for visualisation and validation.

Usage:
    atlas = RegionAtlas()
    vta = atlas["VTA"]
    reward_regions = atlas.by_abbreviations("VTA", "NAcc", "caudate")
    cortical = atlas.cortical
"""

from __future__ import annotations

from typing import Dict, Optional, Sequence, Tuple

from mi_beta.contracts import BrainRegion

from .brainstem import ALL_BRAINSTEM
from .cortical import ALL_CORTICAL
from .subcortical import ALL_SUBCORTICAL

# Re-export individual regions for convenience
from .subcortical import (  # noqa: F401
    VTA,
    NACC,
    CAUDATE,
    AMYGDALA,
    HIPPOCAMPUS,
    PUTAMEN,
    THALAMUS_MGB,
    HYPOTHALAMUS,
    INSULA,
)
from .cortical import (  # noqa: F401
    A1_HG,
    STG,
    STS,
    IFG,
    DLPFC,
    VMPFC,
    OFC,
    ACC,
    SMA,
    PMC,
    ANGULAR_GYRUS,
    TEMPORAL_POLE,
)
from .brainstem import (  # noqa: F401
    IC,
    AN,
    CN,
    SOC,
    PAG,
)


class RegionAtlas:
    """Unified atlas of all brain regions used in the MI-Beta architecture.

    The atlas is built once at import time from the three anatomical
    submodules (subcortical, cortical, brainstem) and provides O(1)
    lookup by abbreviation.

    Attributes:
        subcortical: Tuple of all subcortical BrainRegion instances.
        cortical:    Tuple of all cortical BrainRegion instances.
        brainstem:   Tuple of all brainstem BrainRegion instances.
    """

    def __init__(self) -> None:
        self.subcortical: Tuple[BrainRegion, ...] = ALL_SUBCORTICAL
        self.cortical: Tuple[BrainRegion, ...] = ALL_CORTICAL
        self.brainstem: Tuple[BrainRegion, ...] = ALL_BRAINSTEM

        # Build abbreviation -> BrainRegion index
        self._index: Dict[str, BrainRegion] = {}
        for region in self.all:
            if region.abbreviation in self._index:
                raise ValueError(
                    f"Duplicate abbreviation {region.abbreviation!r} in atlas: "
                    f"{self._index[region.abbreviation].name!r} and "
                    f"{region.name!r}"
                )
            self._index[region.abbreviation] = region

    # ─── All regions ─────────────────────────────────────────────────

    @property
    def all(self) -> Tuple[BrainRegion, ...]:
        """All regions in canonical order: subcortical, cortical, brainstem."""
        return self.subcortical + self.cortical + self.brainstem

    # ─── Lookup ──────────────────────────────────────────────────────

    def __getitem__(self, abbreviation: str) -> BrainRegion:
        """Look up a region by its abbreviation.

        Args:
            abbreviation: Region abbreviation (e.g. "VTA", "A1/HG").

        Returns:
            The matching BrainRegion instance.

        Raises:
            KeyError: If the abbreviation is not in the atlas.
        """
        try:
            return self._index[abbreviation]
        except KeyError:
            available = ", ".join(sorted(self._index.keys()))
            raise KeyError(
                f"Unknown region abbreviation {abbreviation!r}. "
                f"Available: {available}"
            ) from None

    def get(self, abbreviation: str) -> Optional[BrainRegion]:
        """Look up a region by abbreviation, returning None if not found."""
        return self._index.get(abbreviation)

    def __contains__(self, abbreviation: str) -> bool:
        """Check if an abbreviation exists in the atlas."""
        return abbreviation in self._index

    def by_abbreviations(self, *abbreviations: str) -> Tuple[BrainRegion, ...]:
        """Look up multiple regions by abbreviation.

        Args:
            *abbreviations: One or more region abbreviation strings.

        Returns:
            Tuple of matching BrainRegion instances in the order requested.

        Raises:
            KeyError: If any abbreviation is not in the atlas.
        """
        return tuple(self[abbr] for abbr in abbreviations)

    def by_function_keyword(self, keyword: str) -> Tuple[BrainRegion, ...]:
        """Find regions whose function description contains the keyword.

        Args:
            keyword: Case-insensitive substring to search for in each
                     region's function field.

        Returns:
            Tuple of matching regions (may be empty).
        """
        kw = keyword.lower()
        return tuple(r for r in self.all if kw in r.function.lower())

    # ─── Properties ──────────────────────────────────────────────────

    @property
    def abbreviations(self) -> Tuple[str, ...]:
        """All region abbreviations in canonical order."""
        return tuple(r.abbreviation for r in self.all)

    @property
    def total_evidence(self) -> int:
        """Sum of evidence_count across all regions."""
        return sum(r.evidence_count for r in self.all)

    def __len__(self) -> int:
        return len(self._index)

    def __repr__(self) -> str:
        return (
            f"RegionAtlas("
            f"{len(self.subcortical)} subcortical, "
            f"{len(self.cortical)} cortical, "
            f"{len(self.brainstem)} brainstem; "
            f"{len(self)} total)"
        )


# =====================================================================
# MODULE-LEVEL SINGLETON
# =====================================================================

ATLAS = RegionAtlas()
"""Module-level singleton atlas instance.  Import and use directly:

    from mi_beta.brain.regions import ATLAS
    vta = ATLAS["VTA"]
"""

__all__ = [
    "RegionAtlas",
    "ATLAS",
    # Subcortical
    "VTA",
    "NACC",
    "CAUDATE",
    "AMYGDALA",
    "HIPPOCAMPUS",
    "PUTAMEN",
    "THALAMUS_MGB",
    "HYPOTHALAMUS",
    "INSULA",
    # Cortical
    "A1_HG",
    "STG",
    "STS",
    "IFG",
    "DLPFC",
    "VMPFC",
    "OFC",
    "ACC",
    "SMA",
    "PMC",
    "ANGULAR_GYRUS",
    "TEMPORAL_POLE",
    # Brainstem
    "IC",
    "AN",
    "CN",
    "SOC",
    "PAG",
    # Aggregate tuples
    "ALL_SUBCORTICAL",
    "ALL_CORTICAL",
    "ALL_BRAINSTEM",
]
