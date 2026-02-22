"""abstract_future — Anticipation belief (HTP, F2).

"Upcoming high-level structure ~500ms ahead."

Observe: F0:abstract_future_500ms (1.0) — HTP high-level forecast.
No predict/update cycle. Feeds prediction_hierarchy.predict() as context.

See Building/C3-Brain/F2-Pattern-Recognition-and-Prediction/beliefs/htp/
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- HTP output index ---------------------------------------------------------
_F0_ABSTRACT_FUTURE = 10     # F0:abstract_future_500ms


class AbstractFuture(AnticipationBelief):
    """Anticipation belief: abstract structural prediction ~500ms ahead.

    Forward prediction for high-level musical structure (key, tonal center,
    harmonic function). Feeds prediction_hierarchy's predict() method
    and the precision engine.

    de Vries & Wurm 2023: abstract predictions precede stimulus by ~500ms.
    Bonetti et al. 2024: hippocampus/cingulate for sequence prediction.
    """

    NAME = "abstract_future"
    FULL_NAME = "Abstract Future"
    FUNCTION = "F2"
    MECHANISM = "HTP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:abstract_future_500ms", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe abstract future from HTP F0:abstract_future_500ms.

        Args:
            mechanism_output: ``(B, T, 12)`` HTP output tensor.

        Returns:
            ``(B, T)`` forward abstract structure prediction.
        """
        return mechanism_output[:, :, _F0_ABSTRACT_FUTURE]
