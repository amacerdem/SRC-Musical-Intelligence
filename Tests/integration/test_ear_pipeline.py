"""Integration tests for the MI ear pipeline (R3 -> H3).

Tests verify that the R3 spectral extractor and H3 temporal extractor
operate correctly together: shape consistency, value ranges, and demand
coverage.

Run with::

    pytest Tests/integration/test_ear_pipeline.py -v
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root on sys.path
# ---------------------------------------------------------------------------
_PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import pytest
import torch

from Musical_Intelligence.ear import R3Extractor, H3Extractor


# ======================================================================
# Fixtures
# ======================================================================

@pytest.fixture(scope="module")
def r3_extractor() -> R3Extractor:
    """Module-scoped R3Extractor (expensive init, reuse across tests)."""
    return R3Extractor()


@pytest.fixture(scope="module")
def h3_extractor() -> H3Extractor:
    """Module-scoped H3Extractor."""
    return H3Extractor()


@pytest.fixture(scope="module")
def synthetic_mel() -> torch.Tensor:
    """Synthetic mel spectrogram: (B=1, 128, T=200).

    Uses deterministic random values in [0, 1] to simulate a log-mel
    spectrogram input. T=200 is short enough for fast tests but long
    enough to exercise all R3 groups meaningfully.
    """
    gen = torch.Generator().manual_seed(42)
    return torch.rand(1, 128, 200, generator=gen)


@pytest.fixture(scope="module")
def r3_output(r3_extractor: R3Extractor, synthetic_mel: torch.Tensor):
    """Pre-computed R3 output for the module."""
    return r3_extractor.extract(synthetic_mel)


@pytest.fixture(scope="module")
def sample_demand() -> set:
    """A realistic but small demand set covering all 4 bands.

    Includes tuples from micro (H6), meso (H10), macro (H18), and
    ultra (H25) horizons with a mix of morphs and laws.
    """
    demand = set()
    # Micro band -- H6 (short note)
    for r3_idx in (0, 7, 14):
        for morph in (0, 1, 2, 8):
            for law in (0, 1, 2):
                demand.add((r3_idx, 6, morph, law))
    # Meso band -- H10 (moderate beat)
    for r3_idx in (3, 10, 21):
        for morph in (0, 1, 14, 18):
            for law in (0, 2):
                demand.add((r3_idx, 10, morph, law))
    # Macro band -- H18 (1 measure @ 120 BPM)
    for r3_idx in (0, 5):
        for morph in (0, 1, 2):
            for law in (0,):
                demand.add((r3_idx, 18, morph, law))
    # Ultra band -- H25 (short movement)
    for r3_idx in (0,):
        for morph in (0, 1):
            for law in (0, 2):
                demand.add((r3_idx, 25, morph, law))
    return demand


# ======================================================================
# Tests
# ======================================================================

class TestR3ToH3Pipeline:
    """End-to-end R3 -> H3 pipeline with real demand."""

    def test_r3_to_h3_pipeline(
        self,
        r3_output,
        h3_extractor: H3Extractor,
        sample_demand: set,
    ) -> None:
        """R3 extract -> H3 extract produces a valid sparse dictionary."""
        r3_tensor = r3_output.features  # (B, T, 97)

        h3_out = h3_extractor.extract(r3_tensor, sample_demand)

        # H3 output should be a non-empty dictionary
        assert h3_out.n_tuples > 0, "H3 should produce at least one tuple"
        assert isinstance(h3_out.features, dict), "H3 features must be a dict"

        # Every value should be a (B, T) tensor with values in [0, 1]
        B, T, _ = r3_tensor.shape
        for key, tensor in h3_out.features.items():
            assert tensor.shape == (B, T), (
                f"H3 feature {key} has shape {tensor.shape}, "
                f"expected ({B}, {T})"
            )
            assert tensor.min() >= 0.0, (
                f"H3 feature {key} has min={tensor.min().item():.4f} < 0"
            )
            assert tensor.max() <= 1.0, (
                f"H3 feature {key} has max={tensor.max().item():.4f} > 1"
            )


class TestH3DemandCoverage:
    """H3 returns all demanded tuples."""

    def test_h3_demand_coverage(
        self,
        r3_output,
        h3_extractor: H3Extractor,
        sample_demand: set,
    ) -> None:
        """Every demanded 4-tuple appears in the H3 output."""
        r3_tensor = r3_output.features
        h3_out = h3_extractor.extract(r3_tensor, sample_demand)

        returned_keys = set(h3_out.features.keys())
        missing = sample_demand - returned_keys
        extra = returned_keys - sample_demand

        assert not missing, (
            f"H3 output is missing {len(missing)} demanded tuples. "
            f"First 5: {sorted(missing)[:5]}"
        )
        assert not extra, (
            f"H3 output has {len(extra)} unexpected tuples. "
            f"First 5: {sorted(extra)[:5]}"
        )
        assert h3_out.n_tuples == len(sample_demand), (
            f"n_tuples={h3_out.n_tuples} != demand size={len(sample_demand)}"
        )


class TestR3H3ShapeConsistency:
    """R3 output T dimension matches H3 output T dimension."""

    def test_r3_h3_shape_consistency(
        self,
        r3_output,
        h3_extractor: H3Extractor,
        sample_demand: set,
    ) -> None:
        """R3 time dimension T propagates correctly through H3."""
        r3_tensor = r3_output.features  # (B, T, 97)
        B_r3, T_r3, D_r3 = r3_tensor.shape

        # R3 basic checks
        assert D_r3 == 97, f"R3 output dim should be 97, got {D_r3}"
        assert B_r3 == 1, f"Batch size should be 1, got {B_r3}"

        # H3 extraction
        h3_out = h3_extractor.extract(r3_tensor, sample_demand)

        # Every H3 tensor should share the same (B, T)
        for key, tensor in h3_out.features.items():
            assert tensor.shape[0] == B_r3, (
                f"H3 feature {key}: batch dim {tensor.shape[0]} != "
                f"R3 batch dim {B_r3}"
            )
            assert tensor.shape[1] == T_r3, (
                f"H3 feature {key}: time dim {tensor.shape[1]} != "
                f"R3 time dim {T_r3}"
            )

    def test_r3_output_range(self, r3_output) -> None:
        """R3 features should be in [0, 1]."""
        features = r3_output.features
        assert features.min() >= 0.0, (
            f"R3 min={features.min().item():.6f} < 0"
        )
        assert features.max() <= 1.0, (
            f"R3 max={features.max().item():.6f} > 1"
        )

    def test_r3_feature_names(self, r3_output) -> None:
        """R3 output should provide exactly 97 feature names."""
        names = r3_output.feature_names
        assert len(names) == 97, (
            f"Expected 97 feature names, got {len(names)}"
        )
        assert len(set(names)) == 97, "Feature names must be unique"
