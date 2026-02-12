"""
BaseSpectralGroup — Abstract base for R³ spectral feature groups.

Each group computes a subset of the 49D R³ feature vector from mel spectrogram.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Tuple

from torch import Tensor


class BaseSpectralGroup(ABC):
    """Base class for R³ spectral feature groups (A-E)."""

    # ─── Class attributes (override in subclass) ────────────────────
    GROUP_NAME: str          # e.g., "consonance"
    OUTPUT_DIM: int          # e.g., 7
    INDEX_RANGE: Tuple[int, int]  # e.g., (0, 7) — position in R³ vector

    @abstractmethod
    def compute(self, mel: Tensor) -> Tensor:
        """Compute spectral features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, OUTPUT_DIM) spectral features
        """

    @property
    @abstractmethod
    def feature_names(self) -> List[str]:
        """Names of each output dimension."""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"group={self.GROUP_NAME!r}, "
            f"dim={self.OUTPUT_DIM}, "
            f"range={self.INDEX_RANGE})"
        )
