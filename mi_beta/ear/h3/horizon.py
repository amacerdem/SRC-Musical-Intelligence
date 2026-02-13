"""EventHorizon: 32 temporal time scales."""

from __future__ import annotations

from ...core.constants import HORIZON_MS, HORIZON_FRAMES, N_HORIZONS


class EventHorizon:
    """Represents a single temporal horizon (time scale)."""

    def __init__(self, index: int) -> None:
        assert 0 <= index < N_HORIZONS, f"Horizon index {index} out of range [0, {N_HORIZONS})"
        self._index = index

    @property
    def index(self) -> int:
        return self._index

    @property
    def frames(self) -> int:
        return HORIZON_FRAMES[self._index]

    @property
    def ms(self) -> float:
        return HORIZON_MS[self._index]

    @property
    def seconds(self) -> float:
        return self.ms / 1000.0
