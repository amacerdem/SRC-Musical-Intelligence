"""VMM C-Layer -- Cognitive Present (2D).

Two cognitive-level dimensions for mode detection and valence state:

  C0: mode_detection_state  -- Current mode detection confidence [0, 1]
  C1: valence_state         -- Integrated valence state for belief update [0, 1]

H3 consumed:
    (14, 22, 0, 2)   tonalness value H22 L2           -- section brightness 15s
    (14, 22, 19, 2)  tonalness stability H22 L2       -- mode stability 15s
    (4, 19, 0, 2)    sensory_pleasantness value H19 L2 -- consonance state 3s

R3 consumed:
    [0]   roughness             -- valence proxy (inverse)
    [14]  tonalness             -- mode detection

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/vmm/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_TONAL_VAL_15S = (14, 22, 0, 2)
_TONAL_STAB_15S = (14, 22, 19, 2)
_PLEAS_VAL_3S = (4, 19, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_TONALNESS = 14


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    vr_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """C-layer: 2D cognitive present from H3/R3 + V+R/P outputs.

    C-layer outputs are the primary cognitive exports:
        mode_detection_state  -> belief: emotional_valence (Core, tau=0.4)
        valence_state         -> belief: emotional_valence (Core, tau=0.4)

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        vr_outputs: ``(V0, V1, V2, R0, R1, R2, R3)`` each ``(B, T)``.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``.

    Returns:
        ``(C0, C1)`` each ``(B, T)``.
    """
    v0, v1, v2, r0, r1, _r2, r3_eval = vr_outputs
    p0, p1, p2 = p_outputs

    # -- H3 features --
    tonal_val_15s = h3_features[_TONAL_VAL_15S]
    tonal_stab_15s = h3_features[_TONAL_STAB_15S]
    pleas_val_3s = h3_features[_PLEAS_VAL_3S]

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]      # (B, T)
    tonalness = r3_features[..., _TONALNESS]       # (B, T)

    # C0: Mode detection state -- confidence in major/minor categorization
    # Khalfa 2005: mode detection requires phrase-level context (2-3 chords)
    # Mode confidence = mode_signal * stability * tonal_clarity
    c0 = torch.sigmoid(
        0.30 * v1 + 0.25 * tonal_stab_15s + 0.25 * p2
        + 0.20 * tonalness
    )

    # C1: Valence state -- integrated affective valence for belief update
    # Pallesen 2005: fMRI valence tracking in bilateral temporal/frontal cortex
    # Valence state = weighted integration of valence + pathways + certainty
    consonance = 1.0 - roughness
    c1 = torch.sigmoid(
        0.25 * v0 + 0.20 * pleas_val_3s + 0.20 * r3_eval
        + 0.20 * (p0 - p1) + 0.15 * consonance
    )

    return c0, c1
