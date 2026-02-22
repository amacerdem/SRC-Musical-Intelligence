"""timbral_character — Core belief (MIAA, F1).

"I recognize this timbre / warm vs bright."

Dependency chain:
    MIAA (Depth 0, Relay) → timbral_character
    Without MIAA mechanism output, this belief cannot be computed.

Observe: 0.50×P0:melody_retrieval + 0.30×E0:imagery_activation
         + 0.20×M1:familiarity_effect
Predict: τ×prev + (1-τ)×baseline + trend + periodicity + context
Update:  Bayesian gain = π_obs / (π_obs + π_pred)

τ = 0.5 (moderate — timbre character changes slowly, holds across notes).

See Building/C³-Brain/F1-Sensory-Processing/beliefs/miaa/timbral_character.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import CoreBelief

# ── MIAA output indices (11D) ────────────────────────────────────────
_E0_IMAGERY_ACTIVATION = 0    # E0:imagery_activation
_M1_FAMILIARITY_EFFECT = 4    # M1:familiarity_effect
_P0_MELODY_RETRIEVAL = 5      # P0:melody_retrieval

# ── H³ tuples for predict ───────────────────────────────────────────
_TONALNESS_MEAN = (14, 5, 1, 0)       # tonalness mean at alpha-beta
_SPECTRAL_AUTO_MEAN = (17, 8, 1, 0)   # spectral_auto mean at syllable

# ── Predict weights ──────────────────────────────────────────────────
_W_TREND = 0.04
_W_PERIOD = 0.03
_W_CTX = 0.03


class TimbralCharacter(CoreBelief):
    """Core belief: timbre recognition and character assessment.

    Measures confidence in identifying the current timbral quality —
    whether the sound is warm, bright, rich, or thin. High τ (0.5)
    reflects that timbre character is relatively stable across notes
    of the same instrument, changing mainly with instrument switches.

    Dependency: Requires MIAA mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "timbral_character"
    FULL_NAME = "Timbral Character"
    FUNCTION = "F1"
    MECHANISM = "MIAA"
    TAU = 0.5
    BASELINE = 0.5

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("P0:melody_retrieval", 0.50),
        ("E0:imagery_activation", 0.30),
        ("M1:familiarity_effect", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe timbral character from MIAA outputs.

        Args:
            mechanism_output: ``(B, T, 11)`` MIAA output tensor.

        Returns:
            ``(B, T)`` observed timbral character value.
        """
        return (
            0.50 * mechanism_output[:, :, _P0_MELODY_RETRIEVAL]
            + 0.30 * mechanism_output[:, :, _E0_IMAGERY_ACTIVATION]
            + 0.20 * mechanism_output[:, :, _M1_FAMILIARITY_EFFECT]
        )

    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next timbral character value.

        Context signals:
            - ``imagery_recognition``: MIAA Anticipation belief
              (forward-looking recognition probability)

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

        # H³ trend: tonalness mean — slow-changing tonal quality
        trend = h3_features.get(_TONALNESS_MEAN, zero)
        # H³ periodicity: spectral autocorrelation — timbral periodicity
        period = h3_features.get(_SPECTRAL_AUTO_MEAN, zero)
        # Context: imagery recognition from MIAA Anticipation belief
        ctx = context.get("imagery_recognition", zero)

        return base + _W_TREND * trend + _W_PERIOD * period + _W_CTX * ctx
