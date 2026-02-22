"""EDNR E-Layer -- Extraction (4D).

Four expertise-dependent network reorganization features:

  f01: within_connectivity      -- Intra-network coupling strength [0, 1]
  f02: between_connectivity     -- Inter-network coupling (inverse) [0, 1]
  f03: compartmentalization     -- Within/between ratio [0, ~3]
  f04: expertise_signature      -- Expertise-specific pattern [0, 1]

H3 consumed (tuples 0-7 from demand spec):
    (25, 3, 0, 2)   x_l0l5 value H3 L2               -- within-network coupling 100ms
    (25, 3, 2, 2)   x_l0l5 std H3 L2                 -- coupling variability 100ms
    (25, 16, 1, 2)  x_l0l5 mean H16 L2               -- mean coupling over 1s
    (25, 16, 14, 2) x_l0l5 periodicity H16 L2        -- coupling periodicity 1s
    (4, 3, 0, 2)    sensory_pleasantness value H3 L2  -- pleasantness at 100ms
    (4, 16, 1, 2)   sensory_pleasantness mean H16 L2  -- mean pleasantness 1s
    (14, 3, 0, 2)   tonalness value H3 L2             -- tonalness at 100ms
    (14, 16, 1, 2)  tonalness mean H16 L2             -- mean tonalness over 1s

R3 consumed:
    [25:33]  x_l0l5                  -- within-network coupling proxy
    [33:41]  x_l4l5                  -- cross-network coupling proxy
    [14]     tonalness               -- processing complexity indicator
    [4]      sensory_pleasantness    -- processing quality proxy

Paraskevopoulos 2022: musicians show 106 within-network edges vs 192
    between-network edges in non-musicians.
Leipold et al. 2021: robust musicianship effects on intrahemispheric FC
    (pFWE<0.05, n=153).
Moller et al. 2021: NM show distributed CT correlations while musicians
    show only local correlations (FDR<10%).
Papadaki et al. 2023: network strength correlates with interval recognition
    (rho=0.36, p=0.02).

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ednr/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-7 from demand spec) ----------------------------------
_WITHIN_VAL_100MS = (25, 3, 0, 2)        # #0: within-network coupling 100ms
_WITHIN_STD_100MS = (25, 3, 2, 2)        # #1: coupling variability 100ms
_WITHIN_MEAN_1S = (25, 16, 1, 2)         # #2: mean coupling over 1s
_WITHIN_PERIOD_1S = (25, 16, 14, 2)      # #3: coupling periodicity 1s
_PLEAS_VAL_100MS = (4, 3, 0, 2)          # #4: pleasantness at 100ms
_PLEAS_MEAN_1S = (4, 16, 1, 2)           # #5: mean pleasantness 1s
_TONAL_VAL_100MS = (14, 3, 0, 2)         # #6: tonalness at 100ms
_TONAL_MEAN_1S = (14, 16, 1, 2)          # #7: mean tonalness over 1s

# -- R3 indices ----------------------------------------------------------------
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41
_TONALNESS = 14
_SENSORY_PLEASANTNESS = 4

# -- Epsilon for ratio computation ---------------------------------------------
_EPS = 1e-8


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor, Tensor]:
    """E-layer: 4D extraction from H3/R3 features.

    Implements the core expertise-dependent network reorganization features from
    Paraskevopoulos (2022) and Leipold et al. (2021). Two connectivity streams:
        Within (f01): intra-network coupling that increases with musical expertise.
        Between (f02): inter-network coupling that decreases with expertise.
    Plus a ratio (f03) and expertise signature (f04).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f01, f02, f03, f04)`` each ``(B, T)``.
    """
    # -- H3 features --
    within_mean_1s = h3_features[_WITHIN_MEAN_1S]
    within_period_1s = h3_features[_WITHIN_PERIOD_1S]
    tonal_mean_1s = h3_features[_TONAL_MEAN_1S]
    pleas_mean_1s = h3_features[_PLEAS_MEAN_1S]

    # -- R3 features --
    # Cross-network coupling proxy: mean over x_l4l5 group
    cross_mean = r3_features[..., _X_L4L5_START:_X_L4L5_END].mean(dim=-1)
    cross_entropy = r3_features[..., _X_L4L5_START:_X_L4L5_END].std(dim=-1)

    # f01: Within connectivity -- intra-network coupling strength
    # Paraskevopoulos 2022: musicians show 106 within-network edges
    # Leipold et al. 2021: robust musicianship effects on intrahemispheric FC
    # sigma(0.35 * within_mean_1s + 0.30 * within_periodicity_1s)
    f01 = torch.sigmoid(
        0.35 * within_mean_1s
        + 0.30 * within_period_1s
    )

    # f02: Between connectivity -- inter-network coupling (inverse)
    # Paraskevopoulos 2022: NM > M between-network multilinks (192 vs 106)
    # sigma(0.35 * cross_mean_1s + 0.30 * cross_entropy_1s)
    f02 = torch.sigmoid(
        0.35 * cross_mean
        + 0.30 * cross_entropy
    )

    # f03: Compartmentalization -- within/between ratio
    # Moller et al. 2021: NM show distributed CT correlations, M show local only
    # f01 / (f02 + epsilon) -- NOT sigmoid, raw ratio
    f03 = f01 / (f02 + _EPS)

    # f04: Expertise signature -- processing refinement pattern
    # Papadaki et al. 2023: network strength correlates with recognition (rho=0.36)
    # Porfyri et al. 2025: Group x Time F(1,28)=4.635, eta^2=0.168
    # sigma(0.35 * tonalness_mean_1s + 0.35 * pleasantness_mean_1s)
    f04 = torch.sigmoid(
        0.35 * tonal_mean_1s
        + 0.35 * pleas_mean_1s
    )

    return f01, f02, f03, f04
