"""reward_forecast — Anticipation belief (SRP, F6).

"Predicted upcoming reward value — forward reward trajectory."

Observe: F0:reward_forecast (1.0) — SRP forecast output.
No predict/update cycle.

See Building/C3-Brain/F6-Reward-and-Motivation/beliefs/reward-forecast.md
"""
from __future__ import annotations

from typing import Tuple

from torch import Tensor

from Musical_Intelligence.contracts.bases.belief import AnticipationBelief

# -- SRP output index -------------------------------------------------------
_F0_REWARD_FORECAST = 16


class RewardForecast(AnticipationBelief):
    """Anticipation belief: forward reward trajectory forecast."""

    NAME = "reward_forecast"
    FULL_NAME = "Reward Forecast"
    FUNCTION = "F6"
    MECHANISM = "SRP"

    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = (
        ("F0:reward_forecast", 1.0),
    )

    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe reward forecast from SRP F0:reward_forecast.

        Args:
            mechanism_output: ``(B, T, 19)`` SRP output tensor.

        Returns:
            ``(B, T)`` reward forecast value.
        """
        return mechanism_output[:, :, _F0_REWARD_FORECAST]
