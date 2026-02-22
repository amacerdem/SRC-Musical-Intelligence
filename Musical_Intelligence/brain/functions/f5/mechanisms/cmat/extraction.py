"""CMAT E-Layer -- Extraction (1D).

Cross-modal affective transfer potential:
  E0: cross_modal  -- Cross-modal mapping strength [0, 1]

Cross-modal mapping (E0) estimates the degree to which auditory features
map onto other modalities (primarily visual). High pitch corresponds to
brightness (Spence 2011: r=0.72, meta, 15 studies, N=1200+), high
consonance corresponds to positive valence across modalities, and
spectral warmth maps to color temperature (Palmer et al. 2013: N=30).

In audio-only mode, E0 acts as a "transfer potential" score: how
strongly the current acoustic state would evoke cross-modal percepts
if visual/tactile modalities were present. Uses upstream VMM.valence_state
to anchor the mapping in established valence context.

H3 demands consumed (3):
  (4, 6, 0, 2)  sensory_pleasantness value H6 L2  -- fast affect state
  (0, 6, 0, 2)  roughness value H6 L2             -- instant dissonance
  (10, 6, 0, 2) loudness value H6 L2              -- arousal for salience

R3 inputs: roughness[0], sensory_pleasantness[4], loudness[10],
           brightness[15], warmth[16], x_l0l5[25:33]

Upstream: VMM.valence_state (idx 11 of 12D)

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/cmat/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEAS_VAL_H6 = (4, 6, 0, 2)       # sensory_pleasantness value H6 L2
_ROUGH_VAL_H6 = (0, 6, 0, 2)       # roughness value H6 L2
_LOUD_VAL_H6 = (10, 6, 0, 2)       # loudness value H6 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_PLEASANTNESS = 4
_LOUDNESS = 10
_BRIGHTNESS = 15
_WARMTH = 16
_X_L0L5_START = 25
_X_L0L5_END = 33

# -- Upstream dimension indices ------------------------------------------------
_VMM_VALENCE_STATE = 11  # VMM output idx 11 = valence_state (of 12D)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor]:
    """Compute E-layer: 1D cross-modal affective transfer potential.

    E0 (cross_modal): Estimates supramodal transfer strength from the
    convergence of pitch-brightness mapping (R3 brightness weighted by
    fast affect H3), consonance-valence axis (1-roughness * pleasantness),
    and warmth-color correspondence. Anchored by VMM valence context.

    Spence 2011: pitch-brightness r=0.72 (meta, N=1200+).
    Palmer et al. 2013: mode-color mediated by emotion (N=30).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        upstream_outputs: ``{"VMM": (B, T, 12), "AAC": (B, T, 14)}``.

    Returns:
        ``(E0,)`` where E0 is ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    pleas_val = h3_features[_PLEAS_VAL_H6]             # (B, T)
    rough_val = h3_features[_ROUGH_VAL_H6]             # (B, T)
    loud_val = h3_features[_LOUD_VAL_H6]               # (B, T)

    # -- R3 features --
    brightness = r3_features[..., _BRIGHTNESS]          # (B, T)
    warmth = r3_features[..., _WARMTH]                  # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)

    # -- Upstream: VMM valence state --
    vmm = upstream_outputs.get("VMM", torch.zeros(B, T, 12, device=device))
    valence_state = vmm[..., _VMM_VALENCE_STATE]        # (B, T)

    # -- Derived signals --
    consonance = 1.0 - rough_val                        # H3-smoothed consonance
    binding_substrate = x_l0l5.mean(dim=-1)             # (B, T)

    # -- E0: Cross-Modal Mapping Strength --
    # Pitch-brightness: brightness weighted by fast consonance (Spence 2011)
    # Mode-warmth: warmth weighted by valence context (Palmer et al. 2013)
    # Binding: supramodal substrate from interaction features
    # Arousal gate: loudness modulates overall transfer salience
    e0 = torch.sigmoid(
        0.25 * brightness * consonance
        + 0.25 * warmth * valence_state
        + 0.20 * pleas_val * binding_substrate
        + 0.15 * loud_val
        + 0.15 * consonance
    )

    return (e0,)
