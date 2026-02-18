"""HMCEKernelWrapper — causal-mode HMCE adapter for C³ Kernel.

Wraps the production HMCE Relay (STU, 13D) for use inside the
kernel belief cycle.  Feeds tempo_state belief in Wave 1.

Rules:
  1. Expose P-layer (3D) + F-layer (3D) = 6 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — all 18 HMCE demands are already L0
  4. Return None on failure → belief falls back to R³+H³
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.stu.relays.hmce import HMCE


@dataclass(frozen=True)
class HMCEOutput:
    """Approved HMCE outputs for kernel tempo belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: regional encoding
    a1_encoding: Tensor          # Primary auditory cortex activity
    stg_encoding: Tensor         # Superior temporal gyrus activity
    mtg_encoding: Tensor         # Middle temporal gyrus activity
    # F-layer: temporal predictions
    context_prediction: Tensor   # Next context state prediction
    phrase_expect: Tensor        # Phrase boundary expectation
    structure_predict: Tensor    # Large-scale structural prediction


class HMCEKernelWrapper(RelayKernelWrapper):
    """Causal-mode HMCE adapter for C³ Kernel.

    HMCE models the hierarchical temporal receptive window (TRW)
    organization of auditory cortex: A1 (short) → STG (medium)
    → MTG (long).  All 18 H³ demands are L0 (memory), so all
    survive causal filtering.
    """

    # Output indices
    _P_START, _P_END = 7, 10      # a1_encoding, stg_encoding, mtg_encoding
    _F_START, _F_END = 10, 13     # context_prediction, phrase_expect, structure_predict

    def __init__(self) -> None:
        self._hmce = HMCE()

        # All 18 demands are L0 — all survive causal filter
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._hmce.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "HMCE"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from HMCE (18 tuples, all causal)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[HMCEOutput]:
        """Run HMCE and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            HMCEOutput with 6 approved dimensions, or None.
        """
        hmce_13d = self._hmce.compute(h3, r3)  # (B, T, 13)

        return HMCEOutput(
            a1_encoding=hmce_13d[..., 7],
            stg_encoding=hmce_13d[..., 8],
            mtg_encoding=hmce_13d[..., 9],
            context_prediction=hmce_13d[..., 10],
            phrase_expect=hmce_13d[..., 11],
            structure_predict=hmce_13d[..., 12],
        )
