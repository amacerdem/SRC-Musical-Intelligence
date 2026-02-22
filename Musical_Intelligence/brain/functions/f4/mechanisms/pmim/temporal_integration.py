"""PMIM M-Layer -- Temporal Integration (3D).

Three mathematical / integration signals:

  M0: hierarchical_pe    -- Precision-weighted combination of ERAN + MMN [0, 1]
  M1: model_precision    -- Prediction model certainty [0, 1]
  M2: from_synthesis     -- Synthesised PE-precision interaction [0, 1]

Hierarchical PE (M0) combines the two prediction-error streams into a
single metric following hierarchical predictive coding: flux-driven deviance
weighted by dissonance (low-level PE / MMN) plus entropy-driven
unpredictability weighted by lack of fusion (high-level PE / ERAN).

Model precision (M1) quantifies how confident the current predictive model
is. High stumpf fusion, sensory pleasantness, and tonalness all indicate a
well-formed prediction that should produce large PE when violated.

From-synthesis (M2) captures the interaction between PE magnitude and model
precision -- the Bayesian surprise term (PE weighted by inverse precision).

H3 demands consumed (7 tuples):
  entropy:                (22,14,1,0)   mean H14 L0           -- average complexity
  entropy:                (22,18,13,0)  entropy H18 L0        -- higher-order unpredictability
  stumpf_fusion:          (3,10,0,2)    value H10 L2          -- fusion state
  stumpf_fusion:          (3,14,14,0)   periodicity H14 L0    -- cadential regularity
  sensory_pleasantness:   (4,10,0,2)    value H10 L2          -- current consonance
  tonalness:              (14,10,0,2)   value H10 L2          -- harmonic purity
  tonalness:              (14,14,18,0)  trend H14 L0          -- tonal trend

R3 consumed:
  [0]  roughness            -- M0: sensory dissonance for PE weighting
  [3]  stumpf_fusion        -- M0+M1: tonal coherence
  [4]  sensory_pleasantness -- M1: consonance for model precision
  [5]  inharmonicity        -- M0: harmonic template deviation
  [14] tonalness            -- M1: harmonic-to-noise ratio
  [21] spectral_flux        -- M0: change magnitude
  [22] entropy              -- M0: unpredictability

Scientific basis:
  Cheung et al. 2019: uncertainty x surprise -> musical pleasure (fMRI N=40)
  Gold et al. 2019: inverted-U preference for intermediate complexity (N=70)
  Friston 2005: precision-weighted PE in hierarchical generative models

See Building/C3-Brain/F4-Memory-Systems/mechanisms/pmim/PMIM-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ENTROPY_MEAN_H14 = (22, 14, 1, 0)            # average complexity over progression
_ENTROPY_ENTROPY_H18 = (22, 18, 13, 0)        # higher-order unpredictability
_FUSION_VAL_H10 = (3, 10, 0, 2)               # fusion state at chord level
_FUSION_PERIOD_H14 = (3, 14, 14, 0)           # cadential regularity proxy
_PLEASANTNESS_VAL_H10 = (4, 10, 0, 2)         # current consonance
_TONALNESS_VAL_H10 = (14, 10, 0, 2)           # harmonic purity
_TONALNESS_TREND_H14 = (14, 14, 18, 0)        # tonal trend over progression

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_INHARMONICITY = 5
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_ENTROPY = 22


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from P-layer + H3/R3.

    Computes hierarchical PE (M0), model precision (M1), and their
    synthesised interaction (M2).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)`` from extraction layer.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    _p0, _p1, p2 = p_outputs

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                # (B, T)
    fusion = r3_features[..., _STUMPF_FUSION]               # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    inhar = r3_features[..., _INHARMONICITY]                # (B, T)
    tonalness = r3_features[..., _TONALNESS]                # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]                 # (B, T)
    entropy = r3_features[..., _ENTROPY]                    # (B, T)

    # -- M0: Hierarchical PE --
    # Precision-weighted combination of low-level (flux x dissonance) and
    # high-level (entropy x lack-of-fusion) prediction error streams.
    # Cheung et al. 2019: uncertainty x surprise -> pleasure (fMRI N=40).
    # hierarchical_pe = clamp(flux * (roughness + inhar)/2
    #                         + entropy * (1 - fusion), 0, 1)
    m0 = (
        flux * (roughness + inhar) / 2.0
        + entropy * (1.0 - fusion)
    ).clamp(0.0, 1.0)

    # -- M1: Model Precision --
    # Prediction confidence: high fusion, pleasantness, tonalness all
    # indicate a well-formed prediction.
    # Gold et al. 2019: inverted-U for intermediate predictive complexity.
    # model_precision = sigma(fusion * pleasantness * tonalness)
    m1 = torch.sigmoid(fusion * pleasantness * tonalness)

    # -- M2: From-Synthesis --
    # PE-precision interaction: Bayesian surprise = PE * (1 - precision).
    # High PE with low model confidence produces the strongest learning
    # signal. Combines P2 (combined_pred_error) with inverted precision.
    m2 = torch.sigmoid(
        0.50 * p2 * (1.0 - m1) + 0.50 * m0
    )

    return m0, m1, m2
