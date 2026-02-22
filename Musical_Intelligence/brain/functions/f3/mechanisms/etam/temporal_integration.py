"""ETAM M-Layer -- Temporal Integration (2D).

Attention gain and entrainment index from H3 temporal features + E-layer:
  M0: attention_gain      (entrainment-modulated attentional amplification)
  M1: entrainment_index   (strength of periodic entrainment to beat)

H3 demands consumed:
  x_l0l5:           (25,16,0,2) reused from E-layer
  energy_change:    (22,11,14,2) -- periodicity
  x_l0l5:           (25,16,14,2) -- periodicity

See Building/C3-Brain/F3-Attention-and-Salience/mechanisms/etam/
Grahn & Rowe 2012: beat strength modulates attentional gain in STG.
Tierney & Kraus 2015: EEG phase-locking indexes entrainment strength.
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 keys consumed ---------------------------------------------------------
_COUPLING_VAL_1S = (25, 16, 0, 2)       # coupling value 1s (integration)
_ENERGY_PERIOD_750MS = (22, 11, 14, 2)  # energy periodicity 750ms (integration)
_COUPLING_PERIOD_1S = (25, 16, 14, 2)   # coupling periodicity 1s (integration)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: attention gain and entrainment index.

    M0 captures the attentional amplification produced by successful
    entrainment: when all three temporal windows (E0-E2) align with beat
    expectations and coupling is strong, attention is maximally modulated.

    M1 captures the strength of periodic entrainment by combining energy
    and coupling periodicities -- the core oscillatory signature of beat
    tracking.

    Grahn & Rowe 2012: parametric beat strength in putamen/STG (p<0.001).
    Tierney & Kraus 2015: EEG phase coherence predicts beat tracking.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
        e: ``(E0, E1, E2, E3)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``
    """
    e0, e1, e2, _e3 = e

    coupling_val_1s = h3_features[_COUPLING_VAL_1S]
    energy_period_750ms = h3_features[_ENERGY_PERIOD_750MS]
    coupling_period_1s = h3_features[_COUPLING_PERIOD_1S]

    # -- M0: Attention Gain --
    # Entrainment-modulated attentional amplification. Average of three
    # temporal windows (early/mid/late) provides overall entrainment
    # quality; coupling strength at bar-level provides structural context.
    # Grahn 2012: beat strength parametrically modulates STG/putamen.
    window_avg = (e0 + e1 + e2) / 3.0
    m0 = torch.sigmoid(
        0.60 * window_avg
        + 0.40 * coupling_val_1s
    )

    # -- M1: Entrainment Index --
    # Strength of periodic entrainment. Combines energy periodicity
    # (amplitude envelope regularity) with coupling periodicity (metric
    # structure regularity). High M1 = strong beat-locked oscillation.
    # Tierney 2015: EEG phase-locking to beat envelope.
    m1 = torch.sigmoid(
        0.50 * energy_period_750ms
        + 0.50 * coupling_period_1s
    )

    return m0, m1
