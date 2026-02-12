from __future__ import annotations
from typing import Dict
from torch import Tensor
from mi_beta.core.types import UnitOutput
from ._base_adapter import BaseModelSemanticAdapter


class NDUAdapter(BaseModelSemanticAdapter):
    UNIT_NAME = "NDU"

    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        return {"tensor": unit_output.tensor}
