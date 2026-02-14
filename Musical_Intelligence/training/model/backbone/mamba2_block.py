"""Mamba2Block -- Selective State-Space Model (Mamba-2) layer.

Implements the Mamba-2 selective SSM block from Gu & Dao (2024).
Input-dependent A, B, C matrices with selective scan provide:
- O(n) complexity for real-time streaming
- State = memory (compressed history of all past frames)
- Causal processing without future peeking

This is the core computational primitive of the MI-Core backbone.
18 of the 24 backbone layers are Mamba-2 blocks.

Reference:
    Gu, A. & Dao, T. (2024). "Transformers are SSMs: Generalized Models
    and Efficient Algorithms Through Structured State Space Duality."
"""
from __future__ import annotations

import math
from typing import Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class Mamba2Block(nn.Module):
    """Mamba-2 Selective State-Space block.

    Uses input-dependent selection mechanism: the B, C, and delta
    matrices are functions of the input, allowing the model to
    selectively filter information along the sequence.

    Parameters
    ----------
    d_model : int
        Model dimension (default 2048).
    d_state : int
        SSM state dimension (default 64).
    d_conv : int
        Local convolution width (default 4).
    expand : int
        Inner dimension expansion factor (default 2).
    dt_rank : str or int
        Rank of the delta projection. ``"auto"`` sets it to
        ``ceil(d_model / 16)`` (default ``"auto"``).
    """

    def __init__(
        self,
        d_model: int = 2048,
        d_state: int = 64,
        d_conv: int = 4,
        expand: int = 2,
        dt_rank: str | int = "auto",
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = d_model * expand

        if dt_rank == "auto":
            self.dt_rank = math.ceil(d_model / 16)
        else:
            self.dt_rank = int(dt_rank)

        # Input projection: x -> (z, x_proj) where z is gate, x_proj goes to SSM
        self.in_proj = nn.Linear(d_model, self.d_inner * 2, bias=False)

        # Local convolution (causal)
        self.conv1d = nn.Conv1d(
            self.d_inner,
            self.d_inner,
            kernel_size=d_conv,
            padding=d_conv - 1,
            groups=self.d_inner,
            bias=True,
        )

        # SSM parameter projections (input-dependent)
        self.x_proj = nn.Linear(self.d_inner, self.dt_rank + d_state * 2, bias=False)
        self.dt_proj = nn.Linear(self.dt_rank, self.d_inner, bias=True)

        # SSM parameters
        # A is structured as log-space diagonal for stability
        A = torch.arange(1, d_state + 1, dtype=torch.float32)
        self.A_log = nn.Parameter(torch.log(A.repeat(self.d_inner, 1)))
        self.D = nn.Parameter(torch.ones(self.d_inner))

        # Output projection
        self.out_proj = nn.Linear(self.d_inner, d_model, bias=False)

        # Layer norm
        self.norm = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout) if dropout > 0 else nn.Identity()

    def forward(
        self,
        x: Tensor,
        state: Optional[Tensor] = None,
    ) -> Tuple[Tensor, Tensor]:
        """Forward pass through the Mamba-2 block.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)``.
        state : Tensor, optional
            SSM state from previous call, shape ``(B, d_inner, d_state)``.
            If None, initialised to zeros.

        Returns
        -------
        output : Tensor
            Shape ``(B, T, d_model)``.
        new_state : Tensor
            Updated SSM state ``(B, d_inner, d_state)``.
        """
        B, T, D = x.shape
        residual = x
        x = self.norm(x)

        # Input projection: split into x_proj and gate z
        xz = self.in_proj(x)  # (B, T, 2 * d_inner)
        x_proj, z = xz.chunk(2, dim=-1)  # Each (B, T, d_inner)

        # Causal convolution
        x_conv = x_proj.transpose(1, 2)  # (B, d_inner, T)
        x_conv = self.conv1d(x_conv)[:, :, :T]  # Causal: trim future
        x_conv = x_conv.transpose(1, 2)  # (B, T, d_inner)
        x_conv = F.silu(x_conv)

        # Input-dependent SSM parameters
        x_ssm = self.x_proj(x_conv)  # (B, T, dt_rank + 2*d_state)
        dt, B_proj, C_proj = torch.split(
            x_ssm, [self.dt_rank, self.d_state, self.d_state], dim=-1
        )
        dt = self.dt_proj(dt)  # (B, T, d_inner)
        dt = F.softplus(dt)    # Ensure positive discretisation step

        # A matrix (diagonal, from log-space)
        A = -torch.exp(self.A_log)  # (d_inner, d_state), negative for stability

        # Selective scan
        y, new_state = self._selective_scan(
            x_conv, dt, A, B_proj, C_proj, self.D, state
        )

        # Gate and output
        y = y * F.silu(z)
        output = self.out_proj(y)
        output = self.dropout(output)
        output = output + residual

        return output, new_state

    def step(
        self,
        x: Tensor,
        state: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        """Single-step inference for streaming.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, 1, d_model)`` single frame.
        state : Tensor
            SSM state ``(B, d_inner, d_state)``.

        Returns
        -------
        output : Tensor
            Shape ``(B, 1, d_model)``.
        new_state : Tensor
            Updated state.
        """
        return self.forward(x, state)

    @staticmethod
    def _selective_scan(
        x: Tensor,
        dt: Tensor,
        A: Tensor,
        B: Tensor,
        C: Tensor,
        D: Tensor,
        state: Optional[Tensor],
    ) -> Tuple[Tensor, Tensor]:
        """Selective scan (parallel scan over sequence).

        This is the core SSM computation. For training, we use a
        sequential scan (can be replaced with parallel scan for speed).

        Parameters
        ----------
        x : Tensor (B, T, d_inner)
        dt : Tensor (B, T, d_inner)
        A : Tensor (d_inner, d_state)
        B : Tensor (B, T, d_state)
        C : Tensor (B, T, d_state)
        D : Tensor (d_inner,)
        state : Tensor (B, d_inner, d_state) or None
        """
        batch, seq_len, d_inner = x.shape
        d_state = A.shape[1]

        # Discretise: dA = exp(dt * A), dB = dt * B
        # dt: (B, T, d_inner), A: (d_inner, d_state)
        dA = torch.exp(
            dt.unsqueeze(-1) * A.unsqueeze(0).unsqueeze(0)
        )  # (B, T, d_inner, d_state)

        dB = dt.unsqueeze(-1) * B.unsqueeze(2)  # (B, T, d_inner, d_state)

        # Initialise state
        if state is None:
            h = torch.zeros(
                batch, d_inner, d_state,
                device=x.device, dtype=x.dtype,
            )
        else:
            h = state

        # Sequential scan
        outputs = []
        for t in range(seq_len):
            # h = dA * h + dB * x
            h = dA[:, t] * h + dB[:, t] * x[:, t].unsqueeze(-1)
            # y = C * h + D * x
            y_t = (h * C[:, t].unsqueeze(1)).sum(dim=-1) + D * x[:, t]
            outputs.append(y_t)

        y = torch.stack(outputs, dim=1)  # (B, T, d_inner)
        return y, h

    def init_state(self, batch_size: int, device: torch.device) -> Tensor:
        """Create zero-initialised SSM state."""
        return torch.zeros(
            batch_size, self.d_inner, self.d_state,
            device=device,
        )
