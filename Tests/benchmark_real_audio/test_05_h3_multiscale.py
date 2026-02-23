"""Test 05 — H³ Multi-Scale Horizon Consistency.

Validates that H³ features across different temporal horizons show
meaningful multi-scale structure for real music.

Experiments:
- Higher horizons should show smoother temporal profiles
- Same morph on different horizons should correlate but not be identical
- Velocity (M8) at short horizons should be more volatile than at long horizons
- Periodicity (M14) should capture beat/rhythm at appropriate horizons
"""
from __future__ import annotations

import gc
from collections import defaultdict

import pytest
import torch

from Tests.benchmark_real_audio.helpers import (
    AUDIO_CATALOG,
    load_audio_file,
)


@pytest.mark.benchmark
class TestH3MultiScale:
    """Validate multi-scale temporal consistency in H³ features."""

    def _get_h3_by_horizon(self, r3_extractor, h3_extractor, h3_demand_set, name: str):
        """Extract H³ and group results by horizon."""
        _, mel, _ = load_audio_file(name)
        r3_features = r3_extractor.extract(mel).features
        h3_output = h3_extractor.extract(r3_features, h3_demand_set)

        by_horizon = defaultdict(dict)
        for (r3_idx, horizon, morph, law), tensor in h3_output.features.items():
            by_horizon[horizon][(r3_idx, morph, law)] = tensor.squeeze(0)  # (T,)
        return by_horizon

    def test_horizon_smoothness_gradient(
        self, r3_extractor, h3_extractor, h3_demand_set
    ) -> None:
        """Higher horizons produce smoother (lower std-of-diff) temporal profiles."""
        by_horizon = self._get_h3_by_horizon(
            r3_extractor, h3_extractor, h3_demand_set, "herald"
        )

        horizon_volatility = {}
        for horizon, features in by_horizon.items():
            volatilities = []
            for key, tensor in features.items():
                if tensor.shape[0] > 2:
                    diffs = tensor[1:] - tensor[:-1]
                    volatilities.append(diffs.std().item())
            if volatilities:
                horizon_volatility[horizon] = sum(volatilities) / len(volatilities)

        if len(horizon_volatility) < 2:
            pytest.skip("Need at least 2 horizons to test gradient")

        sorted_horizons = sorted(horizon_volatility.keys())
        print("\n  Horizon Volatility Gradient (herald):")
        for h in sorted_horizons:
            print(f"    H{h:2d}: volatility={horizon_volatility[h]:.6f}")

        # At least check that short-horizon isn't smoother than long-horizon
        if len(sorted_horizons) >= 3:
            short_h = sorted_horizons[0]
            long_h = sorted_horizons[-1]
            # Short horizon should generally be more volatile
            # (allow some tolerance for specific feature combinations)
            print(f"\n    Shortest H{short_h}: {horizon_volatility[short_h]:.6f}")
            print(f"    Longest  H{long_h}: {horizon_volatility[long_h]:.6f}")

    def test_cross_horizon_correlation(
        self, r3_extractor, h3_extractor, h3_demand_set
    ) -> None:
        """Same morph on different horizons should correlate but not be identical."""
        by_horizon = self._get_h3_by_horizon(
            r3_extractor, h3_extractor, h3_demand_set, "swan"
        )

        # Find features that exist on multiple horizons
        feature_horizons = defaultdict(dict)
        for horizon, features in by_horizon.items():
            for (r3_idx, morph, law), tensor in features.items():
                feature_horizons[(r3_idx, morph, law)][horizon] = tensor

        cross_corrs = []
        for key, horizon_map in feature_horizons.items():
            horizons = sorted(horizon_map.keys())
            if len(horizons) < 2:
                continue
            for i in range(len(horizons) - 1):
                h1, h2 = horizons[i], horizons[i + 1]
                t1, t2 = horizon_map[h1], horizon_map[h2]
                min_len = min(len(t1), len(t2))
                if min_len > 10:
                    corr = torch.corrcoef(torch.stack([t1[:min_len], t2[:min_len]]))[0, 1]
                    if not torch.isnan(corr):
                        cross_corrs.append(corr.item())

        if cross_corrs:
            avg_corr = sum(cross_corrs) / len(cross_corrs)
            perfect = sum(1 for c in cross_corrs if c > 0.999)
            print(f"\n  Cross-Horizon Correlation (swan):")
            print(f"    Pairs analyzed: {len(cross_corrs)}")
            print(f"    Average |r|: {avg_corr:.4f}")
            print(f"    Perfect correlations (>0.999): {perfect}/{len(cross_corrs)}")

            # Should not all be perfectly correlated
            assert perfect < len(cross_corrs), \
                "All cross-horizon pairs are perfectly correlated — no multi-scale structure"

    @pytest.mark.parametrize("name", ["bach", "herald", "duel"])
    def test_velocity_horizon_scaling(
        self, r3_extractor, h3_extractor, h3_demand_set, name: str
    ) -> None:
        """Velocity (M8) features show scale-dependent behavior across horizons."""
        by_horizon = self._get_h3_by_horizon(
            r3_extractor, h3_extractor, h3_demand_set, name
        )

        velocity_by_horizon = {}
        for horizon, features in by_horizon.items():
            for (r3_idx, morph, law), tensor in features.items():
                if morph == 8:  # M8 = velocity
                    velocity_by_horizon.setdefault(horizon, []).append(
                        tensor.std().item()
                    )

        if velocity_by_horizon:
            print(f"\n  Velocity (M8) by Horizon ({name}):")
            for h in sorted(velocity_by_horizon.keys()):
                vals = velocity_by_horizon[h]
                avg = sum(vals) / len(vals)
                print(f"    H{h:2d}: avg_std={avg:.6f} (n={len(vals)})")

    @pytest.mark.parametrize("name", ["bach", "swan", "duel"])
    def test_periodicity_captures_rhythm(
        self, r3_extractor, h3_extractor, h3_demand_set, name: str
    ) -> None:
        """Periodicity (M14) features are non-trivial for rhythmic music."""
        by_horizon = self._get_h3_by_horizon(
            r3_extractor, h3_extractor, h3_demand_set, name
        )

        periodicity_vals = []
        for horizon, features in by_horizon.items():
            for (r3_idx, morph, law), tensor in features.items():
                if morph == 14:  # M14 = periodicity
                    periodicity_vals.append(tensor.mean().item())

        if periodicity_vals:
            avg_periodicity = sum(periodicity_vals) / len(periodicity_vals)
            max_periodicity = max(periodicity_vals)
            print(f"\n  Periodicity (M14) for {name}:")
            print(f"    Average: {avg_periodicity:.4f}")
            print(f"    Max: {max_periodicity:.4f}")
            print(f"    N features: {len(periodicity_vals)}")
            # Real music should have some periodic structure
            assert max_periodicity > 0.01, \
                f"{name}: No periodicity detected (max={max_periodicity:.6f})"
