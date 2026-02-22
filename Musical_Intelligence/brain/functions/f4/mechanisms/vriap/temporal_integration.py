"""VRIAP M-Layer -- Temporal Integration (2D).

Temporal dynamics for analgesia estimation and active-passive differentiation:
  M0: analgesia_index       -- Composite analgesia (product of E0*E1*E2) [0, 1]
  M1: active_passive_differential -- Motor contribution beyond passive [0, 1]

Analgesia index (M0) is multiplicative: all three E-layer components
(motor engagement, pain gating, multi-modal binding) must co-activate.
If any component is absent, analgesia collapses toward zero. Matches
clinical evidence: active VR + music > passive listening (Liang 2025;
Arican & Soyman 2025).

Active-passive differential (M1) captures the advantage of active motor
engagement over passive distraction. Uses the difference between
engagement (E0) and a familiarity proxy from H3 pleasant/roughness
trends.

H3 demands consumed (5):
  (11, 20, 1, 0) onset_strength mean H20 L0   -- sustained motor drive 5s
  (10, 20, 1, 0) loudness mean H20 L0         -- sustained immersion 5s
  (7, 20, 4, 0)  amplitude max H20 L0         -- engagement ceiling 5s
  (4, 20, 18, 0) sensory_pleasantness trend H20 L0 -- comfort trajectory
  (0, 20, 18, 0) roughness trend H20 L0       -- dissonance trajectory

See Building/C3-Brain/F4-Memory-Systems/mechanisms/vriap/VRIAP-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ONSET_MEAN_H20 = (11, 20, 1, 0)      # onset_strength mean H20 L0
_LOUD_MEAN_H20 = (10, 20, 1, 0)       # loudness mean H20 L0
_AMP_MAX_H20 = (7, 20, 4, 0)          # amplitude max H20 L0
_PLEASANT_TREND_H20 = (4, 20, 18, 0)  # sensory_pleasantness trend H20 L0
_ROUGH_TREND_H20 = (0, 20, 18, 0)     # roughness trend H20 L0


def _familiarity_proxy(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
) -> Tensor:
    """Familiarity proxy from comfort trajectory and low dissonance trend.

    When pleasantness is rising and roughness is falling, the music feels
    familiar/safe. Returns (B, T) in approximately [0, 1] via sigmoid.
    """
    pleasant_trend = h3_features[_PLEASANT_TREND_H20]  # (B, T)
    rough_trend = h3_features[_ROUGH_TREND_H20]        # (B, T)
    return torch.sigmoid(0.50 * pleasant_trend + 0.50 * (1.0 - rough_trend))


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute M-layer: analgesia index and active-passive differential.

    M0 (analgesia_index): Product of all three E-layer signals (E0*E1*E2)
    representing the requirement that motor engagement, pain gating, AND
    multi-modal binding must all be active for meaningful analgesia.
    Arican & Soyman 2025: active engagement required (p=0.001).

    M1 (active_passive_differential): Motor contribution to analgesia
    beyond passive distraction. When engagement (E0) exceeds familiarity,
    active mode dominates. Arican & Soyman 2025: passive music alone not
    significant (p=0.101).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, e2 = e

    # -- M0: Analgesia Index --
    # Multiplicative gating: all three pathways must co-activate.
    # Product is already in [0, 1] since each E component is sigmoid.
    # Liang 2025: VRMS > passive for analgesia; Arican 2025: active > silence
    m0 = (e0 * e1 * e2).clamp(0.0, 1.0)

    # -- M1: Active-Passive Differential --
    # sigma(0.50*f01 + 0.50*(f01 - familiarity))
    # When engagement > familiarity: active mode dominates.
    # When engagement ~ familiarity: passive-like distraction only.
    # Arican & Soyman 2025: passive music alone p=0.101, not significant
    familiarity = _familiarity_proxy(h3_features)      # (B, T)
    m1 = torch.sigmoid(
        0.50 * e0
        + 0.50 * (e0 - familiarity)
    )

    return m0, m1
