"""F1 Sensory Processing — Beliefs.

10 beliefs organized by mechanism:
    bch/  — 4 beliefs (1 Core, 2 Appraisal, 1 Anticipation)
    mpg/  — 2 beliefs (1 Appraisal, 1 Anticipation)
    pscl/ — 2 beliefs (1 Core, 1 Anticipation)
    pccr/ — 2 beliefs (1 Core, 1 Appraisal)

Dependency chain:
    BCH  (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2)
    MPG  (Depth 0) — independent, no downstream F1 beliefs depend on it.
    BCH beliefs require BCH mechanism only.
    MPG beliefs require MPG mechanism only.
    PSCL beliefs require PSCL mechanism (which requires BCH).
    PCCR beliefs require PCCR mechanism (which requires BCH + PSCL).
"""

from .bch import (
    ConsonanceTrajectory,
    HarmonicStability,
    HarmonicTemplateMatch,
    IntervalQuality,
)
from .mpg import ContourContinuation, MelodicContourTracking
from .pccr import OctaveEquivalence, PitchIdentity
from .pscl import PitchContinuation, PitchProminence

__all__ = [
    # BCH beliefs (depth 0 — no upstream dependency)
    "HarmonicStability",
    "IntervalQuality",
    "HarmonicTemplateMatch",
    "ConsonanceTrajectory",
    # MPG beliefs (depth 0 — no upstream dependency)
    "MelodicContourTracking",
    "ContourContinuation",
    # PSCL beliefs (depth 1 — requires BCH)
    "PitchProminence",
    "PitchContinuation",
    # PCCR beliefs (depth 2 — requires BCH + PSCL)
    "PitchIdentity",
    "OctaveEquivalence",
]
