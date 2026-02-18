"""MMPKernelWrapper — causal-mode MMP adapter for C³ Kernel.

Wraps the production MMP Relay (IMU, 12D) for use inside the
kernel belief cycle.  Feeds familiarity_state belief in Wave 1.

Rules:
  1. Expose P-layer (3D) + F-layer (3D) = 6 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — 9 of 18 MMP demands survive (9 are L2)
  4. Return None on failure → belief falls back to R³+H³

Note: MMP has 9 L0 demands at long horizons (H20, H24) which
capture sustained memory/familiarity signals.  The 9 L2 demands
at H16 provide current-state context.  In causal mode, only the
long-horizon memory signals are available, which actually aligns
well with the familiarity concept (what has been heard before).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.imu.relays.mmp import MMP


@dataclass(frozen=True)
class MMPOutput:
    """Approved MMP outputs for kernel familiarity belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    recognition_state: Tensor     # Current recognition level
    melodic_identity: Tensor      # Current melodic match
    familiarity_level: Tensor     # Current familiarity
    # F-layer: forecasts
    recognition_forecast: Tensor  # Predicted recognition trajectory
    emotional_forecast: Tensor    # Predicted emotional response
    scaffold_forecast: Tensor     # Predicted structural integrity


class MMPKernelWrapper(RelayKernelWrapper):
    """Causal-mode MMP adapter for C³ Kernel.

    MMP models musical memory preservation with long-horizon H³
    demands.  In causal mode, 9 of 18 demands survive L0 filtering:
      - stumpf_fusion std H24
      - sensory_pleasantness mean H24
      - warmth mean H20, std H24
      - tonalness mean H20, std H24
      - tristimulus1 mean H24
      - distribution_entropy mean H24
      - loudness std H24

    Long-horizon L0 demands capture sustained patterns — ideal
    for familiarity detection.
    """

    def __init__(self) -> None:
        self._mmp = MMP()

        # Filter to L0-only (9 of 18 survive)
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._mmp.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "MMP"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from MMP (9 tuples, causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[MMPOutput]:
        """Run MMP and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            MMPOutput with 6 approved dimensions, or None.
        """
        mmp_12d = self._mmp.compute(h3, r3)  # (B, T, 12)

        return MMPOutput(
            recognition_state=mmp_12d[..., 3],
            melodic_identity=mmp_12d[..., 4],
            familiarity_level=mmp_12d[..., 5],
            recognition_forecast=mmp_12d[..., 6],
            emotional_forecast=mmp_12d[..., 7],
            scaffold_forecast=mmp_12d[..., 8],
        )
