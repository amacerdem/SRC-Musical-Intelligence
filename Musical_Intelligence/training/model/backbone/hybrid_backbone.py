"""HybridBackbone -- 24-layer Mamba-2 + Sparse Attention interleaved stack.

The MI-Core backbone uses a 3:1 ratio of Mamba-2 to Sparse Attention
layers. This provides:
- Mamba-2: O(n) streaming, state-based memory, causal processing
- Sparse Attention: Long-range planning via global tokens, every 4th layer

Architecture::

    Layer  0: Mamba2Block
    Layer  1: Mamba2Block
    Layer  2: Mamba2Block
    Layer  3: SparseAttention
    Layer  4: Mamba2Block
    ...
    Layer 23: SparseAttention    (6th attention layer)

Total: 18 Mamba-2 + 6 Sparse Attention = 24 layers
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
from torch import Tensor

from .mamba2_block import Mamba2Block
from .sparse_attention import SparseAttention


class HybridBackbone(nn.Module):
    """24-layer interleaved Mamba-2 + Sparse Attention backbone.

    The backbone processes input features into a hidden representation
    suitable for the MI-aligned expert heads.

    Parameters
    ----------
    d_model : int
        Hidden dimension (default 2048).
    n_layers : int
        Total number of layers (default 24).
    d_state : int
        Mamba-2 state dimension (default 64).
    d_conv : int
        Mamba-2 convolution kernel size (default 4).
    expand : int
        Mamba-2 expansion factor (default 2).
    attn_every : int
        Insert sparse attention every N layers (default 4).
    attn_window : int
        Sparse attention window size (default 256).
    attn_global_tokens : int
        Number of global tokens in sparse attention (default 16).
    n_heads : int
        Number of attention heads (default 16).
    dropout : float
        Dropout rate (default 0.0).
    """

    def __init__(
        self,
        d_model: int = 2048,
        n_layers: int = 24,
        d_state: int = 64,
        d_conv: int = 4,
        expand: int = 2,
        attn_every: int = 4,
        attn_window: int = 256,
        attn_global_tokens: int = 16,
        n_heads: int = 16,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_model = d_model
        self.n_layers = n_layers
        self.attn_every = attn_every

        layers: List[nn.Module] = []
        self._layer_types: List[str] = []

        for i in range(n_layers):
            if (i + 1) % attn_every == 0:
                # Sparse Attention layer
                layers.append(
                    SparseAttention(
                        d_model=d_model,
                        n_heads=n_heads,
                        window_size=attn_window,
                        n_global_tokens=attn_global_tokens,
                        dropout=dropout,
                    )
                )
                self._layer_types.append("attn")
            else:
                # Mamba-2 layer
                layers.append(
                    Mamba2Block(
                        d_model=d_model,
                        d_state=d_state,
                        d_conv=d_conv,
                        expand=expand,
                        dropout=dropout,
                    )
                )
                self._layer_types.append("mamba")

        self.layers = nn.ModuleList(layers)

        # Final layer norm
        self.final_norm = nn.LayerNorm(d_model)

    # ------------------------------------------------------------------
    # Forward
    # ------------------------------------------------------------------

    def forward(
        self,
        x: Tensor,
        states: Optional[Dict[int, Tensor]] = None,
        mask: Optional[Tensor] = None,
    ) -> Tuple[Tensor, Dict[int, Tensor]]:
        """Forward pass through all 24 layers.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)``.
        states : dict, optional
            Per-layer Mamba states from previous call.
            Keys are layer indices, values are ``(B, d_inner, d_state)``.
        mask : Tensor, optional
            Attention mask ``(B, T)`` for sparse attention layers.

        Returns
        -------
        output : Tensor
            Shape ``(B, T, d_model)``.
        new_states : dict
            Updated Mamba states for all Mamba layers.
        """
        if states is None:
            states = {}

        new_states: Dict[int, Tensor] = {}

        for i, (layer, layer_type) in enumerate(
            zip(self.layers, self._layer_types)
        ):
            if layer_type == "mamba":
                state = states.get(i, None)
                x, new_state = layer(x, state)
                new_states[i] = new_state
            else:
                # Sparse attention
                x = layer(x, mask)

        x = self.final_norm(x)
        return x, new_states

    # ------------------------------------------------------------------
    # Streaming
    # ------------------------------------------------------------------

    def init_states(self, batch_size: int, device: torch.device) -> Dict[int, Tensor]:
        """Create zero-initialised states for all Mamba layers."""
        states = {}
        for i, (layer, layer_type) in enumerate(
            zip(self.layers, self._layer_types)
        ):
            if layer_type == "mamba":
                states[i] = layer.init_state(batch_size, device)
        return states

    # ------------------------------------------------------------------
    # Info
    # ------------------------------------------------------------------

    @property
    def n_mamba_layers(self) -> int:
        """Number of Mamba-2 layers."""
        return sum(1 for t in self._layer_types if t == "mamba")

    @property
    def n_attn_layers(self) -> int:
        """Number of Sparse Attention layers."""
        return sum(1 for t in self._layer_types if t == "attn")

    def __repr__(self) -> str:
        return (
            f"HybridBackbone(d_model={self.d_model}, n_layers={self.n_layers}, "
            f"mamba={self.n_mamba_layers}, attn={self.n_attn_layers})"
        )
