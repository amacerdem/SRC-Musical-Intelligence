"""VRIAP F-Layer -- Forecast (3D).

Forward predictions for analgesic trajectory and motor engagement:
  F0: analgesia_fc    -- Analgesia trajectory prediction (2-5s ahead) [0, 1]
  F1: engagement_fc   -- Motor engagement prediction (1-3s ahead) [0, 1]
  F2: reserved        -- Reserved for future expansion (zeros) [0, 1]

Analgesia forecast (F0) projects analgesic state 2-5s forward using
H20 (5s window) trend features. Predicts building/stable/declining
analgesia from engagement, pain gating, and multi-modal binding
trajectories. Liang 2025: sustained VRMS FC effects over block durations.

Engagement forecast (F1) projects motor engagement 1-3s ahead using
current state features. Tracks immediate motor coupling trajectory
for anticipating engagement lapses or strengthening.

Reserved (F2) is a placeholder for therapeutic consolidation prediction
using H24 (36s) horizon, currently outputs zeros.

H3 demands consumed (shared with M-layer, plus 5 new):
  (4, 20, 18, 0)  sensory_pleasantness trend H20 L0 -- comfort trajectory
  (0, 20, 18, 0)  roughness trend H20 L0            -- dissonance trajectory
  (10, 20, 1, 0)  loudness mean H20 L0              -- sustained engagement
  (10, 24, 3, 0)  loudness std H24 L0               -- engagement variability
  (22, 20, 1, 0)  entropy mean H20 L0               -- complexity 5s
  (22, 24, 19, 0) entropy stability H24 L0           -- pattern stability 36s
  (3, 20, 1, 0)   stumpf_fusion mean H20 L0         -- binding stability 5s
  (21, 20, 1, 0)  spectral_flux mean H20 L0         -- change rate 5s

See Building/C3-Brain/F4-Memory-Systems/mechanisms/vriap/VRIAP-forecast.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEASANT_TREND_H20 = (4, 20, 18, 0)   # sensory_pleasantness trend H20 L0
_ROUGH_TREND_H20 = (0, 20, 18, 0)      # roughness trend H20 L0
_LOUD_MEAN_H20 = (10, 20, 1, 0)        # loudness mean H20 L0
_LOUD_STD_H24 = (10, 24, 3, 0)         # loudness std H24 L0
_ENTROPY_MEAN_H20 = (22, 20, 1, 0)     # entropy mean H20 L0
_ENTROPY_STAB_H24 = (22, 24, 19, 0)    # entropy stability H24 L0
_STUMPF_MEAN_H20 = (3, 20, 1, 0)       # stumpf_fusion mean H20 L0
_SFLUX_MEAN_H20 = (21, 20, 1, 0)       # spectral_flux mean H20 L0


def _predict_future(
    trajectory: Tensor,
    context: Tensor,
    stability: Tensor,
) -> Tensor:
    """Generic future prediction from trajectory, context, and stability.

    Combines current trajectory direction with contextual support and
    stability anchor to estimate near-future state.

    Args:
        trajectory: (B, T) direction signal (trend or current value).
        context: (B, T) contextual support (mean engagement, etc.).
        stability: (B, T) stability anchor (variability, pattern consistency).

    Returns:
        (B, T) predicted future state via sigmoid.
    """
    return torch.sigmoid(
        0.40 * trajectory
        + 0.35 * context
        + 0.25 * stability
    )


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: analgesia forecast, engagement forecast, reserved.

    F0 (analgesia_fc): Analgesia trajectory from comfort trend (pleasant
    rising, roughness falling), sustained engagement (loudness mean),
    and binding stability (stumpf mean). Predicts analgesic state 2-5s.
    Liang 2025: sustained VRMS FC across experimental blocks.

    F1 (engagement_fc): Motor engagement trajectory from encoding state
    dynamics and pattern stability. Uses entropy mean (predictability
    context) and spectral flux mean (sustained change). Predicts 1-3s.

    F2 (reserved): Zeros. Future: therapeutic consolidation at H24.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, _e1, e2 = e
    m0, _m1 = m

    # -- H3 features --
    pleasant_trend = h3_features[_PLEASANT_TREND_H20]  # (B, T)
    rough_trend = h3_features[_ROUGH_TREND_H20]        # (B, T)
    loud_mean = h3_features[_LOUD_MEAN_H20]            # (B, T)
    loud_std = h3_features[_LOUD_STD_H24]              # (B, T)
    entropy_mean = h3_features[_ENTROPY_MEAN_H20]      # (B, T)
    entropy_stab = h3_features[_ENTROPY_STAB_H24]      # (B, T)
    stumpf_mean = h3_features[_STUMPF_MEAN_H20]        # (B, T)
    sflux_mean = h3_features[_SFLUX_MEAN_H20]          # (B, T)

    # -- Retrieval dynamics (trajectory from M-layer) --
    # Comfort trajectory: pleasantness rising + roughness falling
    comfort_trajectory = 0.50 * pleasant_trend + 0.50 * (1.0 - rough_trend)

    # -- F0: Analgesia Forecast --
    # Predicts analgesic state 2-5s ahead from comfort trajectory,
    # sustained engagement (loudness mean), and binding stability
    # (stumpf mean at 5s window).
    # Liang 2025: sustained VRMS FC effects support predictable trajectories
    # Putkinen 2025: ACC pain-pleasure appraisal trajectory
    f0 = _predict_future(
        trajectory=comfort_trajectory,
        context=loud_mean,
        stability=stumpf_mean,
    )

    # -- Encoding state trajectory --
    # Motor engagement trajectory from current state and pattern context
    encoding_trajectory = 0.50 * e0 + 0.50 * m0

    # -- F1: Engagement Forecast --
    # Predicts motor engagement 1-3s ahead from encoding trajectory,
    # pattern predictability (entropy mean), and event rate (flux mean).
    # Bushnell 2013: mPFC predictive pain modulation
    f1 = _predict_future(
        trajectory=encoding_trajectory,
        context=(1.0 - entropy_mean),
        stability=sflux_mean,
    )

    # -- F2: Reserved --
    # Placeholder for future therapeutic consolidation prediction.
    # Would use H24 (36s) features for long-term analgesic memory.
    f2 = torch.zeros_like(f0)

    return f0, f1, f2
