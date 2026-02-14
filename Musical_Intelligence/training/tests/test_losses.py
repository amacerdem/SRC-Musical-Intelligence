"""Tests for loss functions.

Verifies:
- Each of 14 loss terms produces a non-negative scalar
- CompositeLoss aggregation with curriculum weights
- Encode/Decode/Cycle/Fill losses compute correctly
"""
from __future__ import annotations

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.training.loss.composite_loss import MICompositeLoss
from Musical_Intelligence.training.loss.cycle_loss import CycleLoss
from Musical_Intelligence.training.loss.decode_loss import DecodeLoss
from Musical_Intelligence.training.loss.encode_loss import EncodeLoss
from Musical_Intelligence.training.loss.fill_loss import FillLoss
from Musical_Intelligence.training.loss.regularization import RegularizationLoss


@pytest.fixture
def B():
    return 2


@pytest.fixture
def T():
    return 32


class TestEncodeLoss:
    """Test encode direction losses."""

    def test_all_four_terms(self, B, T):
        loss_fn = EncodeLoss()
        result = loss_fn(
            cochlea_hat=torch.randn(B, T, 128),
            r3_hat=torch.randn(B, T, 128),
            h3_hat=torch.randn(B, T, 5210),
            c3_hat=torch.randn(B, T, 1006),
            mel_target=torch.randn(B, T, 128),
            r3_target=torch.randn(B, T, 128),
            h3_target=torch.randn(B, T, 5210),
            c3_target=torch.randn(B, T, 1006),
        )

        assert "encode_mel" in result
        assert "encode_r3" in result
        assert "encode_h3" in result
        assert "encode_c3" in result

        for name, val in result.items():
            assert isinstance(val, Tensor)
            assert val.dim() == 0  # scalar
            assert val.item() >= 0  # MSE is non-negative

    def test_with_mask(self, B, T):
        loss_fn = EncodeLoss()
        mask = torch.ones(B, T)
        mask[:, T // 2:] = 0  # Mask second half

        result = loss_fn(
            cochlea_hat=torch.randn(B, T, 128),
            r3_hat=torch.randn(B, T, 128),
            h3_hat=torch.randn(B, T, 5210),
            c3_hat=torch.randn(B, T, 1006),
            mel_target=torch.randn(B, T, 128),
            r3_target=torch.randn(B, T, 128),
            h3_target=torch.randn(B, T, 5210),
            c3_target=torch.randn(B, T, 1006),
            mask=mask,
        )

        for val in result.values():
            assert val.item() >= 0

    def test_perfect_prediction_zero_loss(self, B, T):
        loss_fn = EncodeLoss()
        target = torch.randn(B, T, 128)
        result = loss_fn(
            cochlea_hat=target.clone(),
            r3_hat=target.clone(),
            h3_hat=torch.randn(B, T, 5210),
            c3_hat=torch.randn(B, T, 1006),
            mel_target=target,
            r3_target=target,
            h3_target=torch.randn(B, T, 5210),
            c3_target=torch.randn(B, T, 1006),
        )

        assert result["encode_mel"].item() < 1e-6
        assert result["encode_r3"].item() < 1e-6


class TestDecodeLoss:
    """Test decode direction losses."""

    def test_all_terms(self, B, T):
        loss_fn = DecodeLoss()
        result = loss_fn(
            h3_rec=torch.randn(B, T, 5210),
            r3_rec=torch.randn(B, T, 128),
            mel_rec=torch.randn(B, T, 128),
            h3_target=torch.randn(B, T, 5210),
            r3_target=torch.randn(B, T, 128),
            mel_target=torch.randn(B, T, 128),
        )

        assert "decode_h3" in result
        assert "decode_r3" in result
        assert "decode_mel" in result

        for val in result.values():
            assert val.item() >= 0


class TestCycleLoss:
    """Test cycle consistency losses."""

    def test_both_directions(self, B, T):
        loss_fn = CycleLoss()
        result = loss_fn(
            c3_original=torch.randn(B, T, 1006),
            c3_reconstructed=torch.randn(B, T, 1006),
            mel_original=torch.randn(B, T, 128),
            mel_reconstructed=torch.randn(B, T, 128),
        )

        assert "cycle_forward" in result
        assert "cycle_inverse" in result
        assert result["cycle_forward"].item() >= 0
        assert result["cycle_inverse"].item() >= 0


class TestFillLoss:
    """Test fill (masked autoencoder) losses."""

    def test_fill_loss(self, B, T):
        loss_fn = FillLoss()
        mask = torch.ones(B, T, 1006)
        mask[:, :, ::2] = 0  # Mask every other dim

        result = loss_fn(
            c3_filled=torch.randn(B, T, 1006),
            c3_target=torch.randn(B, T, 1006),
            mask=mask,
        )

        assert "fill_c3" in result
        assert result["fill_c3"].item() >= 0


class TestRegularization:
    """Test regularisation losses."""

    def test_temporal_smooth(self, B, T):
        loss_fn = RegularizationLoss()
        mi_space = torch.randn(B, T, 1366)
        balance = torch.tensor(0.05)

        result = loss_fn(mi_space=mi_space, balance_loss=balance)

        assert "temporal_smooth" in result
        assert "expert_balance" in result
        assert result["temporal_smooth"].item() >= 0
        assert result["expert_balance"].item() == pytest.approx(0.05)


class TestCompositeLoss:
    """Test composite loss aggregation."""

    def test_aggregation(self):
        loss_fn = MICompositeLoss()

        losses = {
            "encode_mel": torch.tensor(0.5),
            "encode_r3": torch.tensor(0.3),
            "encode_h3": torch.tensor(0.2),
            "encode_c3": torch.tensor(0.1),
            "decode_h3": torch.tensor(0.4),
            "decode_r3": torch.tensor(0.3),
            "decode_mel": torch.tensor(0.2),
            "decode_wav": torch.tensor(0.1),
            "cycle_forward": torch.tensor(0.3),
            "cycle_inverse": torch.tensor(0.2),
            "fill_c3": torch.tensor(0.5),
            "fill_decode": torch.tensor(0.3),
            "temporal_smooth": torch.tensor(0.01),
            "expert_balance": torch.tensor(0.02),
        }

        total, breakdown = loss_fn(losses, epoch=0)

        assert isinstance(total, Tensor)
        assert total.dim() == 0
        assert total.item() > 0
        assert "total" in breakdown
        assert "phase" in breakdown

    def test_phase_1_weights(self):
        loss_fn = MICompositeLoss(interpolate=False)
        losses = {
            "encode_mel": torch.tensor(1.0),
            "encode_r3": torch.tensor(1.0),
            "encode_h3": torch.tensor(1.0),
            "encode_c3": torch.tensor(1.0),
        }

        _, breakdown = loss_fn(losses, epoch=0)

        # Phase 1: encode_mel=1.0, encode_c3=0.0
        assert breakdown["encode_mel"] == pytest.approx(1.0, abs=0.01)
        assert breakdown["encode_c3"] == pytest.approx(0.0, abs=0.01)

    def test_phase_5_weights(self):
        loss_fn = MICompositeLoss(interpolate=False)
        losses = {
            "fill_c3": torch.tensor(1.0),
            "encode_mel": torch.tensor(1.0),
        }

        _, breakdown = loss_fn(losses, epoch=550)

        # Phase 5: fill_c3=1.0
        assert breakdown["fill_c3"] == pytest.approx(1.0, abs=0.01)
