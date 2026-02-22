"""CTBB M-Layer -- Temporal Integration (3D).

Temporal dynamics of cerebellar motor enhancement:
  M0: timing_enhancement      -- iTBS timing improvement magnitude [0, 1]
  M1: sway_reduction          -- Postural sway reduction estimate [0, 1]
  M2: cerebellar_m1_coupling  -- Cerebellar-M1 pathway strength [0, 1]

Timing enhancement (M0) propagates f25 (cerebellar timing) across time,
reflecting LTP-like facilitation lasting ~20-30 min post-iTBS (Huang 2005).
TAU_DECAY = 1800s governs the temporal envelope.

Sway reduction (M1) combines postural control (f27) with inverted balance
variability. SPECIAL: sway = sigma(0.5*f27 + 0.5*(1-balance_var_1s)).
Sansare 2025: greatest sway reduction at 10-20 min post-iTBS, eta-sq=0.202.

Cerebellar-M1 coupling (M2) integrates cerebellar timing (f25) and M1
modulation (f26). coupling = sigma(0.5*f25 + 0.5*f26). Modeled cautiously
given CBI null result (Sansare 2025, eta-sq=0.045 n.s.).

H3 demands consumed (3):
  (10, 3,  0, 2) timing onset 100ms L2
  (10, 16, 1, 0) mean timing 1s L0
  (10, 16, 2, 0) timing variability 1s L0

R3 inputs: spectral_flux[10]

See Building/C3-Brain/F7-Motor-and-Timing/mechanisms/ctbb/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_TIMING_ONSET_H3 = (10, 3, 0, 2)       # timing onset 100ms L2
_TIMING_MEAN_H16 = (10, 16, 1, 0)      # mean timing 1s L0
_TIMING_VAR_H16 = (10, 16, 2, 0)       # timing variability 1s L0

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_SPECTRAL_FLUX = 10

# -- Temporal constants --------------------------------------------------------
TAU_DECAY = 1800.0  # seconds -- iTBS LTP-like facilitation duration


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    upstream_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute M-layer: 3D temporal integration of cerebellar enhancement.

    M0 (timing_enhancement): Propagates f25 cerebellar timing as the
    temporal enhancement signal. iTBS effect follows LTP-like time course
    with TAU_DECAY=1800s. Huang 2005: peak facilitation ~20-30 min.

    M1 (sway_reduction): SPECIAL inversion formula --
    sway = sigma(0.5*f27 + 0.5*(1-balance_var_1s)).
    Sansare 2025: sway reduction = better balance (higher = less sway).

    M2 (cerebellar_m1_coupling): Average of f25 and f26 for functional
    coupling. CBI null (Sansare 2025) means this is modeled cautiously.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 spectral features.
        e_outputs: ``(E0, E1, E2)`` from extraction layer.
        upstream_outputs: ``{"PEOM": ..., "GSSM": ..., "SPMC": ...}``.

    Returns:
        ``(M0, M1, M2)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs  # f25, f26, f27
    B, T = r3_features.shape[:2]
    device = r3_features.device

    # -- H3 features --
    timing_onset = h3_features.get(
        _TIMING_ONSET_H3, torch.zeros(B, T, device=device),
    )
    timing_mean = h3_features.get(
        _TIMING_MEAN_H16, torch.zeros(B, T, device=device),
    )
    timing_var = h3_features.get(
        _TIMING_VAR_H16, torch.zeros(B, T, device=device),
    )

    # -- Import balance_var from E-layer H3 demands (shared key) --
    # Balance variability is consumed in E-layer but needed here too
    _BALANCE_VAR_H16 = (33, 16, 2, 0)
    balance_var = h3_features.get(
        _BALANCE_VAR_H16, torch.zeros(B, T, device=device),
    )

    # -- M0: Timing Enhancement --
    # Direct propagation of f25 (cerebellar timing) as enhancement signal
    # H3 timing features provide temporal scaffolding:
    #   onset (100ms) for immediate, mean (1s) for sustained, var for precision
    # Huang 2005: LTP-like facilitation with TAU_DECAY=1800s
    m0 = torch.sigmoid(
        0.40 * e0
        + 0.30 * timing_mean
        + 0.30 * (1.0 - timing_var)
    )

    # -- M1: Sway Reduction (SPECIAL: inverted formula) --
    # sway_reduction = sigma(0.5 * f27 + 0.5 * (1 - balance_var_1s))
    # Higher = better balance = more sway reduction
    # Sansare 2025: greatest reduction at 10-20 min, eta-sq=0.202
    m1 = torch.sigmoid(
        0.50 * e2
        + 0.50 * (1.0 - balance_var)
    )

    # -- M2: Cerebellar-M1 Coupling --
    # coupling = sigma(0.5 * f25 + 0.5 * f26)
    # Sansare 2025 CBI null: direct pathway contribution uncertain
    m2 = torch.sigmoid(
        0.50 * e0
        + 0.50 * e1
    )

    return m0, m1, m2
