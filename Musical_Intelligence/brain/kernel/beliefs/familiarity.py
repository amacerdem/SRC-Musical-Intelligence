"""FamiliarityState — IMU belief, Phase 2a.

observe(): Recurrence-aware familiarity from H³ periodicity + stability.
  H³ path:  M14 (periodicity/autocorrelation) as primary signal,
            M2 (std) as supporting stability evidence,
            energy gate from R³ tonal features to suppress silence.
  Fallback: R³-only weighted average with energy gate (early frames)

  High M14 periodicity → "this pattern recurs" → high familiarity
  Low energy (silence)  → gate ≈ 0 → familiarity ≈ 0

predict(): H³-informed linear model.
  trend: h3[(tonalness, H16, M18, L0)] — tonalness trend at macro
  context: perceived_consonance_{t-1} × 0.1

precision_obs: cross-feature periodicity agreement, energy-gated

RFC §6 interaction with reward:
  surprise   = |PE| × π_pred × (1 − familiarity)
  resolution = (1 − |PE|) × π_pred × familiarity
  fam_mod    = 4 × fam × (1 − fam)   — inverted-U, peak at 0.5
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from ..belief import Belief, Likelihood
from ....ear.r3.registry.feature_map import R3FeatureMap


class FamiliarityState(Belief):
    """Recurrence-aware familiarity — high inertia belief (τ=0.85).

    Measures pattern recurrence at macro scale via H³ periodicity (M14),
    with stability (M2) as supporting evidence and energy gating to
    suppress false familiarity during silence.
    Owned by IMU (Implicit Memory Unit).
    """

    name = "familiarity_state"
    owner_unit = "IMU"
    tau = 0.85
    baseline = 0.0
    phase = 2

    # H³ demands for predict(): tonalness trend at macro horizon
    # RFC specifies H24 (ultra), adapted to H16 (macro ~4s) for 30s excerpts
    h3_predict_demands = (
        ("tonalness", 16, 18, 0),  # tonalness trend at macro H16, L0
    )

    # H³ demands for observe(): recurrence + stability at macro horizon
    # M14 = periodicity/autocorrelation (primary recurrence signal)
    # M2 = std (supporting stability evidence)
    h3_observe_demands = (
        ("tonalness", 16, 2, 0),        # tonalness std at H16, L0
        ("key_clarity", 16, 2, 0),      # key clarity std at H16, L0
        ("tonal_stability", 16, 2, 0),  # tonal stability std at H16, L0
        ("tonalness", 16, 14, 0),       # tonalness periodicity at H16, L0
        ("key_clarity", 16, 14, 0),     # key clarity periodicity at H16, L0
        ("tonal_stability", 16, 14, 0), # tonal stability periodicity at H16, L0
    )

    w_trend = 0.10   # Low weight — familiarity is high inertia, slow drift
    w_period = 0.0   # Single predict demand (no periodicity term)
    context_weights = {"perceived_consonance": 0.1}

    def __init__(self, feature_map: R3FeatureMap) -> None:
        super().__init__(feature_map)
        self._idx_tonalness = feature_map.resolve("tonalness")
        self._idx_key_clarity = feature_map.resolve("key_clarity")
        self._idx_tonal_stability = feature_map.resolve("tonal_stability")

    def observe(
        self,
        r3: Tensor,
        h3: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Likelihood:
        """Measure recurrence-aware familiarity from H³ periodicity + stability.

        H³ path (normal):
            Primary: M14 periodicity (autocorrelation) — pattern recurrence.
            Supporting: M2 std (stability) — low variability.
            Gate: R³ tonal energy — suppresses familiarity during silence.

        R³ fallback (early frames / missing H³):
            Weighted average of tonal features, energy-gated.
        """
        B, T = r3.shape[0], r3.shape[1]
        device = r3.device

        # H³ stability measures: M2(std) at H16, L0
        tonalness_std = self._h3(h3, "tonalness", 16, 2, 0)
        key_std = self._h3(h3, "key_clarity", 16, 2, 0)
        tonal_stab_std = self._h3(h3, "tonal_stability", 16, 2, 0)

        # H³ periodicity measures: M14(autocorrelation) at H16, L0
        tonalness_period = self._h3(h3, "tonalness", 16, 14, 0)
        key_period = self._h3(h3, "key_clarity", 16, 14, 0)
        tonal_stab_period = self._h3(h3, "tonal_stability", 16, 14, 0)

        has_h3 = tonalness_std.dim() >= 2

        if has_h3:
            return self._observe_h3(
                r3, tonalness_std, key_std, tonal_stab_std,
                tonalness_period, key_period, tonal_stab_period,
            )
        return self._observe_r3_fallback(r3, B, T, device)

    def _observe_h3(
        self,
        r3: Tensor,
        tonalness_std: Tensor,
        key_std: Tensor,
        tonal_stab_std: Tensor,
        tonalness_period: Tensor,
        key_period: Tensor,
        tonal_stab_period: Tensor,
    ) -> Likelihood:
        """H³-enriched observation: recurrence + stability, energy-gated."""
        # === Energy gate: suppress familiarity during silence ===
        r3_tonalness = r3[..., self._idx_tonalness]
        r3_key = r3[..., self._idx_key_clarity]
        r3_tonal_stab = r3[..., self._idx_tonal_stability]
        energy = (r3_tonalness + r3_key + r3_tonal_stab) / 3.0
        gate = torch.sigmoid(10.0 * (energy - 0.1))

        # === Periodicity: M14 autocorrelation → recurrence signal ===
        # High M14 = pattern recurs at macro horizon = genuinely familiar
        period_signal = (
            (tonalness_period + key_period + tonal_stab_period) / 3.0
        ).clamp(0.0, 1.0)

        # === Stability: M2 std → inverted (supporting evidence) ===
        K = 5.0
        fam_stability = (
            1.0 / (1.0 + K * tonalness_std)
            + 1.0 / (1.0 + K * key_std)
            + 1.0 / (1.0 + K * tonal_stab_std)
        ) / 3.0

        # === R³ tonal level (minor) ===
        r3_level = 0.40 * r3_tonalness + 0.30 * r3_key + 0.30 * r3_tonal_stab

        # === Combine: recurrence (50%) + stability (35%) + R³ level (15%) ===
        raw_value = (
            0.50 * period_signal
            + 0.35 * fam_stability
            + 0.15 * r3_level
        )

        # Apply energy gate: silence → familiarity ≈ 0
        value = (raw_value * gate).clamp(0.0, 1.0)

        # Precision: cross-feature periodicity agreement, energy-gated
        period_stack = torch.stack([
            tonalness_period, key_period, tonal_stab_period,
        ], dim=-1)  # (B, T, 3)
        agreement = 1.0 / (period_stack.std(dim=-1) + 0.1)
        precision = (agreement * gate).clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)

    def _observe_r3_fallback(
        self,
        r3: Tensor,
        B: int,
        T: int,
        device: torch.device,
    ) -> Likelihood:
        """R³-only fallback (before H³ macro horizon fills), energy-gated."""
        r3_tonalness = r3[..., self._idx_tonalness]
        r3_key = r3[..., self._idx_key_clarity]
        r3_tonal_stab = r3[..., self._idx_tonal_stability]

        # Energy gate: suppress during silence
        energy = (r3_tonalness + r3_key + r3_tonal_stab) / 3.0
        gate = torch.sigmoid(10.0 * (energy - 0.1))

        raw = 0.40 * r3_tonalness + 0.30 * r3_key + 0.30 * r3_tonal_stab
        value = (raw * gate).clamp(0.0, 1.0)

        # Low precision, energy-gated
        precision = (torch.full((B, T), 0.5, device=device) * gate).clamp(
            0.01, 10.0,
        )

        return Likelihood(value=value, precision=precision)
