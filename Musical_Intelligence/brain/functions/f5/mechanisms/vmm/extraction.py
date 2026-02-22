"""VMM V+R Layer -- Extraction (7D).

Seven explicit features modeling valence-mode pathways:

  V0: valence                -- Overall musical valence [0, 1]
  V1: mode_signal            -- Major/minor mode detection [0, 1]
  V2: consonance_valence     -- Consonance-derived valence [0, 1]
  R0: happy_pathway          -- Striatal (VS/DS/ACC) activation for major/consonant [0, 1]
  R1: sad_pathway             -- Limbic (hippocampus/amygdala/PHG) for minor/dissonant [0, 1]
  R2: parahippocampal        -- Context processing both pathways [0, 1]
  R3: reward_evaluation      -- ACC/sgACC reward evaluation [0, 1]

H3 consumed:
    (4, 19, 0, 2)   sensory_pleasantness value H19 L2  -- consonance state 3s
    (4, 19, 1, 2)   sensory_pleasantness mean H19 L2   -- consonance mean 3s
    (4, 19, 2, 2)   sensory_pleasantness std H19 L2    -- harmonic ambiguity 3s
    (14, 22, 0, 2)  tonalness value H22 L2             -- section brightness 15s
    (12, 19, 0, 2)  warmth value H19 L2                -- affective warmth 3s
    (16, 19, 0, 2)  spectral_smoothness value H19 L2   -- smoothness 3s

R3 consumed:
    [0]   roughness             -- inverse consonance for valence
    [4]   sensory_pleasantness  -- consonance state
    [12]  warmth                -- affective warmth (sad pathway warmth)
    [14]  tonalness             -- brightness proxy for mode detection
    [16]  spectral_smoothness   -- spectral regularity

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/vmm/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEAS_VAL_3S = (4, 19, 0, 2)
_PLEAS_MEAN_3S = (4, 19, 1, 2)
_PLEAS_STD_3S = (4, 19, 2, 2)
_TONAL_VAL_15S = (14, 22, 0, 2)
_WARMTH_VAL_3S = (12, 19, 0, 2)
_SMOOTH_VAL_3S = (16, 19, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_WARMTH = 12
_TONALNESS = 14
_SPECTRAL_SMOOTHNESS = 16


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor, Tensor, Tensor, Tensor]:
    """V+R layer: 7D extraction from H3/R3 features.

    Models the double dissociation between happy (striatal) and sad (limbic)
    neural pathways. Major/consonant/bright music activates VS/DS/ACC;
    minor/dissonant/dark music activates hippocampus/amygdala/PHG.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(V0, V1, V2, R0, R1, R2, R3)`` each ``(B, T)``.
    """
    # -- H3 features --
    pleas_val_3s = h3_features[_PLEAS_VAL_3S]
    pleas_mean_3s = h3_features[_PLEAS_MEAN_3S]
    pleas_std_3s = h3_features[_PLEAS_STD_3S]
    tonal_val_15s = h3_features[_TONAL_VAL_15S]
    warmth_val_3s = h3_features[_WARMTH_VAL_3S]
    smooth_val_3s = h3_features[_SMOOTH_VAL_3S]

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]  # (B, T)
    warmth = r3_features[..., _WARMTH]                     # (B, T)
    tonalness = r3_features[..., _TONALNESS]               # (B, T)
    smoothness = r3_features[..., _SPECTRAL_SMOOTHNESS]    # (B, T)

    # -- Derived signals --
    consonance = 1.0 - roughness   # inverse roughness = consonance proxy
    mode_bright = 0.50 * tonalness + 0.50 * tonal_val_15s  # brightness ~ major

    # V0: Valence -- overall affective valence from consonance + warmth
    # Pallesen 2005: fMRI valence tracking, consonance-roughness axis
    v0 = torch.sigmoid(
        0.40 * consonance + 0.30 * pleas_val_3s + 0.30 * warmth_val_3s
    )

    # V1: Mode signal -- major vs minor mode detection
    # Khalfa 2005: mode interacts with tempo for emotional categorization
    # Mode detection requires phrase-level context (2-3 chords minimum)
    # High brightness + high consonance = major; low brightness + low cons = minor
    v1 = torch.sigmoid(
        0.40 * mode_bright + 0.35 * pleas_mean_3s + 0.25 * smooth_val_3s
    )

    # V2: Consonance-derived valence -- pure sensory consonance component
    # Koelsch 2006: consonance-dissonance activates different networks
    v2 = torch.sigmoid(
        0.50 * pleasantness + 0.30 * pleas_val_3s + 0.20 * smoothness
    )

    # R0: Happy pathway -- VS/DS/ACC activation for major/consonant/bright
    # Green 2008: happy music selectively activates ventral striatum
    # Happy = high consonance + high brightness + high smoothness
    r0 = torch.sigmoid(
        0.35 * consonance * mode_bright + 0.35 * pleas_mean_3s
        + 0.30 * smooth_val_3s
    )

    # R1: Sad pathway -- hippocampus/amygdala/PHG for minor/dissonant/dark
    # Mitterschiffthaler 2007: sad music activates hippocampus, amygdala
    # Sad = high roughness + low brightness + warmth (comfort in sadness)
    sad_mode = 1.0 - mode_bright
    r1 = torch.sigmoid(
        0.35 * roughness * sad_mode + 0.35 * warmth_val_3s
        + 0.30 * pleas_std_3s
    )

    # R2: Parahippocampal -- context processing, both pathways
    # Blood & Zatorre 2001: PHG activation correlates with dissonance
    # but also processes contextual binding for both valences
    r2 = torch.sigmoid(
        0.40 * warmth + 0.30 * pleas_std_3s + 0.30 * tonal_val_15s
    )

    # R3: Reward evaluation -- ACC/sgACC evaluation of affective significance
    # Pereira 2011: ACC integrates reward evaluation across valences
    r3_out = torch.sigmoid(
        0.35 * pleas_val_3s * consonance + 0.35 * smooth_val_3s
        + 0.30 * warmth_val_3s
    )

    return v0, v1, v2, r0, r1, r2, r3_out
