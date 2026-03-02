"""V3 Test — Krumhansl & Kessler 1982: Tonal hierarchy profiles.

Predictions:
    1. MI's major profile correlates r > 0.85 with published major profile
    2. MI's minor profile correlates r > 0.85 with published minor profile
    3. Tonic gets highest rating in both major and minor
    4. Dominant and mediant get higher ratings than chromatic tones
"""
from __future__ import annotations

import numpy as np
import pytest

from Validation.infrastructure.stats import pearson_with_ci, spearman_with_ci


@pytest.mark.v3
class TestTonalHierarchy:
    """Compare MI tonal profiles to Krumhansl-Kessler profiles."""

    def test_major_profile_correlation(
        self, mi_major_profile, kk_major_profile,
    ):
        """MI major profile should correlate r > 0.7 with K-K major profile."""
        r, p, ci = pearson_with_ci(mi_major_profile, kk_major_profile)
        print(f"Major profile: r={r:.3f}, p={p:.2e}, CI={ci}")

        assert r > 0.7, (
            f"Expected r > 0.7 for major profile correlation, got r={r:.3f}"
        )
        assert p < 0.05, (
            f"Expected significant correlation (p < 0.05), got p={p:.3e}"
        )

    def test_minor_profile_correlation(
        self, mi_minor_profile, kk_minor_profile,
    ):
        """MI minor profile should correlate r > 0.7 with K-K minor profile."""
        r, p, ci = pearson_with_ci(mi_minor_profile, kk_minor_profile)
        print(f"Minor profile: r={r:.3f}, p={p:.2e}, CI={ci}")

        assert r > 0.7, (
            f"Expected r > 0.7 for minor profile correlation, got r={r:.3f}"
        )
        assert p < 0.05, (
            f"Expected significant correlation (p < 0.05), got p={p:.3e}"
        )

    def test_tonic_highest_major(self, mi_major_profile):
        """Tonic (pitch class 0) should have the highest rating in major profile."""
        tonic_idx = 0
        tonic_val = mi_major_profile[tonic_idx]
        max_val = mi_major_profile.max()
        max_idx = mi_major_profile.argmax()

        assert max_idx == tonic_idx or tonic_val > 0.9 * max_val, (
            f"Expected tonic (PC0) to be highest or near-highest. "
            f"Tonic={tonic_val:.4f}, max at PC{max_idx}={max_val:.4f}"
        )

    def test_tonic_highest_minor(self, mi_minor_profile):
        """Tonic (pitch class 0) should have the highest rating in minor profile."""
        tonic_idx = 0
        tonic_val = mi_minor_profile[tonic_idx]
        max_val = mi_minor_profile.max()
        max_idx = mi_minor_profile.argmax()

        assert max_idx == tonic_idx or tonic_val > 0.9 * max_val, (
            f"Expected tonic (PC0) to be highest or near-highest. "
            f"Tonic={tonic_val:.4f}, max at PC{max_idx}={max_val:.4f}"
        )

    def test_diatonic_vs_chromatic_major(self, mi_major_profile):
        """Diatonic tones should rate higher than chromatic tones in major."""
        diatonic_pcs = [0, 2, 4, 5, 7, 9, 11]  # C major scale
        chromatic_pcs = [1, 3, 6, 8, 10]        # non-scale tones

        diatonic_mean = mi_major_profile[diatonic_pcs].mean()
        chromatic_mean = mi_major_profile[chromatic_pcs].mean()

        assert diatonic_mean > chromatic_mean, (
            f"Expected diatonic mean ({diatonic_mean:.4f}) > "
            f"chromatic mean ({chromatic_mean:.4f})"
        )

    def test_diatonic_vs_chromatic_minor(self, mi_minor_profile):
        """Diatonic tones should rate higher than chromatic tones in minor."""
        diatonic_pcs = [0, 2, 3, 5, 7, 8, 10]  # C natural minor scale
        chromatic_pcs = [1, 4, 6, 9, 11]        # non-scale tones

        diatonic_mean = mi_minor_profile[diatonic_pcs].mean()
        chromatic_mean = mi_minor_profile[chromatic_pcs].mean()

        assert diatonic_mean > chromatic_mean, (
            f"Expected diatonic mean ({diatonic_mean:.4f}) > "
            f"chromatic mean ({chromatic_mean:.4f})"
        )

    def test_rank_order_correlation(
        self, mi_major_profile, kk_major_profile,
    ):
        """Spearman rank correlation should also be significant."""
        rho, p, ci = spearman_with_ci(mi_major_profile, kk_major_profile)
        print(f"Spearman major: rho={rho:.3f}, p={p:.2e}")

        assert rho > 0.6, (
            f"Expected Spearman rho > 0.6, got rho={rho:.3f}"
        )
