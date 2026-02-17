"""RewardAggregator — ARU reward computation for C³ v1.0 / v2.5.

RFC §6: Inverted-U salience-gated reward.

v1.0 (single-scale):
  reward_i = salience × (w1×surprise + w2×resolution + w3×exploration − w4×monotony)

v2.0 (multi-scale):
  For beliefs with multi-horizon PEs, reward decomposes across horizons:
  reward = Σ_h w_h × g(PE_h, π_pred, salience, familiarity)
  This captures surprise/resolution at EACH temporal scale independently.

v2.1 (horizon-specific precision):
  Each horizon has its own precision_pred derived from its own PE history.
  reward = Σ_h w_h × g(PE_h, π_pred_h, salience, familiarity)
  Short horizons adapt fast (high π → surprise/resolution).
  Long horizons adapt slow (low π → exploration).

v2.3 (precision compression):
  π_eff = tanh(π_raw / scale) replaces linear π_raw / 10.
  Breaks monotony saturation: at scale=12, π_raw=10 → π_eff=0.68
  instead of 0.95.  Monotony drops from 0.90 to 0.37 (−59%).
  Operating range expands from [0.93, 1.0] to [0.55, 0.68].

v2.5 (surprise-dominant rebalancing):
  Weights shifted to make reward PE-responsive:
  w_surprise 1.0→1.5, w_resolution 1.2→0.8, w_exploration 0.3→0.5,
  w_monotony 0.8→0.6.  Reward formula slope A = d(reward)/d(|PE|)
  increases from 0.028 to 0.398 — climaxes now produce visibly higher
  reward than calm passages.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

import torch
from torch import Tensor


@dataclass
class RewardConfig:
    """Weights for reward components.  All from YAML config.

    v2.5: surprise-dominant rebalancing.
    Old: w_s=1.0, w_r=1.2, w_e=0.3, w_m=0.8 → slope A=0.028 (nearly flat).
    New: w_s=1.5, w_r=0.8, w_e=0.5, w_m=0.6 → slope A=0.398 (14× steeper).
    Climaxes now produce visibly higher reward than calm passages.
    """
    w_surprise: float = 1.5
    w_resolution: float = 0.8
    w_exploration: float = 0.5
    w_monotony: float = 0.6
    # v2.3: tanh compression scale for precision normalization.
    # π_eff = tanh(π_raw / precision_scale).
    # scale=12: π_raw=10 → 0.68, monotony=0.37.
    # scale=15: π_raw=10 → 0.58, monotony=0.27 (more aggressive).
    precision_scale: float = 12.0


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
            # v2.3: tanh compression — breaks monotony saturation.
            # PrecisionEngine outputs in [0.01, 10.0].
            # tanh(10/12) ≈ 0.68 vs linear 10/10 = 1.0.
            pi_pred = torch.tanh(pi_raw / self.cfg.precision_scale)

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

    def compute_multiscale(
        self,
        ms_pe_dict: Dict[str, Dict[int, Tensor]],
        ms_weights: Dict[str, Dict[int, float]],
        ms_precision_dict: Dict[str, Dict[int, Tensor]],
        precision_pred_dict: Dict[str, Tensor],
        salience: Tensor,
        familiarity: Tensor,
        *,
        single_pe_dict: Optional[Dict[str, Tensor]] = None,
        single_precision_dict: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Multi-scale reward: per-horizon PE + precision decomposition.

        v2.1: Each horizon uses its own precision_pred derived from its
        own PE history.  Short horizons adapt fast (high π_pred_h →
        surprise/resolution).  Long horizons adapt slow (low π_pred_h →
        exploration).

        Args:
            ms_pe_dict: ``{belief_name: {horizon: PE (B,T)}}``.
            ms_weights: ``{belief_name: {horizon: weight}}``.
                Normalized per-horizon weights for reward aggregation.
            ms_precision_dict: ``{belief_name: {horizon: precision_pred}}``.
                Per-horizon precision.  Falls back to single-belief
                precision from ``precision_pred_dict`` if not available.
            precision_pred_dict: ``{belief_name: precision_pred scalar}``.
                Single-scale precision (fallback + single-scale beliefs).
            salience: ``(B, T)`` salience state.
            familiarity: ``(B, T)`` familiarity state.
            single_pe_dict: PEs for beliefs still on single-scale path.
            single_precision_dict: Precision for single-scale beliefs.

        Returns:
            reward_valence: ``(B, T)``.
        """
        reward_total = torch.zeros_like(salience)

        # ── Multi-scale beliefs (v2.1: per-horizon precision) ────
        for belief_name, pe_by_horizon in ms_pe_dict.items():
            pi_h_dict = ms_precision_dict.get(belief_name, {})
            pi_fallback = precision_pred_dict.get(
                belief_name, torch.tensor(1.0),
            )
            weights = ms_weights.get(belief_name, {})

            for h, pe_h in pe_by_horizon.items():
                w_h = weights.get(h, 0.0)
                if w_h < 1e-12:
                    continue
                # Skip horizons that didn't produce real data
                if pe_h.dim() < 2:
                    continue

                # Per-horizon precision (v2.1 + v2.3 tanh compression)
                pi_raw = pi_h_dict.get(h, pi_fallback)
                pi_pred = torch.tanh(pi_raw / self.cfg.precision_scale)

                pe_abs = pe_h.abs()

                surprise = pe_abs * pi_pred * (1.0 - familiarity)
                resolution = (1.0 - pe_abs.clamp(max=1.0)) * pi_pred * familiarity
                exploration = pe_abs * (1.0 - pi_pred)
                monotony = pi_pred ** 2

                reward_h = salience * (
                    self.cfg.w_surprise * surprise
                    + self.cfg.w_resolution * resolution
                    + self.cfg.w_exploration * exploration
                    - self.cfg.w_monotony * monotony
                )

                reward_total = reward_total + w_h * reward_h

        # ── Single-scale beliefs (tempo, etc.) ────────────────────
        if single_pe_dict:
            single_prec = single_precision_dict or {}
            for belief_name, pe in single_pe_dict.items():
                pi_raw = single_prec.get(belief_name, torch.tensor(1.0))
                pi_pred = torch.tanh(pi_raw / self.cfg.precision_scale)

                pe_abs = pe.abs()
                surprise = pe_abs * pi_pred * (1.0 - familiarity)
                resolution = (1.0 - pe_abs.clamp(max=1.0)) * pi_pred * familiarity
                exploration = pe_abs * (1.0 - pi_pred)
                monotony = pi_pred ** 2

                reward_i = salience * (
                    self.cfg.w_surprise * surprise
                    + self.cfg.w_resolution * resolution
                    + self.cfg.w_exploration * exploration
                    - self.cfg.w_monotony * monotony
                )
                reward_total = reward_total + reward_i

        # Familiarity modulation (same as v1.0)
        familiarity_mod = 4.0 * familiarity * (1.0 - familiarity)
        reward_total = reward_total * (0.5 + 0.5 * familiarity_mod)

        return reward_total
