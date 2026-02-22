"""MMP C-Layer -- Forecast / Clinical Metrics (3D).

Three clinical output dimensions for AD preservation assessment:

  C0: preservation_index       -- Relative sparing measure [0, 1]
  C1: therapeutic_efficacy     -- Expected clinical benefit [0, 1]
  C2: hippocampal_independence -- Cortical mediation score [0, 1]

H3 consumed:
    (3, 24, 19, 0)   stumpf_fusion stability H24 L0   -- binding stability (36s)
    (18, 24, 1, 0)   tristimulus1 mean H24 L0          -- timbre stability (36s)
    (10, 24, 3, 0)   loudness std H24 L0               -- arousal variability (36s)
    (0, 24, 1, 0)    roughness mean H24 L0             -- long-term valence (36s)
    (7, 24, 5, 0)    amplitude range H24 L0            -- dynamic range (36s)

R3 consumed:
    [12] warmth                 -- cortical pathway
    [14] tonalness              -- cortical pathway
    [18:21] tristimulus1-3      -- cortical pathway
    [3]  stumpf_fusion          -- mixed pathway
    [22] entropy                -- episodic pathway (vulnerable)

C-layer uses long-horizon (H24) features for clinical-scale assessments.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mmp/MMP-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_STAB_36S = (3, 24, 19, 0)
_TRIST1_MEAN_36S = (18, 24, 1, 0)
_LOUDNESS_STD_36S = (10, 24, 3, 0)
_ROUGHNESS_MEAN_36S = (0, 24, 1, 0)
_AMP_RANGE_36S = (7, 24, 5, 0)

# -- R3 indices ----------------------------------------------------------------
_WARMTH = 12
_TONALNESS = 14
_TRIST_START = 18
_TRIST_END = 21
_STUMPF_FUSION = 3
_ENTROPY = 22

# -- Hippocampal dependency constants -----------------------------------------
_CORTICAL_DEP = 0.1     # warmth, tonalness, tristimulus
_MIXED_DEP = 0.3        # stumpf_fusion
_EPISODIC_DEP = 0.8     # entropy

_EPS = 1e-6


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    r_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """C-layer: 3D clinical metrics from H3/R3 + R-layer outputs.

    Computes preservation index, therapeutic efficacy, and hippocampal
    independence for clinical AD assessment.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        r_outputs: ``(R0, R1, R2)`` each ``(B, T)``.

    Returns:
        ``(C0, C1, C2)`` each ``(B, T)``.
    """
    r0, r1, r2 = r_outputs

    # H3 features (all H24 long-horizon for clinical-scale)
    stumpf_stab = h3_features[_STUMPF_STAB_36S]
    trist1_mean = h3_features[_TRIST1_MEAN_36S]
    loudness_std = h3_features[_LOUDNESS_STD_36S]
    roughness_mean = h3_features[_ROUGHNESS_MEAN_36S]
    amp_range = h3_features[_AMP_RANGE_36S]

    # R3 features -- cortical vs episodic pathway strengths
    r3_warmth = r3_features[..., _WARMTH]
    r3_tonalness = r3_features[..., _TONALNESS]
    r3_trist_mean = r3_features[..., _TRIST_START:_TRIST_END].mean(dim=-1)
    r3_stumpf = r3_features[..., _STUMPF_FUSION]
    r3_entropy = r3_features[..., _ENTROPY]

    # Cortical feature strength (AD-resistant pathways)
    cortical_strength = (
        r3_warmth * (1.0 - _CORTICAL_DEP)
        + r3_tonalness * (1.0 - _CORTICAL_DEP)
        + r3_trist_mean * (1.0 - _CORTICAL_DEP)
        + r3_stumpf * (1.0 - _MIXED_DEP)
        + stumpf_stab * 0.5 + trist1_mean * 0.5
    )

    # Episodic feature strength (hippocampal-dependent, vulnerable in AD)
    episodic_strength = (
        r3_entropy * (1.0 - _EPISODIC_DEP)
        + loudness_std * 0.5
        + amp_range * 0.3
    )

    # C0: Preservation index -- relative sparing
    # Jacobsen 2015: SMA/pre-SMA and ACC show least cortical atrophy in AD
    c0 = torch.sigmoid(
        cortical_strength / (cortical_strength + episodic_strength + _EPS) - 0.5
    )

    # C1: Therapeutic efficacy -- composite clinical metric
    # Luxton 2025: Level 1 evidence for cognitive stimulation therapy
    # Fang 2017: MT reduces cognitive decline in autobiographical memory
    c1 = torch.sigmoid(
        (r0 + r1 + r2) / 3.0
        + 0.20 * roughness_mean
    )

    # C2: Hippocampal independence -- cortically mediated response
    # Espinosa 2025: active musicians show increased GM in AD-resistant regions
    cortical_features = (
        r3_warmth + r3_tonalness + r3_trist_mean + stumpf_stab + trist1_mean
    )
    episodic_features = r3_entropy + loudness_std
    c2 = torch.sigmoid(
        cortical_features / (cortical_features + episodic_features + _EPS) - 0.5
    )

    return c0, c1, c2
