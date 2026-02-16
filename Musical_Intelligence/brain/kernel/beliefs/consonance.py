"""PerceivedConsonance — SPU belief, Phase 0.

observe(): Weighted combination of R³ consonance group features.
  Uses roughness (inverse), sethares_dissonance (inverse), sensory_pleasantness,
  harmonic_deviation (inverse), stumpf_fusion.

predict(): H³-informed linear model.
  trend: h3[(roughness, H8, M18, L0)] — roughness trend at meso
  period: h3[(tonalness, H12, M14, L0)] — tonalness periodicity at phrase
  context: tempo_{t-1} × 0.1

precision_obs: spectral SNR × salience_proxy / (H³ std + ε)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ....ear.r3.registry.feature_map import R3FeatureMap


class PerceivedConsonance(Belief):
    """Perceived consonance — fast sensory belief (τ=0.3)."""

    name = "perceived_consonance"
    owner_unit = "SPU"
    tau = 0.3
    baseline = 0.5
    phase = 0

    # H³ demands for predict(): (feature_name, horizon, morph_placeholder, law)
    # Actual morph is resolved in predict() — M18 for trend, M14 for period
    h3_predict_demands = (
        ("roughness", 8, 18, 0),    # roughness trend at meso, L0
        ("tonalness", 12, 14, 0),   # tonalness periodicity at phrase, L0
    )

    w_trend = 0.15
    w_period = 0.10
    context_weights = {"tempo_state": 0.1}

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        # Pre-resolve feature indices for observe()
        self._idx_roughness = feature_map.resolve("roughness")
        self._idx_sethares = feature_map.resolve("sethares_dissonance")
        self._idx_pleasantness = feature_map.resolve("sensory_pleasantness")
        self._idx_harmdev = feature_map.resolve("harmonic_deviation")
        self._idx_stumpf = feature_map.resolve("stumpf_fusion")
        self._idx_tonalness = feature_map.resolve("tonalness")
        self._idx_amplitude = feature_map.resolve("amplitude")

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Extract consonance observation from R³ group A + C features.

        Consonance = weighted average of positive indicators minus negative.
        """
        roughness = r3[..., self._idx_roughness]
        sethares = r3[..., self._idx_sethares]
        pleasant = r3[..., self._idx_pleasantness]
        harmdev = r3[..., self._idx_harmdev]
        stumpf = r3[..., self._idx_stumpf]
        tonalness = r3[..., self._idx_tonalness]

        # Consonance = positive indicators - negative indicators
        # All features are in [0, 1] from R³ normalization
        value = (
            0.30 * pleasant
            + 0.25 * stumpf
            + 0.20 * tonalness
            + 0.15 * (1.0 - roughness)
            + 0.10 * (1.0 - sethares)
        ).clamp(0.0, 1.0)

        # Precision: based on signal energy and spectral clarity
        amplitude = r3[..., self._idx_amplitude]
        spectral_snr = tonalness * amplitude  # proxy for spectral SNR

        # H³ std at consonance horizon (if available)
        h3_std_key = (self._idx_roughness, 8, 2, 0)  # M2=std, H8, L0
        h3_std = h3.get(h3_std_key, torch.tensor(0.1))
        if h3_std.numel() == 1:
            h3_std = torch.full_like(value, 0.1)

        precision = spectral_snr / (h3_std + 1e-6)
        precision = precision.clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)
