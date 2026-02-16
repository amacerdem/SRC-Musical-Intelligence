"""BCHKernelWrapper — causal-mode BCH adapter for C³ Kernel.

Wraps the production BCH Relay for use inside the kernel belief cycle.

Rules (from architecture review):
  1. Only expose 3 of 16D: hierarchy(E[2]), consonance_signal(P[8]),
     template_match(P[9])
  2. H³ demand deduplication against existing kernel demands
  3. Consonance observe() uses:
     0.5×consonance_signal + 0.3×template_match + 0.2×hierarchy
  4. precision_obs updated with BCH output variability
  5. L0 (memory) only — disable L1/L2 for causal online mode
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ...units.spu.relays.bch import BCH


@dataclass(frozen=True)
class BCHOutput:
    """Three approved BCH outputs for kernel consonance.

    All tensors are (B, T) shaped.
    """
    hierarchy: Tensor          # E-layer idx 2 — consonance ranking
    consonance_signal: Tensor  # P-layer idx 8 — current consonance in context
    template_match: Tensor     # P-layer idx 9 — harmonic template match


class BCHKernelWrapper:
    """Causal-mode BCH adapter for C³ Kernel.

    Instantiates the production BCH relay and:
      - Filters H³ demands to L0 (memory law) only for causal operation
      - Runs BCH.compute() and extracts the 3 approved outputs
      - Provides deduplication-aware demand collection
    """

    # BCH output indices for approved dimensions
    _IDX_HIERARCHY = 2          # E-layer: hierarchy
    _IDX_CONSONANCE_SIGNAL = 8  # P-layer: consonance_signal
    _IDX_TEMPLATE_MATCH = 9     # P-layer: template_match

    def __init__(self) -> None:
        self._bch = BCH()

        # Pre-compute L0-only demand set (Rule 5: causal mode)
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._bch.h3_demand:
            if spec.law == 0:  # L0 = memory (causal)
                self._l0_demands.add(spec.as_tuple())

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from BCH (17 tuples, causal mode)."""
        return self._l0_demands

    def h3_demands_deduped(
        self,
        existing: Set[Tuple[int, int, int, int]],
    ) -> Set[Tuple[int, int, int, int]]:
        """Return BCH L0 demands not already in existing set (Rule 2)."""
        return self._l0_demands - existing

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> BCHOutput:
        """Run BCH and extract approved outputs.

        Args:
            r3: (B, T, 128) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            BCHOutput with hierarchy, consonance_signal, template_match.
        """
        bch_16d = self._bch.compute(h3, r3)  # (B, T, 16)

        return BCHOutput(
            hierarchy=bch_16d[..., self._IDX_HIERARCHY],
            consonance_signal=bch_16d[..., self._IDX_CONSONANCE_SIGNAL],
            template_match=bch_16d[..., self._IDX_TEMPLATE_MATCH],
        )
