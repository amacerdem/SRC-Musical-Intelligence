"""BrainOrchestrator -- 5-phase execution of the C3 cognitive architecture.

Phase 1: Mechanisms   -- MechanismRunner computes all 10 mechanisms (cached).
Phase 2: Independent  -- 7 units compute in parallel (SPU,STU,IMU,ASU,NDU,MPU,PCU).
Phase 3: Routing      -- PathwayRunner routes inter-unit signals (P1,P3,P5).
Phase 4: Dependent    -- ARU computes with pathway inputs, then RPU with ARU output.
Phase 5: Assembly     -- Concatenate all 9 unit outputs → (B, T, 1006).

Usage::

    orchestrator = BrainOrchestrator()
    output = orchestrator.forward(h3_features, r3_features)
    # output.tensor: (B, T, 1006)
    # output.unit_slices: {"SPU": (0, 99), "STU": (99, 247), ...}
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, Tuple

import torch

from .mechanisms import MechanismRunner
from .pathways import PathwayRunner
from .units import (
    ARUUnit,
    ASUUnit,
    IMUUnit,
    MPUUnit,
    NDUUnit,
    PCUUnit,
    RPUUnit,
    SPUUnit,
    STUUnit,
)

if TYPE_CHECKING:
    from torch import Tensor


# Execution order for the 9 cognitive units.
INDEPENDENT_UNITS = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU")
DEPENDENT_UNITS = ("ARU", "RPU")
UNIT_ORDER = INDEPENDENT_UNITS + DEPENDENT_UNITS

# Expected total output dimensionality.
TOTAL_DIM = 1006


@dataclass(frozen=True)
class BrainOutput:
    """Result of a full brain forward pass.

    Attributes:
        tensor:       Full brain output ``(B, T, 1006)`` in ``[0, 1]``.
        unit_slices:  Dict mapping unit name to ``(start, end)`` slice
                      within the 1006D output.
        unit_outputs: Dict mapping unit name to its raw output tensor.
    """

    tensor: Tensor
    unit_slices: Dict[str, Tuple[int, int]]
    unit_outputs: Dict[str, Tensor]


class BrainOrchestrator:
    """5-phase orchestrator for the C3 cognitive architecture.

    Manages 10 mechanisms, 9 cognitive units (96 models), and 5 pathways
    to produce a 1006D brain output per time step.
    """

    def __init__(self) -> None:
        # Phase 1: Mechanisms
        self._mechanism_runner = MechanismRunner()

        # Phase 2+4: Cognitive units
        self._units: Dict[str, object] = {
            "SPU": SPUUnit(),
            "STU": STUUnit(),
            "IMU": IMUUnit(),
            "ASU": ASUUnit(),
            "NDU": NDUUnit(),
            "MPU": MPUUnit(),
            "PCU": PCUUnit(),
            "ARU": ARUUnit(),
            "RPU": RPUUnit(),
        }

        # Phase 3: Pathway routing
        self._pathway_runner = PathwayRunner()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def total_dim(self) -> int:
        """Total output dimensionality (1006)."""
        return TOTAL_DIM

    @property
    def unit_dims(self) -> Dict[str, int]:
        """Output dimensionality per unit."""
        dims = {}
        for name in UNIT_ORDER:
            unit = self._units[name]
            total = sum(m.OUTPUT_DIM for m in unit.models)
            dims[name] = total
        return dims

    @property
    def model_count(self) -> int:
        """Total number of models across all units."""
        return sum(len(u.models) for u in self._units.values())

    # ------------------------------------------------------------------
    # Forward pass
    # ------------------------------------------------------------------

    def forward(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
    ) -> BrainOutput:
        """Execute the 5-phase brain forward pass.

        Args:
            h3_features: Sparse H3 temporal features keyed by 4-tuples.
                Each value is ``(B, T)`` tensor.
            r3_features: ``(B, T, 49)`` R3 spectral features (v1) or
                ``(B, T, 128)`` for v2.

        Returns:
            ``BrainOutput`` with concatenated 1006D tensor, unit slices,
            and per-unit output tensors.
        """
        # ═══════════════════════════════════════════════════════════════
        # Phase 1: Mechanisms
        # ═══════════════════════════════════════════════════════════════
        self._mechanism_runner.run(h3_features, r3_features)
        mechanism_outputs = {
            name: self._mechanism_runner.get(name)
            for name in self._mechanism_runner._mechanisms
        }

        # Inject mechanism outputs into all units
        for unit in self._units.values():
            unit.set_mechanism_outputs(mechanism_outputs)

        # ═══════════════════════════════════════════════════════════════
        # Phase 2: Independent units
        # ═══════════════════════════════════════════════════════════════
        unit_outputs: Dict[str, Tensor] = {}
        for name in INDEPENDENT_UNITS:
            unit = self._units[name]
            unit_outputs[name] = unit.compute(
                h3_features, r3_features, cross_unit_inputs=None
            )

        # ═══════════════════════════════════════════════════════════════
        # Phase 3: Pathway routing
        # ═══════════════════════════════════════════════════════════════
        cross_unit_inputs = self._pathway_runner.route(unit_outputs)

        # ═══════════════════════════════════════════════════════════════
        # Phase 4: Dependent units
        # ═══════════════════════════════════════════════════════════════
        # 4a: ARU receives pathway inputs (P1, P3, P5)
        unit_outputs["ARU"] = self._units["ARU"].compute(
            h3_features, r3_features, cross_unit_inputs=cross_unit_inputs
        )

        # 4b: RPU receives ARU output via CROSS_UNIT_READS
        rpu_inputs = dict(cross_unit_inputs)
        rpu_inputs["ARU"] = unit_outputs["ARU"]
        unit_outputs["RPU"] = self._units["RPU"].compute(
            h3_features, r3_features, cross_unit_inputs=rpu_inputs
        )

        # ═══════════════════════════════════════════════════════════════
        # Phase 5: Assembly
        # ═══════════════════════════════════════════════════════════════
        ordered_outputs = [unit_outputs[name] for name in UNIT_ORDER]
        brain_tensor = torch.cat(ordered_outputs, dim=-1)

        # Compute unit slices
        unit_slices: Dict[str, Tuple[int, int]] = {}
        offset = 0
        for name in UNIT_ORDER:
            dim = unit_outputs[name].shape[-1]
            unit_slices[name] = (offset, offset + dim)
            offset += dim

        # Clear mechanism cache
        self._mechanism_runner.clear()

        return BrainOutput(
            tensor=brain_tensor,
            unit_slices=unit_slices,
            unit_outputs=unit_outputs,
        )
