"""
ModelRegistry -- Auto-discovers and indexes all brain model implementations.

The registry scans ``mi_beta.brain.units`` (or any specified package) for
concrete implementations of BaseModel, BaseMechanism, and BaseCognitiveUnit.
It provides lookup by name, unit, tier, and produces the aggregate H3 demand
set that the ear/H3 subsystem must satisfy.

Usage::

    from mi_beta.core.registry import ModelRegistry

    registry = ModelRegistry()
    registry.scan()  # discovers all @register-decorated or BaseModel subclasses

    # Query
    model = registry.get_model("PUPF")
    aru_models = registry.get_models_by_unit("ARU")
    beta_models = registry.get_models_by_tier("beta")

    # Demand
    demand = registry.get_total_demand()
    print(f"H3 must compute {len(demand)} unique 4-tuples")

Design decisions:
    - Auto-discovery via importlib walks the brain.units subpackages.
    - Models self-register by inheriting from BaseModel (detected via
      ``__init_subclass__`` or explicit ``importlib`` subclass scanning).
    - Active/inactive filtering respects MIBetaConfig.active_units and
      MIBetaConfig.active_models without mutating the model classes.
    - Thread-safe reads after scan() completes (scan is NOT thread-safe).
"""

from __future__ import annotations

import importlib
import logging
import pkgutil
from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
    Type,
)

from .constants import UNIT_EXECUTION_ORDER, MODEL_TIERS

logger = logging.getLogger(__name__)


# =====================================================================
# LIGHTWEIGHT PROTOCOL STUBS
# =====================================================================
#
# These are structural typing checks used when the full contracts
# package has not yet been loaded.  The registry does NOT require
# inheriting from these -- it checks for the protocol attributes.
#

def _is_model_class(cls: Type) -> bool:
    """Check if a class looks like a BaseModel implementation.

    Required class attributes:
        NAME: str
        UNIT: str
        TIER: str
        OUTPUT_DIM: int
        h3_demand: property or attribute returning demand specs
        compute: callable method
    """
    return (
        isinstance(cls, type)
        and hasattr(cls, "NAME")
        and hasattr(cls, "UNIT")
        and hasattr(cls, "TIER")
        and hasattr(cls, "OUTPUT_DIM")
        and hasattr(cls, "compute")
        and not getattr(cls, "__abstractmethods__", None)
    )


def _is_mechanism_class(cls: Type) -> bool:
    """Check if a class looks like a BaseMechanism implementation."""
    return (
        isinstance(cls, type)
        and hasattr(cls, "MECHANISM_NAME")
        and hasattr(cls, "OUTPUT_DIM")
        and hasattr(cls, "compute")
        and not getattr(cls, "__abstractmethods__", None)
    )


def _is_unit_class(cls: Type) -> bool:
    """Check if a class looks like a BaseCognitiveUnit implementation."""
    return (
        isinstance(cls, type)
        and hasattr(cls, "UNIT_NAME")
        and hasattr(cls, "CIRCUIT")
        and hasattr(cls, "execute")
        and not getattr(cls, "__abstractmethods__", None)
    )


# =====================================================================
# MODEL ENTRY -- Thin wrapper around a discovered model class
# =====================================================================

class _ModelEntry:
    """Internal wrapper holding a model class and its instantiated singleton."""

    __slots__ = ("cls", "instance", "name", "unit", "tier", "output_dim", "enabled")

    def __init__(self, cls: Type) -> None:
        self.cls = cls
        self.instance: Optional[Any] = None
        self.name: str = cls.NAME
        self.unit: str = cls.UNIT
        self.tier: str = cls.TIER
        self.output_dim: int = cls.OUTPUT_DIM
        self.enabled: bool = True

    def get_instance(self) -> Any:
        """Lazy-instantiate the model (zero-param constructor)."""
        if self.instance is None:
            self.instance = self.cls()
        return self.instance


# =====================================================================
# MODEL REGISTRY
# =====================================================================

