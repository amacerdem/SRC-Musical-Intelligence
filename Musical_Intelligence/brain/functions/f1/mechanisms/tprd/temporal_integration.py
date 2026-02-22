"""TPRD M-Layer — Mathematical Model (2D).

Two computed quantities from the tonotopic-pitch encoding:

  M0: dissociation_idx  — Normalized (tono-pitch)/(tono+pitch+ε) → [0,1]
  M1: spectral_pitch_r  — Spectral-to-pitch coherence ratio

No additional H3/R3 — uses only T-layer outputs.

See Docs/C³/Models/IMU-β8-TPRD/TPRD.md §7.2
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor

_EPS = 1e-7


def compute_temporal_integration(
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D mathematical model from T-layer.

    Args:
        e_outputs: ``(T0, T1, T2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    t0, t1, t2 = e_outputs

    # M0: Dissociation Index
    # (tonotopic - pitch) / (tonotopic + pitch + ε) → [-1, 1] → [0, 1]
    # 0.0 = pitch dominant, 0.5 = balanced, 1.0 = tonotopic dominant
    idx_raw = (t0 - t1) / (t0 + t1 + _EPS)
    m0 = (idx_raw + 1.0) / 2.0

    # M1: Spectral-Pitch Ratio (coherence)
    # When tonotopic and pitch are aligned → high coherence
    # When dissociated → low coherence
    m1 = (1.0 - t2) * torch.min(t0, t1) / (torch.max(t0, t1) + _EPS)

    return m0, m1
