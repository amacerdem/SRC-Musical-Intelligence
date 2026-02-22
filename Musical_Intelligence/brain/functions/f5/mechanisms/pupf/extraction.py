"""PUPF E-Layer -- Extraction (2D).

Pleasure-Uncertainty Prediction Function extraction signals:
  E0: prediction_err   — Spectral prediction error (surprise proxy) [0, 1]
  E1: uncertainty       — Shannon entropy of current context [0, 1]

E0 captures how much the current spectral frame deviates from prediction.
Spectral flux velocity (instantaneous change rate) combined with onset
strength velocity and SRP prediction error provides a multi-source surprise
signal. The amygdala responds to prediction errors with magnitude-dependent
activation (Cheung 2019, d=3.8-4.16).

E1 captures the current level of contextual uncertainty (Shannon entropy).
Distribution entropy and flatness combined with harmonic deviation measure
how uncertain the acoustic environment is. Low entropy = predictable context;
high entropy = uncertain context. This is the H axis of the Goldilocks
function.

H3 demands consumed (6 tuples):
  (21, 16, 20, 0)  spectral_flux entropy H16 L0        -- 1s entropy of spectral change
  (22, 16, 20, 0)  distribution_entropy entropy H16 L0  -- 1s Shannon entropy
  (21, 7, 8, 0)    spectral_flux velocity H7 L0         -- instantaneous surprise rate
  (22, 7, 8, 0)    distribution_entropy velocity H7 L0  -- uncertainty change rate
  (22, 16, 20, 0)  distribution_entropy entropy H16 L0  -- integrated entropy for H
  (11, 7, 8, 0)    onset_strength velocity H7 L0        -- beat onset rate

R3 features:
  [21] spectral_flux, [22] distribution_entropy, [23] distribution_flatness,
  [11] onset_strength, [0] roughness

Upstream reads:
  SRP relay (19D) -- prediction_error at C2 (idx 5)

Cheung et al. 2019: H x S interaction drives amygdala and hippocampus
activation (fMRI, N=39, d=3.8-4.16).
Gold et al. 2019: prediction error drives pleasure (cross-modal, N=40).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/pupf/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_FLUX_ENT_H16 = (21, 16, 20, 0)           # spectral_flux entropy H16 L0
_ENTROPY_ENT_H16 = (22, 16, 20, 0)        # distribution_entropy entropy H16 L0
_FLUX_VEL_H7 = (21, 7, 8, 0)              # spectral_flux velocity H7 L0
_ENTROPY_VEL_H7 = (22, 7, 8, 0)           # distribution_entropy velocity H7 L0
_ONSET_VEL_H7 = (11, 7, 8, 0)             # onset_strength velocity H7 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SPECTRAL_FLUX = 21
_DIST_ENTROPY = 22
_DIST_FLATNESS = 23
_ONSET_STRENGTH = 11
_ROUGHNESS = 0

# -- Upstream relay indices ---------------------------------------------------
_SRP_PREDICTION_ERROR = 5   # SRP C2:prediction_error (idx 5)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute E-layer: prediction error and uncertainty extraction signals.

    E0 (prediction_err) captures surprise magnitude from spectral change.
    Spectral flux velocity (instantaneous surprise rate) combined with
    onset velocity and SRP prediction error forms a multi-source surprise
    signal. Amygdala responds proportionally to prediction error magnitude.

    E1 (uncertainty) captures contextual Shannon entropy -- the H axis of
    the Goldilocks function. Distribution entropy, flatness, and harmonic
    deviation measure how uncertain the acoustic context is. Low entropy =
    predictable; high entropy = uncertain environment.

    Cheung et al. 2019: H x S interaction in amygdala/hippocampus
    (fMRI N=39, d=3.8-4.16).
    Gold et al. 2019: prediction error drives pleasure (N=40).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        relay_outputs: ``{"SRP": (B, T, 19)}``

    Returns:
        ``(E0, E1)`` each ``(B, T)``
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    flux_ent = h3_features[_FLUX_ENT_H16]         # (B, T)
    entropy_ent = h3_features[_ENTROPY_ENT_H16]    # (B, T)
    flux_vel = h3_features[_FLUX_VEL_H7]           # (B, T)
    entropy_vel = h3_features[_ENTROPY_VEL_H7]     # (B, T)
    onset_vel = h3_features[_ONSET_VEL_H7]         # (B, T)

    # -- R3 features --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]     # (B, T)
    dist_entropy = r3_features[..., _DIST_ENTROPY]       # (B, T)
    dist_flatness = r3_features[..., _DIST_FLATNESS]     # (B, T)
    roughness = r3_features[..., _ROUGHNESS]             # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    srp_pe = srp[..., _SRP_PREDICTION_ERROR]  # (B, T) prediction error

    # -- E0: Prediction Error (Surprise) --
    # Multi-source surprise: spectral flux velocity (instantaneous change),
    # onset velocity (beat-level surprise), and SRP prediction error
    # (cognitive-level PE). These jointly index the S axis of the
    # Goldilocks function.
    # Cheung 2019: prediction error magnitude drives amygdala (d=3.8-4.16).
    e0 = torch.sigmoid(
        0.35 * flux_vel * spectral_flux.clamp(min=0.1)
        + 0.30 * onset_vel * srp_pe.clamp(min=0.1)
        + 0.35 * flux_ent * roughness.clamp(min=0.1)
    )

    # -- E1: Uncertainty (Shannon Entropy) --
    # Contextual entropy from distribution features. Distribution entropy
    # at velocity and entropy morphs captures how uncertain the context is.
    # Flatness measures noise-level uncertainty (flat spectrum = high
    # uncertainty). This is the H axis of the Goldilocks function.
    e1 = torch.sigmoid(
        0.35 * entropy_ent * dist_entropy.clamp(min=0.1)
        + 0.35 * entropy_vel * dist_flatness.clamp(min=0.1)
        + 0.30 * entropy_ent
    )

    return e0, e1
