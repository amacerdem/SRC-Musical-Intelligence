"""TempoState — STU belief, Phase 0.

observe(): Weighted combination of R³ rhythm group features.
  Uses tempo_estimate, beat_strength, pulse_clarity, rhythmic_regularity.

predict(): H³-informed linear model.
  trend: h3[(onset_strength, H6, M18, L0)] — spectral_flux trend at beat
  period: h3[(onset_strength, H6, M14, L0)] — beat regularity
  context: perceived_consonance_{t-1} × 0.05

precision_obs: onset_regularity × salience_proxy / (H³ std + ε)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ....ear.r3.registry.feature_map import R3FeatureMap


class TempoState(Belief):
    """Tempo state — medium inertia belief (τ=0.7)."""

    name = "tempo_state"
    owner_unit = "STU"
    tau = 0.7
    baseline = 0.5
    phase = 0

    # H³ demands for predict()
    h3_predict_demands = (
        ("onset_strength", 6, 18, 0),  # onset trend at beat, L0
        ("onset_strength", 6, 14, 0),  # onset periodicity (beat regularity), L0
    )

    w_trend = 0.20
    w_period = 0.25
    context_weights = {"perceived_consonance": 0.05}

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        self._idx_tempo = feature_map.resolve("tempo_estimate")
        self._idx_beat = feature_map.resolve("beat_strength")
        self._idx_pulse = feature_map.resolve("pulse_clarity")
        self._idx_regularity = feature_map.resolve("rhythmic_regularity")
        self._idx_onset = feature_map.resolve("onset_strength")
        self._idx_amplitude = feature_map.resolve("amplitude")

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Extract tempo observation from R³ rhythm group features."""
        tempo = r3[..., self._idx_tempo]
        beat = r3[..., self._idx_beat]
        pulse = r3[..., self._idx_pulse]
        regularity = r3[..., self._idx_regularity]

        # Tempo state = weighted average of rhythmic indicators
        value = (
            0.35 * tempo
            + 0.25 * beat
            + 0.25 * pulse
            + 0.15 * regularity
        ).clamp(0.0, 1.0)

        # Precision: onset regularity × amplitude (clear onsets = reliable)
        onset = r3[..., self._idx_onset]
        amplitude = r3[..., self._idx_amplitude]
        onset_regularity = regularity * onset  # proxy

        h3_std_key = (self._idx_onset, 6, 2, 0)  # M2=std, H6, L0
        h3_std = h3.get(h3_std_key, torch.tensor(0.1))
        if h3_std.numel() == 1:
            h3_std = torch.full_like(value, 0.1)

        precision = onset_regularity * amplitude / (h3_std + 1e-6)
        precision = precision.clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)
