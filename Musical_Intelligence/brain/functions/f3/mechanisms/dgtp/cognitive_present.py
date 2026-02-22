"""DGTP P-Layer -- Cognitive Present (2D).

Present-processing integration for domain-general temporal perception:
  P0: music_beat_perception    (current beat perception quality)
  P1: domain_general_timing    (overall domain-general timing precision)

This layer reads upstream BARM and SNEM to incorporate brainstem
modulation and entrainment signals into beat perception:
  BARM[5] = P0:beat_alignment_accuracy -- brainstem beat alignment
  SNEM[6] = P0:beat_locked_activity    -- neural entrainment to beat

H3 demands consumed:
  x_l0l5: (25,16,19,0) coupling stability 1s memory

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/dgtp/
Grahn 2012: SMA/putamen activation for beat perception.
Tierney 2017: domain-general timing precision.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_H16_STAB = (25, 16, 19, 0)  # x_l0l5 stability 1s memory

# -- Upstream output indices ---------------------------------------------------
_BARM_P0_BEAT_ALIGNMENT = 5   # BARM P0:beat_alignment_accuracy
_SNEM_P0_BEAT_LOCKED = 6      # SNEM P0:beat_locked_activity


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute P-layer: present beat perception and domain-general timing.

    P0 integrates music timing (E0) and domain correlation (M0) with
    upstream SNEM beat-locked activity and BARM beat alignment to assess
    current beat perception quality. When entrainment (SNEM) and brainstem
    modulation (BARM) both signal beat alignment, beat perception is strong.

    P1 integrates the shared mechanism (E2) and shared variance (M1) with
    coupling stability to assess overall domain-general timing precision.

    Graceful degradation: if BARM or SNEM are unavailable, their
    contributions are replaced with zero tensors (no upstream = reduced
    confidence, not failure).

    Grahn 2012: beat perception recruits SMA when beat is salient.
    Tierney 2017: domain-general timing precision links music and speech.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        upstream_outputs: ``{"BARM": (B, T, 10), "SNEM": (B, T, 12)}``.

    Returns:
        ``(P0, P1)`` each ``(B, T)``
    """
    e0, _e1, e2 = e
    m0, m1 = m

    coupling_stability_1s = h3_features[_COUPLING_H16_STAB]  # (B, T)

    # -- Upstream reads (graceful degradation) --
    barm = upstream_outputs.get("BARM")
    snem = upstream_outputs.get("SNEM")

    if barm is not None:
        barm_alignment = barm[..., _BARM_P0_BEAT_ALIGNMENT]  # (B, T)
    else:
        barm_alignment = torch.zeros_like(e0)

    if snem is not None:
        snem_beat_locked = snem[..., _SNEM_P0_BEAT_LOCKED]  # (B, T)
    else:
        snem_beat_locked = torch.zeros_like(e0)

    # -- P0: Music Beat Perception --
    # Current beat perception quality: music timing (E0) + domain
    # correlation (M0) + entrainment (SNEM) + brainstem alignment (BARM).
    # Grahn 2012: beat perception depends on subcortical-cortical loop.
    p0 = torch.sigmoid(
        0.30 * e0
        + 0.30 * m0
        + 0.20 * snem_beat_locked
        + 0.20 * barm_alignment
    )

    # -- P1: Domain-General Timing --
    # Overall timing precision across domains: shared mechanism (E2) +
    # shared variance (M1) + coupling stability (sustained precision).
    # Tierney 2017: domain-general timing precision predicts both
    # music and speech performance.
    p1 = torch.sigmoid(
        0.40 * e2
        + 0.30 * m1
        + 0.30 * coupling_stability_1s
    )

    return p0, p1
