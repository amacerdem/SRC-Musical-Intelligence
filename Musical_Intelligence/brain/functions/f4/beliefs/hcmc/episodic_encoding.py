"""episodic_encoding — Core belief (HCMC, F4).

"I am encoding this music pattern right now."

Observe: 0.40*P0:binding_state + 0.30*E0:fast_binding + 0.30*P1:segmentation_state
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}

τ = 0.7 (high inertia — encoding state reflects sustained hippocampal binding).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- HCMC output indices (11D) ------------------------------------------------
_E0_FAST_BINDING = 0          # E0:fast_binding
_P0_BINDING_STATE = 6         # P0:binding_state
_P1_SEGMENTATION_STATE = 7    # P1:segmentation_state

# -- H3 tuples for predict ----------------------------------------------------
_FUSION_TREND = (3, 20, 18, 0)         # stumpf_fusion M18 trend 5s L0
_FLUX_PERIOD = (21, 16, 14, 2)         # spectral_flux M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.04
_W_CTX = 0.03


class EpisodicEncoding(CoreBelief):
    """Core belief: episodic encoding.

    Measures moment-by-moment hippocampal binding activation.
    High values = strong CA3 autoassociative binding of current input.

    Fernandez-Rubio 2022: left hippocampus activated at 4th tone
    of memorized sequences (MEG, N=71, MCS p<0.001).
    Dependency: Requires HCMC mechanism (Encoder, Depth 1).
    """

    NAME = "episodic_encoding"
    FULL_NAME = "Episodic Encoding"
    FUNCTION = "F4"
    MECHANISM = "HCMC"
    TAU = 0.7
    BASELINE = 0.4

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:binding_state", 0.40),
        ("E0:fast_binding", 0.30),
        ("P1:segmentation_state", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe episodic encoding from HCMC outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` HCMC output tensor.

        Returns:
            ``(B, T)`` observed encoding value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_BINDING_STATE]
            + 0.30 * mechanism_output[:, :, _E0_FAST_BINDING]
            + 0.30 * mechanism_output[:, :, _P1_SEGMENTATION_STATE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next encoding value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``autobiographical_retrieval``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_FUSION_TREND, zero)
        period = h3_features.get(_FLUX_PERIOD, zero)
        ctx = context.get("autobiographical_retrieval", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
