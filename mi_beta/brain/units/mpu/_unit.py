"""
MPUUnit -- Motor Planning Unit definition.

The MPU models how the brain plans and executes motor sequences during
musical performance -- predictive error optimisation, groove states,
dual-stream integration, and sensorimotor calibration.  Its primary neural
circuit is sensorimotor (premotor cortex, cerebellum, basal ganglia), with
pooled effect size d=0.62 from the C3 meta-analysis (Experimental-5,
k < 10 studies).

10 models: PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, NSCP, CTBB, STC.
Total output: 104D per frame.

MPU is an *independent* unit -- it does not receive cross-unit inputs.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_MPU_MODELS


class MPUUnit(BaseCognitiveUnit):
    """Motor Planning Unit -- motor sequencing, groove, and coordination."""

    UNIT_NAME = "MPU"
    FULL_NAME = "Motor Planning Unit"
    CIRCUIT = "sensorimotor"
    POOLED_EFFECT = 0.62

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_MPU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all MPU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Unused by MPU (independent unit).

        Returns:
            (B, T, 104) concatenated output of all 10 MPU models.
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
