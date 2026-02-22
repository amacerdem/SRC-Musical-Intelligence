"""GSSM E-Layer -- Extraction (3D).

Three gait-synchronized stimulation features:

  f07: phase_synchronization   -- Gait-stimulation phase locking [0, 1]
  f08: cv_reduction            -- Stride variability decrease [0, 1]
  f09: balance_improvement     -- Mini-BESTest score increase (interaction) [0, 1]

H3 consumed (tuples 0-6):
    (10, 3, 0, 2)   onset value H3 L2              -- step detection 100ms
    (10, 3, 14, 2)  onset periodicity H3 L2        -- step periodicity 100ms
    (10, 16, 14, 2) onset periodicity H16 L2       -- step periodicity 1s
    (11, 3, 0, 2)   onset_strength value H3 L2     -- heel strike 100ms
    (11, 8, 14, 2)  onset_strength period H8 L2    -- gait periodicity 500ms
    (25, 3, 0, 2)   x_l0l5 value H3 L2            -- SMA-M1 coupling 100ms
    (25, 3, 14, 2)  x_l0l5 periodicity H3 L2      -- coupling periodicity 100ms

R3 consumed:
    [10]     spectral_flux       -- step onset detection
    [11]     onset_strength      -- step event strength
    [25:33]  x_l0l5              -- SMA-M1 coupling

Yamashita 2025: gait-synchronized tACS to M1 phase-locked to heel strike;
swing time CV eta_p^2 = 0.825; stride time CV d = -1.10; Mini-BESTest d = 1.05.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/gssm/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (tuples 0-6 from demand spec) ----------------------------------
_ONSET_VAL_100MS = (10, 3, 0, 2)           # #0: step detection 100ms
_ONSET_PERIOD_100MS = (10, 3, 14, 2)       # #1: step periodicity 100ms
_ONSET_PERIOD_1S = (10, 16, 14, 2)         # #2: step periodicity 1s (stride)
_STRENGTH_VAL_100MS = (11, 3, 0, 2)        # #3: heel strike 100ms
_STRENGTH_PERIOD_500MS = (11, 8, 14, 2)    # #4: gait periodicity 500ms
_COUPLING_VAL_100MS = (25, 3, 0, 2)        # #5: SMA-M1 coupling 100ms
_COUPLING_PERIOD_100MS = (25, 3, 14, 2)    # #6: coupling periodicity 100ms

# -- R3 indices ----------------------------------------------------------------
_SPECTRAL_FLUX = 10          # B group (onset detection)
_ONSET_STRENGTH = 11         # B group
_X_L0L5_START = 25           # F group (coupling)
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(f07, f08, f09)`` each ``(B, T)``.
    """
    # -- H3 features --
    onset_val_100ms = h3_features[_ONSET_VAL_100MS]
    onset_period_100ms = h3_features[_ONSET_PERIOD_100MS]
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]
    strength_val_100ms = h3_features[_STRENGTH_VAL_100MS]
    strength_period_500ms = h3_features[_STRENGTH_PERIOD_500MS]
    coupling_val_100ms = h3_features[_COUPLING_VAL_100MS]
    coupling_period_100ms = h3_features[_COUPLING_PERIOD_100MS]

    # -- R3 features --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]            # (B, T)
    onset_strength = r3_features[..., _ONSET_STRENGTH]          # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]      # (B, T, 8)
    coupling_mean = x_l0l5.mean(dim=-1)                         # (B, T)

    # f07: Phase synchronization -- gait-stimulation phase locking
    # Yamashita 2025: gait-synchronized tACS phase-locked to heel strike
    # Phase_Lock = cos(phi_gait - phi_stim) -> 1.0 for perfect sync
    # sigma(0.40 * step_periodicity_1s + 0.30 * coupling_periodicity_1s)
    # We use step periodicity at 1s (stride cycle) and coupling periodicity
    f07 = torch.sigmoid(
        0.40 * onset_period_1s * onset_strength
        + 0.30 * coupling_period_100ms * coupling_mean
        + 0.30 * strength_period_500ms * strength_val_100ms
    )

    # f08: CV reduction -- stride variability decrease
    # Yamashita 2025: stride time CV reduced 4.51 -> 2.80 (d = -1.10)
    # sigma(0.40 * f07 + 0.30 * coupling_periodicity_100ms)
    f08 = torch.sigmoid(
        0.40 * f07
        + 0.30 * coupling_period_100ms * coupling_val_100ms
        + 0.30 * onset_period_100ms * spectral_flux
    )

    # f09: Balance improvement -- Mini-BESTest score increase
    # Yamashita 2025: Mini-BESTest d = 1.05; CV-balance r = 0.62
    # sigma(0.35 * f07 * f08) -- interaction term
    f09 = torch.sigmoid(
        0.35 * f07 * f08
        + 0.35 * onset_val_100ms * onset_strength
        + 0.30 * coupling_mean * strength_val_100ms
    )

    return f07, f08, f09
