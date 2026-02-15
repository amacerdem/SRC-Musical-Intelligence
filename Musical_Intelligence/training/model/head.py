"""Learned Inverse Heads — Conv1D architectures for mel↔C³ mapping.

Head1 (PerceptionHead): mel → C³ approximation.
    Compresses 128D mel to N-dim nucleus output.
    Supervised by deterministic forward pipeline.

Head2 (ExpressionHead): C³ → mel generation.
    Expands N-dim nucleus output back to 128D mel.
    Supervised by original mel spectrograms.

InverseHeadPair: Holds both heads and provides cycle consistency loss.

Architecture: Conv1D stack with expanding receptive field.
    Each layer adds temporal context matching H³ horizons (25ms→200ms).
    Receptive field ≈ 37 frames (215ms) covers BCH's longest H³ horizon.

Reference: MI-PLASTICITY.md §13.13 (Learned Inverse Heads).
"""
from __future__ import annotations

from typing import Sequence, Tuple

import torch
import torch.nn as nn
from torch import Tensor

from .mi_space_layout import COCHLEA_DIM


# ======================================================================
# Building blocks
# ======================================================================


class ConvBlock(nn.Module):
    """Conv1D → GELU → LayerNorm."""

    def __init__(self, in_ch: int, out_ch: int, kernel_size: int) -> None:
        super().__init__()
        padding = kernel_size // 2  # same-length output
        self.conv = nn.Conv1d(in_ch, out_ch, kernel_size, padding=padding)
        self.act = nn.GELU()
        self.norm = nn.LayerNorm(out_ch)

    def forward(self, x: Tensor) -> Tensor:
        """x: (B, C, T) → (B, C_out, T)."""
        x = self.conv(x)         # (B, C_out, T)
        x = self.act(x)
        # LayerNorm expects (..., C) so transpose → norm → transpose back
        x = self.norm(x.transpose(1, 2)).transpose(1, 2)
        return x


# ======================================================================
# PerceptionHead (mel → target)
# ======================================================================


class PerceptionHead(nn.Module):
    """Head 1: mel(128, T) → target(N, T).

    Approximates the deterministic forward pipeline (mel → R³ → H³ → C³)
    with a lightweight Conv1D stack. Trained on (mel, C³) pairs produced
    by running the pipeline on audio.

    Parameters
    ----------
    target_dim : int
        Output dimensionality (e.g. 12 for BCH, 1006 for full C³).
    hidden_dim : int
        Hidden channel width (default 256).
    kernel_sizes : sequence of int
        Kernel sizes for the Conv1D stack (default (3, 5, 7, 11, 15)).
        Determines receptive field: sum(k-1) + 1 = RF.
    """

    def __init__(
        self,
        target_dim: int,
        hidden_dim: int = 256,
        kernel_sizes: Sequence[int] = (3, 5, 7, 11, 15),
    ) -> None:
        super().__init__()
        layers = []

        # First block: input projection
        layers.append(ConvBlock(COCHLEA_DIM, hidden_dim, kernel_sizes[0]))

        # Hidden blocks: expanding receptive field
        for k in kernel_sizes[1:]:
            layers.append(ConvBlock(hidden_dim, hidden_dim, k))

        self.encoder = nn.Sequential(*layers)

        # Final projection: hidden → target_dim, no activation yet
        self.proj = nn.Conv1d(hidden_dim, target_dim, kernel_size=1)

    def forward(self, mel: Tensor) -> Tensor:
        """Map mel spectrogram to target features.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, 128, T)`` log1p-normalised mel spectrogram.

        Returns
        -------
        Tensor
            Shape ``(B, target_dim, T)`` with values in ``[0, 1]``.
        """
        h = self.encoder(mel)       # (B, hidden, T)
        out = self.proj(h)          # (B, target_dim, T)
        return torch.sigmoid(out)   # [0, 1] to match pipeline output range


# ======================================================================
# ExpressionHead (target → mel)
# ======================================================================


