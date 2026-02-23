"""period_entrainment — Core belief (PEOM, F7).

"Motor period is entrained to the auditory beat."

Observe: 0.50*f01:period_entrainment + 0.30*period_lock_strength
         + 0.20*next_beat_pred_T
Predict: tau*prev + (1-tau)*baseline + trend + periodicity + context
Update:  Bayesian gain = pi_obs / (pi_obs + pi_pred)

tau = 0.65 (high — motor entrainment is slow-adapting).

See Building/C3-Brain/F7-Motor-and-Timing/beliefs/period-entrainment.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- PEOM output indices (11D) ------------------------------------------------
_F01_PERIOD_ENTRAINMENT = 0    # f01:period_entrainment
_PERIOD_LOCK_STRENGTH = 7      # period_lock_strength
_NEXT_BEAT_PRED_T = 9          # next_beat_pred_T

# -- H3 tuples for predict ----------------------------------------------------
_BEAT_PERIODICITY_1S = (10, 16, 14, 2)    # onset_strength M14 periodicity 1s L2
_ONSET_PERIODICITY_1S = (11, 16, 14, 2)   # amplitude_centroid M14 periodicity 1s L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class PeriodEntrainment(CoreBelief):
    """Core belief: motor period entrained to auditory beat.

    Measures strength of motor-period entrainment to the perceived beat.
    High values indicate strong period-locking (Repp 2005).
    Low values indicate weak or absent entrainment.

    Dependency: Requires PEOM mechanism (Relay, Depth 0).
    """

    NAME = "period_entrainment"
    FULL_NAME = "Period Entrainment"
    FUNCTION = "F7"
    MECHANISM = "PEOM"
    TAU = 0.65
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f01:period_entrainment", 0.50),
        ("period_lock_strength", 0.30),
        ("next_beat_pred_T", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe period entrainment from PEOM outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` PEOM output tensor.

        Returns:
            ``(B, T)`` observed period entrainment value.
        """
        return (
            0.50 * mechanism_output[:, :, _F01_PERIOD_ENTRAINMENT]
            + 0.30 * mechanism_output[:, :, _PERIOD_LOCK_STRENGTH]
            + 0.20 * mechanism_output[:, :, _NEXT_BEAT_PRED_T]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next period entrainment value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``kinematic_efficiency``,
                ``next_beat_pred``).
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_BEAT_PERIODICITY_1S, zero)
        period = h3_features.get(_ONSET_PERIODICITY_1S, zero)
        ctx = (
            context.get("kinematic_efficiency", zero)
            + context.get("next_beat_pred", zero)
        ) * 0.5

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
