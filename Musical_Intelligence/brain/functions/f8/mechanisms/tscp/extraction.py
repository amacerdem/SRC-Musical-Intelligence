"""TSCP E-Layer -- Extraction (3D).

Timbre-Specific Cortical Plasticity extraction signals:
  f01: trained_timbre_response   -- Trained instrument cortical enhancement [0, 1]
  f02: timbre_specificity        -- Selectivity for trained vs untrained timbre [0, 1]
  f03: plasticity_magnitude      -- Degree of cortical reorganization [0, 1]

f01 captures the N1m amplitude enhancement for a trained instrument timbre based
on tristimulus balance (harmonic envelope signature) and harmonic purity
((1-inharmonicity) * tonalness). Pantev et al. 2001: timbre-specific N1m
enhancement with double dissociation F(1,15)=28.55, p=.00008.

f02 captures the selectivity of cortical enhancement for the trained instrument
relative to untrained instruments. Spectral contrast (warmth * sharpness_inv)
combined with tonalness stability and consonance-timbre coupling. Pantev 2001:
age-of-inception r=-0.634, p=.026.

f03 captures the degree of cortical reorganization as a training effect size
proxy. Interaction of f01 with timbre flux variability. Santoyo et al. 2023:
enhanced theta phase-locking for timbre-based streams. Whiteford et al. 2025:
plasticity locus is cortical not subcortical (d=-0.064, BF=0.13).

H3 demands consumed (6 tuples):
  (18,  2, 0, 2)  tristimulus1 value H2 L2     -- F0 energy at 17ms
  (19,  2, 0, 2)  tristimulus2 value H2 L2     -- mid-harmonic energy at 17ms
  (20,  2, 0, 2)  tristimulus3 value H2 L2     -- high-harmonic energy at 17ms
  ( 5,  5, 0, 2)  inharmonicity value H5 L2    -- inharmonicity at 46ms
  (14,  8, 19, 0) tonalness stability H8 L0    -- tonalness stability 300ms
  (24,  8,  3, 0) timbre_change std H8 L0      -- timbre flux variability 300ms

R3 features:
  [18:21] tristimulus1/2/3 (harmonic envelope)
  [5]     inharmonicity (instrument character)
  [14]    tonalness (harmonic-to-noise ratio)
  [12]    warmth (low-frequency spectral balance)
  [13]    sharpness (high-frequency energy)
  [41:47] x_l5l7 (consonance-timbre coupling)
  [24]    timbre_change (temporal timbre flux)

Upstream reads:
  EDNR relay -- upstream relay for learning context

Pantev et al. 2001: timbre-specific N1m enhancement (MEG, N=16).
Santoyo et al. 2023: theta phase-locking for timbre streams (EEG).
Whiteford et al. 2025: cortical vs subcortical plasticity (fMRI).
Bellmann & Asano 2024: ALE meta-analysis of timbre processing (k=18, N=338).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/tscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (6 tuples) ----------------------------------------------
_TRIST1_VALUE_H2 = (18, 2, 0, 2)       # tristimulus1 value H2 L2
_TRIST2_VALUE_H2 = (19, 2, 0, 2)       # tristimulus2 value H2 L2
_TRIST3_VALUE_H2 = (20, 2, 0, 2)       # tristimulus3 value H2 L2
_INHARM_VALUE_H5 = (5, 5, 0, 2)        # inharmonicity value H5 L2
_TONALNESS_STAB_H8 = (14, 8, 19, 0)    # tonalness stability H8 L0
_TIMBRE_STD_H8 = (24, 8, 3, 0)         # timbre_change std H8 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_INHARMONICITY = 5
_WARMTH = 12
_SHARPNESS = 13
_TONALNESS = 14
_X_L5L7_START = 41
_X_L5L7_END = 47


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    ednr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: timbre-specific cortical plasticity extraction signals.

    f01 (trained_timbre_response): Tristimulus balance (1 - std of
    tristimulus1/2/3) combined with harmonic purity ((1-inharmonicity) *
    tonalness). High f01 indicates a stimulus with clear, stable harmonic
    structure matching a trained instrument template. Maps to secondary
    auditory cortex (Pantev 2001: ECD posterior/lateral to HG).

    f02 (timbre_specificity): Spectral contrast via warmth * sharpness_inv,
    tonalness stability at 300ms, and consonance-timbre coupling (x_l5l7
    mean). Captures the selectivity of cortical enhancement for the trained
    timbre. Maps to Planum Temporale (Bellmann & Asano 2024: ALE cluster
    R-pSTG/PT, 3128 mm3).

    f03 (plasticity_magnitude): Interaction of f01 with timbre change
    variability (H3 std of timbre_change at 300ms). Novel or varying timbres
    trigger greater plasticity-related activation. Maps to bilateral
    pSTG/HG (Bellmann & Asano 2024: ALE meta-analysis, k=18, N=338).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        ednr: ``(B, T, 10)`` from upstream EDNR relay.

    Returns:
        ``(f01, f02, f03)`` each ``(B, T)``
    """
    # -- H3 features --
    trist1 = h3_features[_TRIST1_VALUE_H2]          # (B, T)
    trist2 = h3_features[_TRIST2_VALUE_H2]          # (B, T)
    trist3 = h3_features[_TRIST3_VALUE_H2]          # (B, T)
    inharm = h3_features[_INHARM_VALUE_H5]           # (B, T)
    tonalness_stab = h3_features[_TONALNESS_STAB_H8] # (B, T)
    timbre_std = h3_features[_TIMBRE_STD_H8]         # (B, T)

    # -- R3 features --
    tonalness = r3_features[..., _TONALNESS]         # (B, T)
    warmth = r3_features[..., _WARMTH]               # (B, T)
    sharpness = r3_features[..., _SHARPNESS]         # (B, T)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 6)
    x_l5l7_mean = x_l5l7.mean(dim=-1)               # (B, T)

    # -- Tristimulus balance: 1 - std(tristimulus1, tristimulus2, tristimulus3) --
    trist_stack = torch.stack([trist1, trist2, trist3], dim=-1)  # (B, T, 3)
    trist_balance = (1.0 - trist_stack.std(dim=-1)).clamp(0.0, 1.0)  # (B, T)

    # -- Harmonic purity: (1 - inharmonicity) * tonalness --
    harmonic_purity = (1.0 - inharm.clamp(0.0, 1.0)) * tonalness.clamp(0.0, 1.0)

    # -- f01: Trained Timbre Response --
    # sigma(0.35 * trist_balance + 0.35 * (1-inharmonicity) * tonalness)
    # Pantev 2001: timbre-specific N1m, F(1,15)=28.55, p=.00008
    f01 = torch.sigmoid(
        0.35 * trist_balance
        + 0.35 * harmonic_purity
    )

    # -- Sharpness inverse for spectral contrast --
    sharpness_inv = (1.0 - sharpness.clamp(0.0, 1.0))

    # -- Timbre stability from tonalness stability H3 --
    timbre_stability = tonalness_stab.clamp(0.0, 1.0)

    # -- f02: Timbre Specificity --
    # sigma(0.40 * warmth * sharpness_inv + 0.30 * timbre_stability + 0.30 * x_l5l7_mean)
    # Pantev 2001: age-of-inception r=-0.634, p=.026
    f02 = torch.sigmoid(
        0.40 * warmth.clamp(0.0, 1.0) * sharpness_inv
        + 0.30 * timbre_stability
        + 0.30 * x_l5l7_mean.clamp(0.0, 1.0)
    )

    # -- f03: Plasticity Magnitude --
    # sigma(0.50 * f01 * timbre_change_std)
    # Santoyo 2023: enhanced theta phase-locking for timbre streams
    # Whiteford 2025: cortical plasticity (d=-0.064, BF=0.13)
    f03 = torch.sigmoid(
        0.50 * f01 * timbre_std.clamp(0.0, 1.0)
    )

    return f01, f02, f03
