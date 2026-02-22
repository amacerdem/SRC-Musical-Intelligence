"""MEAMN E-Layer -- Extraction (3D).

Three explicit features modeling autobiographical memory retrieval:

  E0: f01_retrieval           -- Autobiographical retrieval activation [0, 1]
  E1: f02_nostalgia           -- Nostalgia response intensity [0, 1]
  E2: f03_emotion             -- Emotional memory coloring [0, 1]

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2      -- binding stability at 1s
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0      -- binding over 5s consolidation
    (12, 16, 0, 2)  warmth value H16 L2             -- current timbre warmth
    (12, 20, 1, 0)  warmth mean H20 L0              -- sustained warmth = nostalgia
    (0, 16, 0, 2)   roughness value H16 L2          -- current dissonance
    (0, 20, 18, 0)  roughness trend H20 L0          -- dissonance trajectory
    (10, 16, 0, 2)  loudness value H16 L2           -- current arousal

R3 consumed:
    [0]      roughness      -- E2: valence proxy (inverse)
    [3]      stumpf_fusion  -- E0: binding integrity
    [10]     loudness       -- E2: arousal correlate
    [12]     warmth         -- E1: nostalgia trigger
    [25:33]  x_l0l5         -- E0: memory retrieval binding
    [41:49]  x_l5l7         -- E1: nostalgia warmth signal

See Building/C3-Brain/F4-Memory-Systems/mechanisms/meamn/MEAMN-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_1S = (3, 16, 1, 2)
_STUMPF_MEAN_5S = (3, 20, 1, 0)
_WARMTH_VAL_1S = (12, 16, 0, 2)
_WARMTH_MEAN_5S = (12, 20, 1, 0)
_ROUGH_VAL_1S = (0, 16, 0, 2)
_ROUGH_TREND_5S = (0, 20, 18, 0)
_LOUD_VAL_1S = (10, 16, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_LOUDNESS = 10
_WARMTH = 12
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 features --
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]
    stumpf_mean_5s = h3_features[_STUMPF_MEAN_5S]
    warmth_val_1s = h3_features[_WARMTH_VAL_1S]
    warmth_mean_5s = h3_features[_WARMTH_MEAN_5S]
    rough_val_1s = h3_features[_ROUGH_VAL_1S]
    rough_trend_5s = h3_features[_ROUGH_TREND_5S]
    loud_val_1s = h3_features[_LOUD_VAL_1S]

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]       # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)
    roughness = r3_features[..., _ROUGHNESS]         # (B, T)
    loudness = r3_features[..., _LOUDNESS]           # (B, T)

    # -- Derived signals --
    retrieval = 0.50 * stumpf_mean_1s + 0.50 * stumpf_mean_5s
    familiarity_proxy = 0.50 * warmth_val_1s + 0.50 * warmth_mean_5s
    arousal = torch.sigmoid(loudness * loud_val_1s)
    valence = 1.0 - roughness

    # E0: Autobiographical retrieval -- hippocampus + mPFC + PCC hub
    # Janata 2009: dorsal MPFC tracks tonal space movement during
    # autobiographically salient songs (t(9)=5.784, p<0.0003)
    # f01 = sigma(0.80 * x_l0l5.mean * retrieval * stumpf)
    e0 = torch.sigmoid(
        0.80 * x_l0l5.mean(dim=-1) * retrieval * stumpf
    )

    # E1: Nostalgia response -- hippocampus + STG melodic trace
    # Sakakibara 2025: acoustic similarity triggers nostalgia (eta_p^2=0.636)
    # f02 = sigma(0.70 * x_l5l7.mean * familiarity)
    e1 = torch.sigmoid(
        0.70 * x_l5l7.mean(dim=-1) * familiarity_proxy
    )

    # E2: Emotional memory coloring -- amygdala affective tagging
    # Context-dependent study 2021: multimodal integration in STS and
    # hippocampus (d=0.17, p<0.0001)
    # f03 = sigma(0.60 * (1-roughness) * loudness * arousal)
    e2 = torch.sigmoid(
        0.60 * valence * loudness * arousal
    )

    return e0, e1, e2
