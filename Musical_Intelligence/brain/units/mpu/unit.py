"""MPU — Motor Planning Unit.

Independent (Phase 2).
10 models, 104D total output, circuit: sensorimotor, d = 0.62.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from ....contracts.bases.base_model import BaseModel
from ....contracts.bases.base_unit import BaseCognitiveUnit
from .models import MODEL_CLASSES


class MPUUnit(BaseCognitiveUnit):
    """Motor Planning Unit (MPU).

    Circuit: sensorimotor | d = 0.62 | 10 models | 104D
    """

    UNIT_NAME = "MPU"
    FULL_NAME = "Motor Planning Unit"
    CIRCUIT = "sensorimotor"
    POOLED_EFFECT = 0.62

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in MODEL_CLASSES]

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def models(self) -> List[BaseModel]:
        """Models in tier order (alpha -> beta -> gamma)."""
        return self._models

    # ------------------------------------------------------------------
    # Compute
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all models in tier order and concatenate outputs.

        Returns (B, T, 104) tensor.
        """
        if not self._models:
            B, T = r3_features.shape[:2]
            return torch.zeros(B, T, 0, device=r3_features.device)

        outputs: List[Tensor] = []
        for model in self.active_models:
            out = model.compute(
                h3_features,
                r3_features,
                cross_unit_inputs,
            )
            outputs.append(out)

        return torch.cat(outputs, dim=-1)
