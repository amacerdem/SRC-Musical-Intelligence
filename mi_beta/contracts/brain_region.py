"""
BrainRegion -- Anatomical brain region with MNI coordinates.

Every cognitive model and mechanism is grounded in specific brain regions.
This dataclass captures the neuroanatomical identity of each region so that
models can declare their biological substrate and visualisation tools can
render activations in MNI152 standard space.

MNI coordinates follow the Montreal Neurological Institute convention:
    x: left (-) / right (+)
    y: posterior (-) / anterior (+)
    z: inferior (-) / superior (+)

Brodmann areas are optional because subcortical structures (NAcc, VTA,
amygdala, hippocampus) do not have Brodmann designations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class BrainRegion:
    """A specific brain region with anatomical metadata.

    Attributes:
        name:           Full anatomical name (e.g. "Nucleus Accumbens").
        abbreviation:   Short label (e.g. "NAcc").
        hemisphere:     "L", "R", or "bilateral".
        mni_coords:     (x, y, z) centroid in MNI152 space (mm).
        brodmann_area:  Brodmann area number, if applicable (cortical only).
        function:       Brief functional description.
        evidence_count: Number of studies in the C3 database citing this region
                        for the associated cognitive unit.
    """

    name: str
    abbreviation: str
    hemisphere: str
    mni_coords: Tuple[int, int, int]
    brodmann_area: Optional[int] = None
    function: str = ""
    evidence_count: int = 0

    def __post_init__(self) -> None:
        valid_hemispheres = ("L", "R", "bilateral")
        if self.hemisphere not in valid_hemispheres:
            raise ValueError(
                f"BrainRegion {self.abbreviation!r}: hemisphere must be one of "
                f"{valid_hemispheres}, got {self.hemisphere!r}"
            )
        if len(self.mni_coords) != 3:
            raise ValueError(
                f"BrainRegion {self.abbreviation!r}: mni_coords must be a "
                f"3-tuple (x, y, z), got length {len(self.mni_coords)}"
            )

    @property
    def is_cortical(self) -> bool:
        """True if the region has a Brodmann area designation."""
        return self.brodmann_area is not None

    @property
    def is_subcortical(self) -> bool:
        """True if the region lacks a Brodmann area (subcortical structure)."""
        return self.brodmann_area is None

    def __repr__(self) -> str:
        ba = f", BA{self.brodmann_area}" if self.brodmann_area else ""
        return (
            f"BrainRegion({self.abbreviation} "
            f"[{self.hemisphere}]{ba}, "
            f"MNI=({self.mni_coords[0]}, {self.mni_coords[1]}, {self.mni_coords[2]}))"
        )
