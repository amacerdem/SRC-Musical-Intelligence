"""STAI P-Layer -- Cognitive Present (3D).

Present-time spectral-temporal aesthetic integration signals:
  P0: spectral_quality      — Current spectral encoding quality [0, 1]
  P1: temporal_quality      — Current temporal structure quality [0, 1]
  P2: aesthetic_response    — Present-moment aesthetic response [0, 1]

P0 captures the real-time spectral quality encoding in STG and Heschl's
gyrus. Uses consonance features, timbral richness (warmth, tonalness,
tristimulus), and their H3 temporal tracking. High P0 = spectrally rich
and consonant signal currently being processed.

P1 captures the real-time temporal structure quality. Uses temporal flow
signals, aesthetic integration, and interaction strength to assess how well
the temporal structure supports aesthetic response in the current moment.

P2 captures the present-moment aesthetic response -- the real-time output
of the vmPFC value computation. This is the instantaneous aesthetic
experience, driven by the interaction between spectral quality (P0) and
temporal quality (P1). P2 is the primary signal routed to the
aesthetic_judgment belief.

H3 demands consumed (5 tuples):
  (12, 2, 0, 2)  warmth value H2 L2         -- spectral warmth 17ms
  (14, 5, 1, 0)  tonalness mean H5 L0       -- tonalness 46ms
  (18, 2, 0, 2)  tristimulus1 value H2 L2   -- F0 energy 17ms
  (19, 2, 0, 2)  tristimulus2 value H2 L2   -- mid-harmonic energy 17ms
  (20, 2, 0, 2)  tristimulus3 value H2 L2   -- high-harmonic energy 17ms

R3 features:
  [0] roughness, [2] helmholtz_kang, [3] stumpf_fusion,
  [4] sensory_pleasantness, [12] warmth, [14] tonalness,
  [18:21] tristimulus1-3, [7] amplitude, [8] loudness

Koelsch 2014: STG/Heschl's for spectral quality, vmPFC/OFC for value.
Blood & Zatorre 2001: vmPFC activation correlates with aesthetic response.
Kim et al. 2019: Present-moment aesthetic response requires both spectral
and temporal integrity (2x2 factorial).
Menon & Levitin 2005: NAcc activation tracks moment-by-moment pleasure.

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/stai/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_WARMTH_VAL_H2 = (12, 2, 0, 2)        # warmth value H2 L2
_TONAL_MEAN_H5 = (14, 5, 1, 0)        # tonalness mean H5 L0
_TRIST1_VAL_H2 = (18, 2, 0, 2)        # tristimulus1 value H2 L2
_TRIST2_VAL_H2 = (19, 2, 0, 2)        # tristimulus2 value H2 L2
_TRIST3_VAL_H2 = (20, 2, 0, 2)        # tristimulus3 value H2 L2

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_HELMHOLTZ = 2
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 8
_WARMTH = 12
_TONALNESS = 14
_TRISTIMULUS1 = 18
_TRISTIMULUS2 = 19
_TRISTIMULUS3 = 20


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: present-time spectral quality, temporal quality, response.

    P0 (spectral_quality) captures real-time spectral encoding quality.
    Consonance features combined with timbral richness (warmth, tonalness,
    tristimulus distribution). STG + Heschl's gyrus encoding.

    P1 (temporal_quality) captures real-time temporal structure quality.
    Temporal integrity (E1) combined with aesthetic value (M0) and
    interaction strength (M1). Forward flow coherence assessment.

    P2 (aesthetic_response) captures present-moment aesthetic experience.
    Multiplicative coupling of spectral quality (P0) x temporal quality (P1)
    modulated by aesthetic integration (E2) and value (M0). This is the
    primary signal feeding the aesthetic_judgment belief.

    Koelsch 2014: STG/Heschl's for spectral encoding, vmPFC for value.
    Blood & Zatorre 2001: vmPFC activation = aesthetic response.
    Menon & Levitin 2005: moment-by-moment NAcc pleasure tracking.
    Kim et al. 2019: both dimensions required for full response.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1, e2, e3 = e
    m0, m1 = m

    # -- H3 features --
    warmth_val = h3_features[_WARMTH_VAL_H2]        # (B, T)
    tonal_mean = h3_features[_TONAL_MEAN_H5]        # (B, T)
    trist1_val = h3_features[_TRIST1_VAL_H2]        # (B, T)
    trist2_val = h3_features[_TRIST2_VAL_H2]        # (B, T)
    trist3_val = h3_features[_TRIST3_VAL_H2]        # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    helmholtz = r3_features[..., _HELMHOLTZ]              # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]             # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    loudness = r3_features[..., _LOUDNESS]                # (B, T)
    warmth = r3_features[..., _WARMTH]                    # (B, T)
    tonalness = r3_features[..., _TONALNESS]              # (B, T)

    # -- Derived signals --
    # Timbral richness: tristimulus distribution + warmth + tonalness
    timbral_richness = (
        0.25 * trist1_val
        + 0.25 * trist2_val
        + 0.20 * trist3_val
        + 0.15 * warmth_val
        + 0.15 * tonal_mean
    )

    # Consonance composite
    consonance = (
        0.30 * (1.0 - roughness)
        + 0.25 * helmholtz
        + 0.25 * stumpf
        + 0.20 * pleasantness
    )

    # -- P0: Spectral Quality --
    # Present-time spectral encoding quality. Consonance x timbral richness.
    # STG + Heschl's gyrus spectral encoding (Koelsch 2014).
    p0 = torch.sigmoid(
        0.35 * e0 * timbral_richness.clamp(min=0.1)
        + 0.30 * consonance * tonalness
        + 0.20 * warmth * tonal_mean
        + 0.15 * pleasantness * stumpf
    )

    # -- P1: Temporal Quality --
    # Present-time temporal structure quality. Temporal integrity (E1)
    # combined with interaction strength (M1) and energy dynamics.
    # Forward flow coherence drives reward circuit engagement.
    p1 = torch.sigmoid(
        0.35 * e1 * m1.clamp(min=0.1)
        + 0.30 * m0 * amplitude.clamp(min=0.1)
        + 0.20 * e2 * loudness
        + 0.15 * e3
    )

    # -- P2: Aesthetic Response --
    # Present-moment aesthetic experience. Multiplicative coupling of
    # spectral quality (P0) x temporal quality (P1), modulated by
    # aesthetic integration (E2) and value (M0). This is the primary
    # signal routed to aesthetic_judgment belief.
    # Kim 2019: both dimensions required (disrupting either -> ~35%).
    # Blood & Zatorre 2001: vmPFC activation = aesthetic response.
    p2 = torch.sigmoid(
        0.40 * p0 * p1  # spectral x temporal interaction
        + 0.30 * e2 * m0.clamp(min=0.1)
        + 0.30 * m1 * consonance
    )

    return p0, p1, p2
