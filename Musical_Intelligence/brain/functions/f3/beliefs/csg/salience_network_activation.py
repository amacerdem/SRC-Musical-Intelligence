"""salience_network_activation — Core belief (CSG cross-function, F3).

"Salience network (ACC/insula) is activated by consonance gradient."

Observe: 0.40*P0:salience_network + 0.30*E0:salience_activation
         + 0.30*M0:salience_response
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.3 (low inertia — rapid salience response to consonance changes).
Multi-scale horizons: H5, H7, H10, H13, H18, H21.

CSG is F1-primary. This belief is cross-function: CSG mechanism serves F3.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- CSG output indices (12D) -------------------------------------------------
_E0_SALIENCE_ACTIVATION = 0    # E0:salience_activation
_M0_SALIENCE_RESPONSE = 3      # M0:salience_response
_P0_SALIENCE_NETWORK = 6       # P0:salience_network

# -- H3 tuples for predict ----------------------------------------------------
_ROUGHNESS_TREND = (0, 16, 18, 0)       # roughness M18 trend 1s L0
_PLEAS_PERIODICITY = (4, 3, 14, 2)      # pleasantness M14 periodicity 100ms L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.03


class SalienceNetworkActivation(CoreBelief):
    """Core belief: salience network activation by consonance gradient.

    Measures how strongly the consonance/dissonance gradient drives
    ACC/anterior insula activation. High values = strong salience
    network engagement (typically high dissonance).

    CSG is F1-primary; this belief is cross-function to F3.
    Dependency: Requires CSG mechanism (Relay, Depth 0, F1).
    """

    NAME = "salience_network_activation"
    FULL_NAME = "Salience Network Activation"
    FUNCTION = "F3"
    MECHANISM = "CSG"
    TAU = 0.3
    BASELINE = 0.4

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:salience_network", 0.40),
        ("E0:salience_activation", 0.30),
        ("M0:salience_response", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe salience network activation from CSG outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` CSG output tensor.

        Returns:
            ``(B, T)`` observed salience network activation value.
        """
        return (
            0.40 * mechanism_output[:, :, _P0_SALIENCE_NETWORK]
            + 0.30 * mechanism_output[:, :, _E0_SALIENCE_ACTIVATION]
            + 0.30 * mechanism_output[:, :, _M0_SALIENCE_RESPONSE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next salience network activation value."""
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_ROUGHNESS_TREND, zero)
        period = h3_features.get(_PLEAS_PERIODICITY, zero)
        ctx = context.get("beat_entrainment", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
