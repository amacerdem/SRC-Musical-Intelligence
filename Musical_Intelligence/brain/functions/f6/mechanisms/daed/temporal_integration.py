"""DAED M-Layer -- Temporal Integration (2D).

Two derived mathematical quantities from E-layer dopaminergic signals:

  dissociation_index  -- |f01 - f02| temporal-anatomical dissociation [0, 1]
  temporal_phase      -- f01 / (f01 + f02 + eps) anticipation vs consummation [0, 1]

H3 consumed (tuples 7-13 from demand spec):
    (8, 3, 0, 2)    loudness value H3 L2               -- current intensity state
    (8, 8, 1, 0)    loudness mean H8 L0                -- medium-term context
    (7, 8, 0, 2)    amplitude value H8 L2              -- energy envelope
    (7, 16, 1, 2)   amplitude mean H16 L2              -- sustained energy
    (0, 3, 0, 2)    roughness value H3 L2              -- instantaneous tension
    (10, 4, 0, 2)   onset_strength value H4 L2         -- event detection
    (10, 8, 14, 2)  onset_strength periodicity H8 L2   -- rhythmic regularity

The M-layer H3 demands provide multi-scale temporal context. The two output
dimensions are deterministic functions of E-layer features:

    dissociation_index = |f01_anticipatory_da - f02_consummatory_da|
    temporal_phase = f01 / (f01 + f02 + 1e-8)

Salimpoor 2011: caudate and NAcc show temporally distinct DA release patterns.
Mohebi 2024: DA transients follow a striatal gradient of reward time horizons.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/daed/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 7-13 from demand spec) ---------------------------------
_LOUD_VAL_100MS = (8, 3, 0, 2)          # #7: loudness at 100ms
_LOUD_MEAN_500MS = (8, 8, 1, 0)         # #8: mean loudness 500ms
_AMP_VAL_500MS = (7, 8, 0, 2)           # #9: amplitude at 500ms
_AMP_MEAN_1S = (7, 16, 1, 2)            # #10: mean amplitude 1s
_ROUGH_VAL_100MS = (0, 3, 0, 2)         # #11: roughness at 100ms
_ONSET_VAL_125MS = (10, 4, 0, 2)        # #12: onset at 125ms
_ONSET_PERIOD_500MS = (10, 8, 14, 2)    # #13: peak periodicity 500ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer outputs.

    Computes two derived quantities from the E-layer dopaminergic signals:
        dissociation_index: absolute difference between anticipatory/consummatory DA
        temporal_phase: continuous indicator of anticipation vs consummation phase

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.

    Returns:
        ``(dissociation_index, temporal_phase)`` each ``(B, T)``.
    """
    f01, f02, _f03, _f04 = e_outputs

    # dissociation_index: |f01 - f02| — NOT sigmoid
    # Salimpoor 2011: caudate and NAcc show temporally distinct DA release
    # High = clear phase separation; low = transition state
    dissociation_index = torch.abs(f01 - f02)

    # temporal_phase: f01 / (f01 + f02 + eps) — ratio, NOT sigmoid
    # Mohebi 2024: DA transients follow striatal gradient of reward time horizons
    # Near 1.0 = pure anticipation (caudate dominant)
    # Near 0.0 = pure consummation (NAcc dominant)
    # ~0.5 = transition
    temporal_phase = f01 / (f01 + f02 + 1e-8)

    return dissociation_index, temporal_phase
