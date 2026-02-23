"""neural_synchrony -- Core belief (NSCP, F9).

"Listeners are neurally synchronized during shared musical
experience, reflecting inter-subject coherence."

Observe: 0.50*E0:f22_neural_synchrony + 0.30*M0:isc_magnitude
         + 0.20*P0:coherence_level
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.65 (moderate -- synchrony fluctuates with musical events).

See Building/C3-Brain/F9-Social/beliefs/neural-synchrony.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- NSCP output indices ---------------------------------------------------
_E0_NEURAL_SYNCHRONY = 0             # E0:f22_neural_synchrony
_M0_ISC_MAGNITUDE = 3                # M0:isc_magnitude
_P0_COHERENCE_LEVEL = 6              # P0:coherence_level

# -- H3 tuples for predict -------------------------------------------------
_SYNCHRONY_TREND = (0, 8, 18, 0)     # synchrony M18 trend at 200ms, L0
_SYNCHRONY_PERIOD = (0, 12, 14, 0)   # synchrony M14 period 525ms, L0

# -- Predict weights --------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class NeuralSynchrony(CoreBelief):
    """Core belief: inter-subject neural synchrony during music."""

    NAME = "neural_synchrony"
    FULL_NAME = "Neural Synchrony"
    FUNCTION = "F9"
    MECHANISM = "NSCP"
    TAU = 0.65
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:f22_neural_synchrony", 0.50),
        ("M0:isc_magnitude", 0.30),
        ("P0:coherence_level", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe neural synchrony from NSCP output.

        Args:
            mechanism_output: ``(B, T, 11)`` NSCP output tensor.

        Returns:
            ``(B, T)`` observed neural synchrony value.
        """
        return (
            0.50 * mechanism_output[:, :, _E0_NEURAL_SYNCHRONY]
            + 0.30 * mechanism_output[:, :, _M0_ISC_MAGNITUDE]
            + 0.20 * mechanism_output[:, :, _P0_COHERENCE_LEVEL]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next neural synchrony value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``social_coordination``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_SYNCHRONY_TREND, zero)
        period = h3_features.get(_SYNCHRONY_PERIOD, zero)
        ctx = context.get("social_coordination", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
