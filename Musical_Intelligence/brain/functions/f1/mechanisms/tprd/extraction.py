"""TPRD T-Layer — Tonotopic-Pitch Features (3D).

Three features modeling the medial-lateral dissociation in Heschl's gyrus
(Briley et al. 2013):

  T0: tonotopic    — Tonotopic encoding strength (primary/medial HG)
  T1: pitch        — Pitch representation strength (nonprimary/lateral HG)
  T2: dissociation — Representation dissociation degree

H3 consumed:
    (0, 10, 0, 2)   roughness value H10 L2     — tonotopic beating at chord level
    (14, 0, 0, 2)   tonalness value H0 L2      — immediate pitch salience
    (14, 3, 1, 2)   tonalness mean H3 L2       — brainstem pitch salience
    (17, 3, 14, 2)  spectral_auto period H3 L2 — harmonic periodicity brainstem
    (5, 10, 0, 2)   inharmonicity value H10 L2 — tonotopy-pitch conflict
    (22, 6, 0, 0)   entropy value H6 L0        — spectral complexity at beat

R3 consumed:
    [0] roughness     — tonotopic beating proxy
    [5] inharmonicity — spectral-pitch misalignment
    [7] velocity_A    — amplitude/energy (doc said [7])
    [14] tonalness    — pitch clarity
    [17] spectral_autocorrelation — harmonic periodicity
    [22] entropy      — spectral complexity

See Docs/C³/Models/IMU-β8-TPRD/TPRD.md §6.1 & §7.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_H10 = (0, 10, 0, 2)
_TONALNESS_H0 = (14, 0, 0, 2)
_TONALNESS_MEAN_H3 = (14, 3, 1, 2)
_AUTOCORR_PERIOD_H3 = (17, 3, 14, 2)
_INHARM_H10 = (5, 10, 0, 2)
_ENTROPY_H6 = (22, 6, 0, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARM = 5
_VELOCITY_A = 7   # amplitude (doc says [7])
_TONALNESS = 14
_SPECTRAL_AUTO = 17
_ENTROPY = 22

# -- Coefficients (from TPRD doc §7.1) ----------------------------------------
_A_TONO_1 = 0.35
_A_TONO_2 = 0.35
_A_PITCH_1 = 0.40
_A_PITCH_2 = 0.30
_A_DISSOC_1 = 0.30
_A_DISSOC_2 = 0.25
_A_DISSOC_3 = 0.25


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """T-layer: 3D tonotopic-pitch features from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(T0, T1, T2)`` each ``(B, T)``.
    """
    # R3 features
    roughness = r3_features[:, :, _ROUGHNESS]
    inharm = r3_features[:, :, _INHARM]
    amplitude = r3_features[:, :, _VELOCITY_A]
    tonalness = r3_features[:, :, _TONALNESS]
    autocorr = r3_features[:, :, _SPECTRAL_AUTO]
    entropy = r3_features[:, :, _ENTROPY]

    # H3 features
    roughness_h10 = h3_features[_ROUGHNESS_H10]
    tonalness_h0 = h3_features[_TONALNESS_H0]
    tonalness_mean = h3_features[_TONALNESS_MEAN_H3]
    autocorr_period = h3_features[_AUTOCORR_PERIOD_H3]
    inharm_h10 = h3_features[_INHARM_H10]
    entropy_h6 = h3_features[_ENTROPY_H6]

    # T0: Tonotopic Encoding (primary/medial HG)
    # High roughness + low tonalness = spectral (not pitch) encoding
    # Coefficient sum: 0.35 + 0.35 = 0.70
    t0 = torch.sigmoid(
        _A_TONO_1 * roughness_h10 * (1.0 - tonalness)
        + _A_TONO_2 * entropy_h6 * amplitude
    )

    # T1: Pitch Representation (nonprimary/lateral HG)
    # High pitch salience + tonalness × periodicity = F0 extraction
    # Coefficient sum: 0.40 + 0.30 = 0.70
    # pitch_salience proxy: tonalness_h0 (immediate F0 clarity)
    t1 = torch.sigmoid(
        _A_PITCH_1 * tonalness_mean * autocorr_period
        + _A_PITCH_2 * tonalness_h0 * autocorr
    )

    # T2: Representation Dissociation
    # |tonotopic - pitch| + inharmonicity
    # Coefficient sum: 0.30 + 0.25 + 0.25 = 0.80
    # Basinski 2025: inharmonicity → P3a → dissociation
    t2 = torch.sigmoid(
        _A_DISSOC_1 * torch.abs(t0 - t1)
        + _A_DISSOC_2 * inharm_h10
        + _A_DISSOC_3 * entropy
    )

    return t0, t1, t2
