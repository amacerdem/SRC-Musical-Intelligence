"""attention_capture — Core belief (IACM, F3).

"An inharmonic sound has captured involuntary attention."

Observe: 0.40*E0:inharmonic_capture + 0.30*M0:attention_capture
         + 0.30*P0:p3a_capture
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.25 (lowest in F3 — responds fastest to inharmonic events).
Multi-scale horizons: H3, H5, H7, H10.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- IACM output indices (11D) ------------------------------------------------
_E0_INHARMONIC_CAPTURE = 0     # E0:inharmonic_capture
_M0_ATTENTION_CAPTURE = 3      # M0:attention_capture
_P0_P3A_CAPTURE = 6            # P0:p3a_capture

# -- H3 tuples for predict ----------------------------------------------------
_TONALNESS_TREND = (14, 16, 18, 0)      # tonalness M18 trend 1s L0
_FLATNESS_PERIOD = (16, 3, 14, 2)       # spectral_flatness M14 periodicity 100ms L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.02


class AttentionCapture(CoreBelief):
    """Core belief: involuntary attention capture by inharmonic sounds.

    Measures how strongly an inharmonic event has captured attention.
    High values = strong capture (P3a response, ~300ms). Low = no capture.

    Albouy 2017: inharmonic tones elicit involuntary reorienting.
    Dependency: Requires IACM mechanism (Relay, Depth 0).
    """

    NAME = "attention_capture"
    FULL_NAME = "Attention Capture"
    FUNCTION = "F3"
    MECHANISM = "IACM"
    TAU = 0.25
    BASELINE = 0.3

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:inharmonic_capture", 0.40),
        ("M0:attention_capture", 0.30),
        ("P0:p3a_capture", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe attention capture from IACM outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` IACM output tensor.

        Returns:
            ``(B, T)`` observed attention capture value.
        """
        return (
            0.40 * mechanism_output[:, :, _E0_INHARMONIC_CAPTURE]
            + 0.30 * mechanism_output[:, :, _M0_ATTENTION_CAPTURE]
            + 0.30 * mechanism_output[:, :, _P0_P3A_CAPTURE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next attention capture value."""
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_TONALNESS_TREND, zero)
        period = h3_features.get(_FLATNESS_PERIOD, zero)
        ctx = context.get("beat_entrainment", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
