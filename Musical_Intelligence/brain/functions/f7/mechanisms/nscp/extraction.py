"""NSCP E-Layer -- Extraction (3D).

Neural synchrony features for the ISC-to-commercial-success pathway:
  E0: f22_neural_synchrony      -- ISC proxy from coherence + consonance [0, 1]
  E1: f23_commercial_prediction -- Streaming popularity proxy [0, 1]
  E2: f24_catchiness_index      -- Population motor entrainment [0, 1]

Neural synchrony (E0) is an inter-subject correlation (ISC) proxy that
combines cross-layer coherence periodicity at 1s with harmonic consonance.
Leeuwis 2021: ISC predicts commercial success (R^2 = 0.619 combined).
Hasson 2004: ISC in cortical responses is reliable and content-driven.

Commercial prediction (E1) combines ISC magnitude (E0) with multi-feature
binding periodicity. Leeuwis 2021: 1% ISC increase ~ 2.4M Spotify streams.
Berns 2010: NAcc activity predicts future song sales (r = 0.33).

Catchiness index (E2) captures population motor entrainment via onset
periodicity and loudness entropy. Spiech 2022: inverted-U syncopation-groove
relationship (F(1,29)=10.515, p=.003). Sarasso 2019: consonance enhances
motor inhibition and aesthetic engagement (eta^2=0.685).

H3 demands consumed (5):
  (25, 16, 14, 2) coherence periodicity 1s L2  -- ISC proxy
  (3, 3, 0, 2)    consonance value 100ms L2     -- synchrony quality
  (33, 16, 14, 2) binding periodicity 1s L2     -- commercial prediction
  (10, 16, 14, 2) onset periodicity 1s L2       -- catchiness
  (8, 3, 20, 2)   loudness entropy 100ms L2     -- engagement

R3 inputs: stumpf[3], loudness[8], spectral_flux[10],
           x_l0l5[25:33], x_l4l5[33:41]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/nscp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_COHERENCE_PERIOD_1S = (25, 16, 14, 2)   # x_l0l5 periodicity H16 L2
_CONSONANCE_VAL_100MS = (3, 3, 0, 2)     # stumpf value H3 L2
_BINDING_PERIOD_1S = (33, 16, 14, 2)     # x_l4l5 periodicity H16 L2
_ONSET_PERIOD_1S = (10, 16, 14, 2)       # spectral_flux periodicity H16 L2
_LOUDNESS_ENT_100MS = (8, 3, 20, 2)      # loudness entropy H3 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_STUMPF = 3
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute E-layer: 3D neural synchrony extraction features.

    E0 (f22_neural_synchrony): ISC proxy from cross-layer coherence
    periodicity (1s) and harmonic consonance (100ms). The 1s coherence
    periodicity captures the temporal scale at which EEG ISC was measured
    in Leeuwis 2021.
    Leeuwis 2021: ISC R^2=0.404 early, R^2=0.619 combined.

    E1 (f23_commercial_prediction): Streaming popularity proxy from ISC
    magnitude (E0) combined with multi-feature binding periodicity.
    Songs with consistent multi-feature binding synchronize brains more
    reliably.
    Leeuwis 2021: 1% ISC increase ~ 2.4M more Spotify streams.

    E2 (f24_catchiness_index): Population motor entrainment from onset
    periodicity (beat regularity) and loudness entropy (dynamic
    unpredictability). Reflects Spiech 2022 inverted-U: moderate
    rhythmic complexity maximizes groove.
    Spiech 2022: F(1,29)=10.515, p=.003.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"ASAP": (B, T, 11), "DDSMI": (B, T, 11)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    coherence_period = h3_features[_COHERENCE_PERIOD_1S]     # (B, T)
    consonance_val = h3_features[_CONSONANCE_VAL_100MS]      # (B, T)
    binding_period = h3_features[_BINDING_PERIOD_1S]          # (B, T)
    onset_period = h3_features[_ONSET_PERIOD_1S]              # (B, T)
    loudness_ent = h3_features[_LOUDNESS_ENT_100MS]           # (B, T)

    # -- E0: Neural Synchrony (f22) --
    # sigma(0.40 * coherence_period_1s + 0.30 * consonance_100ms)
    # Leeuwis 2021: ISC predicts commercial success
    # Hasson 2004: ISC content-driven and reliable
    e0 = torch.sigmoid(
        0.40 * coherence_period
        + 0.30 * consonance_val
    )

    # -- E1: Commercial Prediction (f23) --
    # sigma(0.40 * f22 + 0.30 * binding_period_1s)
    # Leeuwis 2021: combined ISC model R^2=0.619
    # Berns 2010: NAcc activity predicts future sales
    e1 = torch.sigmoid(
        0.40 * e0
        + 0.30 * binding_period
    )

    # -- E2: Catchiness Index (f24) --
    # sigma(0.35 * onset_period_1s + 0.30 * loudness_entropy)
    # Spiech 2022: inverted-U syncopation-groove (F(1,29)=10.515)
    # Sarasso 2019: consonance enhances motor inhibition (eta^2=0.685)
    e2 = torch.sigmoid(
        0.35 * onset_period
        + 0.30 * loudness_ent
    )

    return (e0, e1, e2)
