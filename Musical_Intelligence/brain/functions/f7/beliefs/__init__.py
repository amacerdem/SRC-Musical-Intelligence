"""F7 Motor & Timing — Beliefs.

17 beliefs organized by mechanism:
    peom/  — 5 beliefs (2 Core, 2 Appraisal, 1 Anticipation)
    hgsic/ — 6 beliefs (1 Core, 4 Appraisal, 1 Anticipation)
    hmce/  — 6 beliefs (1 Core, 3 Appraisal, 2 Anticipation)

Dependency chain:
    PEOM  (Depth 0) — independent, reads R3/H3 directly.
    HGSIC (Depth 0) — independent, reads R3/H3 directly.
    HMCE  (Depth 0) — independent, reads R3/H3 directly.
"""

from .peom import (
    KinematicEfficiency,
    NextBeatPred,
    PeriodEntrainment,
    PeriodLockStrength,
    TimingPrecision,
)
from .hgsic import (
    AuditoryMotorCoupling,
    BeatProminence,
    GrooveQuality,
    GrooveTrajectory,
    MeterStructure,
    MotorPreparation,
)
from .hmce import (
    ContextDepth,
    LongContext,
    MediumContext,
    PhraseBoundaryPred,
    ShortContext,
    StructurePred,
)

__all__ = [
    # PEOM beliefs (depth 0 — no upstream dependency)
    "PeriodEntrainment",
    "KinematicEfficiency",
    "TimingPrecision",
    "PeriodLockStrength",
    "NextBeatPred",
    # HGSIC beliefs (depth 0 — no upstream dependency)
    "GrooveQuality",
    "BeatProminence",
    "MeterStructure",
    "AuditoryMotorCoupling",
    "MotorPreparation",
    "GrooveTrajectory",
    # HMCE beliefs (depth 0 — no upstream dependency)
    "ContextDepth",
    "ShortContext",
    "MediumContext",
    "LongContext",
    "PhraseBoundaryPred",
    "StructurePred",
]
