"""BaseCognitiveUnit: ABC for the 9 cognitive units."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from torch import Tensor


class BaseCognitiveUnit(ABC):
    UNIT_NAME: str = ""                         # "SPU", "ARU", etc.
    FULL_NAME: str = ""
    CIRCUIT: str = ""                           # "perceptual", "mesolimbic", etc.
    POOLED_EFFECT: float = 0.0                  # Cohen's d from meta-analysis

    @property
    @abstractmethod
    def models(self) -> list:
        ...

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:                                # (B, T, total_dim)
        ...

    @property
    def active_models(self) -> list:
        return self.models

    @property
    def total_dim(self) -> int:
        return sum(m.OUTPUT_DIM for m in self.active_models)

    @property
    def model_names(self) -> Tuple[str, ...]:
        return tuple(m.NAME for m in self.active_models)

    @property
    def mechanism_names(self) -> Tuple[str, ...]:
        names: set = set()
        for m in self.active_models:
            names.update(m.MECHANISM_NAMES)
        return tuple(sorted(names))

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        demands: Set[Tuple[int, int, int, int]] = set()
        for m in self.active_models:
            demands.update(m.h3_demand_tuples())
        return demands

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        names: List[str] = []
        for m in self.active_models:
            names.extend(m.dimension_names)
        return tuple(names)

    @property
    def is_validated(self) -> bool:
        return self.POOLED_EFFECT > 0

    @property
    def model_ranges(self) -> Dict[str, Tuple[int, int]]:
        ranges: Dict[str, Tuple[int, int]] = {}
        offset = 0
        for m in self.active_models:
            ranges[m.NAME] = (offset, offset + m.OUTPUT_DIM)
            offset += m.OUTPUT_DIM
        return ranges

    def validate(self) -> List[str]:
        errors = []
        if not self.UNIT_NAME:
            errors.append("Unit has empty UNIT_NAME")
        for m in self.active_models:
            errors.extend(m.validate_constants())
        return errors
