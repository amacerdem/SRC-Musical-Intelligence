"""RIRI M-Layer -- Temporal Integration (2D).

Multi-modal rehabilitation integration over temporal windows:
  M0: integration_synergy  (geometric mean of E0 x E1 x E2 -- all must contribute)
  M1: temporal_coherence   (cross-modal phase-locked timing quality)

M0 uses the geometric mean (cube root of product) so that if ANY E-layer
pathway collapses to zero the overall synergy collapses.  This models the
empirical finding that synchronized multi-modal stimulation outperforms any
single modality (Jiao 2025, Liang 2025).

M1 measures how tightly all modality channels maintain phase-locked timing.
High coherence = effective rehabilitation.

H3 consumed (M-layer):
  (25, 16, 19, 0)  x_l0l5[0] stability H16 L0   -- entrainment stability 1s
  (11, 6, 14, 2)   onset_strength periodicity H6 L2 -- rhythmic regularity (shared with E)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/riri/RIRI-temporal-integration.md
Jiao 2025: multi-modal synergy enhances rehabilitation outcomes.
Ross & Balasubramaniam 2022: cerebellar forward models for predictive timing.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed (M-layer) ------------------------------------------------
_COUPLING_L0L5_H16_STAB = (25, 16, 19, 0)  # x_l0l5 stability H16 L0
_ONSET_H6_PERIOD = (11, 6, 14, 2)           # onset_strength periodicity H6 L2


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: integration synergy and temporal coherence.

    M0 (integration_synergy) is the geometric mean of the three E-layer
    outputs.  All three rehabilitation pathways -- entrainment, sensorimotor
    integration, and enhanced recovery -- must contribute for synergy to be
    high.  If any single pathway fails, synergy collapses to zero.
    Jiao 2025: multi-modal synergy enhances outcomes.

    M1 (temporal_coherence) measures cross-modal phase-locked timing
    quality.  Entrainment stability (H16, x_l0l5) and onset periodicity
    (H6) combine to indicate how tightly all modality channels maintain
    phase-locked timing.
    Ross & Balasubramaniam 2022: cerebellar forward models for predictive
    timing.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2 = e

    # -- H3 features -------------------------------------------------------
    stability = h3_features[_COUPLING_L0L5_H16_STAB]  # (B, T)
    onset_period = h3_features[_ONSET_H6_PERIOD]       # (B, T)

    # -- M0: Integration Synergy -------------------------------------------
    # Geometric mean of E0 x E1 x E2.  The cube root ensures all three
    # components must contribute.  E-layer outputs are already in [0,1]
    # via sigmoid, so the product is non-negative.
    # synergy = (E0 * E1 * E2) ^ (1/3)
    product = e0 * e1 * e2                  # (B, T), all in [0, 1]
    m0 = torch.pow(product + 1e-8, 1.0 / 3.0)

    # -- M1: Temporal Coherence --------------------------------------------
    # Cross-modal phase-locked timing quality.
    # sigma(0.50 * entrainment_stability + 0.50 * onset_periodicity)
    m1 = torch.sigmoid(
        0.50 * stability
        + 0.50 * onset_period
    )

    return m0, m1
