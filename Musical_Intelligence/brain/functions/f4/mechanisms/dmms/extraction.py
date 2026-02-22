"""DMMS E-Layer -- Extraction (3D).

Three explicit features modeling early developmental music-memory scaffolding:

  E0: early_binding       -- Neonatal music-emotion scaffold strength [0, 1]
  E1: dev_plasticity      -- Critical period formation index [0, 1]
  E2: melodic_imprint     -- Early melodic memory template strength [0, 1]

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2          -- binding coherence at 1s
    (4, 16, 0, 2)   sensory_pleasantness value H16 L2  -- comfort signal
    (12, 16, 0, 2)  warmth value H16 L2                -- caregiver voice proxy
    (14, 16, 0, 2)  tonalness value H16 L2             -- melodic recognition
    (0, 16, 0, 2)   roughness value H16 L2             -- dissonance (inverted)
    (22, 16, 0, 2)  entropy value H16 L2               -- pattern complexity

R3 consumed:
    [0]      roughness              -- E0: consonance proxy (1 - roughness)
    [3]      stumpf_fusion          -- E0: tonal binding coherence
    [4]      sensory_pleasantness   -- E0: comfort/safety association
    [12]     warmth                 -- E0+E2: caregiver voice proxy
    [14]     tonalness              -- E2: melodic recognition template
    [22]     entropy                -- E1: pattern complexity gating
    [25:33]  x_l0l5                 -- E1: salience-binding scaffold
    [41:49]  x_l5l7                 -- E2: familiarity template

See Building/C3-Brain/F4-Memory-Systems/mechanisms/dmms/DMMS-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_1S = (3, 16, 1, 2)         # stumpf_fusion mean H16 L2
_PLEAS_VAL_1S = (4, 16, 0, 2)           # sensory_pleasantness value H16 L2
_WARMTH_VAL_1S = (12, 16, 0, 2)         # warmth value H16 L2
_TONAL_VAL_1S = (14, 16, 0, 2)          # tonalness value H16 L2
_ROUGH_VAL_1S = (0, 16, 0, 2)           # roughness value H16 L2
_ENTROPY_VAL_1S = (22, 16, 0, 2)        # entropy value H16 L2

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_WARMTH = 12
_TONALNESS = 14
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    E0 (early_binding) models neonatal music-emotion scaffold strength.
    Hippocampus + Amygdala pairing driven by consonance (inverse roughness),
    caregiver voice warmth, and tonal binding coherence.
    Partanen 2022: parental singing enhances auditory processing in preterm
    infants (MEG RCT, N=33, eta2=0.229).

    E1 (dev_plasticity) models the critical period formation index.
    mPFC + Auditory cortex plasticity driven by encoding strength,
    salience-binding (x_l0l5), and low entropy (simple patterns scaffold first).
    Qiu 2025: fetal-infant music exposure enhances mPFC/amygdala dendritic
    complexity (mouse, N=48, r=0.38).

    E2 (melodic_imprint) models early melodic memory template strength.
    Auditory cortex + Hippocampus imprinting driven by consonance-timbre
    interaction (x_l5l7) multiplied by tonalness, plus warmth as caregiver
    voice proxy and familiarity from H3 mean signals.
    Trehub 2003: infants prefer consonance, show enhanced processing of
    infant-directed singing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]      # (B, T)
    pleas_val_1s = h3_features[_PLEAS_VAL_1S]           # (B, T)
    warmth_val_1s = h3_features[_WARMTH_VAL_1S]         # (B, T)
    tonal_val_1s = h3_features[_TONAL_VAL_1S]           # (B, T)
    rough_val_1s = h3_features[_ROUGH_VAL_1S]           # (B, T)
    entropy_val_1s = h3_features[_ENTROPY_VAL_1S]       # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]            # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]           # (B, T)
    sensory_pleas = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    warmth = r3_features[..., _WARMTH]                  # (B, T)
    tonalness = r3_features[..., _TONALNESS]            # (B, T)
    entropy = r3_features[..., _ENTROPY]                # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals --
    consonance = 1.0 - roughness                        # (B, T)
    encoding_mean = 0.50 * stumpf_mean_1s + 0.50 * pleas_val_1s  # (B, T)

    # E0: Early Binding -- neonatal music-emotion scaffold
    # Partanen 2022: parental singing -> auditory processing enhancement
    # f37 = sigma(0.35 * (1 - roughness) * warmth
    #           + 0.35 * stumpf * encoding.mean
    #           + 0.30 * sensory_pleasantness)
    e0 = torch.sigmoid(
        0.35 * consonance * warmth
        + 0.35 * stumpf * encoding_mean
        + 0.30 * sensory_pleas
    )

    # E1: Developmental Plasticity -- critical period formation
    # Qiu 2025: dose-dependent mPFC/amygdala plasticity
    # f38 = sigma(0.40 * encoding.mean + 0.30 * x_l0l5.mean
    #           + 0.30 * (1 - entropy))
    e1 = torch.sigmoid(
        0.40 * encoding_mean
        + 0.30 * x_l0l5.mean(dim=-1)
        + 0.30 * (1.0 - entropy)
    )

    # E2: Melodic Imprint -- early melodic memory template
    # Trehub 2003: innate melodic contour sensitivity
    # f39 = sigma(0.40 * x_l5l7.mean * tonalness
    #           + 0.30 * familiarity.mean
    #           + 0.30 * warmth)
    # familiarity.mean approximated by warmth_val_1s (sustained warmth signal)
    e2 = torch.sigmoid(
        0.40 * x_l5l7.mean(dim=-1) * tonalness
        + 0.30 * warmth_val_1s
        + 0.30 * warmth
    )

    return e0, e1, e2
