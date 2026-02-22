"""DAP D-Layer -- Temporal Integration (4D).

Developmental dynamics for affective plasticity:
  D0: critical_period      -- Critical period window activation [0, 1]
  D1: plasticity_coeff     -- Current neural plasticity coefficient [0, 1]
  D2: exposure_history     -- Cumulative exposure history proxy [0, 1]
  D3: neural_maturation    -- Neural maturation level [0, 1]

Critical period (D0) estimates the activation of developmental time
windows for auditory-limbic plasticity. Higher when acoustic features
match infant/early-childhood sensitivity profiles (strong consonance,
clear tonality, moderate arousal). Knudsen 2004: sensitive periods in
neural development.

Plasticity coefficient (D1) tracks the current capacity for affective
learning. High when pleasantness variability (H3 std) is elevated —
indicating the system is still discriminating/exploring hedonic space.
Hensch 2005: molecular brakes on critical period plasticity.

Exposure history (D2) accumulates evidence of prior musical exposure
from predictability (low entropy = familiar patterns) and developmental
sensitivity (E0). Hannon & Trehub 2005: culture-specific rhythm
exposure by 12 months.

Neural maturation (D3) estimates auditory cortex maturation from arousal
dynamics (loudness velocity) weighted by developmental sensitivity.
Chang & Merzenich 2003: critical period for tonotopic map refinement.

H3 demands consumed (3):
  (4, 16, 2, 2)  sensory_pleasantness std H16 L2  -- response variability
  (22, 16, 20, 2) distribution_entropy entropy H16 L2 -- predictability
  (10, 16, 8, 0) loudness velocity H16 L0          -- arousal dynamics

R3 inputs: roughness[0], sensory_pleasantness[4], tonalness[14],
           entropy[22], x_l0l5[25:33]

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/dap/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_STD_H16 = (4, 16, 2, 2)      # sensory_pleasantness std H16 L2
_ENTROPY_ENT_H16 = (22, 16, 20, 2)     # distribution_entropy entropy H16 L2
_LOUD_VEL_H16 = (10, 16, 8, 0)         # loudness velocity H16 L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_TONALNESS = 14
_ENTROPY = 22
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """Compute D-layer: 4D developmental dynamics.

    D0 (critical_period): Critical period window from consonance
    discrimination, tonal clarity, and moderate arousal. Stronger
    signal = acoustic features that match infant sensitive-period profiles.
    Knudsen 2004: sensitive periods.

    D1 (plasticity_coeff): Neural plasticity from hedonic response
    variability (pleasantness std) and entropy. High variability =
    still exploring hedonic space = higher plasticity.
    Hensch 2005: critical period molecular regulation.

    D2 (exposure_history): Cumulative exposure from low entropy
    (familiar patterns) modulated by developmental sensitivity (E0).
    Hannon & Trehub 2005: culture-specific exposure by 12 months.

    D3 (neural_maturation): Auditory cortex maturation from arousal
    dynamics (loudness velocity) and developmental sensitivity.
    Chang & Merzenich 2003: tonotopic map refinement.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0,)`` from extraction layer.
        upstream_outputs: ``{"NEMAC": (B, T, 11), ...}``.

    Returns:
        ``(D0, D1, D2, D3)`` each ``(B, T)``.
    """
    (e0,) = e_outputs

    # -- H3 features --
    pleasant_std = h3_features[_PLEASANT_STD_H16]           # (B, T)
    entropy_ent = h3_features[_ENTROPY_ENT_H16]             # (B, T)
    loud_vel = h3_features[_LOUD_VEL_H16]                   # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]                # (B, T)
    pleasantness = r3_features[..., _PLEASANTNESS]          # (B, T)
    tonalness = r3_features[..., _TONALNESS]                # (B, T)
    entropy = r3_features[..., _ENTROPY]                    # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- D0: Critical Period --
    # sigma(0.30*(1-rough) + 0.30*tonal + 0.20*pleasant + 0.20*x_l0l5.mean)
    # Knudsen 2004: sensitive periods for neural development
    # Trainor 2005: consonance preference as critical period marker
    d0 = torch.sigmoid(
        0.30 * (1.0 - roughness)
        + 0.30 * tonalness
        + 0.20 * pleasantness
        + 0.20 * x_l0l5.mean(dim=-1)
    )

    # -- D1: Plasticity Coefficient --
    # sigma(0.40*pleasant_std + 0.30*entropy_ent + 0.30*e0)
    # Hensch 2005: plasticity = exploration in hedonic space
    # High std = system still discriminating = higher plasticity
    d1 = torch.sigmoid(
        0.40 * pleasant_std
        + 0.30 * entropy_ent
        + 0.30 * e0
    )

    # -- D2: Exposure History --
    # sigma(0.40*(1-entropy) + 0.30*e0 + 0.30*tonal)
    # Hannon & Trehub 2005: culture-specific musical exposure by 12 months
    # Low entropy = familiar patterns = evidence of prior exposure
    d2 = torch.sigmoid(
        0.40 * (1.0 - entropy)
        + 0.30 * e0
        + 0.30 * tonalness
    )

    # -- D3: Neural Maturation --
    # sigma(0.35*loud_vel + 0.35*e0 + 0.30*d0)
    # Chang & Merzenich 2003: critical period tonotopic refinement
    # Arousal dynamics (loudness velocity) reflect neural responsiveness
    d3 = torch.sigmoid(
        0.35 * loud_vel
        + 0.35 * e0
        + 0.30 * d0
    )

    return d0, d1, d2, d3
