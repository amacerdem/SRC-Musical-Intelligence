"""FamiliarityState — IMU belief, Phase 2a.

observe(): Structural familiarity from H³ macro-scale stability.
  H³ path:  inverted std of tonalness, key_clarity, tonal_stability at H16 L0
  Fallback: R³-only weighted average (early frames / missing H³)

  High stability (low H³ M2) → high familiarity → "I've heard this pattern"
  Low stability (high H³ M2)  → low familiarity  → "this is new"

predict(): H³-informed linear model.
  trend: h3[(tonalness, H16, M18, L0)] — tonalness trend at macro
  context: perceived_consonance_{t-1} × 0.1

precision_obs: consistency of H³ stability measures (cross-feature agreement)

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
    """Structural familiarity — high inertia belief (τ=0.85).

    Measures how stable/repetitive the musical context is at macro scale.
    Owned by IMU (Implicit Memory Unit).
    """

    name = "familiarity_state"
    owner_unit = "IMU"
    tau = 0.85
    baseline = 0.5
    phase = 2

    # H³ demands for predict(): tonalness trend at macro horizon
    # RFC specifies H24 (ultra), adapted to H16 (macro ~4s) for 30s excerpts
    h3_predict_demands = (
        ("tonalness", 16, 18, 0),  # tonalness trend at macro H16, L0
    )

    # H³ demands for observe(): stability measurement at macro horizon
    # M2 = std morph.  Low std = stable = familiar.
    h3_observe_demands = (
        ("tonalness", 16, 2, 0),        # tonalness std at H16, L0
        ("key_clarity", 16, 2, 0),      # key clarity std at H16, L0
        ("tonal_stability", 16, 2, 0),  # tonal stability std at H16, L0
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
        """Measure structural familiarity from H³ macro stability.

        H³ path (normal):
            Familiarity = inverse of feature variability at macro horizon.
            Low H³ M2 (std) at H16 (~4s backward) = stable = familiar.

        R³ fallback (early frames / missing H³):
            Weighted average of tonal features as proxy.
        """
        B, T = r3.shape[0], r3.shape[1]
        device = r3.device

        # H³ stability measures: M2(std) at H16, L0
        tonalness_std = self._h3(h3, "tonalness", 16, 2, 0)
        key_std = self._h3(h3, "key_clarity", 16, 2, 0)
        tonal_stab_std = self._h3(h3, "tonal_stability", 16, 2, 0)

        has_h3 = tonalness_std.numel() > 1

        if has_h3:
            return self._observe_h3(
                r3, tonalness_std, key_std, tonal_stab_std
            )
        return self._observe_r3_fallback(r3, B, T, device)

    def _observe_h3(
        self,
        r3: Tensor,
        tonalness_std: Tensor,
        key_std: Tensor,
        tonal_stab_std: Tensor,
    ) -> Likelihood:
        """H³-enriched observation: stability-based familiarity."""
        # Invert std → familiarity: low variability = high familiarity
        # Soft inversion: f = 1 / (1 + K × std)
        K = 5.0
        fam_tonalness = 1.0 / (1.0 + K * tonalness_std)
        fam_key = 1.0 / (1.0 + K * key_std)
        fam_tonal = 1.0 / (1.0 + K * tonal_stab_std)

        # R³ level features: high = recognizable patterns
        r3_tonalness = r3[..., self._idx_tonalness]
        r3_key = r3[..., self._idx_key_clarity]
        r3_tonal_stab = r3[..., self._idx_tonal_stability]

        # Weighted combination: 65% H³ stability + 35% R³ level
        value = (
            0.25 * fam_tonalness
            + 0.20 * fam_key
            + 0.20 * fam_tonal
            + 0.15 * r3_tonalness
            + 0.10 * r3_key
            + 0.10 * r3_tonal_stab
        ).clamp(0.0, 1.0)

        # Precision: cross-feature stability agreement
        # High agreement among 3 stability measures → high confidence
        stab_stack = torch.stack([
            fam_tonalness, fam_key, fam_tonal,
        ], dim=-1)  # (B, T, 3)
        agreement = 1.0 / (stab_stack.std(dim=-1) + 0.1)
        precision = agreement.clamp(0.01, 10.0)

        return Likelihood(value=value, precision=precision)

    def _observe_r3_fallback(
        self,
        r3: Tensor,
        B: int,
        T: int,
        device: torch.device,
    ) -> Likelihood:
        """R³-only fallback (before H³ macro horizon fills)."""
        r3_tonalness = r3[..., self._idx_tonalness]
        r3_key = r3[..., self._idx_key_clarity]
        r3_tonal_stab = r3[..., self._idx_tonal_stability]

        value = (
            0.40 * r3_tonalness
            + 0.30 * r3_key
            + 0.30 * r3_tonal_stab
        ).clamp(0.0, 1.0)

        # Low precision — R³-only is a weak proxy for temporal stability
        precision = torch.full((B, T), 0.5, device=device)

        return Likelihood(value=value, precision=precision)
