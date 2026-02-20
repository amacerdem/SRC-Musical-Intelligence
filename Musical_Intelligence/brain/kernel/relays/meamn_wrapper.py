"""MEAMNKernelWrapper — causal-mode MEAMN adapter for C³ Kernel.

Wraps the production MEAMN Relay (IMU, 12D) for use inside the
kernel belief cycle.  Feeds familiarity_state belief in Wave 1.
Replaces the former MMP wrapper.

Rules:
  1. Expose P-layer (3D) + F-layer (3D usable) = 6 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — causal mode
  4. Return None on failure → belief falls back to R³+H³

Note: MEAMN has 8 L0 demands at long horizons (H20, H24) which
capture sustained memory and retrieval signals.  The 11 L2 demands
at H16 provide current-state context.  In causal mode, the long-
horizon memory signals drive familiarity detection and nostalgia.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.imu.relays.meamn import MEAMN


@dataclass(frozen=True)
class MEAMNOutput:
    """Approved MEAMN outputs for kernel familiarity belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    memory_state: Tensor          # Current retrieval activation
    emotional_color: Tensor       # Current affective tag
    nostalgia_link: Tensor        # Nostalgia-familiarity warmth
    # F-layer: forecasts
    mem_vividness_pred: Tensor    # Memory vividness 2-5s ahead
    emo_response_pred: Tensor     # Emotional response 1-3s ahead
    self_referential_pred: Tensor # Self-referential 5-10s ahead


class MEAMNKernelWrapper(RelayKernelWrapper):
    """Causal-mode MEAMN adapter for C³ Kernel.

    MEAMN models music-evoked autobiographical memory with long-horizon
    H³ demands.  In causal mode, 8 of 19 demands survive L0 filtering:
      - stumpf_fusion mean H24
      - sensory_pleasantness trend H20
      - loudness mean H20, std H24
      - warmth mean H20
      - tonalness mean H20
      - distribution_entropy mean H20, stability H24
      - roughness trend H20
      - amplitude velocity H16, max H20

    Long-horizon L0 demands capture sustained patterns — ideal for
    familiarity and nostalgia detection.
    """

    def __init__(self) -> None:
        self._meamn = MEAMN()

        # Filter to L0-only
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._meamn.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "MEAMN"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from MEAMN (causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[MEAMNOutput]:
        """Run MEAMN and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            MEAMNOutput with 6 approved dimensions, or None.
        """
        meamn_12d = self._meamn.compute(h3, r3)  # (B, T, 12)

        return MEAMNOutput(
            memory_state=meamn_12d[..., 5],
            emotional_color=meamn_12d[..., 6],
            nostalgia_link=meamn_12d[..., 7],
            mem_vividness_pred=meamn_12d[..., 8],
            emo_response_pred=meamn_12d[..., 9],
            self_referential_pred=meamn_12d[..., 10],
        )
