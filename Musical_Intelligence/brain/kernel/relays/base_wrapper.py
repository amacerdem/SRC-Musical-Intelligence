"""RelayKernelWrapper — abstract base for causal-mode relay adapters.

All relay wrappers follow the BCH pattern:
  1. Instantiate the production Relay nucleus
  2. Filter H³ demands to L0 (memory) only for causal online mode
  3. Expose typed compute() output with approved dimensions
  4. Return None on failure → belief falls back to R³+H³ observation

Wave 0 scaffolding — wrappers are instantiated and computed in the
scheduler but their outputs are NOT yet consumed by beliefs.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Set, Tuple

from torch import Tensor


class RelayKernelWrapper(ABC):
    """Abstract base class for relay kernel wrappers.

    Subclasses must implement:
      - h3_demands: L0-only H³ demand set
      - compute(): run relay, extract approved outputs
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Short relay name (e.g. 'HMCE', 'SNEM')."""
        ...

    @property
    @abstractmethod
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from this relay."""
        ...

    def h3_demands_deduped(
        self,
        existing: Set[Tuple[int, int, int, int]],
    ) -> Set[Tuple[int, int, int, int]]:
        """Return L0 demands not already in the existing set."""
        return self.h3_demands - existing

    @abstractmethod
    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[Any]:
        """Run the relay and return typed output.

        Returns None if relay fails or required data is missing.
        Callers (beliefs) fall back to R³+H³ when None is returned.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.
        """
        ...
