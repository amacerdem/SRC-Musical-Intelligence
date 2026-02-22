"""ESME F-Layer -- Forecast (3D).

Forward predictions for expertise-dependent processing:
  F0: feature_enhancement_pred   -- Predicted MMN enhancement level [0, 1]
  F1: expertise_transfer_pred    -- Cross-domain transfer prediction [0, 1]
  F2: developmental_trajectory   -- Long-term plasticity trajectory [0, 1]

F0 (feature_enhancement_pred): Predicts the expected enhancement level
for the next incoming feature based on the current expertise state
(M-layer mmn_expertise_function) and the present deviance pattern
(P-layer).
Mischler et al. 2025: deeper transformer layers more predictive of
neural responses in musicians.

F1 (expertise_transfer_pred): Predicts cross-domain transfer by
weighting all three domain-specific MMNs (pitch 0.3, rhythm 0.3,
timbre 0.4 -- slightly higher weight on timbre).
Criscuolo et al. 2022: musicians show general enhancement across
domains (bilateral STG + L IFG).
Martins et al. 2022 constraint: no clean dissociation at salience
level -- some transfer exists.

F2 (developmental_trajectory): Predicts the long-term plasticity
trajectory by combining expertise enhancement (f04, weight 0.6) with
the unified expertise function (weight 0.4). Captures structural and
functional changes accumulating with years of training.
Bucher et al. 2023: Heschl's Gyrus 130% larger in professional
musicians; OFC co-activation 25-40ms faster.
Bonetti et al. 2024: hierarchical auditory memory AC to hippocampus
to cingulate develops with expertise.

H3 demands consumed: 0 tuples (operates entirely on derived features).

Dependencies:
  E-layer f01, f02, f03 (domain-specific MMNs)
  E-layer f04 (expertise enhancement)
  M-layer mmn_expertise_function (unified metric)
  P-layer deviance signals (current detection state)

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/esme/
"""
from __future__ import annotations

from typing import Tuple

import torch
from torch import Tensor


def compute_forecast(
    h3_features,
    e_outputs: Tuple[Tensor, Tensor, Tensor, Tensor],
    m_outputs: Tuple[Tensor],
    p_outputs: Tuple[Tensor, Tensor, Tensor],
    ednr: Tensor,
    tscp: Tensor,
    cdmr: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """Compute F-layer: 3D forward predictions for expertise processing.

    F0 (feature_enhancement_pred): Predicts enhancement level for the
    next auditory event based on unified MMN-expertise function and
    present deviance levels. When deviance is detected in the trained
    domain, enhancement prediction increases.
    Mischler et al. 2025: hierarchical prediction enhancement.

    F1 (expertise_transfer_pred): Cross-domain transfer prediction.
    sigma(0.3 * f01 + 0.3 * f02 + 0.4 * f03). Slightly higher weight
    on timbre reflecting spectral richness of transfer.
    Criscuolo et al. 2022: general enhancement across domains.
    Martins et al. 2022: no clean dissociation.

    F2 (developmental_trajectory): Long-term plasticity trajectory.
    sigma(0.6 * f04 + 0.4 * mmn_expertise_function). Captures structural
    changes with training.
    Bucher et al. 2023: HG 130% larger in professional musicians.
    Bonetti et al. 2024: hierarchical auditory memory.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        e_outputs: ``(f01, f02, f03, f04)`` each ``(B, T)``
            from extraction layer.
        m_outputs: ``(mmn_expertise_function,)`` each ``(B, T)``
            from temporal integration layer.
        p_outputs: ``(P0, P1, P2)`` each ``(B, T)``
            from cognitive present layer.
        ednr: ``(B, T, 10)`` upstream EDNR output.
        tscp: ``(B, T, 10)`` upstream TSCP output.
        cdmr: ``(B, T, 11)`` upstream CDMR output.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    f01, f02, f03, f04 = e_outputs
    (mmn_expertise,) = m_outputs
    p0, p1, p2 = p_outputs

    # -- F0: Feature Enhancement Prediction ------------------------------------
    # sigma(0.40 * mmn_expertise_function + 0.30 * mean(P0, P1, P2)
    #       + 0.30 * f04)
    # Mischler et al. 2025: deeper layers more predictive in musicians
    deviance_mean = (p0 + p1 + p2) / 3.0
    f0 = torch.sigmoid(
        0.40 * mmn_expertise
        + 0.30 * deviance_mean
        + 0.30 * f04
    )

    # -- F1: Expertise Transfer Prediction -------------------------------------
    # sigma(0.3 * f01 + 0.3 * f02 + 0.4 * f03)
    # Criscuolo et al. 2022: bilateral STG + L IFG in musicians
    # Martins et al. 2022: no clean dissociation at salience level
    f1 = torch.sigmoid(
        0.30 * f01
        + 0.30 * f02
        + 0.40 * f03
    )

    # -- F2: Developmental Trajectory ------------------------------------------
    # sigma(0.6 * f04 + 0.4 * mmn_expertise_function)
    # Bucher et al. 2023: HG 130% larger in professional musicians
    # Bonetti et al. 2024: hierarchical auditory memory pathway
    f2 = torch.sigmoid(
        0.60 * f04
        + 0.40 * mmn_expertise
    )

    return f0, f1, f2
