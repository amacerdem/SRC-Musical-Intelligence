"""Base adapter for mapping a unit's model outputs to L³ semantic space."""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from torch import Tensor
from mi_beta.core.types import UnitOutput, SemanticGroupOutput


class BaseModelSemanticAdapter(ABC):
    UNIT_NAME: str

    @abstractmethod
    def adapt(self, unit_output: UnitOutput) -> Dict[str, Tensor]:
        """Map unit output dimensions to semantic group inputs."""
