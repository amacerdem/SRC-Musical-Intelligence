"""PSH M-Layer — Temporal Integration (2D).

Silencing efficiency and hierarchy dissociation from H3 temporal context:
  M0: silencing_efficiency    (how effectively predictions silence high-level)
  M1: hierarchy_dissociation  (degree of separation between silenced & persistent)

H3 demands consumed:
  amplitude:        (7,0,0,2), (7,1,0,2), (7,3,0,2), (7,3,2,2)
  onset_strength:   (10,0,0,2), (10,3,0,2)
  spectral_flux:    (21,1,0,2), (21,3,0,2), (21,3,2,2)
  tonal_stability:  (41,3,0,0), (41,8,0,0), (41,16,1,0), (41,16,20,0)
  consonance:       (4,16,1,0)
  periodicity:      (5,16,1,0)

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/mechanisms/psh/
de Vries & Wurm 2023: hierarchical dissociation in prediction timing.
Auksztulewicz 2017: repetition suppression dynamics across timescales.
Carbajal & Malmierca 2018: SSA hierarchy from IC to cortex.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
# Amplitude (low-level sensory persistence context)
_AMP_H0_VAL = (7, 0, 0, 2)        # amplitude at 25ms value integration
_AMP_H1_VAL = (7, 1, 0, 2)        # amplitude at 50ms value integration
_AMP_H3_VAL = (7, 3, 0, 2)        # amplitude at 100ms value integration
_AMP_H3_STD = (7, 3, 2, 2)        # amplitude at 100ms std integration

# Onset strength (PE trigger context)
_ONSET_H0_VAL = (11, 0, 0, 2)     # onset_strength at 25ms value integration
_ONSET_H3_VAL = (11, 3, 0, 2)     # onset_strength at 100ms value integration

# Spectral flux (error magnitude context)
_FLUX_H1_VAL = (21, 1, 0, 2)      # spectral_flux at 50ms value integration
_FLUX_H3_VAL = (21, 3, 0, 2)      # spectral_flux at 100ms value integration
_FLUX_H3_STD = (21, 3, 2, 2)      # spectral_flux at 100ms std integration

# Tonal stability (high-level coupling context)
_TONAL_H3_VAL = (41, 3, 0, 0)     # tonal_stability at 100ms value memory
_TONAL_H8_VAL = (41, 8, 0, 0)     # tonal_stability at 500ms value memory
_TONAL_H16_MEAN = (41, 16, 1, 0)  # tonal_stability at 1s mean memory
_TONAL_H16_ENT = (41, 16, 20, 0)  # tonal_stability at 1s entropy memory

# Consonance and periodicity (long-range context)
_CONSONANCE_H16_MEAN = (4, 16, 1, 0)   # sensory_pleasantness at 1s mean memory
_PERIODICITY_H16_MEAN = (5, 16, 1, 0)  # periodicity at 1s mean memory


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: silencing efficiency and hierarchy dissociation.

    M0 measures how effectively the predictive system silences high-level
    representations. Strong tonal context (high tonal stability, low
    uncertainty) + stable consonance = efficient silencing. When high-level
    features are highly predictable, suppression is maximal.

    M1 measures the degree of dissociation between silenced (high-level)
    and persistent (low-level) representations. Large dissociation =
    strong prediction hierarchy. de Vries & Wurm 2023: eta_p^2 = 0.49
    for hierarchical dissociation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1 = e

    # -- H3 features --
    # High-level coupling (tonal stability across timescales)
    tonal_h3 = h3_features[_TONAL_H3_VAL]
    tonal_h8 = h3_features[_TONAL_H8_VAL]
    tonal_h16_mean = h3_features[_TONAL_H16_MEAN]
    tonal_h16_ent = h3_features[_TONAL_H16_ENT]

    # Long-range context
    consonance_1s = h3_features[_CONSONANCE_H16_MEAN]
    periodicity_1s = h3_features[_PERIODICITY_H16_MEAN]

    # Low-level sensory dynamics
    amp_h0 = h3_features[_AMP_H0_VAL]
    amp_h3_std = h3_features[_AMP_H3_STD]

    # Error dynamics
    flux_h3 = h3_features[_FLUX_H3_VAL]
    flux_h3_std = h3_features[_FLUX_H3_STD]

    # -- M0: Silencing Efficiency --
    # High tonal stability (predictions are strong) + low uncertainty
    # (entropy) = efficient silencing of high-level representations.
    # Auksztulewicz 2017: repetition suppression increases with
    # predictability. Inverted entropy: lower uncertainty -> more silencing.
    m0 = torch.sigmoid(
        0.25 * tonal_h16_mean
        + 0.25 * tonal_h8
        + 0.20 * consonance_1s
        + 0.15 * periodicity_1s
        + 0.15 * (1.0 - tonal_h16_ent)
    )

    # -- M1: Hierarchy Dissociation --
    # Degree of separation between silenced high-level and persistent
    # low-level. Large when E0 (high-level proxy) is high but low-level
    # features show ongoing variability (PE). Small flux variability
    # with high tonal context = maximal dissociation.
    # de Vries & Wurm 2023: eta_p^2 = 0.49 (large effect).
    # Carbajal & Malmierca 2018: SSA gradient from IC to cortex.
    m1 = torch.sigmoid(
        0.30 * e0
        + 0.25 * tonal_h3
        + 0.25 * (amp_h0 + amp_h3_std)
        + 0.20 * (flux_h3 - flux_h3_std)
    )

    return m0, m1
