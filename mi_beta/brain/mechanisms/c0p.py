"""Cognitive Projection mechanism stub."""
from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ...contracts.base_mechanism import BaseMechanism


class C0PMechanism(BaseMechanism):
    NAME = "C0P"
    FULL_NAME = "Cognitive Projection"
    HORIZONS = (18, 19, 20)

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        return set()

    def compute(self, h3_features, r3_features):
        B, T, _ = r3_features.shape
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
