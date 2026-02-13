"""MemoryWindow -- L0 Memory law window selection.

L0 (Memory) is the causal temporal law.  It places the attention window
entirely in the past, looking backward from the current frame ``t``.

Window
------
    [max(0, t - n_frames + 1),  t + 1)

The window includes up to ``n_frames`` frames ending at (and including)
the current frame ``t``.  At the track start boundary the window is
truncated at frame 0.

Properties
----------
- Fully causal -- no future frames required
- Zero latency (real-time capable)
- Peak attention at the current frame ``t``

Cognitive basis
---------------
Echoic memory, auditory streaming, sensory trace decay.

Source of truth
---------------
- Docs/H3/Laws/L0-Memory.md            (window formula, cognitive basis)
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md  Section 6.1
"""

from __future__ import annotations


class MemoryWindow:
    """L0 Memory law -- causal (past-only) window selection.

    Stateless and lightweight.  No constructor arguments required.
    """

    def select(self, t: int, n_frames: int, T: int) -> tuple[int, int]:
        """Select the L0 (Memory) window as a half-open range.

        Parameters
        ----------
        t : int
            Current frame index.
        n_frames : int
            Horizon frame count (window size).
        T : int
            Total number of frames in the signal.

        Returns
        -------
        tuple[int, int]
            ``(start, end)`` half-open range ``[start, end)``.
            ``start`` is never negative; ``end`` never exceeds ``T``.

        Examples
        --------
        >>> w = MemoryWindow()
        >>> w.select(0, 10, 100)
        (0, 1)
        >>> w.select(9, 10, 100)
        (0, 10)
        >>> w.select(50, 10, 100)
        (41, 51)
        """
        start = max(0, t - n_frames + 1)
        end = min(t + 1, T)
        return (start, end)
