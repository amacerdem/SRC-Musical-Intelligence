"""plasticity_magnitude -- Appraisal belief (TSCP, F8).

"The degree of cortical plasticity currently active for timbre
processing."

Observe: 0.60*f03:plasticity_magnitude + 0.40*M0:enhancement_function
No predict/update cycle.

See Building/C3-Brain/F8-Learning-and-Plasticity/beliefs/plasticity-magnitude.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- TSCP output indices ---------------------------------------------------
_F03_PLASTICITY_MAGNITUDE = 2        # f03:plasticity_magnitude
_M0_ENHANCEMENT_FUNCTION = 3         # M0:enhancement_function


class PlasticityMagnitude(AppraisalBelief):
    """Appraisal belief: current cortical plasticity magnitude."""

    NAME = "plasticity_magnitude"
    FULL_NAME = "Plasticity Magnitude"
    FUNCTION = "F8"
    MECHANISM = "TSCP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("f03:plasticity_magnitude", 0.60),
        ("M0:enhancement_function", 0.40),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe plasticity magnitude from TSCP output.

        Args:
            mechanism_output: ``(B, T, 10)`` TSCP output tensor.

        Returns:
            ``(B, T)`` observed plasticity magnitude.
        """
        return (
            0.60 * mechanism_output[:, :, _F03_PLASTICITY_MAGNITUDE]
            + 0.40 * mechanism_output[:, :, _M0_ENHANCEMENT_FUNCTION]
        )
