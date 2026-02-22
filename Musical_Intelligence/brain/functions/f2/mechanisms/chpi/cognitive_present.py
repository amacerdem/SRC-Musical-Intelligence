"""CHPI P-Layer -- Cognitive Present (3D).

Present-processing harmonic context and cross-modal convergence:
  P0: harmonic_context_strength  (current harmonic expectation strength)
  P1: crossmodal_convergence     (degree of AV/motor convergence)
  P2: voiceleading_smoothness    (present voice-leading quality)

H3 demands consumed:
  harmonic_change:          (6,3,0,2) reused
  sensory_pleasantness:     (4,16,20,0)
  spectral_change:          (21,4,0,0) reused
  chroma_C:                 (25,3,0,2)
  tonalness:                (14,16,1,0)
  chroma_I:                 (33,4,8,0)

R3 direct reads:
  tristimulus[18:21] -- harmonic balance for voice-leading quality
  harmonic_change[6] -- direct chord transition marker

Upstream reads:
  HTP[3]:hierarchy_gradient -- hierarchical prediction strength
  ICEM[0]:information_content -- surprise magnitude
  PWUP[3]:uncertainty_index -- prediction uncertainty
  WMED[0]:entrainment_strength -- temporal entrainment context

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/chpi/
Tillmann 2003: implicit harmonic priming in STG/IFG.
Calvert 2001: STS convergence for cross-modal binding.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_HARMONIC_CHANGE = 6
_TRISTIMULUS_START = 18
_TRISTIMULUS_END = 21

# -- H3 keys consumed ---------------------------------------------------------
_HARM_CHANGE_H3_VAL = (6, 3, 0, 2)
_CONSONANCE_H16_ENTROPY = (4, 16, 20, 0)
_SPEC_CHANGE_H4_VAL = (21, 4, 0, 0)
_CHROMA_C_H3_VAL = (25, 3, 0, 2)
_TONALNESS_H16_MEAN = (14, 16, 1, 0)
_CHROMA_I_H4_VEL = (33, 4, 8, 0)

# -- Upstream dimension indices ------------------------------------------------
_HTP_HIERARCHY_GRADIENT = 3    # HTP E3:hierarchy_gradient
_ICEM_INFORMATION_CONTENT = 0  # ICEM E0:information_content
_PWUP_UNCERTAINTY_INDEX = 3    # PWUP uncertainty_index
_WMED_ENTRAINMENT = 0          # WMED entrainment_strength


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: harmonic context, cross-modal convergence, voice-leading.

    Integrates upstream mechanism outputs (HTP, ICEM, PWUP, WMED) with
    local E/M layer features and H3 temporal context. This is the core
    integration step where cross-modal information converges with harmonic
    prediction signals.

    Tillmann et al. 2003: harmonic context priming in STG/IFG.
    Calvert et al. 2001: superadditive STS responses to congruent AV.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"HTP": (B,T,12), "ICEM": (B,T,13),
                             "PWUP": (B,T,10), "WMED": (B,T,11)}``

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    # -- R3 direct reads --
    harm_change_raw = r3_features[..., _HARMONIC_CHANGE]
    trist_mean = r3_features[..., _TRISTIMULUS_START:_TRISTIMULUS_END].mean(
        dim=-1
    )

    # -- H3 features --
    harm_change_100ms = h3_features[_HARM_CHANGE_H3_VAL]
    consonance_entropy_1s = h3_features[_CONSONANCE_H16_ENTROPY]
    spec_change_125ms = h3_features[_SPEC_CHANGE_H4_VAL]
    chroma_100ms = h3_features[_CHROMA_C_H3_VAL]
    tonalness_mean_1s = h3_features[_TONALNESS_H16_MEAN]
    pitch_vel_125ms = h3_features[_CHROMA_I_H4_VEL]

    # -- Upstream reads --
    htp = upstream_outputs["HTP"]    # (B, T, 12)
    icem = upstream_outputs["ICEM"]  # (B, T, 13)
    pwup = upstream_outputs["PWUP"]  # (B, T, 10)
    wmed = upstream_outputs["WMED"]  # (B, T, 11)

    hierarchy_gradient = htp[..., _HTP_HIERARCHY_GRADIENT]
    information_content = icem[..., _ICEM_INFORMATION_CONTENT]
    uncertainty_index = pwup[..., _PWUP_UNCERTAINTY_INDEX]
    entrainment = wmed[..., _WMED_ENTRAINMENT]

    # -- P0: Harmonic Context Strength --
    # Current harmonic expectation: HTP hierarchy modulates harmonic change
    # detection. Strong tonal context (tonalness + chroma) + low uncertainty
    # = strong harmonic prediction. Surprise weakens confidence.
    # Tillmann 2003: harmonic priming depends on established tonal context.
    p0 = torch.sigmoid(
        0.20 * hierarchy_gradient
        + 0.20 * tonalness_mean_1s
        + 0.20 * chroma_100ms
        + 0.20 * (1.0 - uncertainty_index)
        + 0.20 * m1
    )

    # -- P1: Crossmodal Convergence --
    # Degree of audiovisual/motor convergence in present. Cross-modal gain
    # (E0) + motor lead (M0) + entrainment (temporal alignment) + hierarchy
    # gradient (prediction quality). Consonance entropy modulates: more
    # variable harmonic context = more reliance on cross-modal cues.
    # Calvert 2001: STS superadditive for congruent AV stimuli.
    p1 = torch.sigmoid(
        0.25 * e0
        + 0.25 * m0
        + 0.20 * entrainment
        + 0.15 * hierarchy_gradient
        + 0.15 * consonance_entropy_1s
    )

    # -- P2: Voiceleading Smoothness --
    # Present voice-leading quality. Parsimony (E1) + low spectral change
    # velocity + balanced trist + low pitch velocity + IC modulation
    # (unexpected voice-leading is less smooth).
    # Koelsch 2005: smooth voice-leading correlates with reduced ERAN.
    p2 = torch.sigmoid(
        0.25 * e1
        + 0.20 * trist_mean
        + 0.20 * (1.0 - spec_change_125ms)
        + 0.20 * (1.0 - pitch_vel_125ms)
        + 0.15 * (1.0 - information_content)
    )

    return p0, p1, p2
