"""SNEMKernelWrapper — causal-mode SNEM adapter for C³ Kernel.

Wraps the production SNEM Relay (ASU, 12D) for use inside the
kernel belief cycle.  Feeds salience_state belief in Wave 1.

Rules:
  1. Expose P-layer (3D) + F-layer (3D) = 6 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — 3 of 18 SNEM demands survive (15 are L2)
  4. Return None on failure → belief falls back to R³+H³

Note: SNEM uses primarily L2 (integration) demands for its
computation.  In causal mode, only 3 L0 demands are available,
so SNEM operates in DEGRADED mode — most H³ inputs will be
zeros, and the relay falls back to R³ features internally.
This is acceptable for Wave 0 scaffolding.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.asu.relays.snem import SNEM


@dataclass(frozen=True)
class SNEMOutput:
    """Approved SNEM outputs for kernel salience belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    beat_locked_activity: Tensor   # Beat-locked neural amplitude
    entrainment_strength: Tensor   # Overall entrainment strength
    selective_gain: Tensor         # Selective gain magnitude
    # F-layer: predictions
    beat_onset_pred: Tensor        # Predicted next beat onset timing
    meter_position_pred: Tensor    # Predicted metrical position
    enhancement_pred: Tensor       # Predicted enhancement trajectory


class SNEMKernelWrapper(RelayKernelWrapper):
    """Causal-mode SNEM adapter for C³ Kernel.

    SNEM models the SS-EP neural entrainment pathway.  In causal
    mode, only 3 of 18 H³ demands survive L0 filtering:
      - (21, 6, 8, 0)  spectral_flux velocity at beat
      - (43, 6, 0, 0)  pulse_clarity value at beat
      - (41, 16, 1, 0) tempo_estimate mean at measure

    The relay computes with degraded H³ input — R³ fallbacks
    provide baseline onset/rhythm features.
    """

    def __init__(self) -> None:
        self._snem = SNEM()

        # Filter to L0-only (3 of 18 survive)
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._snem.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "SNEM"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from SNEM (3 tuples, causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[SNEMOutput]:
        """Run SNEM and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            SNEMOutput with 6 approved dimensions, or None.
        """
        snem_12d = self._snem.compute(h3, r3)  # (B, T, 12)

        return SNEMOutput(
            beat_locked_activity=snem_12d[..., 6],
            entrainment_strength=snem_12d[..., 7],
            selective_gain=snem_12d[..., 8],
            beat_onset_pred=snem_12d[..., 9],
            meter_position_pred=snem_12d[..., 10],
            enhancement_pred=snem_12d[..., 11],
        )
