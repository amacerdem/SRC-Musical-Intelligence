"""MAA F-Layer -- Forecast (3D).

Forward predictions for appreciation trajectory and aesthetic development:
  F0: appreciation_growth   -- Predicted appreciation trajectory (1-3s) [0, 1]
  F1: pattern_recognition   -- Pattern recognition growth prediction [0, 1]
  F2: aesthetic_development -- Aesthetic development trajectory [0, 1]

Appreciation growth (F0) projects the appreciation state forward using
mean dissonance and E-layer composite. If roughness is declining and
familiarity is rising, appreciation is predicted to grow. Gold 2019:
mere exposure shifts preference over 8 repetitions (d=0.42).

Pattern recognition (F1) projects pattern recognition trajectory from
mean consonance and complexity tolerance. As the listener discovers
patterns in atonal music, recognition increases. Mencke 2019: training
modulates sensitivity to stylistic uncertainty.

Aesthetic development (F2) projects long-term aesthetic trajectory from
distribution stability and P-layer evaluation. Stable patterns support
aesthetic consolidation. Cheung 2019: Goldilocks surface stabilises
with exposure.

H3 demands consumed (3):
  (0, 16, 1, 0)   roughness mean H16 L0              -- mean dissonance 1s
  (4, 16, 1, 0)   sensory_pleasantness mean H16 L0   -- mean consonance 1s
  (22, 16, 19, 0) distribution_entropy stability H16 L0 -- preference stability

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_ROUGH_MEAN_H16 = (0, 16, 1, 0)        # roughness mean H16 L0
_PLEASANT_MEAN_H16 = (4, 16, 1, 0)     # sensory_pleasantness mean H16 L0
_ENT_STAB_H16 = (22, 16, 19, 0)        # distribution_entropy stability H16 L0


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
    e: Tuple[Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: appreciation growth, pattern recognition, aesthetic development.

    F0 (appreciation_growth): Appreciation trajectory from inverse
    roughness trajectory (declining roughness = growing comfort) and
    appreciation composite (E3). Stability anchors the prediction.
    Gold 2019: mere exposure shifts preference (d=0.42, 8 reps).

    F1 (pattern_recognition): Pattern recognition from consonance
    trajectory and complexity tolerance (E0). As the listener finds
    structure, recognition grows. Mencke 2019: training modulates
    sensitivity to stylistic uncertainty.

    F2 (aesthetic_development): Long-term aesthetic trajectory from
    aesthetic evaluation (P2) and distribution stability. Stable
    patterns consolidate aesthetic judgements.
    Cheung 2019: Goldilocks surface stabilises with exposure.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0, E1, E2, E3)`` from extraction layer.
        p: ``(P0, P1, P2)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    e0, e1, _e2, e3 = e
    _p0, _p1, p2 = p

    # -- H3 features --
    rough_mean = h3_features[_ROUGH_MEAN_H16]              # (B, T)
    pleasant_mean = h3_features[_PLEASANT_MEAN_H16]        # (B, T)
    ent_stab = h3_features[_ENT_STAB_H16]                  # (B, T)

    # -- Appreciation trajectory --
    # Inverse roughness: declining roughness -> growing comfort -> appreciation
    comfort_trajectory = 0.50 * (1.0 - rough_mean) + 0.50 * e1

    # -- F0: Appreciation Growth --
    # Predicts appreciation state 1-3s ahead from comfort trajectory,
    # appreciation composite (E3), and distribution stability.
    # Gold 2019: mere exposure increases liking (d=0.42 after 8 reps)
    f0 = _predict_future(
        trajectory=comfort_trajectory,
        context=e3,
        stability=ent_stab,
    )

    # -- Pattern recognition trajectory --
    # Consonance trajectory + complexity tolerance: finding structure
    recognition_trajectory = 0.50 * pleasant_mean + 0.50 * e0

    # -- F1: Pattern Recognition --
    # Predicts pattern recognition growth from consonance trajectory,
    # familiarity index (E1), and distribution stability.
    # Mencke 2019: musicians show higher complexity tolerance
    f1 = _predict_future(
        trajectory=recognition_trajectory,
        context=e1,
        stability=ent_stab,
    )

    # -- Aesthetic development trajectory --
    # Aesthetic evaluation + appreciation composite: consolidation
    aesthetic_trajectory = 0.50 * p2 + 0.50 * e3

    # -- F2: Aesthetic Development --
    # Predicts long-term aesthetic trajectory from evaluation,
    # appreciation composite, and distribution stability.
    # Cheung 2019: Goldilocks surface stabilises with exposure
    f2 = _predict_future(
        trajectory=aesthetic_trajectory,
        context=pleasant_mean,
        stability=ent_stab,
    )

    return f0, f1, f2
