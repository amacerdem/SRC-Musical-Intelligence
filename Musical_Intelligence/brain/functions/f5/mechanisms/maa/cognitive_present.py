"""MAA P-Layer -- Cognitive Present (3D).

Present-processing pattern search, context assessment, and aesthetic evaluation:
  P0: pattern_search       -- Active search for structure in atonal material [0, 1]
  P1: context_assessment   -- Cognitive framing context (artistic vs popular) [0, 1]
  P2: aesthetic_evaluation -- Running aesthetic judgement integrating E-layer [0, 1]

Pattern search (P0) models the listener's active attempt to find patterns
in complex/atonal music. Higher when tonalness is low (more atonal) and
coupling pathway is active (searching for structure). Right Heschl's Gyrus
shows heightened response under tonal uncertainty (Bianco 2020: MEG, N=24).

Context assessment (P1) provides the framing context that modulates
appreciation. Uses E-layer framing effect (E2) combined with the
appreciation pathway (x_l5l7) and VMM mode signal for emotional context.
Huang 2016: arMFC activation for artistic framing.

Aesthetic evaluation (P2) integrates all E-layer outputs with current
sensory context to produce a running aesthetic judgement. The appreciation
composite (E3) is weighted by coupling strength and goldilocks reference.
Routes to atonal_appreciation belief (Anticipation).

H3 demands consumed (3):
  (14, 8, 1, 0)   tonalness mean H8 L0    -- current tonal clarity 500ms
  (41, 8, 0, 0)   x_l5l7[0] value H8 L0   -- current coupling 500ms
  (41, 16, 1, 0)  x_l5l7[0] mean H16 L0   -- sustained coupling 1s

R3 inputs: tonalness[14], x_l5l7[41:49]

Upstream: PUPF[6] (goldilocks_zone), VMM[1] (mode_signal)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_TONAL_MEAN_H8 = (14, 8, 1, 0)         # tonalness mean H8 L0
_COUPLING_VAL_H8 = (41, 8, 0, 0)       # x_l5l7[0] value H8 L0
_COUPLING_MEAN_H16 = (41, 16, 1, 0)    # x_l5l7[0] mean H16 L0

# -- R3 feature indices -------------------------------------------------------
_TONALNESS = 14
_X_L5L7_START = 41
_X_L5L7_END = 49

# -- Upstream indices ----------------------------------------------------------
_PUPF_GOLDILOCKS = 6    # PUPF.goldilocks_zone (G1)
_VMM_MODE_SIGNAL = 1    # VMM.mode_signal (V1)


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute P-layer: pattern search, context assessment, aesthetic evaluation.

    P0 (pattern_search): Active pattern search driven by low tonalness
    (atonality triggers search) and coupling pathway activity. When
    tonalness is low, Right Heschl's Gyrus shows heightened response
    (Bianco 2020: MEG, N=24). Searching for structure in chaos.

    P1 (context_assessment): Cognitive framing context from E2 (framing
    effect), coupling pathway, and VMM mode signal. Provides the
    artistic-vs-popular framing that modulates appreciation.
    Huang 2016: arMFC activation for artistic framing.

    P2 (aesthetic_evaluation): Running aesthetic judgement integrating
    E3 (appreciation composite) with sustained coupling and goldilocks
    reference. Routes to atonal_appreciation belief.
    Cheung 2019 + Huang 2016: pleasure = complexity x familiarity x framing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        upstream_outputs: ``{"PUPF": (B, T, 12), "VMM": (B, T, 12)}``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    e0, _e1, e2, e3 = e
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    tonal_mean_h8 = h3_features[_TONAL_MEAN_H8]            # (B, T)
    coupling_val = h3_features[_COUPLING_VAL_H8]            # (B, T)
    coupling_mean = h3_features[_COUPLING_MEAN_H16]         # (B, T)

    # -- R3 features --
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)
    x_l5l7_mean = x_l5l7.mean(dim=-1)                      # (B, T)

    # -- Upstream features --
    pupf = upstream_outputs.get("PUPF", torch.zeros(B, T, 12, device=device))
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    goldilocks_ref = torch.sigmoid(pupf[..., _PUPF_GOLDILOCKS])  # (B, T)
    mode_signal = vmm[..., _VMM_MODE_SIGNAL]                     # (B, T)

    # -- P0: Pattern Search --
    # High when tonalness is low (atonal = searching for structure) and
    # coupling pathway is active (listener engaged in search).
    # sigma(0.40*(1-tonalness) + 0.30*coupling_val + 0.30*E0)
    # Bianco 2020: Right Heschl's Gyrus heightened under tonal uncertainty
    # Mencke 2019: musicians show higher pattern search for complex music
    p0 = torch.sigmoid(
        0.40 * (1.0 - tonal_mean_h8)
        + 0.30 * coupling_val
        + 0.30 * e0
    )

    # -- P1: Context Assessment --
    # Cognitive framing context from E2, appreciation pathway, and mode.
    # sigma(0.40*E2 + 0.30*x_l5l7.mean + 0.30*mode_signal)
    # Huang 2016: arMFC activation for artistic framing (fMRI, N=21)
    p1 = torch.sigmoid(
        0.40 * e2
        + 0.30 * x_l5l7_mean
        + 0.30 * mode_signal
    )

    # -- P2: Aesthetic Evaluation --
    # Running aesthetic judgement from E3 (composite) weighted by sustained
    # coupling and goldilocks reference proximity.
    # sigma(0.40*E3 + 0.30*coupling_mean + 0.30*goldilocks_ref)
    # Routes to atonal_appreciation belief (Anticipation)
    # Cheung 2019: NAcc beta=0.242 for uncertainty-pleasure link
    p2 = torch.sigmoid(
        0.40 * e3
        + 0.30 * coupling_mean
        + 0.30 * goldilocks_ref
    )

    return p0, p1, p2
