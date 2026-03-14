"""DimensionInterpreter — computes 5+5 dual-radar dimensions from beliefs.

Two independent radars, each 5D, all computed from beliefs only.

Radar 1: "What You Hear" (Musical Character)
    speed, volume, weight, texture, depth

Radar 2: "How It Feels" (Emotional Feel)
    mood, energy, hardness, predictability, focus

Usage::

    interpreter = DimensionInterpreter()
    result = interpreter.interpret_numpy(beliefs)  # → dict of numpy arrays
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict

import numpy as np
import torch

from .models import MUSICAL_MODELS, EMOTIONAL_MODELS

if TYPE_CHECKING:
    from torch import Tensor


class DimensionInterpreter:
    """Maps C³ belief outputs → dual-radar 5+5 dimensions.

    Each of the 10 dimensions has its own computation model
    that reads directly from beliefs. Models are pure functions.
    """

    def __init__(self) -> None:
        self._musical_models = MUSICAL_MODELS
        self._emotional_models = EMOTIONAL_MODELS

    def interpret(self, beliefs: Tensor) -> Dict[str, Tensor]:
        """Compute both radars from C³ belief outputs.

        Args:
            beliefs: ``(B, T, 131)`` belief values.

        Returns:
            Dict with ``"musical_5d"`` (B,T,5) and ``"emotional_5d"`` (B,T,5).
        """
        musical = torch.stack(
            [m(beliefs) for m in self._musical_models], dim=-1,
        ).clamp(0, 1)

        emotional = torch.stack(
            [m(beliefs) for m in self._emotional_models], dim=-1,
        ).clamp(0, 1)

        return {
            "musical_5d": musical,
            "emotional_5d": emotional,
        }

    def interpret_numpy(
        self,
        beliefs: np.ndarray,
    ) -> Dict[str, np.ndarray]:
        """Convenience: numpy (T, 131) → dict of numpy arrays.

        Args:
            beliefs: ``(T, 131)`` numpy array.

        Returns:
            Dict with ``"musical_5d"`` (T,5) and ``"emotional_5d"`` (T,5).
        """
        b = torch.from_numpy(beliefs).unsqueeze(0).float()  # (1, T, 131)

        result = self.interpret(b)
        return {
            "musical_5d": result["musical_5d"][0].cpu().numpy(),
            "emotional_5d": result["emotional_5d"][0].cpu().numpy(),
        }
