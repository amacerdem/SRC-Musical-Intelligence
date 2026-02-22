"""CSSL E-Layer -- Extraction (3D).

Three explicit features modeling cross-species song learning mechanisms:

  E0: rhythm_copying           -- Motor-auditory rhythm entrainment strength [0, 1]
  E1: melody_copying           -- Melodic template matching strength [0, 1]
  E2: all_shared_binding       -- Complete melody-rhythm binding [0, 1]

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2       -- binding stability at beat level
    (6, 16, 0, 2)   pitch_strength value H16 L2     -- current pitch clarity
    (11, 16, 0, 2)  onset_strength value H16 L2     -- current rhythm boundary
    (14, 16, 0, 2)  tonalness value H16 L2          -- current tonal purity
    (22, 16, 0, 2)  entropy value H16 L2            -- current pattern complexity
    (12, 16, 0, 2)  warmth value H16 L2             -- current voice quality

R3 consumed:
    [0]  roughness          -- consonance component of binding
    [1]  sethares_dissonance -- harmonic structure quality
    [3]  stumpf_fusion      -- tonal fusion = binding strength
    [5]  harmonicity        -- harmonic-to-noise ratio = song purity
    [6]  pitch_strength     -- pitch clarity for melody template
    [7]  amplitude          -- vocal intensity / energy level
    [11] onset_strength     -- rhythm boundary marker
    [14] tonalness          -- tonal purity for melody matching
    [22] entropy            -- pattern complexity / familiarity
    [25:33] x_l0l5          -- motor-auditory coupling for rhythm
    [41:49] x_l5l7          -- melody-timbre binding for song template

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cssl/CSSL-extraction.md
Burchardt et al. 2025: r=0.88 overall IOI beat correlation (N=54).
Bolhuis & Moorman 2015: HVC-Broca neural homology for song timing.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_H16_L2 = (3, 16, 1, 2)     # stumpf_fusion mean H16 L2
_PITCH_VAL_H16_L2 = (6, 16, 0, 2)       # pitch_strength value H16 L2
_ONSET_VAL_H16_L2 = (11, 16, 0, 2)      # onset_strength value H16 L2
_TONAL_VAL_H16_L2 = (14, 16, 0, 2)      # tonalness value H16 L2
_ENTROPY_VAL_H16_L2 = (22, 16, 0, 2)    # entropy value H16 L2
_WARMTH_VAL_H16_L2 = (12, 16, 0, 2)     # warmth value H16 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_STUMPF = 3
_HARMONICITY = 5
_PITCH_STRENGTH = 6
_AMPLITUDE = 7
_ONSET_STRENGTH = 11
_TONALNESS = 14
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features + upstream.

    Extracts rhythm_copying, melody_copying, and all_shared_binding signals
    that model the cross-species song learning pathway.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: Dict mapping nucleus NAME -> routable output tensor.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    # -- H3 reads --
    onset_val = h3_features[_ONSET_VAL_H16_L2]        # (B, T)
    stumpf_mean = h3_features[_STUMPF_MEAN_H16_L2]    # (B, T)
    tonal_val = h3_features[_TONAL_VAL_H16_L2]        # (B, T)
    pitch_val = h3_features[_PITCH_VAL_H16_L2]        # (B, T)

    # -- R3 reads --
    stumpf = r3_features[..., _STUMPF]                 # (B, T)
    pitch_strength = r3_features[..., _PITCH_STRENGTH]  # (B, T)
    onset_strength = r3_features[..., _ONSET_STRENGTH]  # (B, T)
    tonalness = r3_features[..., _TONALNESS]            # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                  # (B, T)
    x_l5l7_mean = x_l5l7.mean(dim=-1)                  # (B, T)

    # -- Upstream: aggregate retrieval and familiarity proxies --
    # Graceful degradation: if no upstream available, use H3-only path
    retrieval_mean = torch.zeros_like(onset_val)
    familiarity_mean = torch.zeros_like(onset_val)
    n_upstream = 0
    for name, out in upstream_outputs.items():
        retrieval_mean = retrieval_mean + out.mean(dim=-1)
        familiarity_mean = familiarity_mean + out.mean(dim=-1)
        n_upstream += 1
    if n_upstream > 0:
        retrieval_mean = retrieval_mean / n_upstream
        familiarity_mean = familiarity_mean / n_upstream

    # -- Encoding proxy from H3 --
    encoding_mean = (stumpf_mean + tonal_val + pitch_val) / 3.0  # (B, T)

    # E0: Rhythm copying -- motor-auditory rhythm entrainment
    # Burchardt et al. 2025: r=0.88 overall IOI beat correlation (N=54)
    # Basal ganglia / Area X motor loop
    e0 = torch.sigmoid(
        0.30 * x_l0l5_mean
        + 0.30 * onset_strength * encoding_mean
        + 0.30 * retrieval_mean
        + 0.10 * onset_val
    )

    # E1: Melody copying -- melodic template matching strength
    # Bolhuis & Moorman 2015: HVC-Broca neural homology for song timing
    e1 = torch.sigmoid(
        0.35 * stumpf * tonalness
        + 0.35 * familiarity_mean
        + 0.30 * pitch_strength
    )

    # E2: All-shared binding -- complete melody-rhythm binding
    # Burchardt et al. 2025: r=0.94 all-shared element correlation (N=54)
    # Hippocampal sequential binding
    e2 = torch.sigmoid(
        0.40 * x_l5l7_mean * familiarity_mean
        + 0.30 * e0
        + 0.30 * e1
    )

    return e0, e1, e2
