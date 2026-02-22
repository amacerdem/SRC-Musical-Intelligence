"""TPRD P-Layer -- Cognitive Present (2D).

Two present-processing dimensions for tonotopic and pitch activation states:

  P0: tonotopic_state  -- Current tonotopic activation in primary HG [0, 1]
  P1: pitch_state      -- Current pitch representation in nonprimary HG [0, 1]

P0 captures instantaneous tonotopic (frequency-map) processing strength
using harmonic context modulated by roughness. P1 captures instantaneous
pitch (F0) representation strength using pitch salience modulated by
tonalness.

H3 consumed:
    (0, 10, 0, 2)    roughness value H10 L2            -- current tonotopic beating
    (14, 0, 0, 2)    tonalness value H0 L2             -- immediate pitch salience
    (14, 3, 1, 2)    tonalness mean H3 L2              -- brainstem pitch salience
    (3, 0, 0, 2)     stumpf_fusion value H0 L2         -- immediate fusion quality
    (22, 6, 0, 0)    entropy value H6 L0               -- spectral complexity (beat)

R3 consumed:
    [0]   roughness   -- P0: tonotopic activation driver
    [14]  tonalness   -- P1: pitch clarity for pitch_state
    [22]  entropy     -- P0: spectral complexity context

See Building/C3-Brain/F4-Memory-Systems/mechanisms/tprd/TPRD-cognitive-present.md
Fishman 2001: A1/HG phase-locked activity correlates with dissonance.
Briley 2013: anterolateral HG encodes pitch chroma.
Norman-Haignere 2013: pitch regions driven by resolved harmonics.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_VAL_400MS = (0, 10, 0, 2)
_TONAL_VAL_COCHLEAR = (14, 0, 0, 2)
_TONAL_MEAN_BRAINSTEM = (14, 3, 1, 2)
_FUSION_VAL_COCHLEAR = (3, 0, 0, 2)
_ENTROPY_VAL_200MS = (22, 6, 0, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_TONALNESS = 14
_ENTROPY = 22


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    t: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present processing from H3/R3 + T/M outputs.

    P0 (tonotopic_state) provides a real-time readout of tonotopic
    processing engagement. The product of harmonic context (fusion and
    entropy as proxy for spectral richness) and roughness captures
    co-occurrence of spectral complexity and beating. High roughness
    during spectrally rich contexts indicates heavy tonotopic map
    activation. Fishman 2001: A1/HG phase-locked activity correlates
    with perceived dissonance.

    P1 (pitch_state) provides a real-time readout of pitch
    representation strength. Pitch salience (averaged across cochlear
    and brainstem horizons) modulated by tonalness captures F0
    extraction clarity. Briley 2013: anterolateral HG pitch chroma.
    Norman-Haignere 2013: resolved-harmonic preference.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        t: ``(T0, T1, T2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1)`` each ``(B, T)``.
    """
    _t0, _t1, _t2 = t
    _m0, _m1 = m

    # -- R3 slices -------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]   # (B, T)
    tonalness = r3_features[..., _TONALNESS]   # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    roughness_val = h3_features[_ROUGHNESS_VAL_400MS]    # (B, T)
    tonal_cochlear = h3_features[_TONAL_VAL_COCHLEAR]    # (B, T)
    tonal_brainstem = h3_features[_TONAL_MEAN_BRAINSTEM]  # (B, T)
    fusion_cochlear = h3_features[_FUSION_VAL_COCHLEAR]  # (B, T)
    entropy_val = h3_features[_ENTROPY_VAL_200MS]        # (B, T)

    # -- Derived signals -------------------------------------------------------
    # Harmonic context proxy: fusion quality and spectral complexity
    harmony = 0.50 * fusion_cochlear + 0.50 * entropy_val  # (B, T)

    # Pitch salience: average of cochlear and brainstem tonalness
    pitch_sal = 0.50 * tonal_cochlear + 0.50 * tonal_brainstem  # (B, T)

    # -- P0: Tonotopic State ---------------------------------------------------
    # tonotopic_state = clamp(harmony * roughness, 0, 1)
    # Fishman 2001: A1/HG phase-locked activity correlates with dissonance.
    # When spectral context is rich (harmony high) and beating is strong
    # (roughness high), tonotopic processing dominates.
    p0 = (harmony * roughness).clamp(0.0, 1.0)

    # -- P1: Pitch State -------------------------------------------------------
    # pitch_state = clamp(pitch_sal * tonalness, 0, 1)
    # Briley 2013: anterolateral HG encodes pitch chroma.
    # When pitch salience is strong and tonalness is high, pitch
    # representation (F0 extraction) dominates.
    p1 = (pitch_sal * tonalness).clamp(0.0, 1.0)

    return p0, p1
