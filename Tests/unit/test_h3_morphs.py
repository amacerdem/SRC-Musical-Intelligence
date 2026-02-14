"""Unit tests for all 24 H3 temporal morph functions.

Tests individual morphs (via MorphComputer), batch morphs (via batch_morph /
BATCH_DISPATCH), and normalization (via normalize_morph).  Verifies shape
consistency between individual and batch paths, dispatch completeness, and
signed-morph centering behaviour.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch

from Musical_Intelligence.ear.h3.morphology.computer import MorphComputer
from Musical_Intelligence.ear.h3.morphology.batch import batch_morph, BATCH_DISPATCH
from Musical_Intelligence.ear.h3.morphology.scaling import normalize_morph
from Musical_Intelligence.ear.h3.constants.morphs import SIGNED_MORPHS, N_MORPHS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def computer() -> MorphComputer:
    """Single MorphComputer instance for the module."""
    return MorphComputer()


@pytest.fixture(scope="module")
def window_data():
    """Synthetic window data for morph tests.

    Returns (window_2d, weights_1d, window_3d, weights_1d) where:
    - window_2d: (B=4, W=32) for individual morphs
    - window_3d: (B=4, F=10, W=32) for batch morphs
    - weights:   (W=32,) normalized attention weights
    """
    torch.manual_seed(123)
    B, F, W = 4, 10, 32
    window_2d = torch.rand(B, W)
    window_3d = torch.rand(B, F, W)
    # Exponential decay weights (mimicking AttentionKernel)
    positions = torch.linspace(0.0, 1.0, W)
    weights = torch.exp(-3.0 * (1.0 - positions))
    weights = weights / weights.sum()
    return window_2d, window_3d, weights


# ---------------------------------------------------------------------------
# Dispatch completeness
# ---------------------------------------------------------------------------

class TestBatchDispatchCompleteness:
    """Verify BATCH_DISPATCH covers all 24 morphs."""

    def test_batch_dispatch_completeness(self):
        """BATCH_DISPATCH must have exactly 24 entries (0-23)."""
        assert len(BATCH_DISPATCH) == N_MORPHS, (
            f"Expected {N_MORPHS} entries in BATCH_DISPATCH, "
            f"got {len(BATCH_DISPATCH)}"
        )
        for i in range(N_MORPHS):
            assert i in BATCH_DISPATCH, (
                f"Morph index {i} missing from BATCH_DISPATCH"
            )

    def test_computer_dispatch_completeness(self, computer):
        """MorphComputer must dispatch all 24 morph indices."""
        for i in range(N_MORPHS):
            assert i in computer._dispatch, (
                f"Morph index {i} missing from MorphComputer._dispatch"
            )


# ---------------------------------------------------------------------------
# Per-morph shape tests (parametrized over all 24 morphs)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("morph_idx", list(range(N_MORPHS)))
class TestMorphOutputShape:
    """Verify output shapes for each morph function."""

    def test_individual_morph_shape(self, computer, window_data, morph_idx):
        """Individual morph (B, W) -> (B,)."""
        window_2d, _, weights = window_data
        result = computer.compute(window_2d, weights, morph_idx)
        assert result.shape == (window_2d.shape[0],), (
            f"Morph {morph_idx}: expected ({window_2d.shape[0]},), "
            f"got {result.shape}"
        )

    def test_batch_morph_shape(self, window_data, morph_idx):
        """Batch morph (B, F, W) -> (B, F)."""
        _, window_3d, weights = window_data
        B, F, W = window_3d.shape
        result = batch_morph(window_3d, weights, morph_idx)
        assert result.shape == (B, F), (
            f"Morph {morph_idx}: expected ({B}, {F}), got {result.shape}"
        )


# ---------------------------------------------------------------------------
# Individual vs batch consistency
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("morph_idx", list(range(N_MORPHS)))
class TestMorphConsistency:
    """Verify that individual and batch morphs produce consistent results."""

    def test_individual_batch_consistency(self, computer, window_data, morph_idx):
        """For a single frame, individual and batch morphs should agree."""
        window_2d, _, weights = window_data
        B, W = window_2d.shape

        # Individual: (B, W) -> (B,)
        individual_result = computer.compute(window_2d, weights, morph_idx)

        # Batch with F=1: (B, 1, W) -> (B, 1)
        window_3d_single = window_2d.unsqueeze(1)  # (B, 1, W)
        batch_result = batch_morph(window_3d_single, weights, morph_idx)

        assert torch.allclose(
            individual_result, batch_result.squeeze(1), atol=1e-5
        ), (
            f"Morph {morph_idx}: individual and batch results differ "
            f"(max diff: {(individual_result - batch_result.squeeze(1)).abs().max():.6f})"
        )


# ---------------------------------------------------------------------------
# Normalization tests
# ---------------------------------------------------------------------------

class TestNormalization:
    """Verify normalize_morph produces values in [0, 1]."""

    @pytest.mark.parametrize("morph_idx", list(range(N_MORPHS)))
    def test_normalize_morph_range(self, window_data, morph_idx):
        """Normalized morph output must be in [0, 1]."""
        _, window_3d, weights = window_data
        raw = batch_morph(window_3d, weights, morph_idx)
        normed = normalize_morph(raw, morph_idx)
        assert normed.min().item() >= 0.0, (
            f"Morph {morph_idx}: min normalized value {normed.min().item()} < 0"
        )
        assert normed.max().item() <= 1.0, (
            f"Morph {morph_idx}: max normalized value {normed.max().item()} > 1"
        )


class TestSignedMorphsCentered:
    """Verify signed morphs return ~0.5 for constant input after normalization."""

    @pytest.mark.parametrize("morph_idx", sorted(SIGNED_MORPHS))
    def test_signed_morphs_centered(self, morph_idx):
        """Signed morphs on constant input should normalize to ~0.5.

        A constant-valued window has zero derivative, zero skewness, etc.,
        so the raw output should be ~0, which maps to 0.5 under signed
        normalization: (0/scale + 1) / 2 = 0.5.
        """
        B, F, W = 2, 5, 32
        # Constant windows (value 0.5 everywhere)
        windows = torch.full((B, F, W), 0.5)
        weights = torch.ones(W) / W

        raw = batch_morph(windows, weights, morph_idx)
        normed = normalize_morph(raw, morph_idx)

        # For constant input, raw should be ~0 (or exactly 0 for most),
        # so normalized should be ~0.5.
        assert torch.allclose(normed, torch.full_like(normed, 0.5), atol=0.05), (
            f"Signed morph {morph_idx}: expected ~0.5 for constant input, "
            f"got mean={normed.mean().item():.4f}"
        )


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------

class TestMorphErrors:
    """Verify error handling for invalid morph indices."""

    def test_individual_invalid_morph_idx(self, computer):
        """MorphComputer.compute raises ValueError for invalid index."""
        window = torch.rand(2, 16)
        weights = torch.ones(16) / 16
        with pytest.raises(ValueError, match="Invalid morph_idx"):
            computer.compute(window, weights, 24)

    def test_batch_invalid_morph_idx(self):
        """batch_morph raises ValueError for invalid index."""
        windows = torch.rand(2, 5, 16)
        weights = torch.ones(16) / 16
        with pytest.raises(ValueError, match="Invalid morph_idx"):
            batch_morph(windows, weights, -1)
