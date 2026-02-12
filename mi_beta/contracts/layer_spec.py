"""
LayerSpec -- Output layer convention for cognitive models.

Every BaseModel organises its output dimensions into semantically meaningful
layers.  The layer codes follow the convention used across C3 model documents:

    E  -- Extraction / Neurochemical signals  (raw biophysical quantities)
    M  -- Mechanism / Circuit activation       (neural pathway states)
    P  -- Psychological / Subjective states    (Berridge wanting/liking, etc.)
    F  -- Forecast / Predictive signals        (future-oriented estimates)

Not every model uses all four layers.  A simple model may have only E and P;
a complex one (like SRP) may use all four plus additional domain-specific
layers (T for Temporal, N for Neurochemical, etc.).

The LayerSpec is frozen and hashable so it can be collected into tuples and
sets.  The (start, end) range is a half-open interval into the model's
flat output tensor: output[..., start:end].
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class LayerSpec:
    """Specification of a single output layer within a model's output tensor.

    Attributes:
        code:      Short code for the layer type ("E", "M", "P", "F", or custom).
        name:      Full descriptive name (e.g. "Neurochemical Signals").
        start:     Start index in the model's flat output tensor (inclusive).
        end:       End index in the model's flat output tensor (exclusive).
        dim_names: Ordered tuple of dimension names within this layer.
                   len(dim_names) must equal (end - start).
    """

    code: str
    name: str
    start: int
    end: int
    dim_names: Tuple[str, ...]

    def __post_init__(self) -> None:
        expected = self.end - self.start
        actual = len(self.dim_names)
        if actual != expected:
            raise ValueError(
                f"LayerSpec {self.code!r}: dim_names has {actual} entries "
                f"but range [{self.start}:{self.end}] expects {expected}"
            )
        if self.start < 0 or self.end <= self.start:
            raise ValueError(
                f"LayerSpec {self.code!r}: invalid range [{self.start}:{self.end}]"
            )

    @property
    def dim(self) -> int:
        """Number of dimensions in this layer."""
        return self.end - self.start

    def __repr__(self) -> str:
        return (
            f"LayerSpec(code={self.code!r}, name={self.name!r}, "
            f"range=[{self.start}:{self.end}], dim={self.dim})"
        )
