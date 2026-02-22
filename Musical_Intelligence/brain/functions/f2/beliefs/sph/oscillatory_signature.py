"""oscillatory_signature — Appraisal belief (SPH, F2).

"The current oscillatory state reflects match vs mismatch processing."

Observe: 0.40*M2:gamma_power + 0.30*M3:alpha_beta_power
         + 0.30*E3:feedforward_feedback
No predict/update cycle.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/sph/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SPH output indices (14D) -------------------------------------------------
_E3_FEEDFORWARD_FEEDBACK = 3    # E3:feedforward_feedback
_M2_GAMMA_POWER = 6             # M2:gamma_power
_M3_ALPHA_BETA_POWER = 7        # M3:alpha_beta_power


class OscillatorySignature(AppraisalBelief):
    """Appraisal belief: oscillatory state characterisation.

    Captures the balance between gamma-dominant (match) and alpha-beta-
    dominant (mismatch) oscillatory states, combined with feedforward vs
    feedback information flow direction. This three-way signal provides
    a compact summary of the current processing mode.

    High gamma_power + high feedforward → strong match, bottom-up.
    High alpha_beta_power + low feedforward → strong error, top-down.

    Bonetti et al. 2024: gamma M>N, alpha-beta N>M; feedforward
    Heschl→Hippocampus→Cingulate, feedback in reverse.
    """

    NAME = "oscillatory_signature"
    FULL_NAME = "Oscillatory Signature"
    FUNCTION = "F2"
    MECHANISM = "SPH"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M2:gamma_power", 0.40),
        ("M3:alpha_beta_power", 0.30),
        ("E3:feedforward_feedback", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe oscillatory signature from SPH outputs.

        Args:
            mechanism_output: ``(B, T, 14)`` SPH output tensor.

        Returns:
            ``(B, T)`` observed oscillatory state value.
        """
        return (
            0.40 * mechanism_output[:, :, _M2_GAMMA_POWER]
            + 0.30 * mechanism_output[:, :, _M3_ALPHA_BETA_POWER]
            + 0.30 * mechanism_output[:, :, _E3_FEEDFORWARD_FEEDBACK]
        )
