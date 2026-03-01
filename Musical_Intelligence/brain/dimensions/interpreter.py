"""DimensionInterpreter — computes 6D/12D/24D via independent model functions.

Each tier is independently computed from (beliefs, ram, neuro).
NO tier derives from another tier's output.

Usage::

    interpreter = DimensionInterpreter()
    state = interpreter.interpret(beliefs, ram, neuro)  # → DimensionState
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import numpy as np
import torch

from Musical_Intelligence.contracts.dataclasses.brain_output import DimensionState

from .models import COGNITION_MODELS, NEUROSCIENCE_MODELS, PSYCHOLOGY_MODELS

if TYPE_CHECKING:
    from torch import Tensor


class DimensionInterpreter:
    """Maps C³ outputs → independent 3-tier DimensionState.

    Each of the 42 dimensions (6+12+24) has its own computation model
    that reads directly from (beliefs, ram, neuro). Models are pure
    functions defined in ``dimensions/models/``.
    """

    def __init__(self) -> None:
        self._psy_models = PSYCHOLOGY_MODELS
        self._cog_models = COGNITION_MODELS
        self._neuro_models = NEUROSCIENCE_MODELS

    def interpret(
        self,
        beliefs: Tensor,
        ram: Tensor,
        neuro: Tensor,
    ) -> DimensionState:
        """Compute all 3 tiers from C³ outputs.

        Args:
            beliefs: ``(B, T, 131)`` belief values.
            ram:     ``(B, T, 26)``  Region Activation Map.
            neuro:   ``(B, T, 4)``   neurochemical state [DA, NE, OPI, 5HT].

        Returns:
            DimensionState with psychology (B,T,6), cognition (B,T,12),
            neuroscience (B,T,24).
        """
        # 6D: each model independently computes (B, T) from sources
        psy = torch.stack(
            [m(beliefs, ram, neuro) for m in self._psy_models], dim=-1,
        )

        # 12D: each model independently computes (B, T) from sources
        cog = torch.stack(
            [m(beliefs, ram, neuro) for m in self._cog_models], dim=-1,
        )

        # 24D: each model independently computes (B, T) from sources
        ns = torch.stack(
            [m(beliefs, ram, neuro) for m in self._neuro_models], dim=-1,
        )

        return DimensionState(
            psychology=psy.clamp(0, 1),
            cognition=cog.clamp(0, 1),
            neuroscience=ns.clamp(0, 1),
        )

    def interpret_numpy(
        self,
        beliefs: np.ndarray,
        ram: np.ndarray | None = None,
        neuro: np.ndarray | None = None,
    ) -> Dict[str, np.ndarray]:
        """Convenience: numpy (T, 131) → dict of numpy arrays.

        Used by the Lab pipeline where data is already in numpy format.

        Args:
            beliefs: ``(T, 131)`` numpy array.
            ram:     ``(T, 26)``  numpy array, or None (zeros used).
            neuro:   ``(T, 4)``   numpy array, or None (0.5 baseline used).

        Returns:
            Dict with keys ``"dim_6d"`` (T,6), ``"dim_12d"`` (T,12),
            ``"dim_24d"`` (T,24).
        """
        T = beliefs.shape[0]

        # Add batch dimension, convert to torch
        b = torch.from_numpy(beliefs).unsqueeze(0).float()  # (1, T, 131)

        if ram is not None:
            r = torch.from_numpy(ram).unsqueeze(0).float()  # (1, T, 26)
        else:
            r = torch.zeros(1, T, 26)

        if neuro is not None:
            n = torch.from_numpy(neuro).unsqueeze(0).float()  # (1, T, 4)
        else:
            n = torch.full((1, T, 4), 0.5)  # Baseline

        state = self.interpret(b, r, n)
        return {
            "dim_6d": state.psychology[0].cpu().numpy(),
            "dim_12d": state.cognition[0].cpu().numpy(),
            "dim_24d": state.neuroscience[0].cpu().numpy(),
        }
