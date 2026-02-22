"""STAI M-Layer -- Temporal Integration (2D).

Spectral-Temporal Aesthetic Integration integration signals:
  M0: aesthetic_value                — Composite aesthetic value signal [0, 1]
  M1: spectral_temporal_interaction  — Interaction strength metric [0, 1]

M0 integrates spectral integrity, temporal integrity, and their interaction
into a single aesthetic value signal. This is the core aesthetic judgment
metric -- the brain's assessment of how aesthetically valuable the current
stimulus is. Driven by vmPFC value computation (Koelsch 2014) and modulated
by consonance quality + temporal flow.

M1 quantifies the degree of spectral-temporal interaction. When both spectral
and temporal dimensions are intact, M1 is high; when either is disrupted, M1
drops. This captures the Kim 2019 finding that the aesthetic response is
inherently interactive -- not the sum of independent contributions. The
rostral ACC mediates this interaction (Kim 2019: T=6.852).

H3 demands consumed (0 new tuples -- M-layer reuses E-layer H3 features
through the E-layer output signals passed as arguments).

R3 features:
  [0] roughness, [2] helmholtz_kang, [3] stumpf_fusion,
  [4] sensory_pleasantness, [7] amplitude, [33:41] x_l4l5

Kim et al. 2019: Spectral x temporal interaction at rACC (T=6.852, N=20).
Blood & Zatorre 2001: vmPFC value computation for pleasant music (PET N=10).
Menon & Levitin 2005: NAcc/caudate activation correlates with aesthetic
value (fMRI N=13).

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/stai/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- R3 feature indices -------------------------------------------------------
_ROUGHNESS = 0
_HELMHOLTZ = 2
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: integrated aesthetic value and interaction strength.

    M0 (aesthetic_value) integrates spectral integrity (E0), temporal integrity
    (E1), and their interaction (E2) into a composite value signal. vmPFC
    value computation (Koelsch 2014). Consonance quality and binding provide
    perceptual grounding.

    M1 (spectral_temporal_interaction) measures the degree of interaction
    between spectral and temporal dimensions. Captures the Kim 2019 finding
    that aesthetic response requires both dimensions intact. rACC mediates
    this interaction (T=6.852). High M1 = strong bidimensional coupling.

    Kim et al. 2019: rACC mediates spectral x temporal interaction (T=6.852).
    Menon & Levitin 2005: NAcc/caudate activation from aesthetic value.
    Blood & Zatorre 2001: vmPFC value computation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        r3_features: ``(B, T, 97)``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2, e3 = e

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    helmholtz = r3_features[..., _HELMHOLTZ]              # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]             # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                    # (B, T)

    # -- Derived signals --
    # Consonance composite (same as E-layer for consistency)
    consonance = (
        0.30 * (1.0 - roughness)
        + 0.25 * helmholtz
        + 0.25 * stumpf
        + 0.20 * pleasantness
    )

    # -- M0: Aesthetic Value --
    # Composite aesthetic value integrating spectral, temporal, and interaction.
    # vmPFC value computation (Koelsch 2014). NAcc/caudate reward signal
    # (Menon & Levitin 2005). The interaction (E2) contributes most because
    # aesthetic response is supra-additive.
    m0 = torch.sigmoid(
        0.35 * e2 * consonance.clamp(min=0.1)
        + 0.30 * e0 * e1
        + 0.20 * pleasantness * amplitude
        + 0.15 * e3 * x_l4l5_mean
    )

    # -- M1: Spectral-Temporal Interaction --
    # Degree of interaction between spectral and temporal dimensions.
    # rACC mediates this interaction (Kim 2019: T=6.852).
    # High M1 when both dimensions contribute; low when either is disrupted.
    # Implemented as geometric mean of spectral and temporal integrity,
    # modulated by connectivity strength.
    spectral_temporal_coupling = e0 * e1  # multiplicative interaction

    m1 = torch.sigmoid(
        0.40 * spectral_temporal_coupling
        + 0.30 * e3 * e2.clamp(min=0.1)
        + 0.30 * x_l4l5_mean * consonance
    )

    return m0, m1
