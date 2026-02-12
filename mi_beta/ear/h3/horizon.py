"""
EventHorizon — Defines temporal window sizes.

Each horizon represents a time scale at which musical events are analyzed.
32 horizons span from 5.8ms (sub-note) to 981s (full piece).
"""

from __future__ import annotations

from ...core.constants import HORIZON_FRAMES, HORIZON_MS, N_HORIZONS


class EventHorizon:
    """A single temporal horizon."""

    def __init__(self, index: int) -> None:
        assert 0 <= index < N_HORIZONS, f"Horizon index {index} out of range [0, {N_HORIZONS})"
        self.index = index

    @property
    def frames(self) -> int:
        """Window size in frames."""
        return HORIZON_FRAMES[self.index]

    @property
    def ms(self) -> float:
        """Window size in milliseconds."""
        return HORIZON_MS[self.index]

    @property
    def seconds(self) -> float:
        """Window size in seconds."""
        return self.ms / 1000.0

    def __repr__(self) -> str:
        if self.ms < 1000:
            return f"H{self.index}({self.ms:.0f}ms, {self.frames} frames)"
        return f"H{self.index}({self.seconds:.1f}s, {self.frames} frames)"
