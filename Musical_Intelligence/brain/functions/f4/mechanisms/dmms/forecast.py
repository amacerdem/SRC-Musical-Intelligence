"""DMMS F-Layer -- Forecast (3D).

Three forward predictions for scaffold persistence, preference formation,
and therapeutic potential:

  F0: scaffold_persistence    -- Scaffold persistence prediction (36s) [0, 1]
  F1: preference_formation    -- Preference formation prediction (5s) [0, 1]
  F2: therapeutic_potential   -- Therapeutic potential prediction [0, 1]

H3 consumed:
    (3, 24, 1, 0)   stumpf_fusion mean H24 L0     -- long-term binding (shared M)
    (10, 24, 3, 0)  loudness std H24 L0           -- arousal variability 36s
    (22, 24, 19, 0) entropy stability H24 L0      -- pattern stability 36s
    (7, 20, 4, 0)   amplitude max H20 L0          -- peak energy 5s

F-layer also reuses M-layer scaffold_strength and P-layer scaffold_activation.

See Building/C3-Brain/F4-Memory-Systems/mechanisms/dmms/DMMS-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_36S = (3, 24, 1, 0)        # stumpf_fusion mean H24 L0 (shared M)
_LOUD_STD_36S = (10, 24, 3, 0)          # loudness std H24 L0
_ENTROPY_STAB_36S = (22, 24, 19, 0)     # entropy stability H24 L0
_AMP_MAX_5S = (7, 20, 4, 0)             # amplitude max H20 L0


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor, Tensor],
    p_outputs: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from E/M/P outputs + H3 context.

    F0 (scaffold_persistence) predicts whether current scaffold activation
    will be sustained over a 36-second window using H24 horizon signals.
    High persistence means the hippocampal-cortical dialogue is actively
    consolidating the scaffold trace.
    Qiu 2025: dose-dependent social behavior improvement from prenatal-infant
    music exposure (r=0.38, p<0.0001).

    F1 (preference_formation) predicts whether current musical exposure is
    forming new preference scaffolds over a 5-second consolidation window.
    Uses H20 horizon with familiarity trend.
    Trainor & Unrau 2012: training before age 7 enhances processing.

    F2 (therapeutic_potential) predicts the clinical utility of current music
    for therapy applications. Product of scaffold_activation and consonance.
    High when music accesses deep developmental memories.
    Scholkmann 2024: CMT induces measurable hemodynamic changes in neonatal
    cortex (fNIRS, N=17).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.
        m_outputs: ``(M0, M1)`` each ``(B, T)``.
        p_outputs: ``(P0, P1)`` each ``(B, T)``.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _e0, e1, _e2 = e_outputs
    m0, m1 = m_outputs
    p0, _p1 = p_outputs

    # -- H3 features --
    stumpf_mean_36s = h3_features[_STUMPF_MEAN_36S]     # (B, T)
    loud_std_36s = h3_features[_LOUD_STD_36S]           # (B, T)
    entropy_stab_36s = h3_features[_ENTROPY_STAB_36S]   # (B, T)
    amp_max_5s = h3_features[_AMP_MAX_5S]               # (B, T)

    # -- Derived signals --
    scaffold_activation = p0                              # (B, T)
    scaffold_strength = m0                                # (B, T)

    # F0: Scaffold Persistence -- hippocampal consolidation at H24 (36s)
    # Qiu 2025: dose-dependent social behavior from prenatal-infant exposure
    # Long-term binding + stability signals predict persistence
    f0 = torch.sigmoid(
        0.30 * scaffold_strength
        + 0.25 * stumpf_mean_36s
        + 0.25 * entropy_stab_36s
        + 0.20 * (1.0 - loud_std_36s)
    )

    # F1: Preference Formation -- consolidation at H20 (5s)
    # Trainor & Unrau 2012: training-dependent auditory development
    # Plasticity (E1) + imprinting depth (M1) + peak energy (salience)
    f1 = torch.sigmoid(
        0.35 * e1
        + 0.35 * m1
        + 0.30 * amp_max_5s
    )

    # F2: Therapeutic Potential -- scaffold_activation * consonance proxy
    # Scholkmann 2024: CMT hemodynamic changes in neonatal cortex
    # High when music accesses deep scaffolds with pleasant quality
    # consonance proxy from entropy stability (stable patterns = consonant)
    f2 = (scaffold_activation * entropy_stab_36s).clamp(0.0, 1.0)

    return f0, f1, f2
