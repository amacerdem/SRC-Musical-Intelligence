"""ModelRegistry: auto-discovers all BaseModel subclasses."""

from __future__ import annotations

import importlib
import pkgutil
from typing import Dict, List, Optional, Set, Tuple, Type


class ModelRegistry:
    """Discovers and indexes all cognitive model classes."""

    def __init__(self) -> None:
        self._models: Dict[str, object] = {}       # name → instance
        self._by_unit: Dict[str, List[object]] = {} # unit → [instances]
        self._discovered = False

    def discover(self) -> None:
        """Auto-discover all BaseModel subclasses from brain.units.*."""
        if self._discovered:
            return

        from mi_beta.contracts.base_model import BaseModel

        # Import all unit model packages
        import mi_beta.brain.units as units_pkg
        for importer, modname, ispkg in pkgutil.walk_packages(
            units_pkg.__path__, prefix=units_pkg.__name__ + "."
        ):
            try:
                importlib.import_module(modname)
            except Exception:
                pass

        # Collect all subclasses
        for cls in BaseModel.__subclasses__():
            if cls.NAME:
                instance = cls()
                self._models[cls.NAME] = instance
                unit = cls.UNIT
                if unit not in self._by_unit:
                    self._by_unit[unit] = []
                self._by_unit[unit].append(instance)

        self._discovered = True

    def get_model(self, name: str) -> object:
        self.discover()
        return self._models[name]

    def get_unit_models(self, unit_name: str) -> List[object]:
        self.discover()
        return self._by_unit.get(unit_name, [])

    def all_models(self) -> Dict[str, object]:
        self.discover()
        return dict(self._models)

    def all_h3_demands(self) -> Set[Tuple[int, int, int, int]]:
        """Union of all models' h3_demand tuples."""
        self.discover()
        demands: Set[Tuple[int, int, int, int]] = set()
        for model in self._models.values():
            demands.update(model.h3_demand_tuples())
        return demands

    @property
    def model_count(self) -> int:
        self.discover()
        return len(self._models)
