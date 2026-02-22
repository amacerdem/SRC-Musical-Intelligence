"""IGFE P-Layer -- Cognitive Present (3D).

Present-state gamma synchronization, dose accumulation, and memory access:
  P0: gamma_synchronization  (real-time gamma phase-locking strength)
  P1: dose_accumulation      (cumulative entrainment dose in present)
  P2: memory_access          (gamma-facilitated memory retrieval)

H3 demands consumed:
  chroma_C:      (25,0,0,2), (25,1,0,2), (25,3,14,2), (25,16,14,2)
  H_coupling:    (41,8,0,0), (41,16,1,0)
  onset_strength: (11,0,0,2) reused

R3 direct reads:
  warmth:    [12] -- spectral center proxy for frequency alignment

Upstream reads:
  WMED[1] -- wm_contribution (working memory baseline)
  HTP[3]  -- hierarchy_gradient (prediction context)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/igfe/
Galambos 1981: 40 Hz ASSR phase-locking at fronto-central sites.
Pastor 2002: gamma phase-locking predicts memory recall.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 indices ---------------------------------------------------------------
_WARMTH = 12              # spectral center proxy

# -- H3 keys consumed ---------------------------------------------------------
_CHROMA_H0_VAL = (25, 0, 0, 2)       # chroma_C 25ms value integration
_CHROMA_H1_VAL = (25, 1, 0, 2)       # chroma_C 50ms value integration
_CHROMA_H3_PERIOD = (25, 3, 14, 2)   # chroma_C 100ms periodicity integration
_CHROMA_H16_PERIOD = (25, 16, 14, 2) # chroma_C 1s periodicity integration

_H_COUPLING_H8_VAL = (41, 8, 0, 0)   # H_coupling 500ms value memory
_H_COUPLING_H16_MEAN = (41, 16, 1, 0)  # H_coupling 1s mean memory

_ONSET_H0_VAL = (11, 0, 0, 2)        # onset_strength 25ms value integration

# -- Upstream indices ----------------------------------------------------------
_WMED_WM_CONTRIBUTION_IDX = 1   # WMED E1:wm_contribution
_HTP_HIERARCHY_GRADIENT_IDX = 3  # HTP E3:hierarchy_gradient


def compute_cognitive_present(
    r3_features: Tensor,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: gamma synchronization, dose, and memory access.

    Integrates chroma coupling (frequency-specific entrainment), cognitive
    coupling (hippocampal/frontal binding), and upstream WM/hierarchy
    context to assess present-moment gamma enhancement state.

    Galambos 1981: 40 Hz ASSR maximal at fronto-central electrodes.
    Pastor 2002: hippocampal gamma phase-locking predicts recall.
    Polanía 2012: fronto-parietal gamma coupling enhances WM.

    Args:
        r3_features: ``(B, T, 97)`` raw R3.
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"HTP": (B, T, 12), "WMED": (B, T, 11)}``

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``
    """
    e0, e1 = e
    m0, m1 = m

    warmth = r3_features[..., _WARMTH]

    # H3 features -- chroma coupling
    chroma_25ms = h3_features[_CHROMA_H0_VAL]
    chroma_50ms = h3_features[_CHROMA_H1_VAL]
    chroma_period_100ms = h3_features[_CHROMA_H3_PERIOD]
    chroma_period_1s = h3_features[_CHROMA_H16_PERIOD]

    # H3 features -- cognitive coupling
    h_coupling_500ms = h3_features[_H_COUPLING_H8_VAL]
    h_coupling_1s = h3_features[_H_COUPLING_H16_MEAN]

    onset_25ms = h3_features[_ONSET_H0_VAL]

    # -- Upstream reads --
    htp = upstream_outputs["HTP"]    # (B, T, 12)
    wmed = upstream_outputs["WMED"]  # (B, T, 11)

    wm_baseline = wmed[..., _WMED_WM_CONTRIBUTION_IDX]
    hierarchy_grad = htp[..., _HTP_HIERARCHY_GRADIENT_IDX]

    # -- P0: Gamma Synchronization --
    # Real-time gamma phase-locking: fast chroma coupling (25-50ms) captures
    # instantaneous frequency-specific entrainment, gated by IGF match (E0).
    # Onset strength adds event-locked synchronization.
    # Galambos 1981: ASSR peaks at 40 Hz with precise phase-locking.
    gamma_coupling = 0.35 * chroma_25ms + 0.35 * chroma_50ms + 0.30 * onset_25ms
    p0 = torch.sigmoid(
        0.40 * gamma_coupling
        + 0.30 * e0
        + 0.15 * warmth
        + 0.15 * hierarchy_grad
    )

    # -- P1: Dose Accumulation --
    # Cumulative entrainment in the present: sustained chroma periodicity
    # (100ms-1s) captures ongoing frequency-locked stimulation. M1 dose
    # carries temporal history.
    # Bolland 2025: dose-response follows saturation curve.
    sustained_entrain = 0.50 * chroma_period_100ms + 0.50 * chroma_period_1s
    p1 = torch.sigmoid(
        0.35 * sustained_entrain
        + 0.35 * m1
        + 0.15 * e1
        + 0.15 * h_coupling_1s
    )

    # -- P2: Memory Access --
    # Gamma-facilitated memory retrieval: cognitive coupling (hippocampal
    # binding) combined with WM baseline and executive enhancement state.
    # Pastor 2002: gamma phase-locking predicts memory recall.
    # Polanía 2012: WM capacity enhanced by gamma tACS.
    cog_coupling = 0.50 * h_coupling_500ms + 0.50 * h_coupling_1s
    p2 = torch.sigmoid(
        0.30 * cog_coupling
        + 0.25 * m0
        + 0.25 * wm_baseline
        + 0.20 * p0
    )

    return p0, p1, p2
