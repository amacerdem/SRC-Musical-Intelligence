"""EventHorizon -- Lightweight lookup wrapper for horizon constants.

Maps a horizon index (0-31) to its physical attributes: frame count,
duration in milliseconds, duration in seconds, and perceptual band
assignment.  Carries no mutable state; constructed, queried, and
discarded.

Source of truth
---------------
- Docs/H3/Contracts/EventHorizon.md         interface contract
- Docs/H3/Registry/HorizonCatalog.md        authoritative 32-horizon catalog
- ear/h3/constants/horizons.py               HORIZON_FRAMES, HORIZON_MS,
                                             BAND_ASSIGNMENTS
"""
from __future__ import annotations

from ..constants.horizons import (
    BAND_ASSIGNMENTS,
    HORIZON_FRAMES,
    HORIZON_MS,
    N_HORIZONS,
)


class EventHorizon:
    """Thin wrapper that maps a horizon index to its physical attributes.

    Parameters
    ----------
    index:
        Horizon index in ``[0, 31]``.

    Raises
    ------
    ValueError
        If *index* is outside ``[0, 31]``.

    Examples
    --------
    >>> eh = EventHorizon(0)
    >>> eh.frames
    1

    >>> EventHorizon(31).frames
    168999

    >>> EventHorizon(8).band
    'meso'
    """

    __slots__ = ("_index",)

    def __init__(self, index: int) -> None:
        if not (0 <= index < N_HORIZONS):
            raise ValueError(
                f"Horizon index must be in [0, {N_HORIZONS - 1}], "
                f"got {index}"
            )
        self._index = index

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def index(self) -> int:
        """The horizon index (0-31)."""
        return self._index

    @property
    def frames(self) -> int:
        """Number of audio frames in this horizon window."""
        return HORIZON_FRAMES[self._index]

    @property
    def ms(self) -> float:
        """Duration of this horizon in milliseconds."""
        return HORIZON_MS[self._index]

    @property
    def seconds(self) -> float:
        """Duration of this horizon in seconds."""
        return self.ms / 1000.0

    @property
    def band(self) -> str:
        """Perceptual band label: ``'micro'``, ``'meso'``, ``'macro'``, or ``'ultra'``."""
        return BAND_ASSIGNMENTS[self._index]

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"EventHorizon(index={self._index}, "
            f"frames={self.frames}, "
            f"ms={self.ms})"
        )
