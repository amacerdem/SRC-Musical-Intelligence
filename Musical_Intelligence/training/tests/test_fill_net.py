"""Tests for FillNet masked autoencoder.

Verifies:
- Forward pass shape correctness
- Known dimensions are preserved (mask=1 → unchanged)
- Random mask generation produces valid masks
- Gradient flow through fill-net
"""
from __future__ import annotations

import pytest
import torch

from Musical_Intelligence.training.model.fill_net.fill_net import FillNet
from Musical_Intelligence.training.model.mi_space_layout import C3_DIM


@pytest.fixture
def fill_net():
    """Create a small FillNet for testing."""
    return FillNet(
        c3_dim=C3_DIM,
        hidden_dim=64,
        n_layers=2,
        n_heads=4,
        dropout=0.0,
    )


class TestFillNetForward:
    """Test FillNet forward pass."""

    def test_output_shape(self, fill_net):
        B, T = 2, 16
        c3 = torch.randn(B, T, C3_DIM)
        mask = torch.ones(B, T, C3_DIM)
        mask[:, :, ::2] = 0

        c3_masked = c3 * mask
        output = fill_net(c3_masked, mask)

        assert output.shape == (B, T, C3_DIM)

    def test_known_dims_preserved(self, fill_net):
        B, T = 2, 16
        c3 = torch.randn(B, T, C3_DIM)
        mask = torch.ones(B, T, C3_DIM)
        mask[:, :, :100] = 0  # Mask first 100

        c3_masked = c3 * mask
        output = fill_net(c3_masked, mask)

        # Known dims (100:) should match input exactly
        assert torch.allclose(
            output[:, :, 100:],
            c3[:, :, 100:],
            atol=1e-5,
        )

    def test_output_range(self, fill_net):
        """FillNet uses sigmoid, so output should be in [0, 1]."""
        B, T = 2, 16
        c3 = torch.rand(B, T, C3_DIM)  # Values in [0, 1]
        mask = torch.ones(B, T, C3_DIM)
        mask[:, :, ::3] = 0

        c3_masked = c3 * mask
        output = fill_net(c3_masked, mask)

        # Masked (filled) values should be in [0, 1] due to sigmoid
        masked_values = output[mask == 0]
        assert masked_values.min() >= 0.0
        assert masked_values.max() <= 1.0

    def test_all_mask_one(self, fill_net):
        """If everything is known, output should equal input."""
        B, T = 1, 8
        c3 = torch.rand(B, T, C3_DIM)
        mask = torch.ones(B, T, C3_DIM)

        output = fill_net(c3, mask)
        assert torch.allclose(output, c3, atol=1e-5)


class TestRandomMask:
    """Test FillNet.random_mask() static method."""

    def test_mask_shapes(self):
        B, T, D = 4, 32, C3_DIM
        c3 = torch.randn(B, T, D)
        c3_masked, mask = FillNet.random_mask(c3)

        assert c3_masked.shape == c3.shape
        assert mask.shape == c3.shape

    def test_mask_binary(self):
        c3 = torch.randn(2, 16, C3_DIM)
        _, mask = FillNet.random_mask(c3)

        unique = mask.unique()
        assert all(v in (0.0, 1.0) for v in unique.tolist())

    def test_mask_ratio_bounds(self):
        c3 = torch.randn(8, 32, C3_DIM)
        _, mask = FillNet.random_mask(c3, mask_ratio_min=0.3, mask_ratio_max=0.7)

        # Per batch element, mask ratio should be between 0.3 and 0.7
        for b in range(8):
            ratio = 1.0 - mask[b, 0].mean().item()  # Fraction masked
            assert 0.1 < ratio < 0.9  # Allow some tolerance

    def test_masked_values_zeroed(self):
        c3 = torch.randn(2, 16, C3_DIM)
        c3_masked, mask = FillNet.random_mask(c3)

        # Where mask=0, c3_masked should be 0
        assert (c3_masked[mask == 0] == 0).all()

    def test_known_values_preserved(self):
        c3 = torch.randn(2, 16, C3_DIM)
        c3_masked, mask = FillNet.random_mask(c3)

        # Where mask=1, c3_masked should equal original
        assert torch.allclose(c3_masked[mask == 1], c3[mask == 1])


class TestGradientFlow:
    """Test gradient flow through FillNet."""

    def test_gradient_to_input(self, fill_net):
        c3 = torch.randn(1, 8, C3_DIM, requires_grad=True)
        mask = torch.ones(1, 8, C3_DIM)
        mask[:, :, ::2] = 0

        c3_masked = c3 * mask
        output = fill_net(c3_masked, mask)
        loss = output.sum()
        loss.backward()

        assert c3.grad is not None

    def test_gradient_to_params(self, fill_net):
        c3 = torch.randn(1, 8, C3_DIM)
        mask = torch.ones(1, 8, C3_DIM)
        mask[:, :, ::2] = 0

        c3_masked = c3 * mask
        output = fill_net(c3_masked, mask)
        loss = output.sum()
        loss.backward()

        # At least some parameters should have gradients
        has_grad = any(
            p.grad is not None and p.grad.abs().sum() > 0
            for p in fill_net.parameters()
        )
        assert has_grad
