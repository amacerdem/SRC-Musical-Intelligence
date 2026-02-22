"""error_propagation — Appraisal belief (SPH, F2).

"Prediction error is propagating through the hierarchy."

Observe: 0.40*E1:alpha_beta_error + 0.30*P1:prediction_error
         + 0.30*M3:alpha_beta_power
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/sph/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SPH output indices (14D) -------------------------------------------------
_E1_ALPHA_BETA_ERROR = 1    # E1:alpha_beta_error
_M3_ALPHA_BETA_POWER = 7    # M3:alpha_beta_power
_P1_PREDICTION_ERROR = 9    # P1:prediction_error


class ErrorPropagation(AppraisalBelief):
    """Appraisal belief: prediction error propagation strength.

    Measures how strongly prediction error signals are propagating
    through the hierarchical network. High values indicate strong
    mismatch/varied response with alpha-beta oscillatory dominance;
    low values indicate matched/memorised state.

    Carbajal & Malmierca 2018: SSA and MMN are micro/macroscopic
    manifestations of the same deviance detection mechanism, propagating
    IC→MGB→AC.
    Fong et al. 2020: MMN prediction error propagates upward.
    """

    NAME = "error_propagation"
    FULL_NAME = "Error Propagation"
    FUNCTION = "F2"
    MECHANISM = "SPH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("E1:alpha_beta_error", 0.40),
        ("P1:prediction_error", 0.30),
        ("M3:alpha_beta_power", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe error propagation from SPH outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` SPH output tensor.

        Returns:
            ``(B, T)`` observed error propagation value.
        """
        return (
            0.40 * mechanism_output[:, :, _E1_ALPHA_BETA_ERROR]
            + 0.30 * mechanism_output[:, :, _P1_PREDICTION_ERROR]
            + 0.30 * mechanism_output[:, :, _M3_ALPHA_BETA_POWER]
        )
