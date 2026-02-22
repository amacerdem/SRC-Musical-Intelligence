"""PNH H-Layer — Harmonic Encoding (3D).

Three features encoding the Pythagorean ratio complexity hierarchy
(Bidelman & Krishnan 2009):

  H0: ratio_encoding     — Pythagorean complexity proxy (roughness+inharmonicity)
  H1: conflict_response  — IFG/ACC conflict monitoring (dissonance > consonance)
  H2: expertise_mod      — Training-dependent encoding modulation

H3 consumed:
    (0, 10, 0, 2)   roughness value H10 L2    — current dissonance at chord level
    (5, 10, 0, 2)   inharmonicity value H10 L2 — current ratio complexity
    (3, 10, 0, 2)   stumpf value H10 L2       — current tonal fusion

R3 consumed:
    [0] roughness      — sensory dissonance ∝ ratio complexity
    [1] sethares       — timbre-dependent dissonance
    [5] inharmonicity  — ratio complexity proxy
    [8] velocity_D     — loudness (attention weight)

Note: Model doc references x_l0l5[25:33] which is DISSOLVED in 97D freeze.
Replaced with inline energy×consonance coupling: velocity_D × roughness.
Model doc [10] loudness → corrected to [8] velocity_D (97D freeze mapping).

See Docs/C³/Models/IMU-α2-PNH/PNH.md §6.1
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_H10 = (0, 10, 0, 2)
_INHARM_H10 = (5, 10, 0, 2)
_STUMPF_H10 = (3, 10, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_INHARM = 5
_VELOCITY_D = 8  # loudness (doc said [10], corrected to [8] in 97D)

# -- Model coefficients (from PNH doc §6.1) -----------------------------------
_ALPHA = 0.75   # attention weight (ratio encoding)
_BETA = 0.70    # conflict sensitivity
_GAMMA = 0.60   # training weight


def compute_extraction(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """H-layer: 3D harmonic encoding from R3/H3.

    Args:
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(H0, H1, H2)`` each ``(B, T)``.
    """
    # R3 features
    roughness = r3_features[:, :, _ROUGHNESS]
    sethares = r3_features[:, :, _SETHARES]
    inharm = r3_features[:, :, _INHARM]
    velocity_d = r3_features[:, :, _VELOCITY_D]

    # H3 features
    roughness_h10 = h3_features[_ROUGHNESS_H10]
    inharm_h10 = h3_features[_INHARM_H10]
    stumpf_h10 = h3_features[_STUMPF_H10]

    # Energy-consonance coupling (replaces dissolved x_l0l5)
    energy_cons_coupling = velocity_d * roughness

    # H0: Ratio Encoding — Pythagorean complexity proxy
    # σ(α · (roughness + inharmonicity) / 2)
    # Low = simple ratio (consonant), High = complex ratio (dissonant)
    h0 = torch.sigmoid(
        _ALPHA * (roughness_h10 + inharm_h10) / 2.0
    )

    # H1: Conflict Response — IFG/ACC conflict monitoring
    # σ(β · coupling · roughness) — dissonant > consonant activation
    # Kim 2021: R-IFG→L-IFG connectivity for syntactic irregularity
    h1 = torch.sigmoid(
        _BETA * energy_cons_coupling * roughness_h10
    )

    # H2: Expertise Modulation — training-dependent encoding
    # σ(γ · stumpf · (1 - sethares)) — fusion × low-dissonance
    # Crespo-Bojorque 2018: musicians show pattern in more ROIs
    h2 = torch.sigmoid(
        _GAMMA * stumpf_h10 * (1.0 - sethares)
    )

    return h0, h1, h2
