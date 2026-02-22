"""IUCP E-Layer -- Extraction (4D).

Inverted-U Complexity Preference extraction signals:
  E0: ic_liking_curve          -- Inverted-U for information content [0, 1]
  E1: entropy_liking_curve     -- Inverted-U for entropy [0, 1]
  E2: ic_entropy_interaction   -- IC x Entropy interaction surface [0, 1]
  E3: optimal_complexity       -- Preferred complexity level [0, 1]

The core transform 4.0 * x * (1.0 - x) produces a quadratic that peaks at
x=0.5, implementing the Berlyne (1971) optimal complexity principle. Gold 2019
provided the empirical parametrization: IC quadratic beta_quad = -0.09
(p < 0.001), R2 = 26.3% (Study 1, N=43); replicated beta_quad = -0.18,
R2 = 41.6% (Study 2, N=27). Entropy quadratic beta_quad = -0.06 (p = 0.003),
R2 = 19.1% (Study 1); replicated beta_quad = -0.25, R2 = 34.9% (Study 2).

E0 applies the inverted-U to mean IC over 1s, modulated by mean pleasantness.
E1 applies the same transform to concentration entropy over 1s.
E2 captures the IC x entropy interaction (saddle surface, Cheung 2019).
E3 integrates the interaction with hedonic variability for optimal zone.

H3 demands consumed (14 tuples -- all E-layer):
  ( 0,  8,  1, 2)  roughness mean H8 L2         -- harmonic complexity
  ( 0, 16,  2, 2)  roughness std H16 L2          -- roughness variability
  ( 4, 16,  1, 2)  pleasantness mean H16 L2      -- hedonic baseline
  ( 4, 16,  2, 2)  pleasantness std H16 L2       -- hedonic fluctuation
  ( 8, 16,  1, 2)  loudness mean H16 L2          -- perceptual weighting
  (21,  4,  0, 2)  spectral_flux value H4 L2     -- IC at theta
  (21,  8, 20, 2)  spectral_flux entropy H8 L2   -- IC entropy 500ms
  (21, 16,  1, 2)  spectral_flux mean H16 L2     -- mean IC 1s (primary)
  (24,  4,  0, 2)  concentration value H4 L2     -- concentration theta
  (24,  8,  2, 2)  concentration std H8 L2       -- concentration std 500ms
  (24, 16, 20, 2)  concentration entropy H16 L2  -- entropy 1s (primary)
  (33,  8,  1, 2)  x_l4l5 mean H8 L2            -- coupling 500ms
  (33, 16,  2, 2)  x_l4l5 std H16 L2            -- coupling variability
  (33, 16, 20, 2)  x_l4l5 entropy H16 L2        -- coupling entropy

R3 features:
  [0] roughness, [4] sensory_pleasantness, [8] loudness,
  [21] spectral_flux, [24] distribution_concentration

Upstream reads:
  RPEM relay -- prediction error context
  DAED relay -- wanting/liking context

Gold et al. 2019: IC + entropy inverted-U (fMRI, N=43+27).
Gold et al. 2023b: VS + STG fMRI (N=24).
Cheung et al. 2019: IC x entropy saddle surface (fMRI, N=39+40).

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iucp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (all 14 tuples, all L2) --------------------------------
_IC_VALUE_H4 = (21, 4, 0, 2)              # spectral_flux value H4 L2
_IC_ENTROPY_H8 = (21, 8, 20, 2)           # spectral_flux entropy H8 L2
_IC_MEAN_H16 = (21, 16, 1, 2)             # spectral_flux mean H16 L2 (primary)
_CONC_VALUE_H4 = (24, 4, 0, 2)            # concentration value H4 L2
_CONC_STD_H8 = (24, 8, 2, 2)             # concentration std H8 L2
_CONC_ENTROPY_H16 = (24, 16, 20, 2)       # concentration entropy H16 L2 (primary)
_ROUGHNESS_MEAN_H8 = (0, 8, 1, 2)         # roughness mean H8 L2
_ROUGHNESS_STD_H16 = (0, 16, 2, 2)        # roughness std H16 L2
_LOUDNESS_MEAN_H16 = (8, 16, 1, 2)        # loudness mean H16 L2
_PLEAS_MEAN_H16 = (4, 16, 1, 2)           # pleasantness mean H16 L2
_PLEAS_STD_H16 = (4, 16, 2, 2)            # pleasantness std H16 L2
_COUPLING_MEAN_H8 = (33, 8, 1, 2)         # x_l4l5 mean H8 L2
_COUPLING_STD_H16 = (33, 16, 2, 2)        # x_l4l5 std H16 L2
_COUPLING_ENTROPY_H16 = (33, 16, 20, 2)   # x_l4l5 entropy H16 L2

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_SPECTRAL_FLUX = 21
_DIST_CONCENTRATION = 24


def _inverted_u(x: Tensor) -> Tensor:
    """Berlyne inverted-U transform: 4 * x * (1 - x), peaks at x=0.5.

    Input is clamped to [0, 1] to ensure the parabola stays in [0, 1].
    """
    x_c = x.clamp(0.0, 1.0)
    return 4.0 * x_c * (1.0 - x_c)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute E-layer: inverted-U complexity preference extraction signals.

    E0 (ic_liking_curve): Inverted-U for mean IC over 1s, modulated by
    mean pleasantness. Gold 2019: IC quadratic beta_quad = -0.09 (p < 0.001),
    R2 = 26.3%. The quadratic 4*x*(1-x) peaks at x=0.5 (medium complexity).

    E1 (entropy_liking_curve): Inverted-U for concentration entropy over 1s.
    Gold 2019: entropy quadratic beta_quad = -0.06 (p = 0.003), R2 = 19.1%.

    E2 (ic_entropy_interaction): Product of E0 and E1, modulated by coupling
    entropy. Implements the saddle surface from Cheung 2019: high uncertainty
    shifts optimal IC downward (prefer predictable in uncertain contexts).

    E3 (optimal_complexity): Integrates interaction surface with pleasantness
    variability. Provides estimate of listener's current optimal complexity
    zone for P-layer preference tracking.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"RPEM": (B, T, D), "DAED": (B, T, D)}``

    Returns:
        ``(E0, E1, E2, E3)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    mean_ic_1s = h3_features[_IC_MEAN_H16]                   # (B, T)
    conc_entropy_1s = h3_features[_CONC_ENTROPY_H16]          # (B, T)
    pleas_mean_1s = h3_features[_PLEAS_MEAN_H16]              # (B, T)
    pleas_std_1s = h3_features[_PLEAS_STD_H16]                # (B, T)
    coupling_entropy_1s = h3_features[_COUPLING_ENTROPY_H16]  # (B, T)

    # -- Inverted-U transforms --
    ic_quadratic = _inverted_u(mean_ic_1s)
    entropy_quadratic = _inverted_u(conc_entropy_1s)

    # -- E0: IC Liking Curve --
    # sigma(0.40 * ic_quadratic + 0.30 * mean_pleasantness_1s)
    # Gold 2019: IC quadratic beta_quad = -0.09, R2 = 26.3%
    e0 = torch.sigmoid(
        0.40 * ic_quadratic
        + 0.30 * pleas_mean_1s
    )

    # -- E1: Entropy Liking Curve --
    # sigma(0.40 * entropy_quadratic + 0.30 * concentration_entropy_1s)
    # Gold 2019: entropy quadratic beta_quad = -0.06, R2 = 19.1%
    e1 = torch.sigmoid(
        0.40 * entropy_quadratic
        + 0.30 * conc_entropy_1s
    )

    # -- E2: IC x Entropy Interaction --
    # sigma(0.40 * f01 * f02 + 0.30 * coupling_entropy_1s)
    # Cheung 2019: partial eta2 = 0.07 for interaction
    e2 = torch.sigmoid(
        0.40 * e0 * e1
        + 0.30 * coupling_entropy_1s
    )

    # -- E3: Optimal Complexity --
    # sigma(0.50 * f03 + 0.25 * pleasantness_std_1s)
    # Integrates interaction surface with hedonic variability
    e3 = torch.sigmoid(
        0.50 * e2
        + 0.25 * pleas_std_1s
    )

    return e0, e1, e2, e3
