"""
STUUnit -- Sensorimotor Timing Unit definition.

The STU models how the brain encodes temporal structure in music -- beat,
metre, tempo, groove, and auditory-motor coupling.  Its primary neural
circuit is sensorimotor (SMA, Heschl's gyrus), with pooled effect size
d=0.67 from the C3 meta-analysis (Core-4, k >= 10 studies).

14 models: HMCE, AMSC, MDNS, AMSS, TPIO, EDTA, ETAM, HGSIC, OMS,
           TMRM, NEWMD, MTNE, PTGMP, MPFS.
Total output: 148D per frame.

STU is an *independent* unit in the first pass.  Some internal routing
occurs via pathways P2 (HMCE -> AMSC) and P4 (context hierarchy).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_STU_MODELS


class STUUnit(BaseCognitiveUnit):
    """Sensorimotor Timing Unit -- beat, metre, tempo, and groove."""

    UNIT_NAME = "STU"
    FULL_NAME = "Sensorimotor Timing Unit"
    CIRCUIT = "sensorimotor"
    POOLED_EFFECT = 0.67

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_STU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all STU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Optional dict for internal STU routing
                (pathways P2, P4).

        Returns:
            (B, T, 148) concatenated output of all 14 STU models.
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
