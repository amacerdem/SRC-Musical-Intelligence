"""DAEDKernelWrapper — causal-mode DAED adapter for C³ Kernel.

Wraps the production DAED Relay (RPU, 8D) for use inside the
kernel belief cycle.  Feeds reward_valence belief in Wave 1.

Rules:
  1. Expose E-layer wanting+liking (2D) + P-layer (2D) = 4 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — 5 of 16 DAED demands survive (11 are L2)
  4. Return None on failure → belief falls back to reward computation

Note: DAED's anticipatory pathway (caudate) relies heavily on
L0 velocity demands at H16 — the key "loudness rising" signal
survives causal filtering.  The consummatory pathway (NAcc) uses
mostly L2 demands, so it operates degraded in causal mode.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.rpu.relays.daed import DAED


@dataclass(frozen=True)
class DAEDOutput:
    """Approved DAED outputs for kernel reward belief.

    All tensors are (B, T) shaped.
    """
    # E-layer: motivation signals
    wanting_index: Tensor          # Anticipatory motivation (approach)
    liking_index: Tensor           # Consummatory pleasure (hedonic)
    # P-layer: regional activation
    caudate_activation: Tensor     # Anticipation level (scaled)
    nacc_activation: Tensor        # Pleasure level (scaled)


class DAEDKernelWrapper(RelayKernelWrapper):
    """Causal-mode DAED adapter for C³ Kernel.

    DAED models the mesolimbic DA pathway with temporally separated
    anticipatory (caudate) and consummatory (NAcc) signals.  In
    causal mode, 5 of 16 demands survive L0 filtering:
      - loudness mean H8 (memory)
      - loudness velocity H16 (THE anticipatory signal)
      - roughness velocity H8 (tension building)
      - onset_strength velocity H8 (event rate change)
      - spectral_flux entropy H4 (surprise history)

    The anticipatory pathway is well-served by L0 — velocity
    demands are exactly the "building toward climax" signals.
    """

    # E-layer indices for wanting/liking
    _IDX_WANTING = 2
    _IDX_LIKING = 3
    # P-layer indices for regional activation
    _IDX_CAUDATE = 6
    _IDX_NACC = 7

    def __init__(self) -> None:
        self._daed = DAED()

        # Filter to L0-only (5 of 16 survive)
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._daed.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "DAED"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from DAED (5 tuples, causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[DAEDOutput]:
        """Run DAED and extract wanting/liking + regional activations.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            DAEDOutput with 4 approved dimensions, or None.
        """
        daed_8d = self._daed.compute(h3, r3)  # (B, T, 8)

        return DAEDOutput(
            wanting_index=daed_8d[..., self._IDX_WANTING],
            liking_index=daed_8d[..., self._IDX_LIKING],
            caudate_activation=daed_8d[..., self._IDX_CAUDATE],
            nacc_activation=daed_8d[..., self._IDX_NACC],
        )