class ModelRegistry:
    """Auto-discovers and indexes all BaseModel, BaseMechanism, and
    BaseCognitiveUnit implementations within the brain package.

    After ``scan()``, provides fast lookup by name, unit, tier, and
    computes the aggregate H3 demand set.
    """

    def __init__(self) -> None:
        # Primary index: model_name -> _ModelEntry
        self._models: Dict[str, _ModelEntry] = {}

        # Mechanism classes discovered (name -> class)
        self._mechanisms: Dict[str, Type] = {}

        # Cognitive unit classes discovered (unit_name -> class)
        self._units: Dict[str, Type] = {}

        # Secondary indices (built after scan)
        self._by_unit: Dict[str, List[_ModelEntry]] = {}
        self._by_tier: Dict[str, List[_ModelEntry]] = {}

        self._scanned: bool = False

    # ── Discovery ──────────────────────────────────────────────────────

    def scan(self, package: str = "mi_beta.brain") -> None:
        """Walk the package tree and discover all model/mechanism/unit classes.

        This recursively imports all modules under the given package and
        inspects every class defined in them.  Classes that satisfy the
        BaseModel, BaseMechanism, or BaseCognitiveUnit protocol are
        registered automatically.

        Args:
            package: Dotted package path to scan (default: ``mi_beta.brain``).

        Raises:
            ImportError: If the package cannot be found.
        """
        self._models.clear()
        self._mechanisms.clear()
        self._units.clear()
        self._by_unit.clear()
        self._by_tier.clear()

        root = importlib.import_module(package)
        root_path = getattr(root, "__path__", None)
        if root_path is None:
            logger.warning("Package %s has no __path__; scanning module only", package)
            self._inspect_module(root)
        else:
            self._walk_package(package, root_path)

        # Build secondary indices
        self._rebuild_indices()
        self._scanned = True

        logger.info(
            "ModelRegistry: discovered %d models, %d mechanisms, %d units",
            len(self._models),
            len(self._mechanisms),
            len(self._units),
        )

    def _walk_package(self, package: str, path: list) -> None:
        """Recursively walk a package tree, importing each module."""
        for importer, module_name, is_pkg in pkgutil.walk_packages(
            path, prefix=package + "."
        ):
            try:
                mod = importlib.import_module(module_name)
                self._inspect_module(mod)
            except Exception as exc:
                logger.warning(
                    "ModelRegistry: failed to import %s: %s", module_name, exc
                )

    def _inspect_module(self, module: Any) -> None:
        """Inspect all classes in a module and register matching ones."""
        for attr_name in dir(module):
            obj = getattr(module, attr_name, None)
            if obj is None or not isinstance(obj, type):
                continue
            # Skip classes imported from other packages
            if getattr(obj, "__module__", None) != module.__name__:
                continue

            if _is_model_class(obj):
                self._register_model(obj)
            if _is_mechanism_class(obj):
                self._register_mechanism(obj)
            if _is_unit_class(obj):
                self._register_unit(obj)

    def _register_model(self, cls: Type) -> None:
        """Register a single model class."""
        name = cls.NAME
        if name in self._models:
            existing = self._models[name].cls
            if existing is not cls:
                logger.warning(
                    "ModelRegistry: duplicate model name %r -- "
                    "%s.%s overrides %s.%s",
                    name,
                    cls.__module__, cls.__qualname__,
                    existing.__module__, existing.__qualname__,
                )
        self._models[name] = _ModelEntry(cls)

    def _register_mechanism(self, cls: Type) -> None:
        """Register a single mechanism class."""
        name = cls.MECHANISM_NAME
        self._mechanisms[name] = cls

    def _register_unit(self, cls: Type) -> None:
        """Register a single cognitive unit class."""
        name = cls.UNIT_NAME
        self._units[name] = cls

    def _rebuild_indices(self) -> None:
        """Build secondary lookup indices from the primary model dict."""
        self._by_unit.clear()
        self._by_tier.clear()
        for entry in self._models.values():
            self._by_unit.setdefault(entry.unit, []).append(entry)
            self._by_tier.setdefault(entry.tier, []).append(entry)
        # Sort each list by model name for deterministic ordering
        for lst in self._by_unit.values():
            lst.sort(key=lambda e: e.name)
        for lst in self._by_tier.values():
            lst.sort(key=lambda e: e.name)

    # ── Registration (manual) ──────────────────────────────────────────

    def register_model(self, cls: Type) -> None:
        """Manually register a model class (useful for testing).

        Args:
            cls: A class that satisfies the BaseModel protocol.

        Raises:
            TypeError: If the class does not satisfy the protocol.
        """
        if not _is_model_class(cls):
            raise TypeError(
                f"{cls.__qualname__} does not satisfy the BaseModel protocol "
                f"(needs NAME, UNIT, TIER, OUTPUT_DIM, compute)"
            )
        self._register_model(cls)
        self._rebuild_indices()

    # ── Model Queries ──────────────────────────────────────────────────

    def get_model(self, name: str) -> Any:
        """Get a model instance by name.

        Args:
            name: Model name (e.g., "PUPF", "SRP", "BCH").

        Returns:
            The model instance.

        Raises:
            KeyError: If no model with that name is registered.
        """
        if name not in self._models:
            raise KeyError(
                f"Model {name!r} not found. "
                f"Known models: {sorted(self._models.keys())}"
            )
        return self._models[name].get_instance()

    def get_models_by_unit(self, unit: str) -> List[Any]:
        """Get all model instances belonging to a unit.

        Args:
            unit: Unit name (e.g., "ARU", "SPU").

        Returns:
            List of model instances, sorted by name.
        """
        entries = self._by_unit.get(unit, [])
        return [e.get_instance() for e in entries]

    def get_models_by_tier(self, tier: str) -> List[Any]:
        """Get all model instances at a specific evidence tier.

        Args:
            tier: One of "alpha", "beta", "gamma".

        Returns:
            List of model instances, sorted by name.
        """
        entries = self._by_tier.get(tier, [])
        return [e.get_instance() for e in entries]

    def all_models(self) -> List[Any]:
        """Get all registered model instances, sorted by name."""
        return [
            entry.get_instance()
            for entry in sorted(self._models.values(), key=lambda e: e.name)
        ]

    def all_model_names(self) -> List[str]:
        """Get all registered model names, sorted."""
        return sorted(self._models.keys())

    # ── Unit Queries ───────────────────────────────────────────────────

    def all_units(self) -> List[Any]:
        """Get all registered cognitive unit instances, sorted by name."""
        return [
            cls() for name, cls in sorted(self._units.items())
        ]

    def get_unit(self, unit_name: str) -> Any:
        """Get a cognitive unit instance by name.

        Raises:
            KeyError: If no unit with that name is registered.
        """
        if unit_name not in self._units:
            raise KeyError(
                f"Unit {unit_name!r} not found. "
                f"Known units: {sorted(self._units.keys())}"
            )
        return self._units[unit_name]()

    def get_unit_names(self) -> List[str]:
        """Get all registered unit names, sorted."""
        return sorted(self._units.keys())

    # ── Mechanism Queries ──────────────────────────────────────────────

    def all_mechanisms(self) -> List[Any]:
        """Get all registered mechanism instances, sorted by name."""
        return [
            cls() for name, cls in sorted(self._mechanisms.items())
        ]

    def get_mechanism_names(self) -> Set[str]:
        """Get the set of all registered mechanism names."""
        return set(self._mechanisms.keys())

    # ── Enable / Disable ───────────────────────────────────────────────

    def enable_model(self, name: str) -> None:
        """Enable a model for inclusion in active queries and demand.

        Args:
            name: Model name.

        Raises:
            KeyError: If model is not registered.
        """
        if name not in self._models:
            raise KeyError(f"Model {name!r} not found")
        self._models[name].enabled = True

    def disable_model(self, name: str) -> None:
        """Disable a model, excluding it from active queries and demand.

        Args:
            name: Model name.

        Raises:
            KeyError: If model is not registered.
        """
        if name not in self._models:
            raise KeyError(f"Model {name!r} not found")
        self._models[name].enabled = False

    def active_models(self) -> List[Any]:
        """Get all enabled model instances, sorted by name."""
        return [
            entry.get_instance()
            for entry in sorted(self._models.values(), key=lambda e: e.name)
            if entry.enabled
        ]

    def active_model_entries(self) -> List[_ModelEntry]:
        """Get all enabled model entries (internal, for demand/layout)."""
        return [
            entry for entry in sorted(self._models.values(), key=lambda e: e.name)
            if entry.enabled
        ]

    # ── Demand ─────────────────────────────────────────────────────────

    def get_total_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Compute the union of all H3 demands from active models.

        Returns:
            Set of (r3_idx, horizon, morph, law) 4-tuples that the H3
            engine must compute.
        """
        demand: Set[Tuple[int, int, int, int]] = set()
        for entry in self._models.values():
            if not entry.enabled:
                continue
            instance = entry.get_instance()
            # Support both h3_demand property and H3_DEMAND class attribute
            model_demand = getattr(instance, "h3_demand", None)
            if model_demand is None:
                model_demand = getattr(instance, "H3_DEMAND", ())
            # Handle demand specs (objects with .as_tuple())
            for item in model_demand:
                if isinstance(item, tuple) and len(item) == 4:
                    demand.add(item)
                elif hasattr(item, "as_tuple"):
                    demand.add(item.as_tuple())
                else:
                    logger.warning(
                        "ModelRegistry: unrecognised demand item from %s: %r",
                        entry.name, item,
                    )
        return demand

    def get_model_demand(self, name: str) -> Set[Tuple[int, int, int, int]]:
        """Get the H3 demand set for a single model.

        Args:
            name: Model name.

        Returns:
            Set of 4-tuples.

        Raises:
            KeyError: If model is not found.
        """
        if name not in self._models:
            raise KeyError(f"Model {name!r} not found")
        instance = self._models[name].get_instance()
        model_demand = getattr(instance, "h3_demand", None)
        if model_demand is None:
            model_demand = getattr(instance, "H3_DEMAND", ())
        result: Set[Tuple[int, int, int, int]] = set()
        for item in model_demand:
            if isinstance(item, tuple) and len(item) == 4:
                result.add(item)
            elif hasattr(item, "as_tuple"):
                result.add(item.as_tuple())
        return result

    # ── Introspection ──────────────────────────────────────────────────

    @property
    def is_scanned(self) -> bool:
        """True if scan() has been called at least once."""
        return self._scanned

    @property
    def model_count(self) -> int:
        """Total number of registered models."""
        return len(self._models)

    @property
    def active_model_count(self) -> int:
        """Number of currently enabled models."""
        return sum(1 for e in self._models.values() if e.enabled)

    @property
    def unit_count(self) -> int:
        """Number of registered cognitive units."""
        return len(self._units)

    @property
    def mechanism_count(self) -> int:
        """Number of registered mechanisms."""
        return len(self._mechanisms)

    def summary(self) -> Dict[str, Any]:
        """Return a summary dict for debugging / logging."""
        return {
            "scanned": self._scanned,
            "total_models": self.model_count,
            "active_models": self.active_model_count,
            "units": self.get_unit_names(),
            "mechanisms": sorted(self._mechanisms.keys()),
            "tiers": {
                tier: len(entries)
                for tier, entries in sorted(self._by_tier.items())
            },
            "units_with_models": {
                unit: [e.name for e in entries]
                for unit, entries in sorted(self._by_unit.items())
            },
            "total_demand": len(self.get_total_demand()),
        }

    def __repr__(self) -> str:
        status = "scanned" if self._scanned else "not scanned"
        return (
            f"ModelRegistry({status}, "
            f"models={self.model_count}, "
            f"active={self.active_model_count}, "
            f"units={self.unit_count}, "
            f"mechanisms={self.mechanism_count})"
        )
