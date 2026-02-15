"""Shared Region dataclass for per-file cortical/subcortical/brainstem modules."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Region:
    """A brain region in the global registry.

    Attributes:
        index:         Fixed position in the RAM tensor (0-25).
        name:          Full anatomical name.
        abbreviation:  Short label used in RegionLinks.
        hemisphere:    ``"L"``, ``"R"``, or ``"bilateral"``.
        mni_coords:    ``(x, y, z)`` centroid in MNI152 space (mm).
        brodmann_area: BA number if cortical, ``None`` otherwise.
        group:         ``"cortical"``, ``"subcortical"``, or ``"brainstem"``.
    """

    index: int
    name: str
    abbreviation: str
    hemisphere: str
    mni_coords: Tuple[int, int, int]
    brodmann_area: Optional[int]
    group: str
