"""Information morph: M20 entropy.

All functions are pure (torch only, no project dependencies).
"""
from __future__ import annotations

import torch
from torch import Tensor


def m20_entropy(window: Tensor, weights: Tensor) -> Tensor:
    """M20: Shannon entropy over a 16-bin histogram.

    Formula: -sum(p * log2(p)) where p is the bin probability distribution.
    Uses 16 equally-spaced bins over [0, 1].

    Args:
        window: (B, W) R3 values in the time window (expected in [0, 1]).
        weights: (W,) Unused (interface consistency).

    Returns:
        (B,) Raw Shannon entropy in bits (max = log2(16) = 4.0).

    Properties:
        - Unsigned, min window = 4.
        - Returns zeros(B) for win_len < 4.
        - Returns 0.0 for constant input (all mass in one bin).
    """
    B, W = window.shape
    NUM_BINS = 16

    if W < 4:
        return torch.zeros(B, device=window.device, dtype=window.dtype)

    # Clamp to [0, 1] as a safety net for R3 features
    x = window.clamp(0.0, 1.0)

    result = torch.zeros(B, device=window.device, dtype=window.dtype)

    for b in range(B):
        # Compute histogram for this batch item
        # Bin indices: floor(x * NUM_BINS), clamped to [0, NUM_BINS-1]
        bin_idx = (x[b] * NUM_BINS).long().clamp(0, NUM_BINS - 1)
        counts = torch.zeros(NUM_BINS, device=window.device, dtype=window.dtype)
        for i in range(W):
            counts[bin_idx[i]] += 1.0

        # Probability distribution
        p = counts / W

        # Shannon entropy: -sum(p * log2(p)), skipping p == 0
        mask = p > 0
        if mask.any():
            p_nz = p[mask]
            result[b] = -torch.sum(p_nz * torch.log2(p_nz))

    # Ensure clean zero (avoid -0.0 from -sum(1.0 * log2(1.0)))
    return torch.abs(result)
