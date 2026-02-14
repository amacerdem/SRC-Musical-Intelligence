"""Distributed training utilities -- DDP / FSDP setup.

Provides helper functions for setting up PyTorch Distributed Data Parallel
(DDP) or Fully Sharded Data Parallel (FSDP) training.
"""
from __future__ import annotations

import os
from typing import Optional

import torch
import torch.distributed as dist
import torch.nn as nn
from torch.nn.parallel import DistributedDataParallel as DDP


def setup_distributed(
    backend: str = "nccl",
    init_method: str = "env://",
) -> int:
    """Initialise distributed process group.

    Returns the local rank.
    """
    if not dist.is_initialized():
        dist.init_process_group(backend=backend, init_method=init_method)

    local_rank = int(os.environ.get("LOCAL_RANK", 0))
    torch.cuda.set_device(local_rank)
    return local_rank


def cleanup_distributed() -> None:
    """Clean up distributed process group."""
    if dist.is_initialized():
        dist.destroy_process_group()


def wrap_model_ddp(
    model: nn.Module,
    device_id: Optional[int] = None,
    find_unused_parameters: bool = False,
) -> DDP:
    """Wrap model with DistributedDataParallel.

    Parameters
    ----------
    model : nn.Module
        Model to wrap.
    device_id : int, optional
        CUDA device ID. If None, uses current device.
    find_unused_parameters : bool
        Whether to find unused parameters (default False).

    Returns
    -------
    DDP
        Wrapped model.
    """
    if device_id is None:
        device_id = torch.cuda.current_device()

    model = model.to(device_id)
    return DDP(
        model,
        device_ids=[device_id],
        find_unused_parameters=find_unused_parameters,
    )


def is_main_process() -> bool:
    """Check if this is the main (rank 0) process."""
    if not dist.is_initialized():
        return True
    return dist.get_rank() == 0


def get_world_size() -> int:
    """Get the number of distributed processes."""
    if not dist.is_initialized():
        return 1
    return dist.get_world_size()
