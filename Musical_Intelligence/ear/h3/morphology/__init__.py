"""H3 Morphology sub-package -- 24 temporal morphologies (M0-M23).

Re-exports :class:`MorphComputer` as the primary public API.
"""
from __future__ import annotations

from .computer import MorphComputer

__all__ = ["MorphComputer"]
