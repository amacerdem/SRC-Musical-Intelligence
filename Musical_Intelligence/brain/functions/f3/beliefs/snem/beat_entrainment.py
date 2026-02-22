"""beat_entrainment — Core belief (SNEM, F3).

"Neural oscillations are locked to the beat frequency."

Observe: 0.40*P0:beat_locked_activity + 0.30*M0:ssep_enhancement
         + 0.30*E0:beat_entrainment
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.35 (moderate — tracks beat-locking at ~300ms).
Multi-scale horizons: H5, H7, H10, H13, H18, H21.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SNEM output indices (12D) ------------------------------------------------
_E0_BEAT_ENTRAINMENT = 0       # E0:beat_entrainment
_M0_SSEP_ENHANCEMENT = 3      # M0:ssep_enhancement
_P0_BEAT_LOCKED = 6            # P0:beat_locked_activity

# -- H3 tuples for predict ----------------------------------------------------
_FLUX_TREND = (10, 16, 18, 0)           # spectral_flux M18 trend 1s L0
_FLUX_PERIODICITY = (10, 16, 14, 2)     # spectral_flux M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.05
_W_CTX = 0.03


class BeatEntrainment(CoreBelief):
    """Core belief: neural oscillations locked to beat frequency.

    Measures strength of beat-locked entrainment. High values indicate
    strong phase-locking to beat frequency (Nozaradan 2011). Low values
    indicate weak or absent entrainment.

    Dependency: Requires SNEM mechanism (Relay, Depth 0).
    """

    NAME = "beat_entrainment"
    FULL_NAME = "Beat Entrainment"
    FUNCTION = "F3"
    MECHANISM = "SNEM"
    TAU = 0.35
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:beat_locked_activity", 0.40),
        ("M0:ssep_enhancement", 0.30),
        ("E0:beat_entrainment", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe beat entrainment from SNEM outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` SNEM output tensor.

        Returns:
            ``(B, T)`` observed beat entrainment value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_BEAT_LOCKED]
            + 0.30 * mechanism_output[:, :, _M0_SSEP_ENHANCEMENT]
            + 0.30 * mechanism_output[:, :, _E0_BEAT_ENTRAINMENT]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next beat entrainment value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``meter_hierarchy``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_FLUX_TREND, zero)
        period = h3_features.get(_FLUX_PERIODICITY, zero)
        ctx = context.get("meter_hierarchy", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
