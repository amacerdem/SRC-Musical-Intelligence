"""RewardAggregator — ARU reward computation for C³ v1.0.

RFC §6: Inverted-U salience-gated reward.

reward_i = salience_i × (w1×surprise + w2×resolution + w3×exploration − w4×monotony)
  surprise   = |PE_i| × π_pred × (1 − familiarity)
  resolution = (1 − |PE_i|) × π_pred × familiarity
  exploration = entropy(prediction_distribution)  → simplified to PE variance
  monotony    = π_pred²

Final reward_valence = Σ reward_i × familiarity_mod
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

import torch
from torch import Tensor


@dataclass
class RewardConfig:
    """Weights for reward components.  All from YAML config."""
    w_surprise: float = 1.0
    w_resolution: float = 1.2
    w_exploration: float = 0.3
    w_monotony: float = 0.8


class RewardAggregator:
    """Computes reward_valence from typed PEs + precision + salience."""

    def __init__(self, config: RewardConfig | None = None) -> None:
        self.cfg = config or RewardConfig()

    def compute(
        self,
        pe_dict: Dict[str, Tensor],
        precision_pred_dict: Dict[str, Tensor],
        salience: Tensor,
        familiarity: Tensor,
    ) -> Tensor:
        """Compute aggregate reward valence.

        Args:
            pe_dict: {belief_name: PE tensor (B,T)} for predictive beliefs.
            precision_pred_dict: {belief_name: precision_pred scalar}.
            salience: (B, T) salience state.  Default 1.0 if ASU not active.
            familiarity: (B, T) familiarity state.  Default 0.5 if IMU not active.

        Returns:
            reward_valence: (B, T) in roughly [-1, 1] (unbounded in theory).
        """
        reward_total = torch.zeros_like(salience)

        for belief_name, pe in pe_dict.items():
            pi_raw = precision_pred_dict.get(belief_name, torch.tensor(1.0))
            # Normalize precision to [0, 1] — the reward formula assumes
            # pi_pred is a confidence probability, not a raw reliability index.
            # PrecisionEngine outputs in [0.01, 10.0].
            pi_pred = (pi_raw / 10.0).clamp(0.0, 1.0)

            pe_abs = pe.abs()

            # Surprise: unexpected event in unfamiliar context
            surprise = pe_abs * pi_pred * (1.0 - familiarity)

            # Resolution: expected event in familiar context (confirmation)
            resolution = (1.0 - pe_abs.clamp(max=1.0)) * pi_pred * familiarity

            # Exploration: high variance in predictions → epistemic bonus
            # Simplified: use PE magnitude as proxy for prediction uncertainty
            exploration = pe_abs * (1.0 - pi_pred)

            # Monotony: too predictable → boring
            monotony = pi_pred ** 2

            reward_i = salience * (
                self.cfg.w_surprise * surprise
                + self.cfg.w_resolution * resolution
                + self.cfg.w_exploration * exploration
                - self.cfg.w_monotony * monotony
            )

            reward_total = reward_total + reward_i

        # Familiarity modulation: moderate familiarity amplifies reward
        # Inverted-U: peak at ~0.5 familiarity
        familiarity_mod = 4.0 * familiarity * (1.0 - familiarity)  # peaks at 0.5
        reward_total = reward_total * (0.5 + 0.5 * familiarity_mod)

        return reward_total
