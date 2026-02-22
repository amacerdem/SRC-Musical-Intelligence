"""MMP R-Layer -- Extraction (3D).

Three recognition/preservation features modeling preserved musical memory
pathways in Alzheimer's disease:

  R0: preserved_memory      -- Preserved memory index [0, 1]
  R1: melodic_recognition   -- Melodic recognition accuracy [0, 1]
  R2: scaffold_efficacy     -- Memory scaffold efficacy [0, 1]

H3 consumed:
    (3, 16, 0, 2)   stumpf_fusion value H16 L2        -- binding integrity (1s)
    (12, 16, 0, 2)   warmth value H16 L2               -- timbre warmth (1s)
    (12, 20, 1, 0)   warmth mean H20 L0                -- sustained warmth (5s)
    (14, 16, 0, 2)   tonalness value H16 L2            -- melody recognition (1s)
    (18, 16, 0, 2)   tristimulus1 value H16 L2         -- instrument fundamental (1s)
    (22, 16, 0, 2)   entropy value H16 L2              -- pattern complexity (1s)
    (0, 16, 0, 2)    roughness value H16 L2            -- valence proxy (1s)

R3 consumed:
    [3]  stumpf_fusion          -- binding integrity
    [4]  sensory_pleasantness   -- memory valence
    [12] warmth                 -- familiar sound character
    [14] tonalness              -- melody tracking
    [18:21] tristimulus1-3      -- instrument/voice ID
    [22] entropy                -- pattern familiarity (inverse)
    [41:49] x_l5l7              -- timbre warmth (nostalgia)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mmp/MMP-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_VAL_1S = (3, 16, 0, 2)
_WARMTH_VAL_1S = (12, 16, 0, 2)
_WARMTH_MEAN_5S = (12, 20, 1, 0)
_TONALNESS_VAL_1S = (14, 16, 0, 2)
_TRIST1_VAL_1S = (18, 16, 0, 2)
_ENTROPY_VAL_1S = (22, 16, 0, 2)
_ROUGHNESS_VAL_1S = (0, 16, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_STUMPF_FUSION = 3
_SENSORY_PLEASANT = 4
_WARMTH = 12
_TONALNESS = 14
_TRIST_START = 18
_TRIST_END = 21
_ENTROPY = 22
_X_L5L7_START = 41
_X_L5L7_END = 49

# -- Hippocampal dependency weights (lower = more cortical = more preserved) ---
# Used to compute preservation_factor: 1.0 - hippocampal_dependency
_HIPPOCAMPAL_DEP = {
    "cortical": 0.1,     # warmth, tonalness, tristimulus
    "preserved": 0.2,    # x_l5l7 (consonance*timbre)
    "mixed": 0.3,        # stumpf_fusion, pleasantness
    "emotional": 0.4,    # loudness, roughness
    "episodic": 0.8,     # entropy
}


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """R-layer: 3D extraction from H3/R3 features.

    Computes preserved memory, melodic recognition, and scaffold efficacy
    for musical mnemonic preservation in AD.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(R0, R1, R2)`` each ``(B, T)``.
    """
    # H3 features
    stumpf_val = h3_features[_STUMPF_VAL_1S]
    warmth_val = h3_features[_WARMTH_VAL_1S]
    warmth_mean = h3_features[_WARMTH_MEAN_5S]
    tonalness_val = h3_features[_TONALNESS_VAL_1S]
    trist1_val = h3_features[_TRIST1_VAL_1S]
    entropy_val = h3_features[_ENTROPY_VAL_1S]
    roughness_val = h3_features[_ROUGHNESS_VAL_1S]

    # R3 features
    r3_warmth = r3_features[..., _WARMTH]
    r3_tonalness = r3_features[..., _TONALNESS]
    r3_trist_mean = r3_features[..., _TRIST_START:_TRIST_END].mean(dim=-1)
    r3_entropy = r3_features[..., _ENTROPY]
    r3_x_l5l7_mean = r3_features[..., _X_L5L7_START:_X_L5L7_END].mean(dim=-1)

    # Familiarity proxy: sustained warmth over 5s (H20 L0)
    familiarity = torch.sigmoid(warmth_mean)

    # Preservation factor: cortical pathway strength
    # High cortical features (warmth, tonalness, trist) = highly preserved
    # Low episodic dependency = high preservation
    cortical_strength = 0.35 * r3_warmth + 0.35 * r3_tonalness + 0.30 * r3_trist_mean
    preservation_factor = torch.sigmoid(
        cortical_strength * (1.0 - _HIPPOCAMPAL_DEP["cortical"])
        - r3_entropy * _HIPPOCAMPAL_DEP["episodic"]
    )

    # Retrieval proxy for R2: roughness-modulated emotional retrieval
    retrieval = torch.sigmoid(roughness_val * (1.0 - _HIPPOCAMPAL_DEP["emotional"]))

    # R0: Preserved memory index -- angular/lingual gyrus pathway
    # Jacobsen 2015: SMA/pre-SMA and ACC show least cortical atrophy in AD
    r0 = torch.sigmoid(
        familiarity * stumpf_val * warmth_val * preservation_factor
    )

    # R1: Melodic recognition -- STG + angular gyrus pathway
    # Sikka 2015: older adults shift to L-angular for melody recognition
    r1 = torch.sigmoid(
        familiarity * tonalness_val * trist1_val * preservation_factor
    )

    # R2: Memory scaffold efficacy -- music as cognitive aid
    # Derks-Dijkman 2024: 28/37 studies show musical mnemonic benefit
    inv_entropy = 1.0 / (entropy_val.abs() + 1e-6)
    r2 = torch.sigmoid(
        retrieval * r3_x_l5l7_mean * inv_entropy * preservation_factor
    )

    return r0, r1, r2
