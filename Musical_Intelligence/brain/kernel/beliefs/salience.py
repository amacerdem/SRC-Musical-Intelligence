"""SalienceState — ASU belief, Phase 1.

observe(): Bottom-up attention signal from 3 sources:
  1. energy × onset (R³) — loudness-driven perceptual salience
  2. |H³ velocity| (amplitude at H6, L0) — rapid change detection
  3. mean |PE_{t-1}| — previous surprise → current attention

  Weights: 0.40 / 0.35 / 0.25 (sum to 1.0, output in [0, 1]).
  Fallback: energy-only when H³ or PE unavailable (first frames).

predict(): H³-informed linear model.
  trend: h3[(amplitude, H6, M18, L0)] — amplitude trend at beat scale
  context: perceived_consonance_{t-1} × 0.1, tempo_state_{t-1} × 0.1

precision_obs: energy_contrast / (H³_std + ε)

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
    tau = 0.5
    baseline = 0.5
    phase = 1

    # H³ demands for observe(): velocity at beat scale
    h3_observe_demands = (
        ("amplitude", 6, 8, 0),   # M8=velocity, H6=beat, L0=memory
    )

    # H³ demands for predict(): trend at beat scale
    h3_predict_demands = (
        ("amplitude", 6, 18, 0),  # M18=trend, H6=beat, L0=memory
    )

    w_trend = 0.15
    w_period = 0.0    # No periodicity term for salience
    context_weights = {
        "perceived_consonance": 0.1,
        "tempo_state": 0.1,
    }

    # Signal mixing weights
    _W_ENERGY_ONSET = 0.40   # Bottom-up loudness × transient
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

        3 signals:
          1. energy × onset — loudness × transient detection
          2. H³ amplitude velocity — rapid change at beat scale
          3. mean |PE_{t-1}| — surprise carry-over from previous frame

        Signal weights adapt when components are unavailable.
        """
        B, T = r3.shape[0], r3.shape[1]
        device = r3.device

        # Signal 1: energy × onset (both [0,1] after R³ normalization)
        amplitude = r3[..., self._idx_amplitude]
        onset = r3[..., self._idx_onset]
        energy_onset = (amplitude * onset).clamp(0.0, 1.0)

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
                self._W_ENERGY_ONSET * energy_onset
                + self._W_H3_VELOCITY * vel_norm
                + self._W_PREV_PE * pe_norm
            )
        elif has_h3:
            vel_norm = h3_vel.abs().clamp(0.0, 1.0)
            value = 0.55 * energy_onset + 0.45 * vel_norm
        elif has_pe:
            pe_norm = prev_pe_mean.abs().clamp(0.0, 1.0)
            value = 0.60 * energy_onset + 0.40 * pe_norm
        else:
            # Pure bottom-up — first frames
            value = energy_onset

        value = value.clamp(0.0, 1.0)

        # Precision: energy contrast / (H³ std + ε)
        h3_std = self._h3(h3, "amplitude", 6, 2, 0)  # M2=std
        if h3_std.numel() > 1:
            precision = (energy_onset / (h3_std + 0.1)).clamp(0.01, 10.0)
        else:
            precision = torch.full((B, T), 1.0, device=device)

        return Likelihood(value=value, precision=precision)
