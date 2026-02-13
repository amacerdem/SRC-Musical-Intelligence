"""LayerSpec: output layer specification for cognitive models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LayerSpec:
    code: str                    # "E", "M", "P", "F" (or custom)
    name: str                    # "Neurochemical Signals"
    start: int                   # start index (inclusive)
    end: int                     # end index (exclusive)
    dim_names: Tuple[str, ...]   # dimension names for this layer

    @property
    def dim(self) -> int:
        return self.end - self.start
