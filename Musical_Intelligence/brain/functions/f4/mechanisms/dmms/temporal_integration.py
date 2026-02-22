"""DMMS M-Layer -- Temporal Integration (2D).

Two composite signals integrating E-layer with long-horizon temporal context:

  M0: scaffold_strength   -- Overall scaffold formation/activation [0, 1]
  M1: imprinting_depth    -- Depth of melodic imprinting into scaffold [0, 1]

H3 consumed:
    (3, 24, 1, 0)   stumpf_fusion mean H24 L0          -- long-term binding at 36s
    (4, 20, 1, 0)   sensory_pleasantness mean H20 L0   -- sustained pleasantness 5s
    (14, 20, 1, 0)  tonalness mean H20 L0              -- tonal stability 5s
    (12, 20, 1, 0)  warmth mean H20 L0                 -- sustained warmth 5s
    (0, 20, 1, 0)   roughness mean H20 L0              -- consonance scaffold 5s

See Building/C3-Brain/F4-Memory-Systems/mechanisms/dmms/DMMS-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_36S = (3, 24, 1, 0)        # stumpf_fusion mean H24 L0
_PLEAS_MEAN_5S = (4, 20, 1, 0)          # sensory_pleasantness mean H20 L0
_TONAL_MEAN_5S = (14, 20, 1, 0)         # tonalness mean H20 L0
_WARMTH_MEAN_5S = (12, 20, 1, 0)        # warmth mean H20 L0
_ROUGH_MEAN_5S = (0, 20, 1, 0)          # roughness mean H20 L0

# -- R3 indices (reused from extraction for derived signals) -------------------
_STUMPF_FUSION = 3
_TONALNESS = 14
_WARMTH = 12
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer + H3/R3.

    Mathematical formulation:
        binding_coherence = stumpf[3] * consonance
        imprint_depth_raw = x_l5l7.mean() * tonalness[14]
        scaffold_strength = clamp(encoding * binding_coherence
                                  + familiarity * imprint_depth_raw, 0, 1)
        imprinting_depth = sigma(0.35 * familiarity + 0.35 * tonalness
                                 + 0.30 * warmth)

    Strait 2012: early musical training enhances subcortical speech encoding
    (ABR, N=31, r=0.562-0.629).
    Trainor & Unrau 2012: musical training before age 7 enhances auditory
    processing; experience-dependent development.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, _e2 = e_outputs

    # -- H3 features --
    stumpf_mean_36s = h3_features[_STUMPF_MEAN_36S]     # (B, T)
    pleas_mean_5s = h3_features[_PLEAS_MEAN_5S]         # (B, T)
    tonal_mean_5s = h3_features[_TONAL_MEAN_5S]         # (B, T)
    warmth_mean_5s = h3_features[_WARMTH_MEAN_5S]       # (B, T)
    rough_mean_5s = h3_features[_ROUGH_MEAN_5S]         # (B, T)

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]            # (B, T)
    tonalness = r3_features[..., _TONALNESS]             # (B, T)
    warmth = r3_features[..., _WARMTH]                   # (B, T)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals --
    consonance_5s = 1.0 - rough_mean_5s                  # (B, T)
    encoding = 0.50 * pleas_mean_5s + 0.50 * stumpf_mean_36s  # (B, T)

    # Familiarity proxy from warmth + tonalness stability over 5s
    familiarity = torch.sigmoid(
        0.50 * warmth_mean_5s + 0.50 * tonal_mean_5s
    )

    # M0: Scaffold Strength -- multiplicative binding model
    # Strait 2012: encoding * binding_coherence + familiarity * imprint_depth
    binding_coherence = stumpf * consonance_5s            # (B, T)
    imprint_depth_raw = x_l5l7.mean(dim=-1) * tonalness   # (B, T)
    m0 = (encoding * binding_coherence
           + familiarity * imprint_depth_raw).clamp(0.0, 1.0)

    # M1: Imprinting Depth -- how deeply melodic patterns are imprinted
    # Trainor & Unrau 2012: familiar + tonal + warm = deep imprinting
    # sigma(0.35 * familiarity + 0.35 * tonalness + 0.30 * warmth)
    m1 = torch.sigmoid(
        0.35 * familiarity + 0.35 * tonalness + 0.30 * warmth
    )

    return m0, m1
