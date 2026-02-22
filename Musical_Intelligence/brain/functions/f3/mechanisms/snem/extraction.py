"""SNEM E-Layer — Extraction (3D).

Three explicit features modeling beat entrainment and selective enhancement:

  E0: beat_entrainment         — Beat-frequency periodicity [0, 1]
  E1: meter_entrainment        — Metric coupling strength [0, 1]
  E2: selective_enhancement    — Enhancement from entrainment x coupling [0, 1]

H3 consumed:
    (10, 16, 14, 2)  flux periodicity H16 L2          — beat periodicity at 1s
    (11, 16, 14, 2)  onset periodicity H16 L2         — onset periodicity at 1s
    (7, 16, 1, 2)    amplitude mean H16 L2            — beat salience context
    (25, 16, 14, 2)  coupling periodicity H16 L2      — metric structure 1s
    (25, 3, 14, 2)   coupling periodicity H3 L2       — fast metric cue 100ms
    (25, 16, 21, 2)  coupling zero-crossings H16 L2   — phase resets 1s
    (21, 4, 8, 0)    spectral change velocity H4 L0   — enhancement cue
    (8, 3, 20, 2)    loudness entropy H3 L2           — salience context

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/snem/SNEM-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_FLUX_PERIOD_1S = (10, 16, 14, 2)
_ONSET_PERIOD_1S = (11, 16, 14, 2)
_AMP_MEAN_1S = (7, 16, 1, 2)
_COUPLING_PERIOD_1S = (25, 16, 14, 2)
_COUPLING_PERIOD_100MS = (25, 3, 14, 2)
_COUPLING_ZC_1S = (25, 16, 21, 2)
_SPECTRAL_CHANGE_VEL = (21, 4, 8, 0)
_LOUD_ENTROPY = (8, 3, 20, 2)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3 features.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.

    Returns:
        ``(E0, E1, E2)`` each ``(B, T)``.
    """
    flux_period_1s = h3_features[_FLUX_PERIOD_1S]
    onset_period_1s = h3_features[_ONSET_PERIOD_1S]
    amp_mean_1s = h3_features[_AMP_MEAN_1S]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]
    coupling_period_100ms = h3_features[_COUPLING_PERIOD_100MS]
    coupling_zc_1s = h3_features[_COUPLING_ZC_1S]
    spectral_change_vel = h3_features[_SPECTRAL_CHANGE_VEL]
    loud_entropy = h3_features[_LOUD_ENTROPY]

    # E0: Beat entrainment — SS-EP at beat frequency
    # Nozaradan 2011: frequency-tagging reveals beat-locked cortical response
    e0 = torch.sigmoid(
        0.40 * flux_period_1s + 0.35 * onset_period_1s
        + 0.25 * amp_mean_1s
    )

    # E1: Meter entrainment — metric coupling strength
    # Grahn 2007: beat perception recruits SMA/BG via metric structure
    e1 = torch.sigmoid(
        0.40 * coupling_period_1s + 0.30 * coupling_period_100ms
        + 0.30 * coupling_zc_1s
    )

    # E2: Selective enhancement — entrainment x coupling driven
    # Nozaradan 2018: selective neural enhancement at beat frequency
    e2 = torch.sigmoid(
        0.35 * e0 * e1 + 0.35 * spectral_change_vel
        + 0.30 * loud_entropy
    )

    return e0, e1, e2
