"""MEAMN M-Layer -- Temporal Integration (2D).

Two composite signals integrating E-layer with temporal context:

  M0: meam_retrieval    -- MEAM retrieval function [0, 1]
  M1: p_recall          -- P(recall given music) [0, 1]

H3 consumed:
    (4, 16, 0, 2)   sensory_pleasantness value H16 L2   -- current pleasantness
    (4, 20, 18, 0)  sensory_pleasantness trend H20 L0   -- pleasantness trajectory
    (10, 20, 1, 0)  loudness mean H20 L0                -- average arousal over 5s
    (22, 16, 0, 2)  entropy value H16 L2                -- current unpredictability
    (22, 20, 1, 0)  entropy mean H20 L0                 -- average complexity over 5s
    (7, 16, 8, 0)   amplitude velocity H16 L0           -- energy change rate

See Building/C3-Brain/F4-Memory-Systems/mechanisms/meamn/MEAMN-temporal-integration.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEAS_VAL_1S = (4, 16, 0, 2)
_PLEAS_TREND_5S = (4, 20, 18, 0)
_LOUD_MEAN_5S = (10, 20, 1, 0)
_ENTROPY_VAL_1S = (22, 16, 0, 2)
_ENTROPY_MEAN_5S = (22, 20, 1, 0)
_AMP_VEL_1S = (7, 16, 8, 0)


def compute_temporal_integration(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    e_outputs: Tuple[Tensor, Tensor, Tensor],
) -> Tuple[Tensor, Tensor]:
    """M-layer: 2D temporal integration from E-layer + H3.

    Mathematical formulation:
        MEAM_Retrieval = f(Familiarity * EmotionalIntensity * SelfRelevance)
        P(recall|music) = sigma(beta_0 + beta_1*Familiarity + beta_2*Arousal
                                + beta_3*Valence)

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(E0, E1, E2)`` each ``(B, T)``.

    Returns:
        ``(M0, M1)`` each ``(B, T)``.
    """
    e0, e1, e2 = e_outputs

    pleas_val_1s = h3_features[_PLEAS_VAL_1S]
    pleas_trend_5s = h3_features[_PLEAS_TREND_5S]
    loud_mean_5s = h3_features[_LOUD_MEAN_5S]
    entropy_val_1s = h3_features[_ENTROPY_VAL_1S]
    entropy_mean_5s = h3_features[_ENTROPY_MEAN_5S]
    amp_vel_1s = h3_features[_AMP_VEL_1S]

    # Derived signals from doc formulas
    # Familiarity = familiarity_proxy.mean() [from entropy, warmth]
    familiarity = torch.sigmoid(
        1.0 - 0.50 * entropy_val_1s - 0.50 * entropy_mean_5s
    )

    # EmotionalIntensity = |Valence| * Arousal [from R3 + affect dynamics]
    emotional_intensity = pleas_val_1s * torch.sigmoid(loud_mean_5s * amp_vel_1s)

    # SelfRelevance = retrieval_dynamics.mean() [hippocampal binding]
    self_relevance = e0  # E0 is the retrieval dynamics signal

    # M0: MEAM Retrieval -- triple-product model
    # Janata 2009: MEAMs require familiarity x emotion x self-relevance
    # retrieval * familiarity * emotional_intensity
    m0 = torch.sigmoid(
        1.0 * e0 * familiarity * emotional_intensity
    )

    # M1: P(recall | music) -- logistic regression
    # Derks-Dijkman 2024: 28/37 studies show musical mnemonic benefit
    # sigma(beta_0 + beta_1*Familiarity + beta_2*Arousal + beta_3*Valence)
    # Arousal = sigma(R3.loudness * R3.amplitude) -> use loud_mean_5s * amp_vel_1s
    # Valence = 1 - roughness -> use pleas_val_1s as proxy
    arousal = torch.sigmoid(loud_mean_5s * amp_vel_1s)
    m1 = torch.sigmoid(
        -0.50 + 0.40 * familiarity + 0.35 * arousal + 0.25 * pleas_val_1s
    )

    return m0, m1
