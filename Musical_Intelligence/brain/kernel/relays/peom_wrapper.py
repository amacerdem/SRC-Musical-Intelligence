"""PEOMKernelWrapper — causal-mode PEOM adapter for C³ Kernel.

Wraps the production PEOM Relay (MPU, 11D) for use inside the
kernel belief cycle.  Provides motor-auditory entrainment signals
for tempo belief enrichment.

Rules:
  1. Expose P-layer (2D) + F-layer (2D) = 4 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — causal mode
  4. Return None on failure → belief falls back to R³+H³

Note: PEOM has 3 L0 demands:
  - loudness mean H8 (motor drive level)
  - spectral_flux velocity H4 (tempo velocity)
  - spectral_flux mean H16 (sustained spectral change)
The remaining 12 L2 demands provide current-state beat tracking.
In causal mode, the motor drive and tempo velocity signals
capture period locking dynamics.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.mpu.relays.peom import PEOM


@dataclass(frozen=True)
class PEOMOutput:
    """Approved PEOM outputs for kernel tempo belief.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    period_lock_strength: Tensor   # Period-locked neural activity
    kinematic_smoothness: Tensor   # Jerk-reduction metric
    # F-layer: forecasts
    next_beat_pred: Tensor         # Next beat onset prediction
    velocity_profile_pred: Tensor  # Velocity profile 0.5T ahead


class PEOMKernelWrapper(RelayKernelWrapper):
    """Causal-mode PEOM adapter for C³ Kernel.

    PEOM models period entrainment optimization — how motor systems
    lock to auditory rhythm period (not phase).  In causal mode,
    3 of 15 demands survive L0 filtering:
      - loudness mean H8 (motor drive)
      - spectral_flux velocity H4 (tempo velocity at theta)
      - spectral_flux mean H16 (sustained beat context)

    Period-locking dynamics are well-served by mean/velocity
    demands over motor-relevant timescales.
    """

    def __init__(self) -> None:
        self._peom = PEOM()

        # Filter to L0-only
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._peom.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "PEOM"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from PEOM (causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[PEOMOutput]:
        """Run PEOM and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            PEOMOutput with 4 approved dimensions, or None.
        """
        peom_11d = self._peom.compute(h3, r3)  # (B, T, 11)

        return PEOMOutput(
            period_lock_strength=peom_11d[..., 7],
            kinematic_smoothness=peom_11d[..., 8],
            next_beat_pred=peom_11d[..., 9],
            velocity_profile_pred=peom_11d[..., 10],
        )
