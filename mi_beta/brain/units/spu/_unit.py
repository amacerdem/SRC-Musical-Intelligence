"""
SPUUnit -- Spectral Processing Unit definition.

The SPU models how the auditory cortex processes spectral features of sound
-- pitch, consonance, timbre, and spectral integration.  Its primary neural
circuit is perceptual (Heschl's gyrus, Planum Polare), with pooled effect
size d=0.84 from the C3 meta-analysis (Core-4, k >= 10 studies).

9 models: BCH, PSCL, PCCR, STAI, TSCP, MIAA, SDNPS, ESME, SDED.
Total output: 99D per frame.

SPU is an *independent* unit -- it does not receive cross-unit inputs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_SPU_MODELS


class SPUUnit(BaseCognitiveUnit):
    """Spectral Processing Unit -- pitch, consonance, and timbre processing."""

    UNIT_NAME = "SPU"
    FULL_NAME = "Spectral Processing Unit"
    CIRCUIT = "perceptual"
    POOLED_EFFECT = 0.84

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_SPU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all SPU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Unused by SPU (independent unit).

        Returns:
            (B, T, 99) concatenated output of all 9 SPU models.
        """
        outputs: list[Tensor] = []
        for model in self.active_models:
            out = model.compute(
                mechanism_outputs={},
                h3_features=h3_features,
                r3_features=r3_features,
                cross_unit_inputs=None,
            )
            outputs.append(out)

        if not outputs:
            B, T = r3_features.shape[:2]
            return torch.zeros(B, T, 0, device=r3_features.device)

        return torch.cat(outputs, dim=-1)
