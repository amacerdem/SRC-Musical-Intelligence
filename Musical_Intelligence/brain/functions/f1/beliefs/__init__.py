"""F1 Sensory Processing — Beliefs.

14 beliefs organized by mechanism:
    bch/  — 4 beliefs (1 Core, 2 Appraisal, 1 Anticipation)
    csg/  — 1 belief  (1 Appraisal)
    miaa/ — 2 beliefs (1 Core, 1 Anticipation)
    mpg/  — 2 beliefs (1 Appraisal, 1 Anticipation)
    sded/ — 1 belief  (1 Appraisal)
    pscl/ — 2 beliefs (1 Core, 1 Anticipation)
    pccr/ — 2 beliefs (1 Core, 1 Appraisal)

Dependency chain:
    BCH  (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2)
    CSG  (Depth 0) — independent, no downstream F1 beliefs depend on it.
    MIAA (Depth 0) — independent, no downstream F1 beliefs depend on it.
    MPG  (Depth 0) — independent, no downstream F1 beliefs depend on it.
    SDED (Depth 0) — independent, no downstream F1 beliefs depend on it.
    BCH beliefs require BCH mechanism only.
    CSG beliefs require CSG mechanism only.
    MIAA beliefs require MIAA mechanism only.
    MPG beliefs require MPG mechanism only.
    SDED beliefs require SDED mechanism only.
    PSCL beliefs require PSCL mechanism (which requires BCH).
    PCCR beliefs require PCCR mechanism (which requires BCH + PSCL).
"""

from .bch import (
    ConsonanceTrajectory,
    HarmonicStability,
    HarmonicTemplateMatch,
    IntervalQuality,
)
from .csg import ConsonanceSalienceGradient
from .miaa import ImageryRecognition, TimbralCharacter
from .mpg import ContourContinuation, MelodicContourTracking
from .pccr import OctaveEquivalence, PitchIdentity
from .pscl import PitchContinuation, PitchProminence
from .sded import SpectralComplexity

__all__ = [
    # BCH beliefs (depth 0 — no upstream dependency)
    "HarmonicStability",
    "IntervalQuality",
    "HarmonicTemplateMatch",
    "ConsonanceTrajectory",
    # CSG beliefs (depth 0 — no upstream dependency)
    "ConsonanceSalienceGradient",
    # MIAA beliefs (depth 0 — no upstream dependency)
    "TimbralCharacter",
    "ImageryRecognition",
    # MPG beliefs (depth 0 — no upstream dependency)
    "MelodicContourTracking",
    "ContourContinuation",
    # SDED beliefs (depth 0 — no upstream dependency)
    "SpectralComplexity",
    # PSCL beliefs (depth 1 — requires BCH)
    "PitchProminence",
    "PitchContinuation",
    # PCCR beliefs (depth 2 — requires BCH + PSCL)
    "PitchIdentity",
    "OctaveEquivalence",
]
