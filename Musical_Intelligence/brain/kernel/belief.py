"""Belief base class and Likelihood dataclass.

Every C³ belief implements three methods:
  observe(r3, h3, feature_map) -> Likelihood
  predict(beliefs_prev, h3)    -> Tensor
  update(likelihood, predicted, precision_pred) -> Tensor

v2.0 adds multi-scale prediction:
  predict_multiscale(beliefs_prev, h3)  -> Dict[int, Tensor]  per-horizon
  observe_multiscale(h3)                -> Dict[int, Tensor]  per-horizon
  aggregate_prediction(ms_predictions)  -> Tensor              single value

Contract:
  - No hidden state beyond declared fields
  - No direct R³ index access (use feature_map.resolve())
  - All parameters from config (no hardcoded values)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Sequence, Tuple

import torch
from torch import Tensor

from .temporal_weights import (
    CONSONANCE_HORIZONS,
    aggregate_weights,
    scale_matched_weights,
)
from ...ear.r3.registry.feature_map import R3FeatureMap


# ======================================================================
# Likelihood — observation + sensory confidence
# ======================================================================

@dataclass(frozen=True)
class Likelihood:
    """Observation from a belief's observe() method.

    Attributes:
        value:     Scalar observation in [0, 1].  Shape: (B, T).
        precision: Sensory confidence.  Shape: (B, T).
                   High = reliable observation, low = noisy.
    """
    value: Tensor
    precision: Tensor


# ======================================================================
# BeliefState — runtime state of a single belief
# ======================================================================

@dataclass
class BeliefState:
    """Mutable runtime state for one belief variable.

    Stored in the kernel's belief store, updated each frame.
    """
    name: str
    value: Tensor          # (B, T) current posterior
    predicted: Tensor      # (B, T) last prediction
    pe: Tensor             # (B, T) prediction error = observed - predicted
    precision_obs: Tensor  # (B, T) sensory confidence
    precision_pred: Tensor # (B, T) prediction confidence
    gain: Tensor           # (B, T) Bayesian gain


# ======================================================================
# Belief — abstract base class
# ======================================================================

class Belief(ABC):
    """Abstract base for all C³ beliefs.

    Subclasses must implement observe() and predict().
    update() has a default Bayesian implementation.
    """

    # ── Identity (set by subclass) ──────────────────────────────────
    name: str = ""
    owner_unit: str = ""
    tau: float = 0.5
    baseline: float = 0.5
    phase: int = 0

    # ── H³ demand tuples for predict() ──────────────────────────────
    # Each entry: (feature_name, horizon, morph, law)
    h3_predict_demands: Tuple[Tuple[str, int, int, int], ...] = ()

    # ── H³ demand tuples for observe() ──────────────────────────────
    # Used by beliefs that need H³ data for observation (e.g. familiarity, salience)
    h3_observe_demands: Tuple[Tuple[str, int, int, int], ...] = ()

    # ── Context weights for cross-belief prediction ─────────────────
    context_weights: Dict[str, float] = {}

    # ── Predict weights (from YAML config) ──────────────────────────
    w_trend: float = 0.0
    w_period: float = 0.0

    # ── Multi-scale prediction (v2.0) ─────────────────────────────
    # Subclass sets these to enable multi-horizon prediction.
    # If multiscale_horizons is empty, the belief uses single-scale
    # predict() as before (full backward compat).
    multiscale_horizons: Tuple[int, ...] = ()
    multiscale_feature: str = ""       # R³ feature name for H³ lookup
    T_char: float = 0.0               # characteristic timescale (seconds)
    multiscale_alpha: float = 1.2      # exponential decay rate

    def __init__(self, feature_map: R3FeatureMap) -> None:
        self._fm = feature_map
        # Precompute aggregation weights if multi-scale is enabled
        if self.multiscale_horizons and self.T_char > 0:
            self._agg_weights = aggregate_weights(
                self.multiscale_horizons, self.T_char, self.multiscale_alpha,
            )
        else:
            self._agg_weights = {}

    # ── resolve() shortcut ──────────────────────────────────────────

    def _r3(self, r3_tensor: Tensor, name: str) -> Tensor:
        """Extract a single R³ feature by semantic name.

        Returns shape (B, T).
        """
        idx = self._fm.resolve(name)
        return r3_tensor[..., idx]

    def _r3_range(self, r3_tensor: Tensor, group: str) -> Tensor:
        """Extract a group of R³ features by group name.

        Returns shape (B, T, group_dim).
        """
        s = self._fm.resolve_range(group)
        return r3_tensor[..., s]

    # ── H³ access shortcut ──────────────────────────────────────────

    def _h3(
        self,
        h3_dict: Dict[Tuple[int, int, int, int], Tensor],
        feature_name: str,
        horizon: int,
        morph: int,
        law: int,
    ) -> Tensor:
        """Extract an H³ tuple by semantic R³ feature name.

        Resolves feature_name → r3_idx, then looks up (r3_idx, h, m, l).
        Returns shape (B, T).  Returns zeros if tuple not available.
        """
        r3_idx = self._fm.resolve(feature_name)
        key = (r3_idx, horizon, morph, law)
        if key in h3_dict:
            return h3_dict[key]
        # Tuple not computed — return zeros (safe fallback)
        # This can happen if H³ demand aggregation missed this tuple
        return torch.zeros(1)

    # ── Core methods ────────────────────────────────────────────────

    @abstractmethod
    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Extract current observation from sensory input.

        Must return a Likelihood with value and precision.
        Uses full H³ horizon range.
        """
        ...

    def predict(
        self,
        beliefs_prev: Dict[str, Tensor],
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """H³-informed linear forward model.

        Default implementation:
          predicted = τ * prev + (1-τ) * baseline
                    + w_trend * H³_M18(trend)
                    + w_period * H³_M14(periodicity)
                    + w_ctx * Σ(context_weights × beliefs_{t-1})

        Override for beliefs with non-standard prediction (e.g. reward).
        """
        prev = beliefs_prev.get(self.name)
        if prev is None:
            return torch.full((1,), self.baseline)

        # Inertia term
        predicted = self.tau * prev + (1.0 - self.tau) * self.baseline

        # H³ trend (M18 = morph index 18)
        if self.w_trend != 0.0 and self.h3_predict_demands:
            feat_name, h, _, law = self.h3_predict_demands[0]
            trend = self._h3(h3, feat_name, h, 18, law)  # M18 = trend
            if trend.dim() >= 2:
                predicted = predicted + self.w_trend * trend

        # H³ periodicity (M14 = morph index 14)
        if self.w_period != 0.0 and len(self.h3_predict_demands) > 1:
            feat_name, h, _, law = self.h3_predict_demands[1]
            period = self._h3(h3, feat_name, h, 14, law)  # M14 = periodicity
            if period.dim() >= 2:
                predicted = predicted + self.w_period * period

        # Cross-belief context
        for other_name, weight in self.context_weights.items():
            other_val = beliefs_prev.get(other_name)
            if other_val is not None and weight != 0.0:
                predicted = predicted + weight * other_val

        return predicted.clamp(0.0, 1.0)

    # ── Multi-scale prediction (v2.0) ─────────────────────────────

    def predict_multiscale(
        self,
        beliefs_prev: Dict[str, Tensor],
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Dict[int, Tensor]:
        """Multi-scale prediction — one per horizon.

        For each target horizon h, the prediction uses scale-matched
        exponential weighting: evidence from H³ at nearby horizons
        peaks when evidence horizon matches target horizon.

        Returns:
            ``{horizon_idx: predicted_value (B, T)}``.
            Empty dict if multi-scale is not enabled.
        """
        if not self.multiscale_horizons or not self.multiscale_feature:
            return {}

        prev = beliefs_prev.get(self.name)
        if prev is None:
            return {
                h: torch.full((1,), self.baseline)
                for h in self.multiscale_horizons
            }

        predictions: Dict[int, Tensor] = {}

        for h_target in self.multiscale_horizons:
            # Base: inertia + regression to baseline
            pred_h = self.tau * prev + (1.0 - self.tau) * self.baseline

            # Scale-matched trend evidence:
            # For target h, weight all evidence horizons with peak at h
            weights = scale_matched_weights(
                h_target, self.multiscale_horizons, self.multiscale_alpha,
            )

            trend_sum = torch.zeros_like(prev)
            has_trend = False
            for h_ev, w in weights.items():
                trend = self._h3(h3, self.multiscale_feature, h_ev, 18, 0)
                if trend.dim() >= 2:
                    trend_sum = trend_sum + w * trend
                    has_trend = True

            if has_trend:
                pred_h = pred_h + self.w_trend * trend_sum

            # Cross-belief context (same for all horizons)
            for other_name, weight in self.context_weights.items():
                other_val = beliefs_prev.get(other_name)
                if other_val is not None and weight != 0.0:
                    pred_h = pred_h + weight * other_val

            predictions[h_target] = pred_h.clamp(0.0, 1.0)

        return predictions

    def observe_multiscale(
        self,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Dict[int, Tensor]:
        """Multi-scale observation — H³ M0 (mean) per horizon.

        Each horizon provides a smoothed observation at its timescale:
        H³(feature, h, M0=mean, L0).

        Returns:
            ``{horizon_idx: observed_value (B, T)}``.
            Empty dict if multi-scale is not enabled.
        """
        if not self.multiscale_horizons or not self.multiscale_feature:
            return {}

        observations: Dict[int, Tensor] = {}
        for h in self.multiscale_horizons:
            obs = self._h3(h3, self.multiscale_feature, h, 0, 0)  # M0=mean, L0
            observations[h] = obs
        return observations

    def aggregate_prediction(
        self,
        ms_predictions: Dict[int, Tensor],
    ) -> Tensor:
        """Aggregate multi-scale predictions into single value.

        Uses T_char-based weighting: predictions at horizons close to
        the belief's characteristic timescale have highest weight.

        Returns:
            Single aggregated prediction tensor (B, T).
        """
        if not ms_predictions or not self._agg_weights:
            return torch.full((1,), self.baseline)

        result: Optional[Tensor] = None
        for h, pred in ms_predictions.items():
            w = self._agg_weights.get(h, 0.0)
            if w < 1e-12:
                continue
            if pred.dim() < 2:
                continue
            if result is None:
                result = w * pred
            else:
                result = result + w * pred

        if result is None:
            return torch.full((1,), self.baseline)
        return result.clamp(0.0, 1.0)

    def multiscale_h3_demands(self) -> Tuple[Tuple[str, int, int, int], ...]:
        """H³ demands for multi-scale prediction.

        Returns tuples for M0 (observe), M18 (predict/trend), M2 (precision)
        at each horizon in multiscale_horizons.
        """
        if not self.multiscale_horizons or not self.multiscale_feature:
            return ()

        demands = []
        feat = self.multiscale_feature
        for h in self.multiscale_horizons:
            demands.append((feat, h, 0, 0))   # M0 = mean (observation)
            demands.append((feat, h, 18, 0))  # M18 = trend (prediction)
            demands.append((feat, h, 2, 0))   # M2 = std (precision)
        return tuple(demands)

    def update(
        self,
        likelihood: Likelihood,
        predicted: Tensor,
        precision_pred: Tensor,
    ) -> Tensor:
        """Bayesian precision-weighted fusion.

        gain = π_obs / (π_obs + π_pred)
        posterior = (1 - gain) * predicted + gain * observed
        """
        eps = 1e-8
        gain = likelihood.precision / (likelihood.precision + precision_pred + eps)
        posterior = (1.0 - gain) * predicted + gain * likelihood.value
        return posterior.clamp(0.0, 1.0)
