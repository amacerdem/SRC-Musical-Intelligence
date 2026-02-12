"""
Attention Weighting — Exponential decay for temporal windows.

A(dt) = exp(-3|dt|/H)

Recent frames matter more than distant ones. The decay constant 3.0
means the weight drops to ~5% at the window boundary.
"""

from __future__ import annotations

import torch
from torch import Tensor

from ...core.constants import ATTENTION_DECAY


def compute_attention_weights(
    window_size: int,
    device: torch.device = torch.device("cpu"),
    decay: float = ATTENTION_DECAY,
) -> Tensor:
    """Compute exponential attention weights for a window.

    Args:
        window_size: number of frames in the window
        device: torch device
        decay: decay constant (default 3.0)

    Returns:
        (window_size,) tensor of weights, highest at center
    """
    if window_size <= 1:
        return torch.ones(window_size, device=device)

    # Normalized positions from 0 to 1
    positions = torch.linspace(0, 1, window_size, device=device)

    # Exponential decay from the end (most recent frame)
    weights = torch.exp(-decay * (1.0 - positions))

    return weights
