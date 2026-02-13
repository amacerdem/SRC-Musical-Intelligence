"""BaseSemanticGroup: ABC for L3 semantic interpretation groups."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from ..core.types import SemanticGroupOutput


class BaseSemanticGroup(ABC):
    LEVEL: int = 0                   # 1-8 epistemological level
    GROUP_NAME: str = ""             # "alpha", "beta", ..., "theta"
    DISPLAY_NAME: str = ""           # "a", "b", ..., "th"
    OUTPUT_DIM: int = 0

    @abstractmethod
    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        ...

    @property
    @abstractmethod
    def dimension_names(self) -> List[str]:
        ...

    def validate(self) -> List[str]:
        errors = []
        if len(self.dimension_names) != self.OUTPUT_DIM:
            errors.append(
                f"{self.GROUP_NAME}: dimension_names length "
                f"{len(self.dimension_names)} != OUTPUT_DIM {self.OUTPUT_DIM}"
            )
        return errors
