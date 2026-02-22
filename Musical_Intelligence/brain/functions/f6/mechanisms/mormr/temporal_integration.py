"""MORMR M-Layer -- Temporal Integration (1D).

One composite signal integrating opioid release with chills frequency:

  opioid_tone  -- Overall opioid system tone [0, 1]

H3 consumed (tuples 7-11):
    (8, 3, 0, 2)    loudness value H3 L2            -- instantaneous intensity
    (8, 8, 1, 2)    loudness mean H8 L2             -- medium-term intensity
    (8, 16, 1, 2)   loudness mean H16 L2            -- sustained intensity
    (0, 3, 0, 2)    roughness value H3 L2           -- instantaneous consonance
    (4, 3, 0, 2)    pleasantness value H3 L2        -- instantaneous hedonic

The M-layer H3 demands provide multi-scale loudness, roughness, and
pleasantness context that feeds the upstream E-layer computations.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/mormr/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 7-11 from demand spec) ---------------------------------
_LOUD_VAL_100MS = (8, 3, 0, 2)          # #7: loudness at 100ms
_LOUD_MEAN_500MS = (8, 8, 1, 2)         # #8: mean loudness at 500ms
_LOUD_MEAN_1S = (8, 16, 1, 2)           # #9: mean loudness at 1s
_ROUGH_VAL_100MS = (0, 3, 0, 2)         # #10: roughness at 100ms
_PLEAS_VAL_100MS = (4, 3, 0, 2)         # #11: pleasantness at 100ms


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor]:
    """M-layer: 1D temporal integration from E-layer outputs + H3 context.

    Computes opioid tone as a simple average of opioid release and chills count:
        opioid_tone = sigma(0.5 * f01_opioid_release + 0.5 * f02_chills_count)

    Unlike DAED's M-layer which computes a dissociation (difference), MORMR's
    M-layer computes an integration (average). This reflects the pharmacological
    reality: while dopamine has fast, phasic release patterns (DAED), the opioid
    system operates on a slower, more tonic timescale.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``.

    Returns:
        ``(opioid_tone,)`` -- single tensor ``(B, T)`` wrapped in a 1-tuple.
    """
    f01, f02, _f03, _f04 = e_outputs

    # opioid_tone: Overall opioid system tone
    # Putkinen 2025: baseline MOR availability modulates pleasure-BOLD coupling.
    # Tonic component (f01): sustained MOR activation from consonant, warm music
    # Phasic component (f02): burst MOR activation during chills/frisson events
    opioid_tone = torch.sigmoid(0.5 * f01 + 0.5 * f02)

    return (opioid_tone,)
