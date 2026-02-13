"""Neurochemical types and state management."""

from __future__ import annotations

from enum import Enum, unique
from typing import Dict, List, Optional, Tuple

from torch import Tensor


@unique
class NeurochemicalType(Enum):
    DOPAMINE = "dopamine"
    OPIOID = "opioid"
    SEROTONIN = "serotonin"
    NOREPINEPHRINE = "norepinephrine"
    GABA = "gaba"
    GLUTAMATE = "glutamate"


class NeurochemicalState:
    """Storage for neurochemical signals keyed by (chemical, region)."""

    def __init__(self) -> None:
        self._state: Dict[Tuple[NeurochemicalType, str], Tensor] = {}

    def write(self, chemical: NeurochemicalType, region: str, value: Tensor) -> None:
        self._state[(chemical, region)] = value

    def read(self, chemical: NeurochemicalType, region: str) -> Optional[Tensor]:
        return self._state.get((chemical, region))

    def reset(self) -> None:
        self._state.clear()

    def keys(self) -> List[Tuple[NeurochemicalType, str]]:
        return list(self._state.keys())
