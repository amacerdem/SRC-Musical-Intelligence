"""Belief base class and Likelihood dataclass.

Every C³ belief implements three methods:
  observe(r3, h3, feature_map) -> Likelihood
  predict(beliefs_prev, h3)    -> Tensor
  update(likelihood, predicted, precision_pred) -> Tensor

Contract:
  - No hidden state beyond declared fields
  - No direct R³ index access (use feature_map.resolve())
  - No dissolved group access (E: interactions, I: information)
  - All parameters from config (no hardcoded values)
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

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

    def __init__(self, feature_map: R3FeatureMap) -> None:
        self._fm = feature_map
        # Validate no dissolved features in our demands
        self._validate_no_dissolved()

    def _validate_no_dissolved(self) -> None:
        """Ensure this belief doesn't read dissolved R³ features."""
        for feat_name, _, _, _ in self.h3_predict_demands:
            if self._fm.is_dissolved(feat_name):
                raise ValueError(
                    f"Belief {self.name!r}: H³ demand references dissolved "
                    f"R³ feature {feat_name!r}"
                )

    # ── resolve() shortcut ──────────────────────────────────────────

    def _r3(self, r3_tensor: Tensor, name: str) -> Tensor:
        """Extract a single R³ feature by semantic name.

        Returns shape (B, T).
        """
        idx = self._fm.resolve(name)
        if self._fm.is_dissolved_index(idx):
            raise RuntimeError(
                f"Belief {self.name!r}: attempted to read dissolved "
                f"R³ feature {name!r} at index {idx}"
            )
        return r3_tensor[..., idx]

    def _r3_range(self, r3_tensor: Tensor, group: str) -> Tensor:
        """Extract a group of R³ features by group name.

        Returns shape (B, T, group_dim).
        """
        if group in self._fm.dissolved_groups:
            raise RuntimeError(
                f"Belief {self.name!r}: attempted to read dissolved "
                f"R³ group {group!r}"
            )
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
            if trend.numel() > 1:
                predicted = predicted + self.w_trend * trend

        # H³ periodicity (M14 = morph index 14)
        if self.w_period != 0.0 and len(self.h3_predict_demands) > 1:
            feat_name, h, _, law = self.h3_predict_demands[1]
            period = self._h3(h3, feat_name, h, 14, law)  # M14 = periodicity
            if period.numel() > 1:
                predicted = predicted + self.w_period * period

        # Cross-belief context
        for other_name, weight in self.context_weights.items():
            other_val = beliefs_prev.get(other_name)
            if other_val is not None and weight != 0.0:
                predicted = predicted + weight * other_val

        return predicted.clamp(0.0, 1.0)

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
