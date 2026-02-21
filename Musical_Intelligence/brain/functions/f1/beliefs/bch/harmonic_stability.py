"""harmonic_stability — Core belief (BCH, F1).

"This sound is harmonically resolved/stable."

Observe: 0.50×P0:consonance_signal + 0.30×P1:template_match + 0.20×E2:hierarchy
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.3 (low — responds quickly to harmonic changes).
Operates at 8 consonance horizons with activated (non-uniform) weights.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/harmonic-stability.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# ── BCH output indices ──────────────────────────────────────────────
_E2_HIERARCHY = 2          # E2:hierarchy
_P0_CONSONANCE = 8         # P0:consonance_signal
_P1_TEMPLATE = 9           # P1:template_match

# ── H³ tuples for predict ──────────────────────────────────────────
_ROUGHNESS_TREND = (0, 6, 18, 0)      # roughness M18 trend at 200ms, L0
_ROUGHNESS_PERIOD = (0, 12, 1, 0)     # roughness mean 525ms, L0 (proxy)

# ── Predict weights ─────────────────────────────────────────────────
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class HarmonicStability(CoreBelief):
    """Core belief: harmonic stability / consonance assessment."""

    NAME = "harmonic_stability"
    FULL_NAME = "Harmonic Stability"
    FUNCTION = "F1"
    MECHANISM = "BCH"
    TAU = 0.3
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:consonance_signal", 0.50),
        ("P1:template_match", 0.30),
        ("E2:hierarchy", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe harmonic stability from BCH output.

        Args:
            mechanism_output: ``(B, T, 16)`` BCH output tensor.

        Returns:
            ``(B, T)`` observed stability value.
        """
        return (
            0.50 * mechanism_output[:, :, _P0_CONSONANCE]
            + 0.30 * mechanism_output[:, :, _P1_TEMPLATE]
            + 0.20 * mechanism_output[:, :, _E2_HIERARCHY]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next harmonic stability value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``consonance_trajectory``,
                ``pitch_prominence``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_ROUGHNESS_TREND, zero)
        period = h3_features.get(_ROUGHNESS_PERIOD, zero)
        ctx = context.get("consonance_trajectory", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
