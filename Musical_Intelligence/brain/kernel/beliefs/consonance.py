"""PerceivedConsonance — SPU belief, Phase 0.

observe(): BCH-enriched or R³-direct consonance observation.
  BCH mode:  0.5×consonance_signal + 0.3×template_match + 0.2×hierarchy
  Fallback:  weighted average of R³ consonance group features.

predict(): H³-informed linear model (single-scale, backward compat).
  trend: h3[(roughness, H8, M18, L0)] — roughness trend at meso
  period: h3[(tonalness, H12, M14, L0)] — tonalness periodicity at phrase
  context: tempo_{t-1} × 0.1

predict_multiscale() [v2.0]: Scale-matched multi-horizon prediction.
  8 horizons (H5..H28) across micro/meso/macro/ultra bands.
  Each horizon predicts at its own timescale, weighted by
  w(h, Δ) = exp(-α|h - Δ|) — peak when evidence matches target.
  Single belief posterior via T_char-weighted aggregation.

precision_obs:
  BCH mode:  inverse of BCH output variability (cross-signal agreement)
  Fallback:  spectral SNR × salience_proxy / (H³ std + ε)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ..temporal_weights import CONSONANCE_HORIZONS
from ....ear.r3.registry.feature_map import R3FeatureMap

if TYPE_CHECKING:
    from ..relays.bch_wrapper import BCHOutput


class PerceivedConsonance(Belief):
    """Perceived consonance — fast sensory belief (τ=0.3).

    v2.0: Multi-scale prediction enabled.
    8 horizons across 4 bands, T_char=525ms (common beat level).
    """

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

    # ── Multi-scale (v2.0) ────────────────────────────────────────
    multiscale_horizons = CONSONANCE_HORIZONS   # H5,H7,H10,H13,H18,H21,H24,H28
    multiscale_feature = "roughness"
    T_char = 0.525      # 525 ms — common beat, phrase-level consonance
    multiscale_alpha = 0.3

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        # Pre-resolve feature indices for observe() fallback path
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
        *,
        bch_out: Optional[BCHOutput] = None,
    ) -> Likelihood:
        """Extract consonance observation from BCH relay or R³ features.

        BCH mode (Rule 3):
            value = 0.5×consonance_signal + 0.3×template_match + 0.2×hierarchy
            precision from BCH cross-signal agreement (Rule 4)

        Fallback (no BCH):
            Original R³ weighted average.
        """
        if bch_out is not None:
            return self._observe_bch(bch_out)
        return self._observe_r3(r3, h3)

    def _observe_bch(self, bch_out: BCHOutput) -> Likelihood:
        """BCH-enriched observation — Rule 3 weights."""
        value = (
            0.50 * bch_out.consonance_signal
            + 0.30 * bch_out.template_match
            + 0.20 * bch_out.hierarchy
        ).clamp(0.0, 1.0)

        # Rule 4: precision from BCH output variability
        # High agreement across 3 signals → high precision
        bch_stack = torch.stack([
            bch_out.hierarchy,
            bch_out.consonance_signal,
            bch_out.template_match,
        ], dim=-1)  # (B, T, 3)
        bch_variability = bch_stack.std(dim=-1)  # (B, T)
        precision = (1.0 / (bch_variability + 0.1)).clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)

    def _observe_r3(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Fallback: R³-only observation (pre-BCH behavior)."""
        roughness = r3[..., self._idx_roughness]
        sethares = r3[..., self._idx_sethares]
        pleasant = r3[..., self._idx_pleasantness]
        stumpf = r3[..., self._idx_stumpf]
        tonalness = r3[..., self._idx_tonalness]

        value = (
            0.30 * pleasant
            + 0.25 * stumpf
            + 0.20 * tonalness
            + 0.15 * (1.0 - roughness)
            + 0.10 * (1.0 - sethares)
        ).clamp(0.0, 1.0)

        # Precision: spectral SNR / H³ std
        amplitude = r3[..., self._idx_amplitude]
        spectral_snr = tonalness * amplitude

        h3_std_key = (self._idx_roughness, 8, 2, 0)  # M2=std, H8, L0
        h3_std = h3.get(h3_std_key, torch.tensor(0.1))
        if h3_std.numel() == 1:
            h3_std = torch.full_like(value, 0.1)

        precision = spectral_snr / (h3_std + 1e-6)
        precision = precision.clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)
