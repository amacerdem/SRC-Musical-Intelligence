"""LayerSpec -- E/M/P/F Output Layer System.

Defines a single layer of a cognitive model's flat output tensor. Each layer
is a contiguous slice with a short code, descriptive name, and ordered
dimension names.

Layer codes follow the C3 convention:

    E  Extraction / Neurochemical
    M  Mechanism / Circuit
    P  Psychological / Subjective
    F  Forecast / Predictive
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LayerSpec:
    """A contiguous slice of a model's flat output tensor.

    The ``(start, end)`` range is a half-open interval::

        output[..., layer.start:layer.end]  # extracts this layer

    Attributes:
        code:      Short code for the layer type (``"E"``, ``"M"``,
                   ``"P"``, ``"F"``, or custom).
        name:      Full descriptive name (e.g. ``"Neurochemical Signals"``).
        start:     Start index in the flat output tensor (inclusive).
        end:       End index in the flat output tensor (exclusive).
        dim_names: Ordered tuple of dimension names within this layer;
                   ``len(dim_names)`` must equal ``end - start``.
    """

    code: str
    name: str
    start: int
    end: int
    dim_names: tuple[str, ...]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if self.start < 0:
            raise ValueError(
                f"LayerSpec {self.code!r}: start must be >= 0, "
                f"got {self.start}"
            )
        if self.end <= self.start:
            raise ValueError(
                f"LayerSpec {self.code!r}: end must be > start, "
                f"got start={self.start}, end={self.end}"
            )
        expected_dim = self.end - self.start
        if len(self.dim_names) != expected_dim:
            raise ValueError(
                f"LayerSpec {self.code!r}: len(dim_names) must equal "
                f"end - start ({expected_dim}), "
                f"got {len(self.dim_names)}"
            )

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def dim(self) -> int:
        """Number of dimensions in this layer (``end - start``)."""
        return self.end - self.start
