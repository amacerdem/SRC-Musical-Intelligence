"""MSR M-Layer -- Temporal Integration (3D).

Three continuous estimates of PLV/P2 system state:

  plv_high_freq     -- Raw PLV at 40-60 Hz [0, 1]
  p2_amplitude      -- Normalized P2 amplitude [0, 1]
  efficiency_index  -- PLV-P2 balance (alpha*PLV - beta*P2) [0, 1]

H3 consumed (tuples 11-15 from demand spec):
    (25, 4, 14, 2)  x_l0l5 periodicity H4 L2  -- coupling periodicity 125ms (theta)
    (25, 16, 1, 2)  x_l0l5 mean H16 L2        -- mean coupling 1s (PLV baseline)
    (25, 16, 14, 2) x_l0l5 periodicity H16 L2 -- coupling periodicity 1s (beat PLV)
    (8, 3, 0, 2)    loudness value H3 L2       -- loudness at 100ms (P2 input)
    (8, 3, 2, 2)    loudness std H3 L2         -- loudness variability 100ms (P2 mod)

E-layer consumed:
    f04 (high_freq_plv)          -- PLV inherits directly
    f05 (p2_suppression)         -- P2 source for inversion
    f06 (sensorimotor_efficiency) -- efficiency inherits directly

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/msr/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 11-15 from demand spec) --------------------------------
_COUPLING_PERIOD_125MS = (25, 4, 14, 2)   # #11: coupling periodicity 125ms (theta)
_COUPLING_MEAN_1S = (25, 16, 1, 2)        # #12: mean coupling 1s (PLV baseline)
_COUPLING_PERIOD_1S = (25, 16, 14, 2)     # #13: coupling periodicity 1s (beat PLV)
_LOUD_VAL_100MS = (8, 3, 0, 2)            # #14: loudness at 100ms (P2 input)
_LOUD_STD_100MS = (8, 3, 2, 2)            # #15: loudness variability 100ms (P2 mod)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3/R3.

    Integrates E-layer features into continuous mathematical estimates of the
    PLV/P2 system state:
        plv_high_freq: Continuous PLV estimate from f04 + theta/beat periodicity.
        p2_amplitude: P2 from loudness features at 100ms. Higher loudness
            variability maps to higher P2 (novel/unpredictable stimuli).
        efficiency_index: Net PLV-P2 balance using alpha=1.0, beta=0.5 from
            f06 + long-term coupling stability.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        e_outputs: ``(f04, f05, f06)`` each ``(B, T)``.

    Returns:
        ``(plv_high_freq, p2_amplitude, efficiency_index)`` each ``(B, T)``.
    """
    f04, f05, f06 = e_outputs

    # -- H3 features --
    coupling_period_125ms = h3_features[_COUPLING_PERIOD_125MS]
    coupling_mean_1s = h3_features[_COUPLING_MEAN_1S]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]
    loud_val_100ms = h3_features[_LOUD_VAL_100MS]
    loud_std_100ms = h3_features[_LOUD_STD_100MS]

    # plv_high_freq (idx 3): Continuous PLV 40-60 Hz estimate
    # L. Zhang 2015: PLV [0.28, 0.44] -> [0, 1] via sigmoid
    # Inherits f04 + additional theta (125ms) and beat (1s) horizons for stability
    plv_high_freq = torch.sigmoid(
        0.40 * f04
        + 0.25 * coupling_period_125ms
        + 0.20 * coupling_period_1s
        + 0.15 * coupling_mean_1s
    )

    # p2_amplitude (idx 4): Normalized P2 amplitude at 155-180ms post-stimulus
    # L. Zhang 2015: nonmusicians 4.65-5.91 uV vs musicians 1.46-3.29 uV
    # Higher loudness variability = more novel stimuli = higher P2
    p2_amplitude = torch.sigmoid(
        0.40 * loud_val_100ms
        + 0.35 * loud_std_100ms
        + 0.25 * (1.0 - f05)
    )

    # efficiency_index (idx 5): PLV-P2 balance
    # alpha * PLV - beta * P2 (alpha=1.0, beta=0.5)
    # Asymmetric weighting: bottom-up enhancement (PLV) > top-down suppression (P2)
    # Inherits from f06 + long-term coupling baseline for stability
    efficiency_index = torch.sigmoid(
        0.45 * f06
        + 0.30 * (1.0 * plv_high_freq - 0.5 * p2_amplitude)
        + 0.25 * coupling_mean_1s
    )

    return plv_high_freq, p2_amplitude, efficiency_index
