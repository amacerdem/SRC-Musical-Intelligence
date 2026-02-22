"""SPMC E-Layer -- Extraction (3D).

SMA-Premotor-M1 Motor Circuit extraction features:

  f19: sequence_planning    -- SMA temporal sequence encoding [0, 1]
  f20: motor_preparation    -- PMC action selection & motor readiness [0, 1]
  f21: execution_output     -- M1 motor execution output [0, 1]

The E-layer extracts the three core nodes of the hierarchical SMA-PMC-M1
motor circuit.  SMA encodes temporal sequences at the longest timescale;
PMC performs action selection at medium timescale; M1 executes motor
output at the shortest timescale.  f21 uses the multiplicative interaction
f19 * f20 to capture hierarchical flow -- execution depends on both
planning and preparation being active.

H3 consumed (6 tuples -- E-layer):
    (10, 3, 0, 2)    onset_strength value H3 L2         -- SMA onset tracking 100ms
    (10, 16, 14, 2)  onset_strength periodicity H16 L2  -- SMA beat periodicity 1s
    (11, 3, 0, 2)    onset_strength value H3 L2         -- motor timing marker 100ms
    (11, 16, 14, 2)  onset_strength periodicity H16 L2  -- onset periodicity 1s
    (21, 4, 8, 0)    spectral_change velocity H4 L0     -- tempo velocity 125ms
    (7, 16, 1, 2)    amplitude mean H16 L2              -- mean motor output level 1s

R3 consumed:
    [7]      amplitude           -- motor output strength for M1
    [10]     spectral_flux       -- onset detection for SMA sequence markers
    [11]     onset_strength      -- beat event for motor timing signal
    [21]     spectral_change     -- tempo rate for SMA tempo encoding
    [25:33]  x_l0l5              -- hierarchical circuit coupling (SMA-PMC-M1)

Upstream reads:
    PEOM relay (11D), ASAP (11D), VRMSME (11D) -- via relay_outputs

Grahn & Brett 2007: SMA + putamen respond to beat in metric rhythms
    (F(2,38)=20.67, p<.001).
Hoddinott & Grahn 2024: SMA multi-voxel patterns encode beat strength
    via RSA.
Kohler 2025: M1 MVPA content-specific action representations.
Pierrieau 2025: beta oscillations (13-30 Hz) predict motor flexibility.

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/spmc/e_layer.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples (E-layer: 6 tuples) -------------------------------------------
_ONSET_VAL_H3 = (10, 3, 0, 2)          # SMA onset tracking 100ms
_ONSET_PERIOD_H16 = (10, 16, 14, 2)    # SMA beat periodicity 1s
_BEAT_VAL_H3 = (11, 3, 0, 2)           # motor timing marker 100ms
_BEAT_PERIOD_H16 = (11, 16, 14, 2)     # onset periodicity 1s
_TEMPO_VEL_H4 = (21, 4, 8, 0)          # tempo velocity 125ms
_AMP_MEAN_H16 = (7, 16, 1, 2)          # mean motor output level 1s

# -- R3 indices (post-freeze 97D) --------------------------------------------
_AMPLITUDE = 7
_SPECTRAL_FLUX = 10
_ONSET_STRENGTH = 11
_SPECTRAL_CHANGE = 21
_X_L0L5_START = 25
_X_L0L5_END = 33


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """E-layer: 3D extraction from H3/R3 + relay features.

    Computes the three hierarchical motor circuit nodes:
        f19 (SMA sequence planning): Beat periodicity at 1s drives this
            feature, reflecting SMA's role in encoding temporal structure.
            Grahn & Brett 2007: SMA activation scales with metrical
            complexity (F(2,38)=20.67).
        f20 (PMC motor preparation): Combines circuit periodicity with
            tempo velocity for action selection readiness.  Pierrieau 2025:
            beta oscillations in motor cortex predict action selection.
        f21 (M1 execution output): Multiplicative interaction f19 * f20
            captures hierarchical flow -- execution depends on both
            planning and preparation.  Kohler 2025: M1 MVPA.

    All formulas use sigmoid with coefficient sums <= 1.0 (saturation rule).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)``.
        relay_outputs: ``{"PEOM": ..., "ASAP": ..., "VRMSME": ...}``.

    Returns:
        ``(f19, f20, f21)`` each ``(B, T)``.
    """
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    onset_val = h3_features[_ONSET_VAL_H3]          # (B, T)
    beat_period_1s = h3_features[_ONSET_PERIOD_H16]  # (B, T)
    beat_val = h3_features[_BEAT_VAL_H3]             # (B, T)
    onset_period_1s = h3_features[_BEAT_PERIOD_H16]  # (B, T)
    tempo_vel = h3_features[_TEMPO_VEL_H4]           # (B, T)
    amp_mean_1s = h3_features[_AMP_MEAN_H16]         # (B, T)

    # -- R3 features --
    amplitude = r3_features[..., _AMPLITUDE]                # (B, T)
    spectral_flux = r3_features[..., _SPECTRAL_FLUX]        # (B, T)
    onset_strength = r3_features[..., _ONSET_STRENGTH]      # (B, T)
    spectral_change = r3_features[..., _SPECTRAL_CHANGE]    # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    circuit_period = x_l0l5.mean(dim=-1)                    # (B, T)

    # -- Upstream relay features (graceful fallback) --
    peom = relay_outputs.get("PEOM", torch.zeros(B, T, 11, device=device))
    # PEOM P-layer: period_lock_strength (idx 7), kinematic_smoothness (idx 8)
    period_lock = peom[..., 7]    # (B, T)

    # -- f19: Sequence Planning (SMA temporal sequence encoding) --
    # Beat periodicity at 1s drives SMA's temporal sequence encoding.
    # Grahn & Brett 2007: SMA F(2,38)=20.67.
    # Hoddinott & Grahn 2024: SMA RSA beat-strength patterns.
    # f19 = sigma(0.40 * beat_period_1s)
    f19 = torch.sigmoid(
        0.40 * beat_period_1s
        + 0.30 * onset_val * spectral_flux.clamp(min=0.1)
        + 0.30 * period_lock
    )

    # -- f20: Motor Preparation (PMC action selection) --
    # Combines circuit periodicity with tempo velocity for action readiness.
    # Pierrieau 2025: beta (13-30 Hz) predict motor flexibility.
    # Kohler 2025: PMC content-specific action representations.
    # f20 = sigma(0.30 * circuit_period_1s + 0.30 * tempo_velocity)
    f20 = torch.sigmoid(
        0.30 * circuit_period
        + 0.30 * tempo_vel
        + 0.20 * onset_period_1s
        + 0.20 * beat_val * onset_strength.clamp(min=0.1)
    )

    # -- f21: Execution Output (M1 motor execution) --
    # Multiplicative interaction: execution depends on both planning and
    # preparation being active.  Amplitude modulates output strength.
    # Kohler 2025: M1 MVPA self-produced actions.
    # Harrison 2025: sensorimotor cortex during musically-cued movements.
    # f21 = sigma(0.35 * f19 * f20 + 0.30 * mean_amplitude_1s)
    f21 = torch.sigmoid(
        0.35 * f19 * f20
        + 0.30 * amp_mean_1s
        + 0.20 * amplitude.clamp(min=0.1) * spectral_change.clamp(min=0.1)
        + 0.15 * circuit_period
    )

    return f19, f20, f21
