"""Brain mechanisms: 10 shared neural processing mechanisms."""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from ...contracts.base_mechanism import BaseMechanism
from .ppc import PPCMechanism
from .tpc import TPCMechanism
from .bep import BEPMechanism
from .asa import ASAMechanism
from .aed import AEDMechanism
from .cpd import CPDMechanism
from .c0p import C0PMechanism
from .mem import MEMMechanism
from .syn import SYNMechanism
from .tmh import TMHMechanism

ALL_MECHANISM_CLASSES = {
    "PPC": PPCMechanism,
    "TPC": TPCMechanism,
    "BEP": BEPMechanism,
    "ASA": ASAMechanism,
    "AED": AEDMechanism,
    "CPD": CPDMechanism,
    "C0P": C0PMechanism,
    "MEM": MEMMechanism,
    "SYN": SYNMechanism,
    "TMH": TMHMechanism,
}


class MechanismRunner:
    """Runs a subset of mechanisms and caches their outputs."""

    def __init__(self, needed_mechanisms=None):
        self._mechanisms: Dict[str, BaseMechanism] = {}
        self._cache: Dict[str, Tensor] = {}
        if needed_mechanisms:
            for name in needed_mechanisms:
                if name in ALL_MECHANISM_CLASSES:
                    self._mechanisms[name] = ALL_MECHANISM_CLASSES[name]()

    def run(self, h3_features, r3_features):
        self._cache.clear()
        for name, mech in self._mechanisms.items():
            self._cache[name] = mech.compute(h3_features, r3_features)
        return dict(self._cache)
