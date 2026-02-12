"""Run any single model in isolation with synthetic inputs."""
from __future__ import annotations
import torch
from torch import Tensor


def isolate_model(model_name: str, batch_size: int = 1, n_frames: int = 100) -> Tensor:
    from mi_beta.core.registry import ModelRegistry
    registry = ModelRegistry()
    registry.scan()
    model = registry.get_model(model_name)
    # Create synthetic inputs
    mechanism_outputs = {
        m: torch.zeros(batch_size, n_frames, 30)
        for m in model.MECHANISM_NAMES
    }
    h3_features = {
        t: torch.zeros(batch_size, n_frames)
        for t in model.h3_demand_tuples()
    }
    r3_features = torch.zeros(batch_size, n_frames, 49)
    return model.compute(mechanism_outputs, h3_features, r3_features)
