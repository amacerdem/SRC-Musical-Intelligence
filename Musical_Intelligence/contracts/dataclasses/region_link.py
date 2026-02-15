"""RegionLink -- Declarative mapping from nucleus output dims to brain regions.

Each ``RegionLink`` declares that a specific output dimension of a nucleus
contributes to the activation of a specific brain region. The orchestrator
uses these declarations to build the Region Activation Map (RAM): a
``(B, T, 26)`` tensor of brain-region activations.

The ``weight`` field scales the contribution (0-1). The ``citation`` field
provides the neuroscientific evidence for the link.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RegionLink:
    """Maps one output dimension to one brain region.

    Attributes:
        dim_name:  Name of the output dimension (must match a name in
                   the nucleus's ``LAYERS`` dim_names).
        region:    Abbreviation from the global ``REGION_REGISTRY``
                   (e.g. ``"NAcc"``, ``"A1_HG"``, ``"IC"``).
        weight:    Contribution strength in ``[0, 1]``. How strongly this
                   dimension's value drives the region's activation.
        citation:  Evidence source (e.g. ``"Salimpoor 2011"``).
    """

    dim_name: str
    region: str
    weight: float
    citation: str

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if not self.dim_name:
            raise ValueError("RegionLink: dim_name must be non-empty")
        if not self.region:
            raise ValueError("RegionLink: region must be non-empty")
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(
                f"RegionLink {self.dim_name!r} → {self.region!r}: "
                f"weight must be in [0, 1], got {self.weight}"
            )
        if not self.citation:
            raise ValueError(
                f"RegionLink {self.dim_name!r} → {self.region!r}: "
                f"citation must be non-empty"
            )
