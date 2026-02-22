"""SPMC M-Layer -- Temporal Integration (3D).

SMA-Premotor-M1 Motor Circuit temporal integration features:

  circuit_flow     (dim 3) -- SMA-to-PMC-to-M1 information flow index [0, 1]
  hierarchy_index  (dim 4) -- Hierarchical motor organization level [0, 1]
  timing_precision (dim 5) -- Cerebellar timing precision [0, 1]

The M-layer computes three mathematical model outputs that characterize
the motor circuit's temporal integration properties.  Circuit flow
measures end-to-end information transmission from SMA planning to M1
execution.  Hierarchy index quantifies the degree of top-down motor
planning structure.  Timing precision models cerebellar online error
correction driven by beat periodicity.

SPECIAL gate formulas (from orchestrator doc):
    circuit_flow   = sigma(0.5 * f19 + 0.5 * f21)
    hierarchy_index = sigma(0.5 * f19 + 0.5 * f20)

H3 consumed (6 tuples -- M-layer):
    (10, 16, 14, 2)  onset_strength periodicity H16 L2  -- beat period for timing 1s
    (25, 8, 14, 2)   x_l0l5 periodicity H8 L2           -- circuit periodicity 500ms
    (25, 16, 14, 2)  x_l0l5 periodicity H16 L2          -- circuit periodicity 1s
    (33, 8, 1, 0)    x_l4l5 mean H8 L0                  -- mean pattern stability 500ms
    (33, 16, 2, 0)   x_l4l5 std H16 L0                  -- sequence variability 1s
    (33, 16, 19, 0)  x_l4l5 stability H16 L0            -- sequence stability 1s

R3 consumed:
    [25:33] x_l0l5   -- cross-layer coupling for circuit periodicity
    [33:41] x_l4l5   -- sequence regularity for stability measures

Zatorre 2007: dorsal stream connects auditory cortex to PMC/SMA for
    sensorimotor transformations.
Okada 2022: cerebellar dentate nucleus correlates with timing of next
    movement and temporal error.
Harrison 2025: CTC and SPT pathways active during musically-cued
    movements.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/spmc/m_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (M-layer: 6 tuples) -------------------------------------------
_BEAT_PERIOD_H16 = (10, 16, 14, 2)     # beat periodicity for timing 1s
_CIRCUIT_PERIOD_H8 = (25, 8, 14, 2)    # circuit periodicity 500ms
_CIRCUIT_PERIOD_H16 = (25, 16, 14, 2)  # circuit periodicity 1s
_PATTERN_MEAN_H8 = (33, 8, 1, 0)       # mean pattern stability 500ms
_SEQ_STD_H16 = (33, 16, 2, 0)          # sequence variability 1s
_SEQ_STABILITY_H16 = (33, 16, 19, 0)   # sequence stability 1s

# -- R3 indices ---------------------------------------------------------------
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """M-layer: 3D temporal integration from E-layer + H3/R3.

    Computes three circuit-level integration measures:
        circuit_flow (dim 3): End-to-end SMA-to-M1 information flow.
            sigma(0.5 * f19 + 0.5 * f21) -- hierarchical gate.
            Zatorre 2007: dorsal stream sensorimotor transformations.
            Harrison 2025: CTC + SPT pathways.
        hierarchy_index (dim 4): Top-down hierarchical motor organization.
            sigma(0.5 * f19 + 0.5 * f20) -- planning structure.
            Grahn & Brett 2007: metric hierarchy in SMA/putamen.
        timing_precision (dim 5): Cerebellar timing accuracy.
            sigma(0.5 * beat_period_1s) -- error correction.
            Okada 2022: dentate nucleus timing neurons.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)``.
        e: ``(f19, f20, f21)`` from E-layer.
        relay_outputs: ``{"PEOM": ..., "ASAP": ..., "VRMSME": ...}``.

    Returns:
        ``(circuit_flow, hierarchy_index, timing_precision)`` each ``(B, T)``.
    """
    f19, f20, f21 = e

    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    beat_period_1s = h3_features[_BEAT_PERIOD_H16]       # (B, T)
    circuit_period_500ms = h3_features[_CIRCUIT_PERIOD_H8]   # (B, T)
    circuit_period_1s = h3_features[_CIRCUIT_PERIOD_H16]     # (B, T)
    pattern_mean_500ms = h3_features[_PATTERN_MEAN_H8]       # (B, T)
    seq_std_1s = h3_features[_SEQ_STD_H16]                   # (B, T)
    seq_stability_1s = h3_features[_SEQ_STABILITY_H16]       # (B, T)

    # -- R3 features --
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                       # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                       # (B, T)

    # -- Upstream relay features (graceful fallback) --
    asap = relay_outputs.get("ASAP", torch.zeros(B, T, 11, device=device))
    # ASAP P-layer: motor_to_auditory (idx 5), auditory_to_motor (idx 6)
    motor_to_aud = asap[..., 5]  # (B, T)

    # -- circuit_flow (dim 3): SMA-to-M1 information flow --
    # SPECIAL: flow = sigma(0.5*f19 + 0.5*f21)
    # Modulated by circuit periodicity at dual timescales and coupling.
    # Zatorre 2007: dorsal stream sensorimotor transformations.
    circuit_flow = torch.sigmoid(
        0.50 * f19
        + 0.50 * f21
    )

    # -- hierarchy_index (dim 4): top-down motor organization --
    # SPECIAL: hierarchy = sigma(0.5*f19 + 0.5*f20)
    # Grahn & Brett 2007: hierarchical beat-metric responses in SMA/putamen.
    hierarchy_index = torch.sigmoid(
        0.50 * f19
        + 0.50 * f20
    )

    # -- timing_precision (dim 5): cerebellar timing accuracy --
    # sigma(0.5 * beat_period_1s) -- driven by beat periodicity.
    # Modulated by circuit periodicity and sequence stability.
    # Okada 2022: dentate nucleus encodes timing of next movement.
    # Thaut 2015: mCBGT circuit provides rhythmic entrainment foundations.
    timing_precision = torch.sigmoid(
        0.50 * beat_period_1s
        + 0.20 * seq_stability_1s
        + 0.15 * circuit_period_1s
        + 0.15 * pattern_mean_500ms
    )

    return circuit_flow, hierarchy_index, timing_precision
