"""R3FeatureMap and R3GroupInfo -- Frozen read-only snapshots of the R3 registry.

R3GroupInfo stores metadata for a single registered spectral group (name,
dimension, start/end indices, and ordered feature names).

R3FeatureMap stores the complete frozen registry state: total dimensionality,
all group infos, and per-feature R3FeatureSpec entries.  Both are frozen
dataclasses -- once created they cannot be modified.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional, Tuple

from ....contracts.dataclasses.feature_spec import R3FeatureSpec


# ======================================================================
# R3GroupInfo
# ======================================================================

@dataclass(frozen=True)
class R3GroupInfo:
    """Metadata for a registered R3 spectral group.

    Attributes:
        name:          GROUP_NAME of the group (e.g. ``"consonance"``).
        dim:           OUTPUT_DIM -- number of features this group produces.
        start:         Start index in the R3 feature vector (inclusive).
        end:           End index in the R3 feature vector (exclusive).
        feature_names: Ordered tuple of feature names for this group.

    Invariant:
        ``end - start == dim == len(feature_names)``
    """

    name: str
    dim: int
    start: int
    end: int
    feature_names: Tuple[str, ...]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if self.end - self.start != self.dim:
            raise ValueError(
                f"R3GroupInfo {self.name!r}: end - start "
                f"({self.end - self.start}) != dim ({self.dim})"
            )
        if len(self.feature_names) != self.dim:
            raise ValueError(
                f"R3GroupInfo {self.name!r}: len(feature_names) "
                f"({len(self.feature_names)}) != dim ({self.dim})"
            )

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"R3GroupInfo(name={self.name!r}, "
            f"dim={self.dim}, "
            f"range=[{self.start}:{self.end}])"
        )


# ======================================================================
# R3FeatureMap
# ======================================================================

@dataclass(frozen=True)
class R3FeatureMap:
    """Frozen registry snapshot -- total dim + group metadata + feature specs.

    Produced by ``R3FeatureRegistry.freeze()``.  Once created, it is
    immutable and can be passed freely to downstream consumers.

    Attributes:
        total_dim:     Sum of all group dimensions.
        groups:        Per-group metadata in registration order.
        feature_specs: Per-feature R3FeatureSpec entries (one per dimension,
                       ordered by index).  Length equals ``total_dim``.
    """

    total_dim: int
    groups: Tuple[R3GroupInfo, ...]
    feature_specs: Tuple[R3FeatureSpec, ...] = ()

    # ------------------------------------------------------------------
    # Internal lookup caches (not part of the frozen state, built lazily)
    # We use __dict__ mutation on a frozen dataclass via object.__setattr__
    # for the internal caches.
    # ------------------------------------------------------------------

    def _ensure_caches(self) -> None:
        """Lazily build internal lookup dictionaries."""
        if "_group_by_name" not in self.__dict__:
            group_map: Dict[str, R3GroupInfo] = {}
            for g in self.groups:
                group_map[g.name] = g
            object.__setattr__(self, "_group_by_name", group_map)

            spec_map: Dict[int, R3FeatureSpec] = {}
            name_map: Dict[str, int] = {}
            for spec in self.feature_specs:
                spec_map[spec.index] = spec
                name_map[spec.name] = spec.index
            object.__setattr__(self, "_spec_by_index", spec_map)
            object.__setattr__(self, "_index_by_name", name_map)

    # ------------------------------------------------------------------
    # Public accessors
    # ------------------------------------------------------------------

    def get_group(self, name: str) -> R3GroupInfo:
        """Look up a group by its canonical name.

        Args:
            name: GROUP_NAME (e.g. ``"consonance"``, ``"energy"``).

        Returns:
            The corresponding ``R3GroupInfo``.

        Raises:
            KeyError: If no group with that name exists.
        """
        self._ensure_caches()
        group_map: Dict[str, R3GroupInfo] = self.__dict__["_group_by_name"]
        if name not in group_map:
            available = sorted(group_map.keys())
            raise KeyError(
                f"No group named {name!r}. "
                f"Available groups: {available}"
            )
        return group_map[name]

    def get_feature(self, index: int) -> R3FeatureSpec:
        """Look up a feature spec by its index in the R3 vector.

        Args:
            index: Feature index (``0 <= index < total_dim``).

        Returns:
            The corresponding ``R3FeatureSpec``.

        Raises:
            KeyError: If no feature at that index exists.
        """
        self._ensure_caches()
        spec_map: Dict[int, R3FeatureSpec] = self.__dict__["_spec_by_index"]
        if index not in spec_map:
            raise KeyError(
                f"No feature at index {index}. "
                f"Valid range: [0, {self.total_dim})"
            )
        return spec_map[index]

    def resolve(self, name: str) -> int:
        """Resolve a semantic feature name to its current numeric index.

        This is the primary API for C³ kernel code.  All R³ access should
        go through ``resolve()`` rather than hard-coding indices.

        Args:
            name: Canonical feature name (e.g. ``"roughness"``,
                  ``"onset_strength"``).

        Returns:
            The integer index in the R³ feature vector.

        Raises:
            KeyError: If *name* is not a known feature.
        """
        self._ensure_caches()
        name_map: Dict[str, int] = self.__dict__["_index_by_name"]
        if name not in name_map:
            raise KeyError(
                f"Unknown R³ feature {name!r}. "
                f"Known features: {sorted(name_map.keys())[:10]}..."
            )
        return name_map[name]

    def resolve_range(self, group: str) -> slice:
        """Resolve a group name to an index slice.

        Args:
            group: Canonical group name (e.g. ``"consonance"``, ``"energy"``).

        Returns:
            A ``slice(start, end)`` covering the group's indices.

        Raises:
            KeyError: If *group* is not a known group name.
        """
        info = self.get_group(group)
        return slice(info.start, info.end)

    def resolve_many(self, names: Tuple[str, ...]) -> Tuple[int, ...]:
        """Resolve multiple feature names to indices.

        Args:
            names: Tuple of canonical feature names.

        Returns:
            Tuple of integer indices in the same order.
        """
        return tuple(self.resolve(n) for n in names)

    # ------------------------------------------------------------------
    # Group exclusion (for ontology compliance)
    # ------------------------------------------------------------------

    @property
    def dissolved_groups(self) -> Tuple[str, ...]:
        """Groups dissolved from R³ per ontology v1.0.0.

        These groups still exist in code (128D output) but are
        ontologically excluded from C³ consumption.  C³ kernel code
        MUST NOT read features from these groups.
        """
        return ("interactions", "information")

    def is_dissolved(self, name: str) -> bool:
        """Check whether a feature belongs to a dissolved group.

        Works with both spec names (``"amp_x_roughness"``) and
        index-based lookup.
        """
        self._ensure_caches()
        name_map: Dict[str, int] = self.__dict__["_index_by_name"]
        if name in name_map:
            idx = name_map[name]
            spec = self.__dict__["_spec_by_index"][idx]
            return spec.group in self.dissolved_groups
        # Fallback: check all specs by name
        for spec in self.feature_specs:
            if spec.name == name:
                return spec.group in self.dissolved_groups
        raise KeyError(f"Unknown R³ feature {name!r}")

    def is_dissolved_index(self, index: int) -> bool:
        """Check whether a feature index belongs to a dissolved group."""
        self._ensure_caches()
        spec = self.__dict__["_spec_by_index"].get(index)
        if spec is None:
            raise KeyError(f"No feature at index {index}")
        return spec.group in self.dissolved_groups

    # ------------------------------------------------------------------
    # Convenience properties
    # ------------------------------------------------------------------

    @property
    def feature_names(self) -> Tuple[str, ...]:
        """All feature names in index order."""
        names = []
        for g in self.groups:
            names.extend(g.feature_names)
        return tuple(names)

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        lines = [f"R3FeatureMap(total_dim={self.total_dim}, groups=["]
        for g in self.groups:
            lines.append(f"  {g.name}: [{g.start}:{g.end}] ({g.dim}D)")
        lines.append("])")
        return "\n".join(lines)
