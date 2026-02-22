"""meter_hierarchy — Core belief (SNEM, F3).

"Beats are grouped in a metric structure (bar, downbeat, etc.)."

Observe: 0.40*M0:ssep_enhancement + 0.30*E1:meter_entrainment
         + 0.30*E0:beat_entrainment
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.4 (slightly higher — meter structure changes slower than beat).
Multi-scale horizons: H10, H13, H16, H18.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SNEM output indices (12D) ------------------------------------------------
_E0_BEAT_ENTRAINMENT = 0       # E0:beat_entrainment
_E1_METER_ENTRAINMENT = 1     # E1:meter_entrainment
_M0_SSEP_ENHANCEMENT = 3      # M0:ssep_enhancement

# -- H3 tuples for predict ----------------------------------------------------
_COUPLING_TREND = (25, 16, 18, 0)        # x_l0l5 M18 trend 1s L0
_COUPLING_PERIODICITY = (25, 16, 14, 2)  # x_l0l5 M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.05
_W_CTX = 0.03


class MeterHierarchy(CoreBelief):
    """Core belief: metric hierarchical structure.

    Measures strength of metric grouping (bar-level organization).
    High values indicate clear meter (downbeat prominent).
    Low values indicate ambiguous or absent meter.

    Dependency: Requires SNEM mechanism (Relay, Depth 0).
    """

    NAME = "meter_hierarchy"
    FULL_NAME = "Meter Hierarchy"
    FUNCTION = "F3"
    MECHANISM = "SNEM"
    TAU = 0.4
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M0:ssep_enhancement", 0.40),
        ("E1:meter_entrainment", 0.30),
        ("E0:beat_entrainment", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe meter hierarchy from SNEM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` SNEM output tensor.

        Returns:
            ``(B, T)`` observed meter hierarchy value.
        """
        return (
            0.40 * mechanism_output[:, :, _M0_SSEP_ENHANCEMENT]
            + 0.30 * mechanism_output[:, :, _E1_METER_ENTRAINMENT]
            + 0.30 * mechanism_output[:, :, _E0_BEAT_ENTRAINMENT]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next meter hierarchy value."""
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_COUPLING_TREND, zero)
        period = h3_features.get(_COUPLING_PERIODICITY, zero)
        ctx = context.get("beat_entrainment", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
