"""RewardValence — ARU belief, Phase 3.

reward_valence does NOT predict in the traditional sense.
It aggregates salience-gated PEs into a value signal.

observe(): Delegates to RewardAggregator.
predict(): Returns tau-smoothed previous value (no H³ model).
update(): Direct assignment (reward IS the posterior).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ....ear.r3.registry.feature_map import R3FeatureMap


class RewardValence(Belief):
    """Reward valence — slow terminal belief (τ=0.8)."""

    name = "reward_valence"
    owner_unit = "ARU"
    tau = 0.8
    baseline = 0.0  # reward is zero-centered
    phase = 3

    # No H³ demands — reward aggregates PEs, not sensory features
    h3_predict_demands = ()
    w_trend = 0.0
    w_period = 0.0
    context_weights = {}

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Reward has no direct sensory observation.

        Returns a zero-valued likelihood.  The actual reward is computed
        by RewardAggregator and set via set_reward().
        """
        # Placeholder — reward is set externally by the scheduler
        return Likelihood(
            value=torch.zeros(1),
            precision=torch.tensor(1.0),
        )

    def predict(
        self,
        beliefs_prev: Dict[str, Tensor],
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Reward prediction = smoothed previous reward."""
        prev = beliefs_prev.get(self.name)
        if prev is None:
            return torch.full((1,), self.baseline)
        return self.tau * prev + (1.0 - self.tau) * self.baseline

    def update(
        self,
        likelihood: Likelihood,
        predicted: Tensor,
        precision_pred: Tensor,
    ) -> Tensor:
        """For reward, the 'likelihood' value IS the reward from aggregator.

        Apply tau-smoothing between previous prediction and new reward.
        """
        # Reward update: blend prediction (smoothed previous) with new reward
        eps = 1e-8
        gain = likelihood.precision / (likelihood.precision + precision_pred + eps)
        posterior = (1.0 - gain) * predicted + gain * likelihood.value
        return posterior.clamp(-2.0, 2.0)
