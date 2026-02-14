"""Learning rate scheduling for MI-Core training.

Provides cosine warmup scheduling with optional curriculum-aware
adjustments based on the current training phase.
"""
from __future__ import annotations

import math

from torch.optim import Optimizer
from torch.optim.lr_scheduler import LambdaLR


def get_cosine_warmup_scheduler(
    optimizer: Optimizer,
    warmup_steps: int = 1000,
    total_steps: int = 100000,
    min_lr_ratio: float = 0.1,
) -> LambdaLR:
    """Create cosine annealing scheduler with linear warmup.

    Parameters
    ----------
    optimizer : Optimizer
        The optimizer to schedule.
    warmup_steps : int
        Number of warmup steps with linear ramp.
    total_steps : int
        Total training steps.
    min_lr_ratio : float
        Minimum LR as fraction of initial LR.

    Returns
    -------
    LambdaLR
        Learning rate scheduler.
    """
    def lr_lambda(step: int) -> float:
        if step < warmup_steps:
            # Linear warmup
            return step / max(1, warmup_steps)
        else:
            # Cosine decay
            progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
            cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
            return min_lr_ratio + (1.0 - min_lr_ratio) * cosine

    return LambdaLR(optimizer, lr_lambda)
