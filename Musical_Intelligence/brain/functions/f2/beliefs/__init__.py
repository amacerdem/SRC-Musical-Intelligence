"""F2 Pattern Recognition & Prediction — Beliefs.

15 beliefs organized by mechanism:
    htp/  — 5 beliefs (2 Core, 1 Appraisal, 2 Anticipation)
    sph/  — 4 beliefs (1 Core, 2 Appraisal, 1 Anticipation)
    icem/ — 6 beliefs (1 Core, 3 Appraisal, 2 Anticipation)

Dependency chain:
    HTP  (Depth 0) — independent, reads R³/H³ directly.
    SPH  (Depth 0) — independent, reads R³/H³ directly.
    ICEM (Depth 0) — independent, reads R³/H³ directly.
"""

from .htp import (
    AbstractFuture,
    HierarchyCoherence,
    MidlevelFuture,
    PredictionAccuracy,
    PredictionHierarchy,
)
from .icem import (
    ArousalChangePred,
    ArousalScaling,
    DefenseCascade,
    InformationContent,
    ValenceInversion,
    ValenceShiftPred,
)
from .sph import (
    ErrorPropagation,
    OscillatorySignature,
    SequenceCompletion,
    SequenceMatch,
)

__all__ = [
    # HTP beliefs (depth 0 — no upstream dependency)
    "PredictionHierarchy",
    "PredictionAccuracy",
    "HierarchyCoherence",
    "AbstractFuture",
    "MidlevelFuture",
    # SPH beliefs (depth 0 — no upstream dependency)
    "SequenceMatch",
    "ErrorPropagation",
    "OscillatorySignature",
    "SequenceCompletion",
    # ICEM beliefs (depth 0 — no upstream dependency)
    "InformationContent",
    "ArousalScaling",
    "ValenceInversion",
    "DefenseCascade",
    "ArousalChangePred",
    "ValenceShiftPred",
]
