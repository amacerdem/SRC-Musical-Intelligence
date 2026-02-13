"""BaseSpectralGroup: ABC for R3 spectral feature groups."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from torch import Tensor


class BaseSpectralGroup(ABC):
    GROUP_NAME: str = ""                        # "consonance"
    DOMAIN: str = ""                            # "psychoacoustic"
    OUTPUT_DIM: int = 0                         # 7
    INDEX_RANGE: Tuple[int, int] = (0, 0)       # assigned by registry.freeze()

    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor:
        """(B, N_MELS, T) → (B, T, OUTPUT_DIM)"""

    @property
    @abstractmethod
    def feature_names(self) -> List[str]:
        """len == OUTPUT_DIM"""

    @property
    def start_index(self) -> int:
        return self.INDEX_RANGE[0]

    @property
    def end_index(self) -> int:
        return self.INDEX_RANGE[1]

    def validate(self) -> List[str]:
        errors = []
        if len(self.feature_names) != self.OUTPUT_DIM:
            errors.append(
                f"{self.GROUP_NAME}: feature_names length {len(self.feature_names)} "
                f"!= OUTPUT_DIM {self.OUTPUT_DIM}"
            )
        return errors
