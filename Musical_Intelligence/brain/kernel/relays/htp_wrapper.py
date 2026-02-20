"""HTPKernelWrapper — causal-mode HTP adapter for C³ Kernel.

Wraps the production HTP Relay (PCU, 12D) for use inside the
kernel belief cycle.  Provides hierarchical temporal prediction
signals for predictive coding enrichment.

Rules:
  1. Expose P-layer (3D) + F-layer (2D) = 5 approved outputs
  2. H³ demand deduplication against existing kernel demands
  3. L0 (memory) only — causal mode
  4. Return None on failure → belief falls back to R³+H³

Note: HTP has 9 L0 demands spanning delta→beat timescales:
  - spectral_flux velocity H3, value H4 (mid-level dynamics)
  - sharpness velocity H4, mean H8 (pitch prediction)
  - tonal_stability value/mean H8, mean/entropy H16, velocity H4
In causal mode, the delta-band and beat-band L0 demands capture
the abstract-to-sensory prediction hierarchy.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple

from torch import Tensor

from .base_wrapper import RelayKernelWrapper
from ...units.pcu.relays.htp import HTP


@dataclass(frozen=True)
class HTPOutput:
    """Approved HTP outputs for kernel predictive coding.

    All tensors are (B, T) shaped.
    """
    # P-layer: present state
    sensory_match: Tensor          # Low-level prediction match
    pitch_prediction: Tensor       # Mid-level pitch prediction
    abstract_prediction: Tensor    # High-level abstract prediction
    # F-layer: forecasts
    abstract_future_500ms: Tensor  # High cortical prediction
    midlevel_future_200ms: Tensor  # Intermediate area prediction


class HTPKernelWrapper(RelayKernelWrapper):
    """Causal-mode HTP adapter for C³ Kernel.

    HTP models hierarchical temporal prediction — how high-level
    abstract features are predicted ~500ms before input, mid-level
    ~200ms, low-level ~110ms.  In causal mode, 9 of 18 demands
    survive L0 filtering:
      - spectral_flux velocity H3 (mid-level change rate)
      - spectral_flux value H4 (theta-band boundary)
      - sharpness velocity H4 (pitch velocity)
      - sharpness mean H8 (abstract pitch context)
      - tonal_stability value H8, mean H8 (abstract template)
      - tonal_stability mean H16, entropy H16 (long-term context)
      - tonal_stability velocity H4 (mid-level dynamics)

    L0 demands provide the sustained templates against which
    incoming sensory input is compared for prediction error.
    """

    def __init__(self) -> None:
        self._htp = HTP()

        # Filter to L0-only
        self._l0_demands: Set[Tuple[int, int, int, int]] = set()
        for spec in self._htp.h3_demand:
            if spec.law == 0:
                self._l0_demands.add(spec.as_tuple())

    @property
    def name(self) -> str:
        return "HTP"

    @property
    def h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """L0-only H³ demands from HTP (causal mode)."""
        return self._l0_demands

    def compute(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Optional[HTPOutput]:
        """Run HTP and extract P-layer + F-layer outputs.

        Args:
            r3: (B, T, 97) R³ features.
            h3: H³ morphology dict {(r3_idx, h, m, l): (B, T)}.

        Returns:
            HTPOutput with 5 approved dimensions, or None.
        """
        htp_12d = self._htp.compute(h3, r3)  # (B, T, 12)

        return HTPOutput(
            sensory_match=htp_12d[..., 7],
            pitch_prediction=htp_12d[..., 8],
            abstract_prediction=htp_12d[..., 9],
            abstract_future_500ms=htp_12d[..., 10],
            midlevel_future_200ms=htp_12d[..., 11],
        )
