"""CMAT F-Layer -- Forecast (2D).

Forward predictions for cross-modal coherence and generalization:
  F0: coherence_pred     -- Predicted cross-modal coherence (1-2s) [0, 1]
  F1: generalization_pr  -- Predicted generalization to other modalities [0, 1]

Coherence prediction (F0) projects whether the current cross-modal
binding will remain coherent 1-2s ahead. Uses sustained affect (H16
pleasantness value) as trajectory signal, multi-sensory salience (P0)
as context, and congruence strength (T1) as stability anchor.
Palmer et al. 2013: stable emotional context supports music-color
correspondence.

Generalization prediction (F1) estimates how well current cross-modal
mappings would transfer to novel modality pairings. Uses entropy
stability (H16 L0) as the primary driver -- stable acoustic patterns
generalize better. Anchored by supramodal valence (S0) and arousal
(S1) strength.

H3 demands consumed (2 new):
  (4, 16, 0, 2)  sensory_pleasantness value H16 L2 -- sustained affect
  (22, 16, 19, 0) distribution_entropy stability H16 L0 -- pattern stability

See Building/C3-Brain/F5-Emotion-and-Valence/mechanisms/cmat/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuple keys consumed ---------------------------------------------------
_PLEAS_VAL_H16 = (4, 16, 0, 2)      # sensory_pleasantness value H16 L2
_ENTROPY_STAB_H16 = (22, 16, 19, 0)  # distribution_entropy stability H16 L0


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
        context: (B, T) contextual support (salience, valence, etc.).
        stability: (B, T) stability anchor (congruence, pattern consistency).

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
    e: Tuple[Tensor],
    m: Tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """Compute F-layer: coherence prediction and generalization prediction.

    F0 (coherence_pred): Projects cross-modal coherence 1-2s ahead
    from sustained affect trajectory (H16 pleasantness), multi-sensory
    salience (P0), and congruence strength (T1). When affect is stable
    and congruent, coherence is predicted to persist.
    Palmer et al. 2013: stable emotion supports music-color binding.

    F1 (generalization_pr): Projects generalization to novel modality
    pairings from entropy stability (H16), supramodal valence (S0),
    and supramodal arousal (S1). Stable patterns with strong
    supramodal representations generalize broadly.
    Spence 2011: systematic correspondences generalize across cultures.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e: ``(E0,)`` from extraction layer.
        m: ``(S0, S1, S2, T0, T1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1)`` each ``(B, T)``.
    """
    (e0,) = e
    s0, s1, _s2, _t0, t1 = m
    p0, _p1 = p

    # -- H3 features --
    pleas_val_1s = h3_features[_PLEAS_VAL_H16]            # (B, T)
    entropy_stab = h3_features[_ENTROPY_STAB_H16]          # (B, T)

    # -- F0: Coherence Prediction --
    # Projects cross-modal coherence 1-2s ahead.
    # Trajectory: sustained affect (H16 pleasantness value).
    # Context: multi-sensory salience (P0) -- salient events persist.
    # Stability: congruence strength (T1) -- congruent mappings cohere.
    # Palmer et al. 2013: stable emotional context supports correspondence
    f0 = _predict_future(
        trajectory=pleas_val_1s,
        context=p0,
        stability=t1,
    )

    # -- F1: Generalization Prediction --
    # Projects how well mappings transfer to new modality pairings.
    # Trajectory: entropy stability (stable patterns generalize better).
    # Context: supramodal valence (S0) -- strong valence generalizes.
    # Stability: supramodal arousal (S1) -- arousal consistency matters.
    # Spence 2011: correspondences generalize across cultures and ages
    f1 = _predict_future(
        trajectory=entropy_stab,
        context=s0,
        stability=s1,
    )

    return f0, f1
