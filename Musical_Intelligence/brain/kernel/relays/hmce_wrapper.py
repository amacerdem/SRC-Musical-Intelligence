"""HMCEKernelWrapper — causal-mode HMCE adapter for C³ Kernel.

Wraps the production HMCE Relay (STU, 13D) for use inside the
kernel belief cycle.  Feeds tempo_state belief in Wave 1.

v3.0 Wave 2: Cross-relay pathway P3 (SNEM → HMCE).
  When SNEM beat_locked_activity is available, A1 encoding is
  amplified — beat entrainment strengthens onset-level cortical
  response.  Modulation: a1 *= (1 + 0.3 × beat_locked_activity).

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

    # P3 cross-relay: SNEM beat_locked_activity → A1 encoding gain
    _SNEM_A1_GAIN = 0.3  # 30% max amplification from beat entrainment

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
        *,
        snem_beat: Optional[Tensor] = None,
    ) -> Optional[HMCEOutput]:
        """Run HMCE and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.
            snem_beat: (B, T) SNEM beat_locked_activity for P3 pathway.
                When available, amplifies A1 encoding — beat entrainment
                strengthens short-scale cortical response.

        Returns:
            HMCEOutput with 6 approved dimensions, or None.
        """
        hmce_13d = self._hmce.compute(h3, r3)  # (B, T, 13)

        a1 = hmce_13d[..., 7]

        # P3 cross-relay: beat entrainment → A1 gain
        if snem_beat is not None:
            a1 = a1 * (1.0 + self._SNEM_A1_GAIN * snem_beat.clamp(0.0, 1.0))

        return HMCEOutput(
            a1_encoding=a1,
            stg_encoding=hmce_13d[..., 8],
            mtg_encoding=hmce_13d[..., 9],
            context_prediction=hmce_13d[..., 10],
            phrase_expect=hmce_13d[..., 11],
            structure_predict=hmce_13d[..., 12],
        )
