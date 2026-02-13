"""AttentionKernel -- exponential decay kernel for H3 temporal attention.

Generates unnormalized attention weights that assign higher weight to more
recent frames within a temporal window.  The kernel is computed once per
unique horizon and reused across all tuples sharing that horizon.

Formula
-------
    positions = linspace(0, 1, window_size)
    weights[i] = exp(-ATTENTION_DECAY * (1 - positions[i]))

With ATTENTION_DECAY = 3.0 the peak weight is 1.0 (newest frame, last
position) and the boundary weight is exp(-3) ~ 0.0498 (oldest frame,
first position).  The ratio newest:oldest = exp(3) ~ 20.09.

Normalization
-------------
Weights are NOT normalized here.  The caller normalizes after truncation:

    w = weights[:win_len]
    w = w / w.sum().clamp(min=1e-8)

This allows the same weight tensor to be sliced to different lengths at
different time steps without recomputing the exponential.

Source of truth
---------------
- Docs/H3/Contracts/AttentionKernel.md   (formula, edge cases, normalization)
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md    Section 7 (kernel properties)
"""

from __future__ import annotations

import torch
from torch import Tensor

from ..constants.laws import ATTENTION_DECAY


class AttentionKernel:
    """Exponential decay attention kernel for H3 temporal windows.

    The kernel produces monotonically increasing weights where the newest
    frame (last position) receives weight 1.0 and the oldest frame (first
    position) receives weight exp(-ATTENTION_DECAY).

    This class is stateless and lightweight -- it holds no parameters.
    """

    def compute_weights(
        self,
        window_size: int,
        device: torch.device | None = None,
    ) -> Tensor:
        """Compute unnormalized exponential decay attention weights.

        Parameters
        ----------
        window_size : int
            Number of frames in the temporal window.  Must be >= 0.
            A value of 0 returns an empty tensor; a value of 1 returns
            ``tensor([1.0])``.
        device : torch.device or None
            Target device for the output tensor.  Defaults to CPU.

        Returns
        -------
        Tensor
            Shape ``(window_size,)`` with values in
            ``[exp(-ATTENTION_DECAY), 1.0]``.  Monotonically increasing.

        Raises
        ------
        ValueError
            If *window_size* is negative.
        """
        if window_size < 0:
            raise ValueError(
                f"window_size must be >= 0, got {window_size}"
            )

        if device is None:
            device = torch.device("cpu")

        # Edge case: single frame needs no weighting
        if window_size <= 1:
            return torch.ones(window_size, device=device)

        # positions: 0.0 (oldest) -> 1.0 (newest)
        positions = torch.linspace(0.0, 1.0, window_size, device=device)

        # weights: exp(-decay * (1 - pos))
        #   pos=0  -> exp(-decay) ~ 0.0498  (oldest, first element)
        #   pos=1  -> exp(0) = 1.0          (newest, last element)
        weights = torch.exp(-ATTENTION_DECAY * (1.0 - positions))

        return weights
