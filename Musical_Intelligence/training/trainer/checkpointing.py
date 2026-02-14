"""Checkpointing utilities for MI-Core training.

Supports save/load/resume, H3 auxiliary head pruning for export,
and best-model tracking.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

import torch
import torch.nn as nn


def save_checkpoint(
    model: nn.Module,
    optimizer: Any,
    epoch: int,
    global_step: int,
    path: str,
    extra: Optional[Dict] = None,
) -> Path:
    """Save training checkpoint."""
    save_path = Path(path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    state = {
        "epoch": epoch,
        "global_step": global_step,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
    }
    if extra:
        state.update(extra)

    torch.save(state, save_path)
    return save_path


def load_checkpoint(
    path: str,
    model: nn.Module,
    optimizer: Optional[Any] = None,
    map_location: str = "cpu",
) -> Dict:
    """Load checkpoint into model and optionally optimizer."""
    ckpt = torch.load(path, map_location=map_location)
    model.load_state_dict(ckpt["model_state_dict"])
    if optimizer is not None and "optimizer_state_dict" in ckpt:
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
    return ckpt


def export_inference_model(
    model: nn.Module,
    output_path: str,
) -> Path:
    """Export model for inference by pruning training-only components.

    Removes:
    - H3 auxiliary head (training-only, pruned after training)
    - Gradient buffers

    The backbone retains temporal awareness in its Mamba state.
    """
    # Prune H3 aux head
    if hasattr(model, "prune_h3_aux"):
        model.prune_h3_aux()

    # Save state dict without training artifacts
    save_path = Path(output_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)

    state = {k: v for k, v in model.state_dict().items()
             if "h3_aux_head" not in k}

    torch.save({
        "model_state_dict": state,
        "pruned": True,
    }, save_path)

    return save_path
