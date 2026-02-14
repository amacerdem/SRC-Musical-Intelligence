"""MechanismRunner -- Compute all mechanisms once, cache for model reuse."""
from __future__ import annotations

from typing import Dict, Set, Tuple

from torch import Tensor

from .ppc import PPC
from .tpc import TPC
from .bep import BEP
from .asa import ASA
from .tmh import TMH
from .mem import MEM
from .syn import SYN
from .aed import AED
from .cpd import CPD
from .c0p import C0P


class MechanismRunner:
    """Compute all required mechanisms once, cache for model reuse.

    Usage::

        runner = MechanismRunner()
        runner.run(h3_features, r3_features)   # compute all 10 mechanisms
        bep_out = runner.get("BEP")            # (B, T, 30)
        asa_out = runner.get("ASA")            # (B, T, 30)
        runner.clear()                         # free memory
    """

    def __init__(self) -> None:
        self._mechanisms = {
            "PPC": PPC(),
            "TPC": TPC(),
            "BEP": BEP(),
            "ASA": ASA(),
            "TMH": TMH(),
            "MEM": MEM(),
            "SYN": SYN(),
            "AED": AED(),
            "CPD": CPD(),
            "C0P": C0P(),
        }
        self._cache: Dict[str, Tensor] = {}

    def run(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> None:
        """Compute all mechanisms and cache results."""
        self._cache.clear()
        for name, mech in self._mechanisms.items():
            self._cache[name] = mech.compute(h3_features, r3_features)

    def get(self, name: str) -> Tensor:
        """Return cached ``(B, T, 30)`` tensor.

        Raises:
            RuntimeError: If *name* has not been computed yet. Call
                :meth:`run` first.
        """
        if name not in self._cache:
            raise RuntimeError(
                f"Mechanism {name!r} not cached. Call run() first."
            )
        return self._cache[name]

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Union of all mechanism demands."""
        demand: Set[Tuple[int, int, int, int]] = set()
        for mech in self._mechanisms.values():
            demand |= mech.h3_demand
        return demand

    def clear(self) -> None:
        """Free cached tensors."""
        self._cache.clear()
