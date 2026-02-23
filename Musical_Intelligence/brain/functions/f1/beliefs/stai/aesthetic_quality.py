"""aesthetic_quality — Core belief (STAI, F1).

"This sound has high/low aesthetic quality based on spectral-temporal
integration and neural connectivity patterns."

Observe: 0.40*E2:aesthetic_integration + 0.30*P2:aesthetic_response
         + 0.20*M0:aesthetic_value + 0.10*E3:vmpfc_ifg_connectivity
Predict: t*prev + (1-t)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

t = 0.4

See Building/C3-Brain/F1-Sensory-Processing/beliefs/aesthetic-quality.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- STAI output indices ---------------------------------------------------
_E2_AESTHETIC_INTEGRATION = 2     # E2:aesthetic_integration
_E3_VMPFC_IFG_CONN = 3           # E3:vmpfc_ifg_connectivity
_M0_AESTHETIC_VALUE = 4           # M0:aesthetic_value
_P2_AESTHETIC_RESPONSE = 8        # P2:aesthetic_response

# -- H3 tuples for predict -------------------------------------------------
_PLEASANTNESS_TREND = (4, 8, 18, 0)    # sensory_pleasantness M18 trend, L0
_PLEASANTNESS_PERIOD = (4, 8, 14, 0)   # sensory_pleasantness M14 period, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class AestheticQuality(CoreBelief):
    """Core belief: overall aesthetic quality of the auditory stimulus."""

    NAME = "aesthetic_quality"
    FULL_NAME = "Aesthetic Quality"
    FUNCTION = "F1"
    MECHANISM = "STAI"
    TAU = 0.4
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E2:aesthetic_integration", 0.40),
        ("P2:aesthetic_response", 0.30),
        ("M0:aesthetic_value", 0.20),
        ("E3:vmpfc_ifg_connectivity", 0.10),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe aesthetic quality from STAI output.

        Args:
            mechanism_output: ``(B, T, 12)`` STAI output tensor.

        Returns:
            ``(B, T)`` observed aesthetic quality value.
        """
        return (
            0.40 * mechanism_output[:, :, _E2_AESTHETIC_INTEGRATION]
            + 0.30 * mechanism_output[:, :, _P2_AESTHETIC_RESPONSE]
            + 0.20 * mechanism_output[:, :, _M0_AESTHETIC_VALUE]
            + 0.10 * mechanism_output[:, :, _E3_VMPFC_IFG_CONN]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next aesthetic quality value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``harmonic_stability``,
                ``spectral_temporal_synergy``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_PLEASANTNESS_TREND, zero)
        period = h3_features.get(_PLEASANTNESS_PERIOD, zero)
        ctx_hs = context.get("harmonic_stability", zero)
        ctx_sts = context.get("spectral_temporal_synergy", zero)

        return (
            base
            + _W_TREND * trend
            + _W_PERIOD * period
            + _W_CTX * ctx_hs
            + _W_CTX * ctx_sts
        )
