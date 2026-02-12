"""
DimensionMap -- Runtime dimension index tracking across the full MI-space.

Maps every named dimension (e.g. "arousal", "da_nacc", "consonance_level")
to its global index in the assembled MI-space vector, and provides range
queries by model name and unit name.

The DimensionMap is constructed from a SpaceLayout and the ModelRegistry,
combining:
  - Fixed cochlea dimension names (mel_0 .. mel_127)
  - Fixed R3 feature names (from R3Output.feature_names)
  - Dynamic brain dimension names (from each model's DIMENSION_NAMES)
  - Dynamic L3 dimension names (from each semantic group)

Usage::

    from mi_beta.core.dimension_map import DimensionMap

    dim_map = DimensionMap(registry, assembler)

    # Global index of a dimension
    idx = dim_map.index_of("da_nacc")

    # Range of a model in MI-space
    start, end = dim_map.range_of("PUPF")

    # Range of a unit in MI-space
    start, end = dim_map.range_of_unit("ARU")

    # All names
    print(dim_map.all_names())
    print(f"Total: {dim_map.total_dim}")
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .constants import N_MELS, R3_DIM, UNIT_EXECUTION_ORDER


# Default R3 feature names -- matches the canonical 49D R3 vector
_R3_FEATURE_NAMES: Tuple[str, ...] = (
    # Group A: Consonance (7D)
    "perfect_fifth_ratio", "euler_gradus", "harmonicity",
    "stumpf_fusion", "sensory_pleasantness", "roughness_total", "consonance_mean",
    # Group B: Energy (5D)
    "velocity_A", "velocity_D", "loudness", "onset_strength", "rms_energy",
    # Group C: Timbre (9D)
    "warmth", "sharpness", "brightness_kuttruff",
    "brightness", "spectral_centroid", "spectral_bandwidth",
    "tristimulus1", "tristimulus2", "tristimulus3",
    # Group D: Change (4D)
    "spectral_flux", "spectral_flatness", "zero_crossing_rate", "tonalness",
    # Group E: Interactions (24D)
    "cons_x_energy", "cons_x_timbre", "cons_x_change",
    "energy_x_timbre", "energy_x_change", "timbre_x_change",
    "cons_x_energy_x_timbre", "cons_x_energy_x_change",
    "cons_x_timbre_x_change", "energy_x_timbre_x_change",
    "cons_x_energy_x_timbre_x_change",
    "cons_variance", "energy_variance", "timbre_variance", "change_variance",
    "consonance_delta", "energy_delta", "timbre_delta", "change_delta",
    "cons_energy_ratio", "cons_timbre_ratio", "energy_timbre_ratio",
    "harmonic_tension", "spectral_complexity",
)


class DimensionMap:
    """Maps dimension names to indices across the full MI-space.

    Built from a ModelRegistry and a SpaceAssembler (or SpaceLayout).
    Provides O(1) lookup by name and O(1) range queries by model/unit.
    """

    def __init__(
        self,
        registry: "ModelRegistry",
        assembler: "SpaceAssembler",
        r3_feature_names: Optional[Tuple[str, ...]] = None,
        l3_dimension_names: Optional[Tuple[str, ...]] = None,
    ) -> None:
        """Build the dimension map from registry and assembler.

        Args:
            registry: A scanned ModelRegistry.
            assembler: A SpaceAssembler (provides the layout).
            r3_feature_names: Override for R3 names (default: canonical 49D).
            l3_dimension_names: L3 dimension names if L3 is active.
        """
        self._registry = registry
        self._layout = assembler.layout()

        # Use provided or default R3 names
        r3_names = r3_feature_names if r3_feature_names is not None else _R3_FEATURE_NAMES
        if len(r3_names) != R3_DIM:
            raise ValueError(
                f"R3 feature names length {len(r3_names)} != R3_DIM {R3_DIM}"
            )

        # Build the complete ordered list of dimension names
        names: List[str] = []

        # 1. Cochlea dimensions: mel_0 .. mel_127
        for i in range(N_MELS):
            names.append(f"mel_{i}")

        # 2. R3 dimensions
        for rn in r3_names:
            names.append(f"r3_{rn}")

        # 3. Brain dimensions -- iterate units in execution order
        self._unit_global_ranges: Dict[str, Tuple[int, int]] = {}
        self._model_global_ranges: Dict[str, Tuple[int, int]] = {}

        brain_start = self._layout.brain_range[0]

        for unit_name in UNIT_EXECUTION_ORDER:
            if unit_name not in self._layout.unit_ranges:
                continue

            unit_local_s, unit_local_e = self._layout.unit_ranges[unit_name]
            unit_global_s = brain_start + unit_local_s
            unit_global_e = brain_start + unit_local_e
            self._unit_global_ranges[unit_name] = (unit_global_s, unit_global_e)

            # Get models for this unit (sorted alphabetically)
            models = registry.get_models_by_unit(unit_name)
            active = [
                m for m in models
                if assembler._config.is_model_active(m.NAME)
            ]

            for model in active:
                model_key = f"{unit_name}/{model.NAME}"
                if model_key in self._layout.model_ranges:
                    local_s, local_e = self._layout.model_ranges[model_key]
                    global_s = brain_start + local_s
                    global_e = brain_start + local_e
                    self._model_global_ranges[model.NAME] = (global_s, global_e)

                    # Get dimension names from the model
                    dim_names = getattr(model, "DIMENSION_NAMES", None)
                    if dim_names is None:
                        dim_names = getattr(model, "dimension_names", None)

                    if dim_names is not None and len(dim_names) == model.OUTPUT_DIM:
                        for dn in dim_names:
                            names.append(f"{unit_name.lower()}_{model.NAME.lower()}_{dn}")
                    else:
                        # Fallback: generate generic names
                        for i in range(model.OUTPUT_DIM):
                            names.append(
                                f"{unit_name.lower()}_{model.NAME.lower()}_d{i}"
                            )

        # 4. L3 dimensions
        if self._layout.l3_range is not None and l3_dimension_names is not None:
            expected_l3_dim = self._layout.l3_range[1] - self._layout.l3_range[0]
            if len(l3_dimension_names) != expected_l3_dim:
                raise ValueError(
                    f"L3 dimension names length {len(l3_dimension_names)} "
                    f"!= l3_dim {expected_l3_dim}"
                )
            for ln in l3_dimension_names:
                names.append(f"l3_{ln}")
        elif self._layout.l3_range is not None:
            # Generate generic L3 names
            l3_dim = self._layout.l3_range[1] - self._layout.l3_range[0]
            for i in range(l3_dim):
                names.append(f"l3_d{i}")

        # Validate total
        if len(names) != self._layout.total_dim:
            raise ValueError(
                f"DimensionMap built {len(names)} names but layout has "
                f"{self._layout.total_dim} dimensions"
            )

        self._names: Tuple[str, ...] = tuple(names)

        # Build reverse lookup: name -> index
        self._name_to_index: Dict[str, int] = {}
        for idx, name in enumerate(self._names):
            if name in self._name_to_index:
                # Duplicate name -- append index suffix
                deduped = f"{name}_{idx}"
                self._name_to_index[deduped] = idx
            else:
                self._name_to_index[name] = idx

    # ── Index queries ──────────────────────────────────────────────────

    def index_of(self, name: str) -> int:
        """Get the global MI-space index of a dimension by name.

        Args:
            name: Dimension name (e.g. "r3_stumpf_fusion", "aru_pupf_pleasure").

        Returns:
            Integer index into the MI-space vector.

        Raises:
            KeyError: If name is not found.
        """
        if name not in self._name_to_index:
            raise KeyError(
                f"Dimension {name!r} not found. "
                f"Use all_names() to see available dimensions."
            )
        return self._name_to_index[name]

    def indices_of(self, names: List[str]) -> List[int]:
        """Get global indices for multiple dimension names.

        Args:
            names: List of dimension names.

        Returns:
            List of integer indices, in the same order.
        """
        return [self.index_of(n) for n in names]

    # ── Range queries ──────────────────────────────────────────────────

    def range_of(self, model_name: str) -> Tuple[int, int]:
        """Get the global MI-space range of a model's output dimensions.

        Args:
            model_name: Model name (e.g. "PUPF", "SRP").

        Returns:
            (start, end) half-open interval in MI-space.

        Raises:
            KeyError: If model name is not found.
        """
        if model_name not in self._model_global_ranges:
            raise KeyError(
                f"Model {model_name!r} not found in dimension map. "
                f"Known models: {sorted(self._model_global_ranges.keys())}"
            )
        return self._model_global_ranges[model_name]

    def range_of_unit(self, unit_name: str) -> Tuple[int, int]:
        """Get the global MI-space range of a unit's output dimensions.

        Args:
            unit_name: Unit name (e.g. "ARU", "SPU").

        Returns:
            (start, end) half-open interval in MI-space.

        Raises:
            KeyError: If unit name is not found.
        """
        if unit_name not in self._unit_global_ranges:
            raise KeyError(
                f"Unit {unit_name!r} not found in dimension map. "
                f"Known units: {sorted(self._unit_global_ranges.keys())}"
            )
        return self._unit_global_ranges[unit_name]

    def range_of_section(self, section: str) -> Tuple[int, int]:
        """Get the range of a major section ("cochlea", "r3", "brain", "l3").

        Args:
            section: One of "cochlea", "r3", "brain", "l3".

        Returns:
            (start, end) half-open interval.

        Raises:
            KeyError: If section is unknown or not present.
        """
        if section == "cochlea":
            return self._layout.cochlea_range
        elif section == "r3":
            return self._layout.r3_range
        elif section == "brain":
            return self._layout.brain_range
        elif section == "l3":
            if self._layout.l3_range is None:
                raise KeyError("L3 section is not active in this layout")
            return self._layout.l3_range
        else:
            raise KeyError(
                f"Unknown section {section!r}. "
                f"Must be one of: cochlea, r3, brain, l3"
            )

    # ── Name queries ───────────────────────────────────────────────────

    def all_names(self) -> List[str]:
        """Return the ordered list of all dimension names.

        The list length equals ``total_dim``.
        """
        return list(self._names)

    def names_of_model(self, model_name: str) -> List[str]:
        """Get dimension names for a specific model.

        Args:
            model_name: Model name.

        Returns:
            List of dimension names for that model's output range.
        """
        s, e = self.range_of(model_name)
        return list(self._names[s:e])

    def names_of_unit(self, unit_name: str) -> List[str]:
        """Get dimension names for a specific unit.

        Args:
            unit_name: Unit name.

        Returns:
            List of dimension names for that unit's output range.
        """
        s, e = self.range_of_unit(unit_name)
        return list(self._names[s:e])

    def names_of_section(self, section: str) -> List[str]:
        """Get dimension names for a major section.

        Args:
            section: One of "cochlea", "r3", "brain", "l3".

        Returns:
            List of dimension names.
        """
        s, e = self.range_of_section(section)
        return list(self._names[s:e])

    # ── Introspection ──────────────────────────────────────────────────

    def total_dim(self) -> int:
        """Total dimensionality of the MI-space."""
        return self._layout.total_dim

    def has_dimension(self, name: str) -> bool:
        """Check whether a dimension name exists."""
        return name in self._name_to_index

    def search(self, pattern: str) -> List[Tuple[str, int]]:
        """Search for dimension names containing a substring.

        Args:
            pattern: Substring to search for (case-insensitive).

        Returns:
            List of (name, index) tuples matching the pattern.
        """
        pattern_lower = pattern.lower()
        return [
            (name, idx)
            for name, idx in self._name_to_index.items()
            if pattern_lower in name.lower()
        ]

    def __len__(self) -> int:
        return self._layout.total_dim

    def __contains__(self, name: str) -> bool:
        return self.has_dimension(name)

    def __repr__(self) -> str:
        return (
            f"DimensionMap(total={self.total_dim()}, "
            f"models={len(self._model_global_ranges)}, "
            f"units={len(self._unit_global_ranges)})"
        )
