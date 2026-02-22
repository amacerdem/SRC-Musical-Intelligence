"""OII F-Layer -- Forecast (2D).

Two explicit features predicting upcoming oscillatory mode states:

  F0: integration_pred   -- Integration mode prediction (1-2s ahead) [0, 1]
  F1: segregation_pred   -- Segregation mode prediction (0.5-1s ahead) [0, 1]

H3 consumed:
    (3, 18, 1, 0)  stumpf_fusion mean H18 L0        -- phrase-level binding stability
    (22, 14, 1, 0) entropy mean H14 L0              -- complexity trajectory
    (11, 14, 8, 0) onset_strength velocity H14 L0   -- mode switch rate (shared w/ M)
    (21, 18, 1, 0) spectral_flux mean H18 L0        -- transition rate for integration
    (15, 18, 3, 0) spectral_centroid std H18 L0     -- frequency balance variability
    (0, 24, 1, 0)  roughness mean H24 L0            -- dissonance over 36s episodic chunk
    (7, 16, 8, 0)  amplitude velocity H16 L0        -- energy change rate
    (7, 20, 4, 0)  amplitude max H20 L0             -- peak energy over 5s

R3 consumed:
    [0]  roughness          -- F1: gamma demand trajectory
    [3]  stumpf_fusion      -- F0: binding quality trajectory
    [7]  amplitude          -- F0+F1: energy trajectory for mode prediction
    [15] spectral_centroid  -- F0: frequency balance for integration prediction
    [22] entropy            -- F1: complexity trajectory

Reads: MSPBA via relay_outputs (graceful fallback).

See Building/C3-Brain/F4-Memory-Systems/mechanisms/oii/OII-forecast.md
Bruzzone et al. 2022: theta/alpha integration patterns track cognitive state (MEG N=66).
Samiee et al. 2022: cross-frequency PAC dynamics shift with stimulus (MEG N=16).
Cabral et al. 2022: metastable oscillatory modes predict mode transitions.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FUSION_MEAN_H18 = (3, 18, 1, 0)        # stumpf_fusion mean H18 L0
_ENTROPY_MEAN_H14 = (22, 14, 1, 0)      # entropy mean H14 L0
_ONSET_VEL_H14 = (11, 14, 8, 0)         # onset_strength velocity H14 L0 (shared w/ M)
_FLUX_MEAN_H18 = (21, 18, 1, 0)         # spectral_flux mean H18 L0
_CENTROID_STD_H18 = (15, 18, 3, 0)      # spectral_centroid std H18 L0
_ROUGH_MEAN_H24 = (0, 24, 1, 0)         # roughness mean H24 L0
_AMP_VEL_H16 = (7, 16, 8, 0)           # amplitude velocity H16 L0
_AMP_MAX_H20 = (7, 20, 4, 0)           # amplitude max H20 L0

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_AMPLITUDE = 7
_SPECTRAL_CENTROID = 15
_ENTROPY = 22


def _relay_field(
    relay_outputs: Dict[str, Tensor],
    name: str,
    idx: int,
    shape_ref: Tensor,
) -> Tensor:
    """Gracefully extract a single field from an upstream relay."""
    relay = relay_outputs.get(name)
    if relay is None:
        return torch.zeros_like(shape_ref)
    return relay[..., idx]


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: oscillatory mode state predictions.

    F0 (integration_pred) forecasts the upcoming integration state 1-2s
    ahead based on structural expectation trajectory and binding quality
    trends.  Uses H18 (2s phrase window) because integration operates at
    the phrase level -- theta oscillations bind information across the full
    harmonic arc.  When structural expectations point toward cadential
    resolution (high binding trend), integration mode is predicted.

    F1 (segregation_pred) forecasts the upcoming segregation demand 0.5-1s
    ahead based on entropy and onset velocity trajectories.  Uses H14
    (700ms progression window) matching the faster timescale of gamma-band
    processing.  When entropy is increasing and onset velocity is high
    (many transient events), segregation mode is predicted.

    Bruzzone et al. 2022: DTI + MEG N=66/67, theta/alpha integration
    patterns track cognitive state; structural degree p=0.007.
    Samiee et al. 2022: MEG N=16, cross-frequency PAC dynamics shift
    with stimulus properties; directed connectivity shows bottom-up delta
    and top-down beta.
    Cabral et al. 2022: metastable oscillatory modes -- frequency,
    duration, scale controlled by coupling parameters.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e: ``(E0, E1, E2)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.
        relay_outputs: Upstream mechanism outputs (MSPBA, etc.).

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    _e0, _e1, _e2 = e
    p0, p1, _p2 = p

    # -- H3 features --
    fusion_h18 = h3_features[_FUSION_MEAN_H18]         # (B, T)
    entropy_h14 = h3_features[_ENTROPY_MEAN_H14]       # (B, T)
    onset_vel_h14 = h3_features[_ONSET_VEL_H14]        # (B, T)
    flux_h18 = h3_features[_FLUX_MEAN_H18]             # (B, T)
    centroid_std_h18 = h3_features[_CENTROID_STD_H18]   # (B, T)
    rough_h24 = h3_features[_ROUGH_MEAN_H24]           # (B, T)
    amp_vel_h16 = h3_features[_AMP_VEL_H16]            # (B, T)
    amp_max_h20 = h3_features[_AMP_MAX_H20]            # (B, T)

    # -- Upstream relay (graceful fallback) --
    ref = fusion_h18
    struct_expect = _relay_field(relay_outputs, "MSPBA", 0, ref)

    # -- F0: Integration Prediction --
    # sigma(0.25 * struct_expect + 0.20 * fusion_h18).
    # Phrase-level binding stability forecasts integration mode.
    # Bruzzone et al. 2022: theta/alpha integration patterns track state.
    f0 = torch.sigmoid(
        0.25 * (struct_expect + p0) / 2.0
        + 0.20 * fusion_h18
    )

    # -- F1: Segregation Prediction --
    # sigma(0.20 * entropy_h14 + 0.20 * onset_velocity_h14).
    # Entropy + onset velocity trajectories forecast segregation demand.
    # Samiee et al. 2022: cross-frequency PAC dynamics shift w/ stimulus.
    f1 = torch.sigmoid(
        0.20 * entropy_h14
        + 0.20 * onset_vel_h14
    )

    return f0, f1
