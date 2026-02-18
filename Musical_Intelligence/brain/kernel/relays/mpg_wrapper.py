"""MPGKernelWrapper — causal-mode MPG adapter for C³ Kernel.

Wraps the production MPG Relay (NDU, 10D) for use inside the
kernel belief cycle.  Feeds salience_state belief in Wave 1
(contributes novelty/onset information alongside SNEM).

Rules:
  1. Expose P-layer (2D) + F-layer (1D) = 3 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — 2 of 16 MPG demands survive (14 are L2)
  4. Return None on failure → belief falls back to R³+H³

Note: MPG uses primarily L2 (integration) demands.  In causal
mode, only 2 L0 demands survive:
  - (13, 4, 8, 0) sharpness velocity at H4 — pitch contour
  - (60, 3, 8, 0) tonal_stability velocity at H3 — harmonic contour

The relay operates heavily degraded but still provides R³-based
onset/contour features through internal fallbacks.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.ndu.relays.mpg import MPG


@dataclass(frozen=True)
class MPGOutput:
    """Approved MPG outputs for kernel salience belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    onset_state: Tensor             # Current onset-locked activity
    contour_state: Tensor           # Current contour tracking
    # F-layer: prediction
    phrase_boundary_pred: Tensor    # Phrase boundary prediction


class MPGKernelWrapper(RelayKernelWrapper):
    """Causal-mode MPG adapter for C³ Kernel.

    MPG models the posterior-to-anterior melodic processing gradient
    in auditory cortex.  In causal mode, only 2 of 16 demands
    survive L0 filtering — the relay operates with heavy R³ fallback.
    """

    def __init__(self) -> None:
        self._mpg = MPG()

        # Filter to L0-only (2 of 16 survive)
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._mpg.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "MPG"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from MPG (2 tuples, causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[MPGOutput]:
        """Run MPG and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            MPGOutput with 3 approved dimensions, or None.
        """
        mpg_10d = self._mpg.compute(h3, r3)  # (B, T, 10)

        return MPGOutput(
            onset_state=mpg_10d[..., 7],
            contour_state=mpg_10d[..., 8],
            phrase_boundary_pred=mpg_10d[..., 9],
        )
