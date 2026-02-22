"""prediction_hierarchy — Core belief (HTP, F2).

"Abstract/mid/low-level patterns are predictable ahead."

Observe: 0.40*E0:high_level_lead + 0.30*E1:mid_level_lead
         + 0.30*E2:low_level_lead
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.4 (moderate — balances prediction persistence with responsiveness).
Multi-scale: 6 horizons (H7=250ms, H10=400ms, H13=600ms, H16=1s, H18=2s, H21=8s).

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/htp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- HTP output indices (12D) -------------------------------------------------
_E0_HIGH_LEVEL_LEAD = 0     # E0:high_level_lead
_E1_MID_LEVEL_LEAD = 1      # E1:mid_level_lead
_E2_LOW_LEVEL_LEAD = 2      # E2:low_level_lead

# -- H3 tuples for predict ----------------------------------------------------
_TONAL_STAB_TREND = (60, 8, 18, 0)   # tonal_stability M18 trend 500ms L0
_ONSET_PERIOD = (11, 3, 14, 2)       # onset_strength M14 periodicity 100ms L2

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class PredictionHierarchy(CoreBelief):
    """Core belief: hierarchical prediction strength.

    Measures how predictable the current input is at all three
    hierarchy levels. High values indicate strong prediction at all
    levels; low values indicate unpredictable input (surprise).

    de Vries & Wurm 2023: ηp²=0.49 for hierarchical prediction timing.
    """

    NAME = "prediction_hierarchy"
    FULL_NAME = "Prediction Hierarchy"
    FUNCTION = "F2"
    MECHANISM = "HTP"
    TAU = 0.4
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E0:high_level_lead", 0.40),
        ("E1:mid_level_lead", 0.30),
        ("E2:low_level_lead", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe prediction hierarchy from HTP outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` HTP output tensor.

        Returns:
            ``(B, T)`` observed prediction hierarchy value.
        """
        return (
            0.40 * mechanism_output[:, :, _E0_HIGH_LEVEL_LEAD]
            + 0.30 * mechanism_output[:, :, _E1_MID_LEVEL_LEAD]
            + 0.30 * mechanism_output[:, :, _E2_LOW_LEVEL_LEAD]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next prediction hierarchy value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``abstract_future``,
                ``harmonic_stability``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_TONAL_STAB_TREND, zero)
        period = h3_features.get(_ONSET_PERIOD, zero)
        ctx = context.get("abstract_future", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
