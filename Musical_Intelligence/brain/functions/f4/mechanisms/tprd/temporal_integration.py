"""TPRD M-Layer -- Temporal Integration (2D).

Two composite signals capturing dissociation dynamics and spectral-pitch coherence:

  M0: dissociation_index    -- Normalized tonotopic-pitch dissociation [0, 1]
  M1: spectral_pitch_ratio  -- Spectral-to-pitch coherence ratio [0, 1]

M0 computes a contrast ratio between tonotopic (T0) and pitch (T1)
encoding strengths, remapped from [-1, 1] to [0, 1]. 0.5 = balanced,
0 = pitch dominant (nonprimary HG), 1 = tonotopic dominant (primary HG).

M1 quantifies spectral-pitch coherence using tonalness and spectral
autocorrelation periodicity, supported by brainstem FFR consonance
correspondence (Bidelman 2013: r >= 0.81).

H3 consumed:
    (0, 14, 1, 0)    roughness mean H14 L0            -- avg tonotopic load (700ms)
    (5, 14, 1, 0)    inharmonicity mean H14 L0        -- avg conflict (700ms)
    (3, 6, 1, 0)     stumpf_fusion mean H6 L0         -- beat-level fusion (200ms)
    (14, 6, 1, 0)    tonalness mean H6 L0             -- beat-level pitch clarity (200ms)
    (17, 6, 14, 0)   spectral_autocorrelation period H6 L0 -- beat-level harmonic periodicity
    (22, 14, 1, 0)   entropy mean H14 L0              -- avg spectral complexity (700ms)

R3 consumed:
    [0]   roughness                -- M0: tonotopic component
    [5]   inharmonicity            -- M0: spectral-pitch conflict
    [14]  tonalness                -- M0+M1: pitch clarity
    [17]  spectral_autocorrelation -- M1: harmonic periodicity
    [22]  entropy                  -- M0: spectral complexity modulation

See Building/C3-Brain/F4-Memory-Systems/mechanisms/tprd/TPRD-temporal-integration.md
Briley 2013: medial-lateral gradient in HG.
Bidelman 2013: brainstem FFR consonance hierarchy (r >= 0.81).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_MEAN_700MS = (0, 14, 1, 0)
_INHARM_MEAN_700MS = (5, 14, 1, 0)
_FUSION_MEAN_200MS = (3, 6, 1, 0)
_TONAL_MEAN_200MS = (14, 6, 1, 0)
_SPEC_AUTOCORR_PERIOD_200MS = (17, 6, 14, 0)
_ENTROPY_MEAN_700MS = (22, 14, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARMONICITY = 5
_TONALNESS = 14
_SPECTRAL_AUTOCORR = 17
_ENTROPY = 22

# -- Constants -----------------------------------------------------------------
_EPS = 1e-7


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    t: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from T-layer + H3/R3.

    M0 (dissociation_index) captures the medial-lateral gradient in
    Heschl's gyrus as a continuous value. The contrast ratio
    (tonotopic - pitch) / (tonotopic + pitch + eps) is remapped from
    [-1, 1] to [0, 1]. This operationalizes the core finding of
    Briley 2013: tonotopy (medial) to pitch (anterolateral) gradient.

    M1 (spectral_pitch_ratio) measures coherence between physical
    spectral content and perceived pitch. Uses tonalness and spectral
    autocorrelation periodicity at beat level (H6, 200ms) to assess
    how well F0 extraction aligns with spectral structure.
    Bidelman 2013: subcortical pitch salience predicts consonance
    (r >= 0.81).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        t: ``(T0, T1, T2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    t0, t1, _t2 = t

    # -- R3 slices -------------------------------------------------------------
    tonalness = r3_features[..., _TONALNESS]             # (B, T)
    spectral_autocorr = r3_features[..., _SPECTRAL_AUTOCORR]  # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    tonal_mean_200ms = h3_features[_TONAL_MEAN_200MS]           # (B, T)
    spec_autocorr_period = h3_features[_SPEC_AUTOCORR_PERIOD_200MS]  # (B, T)
    fusion_mean_200ms = h3_features[_FUSION_MEAN_200MS]         # (B, T)

    # -- M0: Dissociation Index ------------------------------------------------
    # Contrast ratio: (tonotopic - pitch) / (tonotopic + pitch + eps)
    # Remapped from [-1, 1] to [0, 1]: idx = (raw + 1) / 2
    # 0.0 = pure pitch dominant, 0.5 = balanced, 1.0 = pure tonotopic
    # Briley 2013: medial HG (tonotopic) vs anterolateral HG (pitch).
    idx_raw = (t0 - t1) / (t0 + t1 + _EPS)
    m0 = (idx_raw + 1.0) / 2.0  # (B, T), already in [0, 1]

    # -- M1: Spectral-Pitch Ratio ---------------------------------------------
    # Coherence between physical spectral content and perceived pitch.
    # Uses beat-level (H6) tonalness and spectral autocorrelation
    # periodicity plus fusion quality for pitch stability context.
    # Bidelman 2013: brainstem FFR encodes consonance hierarchy.
    m1 = torch.sigmoid(
        0.35 * tonal_mean_200ms * spectral_autocorr
        + 0.35 * spec_autocorr_period * tonalness
        + 0.30 * fusion_mean_200ms
    )

    return m0, m1
