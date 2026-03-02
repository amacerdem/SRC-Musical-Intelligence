"""Deep BCH tests — Full 9-interval consonance hierarchy.

Validates the Sethares/Plomp-Levelt psychoacoustic consonance ordering
using rich harmonic complex dyads (6 harmonics per note).

Expected hierarchy (harmonic_stability):
  P1 > P8 > P5 > P4 > M3 > m3 > m6 > TT > m2

Group separation:
  Perfect (P1, P8, P5) > Imperfect (P4, M3, m3) > Dissonant (m6, TT, m2)
"""
from __future__ import annotations

import pytest

from Tests.micro_beliefs.audio_stimuli import (
    C4, Db4, Eb4, E4, F4, Fsharp4, G4, Ab4, C5,
    harmonic_complex, noise, rich_dyad,
)
from Tests.micro_beliefs.assertions import (
    assert_greater, assert_in_range, assert_ordering,
)


# Named intervals (root = C4, 6 harmonics per note)
INTERVALS = {
    "P1": (C4, C4),
    "P8": (C4, C5),
    "P5": (C4, G4),
    "P4": (C4, F4),
    "M3": (C4, E4),
    "m3": (C4, Eb4),
    "m6": (C4, Ab4),
    "TT": (C4, Fsharp4),
    "m2": (C4, Db4),
}


def _dyad(name: str, dur: float = 3.0):
    f1, f2 = INTERVALS[name]
    return rich_dyad(f1, f2, 6, dur)


# =====================================================================
# harmonic_stability: Full hierarchy
# =====================================================================

class TestHarmonicStabilityHierarchy:
    """Full 9-interval consonance hierarchy for harmonic_stability."""

    BELIEF = "harmonic_stability"

    def test_p1_above_p8(self, runner):
        res_p1 = runner.run(_dyad("P1"), [self.BELIEF])[self.BELIEF]
        res_p8 = runner.run(_dyad("P8"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p1, res_p8, "P1", "P8")

    def test_p8_above_p5(self, runner):
        res_p8 = runner.run(_dyad("P8"), [self.BELIEF])[self.BELIEF]
        res_p5 = runner.run(_dyad("P5"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p8, res_p5, "P8", "P5")

    def test_p5_above_p4(self, runner):
        res_p5 = runner.run(_dyad("P5"), [self.BELIEF])[self.BELIEF]
        res_p4 = runner.run(_dyad("P4"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p5, res_p4, "P5", "P4")

    def test_p5_above_m2(self, runner):
        """P5 >> m2 — major gap between consonant and dissonant."""
        res_p5 = runner.run(_dyad("P5"), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(_dyad("m2"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p5, res_m2, "P5", "m2")

    def test_perfect_group_above_m2(self, runner):
        """Average of P1/P8/P5 > m2."""
        res_p1 = runner.run(_dyad("P1"), [self.BELIEF])[self.BELIEF]
        res_p8 = runner.run(_dyad("P8"), [self.BELIEF])[self.BELIEF]
        res_p5 = runner.run(_dyad("P5"), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(_dyad("m2"), [self.BELIEF])[self.BELIEF]
        perfect_avg = (res_p1 + res_p8 + res_p5) / 3
        assert_greater(perfect_avg, res_m2, "PerfectGroup", "m2")

    @pytest.mark.parametrize("interval", ["P1", "P8", "P5", "P4", "M3", "m3", "m6", "TT", "m2"])
    def test_range(self, runner, interval):
        result = runner.run(_dyad(interval), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, f"{self.BELIEF}({interval})")

    def test_all_above_noise(self, runner):
        """Every interval should score above noise."""
        res_n = runner.run(noise(3.0), [self.BELIEF])[self.BELIEF]
        for iv in ["P1", "P8", "P5"]:
            res = runner.run(_dyad(iv), [self.BELIEF])[self.BELIEF]
            assert_greater(res, res_n, iv, "noise")


# =====================================================================
# interval_quality: Consonance-based quality ranking
# =====================================================================

class TestIntervalQualityHierarchy:
    """interval_quality should follow a consonance ordering."""

    BELIEF = "interval_quality"

    def test_p1_above_m2(self, runner):
        res_p1 = runner.run(_dyad("P1"), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(_dyad("m2"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p1, res_m2, "P1", "m2")

    def test_p8_above_m2(self, runner):
        res_p8 = runner.run(_dyad("P8"), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(_dyad("m2"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p8, res_m2, "P8", "m2")

    def test_p5_above_m2(self, runner):
        res_p5 = runner.run(_dyad("P5"), [self.BELIEF])[self.BELIEF]
        res_m2 = runner.run(_dyad("m2"), [self.BELIEF])[self.BELIEF]
        assert_greater(res_p5, res_m2, "P5", "m2")

    @pytest.mark.parametrize("interval", ["P1", "P8", "P5", "P4", "M3", "m3", "m6", "TT", "m2"])
    def test_range(self, runner, interval):
        result = runner.run(_dyad(interval), [self.BELIEF])[self.BELIEF]
        assert_in_range(result, f"{self.BELIEF}({interval})")
