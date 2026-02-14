"""SPU — Spectral Processing Unit.

Independent (Phase 2).
9 models, 99D total output, circuit: perceptual, d = 0.84.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from ....contracts.bases.base_model import BaseModel
from ....contracts.bases.base_unit import BaseCognitiveUnit
from .models import MODEL_CLASSES


class SPUUnit(BaseCognitiveUnit):
    """Spectral Processing Unit (SPU).

    Circuit: perceptual | d = 0.84 | 9 models | 99D
    """

    UNIT_NAME = "SPU"
    FULL_NAME = "Spectral Processing Unit"
    CIRCUIT = "perceptual"
    POOLED_EFFECT = 0.84

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in MODEL_CLASSES]
        self._mechanism_outputs: Dict[str, Tensor] = {}

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def models(self) -> List[BaseModel]:
        """Models in tier order (alpha -> beta -> gamma)."""
        return self._models

    # ------------------------------------------------------------------
    # Mechanism injection
    # ------------------------------------------------------------------

    def set_mechanism_outputs(self, mechanism_outputs: Dict[str, Tensor]) -> None:
        """Inject cached mechanism outputs before compute()."""
        self._mechanism_outputs = mechanism_outputs

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

        Returns (B, T, 99) tensor.
        """
        if not self._models:
            B, T = r3_features.shape[:2]
            return torch.zeros(B, T, 0, device=r3_features.device)

        outputs: List[Tensor] = []
        for model in self.active_models:
            out = model.compute(
                self._mechanism_outputs,
                h3_features,
                r3_features,
                cross_unit_inputs,
            )
            outputs.append(out)

        return torch.cat(outputs, dim=-1)
