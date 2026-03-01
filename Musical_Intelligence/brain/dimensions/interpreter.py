"""DimensionInterpreter — computes 6D/12D/24D via independent model functions.

Each tier is independently computed from beliefs only.
NO tier derives from another tier's output.

Usage::

    interpreter = DimensionInterpreter()
    state = interpreter.interpret(beliefs)  # → DimensionState
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
    """Maps C³ belief outputs → independent 3-tier DimensionState.

    Each of the 42 dimensions (6+12+24) has its own computation model
    that reads directly from beliefs. Models are pure functions defined
    in ``dimensions/models/``.
    """

    def __init__(self) -> None:
        self._psy_models = PSYCHOLOGY_MODELS
        self._cog_models = COGNITION_MODELS
        self._neuro_models = NEUROSCIENCE_MODELS

    def interpret(self, beliefs: Tensor) -> DimensionState:
        """Compute all 3 tiers from C³ belief outputs.

        Args:
            beliefs: ``(B, T, 131)`` belief values.

        Returns:
            DimensionState with psychology (B,T,6), cognition (B,T,12),
            neuroscience (B,T,24).
        """
        psy = torch.stack(
            [m(beliefs) for m in self._psy_models], dim=-1,
        )

        cog = torch.stack(
            [m(beliefs) for m in self._cog_models], dim=-1,
        )

        ns = torch.stack(
            [m(beliefs) for m in self._neuro_models], dim=-1,
        )

        return DimensionState(
            psychology=psy.clamp(0, 1),
            cognition=cog.clamp(0, 1),
            neuroscience=ns.clamp(0, 1),
        )

    def interpret_numpy(
        self,
        beliefs: np.ndarray,
    ) -> Dict[str, np.ndarray]:
        """Convenience: numpy (T, 131) → dict of numpy arrays.

        Used by the Lab pipeline where data is already in numpy format.

        Args:
            beliefs: ``(T, 131)`` numpy array.

        Returns:
            Dict with keys ``"dim_6d"`` (T,6), ``"dim_12d"`` (T,12),
            ``"dim_24d"`` (T,24).
        """
        b = torch.from_numpy(beliefs).unsqueeze(0).float()  # (1, T, 131)

        state = self.interpret(b)
        return {
            "dim_6d": state.psychology[0].cpu().numpy(),
            "dim_12d": state.cognition[0].cpu().numpy(),
            "dim_24d": state.neuroscience[0].cpu().numpy(),
        }
