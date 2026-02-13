"""CrossUnitPathway: cross-unit signal routing specification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CrossUnitPathway:
    pathway_id: str              # "P1_SPU_ARU"
    name: str                    # human-readable
    source_unit: str             # "SPU"
    source_model: str            # "BCH"
    source_dims: Tuple[str, ...] # dimension names provided
    target_unit: str             # "ARU"
    target_model: str            # "SRP"
    correlation: str             # "r=0.81"
    citation: str                # justifying paper

    @property
    def is_intra_unit(self) -> bool:
        return self.source_unit == self.target_unit

    @property
    def is_inter_unit(self) -> bool:
        return self.source_unit != self.target_unit

    @property
    def edge(self) -> Tuple[str, str]:
        return (self.source_unit, self.target_unit)
