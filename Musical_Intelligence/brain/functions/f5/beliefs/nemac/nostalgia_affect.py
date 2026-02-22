"""nostalgia_affect — Core belief (NEMAC, F5).

"I feel nostalgic."

Observe: 0.40*W0:nostalgia_intens + 0.30*E1:nostalgia + 0.30*P0:nostalgia_correl
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.65 (highest F5 inertia — nostalgia builds slowly and lingers).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- NEMAC output indices (11D) ------------------------------------------------
_E1_NOSTALGIA = 1             # E1:nostalgia
_W0_NOSTALGIA_INTENS = 5      # W0:nostalgia_intens
_P0_NOSTALGIA_CORREL = 7      # P0:nostalgia_correl

# -- H3 tuples for predict ----------------------------------------------------
_WARMTH_TREND = (12, 20, 18, 0)       # warmth M18 trend 5s L0
_TONALNESS_PERIOD = (14, 20, 14, 2)   # tonalness M14 periodicity 5s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.03
_W_PERIOD = 0.03
_W_CTX = 0.04


class NostalgiaAffect(CoreBelief):
    """Core belief: felt nostalgia.

    Measures felt nostalgic affect from music. Nostalgia builds slowly
    when familiar-warm music activates mPFC-hippocampus hub.

    Sakakibara 2025: acoustic similarity alone triggers nostalgia
    (EEG, N=33, eta_p^2=0.636).
    Dependency: Requires NEMAC mechanism (Encoder, Depth 1).
    """

    NAME = "nostalgia_affect"
    FULL_NAME = "Nostalgia Affect"
    FUNCTION = "F5"
    MECHANISM = "NEMAC"
    TAU = 0.65
    BASELINE = 0.3

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("W0:nostalgia_intens", 0.40),
        ("E1:nostalgia", 0.30),
        ("P0:nostalgia_correl", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe nostalgia affect from NEMAC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` NEMAC output tensor.

        Returns:
            ``(B, T)`` observed nostalgia affect value.
        """
        return (
            0.40 * mechanism_output[:, :, _W0_NOSTALGIA_INTENS]
            + 0.30 * mechanism_output[:, :, _E1_NOSTALGIA]
            + 0.30 * mechanism_output[:, :, _P0_NOSTALGIA_CORREL]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next nostalgia affect value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``self_referential_nostalgia``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_WARMTH_TREND, zero)
        period = h3_features.get(_TONALNESS_PERIOD, zero)
        ctx = context.get("self_referential_nostalgia", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
