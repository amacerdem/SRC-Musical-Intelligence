"""BaseMechanism: ABC for shared brain mechanisms."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Set, Tuple

from torch import Tensor

from ..core.constants import MECHANISM_DIM


class BaseMechanism(ABC):
    NAME: str = ""                              # "AED", "PPC", etc.
    FULL_NAME: str = ""
    OUTPUT_DIM: int = MECHANISM_DIM             # standard 30
    HORIZONS: Tuple[int, ...] = ()              # which horizons this mechanism uses

    @property
    @abstractmethod
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        ...

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:                                # (B, T, OUTPUT_DIM)
        ...

    @property
    def demand_count(self) -> int:
        return len(self.h3_demand)

    @property
    def horizons_used(self) -> Set[int]:
        return {t[1] for t in self.h3_demand}

    @property
    def r3_indices_used(self) -> Set[int]:
        return {t[0] for t in self.h3_demand}

    def validate(self) -> List[str]:
        errors = []
        if not self.NAME:
            errors.append("Mechanism has empty NAME")
        return errors
