"""nostalgia_intensity — Core belief (MEAMN, F4).

"This feels like home." Warmth-familiarity response to consonance-timbre.

Observe: 0.40*P2:nostalgia_link + 0.30*E1:f02_nostalgia + 0.30*P0:memory_state
Predict: τ×prev + w_trend×M18 + w_period×M14 + w_ctx×beliefs_{t-1}

τ = 0.8 (very high inertia — nostalgia builds slowly and lingers).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# -- MEAMN output indices (12D) ------------------------------------------------
_E1_F02_NOSTALGIA = 1         # E1:f02_nostalgia
_P0_MEMORY_STATE = 5          # P0:memory_state
_P2_NOSTALGIA_LINK = 7        # P2:nostalgia_link

# -- H3 tuples for predict ----------------------------------------------------
_WARMTH_TREND = (12, 20, 18, 0)        # warmth M18 trend 5s L0
_WARMTH_MEAN = (12, 20, 1, 0)          # warmth M1 mean 5s L0

# -- Predict weights -----------------------------------------------------------
_W_TREND = 0.03
_W_PERIOD = 0.04
_W_CTX = 0.03


class NostalgiaIntensity(CoreBelief):
    """Core belief: nostalgia intensity.

    Measures warmth-familiarity response to consonance-timbre interaction.
    High values = strong nostalgia ("warm glow" from familiar timbral qualities).

    Sakakibara 2025: acoustic similarity alone triggers nostalgia
    (EEG, N=33, eta_p^2=0.636).
    Dependency: Requires MEAMN mechanism (Relay, Depth 0).
    """

    NAME = "nostalgia_intensity"
    FULL_NAME = "Nostalgia Intensity"
    FUNCTION = "F4"
    MECHANISM = "MEAMN"
    TAU = 0.8
    BASELINE = 0.2

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P2:nostalgia_link", 0.40),
        ("E1:f02_nostalgia", 0.30),
        ("P0:memory_state", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe nostalgia intensity from MEAMN outputs.

        Args:
            mechanism_output: ``(B, T, 12)`` MEAMN output tensor.

        Returns:
            ``(B, T)`` observed nostalgia intensity value.
        """
        return (
            0.40 * mechanism_output[:, :, _P2_NOSTALGIA_LINK]
            + 0.30 * mechanism_output[:, :, _E1_F02_NOSTALGIA]
            + 0.30 * mechanism_output[:, :, _P0_MEMORY_STATE]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next nostalgia intensity.

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

        trend = h3_features.get(_WARMTH_TREND, zero)
        period = h3_features.get(_WARMTH_MEAN, zero)
        ctx = context.get("autobiographical_retrieval", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
