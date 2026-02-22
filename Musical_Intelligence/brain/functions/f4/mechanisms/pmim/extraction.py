"""PMIM P-Layer -- Extraction / Prediction Features (3D).

Three prediction-error signals modelling ERAN and MMN responses:

  P0: eran_response       -- Long-term syntax violation signal [0, 1]
  P1: mmn_response        -- Short-term deviance detection signal [0, 1]
  P2: combined_pred_error  -- Integrated PE from shared IFG generators [0, 1]

ERAN (early right anterior negativity) is elicited when the current chord
violates stored harmonic rules — a memory-based prediction signal generated
in inferior BA 44 bilateral. MMN (mismatch negativity) detects short-term
deviance within the echoic memory window (~10 s). The combined PE merges
both streams, weighted by dissonance context.

H3 demands consumed (8 tuples):
  roughness:        (0,10,0,2)   value H10 L2       -- current dissonance
  roughness:        (0,14,1,0)   mean H14 L0        -- average dissonance
  inharmonicity:    (5,10,0,2)   value H10 L2       -- ratio deviation
  inharmonicity:    (5,14,8,0)   velocity H14 L0    -- complexity change rate
  entropy:          (22,10,0,2)  value H10 L2       -- current unpredictability
  spectral_flux:    (21,10,0,2)  value H10 L2       -- current change magnitude
  spectral_flux:    (21,14,8,0)  velocity H14 L0    -- change acceleration
  onset_strength:   (11,10,0,2)  value H10 L2       -- onset salience

R3 consumed:
  [0]     roughness           -- P2: sensory dissonance for PE weighting
  [5]     inharmonicity       -- P2: harmonic template deviation
  [21]    spectral_flux       -- P1: change detection (MMN basis)
  [22]    entropy             -- P0: syntactic unpredictability (ERAN basis)
  [25:33] x_l0l5             -- P1: sensory-level prediction coupling (MMN)
  [41:49] x_l5l7             -- P0: high-level syntactic prediction (ERAN)

Relay consumed:
  PNH (via relay_outputs) -- ratio_encoding for harmonic context

Scientific basis:
  Koelsch et al. 2000: ERAN at 150-180 ms, Neapolitan sixth (EEG N=24, p<0.001)
  Wagner et al. 2018: MMN for harmonic interval deviants (EEG N=15)
  Bonetti et al. 2024: hierarchical PE auditory cortex -> hippocampus (MEG N=83)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pmim/PMIM-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_VAL_H10 = (0, 10, 0, 2)       # current dissonance at chord level
_ROUGHNESS_MEAN_H14 = (0, 14, 1, 0)      # average dissonance over progression
_INHARMONICITY_VAL_H10 = (5, 10, 0, 2)   # current ratio deviation
_INHARMONICITY_VEL_H14 = (5, 14, 8, 0)   # rate of complexity change
_ENTROPY_VAL_H10 = (22, 10, 0, 2)        # current unpredictability
_FLUX_VAL_H10 = (21, 10, 0, 2)           # current change magnitude
_FLUX_VEL_H14 = (21, 14, 8, 0)           # acceleration of change
_ONSET_VAL_H10 = (11, 10, 0, 2)          # onset salience for MMN triggering

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARMONICITY = 5
_SPECTRAL_FLUX = 21
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D prediction-error extraction from H3/R3 + PNH relay.

    Computes ERAN response (P0), MMN response (P1), and combined prediction
    error (P2) using multi-scale temporal features, raw spectral features,
    and upstream PNH ratio encoding for harmonic context.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: ``{"PNH": (B, T, 11)}`` -- PNH ratio encoding.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    entropy_val = h3_features[_ENTROPY_VAL_H10]           # (B, T)
    flux_val = h3_features[_FLUX_VAL_H10]                 # (B, T)
    flux_vel = h3_features[_FLUX_VEL_H14]                 # (B, T)
    onset_val = h3_features[_ONSET_VAL_H10]               # (B, T)
    roughness_val = h3_features[_ROUGHNESS_VAL_H10]       # (B, T)
    roughness_mean = h3_features[_ROUGHNESS_MEAN_H14]     # (B, T)
    inhar_val = h3_features[_INHARMONICITY_VAL_H10]       # (B, T)
    inhar_vel = h3_features[_INHARMONICITY_VEL_H14]       # (B, T)

    # -- R3 features --
    roughness_r3 = r3_features[..., _ROUGHNESS]           # (B, T)
    inhar_r3 = r3_features[..., _INHARMONICITY]           # (B, T)
    flux_r3 = r3_features[..., _SPECTRAL_FLUX]            # (B, T)
    entropy_r3 = r3_features[..., _ENTROPY]               # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END] # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END] # (B, T, 8)

    # -- PNH relay (graceful fallback) --
    pnh = relay_outputs.get("PNH", torch.zeros(B, T, 11, device=device))
    harmony = pnh.mean(dim=-1)                            # (B, T)

    # -- Derived signals --
    pred_error = 0.50 * flux_vel + 0.50 * inhar_vel       # (B, T)

    # -- P0: ERAN Response --
    # Long-term syntax violation. Entropy proxies unpredictability,
    # harmony.mean() reflects tonal context, x_l5l7.mean() captures
    # high-level syntax template (consonance-timbre interactions).
    # Koelsch 2000: ERAN at 150-180 ms, right-frontal maximum.
    # f13 = sigma(0.30 * entropy * harmony.mean * x_l5l7.mean)
    p0 = torch.sigmoid(
        0.30 * entropy_r3 * harmony * x_l5l7.mean(dim=-1)
    )

    # -- P1: MMN Response --
    # Short-term deviance detection. Spectral flux as change magnitude,
    # prediction error from synthesis, x_l0l5 as sensory comparison.
    # Wagner et al. 2018: MMN for harmonic interval deviants.
    # f14 = sigma(0.30 * flux * pred_error.mean * x_l0l5.mean)
    p1 = torch.sigmoid(
        0.30 * flux_r3 * pred_error * x_l0l5.mean(dim=-1)
    )

    # -- P2: Combined Prediction Error --
    # Integrated PE weighted by dissonance (roughness + inharmonicity).
    # Bonetti et al. 2024: hierarchical PE auditory cortex -> hippocampus.
    # f15 = sigma(0.40 * pred_error.mean * (roughness + inharmonicity) / 2)
    p2 = torch.sigmoid(
        0.40 * pred_error * (roughness_r3 + inhar_r3) / 2.0
    )

    return p0, p1, p2
