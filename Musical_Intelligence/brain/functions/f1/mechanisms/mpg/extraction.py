"""MPG E-Layer — Extraction (4D).

Instantaneous melodic gradient features from R³ + H³.
Matches Building/C³-Brain/F1-Sensory-Processing/mechanisms/mpg/MPG-extraction.md

Uses sigmoid activation following Rupp et al. 2022 gradient model.
Coefficient saturation rule: |wi| sum ≤ 1.0 per sigmoid.

Outputs:
    E0: onset_posterior          [0, 1]  Posterior AC dominance at onset
    E1: sequence_anterior        [0, 1]  Anterior AC activation for contour
    E2: contour_complexity       [0, 1]  Melodic complexity index
    E3: gradient_ratio           [0, 1]  Posterior/anterior ratio
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# ── R³ feature indices (post-freeze 97D) ─────────────────────────────
_AMPLITUDE = 7        # amplitude
_ONSET = 11           # onset_strength
_SHARPNESS = 13       # sharpness (was "brightness" in R³ v1)
_SPECTRAL_FLUX = 21   # spectral_flux (moved from old [10])
_PITCH_HEIGHT = 37    # pitch_height (replaces dissolved pitch_change)
_PITCH_SAL = 39       # pitch_salience (replaces dissolved x_l4l5)

# ── Gradient ratio epsilon ───────────────────────────────────────────
_EPS = 1e-6


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: 4D instantaneous extraction with sigmoid activation.

    Args:
        r3_features: ``(B, T, 97)`` R³ spectral features.
        h3_features: Per-demand H³ time series.

    Returns:
        Tuple of (E0, E1, E2, E3), each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    def h3(r3_idx: int, horizon: int, morph: int, law: int) -> Tensor:
        key = (r3_idx, horizon, morph, law)
        if key in h3_features:
            return h3_features[key]
        return torch.zeros(B, T, device=device)

    def r3(idx: int) -> Tensor:
        return r3_features[:, :, idx]

    # E0: Onset Posterior — posterior AC dominance at sequence onset
    #     Rupp 2022: posterior regions process onset; Patterson 2002: pitch in HG
    #     Coefficients: 0.40 + 0.35 + 0.25 = 1.0
    e0 = torch.sigmoid(
        0.40 * h3(_ONSET, 0, 0, 2)          # onset_strength instant
        + 0.35 * h3(_SPECTRAL_FLUX, 3, 0, 2)  # spectral_flux at ~100ms
        + 0.25 * h3(_AMPLITUDE, 3, 0, 2)    # amplitude at ~100ms
    )

    # E1: Sequence Anterior — anterior AC activation for contour tracking
    #     Rupp 2022: anterior regions process subsequent notes & pitch variation
    #     Coefficients: 0.35 + 0.35 + 0.30 = 1.0
    e1 = torch.sigmoid(
        0.35 * h3(_SHARPNESS, 4, 8, 0)      # sharpness velocity ~125ms
        + 0.35 * h3(_PITCH_HEIGHT, 4, 18, 2)  # pitch_height trend ~125ms
        + 0.30 * h3(_PITCH_HEIGHT, 3, 0, 2)  # pitch_height value ~100ms
    )

    # E2: Contour Complexity — melodic unpredictability
    #     Briley 2013: IRN sources show spectral complexity sensitivity
    #     Coefficients: 0.35 + 0.35 + 0.30 = 1.0
    e2 = torch.sigmoid(
        0.35 * h3(_PITCH_HEIGHT, 4, 18, 2)   # pitch_height trend ~125ms
        + 0.35 * h3(_SHARPNESS, 3, 2, 2)     # sharpness std ~100ms
        + 0.30 * h3(_PITCH_SAL, 3, 8, 0)     # pitch_salience velocity ~100ms
    )

    # E3: Gradient Ratio — posterior/anterior balance
    #     f01 / (f01 + f02 + ε): 1.0 = pure onset, 0.0 = pure contour
    e3 = e0 / (e0 + e1 + _EPS)

    return e0, e1, e2, e3
