"""sequence_match — Core belief (SPH, F2).

"The incoming sequence matches a memorised pattern."

Observe: 0.40*E0:gamma_match + 0.30*P0:memory_match + 0.30*M2:gamma_power
Predict: τ×prev + (1-τ)×baseline + trend + velocity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.45 (moderate-high — sequence memory has persistence but adapts).
Multi-scale: 6 horizons (standard belief schedule).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/sph/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- SPH output indices (14D) -------------------------------------------------
_E0_GAMMA_MATCH = 0       # E0:gamma_match
_M2_GAMMA_POWER = 6       # M2:gamma_power
_P0_MEMORY_MATCH = 8      # P0:memory_match

# -- H3 tuples for predict ----------------------------------------------------
_TONAL_STAB_TREND = (60, 8, 18, 0)     # tonal_stability M18 trend 500ms L0
_PITCH_SAL_VEL = (39, 4, 8, 0)         # pitch_salience M8 velocity 125ms L0

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.04
_W_VEL = 0.03
_W_CTX = 0.02


class SequenceMatch(CoreBelief):
    """Core belief: auditory sequence match strength.

    Measures how well the incoming auditory sequence matches a memorised
    pattern. High values indicate strong memory match (gamma-dominant
    oscillatory state); low values indicate novel or varied sequences
    (alpha-beta dominant).

    Bonetti et al. 2024: memorised sequences → positive ~350ms, gamma
    power enhanced. Varied → negative ~250ms, alpha-beta enhanced.
    """

    NAME = "sequence_match"
    FULL_NAME = "Sequence Match"
    FUNCTION = "F2"
    MECHANISM = "SPH"
    TAU = 0.45
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:gamma_match", 0.40),
        ("P0:memory_match", 0.30),
        ("M2:gamma_power", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe sequence match from SPH outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` SPH output tensor.

        Returns:
            ``(B, T)`` observed sequence match value.
        """
        return (
            0.40 * mechanism_output[:, :, _E0_GAMMA_MATCH]
            + 0.30 * mechanism_output[:, :, _P0_MEMORY_MATCH]
            + 0.30 * mechanism_output[:, :, _M2_GAMMA_POWER]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next sequence match value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``prediction_hierarchy``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_TONAL_STAB_TREND, zero)
        vel = h3_features.get(_PITCH_SAL_VEL, zero)
        ctx = context.get("prediction_hierarchy", zero)

        return base + _W_TREND * trend + _W_VEL * vel + _W_CTX * ctx
