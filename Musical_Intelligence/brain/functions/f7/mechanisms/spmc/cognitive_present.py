"""SPMC P-Layer -- Cognitive Present (2D).

SMA-Premotor-M1 Motor Circuit present-moment features:

  sma_activity (dim 6) -- Temporal-context SMA planning activation [0, 1]
  m1_output    (dim 7) -- Beat-entrainment M1 execution output [0, 1]

The P-layer captures the instantaneous state of the two primary cortical
nodes in the motor hierarchy.  SMA activity represents the current
planning activation driven by sequence planning combined with short-
timescale (100ms) onset and circuit coupling signals.  M1 output
represents the current execution state from beat-by-beat motor response.

The P-layer uses the shortest H3 horizons (100ms, value morphology) to
ground the present-moment motor state, distinguishing it from the longer
integration windows of the M-layer and the predictive horizons of the
F-layer.

H3 consumed (4 tuples -- P-layer):
    (10, 3, 0, 2)  onset_strength value H3 L2  -- onset tracking 100ms (SMA)
    (11, 3, 0, 2)  onset_strength value H3 L2  -- motor timing marker 100ms (M1)
    (25, 3, 0, 2)  x_l0l5 value H3 L2          -- circuit coupling 100ms (SMA)
    (33, 3, 0, 2)  x_l4l5 value H3 L2          -- sequence regularity 100ms (M1)

R3 consumed:
    [10]     spectral_flux   -- onset tracking for SMA present state
    [11]     onset_strength  -- beat event for M1 present state
    [25:33]  x_l0l5          -- circuit coupling for SMA present activity
    [33:41]  x_l4l5          -- sequence regularity for M1 present output

Grahn & Brett 2007: pre-SMA activation for beat induction (Z=5.03).
Hoddinott & Grahn 2024: SMA patterns encode beat strength in present
    moment (RSA).
Kohler 2025: left M1 content-specific representations of self-produced
    actions (MVPA).
Harrison 2025: sensorimotor cortex during externally/internally cued
    movements.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/spmc/p_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (P-layer: 4 tuples) -------------------------------------------
_ONSET_VAL_H3 = (10, 3, 0, 2)     # onset tracking 100ms for SMA
_BEAT_VAL_H3 = (11, 3, 0, 2)      # motor timing marker 100ms for M1
_CIRCUIT_VAL_H3 = (25, 3, 0, 2)   # circuit coupling 100ms for SMA
_SEQ_VAL_H3 = (33, 3, 0, 2)       # sequence regularity 100ms for M1

# -- R3 indices ---------------------------------------------------------------
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41


def compute_cognitive_present(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """P-layer: 2D present-moment motor state from E/M layers + H3/R3.

    Computes two cortical node snapshots:
        sma_activity (dim 6): Current SMA planning activation.  Combines
            E-layer sequence planning (f19) with 100ms onset tracking and
            circuit coupling.  Grahn & Brett 2007: pre-SMA Z=5.03.
            Hoddinott & Grahn 2024: SMA RSA beat-strength.
        m1_output (dim 7): Current M1 execution state.  Combines E-layer
            execution output (f21) with 100ms motor timing markers and
            sequence regularity.  Kohler 2025: left M1 MVPA.
            Harrison 2025: sensorimotor cortex activation.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)``.
        e: ``(f19, f20, f21)`` from E-layer.
        m: ``(circuit_flow, hierarchy_index, timing_precision)`` from M-layer.

    Returns:
        ``(sma_activity, m1_output)`` each ``(B, T)``.
    """
    f19, _f20, f21 = e
    circuit_flow, _hierarchy_index, timing_precision = m

    # -- H3 features (100ms horizons -- cognitive present) --
    onset_val = h3_features[_ONSET_VAL_H3]       # (B, T)
    beat_val = h3_features[_BEAT_VAL_H3]          # (B, T)
    circuit_val = h3_features[_CIRCUIT_VAL_H3]    # (B, T)
    seq_val = h3_features[_SEQ_VAL_H3]            # (B, T)

    # -- R3 features --
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]        # (B, T)
    onset_strength = r3_features[..., _ONSET_STRENGTH]      # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l0l5_mean = x_l0l5.mean(dim=-1)                       # (B, T)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]  # (B, T, 8)
    x_l4l5_mean = x_l4l5.mean(dim=-1)                       # (B, T)

    # -- sma_activity (dim 6): SMA planning activation --
    # Sequence planning + 100ms onset tracking + circuit coupling.
    # Short-timescale grounds present-moment planning state.
    # Grahn & Brett 2007: pre-SMA Z=5.03 for beat induction.
    sma_activity = torch.sigmoid(
        0.35 * f19
        + 0.25 * onset_val * spectral_flux.clamp(min=0.1)
        + 0.20 * circuit_val * x_l0l5_mean.clamp(min=0.1)
        + 0.20 * circuit_flow
    )

    # -- m1_output (dim 7): M1 execution output --
    # Execution output + 100ms motor timing + sequence regularity.
    # Beat-by-beat motor response in the present moment.
    # Kohler 2025: M1 MVPA self-produced actions.
    m1_output = torch.sigmoid(
        0.35 * f21
        + 0.25 * beat_val * onset_strength.clamp(min=0.1)
        + 0.20 * seq_val * x_l4l5_mean.clamp(min=0.1)
        + 0.20 * timing_precision
    )

    return sma_activity, m1_output
