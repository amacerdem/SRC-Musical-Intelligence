"""BARM M-Layer -- Temporal Integration (2D).

Brainstem response modulation integrated over temporal windows:
  M0: veridical_perception  (accuracy of brainstem temporal representation)
  M1: regularization_effect (strength of imposed temporal regularity)

M0 integrates beat alignment (E1) with sync benefit (E2) to assess how
veridically the brainstem encodes the temporal structure. M1 combines
regularization tendency (E0) with spectral change periodicity to measure
how strongly the brainstem imposes structure on irregular input.

H3 demands consumed:
  spectral_change:  (21,8,14,0)  periodicity at 500ms memory

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/barm/
Skoe & Kraus 2010: brainstem faithfully encodes temporal fine structure.
Musacchia et al. 2007: enhanced subcortical representation in musicians.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_SPEC_CHANGE_H8_PERIOD = (21, 8, 14, 0)     # spectral_change periodicity 500ms memory


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: integrated brainstem modulation signals.

    M0 (veridical_perception) assesses how faithfully the brainstem
    represents the temporal structure. High beat alignment (E1) combined
    with sync benefit (E2) indicates accurate subcortical encoding.

    M1 (regularization_effect) captures the net effect of the brainstem's
    tendency to regularize. Combines E0 (regularization tendency) with
    the spectral change periodicity as an inverse-regularity reference:
    low periodicity means the signal is irregular, requiring more
    regularization.

    Skoe & Kraus 2010: Brainstem responses faithfully encode temporal
    fine structure; musicians show superior encoding (d=1.2).
    Musacchia et al. 2007: Enhanced subcortical representation measured
    via ABR amplitude (d=0.8).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2 = e

    # -- H3 features --
    spec_change_period = h3_features[_SPEC_CHANGE_H8_PERIOD]   # (B, T)

    # -- M0: Veridical Perception --
    # Accurate brainstem encoding = good beat alignment + sync benefit.
    # When both are high, the subcortical representation is faithful.
    m0 = torch.sigmoid(
        0.50 * e1
        + 0.50 * e2
    )

    # -- M1: Regularization Effect --
    # The net strength of regularization: E0 provides the tendency,
    # and (1 - spectral change periodicity) provides the amount of
    # irregularity that the brainstem must compensate for.
    m1 = torch.sigmoid(
        0.50 * e0
        + 0.50 * (1.0 - spec_change_period)
    )

    return m0, m1
