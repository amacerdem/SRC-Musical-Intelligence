"""PredictionWindow -- L1 Prediction law window selection.

L1 (Prediction) is the anticipatory temporal law.  It places the attention
window entirely in the future, looking forward from the current frame ``t``.

Window
------
    [t,  min(T, t + n_frames))

The window includes up to ``n_frames`` frames starting at (and including)
the current frame ``t``.  At the track end boundary the window is
truncated at the final frame.

Properties
----------
- Non-causal -- requires future frames
- Latency = n_frames (full horizon duration)
- Mirror of L0

Cognitive basis
---------------
Predictive coding, expectation formation, Bayesian brain hypothesis.

Source of truth
---------------
- Docs/H3/Laws/L1-Prediction.md         (window formula)
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md   Section 6.2
"""

from __future__ import annotations


class PredictionWindow:
    """L1 Prediction law -- anticipatory (future-only) window selection.

    Stateless and lightweight.  No constructor arguments required.
    """

    def select(self, t: int, n_frames: int, T: int) -> tuple[int, int]:
        """Select the L1 (Prediction) window as a half-open range.

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
        >>> w = PredictionWindow()
        >>> w.select(99, 10, 100)
        (99, 100)
        >>> w.select(90, 10, 100)
        (90, 100)
        >>> w.select(50, 10, 100)
        (50, 60)
        """
        start = t
        end = min(T, t + n_frames)
        return (start, end)
