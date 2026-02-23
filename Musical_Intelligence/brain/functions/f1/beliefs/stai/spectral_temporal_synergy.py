"""spectral_temporal_synergy — Appraisal belief (STAI, F1).

"The spectral and temporal dimensions of this sound are interacting
cohesively, producing an integrated percept."

Observe: 0.50*M1:spectral_temporal_interaction
         + 0.30*E2:aesthetic_integration + 0.20*P0:spectral_quality
No predict/update cycle.

See Building/C3-Brain/F1-Sensory-Processing/beliefs/spectral-temporal-synergy.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AppraisalBelief

# -- STAI output indices ---------------------------------------------------
_E2_AESTHETIC_INTEGRATION = 2     # E2:aesthetic_integration
_M1_SPEC_TEMP_INTERACTION = 5     # M1:spectral_temporal_interaction
_P0_SPECTRAL_QUALITY = 6          # P0:spectral_quality


class SpectralTemporalSynergy(AppraisalBelief):
    """Appraisal belief: spectral-temporal binding strength."""

    NAME = "spectral_temporal_synergy"
    FULL_NAME = "Spectral Temporal Synergy"
    FUNCTION = "F1"
    MECHANISM = "STAI"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("M1:spectral_temporal_interaction", 0.50),
        ("E2:aesthetic_integration", 0.30),
        ("P0:spectral_quality", 0.20),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe spectral-temporal synergy from STAI output.

        Args:
            mechanism_output: ``(B, T, 12)`` STAI output tensor.

        Returns:
            ``(B, T)`` spectral-temporal synergy value.
        """
        return (
            0.50 * mechanism_output[:, :, _M1_SPEC_TEMP_INTERACTION]
            + 0.30 * mechanism_output[:, :, _E2_AESTHETIC_INTEGRATION]
            + 0.20 * mechanism_output[:, :, _P0_SPECTRAL_QUALITY]
        )
