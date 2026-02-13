"""Attention weighting for H3 temporal windows."""

from __future__ import annotations

import torch
from torch import Tensor

from ...core.constants import ATTENTION_DECAY


def compute_attention_weights(
    window_size: int,
    device: torch.device = torch.device("cpu"),
    decay: float = ATTENTION_DECAY,
) -> Tensor:
    """Exponential attention weights: recent frames weighted more.

    Args:
        window_size: Number of frames in the window
        device: Torch device
        decay: Exponential decay constant (default 3.0)

    Returns:
        (window_size,) tensor with weights [low, ..., high]
    """
    if window_size <= 1:
        return torch.ones(window_size, device=device)

    positions = torch.linspace(0.0, 1.0, window_size, device=device)
    weights = torch.exp(-decay * (1.0 - positions))
    return weights
