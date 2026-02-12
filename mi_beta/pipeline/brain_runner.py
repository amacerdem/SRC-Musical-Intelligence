"""
BrainOrchestrator -- Sequences brain computation through five phases.

Phase 1: Mechanisms   -- Shared sub-computations cached for reuse
Phase 2: Independent  -- SPU, STU, IMU, ASU, NDU, MPU, PCU
Phase 3: Pathways     -- Route signals between units
Phase 4: Dependent    -- ARU, RPU (receive cross-unit inputs)
Phase 5: Assembly     -- Concatenate into BrainOutput with dimension map

The orchestrator does NOT own the MechanismRunner lifecycle; instead it
creates one from the ModelRegistry (which auto-discovers all models and
their mechanism requirements).  If no registry is provided, mechanisms
are skipped (units still compute from raw H3/R3 inputs).

Usage::

    brain = BrainOrchestrator(active_units=("SPU", "ARU"))
    output = brain.compute(h3_features, r3_features)
    # output.tensor -> (B, T, brain_dim)
    # output.unit_ranges -> {"SPU": (0, 40), "ARU": (40, 80)}
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.core.types import BrainOutput, UnitOutput, ModelOutput
from mi_beta.brain.units import UnitRunner, ALL_UNIT_NAMES
from mi_beta.brain.pathways import PathwayRunner
from mi_beta.brain.neurochemicals import NeurochemicalStateManager

logger = logging.getLogger(__name__)


class BrainOrchestrator:
    """Sequences brain computation: mechanisms -> units -> pathways -> output.

    The orchestrator manages the two-pass unit execution strategy:
        1. Independent units compute from H3/R3 inputs only.
        2. PathwayRunner routes signals between units.
        3. Dependent units compute with cross-unit inputs.
        4. All unit tensors are assembled into a single BrainOutput.

    Args:
        active_units: Tuple of unit names to activate.  Defaults to all 9.
    """

    def __init__(
        self,
        active_units: Optional[Tuple[str, ...]] = None,
    ) -> None:
        self.unit_runner = UnitRunner(active_units=active_units)
        self.pathway_runner = PathwayRunner()
        self.neurochemical_state = NeurochemicalStateManager()

    # ── Main computation ───────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> BrainOutput:
        """Run the full brain computation pipeline.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features from the H3 engine.
            r3_features: (B, T, 49) R3 spectral features.

        Returns:
            BrainOutput with concatenated tensor, per-unit ranges, and
            dimension names.
        """
        # Phase 1: Mechanisms (skipped -- mechanisms are internal to models)
        # In the full implementation, MechanismRunner would pre-compute
        # shared mechanisms here and pass outputs to models.

        # Phase 2: Independent units
        independent = self.unit_runner.compute_all_independent(
            h3_features, r3_features
        )

        # Phase 3: Pathways
        cross_inputs = self.pathway_runner.route(independent)

        # Phase 4: Dependent units
        dependent = self.unit_runner.compute_dependent(
            h3_features, r3_features, cross_inputs
        )

        # Phase 5: Assemble
        all_outputs = {**independent, **dependent}
        return self._assemble(all_outputs)

    # ── Assembly ───────────────────────────────────────────────────────

    def _assemble(self, unit_tensors: Dict[str, Tensor]) -> BrainOutput:
        """Concatenate unit tensors into a single BrainOutput.

        Units are concatenated in UNIT_EXECUTION_ORDER to ensure
        deterministic dimension mapping across runs.

        Args:
            unit_tensors: Dict mapping unit_name -> (B, T, unit_dim) tensor.

        Returns:
            BrainOutput with combined tensor and per-unit metadata.
        """
        tensors: List[Tensor] = []
        unit_ranges: Dict[str, Tuple[int, int]] = {}
        dim_names: List[str] = []
        offset = 0

        for name in ALL_UNIT_NAMES:
            if name not in unit_tensors:
                continue
            t = unit_tensors[name]
            d = t.shape[-1]
            unit_ranges[name] = (offset, offset + d)
            tensors.append(t)
            # Generate dimension names from unit name and index
            for i in range(d):
                dim_names.append(f"{name}_d{i}")
            offset += d

        if tensors:
            combined = torch.cat(tensors, dim=-1)
        else:
            combined = torch.zeros(1, 1, 0)

        return BrainOutput(
            tensor=combined,
            unit_outputs={},  # Placeholder -- full UnitOutput objects in real impl
            unit_ranges=unit_ranges,
            dimension_names=tuple(dim_names),
        )

    # ── Properties ─────────────────────────────────────────────────────

    @property
    def active_unit_names(self) -> List[str]:
        """Names of currently active units."""
        return list(self.unit_runner.active_units.keys())

    @property
    def total_dim(self) -> int:
        """Total brain output dimensionality across all active units."""
        return self.unit_runner.total_dim

    # ── Lifecycle ──────────────────────────────────────────────────────

    def reset(self) -> None:
        """Reset neurochemical state between pipeline passes."""
        self.neurochemical_state.reset()

    # ── Introspection ──────────────────────────────────────────────────

    def summary(self) -> Dict[str, object]:
        """Return a summary dict for debugging / logging."""
        return {
            "active_units": self.active_unit_names,
            "total_dim": self.total_dim,
            "pathways": len(self.pathway_runner.pathways),
            "neurochemical_signals": len(self.neurochemical_state),
        }

    def __repr__(self) -> str:
        return (
            f"BrainOrchestrator("
            f"units={len(self.active_unit_names)}, "
            f"dim={self.total_dim}, "
            f"pathways={len(self.pathway_runner.pathways)})"
        )
