"""SalienceState — ASU belief, Phase 1.

observe(): Bottom-up attention signal from 3 sources:
  1. energy + onset (R³, additive) — loudness + transient detection
  2. |H³ velocity| (amplitude at H6, L0) — rapid change detection
  3. mean |PE_{t-1}| — previous surprise → current attention

  Weights: 0.40 / 0.35 / 0.25 (sum to 1.0, output in [0, 1]).
  Fallback: energy-only when H³ or PE unavailable (first frames).

  Note: energy and onset are additive (not multiplicative) to ensure
  continuous signal during sustained passages. Multiplicative product
  creates a degenerate zero-observation for most frames.

predict(): H³-informed linear model (bottom-up only).
  trend: h3[(amplitude, H6, M18, L0)] — amplitude trend at beat scale
  No cross-belief context — salience prediction is purely bottom-up.

precision_obs: amplitude / (H³_std + ε).  Decoupled from onset to
  maintain meaningful precision during sustained passages.

RFC §5: Phase 1 — attentional gate before belief prediction.
Salience gates reward (not beliefs): reward_i = salience × (surprise + ...)
"""
from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ....ear.r3.registry.feature_map import R3FeatureMap


class SalienceState(Belief):
    """Attentional salience — medium inertia belief (τ=0.5).

    Gates reward computation: only salient events contribute to reward.
    Owned by ASU (Attentional Salience Unit).
    """

    name = "salience_state"
    owner_unit = "ASU"
    tau = 0.3       # Fast response — attention is reactive, not inertial
    baseline = 0.3  # Matched to typical observation level (energy signal)
    phase = 1

    # H³ demands for observe(): velocity at beat scale
    h3_observe_demands = (
        ("amplitude", 6, 8, 0),   # M8=velocity, H6=beat, L0=memory
    )

    # H³ demands for predict(): trend at beat scale
    h3_predict_demands = (
        ("amplitude", 6, 18, 0),  # M18=trend, H6=beat, L0=memory
    )

    w_trend = 0.20   # Slightly higher — salience should follow energy trends
    w_period = 0.0   # No periodicity term for salience
    context_weights = {}  # No cross-belief inflation — salience is bottom-up

    # Signal mixing weights (additive, sum to 1.0)
    _W_ENERGY = 0.40         # Bottom-up loudness + transient
    _W_H3_VELOCITY = 0.35   # Rapid temporal change
    _W_PREV_PE = 0.25       # Surprise carry-over

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        self._idx_amplitude = feature_map.resolve("amplitude")
        self._idx_onset = feature_map.resolve("onset_strength")

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
        *,
        prev_pe_mean: Optional[Tensor] = None,
    ) -> Likelihood:
        """Extract salience from bottom-up attention signals.

        3 signals (additive):
          1. energy — 0.6×amplitude + 0.4×onset (continuous, non-zero)
          2. H³ amplitude velocity — rapid change at beat scale
          3. mean |PE_{t-1}| — surprise carry-over from previous frame

        Signal weights adapt when components are unavailable.
        Precision decoupled from observation: amplitude / (H³_std + ε).
        """
        B, T = r3.shape[0], r3.shape[1]
        device = r3.device

        # Signal 1: energy + onset (additive, not multiplicative)
        # amplitude provides continuous loudness signal
        # onset provides transient boost at note attacks
        amplitude = r3[..., self._idx_amplitude]
        onset = r3[..., self._idx_onset]
        energy = (0.6 * amplitude + 0.4 * onset).clamp(0.0, 1.0)

        # Signal 2: H³ velocity (amplitude rapid change at beat horizon)
        h3_vel = self._h3(h3, "amplitude", 6, 8, 0)  # M8=velocity
        has_h3 = h3_vel.numel() > 1

        # Signal 3: PE_{t-1} carry-over
        has_pe = prev_pe_mean is not None and prev_pe_mean.numel() > 1

        # Adaptive mixing based on signal availability
        if has_h3 and has_pe:
            vel_norm = h3_vel.abs().clamp(0.0, 1.0)
            pe_norm = prev_pe_mean.abs().clamp(0.0, 1.0)
            value = (
                self._W_ENERGY * energy
                + self._W_H3_VELOCITY * vel_norm
                + self._W_PREV_PE * pe_norm
            )
        elif has_h3:
            vel_norm = h3_vel.abs().clamp(0.0, 1.0)
            value = 0.55 * energy + 0.45 * vel_norm
        elif has_pe:
            pe_norm = prev_pe_mean.abs().clamp(0.0, 1.0)
            value = 0.60 * energy + 0.40 * pe_norm
        else:
            # Pure bottom-up — first frames
            value = energy

        value = value.clamp(0.0, 1.0)

        # Precision: amplitude / (H³ std + ε)
        # Decoupled from onset — amplitude is continuous and reliable
        h3_std = self._h3(h3, "amplitude", 6, 2, 0)  # M2=std
        if h3_std.numel() > 1:
            precision = (amplitude / (h3_std + 0.1)).clamp(0.01, 10.0)
        else:
            precision = torch.full((B, T), 1.0, device=device)

        return Likelihood(value=value, precision=precision)
