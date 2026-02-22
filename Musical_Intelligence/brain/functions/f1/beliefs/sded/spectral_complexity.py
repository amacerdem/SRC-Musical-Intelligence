"""spectral_complexity — Appraisal belief (SDED, F1).

"The spectral content is complex / has multiple dissonance sources."

Dependency chain:
    SDED (Depth 0, Relay) -> spectral_complexity
    Without SDED mechanism output, this belief cannot be computed.

Observe: 0.40*M0:detection_function + 0.30*P0:roughness_detection
         + 0.30*P1:deviation_detection
No predict/update cycle.

See Building/C3-Brain/F1-Sensory-Processing/beliefs/sded/spectral_complexity.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- SDED output indices (10D) ------------------------------------------------
_M0_DETECTION_FUNCTION = 3     # M0:detection_function
_P0_ROUGHNESS_DETECTION = 4    # P0:roughness_detection
_P1_DEVIATION_DETECTION = 5    # P1:deviation_detection


class SpectralComplexity(AppraisalBelief):
    """Appraisal belief: spectral complexity assessment.

    Measures how complex the current spectral dissonance pattern is.
    High values indicate multiple interacting dissonance sources
    (strong detection, clear roughness, significant context deviation).
    Low values indicate simple harmonic content with minimal roughness.

    Dependency: Requires SDED mechanism (Relay, Depth 0, no upstream).
    """

    NAME = "spectral_complexity"
    FULL_NAME = "Spectral Complexity"
    FUNCTION = "F1"
    MECHANISM = "SDED"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M0:detection_function", 0.40),
        ("P0:roughness_detection", 0.30),
        ("P1:deviation_detection", 0.30),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe spectral complexity from SDED outputs.

        Args:
            mechanism_output: ``(B, T, 10)`` SDED output tensor.

        Returns:
            ``(B, T)`` observed spectral complexity value.
        """
        return (
            0.40 * mechanism_output[:, :, _M0_DETECTION_FUNCTION]
            + 0.30 * mechanism_output[:, :, _P0_ROUGHNESS_DETECTION]
            + 0.30 * mechanism_output[:, :, _P1_DEVIATION_DETECTION]
        )
