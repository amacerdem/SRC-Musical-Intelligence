"""Brain pathways: 5 cross-unit signal routes."""
from __future__ import annotations
from typing import Dict, Tuple
from torch import Tensor
from ...contracts.pathway_spec import CrossUnitPathway
from .p1_spu_aru import P1_SPU_ARU
from .p2_stu_internal import P2_STU_INTERNAL
from .p3_imu_aru import P3_IMU_ARU
from .p4_stu_internal import P4_STU_INTERNAL
from .p5_stu_aru import P5_STU_ARU

ALL_PATHWAYS = (P1_SPU_ARU, P2_STU_INTERNAL, P3_IMU_ARU, P4_STU_INTERNAL, P5_STU_ARU)

class PathwayRunner:
    def __init__(self):
        self._pathways = ALL_PATHWAYS
    @property
    def pathways(self):
        return self._pathways
    def route(self, unit_outputs: Dict[str, Tensor]) -> Dict[str, Tensor]:
        # Currently passthrough: passes full unit tensors
        result = {}
        for pw in self._pathways:
            if pw.source_unit in unit_outputs:
                result[pw.pathway_id] = unit_outputs[pw.source_unit]
        return result
