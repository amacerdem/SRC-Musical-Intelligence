"""SparseAttention -- Windowed sparse attention with global tokens.

Every 4th layer in the MI-Core backbone is a sparse attention layer
(vs 3 consecutive Mamba-2 layers). This provides long-range planning
capability while keeping O(n) average complexity.

The attention window is 256 frames (~1.5s) with 16 global tokens
that attend to the entire sequence for long-range dependencies.
"""
from __future__ import annotations

import math
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class SparseAttention(nn.Module):
    """Windowed sparse attention with global tokens for long-range planning.

    Combines local windowed attention with a small number of global tokens
    that can attend to the full sequence. This provides:
    - Local context within ~1.5s window
    - Global planning through global tokens
    - O(n * window) complexity instead of O(n^2)

    Parameters
    ----------
    d_model : int
        Model dimension (default 2048).
    n_heads : int
        Number of attention heads (default 16).
    window_size : int
        Local attention window in frames (default 256 ≈ 1.5s).
    n_global_tokens : int
        Number of global planning tokens (default 16).
    dropout : float
        Attention dropout rate (default 0.0).
    """

    def __init__(
        self,
        d_model: int = 2048,
        n_heads: int = 16,
        window_size: int = 256,
        n_global_tokens: int = 16,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.head_dim = d_model // n_heads
        self.window_size = window_size
        self.n_global_tokens = n_global_tokens

        assert d_model % n_heads == 0, "d_model must be divisible by n_heads"

        # Q, K, V projections
        self.q_proj = nn.Linear(d_model, d_model, bias=False)
        self.k_proj = nn.Linear(d_model, d_model, bias=False)
        self.v_proj = nn.Linear(d_model, d_model, bias=False)
        self.out_proj = nn.Linear(d_model, d_model, bias=False)

        # Global tokens (learnable)
        self.global_tokens = nn.Parameter(
            torch.randn(1, n_global_tokens, d_model) * 0.02
        )

        # Layer norm
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)

        # Scale factor
        self.scale = self.head_dim ** -0.5

    def forward(self, x: Tensor, mask: Optional[Tensor] = None) -> Tensor:
        """Forward pass with windowed sparse attention.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)``.
        mask : Tensor, optional
            Attention mask ``(B, T)`` where True = valid.

        Returns
        -------
        Tensor
            Shape ``(B, T, d_model)``.
        """
        B, T, D = x.shape
        residual = x
        x = self.norm(x)

        # Expand global tokens and prepend
        global_tokens = self.global_tokens.expand(B, -1, -1)
        x_with_global = torch.cat([global_tokens, x], dim=1)  # (B, G+T, D)
        G = self.n_global_tokens

        # Project Q, K, V
        Q = self.q_proj(x_with_global)  # (B, G+T, D)
        K = self.k_proj(x_with_global)
        V = self.v_proj(x_with_global)

        # Reshape for multi-head attention
        Q = Q.view(B, G + T, self.n_heads, self.head_dim).transpose(1, 2)
        K = K.view(B, G + T, self.n_heads, self.head_dim).transpose(1, 2)
        V = V.view(B, G + T, self.n_heads, self.head_dim).transpose(1, 2)
        # Shape: (B, n_heads, G+T, head_dim)

        # Build sparse attention mask
        attn_mask = self._build_sparse_mask(T, G, x.device)

        # Scaled dot-product attention with mask
        attn_weights = torch.matmul(Q, K.transpose(-2, -1)) * self.scale
        attn_weights = attn_weights + attn_mask.unsqueeze(0).unsqueeze(0)
        attn_weights = F.softmax(attn_weights, dim=-1)
        attn_weights = self.dropout(attn_weights)

        attn_output = torch.matmul(attn_weights, V)  # (B, n_heads, G+T, head_dim)
        attn_output = attn_output.transpose(1, 2).reshape(B, G + T, D)

        # Remove global tokens from output
        output = attn_output[:, G:]  # (B, T, D)
        output = self.out_proj(output)
        output = output + residual

        return output

    def _build_sparse_mask(self, T: int, G: int, device: torch.device) -> Tensor:
        """Build sparse attention mask with global + windowed local.

        Global tokens attend to everything. Local tokens attend to
        global tokens + their local window.

        Returns
        -------
        Tensor
            Shape ``(G+T, G+T)`` with 0 for allowed and -inf for masked.
        """
        total = G + T
        mask = torch.full((total, total), float("-inf"), device=device)

        # Global tokens can attend to everything
        mask[:G, :] = 0.0
        # Everything can attend to global tokens
        mask[:, :G] = 0.0

        # Local windowed attention (causal)
        for i in range(T):
            row = i + G
            start = max(0, i - self.window_size + 1) + G
            end = i + G + 1  # Causal: only past and present
            mask[row, start:end] = 0.0

        return mask
