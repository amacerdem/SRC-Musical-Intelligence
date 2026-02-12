"""
IMUUnit -- Integrative Memory Unit definition.

The IMU models how the brain stores, retrieves, and integrates musical
memories -- autobiographical associations, tonal schema, recognition, and
consolidation.  Its primary neural circuit is mnemonic (Hippocampus, mPFC),
with pooled effect size d=0.53 from the C3 meta-analysis (Core-4,
k >= 10 studies).

15 models: MEAMN, PNH, MMP, RASN, PMIM, OII, HCMC, RIRI, MSPBA,
           VRIAP, TPRD, CMAPCC, DMMS, CSSL, CDEM.
Total output: 159D per frame.

IMU is an *independent* unit -- it does not receive cross-unit inputs in
the first pass.  Its memory_state output feeds into ARU via pathway P3.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseModel, BaseCognitiveUnit

from .models import ALL_IMU_MODELS


class IMUUnit(BaseCognitiveUnit):
    """Integrative Memory Unit -- musical memory and schema processing."""

    UNIT_NAME = "IMU"
    FULL_NAME = "Integrative Memory Unit"
    CIRCUIT = "mnemonic"
    POOLED_EFFECT = 0.53

    def __init__(self) -> None:
        self._models: List[BaseModel] = [cls() for cls in ALL_IMU_MODELS]

    @property
    def models(self) -> List[BaseModel]:
        return self._models

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Run all IMU models and concatenate outputs.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Unused by IMU (independent unit).

        Returns:
            (B, T, 159) concatenated output of all 15 IMU models.
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
