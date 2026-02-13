"""Beat Entrainment Processing mechanism stub."""
from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ...contracts.base_mechanism import BaseMechanism


class BEPMechanism(BaseMechanism):
    NAME = "BEP"
    FULL_NAME = "Beat Entrainment Processing"
    HORIZONS = (6, 9, 11)

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        return set()

    def compute(self, h3_features, r3_features):
        B, T, _ = r3_features.shape
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
