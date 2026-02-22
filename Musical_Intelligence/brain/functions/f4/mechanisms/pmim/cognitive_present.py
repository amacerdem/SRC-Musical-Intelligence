"""PMIM S-Layer -- Cognitive Present / State (3D).

Three present-state dimensions for memory-prediction interaction:

  S0: syntax_state     -- Current harmonic syntax processing state [0, 1]
  S1: deviance_state   -- Current deviance detection activation [0, 1]
  S2: memory_update    -- Memory updating rate [0, 1]

Syntax state (S0) tracks the degree to which the current harmonic
environment conforms to stored syntactic rules. Deviance state (S1)
reflects real-time mismatch between predicted and actual input across
both ERAN and MMN systems. Memory update (S2) captures how strongly
current prediction errors drive model revision in hippocampus and mPFC.

H3 demands consumed (3 tuples):
  roughness:              (0,18,18,0)   trend H18 L0          -- dissonance trajectory
  sensory_pleasantness:   (4,18,19,0)   stability H18 L0      -- consonance stability
  loudness:               (10,10,0,2)   value H10 L2          -- current intensity

R3 consumed:
  [0]  roughness            -- S0: dissonance in current syntax
  [3]  stumpf_fusion        -- S0+S2: tonal coherence as syntax proxy
  [4]  sensory_pleasantness -- S0: consonance confirming syntactic regularity
  [10] loudness (onset_str) -- S1: intensity modulates PE salience
  [21] spectral_flux        -- S1: change magnitude for deviance detection

Scientific basis:
  Koelsch 2009: ERAN reflects music-syntactic processing in BA 44 bilateral
  Fong et al. 2020: MMN as PE in hierarchical generative model
  Bonetti et al. 2024: feedforward PE auditory cortex -> hippocampus (MEG N=83)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pmim/PMIM-cognitive-present.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_TREND_H18 = (0, 18, 18, 0)         # dissonance trajectory over phrase
_PLEASANTNESS_STAB_H18 = (4, 18, 19, 0)       # consonance stability over phrase
_LOUDNESS_VAL_H10 = (10, 10, 0, 2)            # current intensity at chord level

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_ONSET_STRENGTH = 11          # R3[10] maps to onset_strength proxy
_SPECTRAL_FLUX = 21


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """S-layer: 3D present-state from P/M layers + H3/R3.

    Computes syntax state (S0), deviance state (S1), and memory update
    rate (S2) using prediction-error and precision signals from upstream
    layers together with multi-scale temporal and raw spectral features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)`` from extraction.
        m_outputs: ``(M0, M1, M2)`` each ``(B, T)`` from temporal integration.

    Returns:
        ``(S0, S1, S2)`` each ``(B, T)``.
    """
    p0, p1, p2 = p_outputs
    m0, m1, _m2 = m_outputs

    # -- H3 features --
    roughness_trend = h3_features[_ROUGHNESS_TREND_H18]       # (B, T)
    pleasantness_stab = h3_features[_PLEASANTNESS_STAB_H18]   # (B, T)
    loudness_val = h3_features[_LOUDNESS_VAL_H10]             # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                  # (B, T)
    fusion = r3_features[..., _STUMPF_FUSION]                 # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]    # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]                   # (B, T)

    # -- S0: Syntax State --
    # Tracks tonal context stability. High when harmonic environment
    # conforms to stored rules (high fusion, pleasantness, stable
    # consonance trajectory). ERAN P0 inverted: low ERAN = stable syntax.
    # Koelsch 2009: ERAN reflects music-syntactic processing.
    s0 = torch.sigmoid(
        0.30 * fusion * pleasantness
        + 0.30 * pleasantness_stab
        + 0.20 * (1.0 - roughness)
        + 0.20 * (1.0 - p0)
    )

    # -- S1: Deviance State --
    # Real-time surprise meter: how much current input deviates from
    # both long-term (ERAN/P0) and short-term (MMN/P1) predictions.
    # Loudness modulates PE salience (louder deviants more salient).
    # Fong et al. 2020: MMN as PE in hierarchical generative model.
    s1 = torch.sigmoid(
        0.30 * p0 + 0.30 * p1
        + 0.20 * flux
        + 0.20 * loudness_val
    )

    # -- S2: Memory Update --
    # Rate at which predictive model is revised.
    # dModel/dt = eta * PE_weighted * (1 - Expectation_Confidence)
    # Strong PE (m0) in contexts of low precision (1-m1) produces
    # large updates. Roughness trend provides temporal context.
    # Bonetti et al. 2024: feedforward PE drives hippocampal updating.
    s2 = torch.sigmoid(
        0.35 * m0 * (1.0 - m1)
        + 0.30 * p2
        + 0.20 * (1.0 - fusion)
        + 0.15 * roughness_trend
    )

    return s0, s1, s2
