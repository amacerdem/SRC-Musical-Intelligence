"""R3FeatureRegistry -- Mutable builder that freezes into an R3FeatureMap.

The registry follows a two-phase lifecycle:

    Phase 1 (MUTABLE):  ``register()`` collects BaseSpectralGroup instances.
    Phase 2 (FROZEN):   ``freeze()`` assigns contiguous INDEX_RANGE per group
                         and returns an immutable ``R3FeatureMap``.

After ``freeze()`` is called, ``register()`` raises ``RuntimeError``.
Calling ``freeze()`` multiple times is idempotent (returns the same map).
"""
from __future__ import annotations

from typing import List, Optional

from ....contracts.bases.base_spectral_group import BaseSpectralGroup
from ....contracts.dataclasses.feature_spec import R3FeatureSpec
from .feature_map import R3FeatureMap, R3GroupInfo


class R3FeatureRegistry:
    """Mutable registry that collects spectral groups and freezes into a map.

    Usage::

        registry = R3FeatureRegistry()
        registry.register(ConsonanceGroup())
        registry.register(EnergyGroup())
        ...
        feature_map = registry.freeze()

    After ``freeze()``, no further groups may be registered.
    """

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self) -> None:
        self._groups: List[BaseSpectralGroup] = []
        self._frozen: Optional[R3FeatureMap] = None

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, group: BaseSpectralGroup) -> None:
        """Add a spectral group to the registry.

        Groups are appended in order; index ranges are assigned at
        ``freeze()`` time.  Cannot register after ``freeze()``.

        Args:
            group: A ``BaseSpectralGroup`` instance to register.

        Raises:
            RuntimeError: If the registry has already been frozen.
            ValueError: If ``group.GROUP_NAME`` duplicates a previously
                registered group.
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

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def groups(self) -> List[BaseSpectralGroup]:
        """Registered groups (returns a copy of the internal list).

        Modifications to the returned list do not affect the registry.
        """
        return list(self._groups)

    @property
    def is_frozen(self) -> bool:
        """Whether the registry has been frozen."""
        return self._frozen is not None

    # ------------------------------------------------------------------
    # Freeze
    # ------------------------------------------------------------------

    def freeze(self) -> R3FeatureMap:
        """Finalize registry and assign contiguous index ranges.

        Iterates over registered groups in registration order, assigns
        each group a contiguous ``INDEX_RANGE = [offset, offset + dim)``,
        mutates the group's ``INDEX_RANGE`` attribute in-place, and
        creates a frozen ``R3FeatureMap`` with per-group ``R3GroupInfo``
        entries and per-feature ``R3FeatureSpec`` entries.

        Returns:
            ``R3FeatureMap`` with ``total_dim`` and per-group metadata.

        Note:
            Calling ``freeze()`` multiple times is idempotent -- the same
            cached ``R3FeatureMap`` is returned on subsequent calls.
        """
        if self._frozen is not None:
            return self._frozen

        offset = 0
        group_infos: List[R3GroupInfo] = []
        feature_specs: List[R3FeatureSpec] = []

        for group in self._groups:
            dim = group.OUTPUT_DIM
            names = tuple(group.feature_names)

            info = R3GroupInfo(
                name=group.GROUP_NAME,
                dim=dim,
                start=offset,
                end=offset + dim,
                feature_names=names,
            )

            # Update the group's INDEX_RANGE to reflect its assigned position
            group.INDEX_RANGE = (offset, offset + dim)

            # Create R3FeatureSpec entries for each feature in this group
            for i, name in enumerate(names):
                feature_specs.append(
                    R3FeatureSpec(
                        name=name,
                        group=group.GROUP_NAME,
                        index=offset + i,
                        description="",
                        citation="",
                    )
                )

            group_infos.append(info)
            offset += dim

        self._frozen = R3FeatureMap(
            total_dim=offset,
            groups=tuple(group_infos),
            feature_specs=tuple(feature_specs),
        )
        return self._frozen

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        state = "frozen" if self._frozen is not None else "mutable"
        n = len(self._groups)
        return f"R3FeatureRegistry(state={state}, groups={n})"
