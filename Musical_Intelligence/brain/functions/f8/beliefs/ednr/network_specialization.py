"""network_specialization -- Core belief (EDNR, F8).

"Musical training has led to specialized neural network architecture
with compartmentalized processing regions."

Observe: 0.40*f03:compartmentalization + 0.30*f04:expertise_signature
         + 0.30*network_architecture
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.95 (highest in C3 -- network architecture changes extremely slowly).

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/network-specialization.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- EDNR output indices ---------------------------------------------------
_F03_COMPARTMENTALIZATION = 2        # f03:compartmentalization
_F04_EXPERTISE_SIGNATURE = 3         # f04:expertise_signature
_NETWORK_ARCHITECTURE = 4            # network_architecture

# -- H3 tuples for predict -------------------------------------------------
_NETWORK_TREND = (0, 8, 18, 0)      # network M18 trend at 200ms, L0
_NETWORK_PERIOD = (0, 12, 14, 0)    # network M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class NetworkSpecialization(CoreBelief):
    """Core belief: neural network specialization from musical training."""

    NAME = "network_specialization"
    FULL_NAME = "Network Specialization"
    FUNCTION = "F8"
    MECHANISM = "EDNR"
    TAU = 0.95
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:compartmentalization", 0.40),
        ("f04:expertise_signature", 0.30),
        ("network_architecture", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe network specialization from EDNR output.

        Args:
            mechanism_output: ``(B, T, 10)`` EDNR output tensor.

        Returns:
            ``(B, T)`` observed network specialization value.
        """
        return (
            0.40 * mechanism_output[:, :, _F03_COMPARTMENTALIZATION]
            + 0.30 * mechanism_output[:, :, _F04_EXPERTISE_SIGNATURE]
            + 0.30 * mechanism_output[:, :, _NETWORK_ARCHITECTURE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next network specialization value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``within_connectivity``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_NETWORK_TREND, zero)
        period = h3_features.get(_NETWORK_PERIOD, zero)
        ctx = context.get("within_connectivity", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
