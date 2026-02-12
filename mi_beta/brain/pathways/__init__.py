"""
MI-Beta Brain Pathways -- Cross-unit signal routing declarations.

Routes signals between cognitive units via declared CrossUnitPathway
instances.  Each pathway declares a directed data dependency from a
source model in one unit to a target model in another (or the same) unit.

Current pathways:

    P1: SPU -> ARU  (consonance -> pleasure)       Bidelman 2009, r=0.81
    P2: STU -> STU  (beat -> motor sync)            Grahn & Brett 2007, r=0.70
    P3: IMU -> ARU  (memory -> affect)              Janata 2009, r=0.55
    P4: STU -> STU  (context -> prediction)         Mischler 2025, r=0.99
    P5: STU -> ARU  (tempo -> emotion)              Juslin & Vastfjall 2008, r=0.60

The PathwayRunner inspects independent unit outputs and packages
cross-unit inputs for the dependent units (ARU, RPU).
"""

from __future__ import annotations

from typing import Dict, List, Tuple

from torch import Tensor

from mi_beta.contracts import CrossUnitPathway

from .p1_spu_aru import P1_SPU_ARU
from .p2_stu_internal import P2_STU_INTERNAL
from .p3_imu_aru import P3_IMU_ARU
from .p4_stu_internal import P4_STU_INTERNAL
from .p5_stu_aru import P5_STU_ARU

ALL_PATHWAYS: Tuple[CrossUnitPathway, ...] = (
    P1_SPU_ARU,
    P2_STU_INTERNAL,
    P3_IMU_ARU,
    P4_STU_INTERNAL,
    P5_STU_ARU,
)


class PathwayRunner:
    """Routes signals between cognitive units via declared pathways.

    In the two-pass brain execution model:
        1. Independent units (SPU, STU, IMU, ASU, NDU, MPU, PCU) compute first.
        2. PathwayRunner extracts relevant signals from their outputs.
        3. Dependent units (ARU, RPU) receive routed signals as cross_unit_inputs.

    Currently operates as a passthrough -- each pathway's source_unit tensor
    is passed in its entirety, keyed by pathway_id.  In the full implementation
    this will extract specific source_dims from source model slices.
    """

    def __init__(self) -> None:
        self._pathways = ALL_PATHWAYS

    @property
    def pathways(self) -> Tuple[CrossUnitPathway, ...]:
        """All declared pathways."""
        return self._pathways

    @property
    def inter_unit_pathways(self) -> List[CrossUnitPathway]:
        """Pathways that cross unit boundaries."""
        return [p for p in self._pathways if p.is_inter_unit]

    @property
    def intra_unit_pathways(self) -> List[CrossUnitPathway]:
        """Pathways within the same unit."""
        return [p for p in self._pathways if p.is_intra_unit]

    def route(self, unit_outputs: Dict[str, Tensor]) -> Dict[str, Tensor]:
        """Route signals from independent unit outputs to dependent units.

        Extracts source unit tensors for each pathway and packages them
        as a dict keyed by pathway_id.  Dependent units can look up their
        cross-unit inputs by pathway_id.

        Currently a passthrough: passes full unit tensors as cross-unit
        inputs.  In the full implementation, this will extract specific
        dimensions from source model slices within the unit tensor.

        Args:
            unit_outputs: Dict mapping unit_name -> (B, T, unit_dim) tensor
                from the independent computation pass.

        Returns:
            Dict mapping pathway_id -> (B, T, D) tensor of cross-unit
            inputs for the dependent pass.
        """
        cross_inputs: Dict[str, Tensor] = {}
        for pathway in self._pathways:
            if pathway.source_unit in unit_outputs:
                cross_inputs[pathway.pathway_id] = unit_outputs[pathway.source_unit]
        return cross_inputs

    def get_targets_for_unit(self, unit_name: str) -> List[CrossUnitPathway]:
        """Get all pathways that target a specific unit.

        Args:
            unit_name: Target unit name (e.g. "ARU").

        Returns:
            List of pathways whose target_unit matches.
        """
        return [p for p in self._pathways if p.target_unit == unit_name]

    def get_sources_for_unit(self, unit_name: str) -> List[CrossUnitPathway]:
        """Get all pathways that originate from a specific unit.

        Args:
            unit_name: Source unit name (e.g. "SPU").

        Returns:
            List of pathways whose source_unit matches.
        """
        return [p for p in self._pathways if p.source_unit == unit_name]

    def __repr__(self) -> str:
        inter = len(self.inter_unit_pathways)
        intra = len(self.intra_unit_pathways)
        return (
            f"PathwayRunner("
            f"pathways={len(self._pathways)}, "
            f"inter={inter}, intra={intra})"
        )


__all__ = [
    # Pathway declarations
    "P1_SPU_ARU",
    "P2_STU_INTERNAL",
    "P3_IMU_ARU",
    "P4_STU_INTERNAL",
    "P5_STU_ARU",
    "ALL_PATHWAYS",
    # Runner
    "PathwayRunner",
]