class ExpressionHead(nn.Module):
    """Head 2: target(N, T) → mel(128, T).

    Generates mel spectrograms from cognitive state vectors. This is the
    learned inverse — it does not invert the pipeline analytically, but
    learns a mapping from (mel, C³) pairs.

    Parameters
    ----------
    target_dim : int
        Input dimensionality (e.g. 12 for BCH, 1006 for full C³).
    hidden_dim : int
        Hidden channel width (default 256).
    kernel_sizes : sequence of int
        Kernel sizes for the Conv1D stack (default (15, 11, 7, 5, 3)).
        Reversed from PerceptionHead — expanding from narrow input.
    """

    def __init__(
        self,
        target_dim: int,
        hidden_dim: int = 256,
        kernel_sizes: Sequence[int] = (15, 11, 7, 5, 3),
    ) -> None:
        super().__init__()

        # Input projection: target_dim → hidden (1×1 conv)
        self.input_proj = ConvBlock(target_dim, hidden_dim, kernel_size=1)

        # Hidden blocks: temporal context
        layers = []
        for k in kernel_sizes:
            layers.append(ConvBlock(hidden_dim, hidden_dim, k))
        self.decoder = nn.Sequential(*layers)

        # Final projection: hidden → mel bins
        self.proj = nn.Conv1d(hidden_dim, COCHLEA_DIM, kernel_size=1)

    def forward(self, target: Tensor) -> Tensor:
        """Map target features to mel spectrogram.

        Parameters
        ----------
        target : Tensor
            Shape ``(B, target_dim, T)`` cognitive state features.

        Returns
        -------
        Tensor
            Shape ``(B, 128, T)`` reconstructed mel spectrogram in ``[0, 1]``.
        """
        h = self.input_proj(target)  # (B, hidden, T)
        h = self.decoder(h)          # (B, hidden, T)
        out = self.proj(h)           # (B, 128, T)
        return torch.sigmoid(out)    # [0, 1] to match mel range


# ======================================================================
# InverseHeadPair
# ======================================================================


class InverseHeadPair(nn.Module):
    """Paired perception + expression heads with cycle consistency.

    Holds Head1 (mel→target) and Head2 (target→mel). Provides:
    - Independent forward passes for each head
    - Cycle consistency loss: head1(head2(target)) ≈ target

    Parameters
    ----------
    target_dim : int
        Dimensionality of the target space (e.g. 12 for BCH).
    hidden_dim : int
        Hidden channel width for both heads.
    kernel_sizes : sequence of int
        Kernel sizes (perception uses as-is, expression uses reversed).
    """

    def __init__(
        self,
        target_dim: int,
        hidden_dim: int = 256,
        kernel_sizes: Sequence[int] = (3, 5, 7, 11, 15),
    ) -> None:
        super().__init__()
        self.perception = PerceptionHead(
            target_dim=target_dim,
            hidden_dim=hidden_dim,
            kernel_sizes=kernel_sizes,
        )
        self.expression = ExpressionHead(
            target_dim=target_dim,
            hidden_dim=hidden_dim,
            kernel_sizes=tuple(reversed(kernel_sizes)),
        )
        self.target_dim = target_dim

    def forward_head1(self, mel: Tensor) -> Tensor:
        """Perception: mel(B, 128, T) → target_hat(B, N, T)."""
        return self.perception(mel)

    def forward_head2(self, target: Tensor) -> Tensor:
        """Expression: target(B, N, T) → mel_hat(B, 128, T)."""
        return self.expression(target)

    def cycle_loss(self, target: Tensor) -> Tuple[Tensor, Tensor]:
        """Cycle consistency: target → mel_hat → target_hat ≈ target.

        Parameters
        ----------
        target : Tensor
            Shape ``(B, N, T)`` ground-truth target features.

        Returns
        -------
        loss : Tensor
            Scalar MSE between target and reconstructed target.
        mel_hat : Tensor
            Intermediate mel reconstruction (useful for logging).
        """
        mel_hat = self.expression(target)           # (B, 128, T)
        target_hat = self.perception(mel_hat)       # (B, N, T)
        loss = torch.nn.functional.mse_loss(target_hat, target)
        return loss, mel_hat
