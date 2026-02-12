"""
ARUUnit -- Affective Resonance Unit definition.

The ARU models how the human brain generates and processes musical emotion,
pleasure, and affective responses.  Its primary neural circuit is mesolimbic
(NAcc, VTA, Amygdala), with pooled effect size d=0.83 from the C3
meta-analysis (Core-4, k >= 10 studies).

10 models: SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR.
Total output: 120D per frame.

ARU is a *dependent* unit -- it receives cross-unit inputs from SPU, STU,
and IMU via pathways P1 (SPU->ARU), P3 (IMU->ARU), and P5 (STU->ARU).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_ARU_MODELS


class ARUUnit(BaseCognitiveUnit):
    """Affective Resonance Unit -- musical emotion and pleasure processing."""

    UNIT_NAME = "ARU"
    FULL_NAME = "Affective Resonance Unit"
    CIRCUIT = "mesolimbic"
    POOLED_EFFECT = 0.83

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_ARU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all ARU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Dict of named tensors from SPU, STU, and IMU
                via pathways P1, P3, P5.

        Returns:
            (B, T, 120) concatenated output of all 10 ARU models.
        """
        outputs: list[Tensor] = []
        for model in self.active_models:
            out = model.compute(
                mechanism_outputs={},
                h3_features=h3_features,
                r3_features=r3_features,
                cross_unit_inputs=cross_unit_inputs,
            )
            outputs.append(out)

        if not outputs:
            B, T = r3_features.shape[:2]
            return torch.zeros(B, T, 0, device=r3_features.device)

        return torch.cat(outputs, dim=-1)
