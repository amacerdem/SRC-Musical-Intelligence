"""CSSL M-Layer -- Temporal Integration (2D).

Temporal dynamics of cross-species conservation and template fidelity:
  M0: conservation_index   (cross-species conservation strength)
  M1: template_fidelity    (song template match quality)

M0 captures how "species-general" the current musical pattern is, using
three features universal across vocal learning species: stumpf fusion
(tonal coherence), harmonicity (harmonic-to-noise ratio), and tonalness.

M1 captures song template match quality from familiarity context,
predictability (inverted entropy), and tonal binding coherence.

H3 demands consumed:
    (3, 20, 1, 0)   stumpf_fusion mean H20 L0      -- binding over phrase window
    (3, 24, 1, 0)   stumpf_fusion mean H24 L0      -- long-term binding context
    (6, 20, 1, 0)   pitch_strength mean H20 L0     -- pitch stability over phrase
    (14, 20, 1, 0)  tonalness mean H20 L0          -- tonal stability over phrase
    (22, 20, 1, 0)  entropy mean H20 L0            -- average complexity over 5s

R3 consumed:
    [3]  stumpf_fusion  -- tonal coherence for conservation
    [5]  harmonicity    -- harmonic-to-noise ratio = song purity
    [14] tonalness      -- tonal purity for conservation
    [22] entropy        -- pattern complexity for fidelity

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cssl/CSSL-temporal-integration.md
Zhang et al. 2024: homologous auditory dorsal/ventral pathways (dMRI, N=21).
Lipkind et al. 2013: stepwise vocal combinatorial capacity parallels.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_STUMPF_MEAN_H20_L0 = (3, 20, 1, 0)    # stumpf_fusion mean H20 L0
_STUMPF_MEAN_H24_L0 = (3, 24, 1, 0)    # stumpf_fusion mean H24 L0
_PITCH_MEAN_H20_L0 = (6, 20, 1, 0)     # pitch_strength mean H20 L0
_TONAL_MEAN_H20_L0 = (14, 20, 1, 0)    # tonalness mean H20 L0
_ENTROPY_MEAN_H20_L0 = (22, 20, 1, 0)  # entropy mean H20 L0

# -- R3 feature indices -------------------------------------------------------
_STUMPF = 3
_HARMONICITY = 5
_TONALNESS = 14
_ENTROPY = 22


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: conservation index and template fidelity.

    M0 quantifies how "species-general" the current musical pattern is,
    combining tonal coherence, harmonic purity, and tonalness -- features
    universal across vocal learning species.

    M1 measures song template match quality from familiarity (proxied via
    upstream encoding context), predictability (inverted entropy), and
    tonal binding coherence.

    Zhang et al. 2024: homologous auditory dorsal/ventral pathways across
    marmosets, macaques, and humans (dMRI, N=21, P<0.001).
    Lipkind et al. 2013: stepwise vocal combinatorial capacity parallels
    between songbirds and human infants.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    _e0, _e1, e2 = e

    # -- H3 reads --
    stumpf_h20 = h3_features[_STUMPF_MEAN_H20_L0]    # (B, T)
    tonal_h20 = h3_features[_TONAL_MEAN_H20_L0]      # (B, T)
    entropy_h20 = h3_features[_ENTROPY_MEAN_H20_L0]   # (B, T)

    # -- R3 reads --
    stumpf = r3_features[..., _STUMPF]                # (B, T)
    harmonicity = r3_features[..., _HARMONICITY]      # (B, T)
    tonalness = r3_features[..., _TONALNESS]          # (B, T)
    entropy = r3_features[..., _ENTROPY]              # (B, T)

    # -- Familiarity proxy from E-layer binding --
    # E2 (all_shared_binding) encodes familiarity-gated binding
    familiarity_proxy = e2  # (B, T)

    # -- M0: Conservation Index --
    # Cross-species conservation strength: how "universal" the pattern is.
    # Uses R3-instant features for real-time conservation assessment,
    # blended with H3 phrase-level stability.
    # Zhang et al. 2024: homologous auditory pathways across 3 primate species.
    m0 = torch.sigmoid(
        0.35 * (0.5 * stumpf + 0.5 * stumpf_h20)
        + 0.35 * harmonicity
        + 0.30 * (0.5 * tonalness + 0.5 * tonal_h20)
    )

    # -- M1: Template Fidelity --
    # Song template match quality: familiarity is weighted highest because
    # template fidelity is fundamentally about recognition. Low entropy
    # indicates predictable patterns that match templates better.
    # Lipkind et al. 2013: stepwise vocal combinatorial capacity parallels.
    m1 = torch.sigmoid(
        0.50 * familiarity_proxy
        + 0.30 * (1.0 - (0.5 * entropy + 0.5 * entropy_h20))
        + 0.20 * stumpf
    )

    return m0, m1
