"""MI-Space dimension name → global index mapping."""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

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
    """Maps every named dimension to its global index in MI-space."""

    def __init__(
        self,
        registry: Any = None,
        assembler: Any = None,
        r3_feature_names: Optional[Tuple[str, ...]] = None,
        l3_dimension_names: Optional[Tuple[str, ...]] = None,
    ) -> None:
        self._names: List[str] = []
        self._index: dict[str, int] = {}
        self._model_ranges: dict[str, Tuple[int, int]] = {}
        self._unit_ranges: dict[str, Tuple[int, int]] = {}
        self._section_ranges: dict[str, Tuple[int, int]] = {}

        r3_names = r3_feature_names or _R3_FEATURE_NAMES

        # Cochlea section: mel_0 .. mel_127
        cochlea_start = 0
        for i in range(128):
            name = f"mel_{i}"
            self._names.append(name)
            self._index[name] = cochlea_start + i
        self._section_ranges["cochlea"] = (0, 128)

        # R3 section
        r3_start = 128
        for i, rname in enumerate(r3_names):
            qname = f"r3_{rname}"
            self._names.append(qname)
            self._index[qname] = r3_start + i
        self._section_ranges["r3"] = (r3_start, r3_start + len(r3_names))

        # Brain section — populated later when BrainOutput is available
        brain_start = r3_start + len(r3_names)
        self._brain_start = brain_start

    def _register_brain(
        self,
        unit_ranges: dict[str, Tuple[int, int]],
        unit_outputs: Any,
        dimension_names: Tuple[str, ...],
    ) -> None:
        """Register brain dimensions after BrainOutput is computed."""
        offset = self._brain_start
        for i, dname in enumerate(dimension_names):
            self._names.append(dname)
            self._index[dname] = offset + i
        brain_end = offset + len(dimension_names)
        self._section_ranges["brain"] = (offset, brain_end)
        for unit_name, (us, ue) in unit_ranges.items():
            self._unit_ranges[unit_name] = (offset + us, offset + ue)

    # ── Index queries ──────────────────────────────────────────────────────

    def index_of(self, name: str) -> int:
        return self._index[name]

    def indices_of(self, names: List[str]) -> List[int]:
        return [self._index[n] for n in names]

    # ── Range queries ──────────────────────────────────────────────────────

    def range_of(self, model_name: str) -> Tuple[int, int]:
        return self._model_ranges[model_name]

    def range_of_unit(self, unit_name: str) -> Tuple[int, int]:
        return self._unit_ranges[unit_name]

    def range_of_section(self, section: str) -> Tuple[int, int]:
        return self._section_ranges[section]

    # ── Name queries ───────────────────────────────────────────────────────

    def all_names(self) -> List[str]:
        return list(self._names)

    def names_of_model(self, model_name: str) -> List[str]:
        s, e = self._model_ranges[model_name]
        return self._names[s:e]

    def names_of_unit(self, unit_name: str) -> List[str]:
        s, e = self._unit_ranges[unit_name]
        return self._names[s:e]

    def search(self, pattern: str) -> List[Tuple[str, int]]:
        """Substring search across all dimension names."""
        return [(n, i) for n, i in self._index.items() if pattern in n]
