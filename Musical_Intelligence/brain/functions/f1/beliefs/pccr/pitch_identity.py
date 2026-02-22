"""pitch_identity — Core belief (PCCR, F1).

"This pitch belongs to chroma class X."

Dependency chain:
    BCH (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2) → pitch_identity
    Without PCCR mechanism output, this belief cannot be computed.
    PCCR itself requires BCH + PSCL (see PCCR.__init__.py).

Observe: 0.55×P0:chroma_identity_signal + 0.25×P2:chroma_salience
         + 0.20×E1:chroma_clarity
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.4 (moderate — chroma recognition takes more time than detection).
Operates at 6 horizons with T_char = 500ms.

See Building/C³-Brain/F1-Sensory-Processing/beliefs/pccr/pitch_identity.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# ── PCCR output indices (11D) ───────────────────────────────────────
_E1_CHROMA_CLARITY = 1          # E1:chroma_clarity
_P0_CHROMA_IDENTITY = 5        # P0:chroma_identity_signal
_P2_CHROMA_SALIENCE = 7        # P2:chroma_salience

# ── H³ tuples for predict ──────────────────────────────────────────
_PCE_TREND = (38, 6, 18, 0)         # PCE M18 trend at 200ms, L0
_TONAL_PERIOD = (14, 12, 14, 0)     # tonalness M14 periodicity at 525ms, L0

# ── Predict weights ─────────────────────────────────────────────────
_W_TREND = 0.05
_W_PERIOD = 0.03
_W_CTX = 0.02


class PitchIdentity(CoreBelief):
    """Core belief: pitch-class (chroma) identification confidence.

    Dependency: Requires PCCR mechanism (which requires BCH → PSCL → PCCR).
    """

    NAME = "pitch_identity"
    FULL_NAME = "Pitch Identity"
    FUNCTION = "F1"
    MECHANISM = "PCCR"
    TAU = 0.4
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:chroma_identity_signal", 0.55),
        ("P2:chroma_salience", 0.25),
        ("E1:chroma_clarity", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe pitch identity from PCCR output.

        Args:
            mechanism_output: ``(B, T, 11)`` PCCR output tensor.

        Returns:
            ``(B, T)`` observed chroma identity value.
        """
        return (
            0.55 * mechanism_output[:, :, _P0_CHROMA_IDENTITY]
            + 0.25 * mechanism_output[:, :, _P2_CHROMA_SALIENCE]
            + 0.20 * mechanism_output[:, :, _E1_CHROMA_CLARITY]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next pitch identity value.

        Context signals:
            - ``chroma_continuation``: PCCR F0 proxy (own mechanism trend)
            - ``pitch_prominence``: PSCL Core belief (upstream gate)

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values.
            h3_features: H³ temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """
        B, T = prev.shape
        device = prev.device
        zero = torch.zeros(B, T, device=device)

        base = self.TAU * prev + (1.0 - self.TAU) * self.BASELINE

        # H³ trend: PCE trend (inverted — low PCE trend = stable chroma)
        trend = h3_features.get(_PCE_TREND, zero)
        # H³ periodicity: tonalness cycling
        period = h3_features.get(_TONAL_PERIOD, zero)
        # Context: chroma continuation from PCCR F0 (stored as belief proxy)
        ctx = context.get("chroma_continuation", zero)

        return base + _W_TREND * (1.0 - trend) + _W_PERIOD * period + _W_CTX * ctx
