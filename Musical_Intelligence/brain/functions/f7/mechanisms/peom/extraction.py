"""PEOM E-Layer -- Extraction (3D).

Three period entrainment features modeling the motor system's optimization:

  f01: period_entrainment       -- Motor period lock to auditory period [0, 1]
  f02: velocity_optimization    -- Kinematic smoothness via fixed period [0, 1]
  f03: variability_reduction    -- CV reduction with rhythmic cueing [0, 1]

H3 consumed (tuples 0-8):
    (10, 3, 0, 2)   onset value H3 L2               -- onset at 100ms alpha
    (10, 3, 14, 2)  onset periodicity H3 L2          -- beat periodicity 100ms
    (10, 16, 14, 2) onset periodicity H16 L2         -- beat periodicity 1s
    (11, 3, 0, 2)   onset_strength value H3 L2       -- onset strength 100ms
    (11, 16, 14, 2) onset_strength periodicity H16 L2 -- onset periodicity 1s
    (7, 3, 0, 2)    amplitude value H3 L2            -- beat amplitude 100ms
    (7, 3, 2, 2)    amplitude std H3 L2              -- amplitude variability
    (25, 3, 0, 2)   coupling value H3 L2             -- motor-auditory coupling
    (25, 3, 14, 2)  coupling periodicity H3 L2       -- coupling periodicity

R3 consumed:
    [7]      amplitude               -- beat strength proxy
    [10]     spectral_flux            -- onset detection
    [11]     onset_strength           -- beat event detection
    [25:33]  x_l0l5                   -- motor-auditory coupling

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/peom/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-8 from demand spec) ----------------------------------
_ONSET_VAL_100MS = (10, 3, 0, 2)          # #0: onset at 100ms alpha
_ONSET_PERIOD_100MS = (10, 3, 14, 2)      # #1: beat periodicity 100ms
_ONSET_PERIOD_1S = (10, 16, 14, 2)        # #2: beat periodicity 1s
_ONSET_STR_VAL_100MS = (11, 3, 0, 2)      # #3: onset strength 100ms
_ONSET_STR_PERIOD_1S = (11, 16, 14, 2)    # #4: onset periodicity 1s
_AMP_VAL_100MS = (7, 3, 0, 2)             # #5: beat amplitude 100ms
_AMP_STD_100MS = (7, 3, 2, 2)             # #6: amplitude variability 100ms
_COUPLING_VAL_100MS = (25, 3, 0, 2)       # #7: motor-auditory coupling 100ms
_COUPLING_PERIOD_100MS = (25, 3, 14, 2)   # #8: coupling periodicity 100ms

# -- R3 indices ----------------------------------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10       # onset detection (R3 naming: spectral_flux -> onset_strength)
_ONSET_STRENGTH = 11
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Implements Thaut et al. (2015, 1998b) period entrainment model:
        f01: period entrainment from beat/onset periodicity at 1s
        f02: velocity optimization from coupling periodicity
        f03: variability reduction as f01 * f02 interaction

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f01, f02, f03)`` each ``(B, T)``.
    """
    # -- H3 features --
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]          # beat periodicity 1s
    onset_str_period_1s = h3_features[_ONSET_STR_PERIOD_1S]  # onset periodicity 1s
    coupling_period_100ms = h3_features[_COUPLING_PERIOD_100MS]  # coupling period

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    onset = r3_features[..., _SPECTRAL_FLUX]              # (B, T)
    onset_str = r3_features[..., _ONSET_STRENGTH]         # (B, T)

    # f01: Period entrainment -- motor period lock to auditory period
    # Thaut 2015: period locking defines entrainment; dP/dt = alpha*(T-P(t))
    # Thaut 1998b: motor period entrains even during subliminal 2% tempo changes
    # sigma(0.40 * beat_periodicity_1s + 0.35 * onset_periodicity_1s)
    # Remaining 0.25 from R3 onset/amplitude context
    f01 = torch.sigmoid(
        0.40 * onset_period_1s
        + 0.35 * onset_str_period_1s
        + 0.25 * onset_str * amplitude
    )

    # f02: Velocity optimization -- kinematic smoothness via fixed period
    # Thaut 2015: fixed period provides CTR that reduces jerk
    # Ross & Balasubramaniam 2022: sensorimotor simulation
    # sigma(0.35 * coupling_periodicity_1s)
    # Remaining 0.65 from onset and coupling R3 context
    f02 = torch.sigmoid(
        0.35 * coupling_period_100ms
        + 0.35 * onset * amplitude
        + 0.30 * onset_str
    )

    # f03: Variability reduction -- CV reduction with rhythmic cueing
    # Yamashita 2025: CV reduction d=-1.10, stride time CV 4.51 -> 2.80
    # Interaction term: f01 * f02
    # sigma(0.35 * f01 * f02)
    f03 = torch.sigmoid(
        0.35 * f01 * f02
    )

    return f01, f02, f03
