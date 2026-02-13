"""Neurochemical state management: 4 primary systems."""
from __future__ import annotations
from typing import Dict, List, Optional
from torch import Tensor
from ...contracts.neurochemical import NeurochemicalType, NeurochemicalState

class NeurochemicalStateManager:
    def __init__(self):
        self._da = NeurochemicalState()
        self._opioid = NeurochemicalState()
        self._serotonin = NeurochemicalState()
        self._ne = NeurochemicalState()
    def write_da(self, region, value): self._da.write(NeurochemicalType.DOPAMINE, region, value)
    def read_da(self, region): return self._da.read(NeurochemicalType.DOPAMINE, region)
    def write_opioid(self, region, value): self._opioid.write(NeurochemicalType.OPIOID, region, value)
    def read_opioid(self, region): return self._opioid.read(NeurochemicalType.OPIOID, region)
    def write_serotonin(self, region, value): self._serotonin.write(NeurochemicalType.SEROTONIN, region, value)
    def read_serotonin(self, region): return self._serotonin.read(NeurochemicalType.SEROTONIN, region)
    def write_ne(self, region, value): self._ne.write(NeurochemicalType.NOREPINEPHRINE, region, value)
    def read_ne(self, region): return self._ne.read(NeurochemicalType.NOREPINEPHRINE, region)
    def reset(self):
        self._da.reset(); self._opioid.reset(); self._serotonin.reset(); self._ne.reset()
    @property
    def all_signals(self) -> Dict[str, List[str]]:
        return {
            "dopamine": [str(k) for k in self._da.keys()],
            "opioid": [str(k) for k in self._opioid.keys()],
            "serotonin": [str(k) for k in self._serotonin.keys()],
            "norepinephrine": [str(k) for k in self._ne.keys()],
        }
