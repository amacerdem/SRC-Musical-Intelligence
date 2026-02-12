"""
RPUUnit -- Reward Processing Unit definition.

The RPU models how the brain computes reward signals from musical stimuli
-- dopamine dynamics, reward prediction error, information-uncertainty
coupling, and aesthetic computation.  Its primary neural circuit is
mesolimbic (ventral striatum, OFC, vmPFC), with pooled effect size d=0.70
from the C3 meta-analysis (Experimental-5, k < 10 studies).

9 models: DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, IOTMS, SSPS.
Total output: 94D per frame.

RPU is a *dependent* unit -- it receives cross-unit inputs from ARU and
SPU after the first-pass independent units have been computed.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_RPU_MODELS


class RPUUnit(BaseCognitiveUnit):
    """Reward Processing Unit -- DA dynamics, reward prediction, aesthetics."""

    UNIT_NAME = "RPU"
    FULL_NAME = "Reward Processing Unit"
    CIRCUIT = "mesolimbic"
    POOLED_EFFECT = 0.70

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_RPU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all RPU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Dict of named tensors from ARU and SPU
                routed via cross-unit pathways.

        Returns:
            (B, T, 94) concatenated output of all 9 RPU models.
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
