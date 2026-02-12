"""
R3FeatureRegistry — Auto-discovery and registration for R3 spectral groups.

Manages the ordered collection of BaseSpectralGroup instances,
assigns index ranges, and produces a frozen R3FeatureMap for
downstream consumers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from ...contracts import BaseSpectralGroup


# ═══════════════════════════════════════════════════════════════════════
# FROZEN OUTPUT
# ═══════════════════════════════════════════════════════════════════════

@dataclass(frozen=True)
class R3GroupInfo:
    """Metadata for a registered R3 group."""
    name: str
    dim: int
    start: int
    end: int
    feature_names: Tuple[str, ...]


@dataclass(frozen=True)
class R3FeatureMap:
    """Frozen registry snapshot — total dim + group metadata."""
    total_dim: int
    groups: Tuple[R3GroupInfo, ...]

    def __repr__(self) -> str:
        lines = [f"R3FeatureMap(total_dim={self.total_dim}, groups=["]
        for g in self.groups:
            lines.append(f"  {g.name}: [{g.start}:{g.end}] ({g.dim}D)")
        lines.append("])")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════
# MUTABLE REGISTRY
# ═══════════════════════════════════════════════════════════════════════

class R3FeatureRegistry:
    """Collects BaseSpectralGroup instances and assigns index ranges.

    Usage:
        registry = R3FeatureRegistry()
        registry.register(ConsonanceGroup())
        registry.register(EnergyGroup())
        ...
        feature_map = registry.freeze()
    """

    def __init__(self) -> None:
        self._groups: List[BaseSpectralGroup] = []
        self._frozen: Optional[R3FeatureMap] = None

    def register(self, group: BaseSpectralGroup) -> None:
        """Add a spectral group to the registry.

        Groups are appended in order; index ranges are assigned at freeze().
        Cannot register after freeze().
        """
        if self._frozen is not None:
            raise RuntimeError(
                "Cannot register groups after freeze(). "
                "Create a new R3FeatureRegistry if you need to modify."
            )
        # Check for duplicate group names
        for existing in self._groups:
            if existing.GROUP_NAME == group.GROUP_NAME:
                raise ValueError(
                    f"Duplicate group name: {group.GROUP_NAME!r}. "
                    f"Each group must have a unique GROUP_NAME."
                )
        self._groups.append(group)

    @property
    def groups(self) -> List[BaseSpectralGroup]:
        """Registered groups (mutable list)."""
        return list(self._groups)

    def freeze(self) -> R3FeatureMap:
        """Finalize registry and assign contiguous index ranges.

        Returns:
            R3FeatureMap with total_dim and per-group metadata.
        """
        if self._frozen is not None:
            return self._frozen

        offset = 0
        group_infos: List[R3GroupInfo] = []

        for group in self._groups:
            dim = group.OUTPUT_DIM
            info = R3GroupInfo(
                name=group.GROUP_NAME,
                dim=dim,
                start=offset,
                end=offset + dim,
                feature_names=tuple(group.feature_names),
            )
            # Update the group's INDEX_RANGE to reflect its assigned position
            group.INDEX_RANGE = (offset, offset + dim)
            group_infos.append(info)
            offset += dim

        self._frozen = R3FeatureMap(
            total_dim=offset,
            groups=tuple(group_infos),
        )
        return self._frozen
