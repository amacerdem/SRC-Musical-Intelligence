"""SalienceState — ASU belief, Phase 1.

observe(): Bottom-up attention signal from 3 sources:
  1. energy + onset (R³, additive) — loudness + transient detection
  2. max(H³ velocity across amplitude/onset/flux) — multi-feature change
  3. mean |PE_{t-1}| — previous surprise → current attention

  Mixing: mean+max — 0.5×weighted_avg + 0.5×element_max.
  Prevents peak dilution: at a climax the dominant signal is preserved.
  Fallback: energy-only when H³ or PE unavailable (first frames).

predict(): H³-informed linear model (bottom-up only).
  trend: h3[(amplitude, H6, M18, L0)] — amplitude trend at beat scale
  No cross-belief context — salience prediction is purely bottom-up.

precision_obs: change-responsive — proportional to change magnitude.
  High change = high confidence = faster Bayesian response.

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
    """Attentional salience — fast reactive belief (τ=0.3).

    Gates reward computation: only salient events contribute to reward.
    Owned by ASU (Attentional Salience Unit).
    """

    name = "salience_state"
    owner_unit = "ASU"
    tau = 0.3       # Fast response — attention is reactive, not inertial
    baseline = 0.3  # Matched to typical observation level (energy signal)
    phase = 1

    # H³ demands for observe(): velocity at beat scale (multi-feature)
    h3_observe_demands = (
        ("amplitude", 6, 8, 0),        # M8=velocity, H6=beat, L0=memory
        ("onset_strength", 6, 8, 0),   # onset velocity, H6=beat, L0=memory
        ("spectral_flux", 6, 8, 0),    # spectral change velocity, H6, L0
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
    _W_H3_VELOCITY = 0.35   # Rapid temporal change (max across features)
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

        3 signals with mean+max mixing:
          1. energy — 0.6×amplitude + 0.4×onset (continuous, non-zero)
          2. H³ change — max velocity across amplitude/onset/flux
          3. mean |PE_{t-1}| — surprise carry-over from previous frame

        value = 0.5×weighted_avg + 0.5×element_max (peak preservation).
        Precision: proportional to change magnitude (not just amplitude).
        """
        B, T = r3.shape[0], r3.shape[1]
        device = r3.device

        # Signal 1: energy + onset (additive, not multiplicative)
        amplitude = r3[..., self._idx_amplitude]
        onset = r3[..., self._idx_onset]
        energy = (0.6 * amplitude + 0.4 * onset).clamp(0.0, 1.0)

        # Signal 2: multi-feature H³ velocity — max across change detectors
        vel_amp = self._h3(h3, "amplitude", 6, 8, 0)
        vel_onset = self._h3(h3, "onset_strength", 6, 8, 0)
        vel_flux = self._h3(h3, "spectral_flux", 6, 8, 0)
        has_h3 = vel_amp.dim() >= 2

        # Signal 3: PE_{t-1} carry-over
        has_pe = prev_pe_mean is not None and prev_pe_mean.dim() >= 2

        # Adaptive mixing based on signal availability
        if has_h3 and has_pe:
            h3_change = torch.maximum(
                torch.maximum(vel_amp.abs(), vel_onset.abs()),
                vel_flux.abs(),
            ).clamp(0.0, 1.0)
            pe_norm = prev_pe_mean.abs().clamp(0.0, 1.0)

            # Mean+max mixing: base preserves average, peak preserves spikes
            base = (
                self._W_ENERGY * energy
                + self._W_H3_VELOCITY * h3_change
                + self._W_PREV_PE * pe_norm
            )
            peak = torch.maximum(
                torch.maximum(energy, h3_change), pe_norm,
            )
            value = 0.5 * base + 0.5 * peak
        elif has_h3:
            h3_change = torch.maximum(
                torch.maximum(vel_amp.abs(), vel_onset.abs()),
                vel_flux.abs(),
            ).clamp(0.0, 1.0)
            base = 0.55 * energy + 0.45 * h3_change
            peak = torch.maximum(energy, h3_change)
            value = 0.5 * base + 0.5 * peak
        elif has_pe:
            pe_norm = prev_pe_mean.abs().clamp(0.0, 1.0)
            base = 0.60 * energy + 0.40 * pe_norm
            peak = torch.maximum(energy, pe_norm)
            value = 0.5 * base + 0.5 * peak
        else:
            # Pure bottom-up — first frames
            value = energy
            h3_change = energy  # Precision fallback

        value = value.clamp(0.0, 1.0)

        # Precision: change-responsive — high change = high confidence
        # Breaks the self-reinforcing loop: flat salience → low PE →
        # high precision_pred → low gain → salience stays flat.
        if has_h3:
            change_mag = (0.5 * energy + 0.5 * h3_change).clamp(0.01, 1.0)
            precision = (change_mag * 10.0).clamp(0.5, 10.0)
        else:
            precision = torch.full((B, T), 1.0, device=device)

        return Likelihood(value=value, precision=precision)
