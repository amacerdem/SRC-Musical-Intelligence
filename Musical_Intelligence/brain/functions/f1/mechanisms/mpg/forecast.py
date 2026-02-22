"""MPG F-Layer — Forecast (1D).

Phrase boundary prediction from melodic contour dynamics.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/mpg/MPG-forecast.md

Uses sigmoid activation: phrase boundaries are predicted when contour
dynamics shift (pitch trend changes) and onset periodicity breaks.

Outputs:
    F0: phrase_boundary_pred  [0, 1]  Phrase boundary prediction
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices ───────────────────────────────────────────────
_ONSET = 11           # onset_strength
_PITCH_HEIGHT = 37    # pitch_height
_BEAT_STR = 42        # beat_strength


def compute_forecast(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    p_outputs: Tuple[Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """Compute F-layer: 1D phrase boundary prediction from H³ + P + M.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.
        p_outputs: Tuple of (P0, P1) from cognitive_present.
        m_outputs: Tuple of (M0, M1, M2) from temporal_integration.

    Returns:
        Tuple of (F0,), with ``(B, T)`` shape.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    _p0, p1 = p_outputs
    m0, _m1, _m2 = m_outputs

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    # F0: phrase_boundary_pred — Cheung 2019: uncertainty×surprise at boundaries
    #     Phrase boundaries occur when:
    #       - pitch contour direction changes (pitch_height trend)
    #       - onset periodicity breaks (onset periodicity disruption)
    #       - rhythmic structure shifts (beat_strength periodicity)
    #     Coefficients: 0.30 + 0.25 + 0.25 + 0.20 = 1.0
    f0 = torch.sigmoid(
        0.30 * h3(_PITCH_HEIGHT, 4, 18, 2)   # pitch_height trend ~125ms
        + 0.25 * (1.0 - h3(_ONSET, 16, 14, 2))  # onset periodicity break ~1s
        + 0.25 * p1                            # contour_state (anterior activity)
        + 0.20 * (1.0 - h3(_BEAT_STR, 3, 14, 2))  # beat periodicity break
    )

    return (f0,)
