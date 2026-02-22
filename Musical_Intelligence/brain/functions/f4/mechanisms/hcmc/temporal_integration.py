"""HCMC M-Layer -- Temporal Integration (3D).

Hippocampal-cortical memory circuit mathematical model:

  M0: consolidation_strength  -- Hippocampal-to-cortical transfer strength [0, 1]
  M1: encoding_rate           -- Rate of new episodic trace formation [0, 1]
  M2: from_synthesis          -- Synthesis of binding x segmentation x storage [0, 1]

H3 consumed:
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0        -- binding stability over 5s
    (3, 24, 19, 0)  stumpf_fusion stability H24 L0   -- long-term binding stability 36s
    (22, 20, 13, 0) entropy entropy H20 L0            -- entropy of entropy over 5s
    (22, 24, 19, 0) entropy stability H24 L0          -- pattern stability over 36s
    (21, 20, 5, 0)  spectral_flux range H20 L0        -- flux dynamic range over 5s
    (11, 20, 5, 0)  onset_strength range H20 L0       -- onset dynamic range over 5s
    (10, 20, 1, 0)  loudness mean H20 L0              -- average salience over 5s

R3 consumed:
    [3]      stumpf_fusion  -- M0: binding coherence gate
    [21]     spectral_flux  -- M1: boundary trigger
    [11]     onset_strength -- M1: event marker
    [10]     loudness       -- M1: arousal correlate
    [22]     entropy        -- M0: pattern regularity
    [25:33]  x_l0l5         -- M0: encoding strength

See Building/C3-Brain/F4-Memory-Systems/mechanisms/hcmc/HCMC-temporal-integration.md
McClelland et al. 1995: Complementary learning systems -- fast hippocampal + slow cortical.
Squire & Alvarez 1995: Hippocampal-cortical consolidation theory.
Buzsaki 2015: Sharp-wave ripples drive hippocampal-cortical transfer.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_5S = (3, 20, 1, 0)         # stumpf_fusion mean H20 L0
_STUMPF_STAB_36S = (3, 24, 19, 0)       # stumpf_fusion stability H24 L0
_ENTROPY_ENT_5S = (22, 20, 13, 0)       # entropy entropy H20 L0
_ENTROPY_STAB_36S = (22, 24, 19, 0)     # entropy stability H24 L0
_FLUX_RANGE_5S = (21, 20, 5, 0)         # spectral_flux range H20 L0
_ONSET_RANGE_5S = (11, 20, 5, 0)        # onset_strength range H20 L0
_LOUD_MEAN_5S = (10, 20, 1, 0)          # loudness mean H20 L0

# -- R3 indices ----------------------------------------------------------------
_STUMPF_FUSION = 3
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_SPECTRAL_FLUX = 21
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3/R3.

    M0 (consolidation_strength): Hippocampal-to-cortical transfer.
    Combines encoding strength (from E-layer binding) with pattern stability
    (harmonic consistency over time), gated by tonal fusion (stumpf).
    McClelland et al. 1995: complementary learning systems.

    M1 (encoding_rate): Event-driven measure of how rapidly new episodic
    traces form. High flux and onsets drive faster encoding.
    Squire & Alvarez 1995: hippocampal-cortical consolidation rate.

    M2 (from_synthesis): Synthesis of all three E-layer outputs into a
    unified memory formation signal. Captures the joint state of binding,
    segmentation, and storage as an integrated consolidation readout.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e

    # -- H3 features --
    stumpf_mean_5s = h3_features[_STUMPF_MEAN_5S]       # (B, T)
    entropy_ent_5s = h3_features[_ENTROPY_ENT_5S]        # (B, T)
    entropy_stab_36s = h3_features[_ENTROPY_STAB_36S]    # (B, T)
    flux_range_5s = h3_features[_FLUX_RANGE_5S]          # (B, T)
    onset_range_5s = h3_features[_ONSET_RANGE_5S]        # (B, T)
    loud_mean_5s = h3_features[_LOUD_MEAN_5S]            # (B, T)

    # -- R3 features --
    stumpf = r3_features[..., _STUMPF_FUSION]            # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]              # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]        # (B, T)
    loudness = r3_features[..., _LOUDNESS]               # (B, T)
    entropy = r3_features[..., _ENTROPY]                 # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- Derived signals --
    # Encoding_Strength = e0 (fast binding) * binding_coherence
    binding_coherence = stumpf * x_l0l5.mean(dim=-1)     # (B, T)
    encoding_strength = e0 * binding_coherence

    # Pattern_Stability = familiarity_proxy * (1 - entropy)
    # Use entropy stability at 36s as familiarity proxy
    familiarity_proxy = entropy_stab_36s
    pattern_stability = familiarity_proxy * (1.0 - entropy)

    # -- M0: Consolidation Strength --
    # consolidation_str = (Encoding_Strength x Pattern_Stability x stumpf).clamp(0, 1)
    # McClelland et al. 1995: fast hippocampal + slow cortical integration.
    # Buzsaki 2015: sharp-wave ripples drive hippocampal-cortical transfer.
    m0 = (encoding_strength * pattern_stability * stumpf).clamp(0.0, 1.0)

    # -- M1: Encoding Rate --
    # sigma(0.35 * flux + 0.35 * onset_str + 0.30 * loudness)
    # Squire & Alvarez 1995: hippocampal-cortical consolidation rate.
    m1 = torch.sigmoid(
        0.35 * flux + 0.35 * onset_str + 0.30 * loudness
    )

    # -- M2: Synthesis --
    # Joint binding-segmentation-storage signal gated by 5s stability.
    # Captures the integrated memory formation state from all three E-layer
    # outputs, weighted by temporal stability of the underlying features.
    m2 = torch.sigmoid(
        0.35 * e0 * stumpf_mean_5s
        + 0.35 * e1 * flux_range_5s
        + 0.30 * e2 * (1.0 - entropy_ent_5s)
    )

    return m0, m1, m2
