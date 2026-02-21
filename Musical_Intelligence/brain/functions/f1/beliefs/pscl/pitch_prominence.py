"""pitch_prominence — Core belief (PSCL, F1).

"I perceive a prominent pitch."

Observe: 0.60×P0:pitch_prominence_sig + 0.25×P1:hg_cortical_response
         + 0.15×P3:salience_hierarchy
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.35 (moderate-low — cortical pitch tracking with ~300ms response).
Operates at 6 horizons with T_char = 400ms.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/pitch-prominence.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# ── PSCL output indices ─────────────────────────────────────────────
_P0_PROMINENCE = 8         # P0:pitch_prominence_sig
_P1_HG_CORTICAL = 9       # P1:hg_cortical_response
_P3_SALIENCE_HIER = 11    # P3:salience_hierarchy

# ── H³ tuples for predict ──────────────────────────────────────────
_PITCHSAL_TREND = (39, 6, 18, 0)      # pitch_salience M18 trend 200ms, L0
_CONC_PERIOD = (24, 6, 14, 0)         # concentration M14 periodicity 200ms, L0

# ── Predict weights ─────────────────────────────────────────────────
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class PitchProminence(CoreBelief):
    """Core belief: pitch prominence / salience assessment."""

    NAME = "pitch_prominence"
    FULL_NAME = "Pitch Prominence"
    FUNCTION = "F1"
    MECHANISM = "PSCL"
    TAU = 0.35
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:pitch_prominence_sig", 0.60),
        ("P1:hg_cortical_response", 0.25),
        ("P3:salience_hierarchy", 0.15),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe pitch prominence from PSCL output.

        Args:
            mechanism_output: ``(B, T, 16)`` PSCL output tensor.

        Returns:
            ``(B, T)`` observed prominence value.
        """
        return (
            0.60 * mechanism_output[:, :, _P0_PROMINENCE]
            + 0.25 * mechanism_output[:, :, _P1_HG_CORTICAL]
            + 0.15 * mechanism_output[:, :, _P3_SALIENCE_HIER]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next pitch prominence value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values (``pitch_continuation``,
                ``harmonic_stability``).
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        trend = h3_features.get(_PITCHSAL_TREND, zero)
        period = h3_features.get(_CONC_PERIOD, zero)
        ctx = context.get("pitch_continuation", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
