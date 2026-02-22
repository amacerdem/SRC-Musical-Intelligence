"""SDNPS E-Layer — Extraction (3D).

Three explicit features modeling stimulus-dependent neural pitch salience
(Cousineau et al. 2015):

  E0: nps_value           — Neural Pitch Salience proxy (FFR magnitude)
  E1: stimulus_dependency — Generalization limit (simple→complex)
  E2: roughness_corr      — Roughness correlation (invariant r=-0.57)

H3 consumed:
    (0, 6, 14, 0)  roughness periodicity H6 L0 — roughness periodicity 200ms
    (14, 0,  0, 2)  tonalness value H0 L2       — current pitch clarity
    (5,  0,  0, 2)  inharmonicity value H0 L2   — spectral complexity

R3 consumed:
    [5]  inharmonicity — spectral deviation
    [14] tonalness     — harmonic-to-noise ratio
    [17] spectral_autocorrelation — harmonic periodicity
    [18] tristimulus1  — fundamental energy
    [19] tristimulus2  — mid harmonics
    [20] tristimulus3  — high harmonics

See Docs/C³/Models/SPU-γ1-SDNPS/SDNPS.md §7.2
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_PERIOD_H6 = (0, 6, 14, 0)

# -- R3 indices ----------------------------------------------------------------
_INHARM = 5
_TONALNESS = 14
_SPECTRAL_AUTO = 17
_TRIST1 = 18
_TRIST2 = 19
_TRIST3 = 20

# -- Empirical constants (Cousineau et al. 2015) ------------------------------
_NPS_ROUGH_R = -0.57  # NPS ↔ roughness (stimulus-invariant)


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # R3 features
    inharm = r3_features[:, :, _INHARM]
    tonalness = r3_features[:, :, _TONALNESS]
    autocorr = r3_features[:, :, _SPECTRAL_AUTO]
    trist1 = r3_features[:, :, _TRIST1]
    trist2 = r3_features[:, :, _TRIST2]
    trist3 = r3_features[:, :, _TRIST3]

    # H3 features
    roughness_period = h3_features[_ROUGHNESS_PERIOD_H6]

    # Derived: tristimulus balance (1 - std → 1.0 when equal, low when skewed)
    trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)
    trist_balance = 1.0 - torch.std(trist_stack, dim=-1, correction=0)

    # Spectral complexity: high inharmonicity + low tonalness + skewed tristimulus
    spectral_complexity = inharm * (1.0 - tonalness) * (1.0 - trist_balance)

    # E0: NPS Value (FFR magnitude proxy)
    # Coefficient sum: 0.40 + 0.30 + 0.30 = 1.0
    # Cousineau 2015: NPS derived from brainstem phase-locking
    e0 = torch.sigmoid(
        0.40 * tonalness * autocorr
        + 0.30 * (1.0 - inharm)
        + 0.30 * trist_balance
    )

    # E1: Stimulus Dependency (generalization limit)
    # High for synthetic (simple spectra), low for natural (complex)
    # Coefficient sum: 0.50 + 0.50 = 1.0
    e1 = torch.sigmoid(
        0.50 * (1.0 - spectral_complexity) * e0
        + 0.50 * roughness_period
    )

    # E2: Roughness Correlation (empirical r=-0.57, stimulus-invariant)
    # Output range: [-0.57, 0] → clamp to [0, 1] for layer consistency
    # We store the raw roughness mean H3 scaled by empirical coefficient
    roughness_mean = h3_features[(0, 3, 1, 2)]
    e2 = torch.sigmoid(-_NPS_ROUGH_R * roughness_mean)

    return e0, e1, e2
