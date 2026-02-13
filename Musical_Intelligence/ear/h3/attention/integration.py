"""IntegrationWindow -- L2 Integration law window selection.

L2 (Integration) is the bidirectional temporal law.  It centers the
attention window on the current frame ``t``, extending approximately
equally into the past and future.

Window
------
    half = n_frames // 2
    [max(0, t - half),  min(T, t + n_frames - half))

For even ``n_frames`` the split is exactly symmetric.  For odd
``n_frames`` one extra frame falls on the future side.

Properties
----------
- Semi-causal -- uses both past and future frames
- Latency = n_frames // 2 (half the horizon duration)
- Symmetric around current frame when not at boundaries

Cognitive basis
---------------
Gestalt perception, auditory scene analysis, temporal binding.

Source of truth
---------------
- Docs/H3/Laws/L2-Integration.md        (window formula)
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md   Section 6.3
"""

from __future__ import annotations


class IntegrationWindow:
    """L2 Integration law -- bidirectional (symmetric) window selection.

    Stateless and lightweight.  No constructor arguments required.
    """

    def select(self, t: int, n_frames: int, T: int) -> tuple[int, int]:
        """Select the L2 (Integration) window as a half-open range.

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
        >>> w = IntegrationWindow()
        >>> w.select(0, 10, 100)
        (0, 5)
        >>> w.select(99, 10, 100)
        (94, 100)
        >>> w.select(50, 10, 100)
        (45, 55)
        """
        half = n_frames // 2
        start = max(0, t - half)
        end = min(T, t + n_frames - half)
        return (start, end)
