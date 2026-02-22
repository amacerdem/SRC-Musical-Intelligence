"""PUPF U+G Layer -- Temporal Integration (5D).

Pleasure-Uncertainty Prediction Function integration signals:
  U0: entropy_H           — Integrated uncertainty H over time [0, 1]
  U1: surprise_S           — Integrated surprise S over time [0, 1]
  U2: HS_interaction       — H x S interaction term (Goldilocks core) [0, 1]
  G0: pleasure_P           — Pleasure from H x S function [0, 1]
  G1: goldilocks_zone      — Whether current H,S is in Goldilocks zone [0, 1]

U0 integrates entropy over multiple temporal horizons (525ms, 800ms, 1s) to
produce a stable uncertainty estimate. This is the H axis of the Goldilocks
function. Low H = predictable musical context; high H = uncertain context.

U1 integrates surprise signals over matching horizons. Spectral flux velocity
at multiple scales captures how surprising events are across temporal windows.
This is the S axis of the Goldilocks function.

U2 is the key H x S interaction term. Cheung 2019 showed that the interaction
of entropy and surprise (not either alone) drives amygdala/hippocampus
activation with large effect sizes (d=3.8-4.16). The interaction captures
how surprising events land in predictable vs uncertain contexts.

G0 implements the pleasure function: pleasure peaks when uncertainty is low
but surprise is high (certain context, unexpected event). This maps the
inverted-U relationship between H x S and hedonic response.

G1 indicates whether current H and S values fall in the Goldilocks zone --
the narrow band where pleasure is maximized. Low H + high S = maximal
pleasure. High H + high S = overwhelm. Low H + low S = boredom.

H3 demands consumed (9 tuples):
  (22, 12, 18, 0)  distribution_entropy trend H12 L0  -- entropy trajectory 525ms
  (22, 15, 2, 0)   distribution_entropy std H15 L0    -- entropy variability 800ms
  (21, 12, 8, 0)   spectral_flux velocity H12 L0      -- surprise rate half-beat
  (21, 15, 8, 0)   spectral_flux velocity H15 L0      -- surprise rate 800ms
  (21, 16, 18, 0)  spectral_flux trend H16 L0         -- surprise trajectory 1s
  (6, 12, 8, 0)    harmonic_deviation velocity H12 L0  -- harmonic PE rate
  (6, 16, 2, 0)    harmonic_deviation std H16 L0       -- harmonic uncertainty 1s
  (4, 16, 0, 0)    sensory_pleasantness value H16 L0   -- hedonic baseline
  (8, 12, 8, 0)    velocity_A velocity H12 L0          -- tempo dynamics half-beat

R3 features:
  [21] spectral_flux, [22] distribution_entropy, [23] distribution_flatness,
  [24] distribution_concentration, [4] sensory_pleasantness,
  [6] harmonic_deviation, [25:33] x_l0l5

Upstream reads:
  SRP relay (19D) -- prediction_error at C2 (idx 5)

Cheung et al. 2019: H x S interaction: low entropy + high surprise = maximal
amygdala/hippocampus response (fMRI, N=39, d=3.8-4.16).
Gold et al. 2019: prediction error drives aesthetic pleasure (N=40).
Koelsch 2014: tension-resolution-pleasure cycle in music.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/pupf/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_ENTROPY_TREND_H12 = (22, 12, 18, 0)      # distribution_entropy trend H12 L0
_ENTROPY_STD_H15 = (22, 15, 2, 0)         # distribution_entropy std H15 L0
_FLUX_VEL_H12 = (21, 12, 8, 0)            # spectral_flux velocity H12 L0
_FLUX_VEL_H15 = (21, 15, 8, 0)            # spectral_flux velocity H15 L0
_FLUX_TREND_H16 = (21, 16, 18, 0)         # spectral_flux trend H16 L0
_HARM_VEL_H12 = (6, 12, 8, 0)             # harmonic_deviation velocity H12 L0
_HARM_STD_H16 = (6, 16, 2, 0)             # harmonic_deviation std H16 L0
_PLEAS_VAL_H16 = (4, 16, 0, 0)            # sensory_pleasantness value H16 L0
_VELA_VEL_H12 = (8, 12, 8, 0)             # velocity_A velocity H12 L0

# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SPECTRAL_FLUX = 21
_DIST_ENTROPY = 22
_DIST_FLATNESS = 23
_DIST_CONCENTRATION = 24
_SENSORY_PLEASANTNESS = 4
_HARMONIC_DEVIATION = 6
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream relay indices ---------------------------------------------------
_SRP_PREDICTION_ERROR = 5   # SRP C2:prediction_error (idx 5)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Compute U+G layer: integrated uncertainty, surprise, and pleasure.

    U0 (entropy_H) integrates entropy signals over multi-scale temporal
    windows. Entropy trend (525ms) + entropy std (800ms) + entropy entropy
    (1s) combine for a stable uncertainty estimate.

    U1 (surprise_S) integrates surprise signals. Spectral flux velocity at
    200ms, 525ms, and 800ms captures surprise rate across temporal scales.
    Harmonic deviation velocity adds pitch-domain surprise.

    U2 (HS_interaction) is the core interaction term. Cheung 2019 showed
    H x S interaction (not H or S alone) drives amygdala/hippocampus with
    d=3.8-4.16. Computed as product of normalized H and S modulated by
    harmonic precision.

    G0 (pleasure_P) implements the pleasure function: pleasure = f(H, S)
    where low H + high S = maximal pleasure. Sensory pleasantness baseline
    anchors the hedonic computation.

    G1 (goldilocks_zone) indicates whether H and S are in the optimal zone.
    Low entropy + high surprise = Goldilocks zone (certain context,
    surprising event). High entropy + high surprise = overwhelm.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1)`` from extraction layer.
        relay_outputs: ``{"SRP": (B, T, 19)}``

    Returns:
        ``(U0, U1, U2, G0, G1)`` each ``(B, T)``
    """
    e0, e1 = e

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    entropy_trend = h3_features[_ENTROPY_TREND_H12]    # (B, T)
    entropy_std = h3_features[_ENTROPY_STD_H15]        # (B, T)
    flux_vel_12 = h3_features[_FLUX_VEL_H12]           # (B, T)
    flux_vel_15 = h3_features[_FLUX_VEL_H15]           # (B, T)
    flux_trend = h3_features[_FLUX_TREND_H16]          # (B, T)
    harm_vel = h3_features[_HARM_VEL_H12]              # (B, T)
    harm_std = h3_features[_HARM_STD_H16]              # (B, T)
    pleas_val = h3_features[_PLEAS_VAL_H16]            # (B, T)
    vela_vel = h3_features[_VELA_VEL_H12]              # (B, T)

    # -- R3 features --
    dist_entropy = r3_features[..., _DIST_ENTROPY]            # (B, T)
    dist_flatness = r3_features[..., _DIST_FLATNESS]          # (B, T)
    dist_concentration = r3_features[..., _DIST_CONCENTRATION]  # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]     # (B, T)
    harm_dev = r3_features[..., _HARMONIC_DEVIATION]           # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]     # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                         # (B, T)

    # -- Upstream relay features (graceful fallback) --
    srp = relay_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    srp_pe = srp[..., _SRP_PREDICTION_ERROR]  # (B, T) prediction error

    # -- U0: Entropy H (Integrated Uncertainty) --
    # Multi-scale entropy integration: trend (525ms) for trajectory,
    # std (800ms) for variability, plus E1 (extraction-level uncertainty).
    # Flatness adds noise-level uncertainty. High U0 = uncertain context.
    u0 = torch.sigmoid(
        0.35 * entropy_trend * dist_entropy.clamp(min=0.1)
        + 0.35 * entropy_std * dist_flatness.clamp(min=0.1)
        + 0.30 * e1
    )

    # -- U1: Surprise S (Integrated Surprise) --
    # Multi-scale surprise integration: flux velocity at 525ms and 800ms
    # captures surprise rate across temporal scales. Harmonic deviation
    # velocity adds pitch-domain surprise. Tempo dynamics (velocity_A)
    # adds rhythmic surprise.
    u1 = torch.sigmoid(
        0.30 * flux_vel_12 * flux_vel_15.clamp(min=0.1)
        + 0.30 * harm_vel * e0.clamp(min=0.1)
        + 0.20 * vela_vel
        + 0.20 * srp_pe
    )

    # -- U2: H x S Interaction --
    # The core Goldilocks interaction. Cheung 2019: neither H nor S alone
    # but their interaction drives amygdala/hippocampus (d=3.8-4.16).
    # Modulated by harmonic std (precision of pitch predictions) and
    # energy-consonance coupling (x_l0l5).
    u2 = torch.sigmoid(
        0.40 * u0 * u1
        + 0.30 * harm_std * x_l0l5_mean.clamp(min=0.1)
        + 0.30 * flux_trend * entropy_trend
    )

    # -- G0: Pleasure P --
    # Pleasure function: pleasure = f(H, S). Low H + high S = maximal
    # pleasure (certain context, surprising event). Anchored by sensory
    # pleasantness baseline and hedonic value at 1s.
    # Gold et al. 2019: prediction error drives aesthetic pleasure.
    inverted_h = 1.0 - u0  # low entropy = high pleasure potential
    g0 = torch.sigmoid(
        0.35 * inverted_h * u1.clamp(min=0.1)
        + 0.35 * pleas_val * pleasantness.clamp(min=0.1)
        + 0.30 * u2 * dist_concentration.clamp(min=0.1)
    )

    # -- G1: Goldilocks Zone --
    # Whether current H and S values fall in the optimal pleasure zone.
    # Low H + high S = Goldilocks (maximal pleasure). Narrow band indicator.
    # High H + high S = overwhelm (too uncertain + too surprising).
    # Low H + low S = boredom (predictable + unsurprising).
    goldilocks_raw = (1.0 - u0) * u1  # low entropy * high surprise
    g1 = torch.sigmoid(
        0.40 * goldilocks_raw
        + 0.30 * g0 * harm_dev.clamp(min=0.1)
        + 0.30 * u2
    )

    return u0, u1, u2, g0, g1
