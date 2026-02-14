"""Positional encoding utilities for the MI-Core backbone.

Provides Rotary Positional Encoding (RoPE) and learned positional
embeddings for use in the sparse attention layers.
"""
from __future__ import annotations

import math

import torch
import torch.nn as nn
from torch import Tensor


class RotaryPositionalEncoding(nn.Module):
    """Rotary Positional Encoding (RoPE).

    Reference: Su et al. (2021) "RoFormer: Enhanced Transformer with
    Rotary Position Embedding."

    Parameters
    ----------
    dim : int
        Embedding dimension (must be even).
    max_seq_len : int
        Maximum sequence length (default 16384 ≈ 95s at 172Hz).
    base : float
        Base frequency for the encoding (default 10000).
    """

    def __init__(
        self,
        dim: int,
        max_seq_len: int = 16384,
        base: float = 10000.0,
    ) -> None:
        super().__init__()
        assert dim % 2 == 0, "RoPE dimension must be even"

        self.dim = dim
        self.max_seq_len = max_seq_len

        # Precompute frequency bands
        inv_freq = 1.0 / (
            base ** (torch.arange(0, dim, 2).float() / dim)
        )
        self.register_buffer("inv_freq", inv_freq, persistent=False)

        # Precompute cos/sin cache
        self._build_cache(max_seq_len)

    def _build_cache(self, seq_len: int) -> None:
        """Build cos/sin cache for given sequence length."""
        t = torch.arange(seq_len, dtype=self.inv_freq.dtype)
        freqs = torch.outer(t, self.inv_freq)  # (T, dim/2)
        cache = torch.stack([freqs.cos(), freqs.sin()], dim=-1)  # (T, dim/2, 2)
        self.register_buffer("_cache", cache, persistent=False)

    def forward(self, x: Tensor) -> Tensor:
        """Apply rotary positional encoding.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, dim)`` or ``(B, n_heads, T, head_dim)``.

        Returns
        -------
        Tensor
            Same shape as input with rotary encoding applied.
        """
        if x.dim() == 4:
            B, H, T, D = x.shape
            x_reshape = x.reshape(B * H, T, D)
            out = self._apply_rope(x_reshape, T)
            return out.reshape(B, H, T, D)
        else:
            return self._apply_rope(x, x.shape[1])

    def _apply_rope(self, x: Tensor, seq_len: int) -> Tensor:
        """Apply RoPE to tensor of shape (*, T, dim)."""
        if seq_len > self.max_seq_len:
            self._build_cache(seq_len)

        cos_sin = self._cache[:seq_len]  # (T, dim/2, 2)
        cos = cos_sin[..., 0]  # (T, dim/2)
        sin = cos_sin[..., 1]  # (T, dim/2)

        # Split x into even and odd
        x1 = x[..., 0::2]  # (*, T, dim/2)
        x2 = x[..., 1::2]  # (*, T, dim/2)

        # Apply rotation
        out1 = x1 * cos - x2 * sin
        out2 = x1 * sin + x2 * cos

        # Interleave back
        out = torch.stack([out1, out2], dim=-1).flatten(-2)
        return out


class LearnedPositionalEncoding(nn.Module):
    """Learned positional embeddings.

    Parameters
    ----------
    d_model : int
        Embedding dimension.
    max_seq_len : int
        Maximum sequence length.
    """

    def __init__(self, d_model: int, max_seq_len: int = 16384) -> None:
        super().__init__()
        self.embedding = nn.Embedding(max_seq_len, d_model)
        nn.init.normal_(self.embedding.weight, std=0.02)

    def forward(self, x: Tensor) -> Tensor:
        """Add positional embeddings.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)``.

        Returns
        -------
        Tensor
            Shape ``(B, T, d_model)`` with positional encoding added.
        """
        T = x.shape[1]
        positions = torch.arange(T, device=x.device)
        return x + self.embedding(positions).unsqueeze(0)
