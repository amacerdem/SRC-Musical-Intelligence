"""CircuitRegistry -- lookup circuits by name or unit."""
from __future__ import annotations

from typing import Dict, List, Optional

from .definitions import CircuitDef, ALL_CIRCUITS


class CircuitRegistry:
    """Lookup circuits by name or unit.

    Indexes all six circuits (five operational + imagery) on construction.
    """

    def __init__(self) -> None:
        self._by_name: Dict[str, CircuitDef] = {c.name: c for c in ALL_CIRCUITS}
        self._by_unit: Dict[str, List[CircuitDef]] = {}
        for c in ALL_CIRCUITS:
            for u in c.units:
                self._by_unit.setdefault(u, []).append(c)

    # ── Lookups ──────────────────────────────────────────────────────

    def get_by_name(self, name: str) -> Optional[CircuitDef]:
        """Return the circuit with the given short name, or ``None``."""
        return self._by_name.get(name)

    def get_by_unit(self, unit: str) -> List[CircuitDef]:
        """Return all circuits that include *unit*."""
        return self._by_unit.get(unit, [])

    # ── Dunder ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"CircuitRegistry(circuits={len(self._by_name)})"
