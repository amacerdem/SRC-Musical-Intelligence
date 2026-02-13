"""BrainRegion -- Neuroanatomical identity with MNI152 coordinates.

Every cognitive model and mechanism is grounded in specific brain regions.
``BrainRegion`` captures the neuroanatomical identity so that models can
declare their biological substrate and visualisation tools can render
activations in MNI152 standard space.

MNI152 coordinate convention:

    x: Left(-) / Right(+)
    y: Posterior(-) / Anterior(+)
    z: Inferior(-) / Superior(+)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


_VALID_HEMISPHERES = frozenset({"L", "R", "bilateral"})


@dataclass(frozen=True)
class BrainRegion:
    """A brain region with MNI152 coordinates and optional Brodmann area.

    Attributes:
        name:           Full anatomical name (e.g.
                        ``"Nucleus Accumbens"``).
        abbreviation:   Short label (e.g. ``"NAcc"``).
        hemisphere:     ``"L"``, ``"R"``, or ``"bilateral"``.
        mni_coords:     ``(x, y, z)`` centroid in MNI152 space (mm).
        brodmann_area:  Brodmann area number if applicable (cortical
                        regions only). ``None`` for subcortical /
                        brainstem structures.
        function:       Brief functional description.
        evidence_count: Number of studies in the C3 database citing
                        this region.
    """

    name: str
    abbreviation: str
    hemisphere: str
    mni_coords: tuple[int, int, int]
    brodmann_area: Optional[int] = None
    function: str = ""
    evidence_count: int = 0

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if self.hemisphere not in _VALID_HEMISPHERES:
            raise ValueError(
                f"BrainRegion {self.name!r}: hemisphere must be one of "
                f"{sorted(_VALID_HEMISPHERES)}, got {self.hemisphere!r}"
            )
        if len(self.mni_coords) != 3:
            raise ValueError(
                f"BrainRegion {self.name!r}: mni_coords must be a 3-tuple "
                f"(x, y, z), got length {len(self.mni_coords)}"
            )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def is_cortical(self) -> bool:
        """``True`` if the region has a Brodmann area designation."""
        return self.brodmann_area is not None

    @property
    def is_subcortical(self) -> bool:
        """``True`` if the region lacks a Brodmann area (subcortical structure)."""
        return self.brodmann_area is None
