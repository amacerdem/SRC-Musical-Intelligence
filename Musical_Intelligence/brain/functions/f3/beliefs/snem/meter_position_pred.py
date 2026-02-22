"""meter_position_pred — Anticipation belief (SNEM, F3).

"Currently at position X in metric hierarchy (0=weak beat, 1=downbeat)."

Observe: 0.50*F1:meter_position_pred + 0.50*M2:beat_salience
No predict/update cycle. Feeds F4 Memory (episodic boundaries).
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SNEM output indices (12D) ------------------------------------------------
_M2_BEAT_SALIENCE = 5          # M2:beat_salience
_F1_METER_POSITION_PRED = 10   # F1:meter_position_pred


class MeterPositionPred(AnticipationBelief):
    """Anticipation belief: current metric position prediction.

    Forward prediction for position within metric hierarchy.
    High values indicate downbeat, low values indicate weak beat.

    Dependency: Requires SNEM mechanism (Relay, Depth 0).
    """

    NAME = "meter_position_pred"
    FULL_NAME = "Meter Position Prediction"
    FUNCTION = "F3"
    MECHANISM = "SNEM"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F1:meter_position_pred", 0.50),
        ("M2:beat_salience", 0.50),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe meter position prediction from SNEM.

        Args:
            mechanism_output: ``(B, T, 12)`` SNEM output tensor.

        Returns:
            ``(B, T)`` meter position prediction value.
        """
        return (
            0.50 * mechanism_output[:, :, _F1_METER_POSITION_PRED]
            + 0.50 * mechanism_output[:, :, _M2_BEAT_SALIENCE]
        )
