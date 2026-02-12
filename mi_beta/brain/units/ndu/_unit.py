"""
NDUUnit -- Novelty Detection Unit definition.

The NDU models how the brain detects deviations from expected auditory
patterns -- mismatch negativity (MMN), spectral deviance, statistical
learning violations, and error correction.  Its primary neural circuit is
salience (bilateral temporal cortex, IFG), with pooled effect size d=0.55
from the C3 meta-analysis (Experimental-5, k < 10 studies).

9 models: MPG, SDD, EDNR, DSP_, CDMR, SLEE, SDDP, ONI, ECT.
Total output: 94D per frame.

NDU is an *independent* unit -- it does not receive cross-unit inputs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_NDU_MODELS


class NDUUnit(BaseCognitiveUnit):
    """Novelty Detection Unit -- mismatch, deviance, and prediction error."""

    UNIT_NAME = "NDU"
    FULL_NAME = "Novelty Detection Unit"
    CIRCUIT = "salience"
    POOLED_EFFECT = 0.55

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_NDU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all NDU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Unused by NDU (independent unit).

        Returns:
            (B, T, 94) concatenated output of all 9 NDU models.
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
