"""VMM P-Layer -- Temporal Integration (3D).

Three perceived-emotion signals integrating V+R layer with temporal context:

  P0: perceived_happy     -- Perceived happiness from happy pathway [0, 1]
  P1: perceived_sad       -- Perceived sadness from sad pathway [0, 1]
  P2: emotion_certainty   -- Confidence in emotion categorization [0, 1]

H3 consumed:
    (4, 19, 1, 2)   sensory_pleasantness mean H19 L2   -- consonance mean 3s
    (4, 19, 2, 2)   sensory_pleasantness std H19 L2    -- harmonic ambiguity 3s
    (14, 22, 19, 2) tonalness stability H22 L2         -- mode stability 15s

R3 consumed:
    [4]   sensory_pleasantness  -- hedonic signal
    [14]  tonalness             -- brightness for mode confidence

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/vmm/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEAS_MEAN_3S = (4, 19, 1, 2)
_PLEAS_STD_3S = (4, 19, 2, 2)
_TONAL_STAB_15S = (14, 22, 19, 2)

# -- R3 indices ----------------------------------------------------------------
_SENSORY_PLEASANTNESS = 4
_TONALNESS = 14


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    vr_outputs: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """P-layer: 3D temporal integration from V+R layer + H3/R3.

    Integrates the double-dissociated pathways into perceived emotion
    categories. Mode stability over 15s determines categorization
    confidence (Khalfa 2005: mode x tempo interaction).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        vr_outputs: ``(V0, V1, V2, R0, R1, R2, R3)`` each ``(B, T)``.

    Returns:
        ``(P0, P1, P2)`` each ``(B, T)``.
    """
    v0, v1, v2, r0, r1, r2, r3_eval = vr_outputs

    # -- H3 features --
    pleas_mean_3s = h3_features[_PLEAS_MEAN_3S]
    pleas_std_3s = h3_features[_PLEAS_STD_3S]
    tonal_stab_15s = h3_features[_TONAL_STAB_15S]

    # -- R3 features --
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    tonalness = r3_features[..., _TONALNESS]                 # (B, T)

    # P0: Perceived happiness -- integration of happy pathway signals
    # Green 2008: VS activation for happy music, major mode + high consonance
    # Happy perception = happy_pathway * mode_signal * consonance_valence
    p0 = torch.sigmoid(
        0.35 * r0 + 0.30 * v1 + 0.20 * pleas_mean_3s
        + 0.15 * pleasantness
    )

    # P1: Perceived sadness -- integration of sad pathway signals
    # Mitterschiffthaler 2007: hippocampus/amygdala for sad music
    # Sad perception = sad_pathway * (1 - mode_signal) * parahippocampal
    p1 = torch.sigmoid(
        0.35 * r1 + 0.30 * (1.0 - v1) + 0.20 * r2
        + 0.15 * pleas_std_3s
    )

    # P2: Emotion certainty -- confidence in categorization
    # Khalfa 2005: mode detection requires phrase-level context
    # High stability + low ambiguity = high certainty
    ambiguity = pleas_std_3s  # high std = ambiguous harmony
    p2 = torch.sigmoid(
        0.40 * tonal_stab_15s + 0.30 * tonalness
        - 0.30 * ambiguity
    )

    return p0, p1, p2
