"""SRPKernelWrapper — causal-mode SRP adapter for C³ Kernel.

Wraps the production SRP Relay (ARU, 14D) for use inside the
kernel belief cycle.  Provides wanting/liking/pleasure signals
for reward modulation.

Rules:
  1. Expose P-layer (3D) + F-layer (4D) = 7 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — causal mode
  4. Return None on failure → belief falls back to R³+H³

Note: SRP has 4 L0 demands:
  - roughness trend H20 (resolution direction)
  - sensory_pleasantness mean H20 (sustained pleasure)
  - amplitude velocity H20 (energy buildup)
  - beat_strength trend H20 (wanting ramp)
The remaining 14 L2 demands provide current-state context.
In causal mode, the phrase-level memory signals capture
anticipatory DA ramp and sustained pleasure.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.aru.relays.srp import SRP


@dataclass(frozen=True)
class SRPOutput:
    """Approved SRP outputs for kernel reward belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: psychological states
    wanting: Tensor               # Berridge incentive salience
    liking: Tensor                # Berridge hedonic impact
    pleasure: Tensor              # Composite subjective pleasure
    # F-layer: forecasts
    tension: Tensor               # Huron T preparatory arousal
    reward_forecast: Tensor       # Expected reward 2-8s ahead
    chills_proximity: Tensor      # Proximity to chills event
    resolution_expect: Tensor     # Expected harmonic resolution


class SRPKernelWrapper(RelayKernelWrapper):
    """Causal-mode SRP adapter for C³ Kernel.

    SRP models the striatal reward pathway — DA-mediated wanting
    (caudate) and liking (NAcc).  In causal mode, 4 of 18 demands
    survive L0 filtering:
      - roughness trend H20 (resolution direction)
      - sensory_pleasantness mean H20 (sustained pleasure)
      - amplitude velocity H20 (phrase-level buildup)
      - beat_strength trend H20 (anticipatory DA ramp)

    The anticipatory pathway is well-served by L0 — trend demands
    are exactly the "building toward climax" signals.
    """

    def __init__(self) -> None:
        self._srp = SRP()

        # Filter to L0-only
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._srp.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "SRP"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from SRP (causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[SRPOutput]:
        """Run SRP and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            SRPOutput with 7 approved dimensions, or None.
        """
        srp_14d = self._srp.compute(h3, r3)  # (B, T, 14)

        return SRPOutput(
            wanting=srp_14d[..., 7],
            liking=srp_14d[..., 8],
            pleasure=srp_14d[..., 9],
            tension=srp_14d[..., 10],
            reward_forecast=srp_14d[..., 11],
            chills_proximity=srp_14d[..., 12],
            resolution_expect=srp_14d[..., 13],
        )
