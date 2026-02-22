"""DAP E-Layer -- Extraction (1D).

Developmental sensitivity feature for affective plasticity:
  E0: dev_sensitiv   -- Developmental sensitivity index [0, 1]

Developmental sensitivity (E0) captures how strongly the current acoustic
signal activates early-formed auditory-limbic templates. Higher consonance
discrimination (low roughness), hedonic response strength (pleasantness),
and arousal baseline (loudness) indicate stronger developmental exposure.
Gated by NEMAC nostalgia signal: nostalgic familiarity amplifies
sensitivity to childhood-relevant timbral/harmonic features.

Trainor 2005: Infants show preference for consonant over dissonant
intervals by 2 months; critical period for auditory cortex A1/STG.

H3 demands consumed (3):
  (4, 16, 0, 2)  sensory_pleasantness value H16 L2  -- hedonic maturation
  (0, 16, 0, 2)  roughness value H16 L2             -- consonance disc.
  (10, 16, 0, 2) loudness value H16 L2              -- arousal baseline

R3 inputs: roughness[0], sensory_pleasantness[4], loudness[10],
           tonalness[14], x_l0l5[25:33]

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/dap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_VAL_H16 = (4, 16, 0, 2)     # sensory_pleasantness value H16 L2
_ROUGH_VAL_H16 = (0, 16, 0, 2)        # roughness value H16 L2
_LOUD_VAL_H16 = (10, 16, 0, 2)        # loudness value H16 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_TONALNESS = 14
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- NEMAC upstream index ------------------------------------------------------
_NEMAC_NOSTALGIA_IDX = 1  # E1:nostalgia in NEMAC 11D output


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor]:
    """Compute E-layer: 1D developmental sensitivity.

    E0 (dev_sensitiv): Developmental sensitivity from consonance
    discrimination (low roughness), hedonic strength (pleasantness),
    arousal baseline (loudness), and tonal template (tonalness).
    NEMAC nostalgia gates the signal: nostalgic warmth amplifies
    developmental responsiveness.

    Trainor 2005: Consonance preference emerges by 2 months; critical
    period plasticity in A1/STG. Trehub et al. 2015: Parental singing
    establishes music-emotion binding templates.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"NEMAC": (B, T, 11), ...}``.

    Returns:
        ``(E0,)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    pleasant_val = h3_features[_PLEASANT_VAL_H16]          # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H16]                # (B, T)
    loud_val = h3_features[_LOUD_VAL_H16]                  # (B, T)

    # -- R3 features --
    tonalness = r3_features[..., _TONALNESS]               # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- NEMAC nostalgia (cross-depth upstream) --
    nemac = upstream_outputs.get(
        "NEMAC", torch.zeros(B, T, 11, device=device),
    )
    nostalgia = nemac[..., _NEMAC_NOSTALGIA_IDX]           # (B, T)

    # -- E0: Developmental Sensitivity --
    # sigma(0.25*(1-rough) + 0.25*pleasant + 0.15*loud + 0.15*tonal
    #       + 0.10*x_l0l5.mean + 0.10*nostalgia)
    # Trainor 2005: consonance discrimination = developmental marker
    # Trehub 2015: parental singing templates
    e0 = torch.sigmoid(
        0.25 * (1.0 - rough_val)
        + 0.25 * pleasant_val
        + 0.15 * loud_val
        + 0.15 * tonalness
        + 0.10 * x_l0l5.mean(dim=-1)
        + 0.10 * nostalgia
    )

    return (e0,)
