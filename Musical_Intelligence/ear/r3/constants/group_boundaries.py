from __future__ import annotations

from typing import NamedTuple, Tuple


class R3GroupBoundary(NamedTuple):
    letter: str
    name: str
    start: int
    end: int
    dim: int
    stage: int


R3_GROUP_BOUNDARIES: Tuple[R3GroupBoundary, ...] = (
    R3GroupBoundary("A", "Consonance",                0,   7,   7, 1),
    R3GroupBoundary("B", "Energy",                    7,  12,   5, 1),
    R3GroupBoundary("C", "Timbre",                   12,  21,   9, 1),
    R3GroupBoundary("D", "Change",                   21,  25,   4, 1),
    R3GroupBoundary("F", "Pitch & Chroma",           25,  41,  16, 1),
    R3GroupBoundary("G", "Rhythm & Groove",          41,  51,  10, 2),
    R3GroupBoundary("H", "Harmony & Tonality",       51,  63,  12, 2),
    R3GroupBoundary("J", "Timbre Extended",          63,  83,  20, 1),
    R3GroupBoundary("K", "Modulation & Psychoacoustic", 83, 97, 14, 1),
)

assert len(R3_GROUP_BOUNDARIES) == 9
assert sum(g.dim for g in R3_GROUP_BOUNDARIES) == 97
assert all(g.end - g.start == g.dim for g in R3_GROUP_BOUNDARIES)
assert R3_GROUP_BOUNDARIES[0].start == 0
assert R3_GROUP_BOUNDARIES[-1].end == 97
assert all(
    R3_GROUP_BOUNDARIES[i].end == R3_GROUP_BOUNDARIES[i + 1].start
    for i in range(len(R3_GROUP_BOUNDARIES) - 1)
)

# Stage assignments: 1={A,B,C,D,F,J,K}, 2={G,H}
_STAGE_1 = frozenset(g.letter for g in R3_GROUP_BOUNDARIES if g.stage == 1)
_STAGE_2 = frozenset(g.letter for g in R3_GROUP_BOUNDARIES if g.stage == 2)
assert _STAGE_1 == frozenset({"A", "B", "C", "D", "F", "J", "K"})
assert _STAGE_2 == frozenset({"G", "H"})

# Slice constants -- (start, end) tuples for indexing into the 97D R3 vector
R3_CONSONANCE: Tuple[int, int] = (0, 7)
R3_ENERGY: Tuple[int, int] = (7, 12)
R3_TIMBRE: Tuple[int, int] = (12, 21)
R3_CHANGE: Tuple[int, int] = (21, 25)
R3_PITCH_CHROMA: Tuple[int, int] = (25, 41)
R3_RHYTHM_GROOVE: Tuple[int, int] = (41, 51)
R3_HARMONY_TONALITY: Tuple[int, int] = (51, 63)
R3_TIMBRE_EXTENDED: Tuple[int, int] = (63, 83)
R3_MODULATION_PSYCHO: Tuple[int, int] = (83, 97)
