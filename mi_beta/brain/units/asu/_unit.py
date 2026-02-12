"""
ASUUnit -- Auditory Salience Unit definition.

The ASU models how the brain detects and prioritises salient auditory events
-- sudden onsets, spectral deviance, interaural differences, and bottom-up
attention capture.  Its primary neural circuit is salience (anterior
insula, ACC), with pooled effect size d=0.60 from the C3 meta-analysis
(Experimental-5, k < 10 studies).

9 models: SNEM, IACM, CSG, BARM, STANM, AACM, PWSM, DGTP, SDL.
Total output: 94D per frame.

ASU is an *independent* unit -- it does not receive cross-unit inputs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_ASU_MODELS


class ASUUnit(BaseCognitiveUnit):
    """Auditory Salience Unit -- salience detection and attention capture."""

    UNIT_NAME = "ASU"
    FULL_NAME = "Auditory Salience Unit"
    CIRCUIT = "salience"
    POOLED_EFFECT = 0.60

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_ASU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all ASU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Unused by ASU (independent unit).

        Returns:
            (B, T, 94) concatenated output of all 9 ASU models.
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
