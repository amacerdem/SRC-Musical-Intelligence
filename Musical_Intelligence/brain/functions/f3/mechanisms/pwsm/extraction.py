"""PWSM E-Layer -- Extraction (3D).

Three features modeling precision weighting and error dynamics:

  f19: precision_weighting  -- Precision weight for current prediction errors
  f20: error_suppression    -- Degree of error suppression (adaptation)
  f21: stability_encoding   -- Context stability encoding for precision base

H3 consumed:
    (10, 16, 17, 2)  spectral_flux peaks H16 bidi  -- salient onset detection
    (22, 16, 2, 2)   entropy std H16 bidi           -- spectral uncertainty
    (11, 3, 2, 2)    onset_strength std H3 bidi     -- onset variability
    (37, 3, 20, 2)   pitch_height contour H3 bidi   -- melodic contour
    (21, 3, 0, 2)    spectral_change value H3 bidi  -- instant deviation
    (21, 16, 2, 2)   spectral_change std H16 bidi   -- long-range variability

R3 consumed:
    [10] spectral_flux     -- onset energy
    [22] distribution_entropy -- spectral complexity

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/pwsm/PWSM-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_PEAKS_H16 = (10, 16, 17, 2)
_ENTROPY_STD_H16 = (22, 16, 2, 2)
_ONSET_STD_H3 = (11, 3, 2, 2)
_PITCH_CONTOUR_H3 = (37, 3, 20, 2)
_SPECTRAL_CHANGE_H3 = (21, 3, 0, 2)
_SPECTRAL_CHANGE_STD_H16 = (21, 16, 2, 2)

# -- R3 indices ----------------------------------------------------------------
_SPECTRAL_FLUX = 10
_ENTROPY = 22


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f19, f20, f21)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device
    zero = torch.zeros(B, T, device=device)

    # H3 features
    flux_peaks = h3_features.get(_FLUX_PEAKS_H16, zero)
    entropy_std = h3_features.get(_ENTROPY_STD_H16, zero)
    onset_std = h3_features.get(_ONSET_STD_H3, zero)
    pitch_contour = h3_features.get(_PITCH_CONTOUR_H3, zero)
    spectral_change = h3_features.get(_SPECTRAL_CHANGE_H3, zero)
    spectral_change_std = h3_features.get(_SPECTRAL_CHANGE_STD_H16, zero)

    # R3 direct
    flux_r3 = r3_features[:, :, _SPECTRAL_FLUX]
    entropy_r3 = r3_features[:, :, _ENTROPY]

    # f19: Precision Weighting -- precision = 1/variance
    # Friston 2005: precision is inverse variance of prediction errors
    # Low entropy_std = high precision = high weight
    f19 = torch.sigmoid(
        0.30 * flux_peaks
        + 0.25 * (1.0 - entropy_std)
        + 0.25 * onset_std
        + 0.20 * spectral_change
    )

    # f20: Error Suppression -- adaptation mechanism
    # Garrido 2009: repetition suppression reduces PE for standards
    # High regularity (low variability) = more suppression
    f20 = torch.sigmoid(
        0.30 * (1.0 - spectral_change_std)
        + 0.25 * (1.0 - onset_std)
        + 0.25 * (1.0 - entropy_r3)
        + 0.20 * flux_r3
    )

    # f21: Stability Encoding -- context stability for precision base
    # Winkler 2009: regularity representations track statistical structure
    f21 = torch.sigmoid(
        0.30 * (1.0 - spectral_change_std)
        + 0.25 * (1.0 - entropy_std)
        + 0.25 * pitch_contour
        + 0.20 * flux_peaks
    )

    return f19, f20, f21
