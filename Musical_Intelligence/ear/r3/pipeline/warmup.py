"""WarmupManager -- tracks warm-up zones for R3 features.

Some R3 features require temporal context (autocorrelation windows, EMA
buffers, modulation FFT) before they produce reliable output.  During the
warm-up period, features either output zero or are scaled by a confidence
ramp.

Warm-up tiers
-------------
- **Tier 0 (0 frames)**: Immediately valid.
  Groups A, B, C, D, F, H, J, and K psychoacoustic features [91-96].
- **Tier 1 (344 frames, ~2.0s)**:
  K modulation [83:91]: zero before warmup.
  G tempo/beat/pulse [41:43]: autocorrelation window.
  G other rhythm [45:50]: IOI-based features.
- **Tier 2 (688 frames, ~4.0s)**:
  G syncopation [44]: requires stable tempo + metrical grid.

Source of truth
---------------
- Docs/R3/R3-SPECTRAL-ARCHITECTURE.md  Section 12: Warm-up table
- Docs/R3/Pipeline/StateManagement.md  Confidence ramp
"""

from __future__ import annotations

from typing import FrozenSet


# ======================================================================
# Warm-up feature sets
# ======================================================================

# Features that output zero until 344 frames have elapsed
WARMUP_344_ZERO: FrozenSet[int] = frozenset(
    list(range(83, 91))  # K modulation spectrum + centroid/bandwidth
)

# Features that use confidence ramp min(1.0, t/344)
WARMUP_344_RAMP: FrozenSet[int] = frozenset({
    41, 42, 43,      # G tempo, beat_strength, pulse_clarity
    45, 46, 47, 48, 49, 50,  # G metricality through rhythmic_regularity
})

# Features that output zero until 688 frames have elapsed
WARMUP_688_ZERO: FrozenSet[int] = frozenset({
    44,  # G syncopation_index
})

# All warm-up features combined
WARMUP_ALL: FrozenSet[int] = WARMUP_344_ZERO | WARMUP_344_RAMP | WARMUP_688_ZERO


class WarmupManager:
    """Tracks warm-up state for R3 features that need temporal context.

    Features without warm-up requirements are always fully confident.
    Features in the warm-up zone either produce zero output (modulation,
    syncopation) or are scaled by a linear confidence ramp (rhythm-based
    features).

    Usage
    -----
    ::

        wm = WarmupManager()
        conf = wm.get_confidence(frame_count=100, feature_index=83)
        # → 0.0 (modulation not yet valid)

        conf = wm.get_confidence(frame_count=200, feature_index=41)
        # → 0.581 (tempo_estimate at 58.1% confidence)

        wm.is_warmed_up(frame_count=688)
        # → True (all features fully warmed)
    """

    # Expose as class constants
    WARMUP_344_FEATURES: FrozenSet[int] = WARMUP_344_ZERO | WARMUP_344_RAMP
    WARMUP_688_FEATURES: FrozenSet[int] = WARMUP_688_ZERO

    def is_warmed_up(self, frame_count: int) -> bool:
        """Check whether ALL features are fully warmed.

        Parameters
        ----------
        frame_count : int
            Number of frames processed so far.

        Returns
        -------
        bool
            ``True`` when ``frame_count >= 688`` (longest warm-up).
        """
        return frame_count >= 688

    def get_confidence(self, frame_count: int, feature_index: int) -> float:
        """Get confidence multiplier for a feature at a given frame.

        Parameters
        ----------
        frame_count : int
            Number of frames processed so far (0-indexed).
        feature_index : int
            R3 feature index in ``[0, 97)``.

        Returns
        -------
        float
            Confidence in ``[0.0, 1.0]``:
            - ``1.0`` for features with no warm-up requirement.
            - ``0.0`` for zero-output features before their threshold.
            - Linear ramp ``min(1.0, t/344)`` for ramp features.
        """
        # No warm-up needed
        if feature_index not in WARMUP_ALL:
            return 1.0

        # 688-frame zero features (syncopation)
        if feature_index in WARMUP_688_ZERO:
            return 1.0 if frame_count >= 688 else 0.0

        # 344-frame zero features (modulation spectrum)
        if feature_index in WARMUP_344_ZERO:
            return 1.0 if frame_count >= 344 else 0.0

        # 344-frame ramp features (rhythm)
        if feature_index in WARMUP_344_RAMP:
            return min(1.0, frame_count / 344.0)

        return 1.0

    def get_warmup_frames(self, feature_index: int) -> int:
        """Get the warm-up duration for a feature.

        Parameters
        ----------
        feature_index : int
            R3 feature index in ``[0, 97)``.

        Returns
        -------
        int
            Number of frames needed for full confidence.
        """
        if feature_index in WARMUP_688_ZERO:
            return 688
        if feature_index in WARMUP_344_ZERO:
            return 344
        if feature_index in WARMUP_344_RAMP:
            return 344
        return 0

    def __repr__(self) -> str:
        return (
            f"WarmupManager("
            f"tier1_zero={len(WARMUP_344_ZERO)}, "
            f"tier1_ramp={len(WARMUP_344_RAMP)}, "
            f"tier2={len(WARMUP_688_ZERO)})"
        )
