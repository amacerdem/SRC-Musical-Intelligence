"""PNH H-Layer — Harmonic Encoding / Extraction (3D).

Non-standard first layer: H (Harmonic) instead of E (Extraction).
Three features modeling Pythagorean ratio complexity at the brainstem/cortical level:

  H0: ratio_complexity       — Pythagorean ratio complexity encoding [0, 1]
  H1: conflict_monitoring    — IFG/ACC conflict response to dissonance [0, 1]
  H2: expertise_modulation   — Training-dependent encoding modulation [0, 1]

H3 consumed:
    (0, 10, 0, 2)   roughness value H10 L2          — current dissonance (400ms)
    (0, 14, 1, 0)   roughness mean H14 L0           — avg dissonance over progression (700ms)
    (5, 10, 0, 2)   inharmonicity value H10 L2      — current ratio complexity (400ms)
    (5, 14, 1, 0)   inharmonicity mean H14 L0       — avg complexity over progression (700ms)
    (3, 10, 0, 2)   stumpf_fusion value H10 L2      — current tonal fusion (400ms)
    (10, 10, 0, 2)  loudness value H10 L2           — attention weight (400ms)

R3 consumed:
    [0]  roughness                — sensory dissonance proportional to ratio complexity
    [1]  sethares_dissonance      — timbre-dependent dissonance for expertise
    [5]  inharmonicity            — ratio complexity proxy
    [6]  harmonic_deviation       — error from ideal harmonics
    [14] tonalness                — harmonic-to-noise ratio purity
    [25:33] x_l0l5               — pitch-roughness coupling for conflict

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pnh/PNH-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_VAL_400MS = (0, 10, 0, 2)
_ROUGHNESS_MEAN_700MS = (0, 14, 1, 0)
_INHARM_VAL_400MS = (5, 10, 0, 2)
_INHARM_MEAN_700MS = (5, 14, 1, 0)
_FUSION_VAL_400MS = (3, 10, 0, 2)
_LOUDNESS_VAL_400MS = (10, 10, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_INHARMONICITY = 5
_HARMONIC_DEV = 6
_TONALNESS = 14
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """H-layer: 3D harmonic encoding from H3 + R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(H0, H1, H2)`` each ``(B, T)``.
    """
    # -- R3 slices -------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]           # (B, T)
    sethares = r3_features[..., _SETHARES]             # (B, T)
    inharmonicity = r3_features[..., _INHARMONICITY]   # (B, T)
    tonalness = r3_features[..., _TONALNESS]           # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- H3 lookups ------------------------------------------------------------
    roughness_val = h3_features[_ROUGHNESS_VAL_400MS]      # (B, T)
    roughness_mean = h3_features[_ROUGHNESS_MEAN_700MS]    # (B, T)
    inharm_val = h3_features[_INHARM_VAL_400MS]            # (B, T)
    fusion_val = h3_features[_FUSION_VAL_400MS]            # (B, T)
    loudness_val = h3_features[_LOUDNESS_VAL_400MS]        # (B, T)

    # -- Derived intermediates -------------------------------------------------
    # Prediction error proxy: deviation of current roughness from progression mean
    pred_error = (roughness_val - roughness_mean).abs()

    # Familiarity proxy: inverse of harmonic deviation (higher tonalness = more familiar)
    familiarity = tonalness

    # Training proxy: fusion strength as expertise indicator
    training = fusion_val

    # H0: Ratio complexity — Pythagorean log2(n*d) proxy
    # Bidelman & Krishnan 2009: brainstem FFR follows Pythagorean hierarchy (r>=0.81)
    h0 = torch.sigmoid(
        0.75 * (roughness + inharmonicity) / 2.0
    )

    # H1: Conflict monitoring — IFG/ACC activation for dissonant intervals
    # Kim et al. 2021: R-IFG to L-IFG connectivity for syntactic irregularity
    h1 = torch.sigmoid(
        0.70 * pred_error * x_l0l5.mean(dim=-1) * roughness
    )

    # H2: Expertise modulation — training-dependent encoding
    # Crespo-Bojorque et al. 2018: consonance-context MMN in all;
    # dissonance-context MMN only in musicians
    h2 = torch.sigmoid(
        0.60 * familiarity * (1.0 - sethares) * training
    )

    return h0, h1, h2
