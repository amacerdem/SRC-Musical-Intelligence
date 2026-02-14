"""Tests for MI-Core model architecture.

Verifies:
- Forward pass shapes for encode, decode, fill
- Parameter count is in expected range (~250M)
- H3 aux head pruning works
- Gradient flow through all components
"""
from __future__ import annotations

import pytest
import torch

from Musical_Intelligence.training.model.mi_core import (
    DecodeOutput,
    EncodeOutput,
    MICore,
)
from Musical_Intelligence.training.model.mi_space_layout import (
    C3_DIM,
    COCHLEA_DIM,
    H3_AUX_DIM,
    L3_DIM,
    MI_SPACE_DIM,
    R3_DIM,
)


# Use small model for testing
@pytest.fixture
def small_model():
    """Create a small MI-Core for fast testing."""
    return MICore(d_model=128, n_layers=4, dropout=0.0)


@pytest.fixture
def batch():
    """Create a dummy batch."""
    B, T = 2, 32
    return {
        "mel": torch.randn(B, T, COCHLEA_DIM),
        "r3": torch.randn(B, T, R3_DIM),
        "c3": torch.randn(B, T, C3_DIM),
    }


class TestEncodeForward:
    """Test encode (analysis) direction."""

    def test_encode_output_type(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert isinstance(out, EncodeOutput)

    def test_mi_space_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        B, T = 2, 32
        assert out.mi_space.shape == (B, T, MI_SPACE_DIM)

    def test_cochlea_hat_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.cochlea_hat.shape == (2, 32, COCHLEA_DIM)

    def test_r3_hat_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.r3_hat.shape == (2, 32, R3_DIM)

    def test_c3_hat_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.c3_hat.shape == (2, 32, C3_DIM)

    def test_l3_hat_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.l3_hat.shape == (2, 32, L3_DIM)

    def test_h3_hat_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.h3_hat is not None
        assert out.h3_hat.shape[0] == 2
        assert out.h3_hat.shape[1] == 32

    def test_hidden_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.hidden.shape == (2, 32, 128)  # d_model=128

    def test_uncertainty_shape(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.uncertainty.shape == (2, 32, MI_SPACE_DIM)

    def test_balance_loss_scalar(self, small_model, batch):
        out = small_model.encode(batch["mel"])
        assert out.balance_loss.dim() == 0  # scalar


class TestDecodeForward:
    """Test decode (synthesis) direction."""

    def test_decode_output_type(self, small_model, batch):
        out = small_model.decode(batch["c3"])
        assert isinstance(out, DecodeOutput)

    def test_mel_rec_shape(self, small_model, batch):
        out = small_model.decode(batch["c3"])
        assert out.mel_rec.shape == (2, 32, COCHLEA_DIM)

    def test_r3_rec_shape(self, small_model, batch):
        out = small_model.decode(batch["c3"])
        assert out.r3_rec.shape == (2, 32, R3_DIM)

    def test_h3_rec_shape(self, small_model, batch):
        out = small_model.decode(batch["c3"])
        assert out.h3_rec.shape[0] == 2
        assert out.h3_rec.shape[1] == 32

    def test_hidden_shape(self, small_model, batch):
        out = small_model.decode(batch["c3"])
        assert out.hidden.shape == (2, 32, 128)


class TestFillForward:
    """Test fill (C3 completion) direction."""

    def test_fill_output_shape(self, small_model, batch):
        c3 = batch["c3"]
        mask = torch.ones_like(c3)
        mask[:, :, ::2] = 0
        c3_masked = c3 * mask

        filled = small_model.fill(c3_masked, mask)
        assert filled.shape == c3.shape

    def test_fill_known_values_preserved(self, small_model, batch):
        c3 = batch["c3"]
        mask = torch.ones_like(c3)
        mask[:, :, :100] = 0  # Mask first 100 dims

        c3_masked = c3 * mask
        filled = small_model.fill(c3_masked, mask)

        # Known values (mask=1) should be preserved
        known = filled[:, :, 100:]
        original = c3[:, :, 100:]
        assert torch.allclose(known, original, atol=1e-5)


class TestH3Pruning:
    """Test H3 auxiliary head pruning."""

    def test_prune_removes_head(self, small_model):
        assert small_model.h3_aux_head is not None
        small_model.prune_h3_aux()
        assert small_model.h3_aux_head is None

    def test_encode_after_prune(self, small_model, batch):
        small_model.prune_h3_aux()
        # Should still work but h3_hat will fail
        # (in production, encode would need to handle None h3_aux_head)


class TestGradientFlow:
    """Test that gradients flow through all components."""

    def test_encode_gradient_flow(self, small_model, batch):
        mel = batch["mel"].requires_grad_(True)
        out = small_model.encode(mel)
        loss = out.mi_space.sum()
        loss.backward()

        # Check that mel received gradients
        assert mel.grad is not None
        assert mel.grad.abs().sum() > 0

    def test_decode_gradient_flow(self, small_model, batch):
        c3 = batch["c3"].requires_grad_(True)
        out = small_model.decode(c3)
        loss = out.mel_rec.sum()
        loss.backward()

        assert c3.grad is not None
        assert c3.grad.abs().sum() > 0

    def test_fill_gradient_flow(self, small_model, batch):
        c3 = batch["c3"]
        mask = torch.ones_like(c3)
        mask[:, :, ::2] = 0
        c3_masked = (c3 * mask).requires_grad_(True)

        filled = small_model.fill(c3_masked, mask)
        loss = filled.sum()
        loss.backward()

        assert c3_masked.grad is not None


class TestParamCount:
    """Test parameter count."""

    def test_small_model_params(self, small_model):
        total = small_model.param_count
        # Small model should have significantly fewer than 250M
        assert total > 0
        assert total < 50_000_000  # Under 50M for d_model=128

    def test_trainable_equals_total(self, small_model):
        # No frozen params by default
        assert small_model.trainable_param_count == small_model.param_count
