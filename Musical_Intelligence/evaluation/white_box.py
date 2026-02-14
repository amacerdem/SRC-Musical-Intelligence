"""White-box traceability -- dim → formula → citation chain.

Verifies that MI-Core's learned representations maintain traceability
to the deterministic MI Teacher's scientific foundations.

For any C3 dimension d, traces:
  d → model → formula → mechanism → paper citation

This is the key differentiator of MI: every output dimension is
scientifically grounded, not a black-box latent.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class TraceEntry:
    """Traceability chain for a single C3 dimension.

    Attributes:
        dim_index: Absolute index in the 1006D C3 space.
        unit: Cognitive unit name (e.g. "SPU").
        model: Model acronym (e.g. "PLE").
        layer: Output layer name (E/M/P/F).
        layer_index: Index within the model's output.
        mechanism: Mechanism name (e.g. "BEP", "ASA").
        formula: Formula description (if available).
    """

    dim_index: int
    unit: str
    model: str
    layer: str
    layer_index: int
    mechanism: str
    formula: Optional[str] = None


class WhiteBoxTracer:
    """Trace any MI-space dimension to its scientific source.

    Uses the BrainOrchestrator's unit and model metadata to build
    a complete traceability map from dimension index to formula.

    Usage::

        tracer = WhiteBoxTracer()
        entry = tracer.trace_dim(300)
        print(entry)
        # TraceEntry(dim_index=300, unit="SPU", model="PLE", ...)
    """

    def __init__(self) -> None:
        self._trace_map: Dict[int, TraceEntry] = {}
        self._built = False

    def build(self) -> None:
        """Build traceability map from BrainOrchestrator metadata."""
        from Musical_Intelligence.brain.orchestrator import BrainOrchestrator

        orch = BrainOrchestrator()
        dim_offset = 0

        for unit_name in (
            "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU"
        ):
            unit = orch.units[unit_name]
            for model in unit.models:
                layers = model.LAYERS
                mechanisms = model.MECHANISM_NAMES

                for layer_idx, layer_name in enumerate(layers):
                    abs_idx = dim_offset + layer_idx
                    self._trace_map[abs_idx] = TraceEntry(
                        dim_index=abs_idx,
                        unit=unit_name,
                        model=model.NAME,
                        layer=layer_name,
                        layer_index=layer_idx,
                        mechanism=mechanisms[0] if mechanisms else "unknown",
                    )

                dim_offset += model.OUTPUT_DIM

        self._built = True

    def trace_dim(self, dim_index: int) -> TraceEntry:
        """Trace a C3 dimension to its source.

        Parameters
        ----------
        dim_index : int
            Index in the 1006D C3 space (0-based).

        Returns
        -------
        TraceEntry
            Complete traceability chain.
        """
        if not self._built:
            self.build()

        if dim_index not in self._trace_map:
            raise KeyError(
                f"Dimension {dim_index} not found in C3 space (0-1005)"
            )
        return self._trace_map[dim_index]

    def trace_range(
        self, start: int, end: int
    ) -> List[TraceEntry]:
        """Trace a range of C3 dimensions."""
        if not self._built:
            self.build()
        return [
            self._trace_map[d]
            for d in range(start, end)
            if d in self._trace_map
        ]

    def trace_unit(self, unit_name: str) -> List[TraceEntry]:
        """Get all trace entries for a cognitive unit."""
        if not self._built:
            self.build()
        return [e for e in self._trace_map.values() if e.unit == unit_name]

    def trace_model(self, model_name: str) -> List[TraceEntry]:
        """Get all trace entries for a specific model."""
        if not self._built:
            self.build()
        return [e for e in self._trace_map.values() if e.model == model_name]

    def summary(self) -> Dict[str, Dict[str, int]]:
        """Get dimension count per unit and model.

        Returns
        -------
        dict
            Nested dict: unit_name → model_name → n_dims
        """
        if not self._built:
            self.build()

        result: Dict[str, Dict[str, int]] = {}
        for entry in self._trace_map.values():
            if entry.unit not in result:
                result[entry.unit] = {}
            result[entry.unit][entry.model] = (
                result[entry.unit].get(entry.model, 0) + 1
            )
        return result

    def format_trace(self, dim_index: int) -> str:
        """Format a single dimension trace as a readable string."""
        e = self.trace_dim(dim_index)
        return (
            f"C3[{e.dim_index}] → {e.unit}/{e.model}.{e.layer} "
            f"(layer_idx={e.layer_index}, mechanism={e.mechanism})"
        )
