"""TAR E-Layer -- Extraction (1D).

Therapeutic state extraction feature:
  E0: therapeutic   -- Overall therapeutic potential of current sound [0, 1]

Combines anxiolytic indicators (consonance, low arousal, slow tempo) with
antidepressant indicators (positive valence, reward activation) and
upstream cross-modal integration to estimate the instantaneous therapeutic
potential of the current musical frame.

The anxiolytic pathway tracks consonance (low roughness), soft dynamics
(low loudness), and slow tempo (low velocity). The antidepressant
pathway tracks hedonic tone (pleasantness) and reward (SRP.pleasure).
CMAT.cross_modal provides cross-modal binding context.

Chanda & Levitin (2013): Music modulates stress hormones and
neurotransmitters; anxiolytic effects via PNS activation.

Koelsch (2014): Consonant music downregulates amygdala threat response;
dissonance activates fear/anxiety circuits.

H3 demands consumed (5):
  (4, 6, 0, 2)   sensory_pleasantness value H6 L2   -- fast mood state
  (4, 16, 0, 2)  sensory_pleasantness value H16 L2  -- slow mood state
  (0, 6, 0, 2)   roughness value H6 L2              -- consonance for anxiety
  (10, 6, 0, 2)  loudness value H6 L2               -- arousal for dynamics
  (8, 6, 8, 0)   velocity_A velocity H6 L0          -- tempo proxy

R3 inputs: roughness[0], sensory_pleasantness[4], harmonicity[5],
           warmth[16], x_l4l5[33:41]

Upstream inputs: SRP.pleasure (idx 15), CMAT.cross_modal (idx 0)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/0_mechanisms-orchestrator.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_VAL_H6 = (4, 6, 0, 2)       # sensory_pleasantness value H6 L2
_PLEASANT_VAL_H16 = (4, 16, 0, 2)     # sensory_pleasantness value H16 L2
_ROUGH_VAL_H6 = (0, 6, 0, 2)          # roughness value H6 L2
_LOUD_VAL_H6 = (10, 6, 0, 2)          # loudness value H6 L2
_VELOA_VEL_H6 = (8, 6, 8, 0)          # velocity_A velocity H6 L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_HARMONICITY = 5
_WARMTH = 16
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor]:
    """Compute E-layer: 1D therapeutic state feature.

    E0 (therapeutic): Overall therapeutic potential combining anxiolytic
    indicators (consonance, low arousal, slow tempo) and antidepressant
    indicators (positive valence, reward, cross-modal binding).

    Anxiolytic component: high consonance (1 - roughness) + low arousal
    (1 - loudness) + slow tempo (1 - velocity). Consonant, soft, slow
    music activates PNS and downregulates amygdala.
    Chanda & Levitin (2013): cortisol decrease via PNS activation.

    Antidepressant component: hedonic tone (pleasantness) + reward
    (SRP.pleasure) + warmth (comfort signal). Positive-valence music
    activates NAcc DA circuits.
    Koelsch (2014): NAcc reward response to consonant music.

    Cross-modal: CMAT provides binding strength across modalities,
    enhancing therapeutic engagement through immersive experience.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"SRP": (B,T,19), "CMAT": (B,T,10), ...}``.

    Returns:
        ``(E0,)`` -- single tensor ``(B, T)``.
    """
    B, T, _ = r3_features.shape
    device = r3_features.device

    # -- H3 features --
    pleasant_fast = h3_features[_PLEASANT_VAL_H6]      # (B, T)
    pleasant_slow = h3_features[_PLEASANT_VAL_H16]      # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H6]              # (B, T)
    loud_val = h3_features[_LOUD_VAL_H6]                # (B, T)
    veloa_vel = h3_features[_VELOA_VEL_H6]              # (B, T)

    # -- R3 features --
    warmth = r3_features[..., _WARMTH]                  # (B, T)
    harmonicity = r3_features[..., _HARMONICITY]        # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)

    # -- Upstream: SRP.pleasure (P2, idx 15), CMAT.cross_modal (E0, idx 0) --
    srp = upstream_outputs.get("SRP", torch.zeros(B, T, 19, device=device))
    pleasure = srp[..., 15]                             # (B, T)
    cmat = upstream_outputs.get("CMAT", torch.zeros(B, T, 10, device=device))
    cross_modal = cmat[..., 0]                          # (B, T)

    # -- Anxiolytic component --
    # High consonance (low roughness) + low arousal (low loudness) +
    # slow tempo (low velocity) + harmonic purity
    anxiolytic = (
        0.30 * (1.0 - rough_val)
        + 0.25 * (1.0 - loud_val)
        + 0.25 * (1.0 - veloa_vel.abs().clamp(0.0, 1.0))
        + 0.20 * harmonicity
    )

    # -- Antidepressant component --
    # Positive valence (pleasantness) + reward (SRP.pleasure) + warmth
    # + therapeutic engagement (x_l4l5 coupling)
    antidepressant = (
        0.30 * (0.50 * pleasant_fast + 0.50 * pleasant_slow)
        + 0.25 * pleasure
        + 0.25 * warmth
        + 0.20 * x_l4l5.mean(dim=-1)
    )

    # -- E0: Therapeutic potential --
    # sigma(0.40 * anxiolytic + 0.40 * antidepressant + 0.20 * cross_modal)
    # Balanced integration of both pathways with cross-modal enhancement
    e0 = torch.sigmoid(
        0.40 * anxiolytic
        + 0.40 * antidepressant
        + 0.20 * cross_modal
    )

    return (e0,)
