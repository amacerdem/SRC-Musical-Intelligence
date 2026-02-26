"""DimensionInterpreter — aggregates 131 beliefs into 6D/12D/24D hierarchy.

Follows the PsiInterpreter pattern from ``brain/psi_interpreter.py``.
Each 24D node = mean of its belief subset.
Each 12D node = mean of its 2 child 24D values.
Each  6D node = mean of its 2 child 12D values.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Tuple

import numpy as np
import torch

from Musical_Intelligence.contracts.dataclasses.brain_output import DimensionState

from .registry import ALL_COGNITION, ALL_NEUROSCIENCE, ALL_PSYCHOLOGY

if TYPE_CHECKING:
    from torch import Tensor


class DimensionInterpreter:
    """Maps 131 C³ beliefs → hierarchical DimensionState.

    Pre-computes index tensors at construction time for fast gather operations.
    """

    def __init__(self) -> None:
        # Pre-compute belief index lists for each 24D node
        self._neuro_indices: List[Tuple[int, ...]] = [
            d.belief_indices for d in ALL_NEUROSCIENCE
        ]
        # Pre-compute parent mappings: 12D → which 24D children
        self._cog_children: List[Tuple[int, int]] = []
        neuro_by_parent: Dict[str, List[int]] = {}
        for d in ALL_NEUROSCIENCE:
            neuro_by_parent.setdefault(d.parent_key, []).append(d.index)
        for d in ALL_COGNITION:
            children = neuro_by_parent.get(d.key, [])
            assert len(children) == 2, f"Cognition dim {d.key!r} has {len(children)} children, expected 2"
            self._cog_children.append((children[0], children[1]))

        # Pre-compute parent mappings: 6D → which 12D children
        self._psy_children: List[Tuple[int, int]] = []
        cog_by_parent: Dict[str, List[int]] = {}
        for d in ALL_COGNITION:
            cog_by_parent.setdefault(d.parent_key, []).append(d.index)
        for d in ALL_PSYCHOLOGY:
            children = cog_by_parent.get(d.key, [])
            assert len(children) == 2, f"Psychology dim {d.key!r} has {len(children)} children, expected 2"
            self._psy_children.append((children[0], children[1]))

    def interpret(self, beliefs: Tensor) -> DimensionState:
        """Compute hierarchical dimensions from belief tensor.

        Args:
            beliefs: ``(B, T, 131)`` belief values.

        Returns:
            DimensionState with psychology (B,T,6), cognition (B,T,12),
            neuroscience (B,T,24).
        """
        B, T = beliefs.shape[:2]
        device = beliefs.device

        # 24D: mean of belief subsets
        neuro = torch.zeros(B, T, 24, device=device)
        for i, indices in enumerate(self._neuro_indices):
            idx = torch.tensor(indices, dtype=torch.long, device=device)
            neuro[:, :, i] = beliefs.index_select(-1, idx).mean(dim=-1)

        # 12D: mean of 2 child 24D values
        cog = torch.zeros(B, T, 12, device=device)
        for i, (c0, c1) in enumerate(self._cog_children):
            cog[:, :, i] = (neuro[:, :, c0] + neuro[:, :, c1]) * 0.5

        # 6D: mean of 2 child 12D values
        psy = torch.zeros(B, T, 6, device=device)
        for i, (c0, c1) in enumerate(self._psy_children):
            psy[:, :, i] = (cog[:, :, c0] + cog[:, :, c1]) * 0.5

        return DimensionState(
            psychology=psy.clamp(0, 1),
            cognition=cog.clamp(0, 1),
            neuroscience=neuro.clamp(0, 1),
        )

    def interpret_numpy(self, beliefs: np.ndarray) -> Dict[str, np.ndarray]:
        """Convenience: numpy (T, 131) → dict of numpy arrays.

        Used by the Lab pipeline where data is already in numpy format.

        Args:
            beliefs: ``(T, 131)`` numpy array.

        Returns:
            Dict with keys ``"dim_6d"`` (T,6), ``"dim_12d"`` (T,12),
            ``"dim_24d"`` (T,24).
        """
        # Add batch dimension, convert to torch
        t = torch.from_numpy(beliefs).unsqueeze(0)  # (1, T, 131)
        state = self.interpret(t)
        return {
            "dim_6d": state.psychology[0].cpu().numpy(),
            "dim_12d": state.cognition[0].cpu().numpy(),
            "dim_24d": state.neuroscience[0].cpu().numpy(),
        }
