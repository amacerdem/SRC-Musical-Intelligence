"""
SpaceAssembler -- Dynamic MI-space layout and tensor assembly.

The MI-space is a flat vector:

    [cochlea(128D) | r3(49D) | brain(variable) | l3(variable)]

The brain section's size depends on which units and models are active.
SpaceLayout captures the range of every section at runtime.
SpaceAssembler builds the layout from a registry and concatenates
component tensors into the final MI-space vector.

Usage::

    from mi_beta.core.registry import ModelRegistry
    from mi_beta.core.config import MI_BETA_CONFIG
    from mi_beta.core.space_assembler import SpaceAssembler

    registry = ModelRegistry()
    registry.scan()

    assembler = SpaceAssembler(registry, MI_BETA_CONFIG)
    layout = assembler.layout()
    print(f"MI-space: {layout.total_dim}D")
    print(f"  Brain: {layout.brain_range} ({layout.brain_dim}D)")

    mi_space = assembler.assemble(cochlea_tensor, r3_tensor, brain_tensor, l3_tensor)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from .constants import N_MELS, R3_DIM, UNIT_EXECUTION_ORDER


# =====================================================================
# SPACE LAYOUT -- Immutable snapshot of the MI-space geometry
# =====================================================================

@dataclass(frozen=True)
class SpaceLayout:
    """Immutable description of the MI-space geometry.

    All ranges are half-open intervals [start, end).

    Attributes:
        cochlea_range: Range of the cochlea (mel) section.  Always (0, 128).
        r3_range: Range of the R3 spectral section.
        brain_range: Range of the brain section.
        l3_range: Range of the L3 language section (if present).
        total_dim: Total dimensionality of the MI-space vector.
        unit_ranges: Per-unit ranges within the brain section
                     (relative to the BRAIN start, not MI-space start).
        model_ranges: Per-model ranges within the brain section
                      (relative to the BRAIN start). Keys are "UNIT/MODEL".
    """

    cochlea_range: Tuple[int, int]
    r3_range: Tuple[int, int]
    brain_range: Tuple[int, int]
    l3_range: Optional[Tuple[int, int]]
    total_dim: int

    # Per-unit ranges within brain (offsets relative to brain_range[0])
    unit_ranges: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    # Per-model ranges within brain (offsets relative to brain_range[0])
    # Key format: "UNIT/MODEL" e.g. "ARU/PUPF"
    model_ranges: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    # ── Derived properties ─────────────────────────────────────────────

    @property
    def cochlea_dim(self) -> int:
        return self.cochlea_range[1] - self.cochlea_range[0]

    @property
    def r3_dim(self) -> int:
        return self.r3_range[1] - self.r3_range[0]

    @property
    def brain_dim(self) -> int:
        return self.brain_range[1] - self.brain_range[0]

    @property
    def l3_dim(self) -> int:
        if self.l3_range is None:
            return 0
        return self.l3_range[1] - self.l3_range[0]

    @property
    def n_units(self) -> int:
        return len(self.unit_ranges)

    @property
    def n_models(self) -> int:
        return len(self.model_ranges)

    def global_unit_range(self, unit_name: str) -> Tuple[int, int]:
        """Get a unit's range in the full MI-space (not relative to brain).

        Args:
            unit_name: e.g. "ARU"

        Returns:
            (start, end) in MI-space coordinates.

        Raises:
            KeyError: If unit not in layout.
        """
        brain_start = self.brain_range[0]
        local_s, local_e = self.unit_ranges[unit_name]
        return (brain_start + local_s, brain_start + local_e)

    def global_model_range(self, key: str) -> Tuple[int, int]:
        """Get a model's range in the full MI-space.

        Args:
            key: "UNIT/MODEL" format, e.g. "ARU/PUPF"

        Returns:
            (start, end) in MI-space coordinates.

        Raises:
            KeyError: If model key not in layout.
        """
        brain_start = self.brain_range[0]
        local_s, local_e = self.model_ranges[key]
        return (brain_start + local_s, brain_start + local_e)

    def __repr__(self) -> str:
        parts = [
            f"cochlea={self.cochlea_range}({self.cochlea_dim}D)",
            f"r3={self.r3_range}({self.r3_dim}D)",
            f"brain={self.brain_range}({self.brain_dim}D)",
        ]
        if self.l3_range is not None:
            parts.append(f"l3={self.l3_range}({self.l3_dim}D)")
        units_str = ", ".join(
            f"{name}:{e - s}D"
            for name, (s, e) in sorted(self.unit_ranges.items())
        )
        return (
            f"SpaceLayout(total={self.total_dim}D, "
            f"{', '.join(parts)}, "
            f"units=[{units_str}])"
        )


# =====================================================================
# SPACE ASSEMBLER -- Builds layout and concatenates tensors
# =====================================================================

class SpaceAssembler:
    """Builds the dynamic MI-space layout from a registry and assembles
    component tensors into the final vector.

    The assembler computes the layout once from the registry state and
    caches it.  If the registry changes (models enabled/disabled), call
    ``invalidate()`` to force a recompute.
    """

    def __init__(
        self,
        registry: "ModelRegistry",
        config: "MIBetaConfig",
        l3_dim: int = 0,
    ) -> None:
        """
        Args:
            registry: A scanned ModelRegistry.
            config: Pipeline configuration.
            l3_dim: Total L3 output dimensionality (0 if L3 is not active).
        """
        self._registry = registry
        self._config = config
        self._l3_dim = l3_dim
        self._layout: Optional[SpaceLayout] = None

    def invalidate(self) -> None:
        """Force recomputation of the layout on next access."""
        self._layout = None

    def set_l3_dim(self, l3_dim: int) -> None:
        """Update the L3 dimensionality (e.g. after L3 models are resolved)."""
        if l3_dim != self._l3_dim:
            self._l3_dim = l3_dim
            self._layout = None

    # ── Layout computation ─────────────────────────────────────────────

    def layout(self) -> SpaceLayout:
        """Compute (or return cached) MI-space layout.

        The layout is deterministic: units appear in UNIT_EXECUTION_ORDER,
        and models within each unit are sorted alphabetically by name.

        Returns:
            SpaceLayout describing every section's range.
        """
        if self._layout is not None:
            return self._layout

        # Fixed sections
        cochlea_start = 0
        cochlea_end = cochlea_start + N_MELS       # 128
        r3_start = cochlea_end
        r3_end = r3_start + R3_DIM                  # 177

        # Brain section -- iterate units in execution order
        brain_offset = 0
        unit_ranges: Dict[str, Tuple[int, int]] = {}
        model_ranges: Dict[str, Tuple[int, int]] = {}

        for unit_name in UNIT_EXECUTION_ORDER:
            if not self._config.is_unit_active(unit_name):
                continue

            unit_start = brain_offset
            models = self._registry.get_models_by_unit(unit_name)

            # Filter by active_models config
            active = [
                m for m in models
                if self._config.is_model_active(m.NAME)
            ]

            for model in active:
                model_start = brain_offset
                model_end = brain_offset + model.OUTPUT_DIM
                model_ranges[f"{unit_name}/{model.NAME}"] = (model_start, model_end)
                brain_offset = model_end

            unit_end = brain_offset
            if unit_end > unit_start:
                unit_ranges[unit_name] = (unit_start, unit_end)

        brain_start = r3_end
        brain_end = brain_start + brain_offset

        # L3 section
        if self._l3_dim > 0:
            l3_start = brain_end
            l3_end = l3_start + self._l3_dim
            l3_range: Optional[Tuple[int, int]] = (l3_start, l3_end)
            total = l3_end
        else:
            l3_range = None
            total = brain_end

        self._layout = SpaceLayout(
            cochlea_range=(cochlea_start, cochlea_end),
            r3_range=(r3_start, r3_end),
            brain_range=(brain_start, brain_end),
            l3_range=l3_range,
            total_dim=total,
            unit_ranges=unit_ranges,
            model_ranges=model_ranges,
        )
        return self._layout

    # ── Tensor assembly ────────────────────────────────────────────────

    def assemble(
        self,
        cochlea: Tensor,
        r3: Tensor,
        brain: Tensor,
        l3: Optional[Tensor] = None,
    ) -> Tensor:
        """Concatenate component tensors into the MI-space vector.

        Args:
            cochlea: (B, T, 128) mel spectrogram (transposed to B,T,D).
            r3: (B, T, 49) R3 spectral features.
            brain: (B, T, brain_dim) brain output.
            l3: (B, T, l3_dim) L3 output, or None.

        Returns:
            (B, T, total_dim) MI-space vector.

        Raises:
            ValueError: If tensor dimensions do not match the layout.
        """
        lay = self.layout()

        # Validate dimensions
        if cochlea.shape[-1] != lay.cochlea_dim:
            raise ValueError(
                f"Cochlea dim mismatch: got {cochlea.shape[-1]}, "
                f"expected {lay.cochlea_dim}"
            )
        if r3.shape[-1] != lay.r3_dim:
            raise ValueError(
                f"R3 dim mismatch: got {r3.shape[-1]}, "
                f"expected {lay.r3_dim}"
            )
        if brain.shape[-1] != lay.brain_dim:
            raise ValueError(
                f"Brain dim mismatch: got {brain.shape[-1]}, "
                f"expected {lay.brain_dim}"
            )

        parts = [cochlea, r3, brain]

        if l3 is not None:
            if lay.l3_range is None:
                raise ValueError(
                    "L3 tensor provided but layout has no L3 range "
                    "(l3_dim was 0 at layout time)"
                )
            if l3.shape[-1] != lay.l3_dim:
                raise ValueError(
                    f"L3 dim mismatch: got {l3.shape[-1]}, "
                    f"expected {lay.l3_dim}"
                )
            parts.append(l3)
        elif lay.l3_range is not None:
            raise ValueError(
                "Layout expects L3 output but no l3 tensor provided"
            )

        return torch.cat(parts, dim=-1)

    def assemble_brain(
        self,
        unit_tensors: Dict[str, Tensor],
    ) -> Tensor:
        """Assemble the brain tensor from per-unit outputs.

        Units are concatenated in UNIT_EXECUTION_ORDER.

        Args:
            unit_tensors: Mapping of unit_name -> (B, T, unit_dim) tensor.

        Returns:
            (B, T, brain_dim) concatenated brain tensor.

        Raises:
            ValueError: If a required active unit is missing or has wrong dim.
        """
        lay = self.layout()
        parts: List[Tensor] = []

        for unit_name in UNIT_EXECUTION_ORDER:
            if unit_name not in lay.unit_ranges:
                continue
            if unit_name not in unit_tensors:
                raise ValueError(
                    f"Missing tensor for active unit {unit_name!r}"
                )
            expected_dim = lay.unit_ranges[unit_name][1] - lay.unit_ranges[unit_name][0]
            actual_dim = unit_tensors[unit_name].shape[-1]
            if actual_dim != expected_dim:
                raise ValueError(
                    f"Unit {unit_name!r} dim mismatch: "
                    f"got {actual_dim}, expected {expected_dim}"
                )
            parts.append(unit_tensors[unit_name])

        if not parts:
            # No active units -- return empty brain tensor
            sample = next(iter(unit_tensors.values()), None)
            if sample is not None:
                B, T = sample.shape[0], sample.shape[1]
                return torch.zeros(B, T, 0, device=sample.device, dtype=sample.dtype)
            return torch.zeros(1, 1, 0)

        return torch.cat(parts, dim=-1)

    def __repr__(self) -> str:
        lay = self.layout()
        return f"SpaceAssembler(total_dim={lay.total_dim})"
