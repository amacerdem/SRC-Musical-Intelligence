"""WarmUpHandler -- warm-up zone analysis for H3 temporal windows.

At the boundaries of a sequence, the attention window is only partially
filled.  This module provides utilities to determine which frames are
within the warm-up zone and how many frames are needed before a given
(horizon, law) combination produces reliable output.

Per-law warm-up patterns
------------------------
- **L0 (Memory)**: Start of sequence.  First ``n_frames`` frames have
  incomplete past context.  Frame ``t`` is fully warmed when
  ``t >= n_frames - 1``.
- **L1 (Prediction)**: End of sequence.  Last ``n_frames`` frames have
  incomplete future context.  Frame ``t`` is fully warmed when
  ``t <= T - n_frames``.
- **L2 (Integration)**: Both boundaries.  First and last ``n_frames // 2``
  frames have incomplete context.  Frame ``t`` is fully warmed when
  ``t >= n_frames // 2`` and ``t <= T - n_frames // 2``.

Source of truth
---------------
- Docs/H3/Pipeline/WarmUp.md   per-law patterns, duration by band
"""

from __future__ import annotations

from ..constants.horizons import HORIZON_FRAMES
from ..constants.laws import LAW_MEMORY, LAW_PREDICTION, LAW_INTEGRATION


class WarmUpHandler:
    """Stateless utility for H3 warm-up zone analysis.

    Warm-up zones are regions near sequence boundaries where the attention
    window is truncated, producing less reliable morph outputs.  This class
    answers three questions for any ``(horizon, law, T)`` combination:

    1. How many frames must pass before output is reliable?
    2. Is a specific frame fully warmed?
    3. What fraction of frames in a sequence are fully warmed?
    """

    # ------------------------------------------------------------------
    # warmup_frames
    # ------------------------------------------------------------------

    @staticmethod
    def warmup_frames(horizon: int, law: int) -> int:
        """Number of frames needed before output is fully reliable.

        Parameters
        ----------
        horizon : int
            Horizon index in ``[0, 31]``.
        law : int
            Law index: 0 (Memory), 1 (Prediction), 2 (Integration).

        Returns
        -------
        int
            Number of warm-up frames.  For L0 and L1 this equals
            ``n_frames``; for L2 it equals ``n_frames // 2``.

        Raises
        ------
        ValueError
            If *horizon* or *law* is out of range.
        """
        n_frames = _get_n_frames(horizon)
        _validate_law(law)

        if law == LAW_MEMORY:
            return n_frames
        elif law == LAW_PREDICTION:
            return n_frames
        else:  # LAW_INTEGRATION
            return n_frames // 2

    # ------------------------------------------------------------------
    # is_warmed
    # ------------------------------------------------------------------

    @staticmethod
    def is_warmed(t: int, horizon: int, law: int, T: int) -> bool:
        """Check whether frame *t* has a fully populated attention window.

        Parameters
        ----------
        t : int
            Frame index in ``[0, T)``.
        horizon : int
            Horizon index in ``[0, 31]``.
        law : int
            Law index: 0 (Memory), 1 (Prediction), 2 (Integration).
        T : int
            Total number of frames in the sequence.

        Returns
        -------
        bool
            ``True`` if frame *t* has a complete (non-truncated) window.

        Raises
        ------
        ValueError
            If *horizon* or *law* is out of range.
        """
        n_frames = _get_n_frames(horizon)
        _validate_law(law)

        if law == LAW_MEMORY:
            # Past window: first full window at t = n_frames - 1
            return t >= n_frames - 1

        elif law == LAW_PREDICTION:
            # Future window: last full window at t = T - n_frames
            return t <= T - n_frames

        else:  # LAW_INTEGRATION
            # Bidirectional: half-window must fit on both sides
            half = n_frames // 2
            return t >= half and t <= T - (n_frames - half)

    # ------------------------------------------------------------------
    # warmup_fraction
    # ------------------------------------------------------------------

    @staticmethod
    def warmup_fraction(horizon: int, T: int) -> float:
        """Fraction of frames that are fully warmed (worst-case across laws).

        Returns the fraction for the most conservative case (L0 or L1,
        which require ``n_frames`` warm-up).  This represents the minimum
        fraction of usable frames regardless of which law is applied.

        Parameters
        ----------
        horizon : int
            Horizon index in ``[0, 31]``.
        T : int
            Total number of frames in the sequence.

        Returns
        -------
        float
            Value in ``[0.0, 1.0]``.  Returns ``0.0`` when the sequence
            is shorter than the horizon (ultra horizons on short audio).

        Raises
        ------
        ValueError
            If *horizon* is out of range.
        """
        n_frames = _get_n_frames(horizon)

        if T <= 0:
            return 0.0

        # For L0: fully warmed frames are [n_frames - 1, T - 1]
        #   count = T - n_frames + 1    (if T >= n_frames, else 0)
        # For L1: fully warmed frames are [0, T - n_frames]
        #   count = T - n_frames + 1    (same)
        # For L2: both boundaries eat n_frames // 2
        #   count = T - n_frames + 1    (approximately same)
        #
        # Use L0/L1 formula as the worst case for Memory/Prediction:
        warmed_count = max(0, T - n_frames + 1)
        return warmed_count / T


# ======================================================================
# Module-level helpers
# ======================================================================

def _get_n_frames(horizon: int) -> int:
    """Look up frame count for a horizon index, with validation."""
    if not (0 <= horizon <= 31):
        raise ValueError(
            f"horizon must be in [0, 31], got {horizon}"
        )
    return HORIZON_FRAMES[horizon]


def _validate_law(law: int) -> None:
    """Raise ``ValueError`` if law is not 0, 1, or 2."""
    if law not in (LAW_MEMORY, LAW_PREDICTION, LAW_INTEGRATION):
        raise ValueError(
            f"law must be 0, 1, or 2, got {law}"
        )
