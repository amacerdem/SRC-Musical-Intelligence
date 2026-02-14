"""NeurochemicalRegistry -- lookup neurochemicals by name or abbreviation."""
from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .dopamine import Neurochemical, DOPAMINE
from .opioid import OPIOID
from .serotonin import SEROTONIN
from .norepinephrine import NOREPINEPHRINE

ALL_NEUROCHEMICALS: Tuple[Neurochemical, ...] = (
    DOPAMINE,
    OPIOID,
    SEROTONIN,
    NOREPINEPHRINE,
)
"""All four neurochemical systems."""


class NeurochemicalRegistry:
    """Lookup neurochemicals by name or abbreviation.

    Indexes all four neurochemical systems on construction.
    """

    def __init__(self) -> None:
        self._by_name: Dict[str, Neurochemical] = {
            n.name: n for n in ALL_NEUROCHEMICALS
        }
        self._by_abbr: Dict[str, Neurochemical] = {
            n.abbreviation: n for n in ALL_NEUROCHEMICALS
        }
        self._all = ALL_NEUROCHEMICALS

    # ── Lookups ──────────────────────────────────────────────────────

    def get_by_name(self, name: str) -> Optional[Neurochemical]:
        """Return the neurochemical with the given full name, or ``None``."""
        return self._by_name.get(name)

    def get_by_abbreviation(self, abbr: str) -> Optional[Neurochemical]:
        """Return the neurochemical with the given abbreviation, or ``None``."""
        return self._by_abbr.get(abbr)

    # ── Properties ───────────────────────────────────────────────────

    @property
    def all_neurochemicals(self) -> Tuple[Neurochemical, ...]:
        """All registered neurochemical systems."""
        return self._all

    # ── Dunder ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        return f"NeurochemicalRegistry(neurochemicals={len(self._all)})"
