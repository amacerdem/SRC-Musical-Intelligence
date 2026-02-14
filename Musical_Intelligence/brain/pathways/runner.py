"""PathwayRunner -- routes inter-unit data between cognitive units.

Only handles inter-unit pathways (P1, P3, P5). Intra-unit pathways
(P2, P4) are handled within the source unit's compute() method.

Usage::

    runner = PathwayRunner()
    cross_inputs = runner.route(unit_outputs)
    # cross_inputs: {"P1_SPU_ARU": (B,T,99), "P3_IMU_ARU": (B,T,159), ...}
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict

from .definitions import INTER_UNIT_PATHWAYS

if TYPE_CHECKING:
    from torch import Tensor

logger = logging.getLogger(__name__)


class PathwayRunner:
    """Routes inter-unit pathway data between cognitive units.

    Extracts source unit outputs and keys them by pathway_id for
    consumption by dependent units (ARU, RPU).
    """

    def __init__(self) -> None:
        self._pathways = INTER_UNIT_PATHWAYS

    @property
    def pathway_count(self) -> int:
        """Number of inter-unit pathways managed."""
        return len(self._pathways)

    @property
    def pathway_ids(self) -> tuple[str, ...]:
        """IDs of all managed pathways."""
        return tuple(p.pathway_id for p in self._pathways)

    def route(self, unit_outputs: Dict[str, "Tensor"]) -> Dict[str, "Tensor"]:
        """Extract and route inter-unit pathway data.

        For each inter-unit pathway, extracts the source unit's full
        output tensor and keys it by pathway_id.

        Args:
            unit_outputs: Dict mapping unit name to output tensor.
                E.g. ``{"SPU": (B,T,99), "STU": (B,T,148), ...}``.

        Returns:
            Dict mapping pathway_id to source unit output tensor.
            E.g. ``{"P1_SPU_ARU": (B,T,99), ...}``.
        """
        cross_inputs: Dict[str, Tensor] = {}

        for pathway in self._pathways:
            source = pathway.source_unit
            if source not in unit_outputs:
                logger.warning(
                    "Pathway %s: source unit %s not in unit_outputs",
                    pathway.pathway_id,
                    source,
                )
                continue

            cross_inputs[pathway.pathway_id] = unit_outputs[source]
            logger.debug(
                "Routed %s: %s -> %s (shape %s)",
                pathway.pathway_id,
                source,
                pathway.target_unit,
                unit_outputs[source].shape,
            )

        return cross_inputs
