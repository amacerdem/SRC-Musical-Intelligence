"""MSR E-Layer -- Extraction (3D).

Three sensorimotor reorganization features:

  f04: high_freq_plv          -- 40-60 Hz phase-locking value [0, 1]
  f05: p2_suppression         -- P2 vertex potential suppression [0, 1]
  f06: sensorimotor_efficiency -- Net efficiency (PLV - P2) [0, 1]

H3 consumed (tuples 0-10 from demand spec):
    (25, 0, 0, 2)   x_l0l5 value H0 L2        -- coupling 25ms gamma
    (25, 1, 0, 2)   x_l0l5 value H1 L2        -- coupling 50ms gamma (PLV source)
    (25, 1, 1, 2)   x_l0l5 mean H1 L2         -- mean coupling 50ms (baseline)
    (25, 3, 0, 2)   x_l0l5 value H3 L2        -- coupling 100ms alpha (PLV integ)
    (25, 3, 2, 2)   x_l0l5 std H3 L2          -- coupling variability 100ms
    (25, 3, 14, 2)  x_l0l5 periodicity H3 L2  -- coupling periodicity 100ms
    (33, 3, 0, 2)   x_l4l5 value H3 L2        -- sensorimotor coupling 100ms
    (33, 3, 2, 2)   x_l4l5 std H3 L2          -- coupling stability 100ms
    (33, 3, 20, 2)  x_l4l5 entropy H3 L2      -- coupling entropy 100ms
    (8, 3, 20, 2)   loudness entropy H3 L2     -- loudness entropy 100ms (P2 proxy)
    (10, 16, 14, 2) onset_strength period H16 L2 -- onset periodicity 1s

R3 consumed:
    [8]      loudness (velocity_D)        -- P2 amplitude proxy
    [10]     spectral_flux (onset_str)    -- onset detection for bottom-up
    [25:33]  x_l0l5                       -- motor-auditory coupling (PLV)
    [33:41]  x_l4l5                       -- sensorimotor coupling (training)

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/msr/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-10 from demand spec) ---------------------------------
_COUPLING_VAL_25MS = (25, 0, 0, 2)       # #0: coupling at 25ms gamma
_COUPLING_VAL_50MS = (25, 1, 0, 2)       # #1: coupling at 50ms gamma (PLV source)
_COUPLING_MEAN_50MS = (25, 1, 1, 2)      # #2: mean coupling 50ms (baseline)
_COUPLING_VAL_100MS = (25, 3, 0, 2)      # #3: coupling at 100ms alpha (PLV integ)
_COUPLING_STD_100MS = (25, 3, 2, 2)      # #4: coupling variability 100ms
_COUPLING_PERIOD_100MS = (25, 3, 14, 2)  # #5: coupling periodicity 100ms
_SM_COUPLING_VAL_100MS = (33, 3, 0, 2)   # #6: sensorimotor coupling 100ms
_SM_COUPLING_STD_100MS = (33, 3, 2, 2)   # #7: coupling stability 100ms
_SM_COUPLING_ENT_100MS = (33, 3, 20, 2)  # #8: coupling entropy 100ms
_LOUD_ENTROPY_100MS = (8, 3, 20, 2)      # #9: loudness entropy 100ms (P2 proxy)
_ONSET_PERIOD_1S = (10, 16, 14, 2)       # #10: onset periodicity 1s (P2 suppress)

# -- R3 indices ----------------------------------------------------------------
_LOUDNESS = 8
_ONSET_STRENGTH = 10
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Implements the dual reorganization pattern from L. Zhang et al. (2015).
    Three parallel computations:
        f04 (bottom-up): Motor-auditory coupling at gamma (25-100ms) horizons
            tracks enhanced 40-60 Hz PLV in musicians (d = 1.13).
        f05 (top-down): Loudness entropy + onset periodicity at 1s tracks
            P2 vertex potential suppression from training (d = 1.16).
        f06 (net efficiency): Subtractive formula: sigma(0.50*f04 - 0.30*f05)
            captures dual reorganization efficiency (d = 1.28).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f04, f05, f06)`` each ``(B, T)``.
    """
    # -- H3 features --
    coupling_val_25ms = h3_features[_COUPLING_VAL_25MS]
    coupling_val_50ms = h3_features[_COUPLING_VAL_50MS]
    coupling_mean_50ms = h3_features[_COUPLING_MEAN_50MS]
    coupling_val_100ms = h3_features[_COUPLING_VAL_100MS]
    coupling_std_100ms = h3_features[_COUPLING_STD_100MS]
    coupling_period_100ms = h3_features[_COUPLING_PERIOD_100MS]
    sm_coupling_val_100ms = h3_features[_SM_COUPLING_VAL_100MS]
    sm_coupling_std_100ms = h3_features[_SM_COUPLING_STD_100MS]
    sm_coupling_ent_100ms = h3_features[_SM_COUPLING_ENT_100MS]
    loud_entropy_100ms = h3_features[_LOUD_ENTROPY_100MS]
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]

    # -- R3 features (context) --
    # R3 available for coupling context; H3 multi-scale dynamics are primary.

    # f04: High-frequency PLV (40-60 Hz phase-locking value)
    # L. Zhang 2015: musicians PLV = 0.40-0.44 vs nonmusicians 0.28-0.31
    # sigma(0.40 * coupling_period_100ms + 0.25 * coupling_gamma_50ms)
    # Multi-scale gamma/alpha coupling = bottom-up precision enhancement
    f04 = torch.sigmoid(
        0.40 * coupling_period_100ms
        + 0.25 * coupling_val_50ms
        + 0.15 * coupling_val_25ms
        + 0.10 * coupling_val_100ms
        + 0.10 * coupling_mean_50ms
    )

    # f05: P2 suppression (P2 vertex potential suppression)
    # L. Zhang 2015: nonmusicians P2 = 4.65-5.91 uV vs musicians 1.46-3.29 uV
    # sigma(0.40 * loudness_entropy + 0.30 * onset_periodicity_1s)
    # Higher entropy + periodicity = more predictable input = more P2 suppression
    f05 = torch.sigmoid(
        0.40 * loud_entropy_100ms
        + 0.30 * onset_period_1s
        + 0.15 * sm_coupling_ent_100ms
        + 0.15 * sm_coupling_val_100ms
    )

    # f06: Sensorimotor efficiency (net PLV - P2 balance)
    # L. Zhang 2015: dual reorganization TFD d = 1.28
    # SPECIAL: Subtractive formula -- sigma(0.50 * f04 - 0.30 * f05)
    # P2 suppression is an inverted signal: higher suppression = less resource use
    f06 = torch.sigmoid(
        0.50 * f04
        - 0.30 * f05
    )

    return f04, f05, f06
