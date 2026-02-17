"""Brain Orchestrator — top-level entry point for C³ processing.

Transforms R³ spectral features and H³ temporal demands into a complete
``BrainOutput`` with four channels: tensor, RAM, neuro, and Ψ³.

Usage:
    orchestrator = BrainOrchestrator(nuclei=[bch, ...])
    output = orchestrator.process(r3_output, h3_features)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

import torch

# Backward-compatibility: old conftest.py imports UNIT_ORDER
UNIT_ORDER = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU")

from Musical_Intelligence.brain.executor import execute
from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter
from Musical_Intelligence.contracts.bases.nucleus import Nucleus
from Musical_Intelligence.contracts.dataclasses.brain_output import BrainOutput

if TYPE_CHECKING:
    from torch import Tensor


class BrainOrchestrator:
    """Top-level C³ processor.

    Holds a collection of nuclei and processes audio features through
    the depth-ordered execution engine.
    """

    def __init__(
        self,
        nuclei: List[Nucleus],
        psi_interpreter: PsiInterpreter | None = None,
    ) -> None:
        self.nuclei = nuclei
        self.psi = psi_interpreter or PsiInterpreter()

        # Validate nuclei
        for n in nuclei:
            errors = n.validate_constants()
            if errors:
                raise ValueError(
                    f"Nucleus {n.NAME!r} has validation errors: {errors}"
                )

    def process(
        self,
        r3_features: Tensor,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> BrainOutput:
        """Run the full C³ pipeline.

        Args:
            r3_features: ``(B, T, 97)`` R³ spectral features.
            h3_features: Per-demand H³ time series.
            cross_unit_inputs: Optional cross-unit pathway tensors.

        Returns:
            ``BrainOutput`` with tensor, ram, neuro, psi.
        """
        # Execute all nuclei in depth order
        outputs, ram, neuro = execute(
            self.nuclei, h3_features, r3_features, cross_unit_inputs,
        )

        # Assemble scope-filtered tensor (external + hybrid dims)
        tensor = self._assemble_tensor(outputs)

        # Ψ³ cognitive interpretation
        psi = self.psi.interpret(tensor, ram, neuro)

        return BrainOutput(
            tensor=tensor,
            ram=ram,
            neuro=neuro,
            psi=psi,
        )

    def _assemble_tensor(self, outputs: Dict[str, Tensor]) -> Tensor:
        """Concatenate exportable dims from all nuclei.

        Collects ``external`` + ``hybrid`` scoped dimensions from each
        nucleus's output, in nucleus order (sorted by depth, then name).
        """
        parts: List[Tensor] = []

        sorted_nuclei = sorted(
            self.nuclei,
            key=lambda n: (n.PROCESSING_DEPTH, n.NAME),
        )

        for nucleus in sorted_nuclei:
            if nucleus.NAME not in outputs:
                continue
            full_output = outputs[nucleus.NAME]
            exp_dims = nucleus.exportable_dims
            if exp_dims:
                # Select only exportable dimension indices
                idx = torch.tensor(exp_dims, dtype=torch.long,
                                   device=full_output.device)
                parts.append(full_output.index_select(-1, idx))

        if not parts:
            # Return empty tensor with correct batch/time dims
            B, T = next(iter(outputs.values())).shape[:2]
            return torch.zeros(B, T, 0, device=next(iter(outputs.values())).device)

        return torch.cat(parts, dim=-1)
