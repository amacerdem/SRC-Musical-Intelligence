"""F3 Attention & Salience — Beliefs.

15 beliefs organized by mechanism:
    snem/ — 5 beliefs (2 Core, 1 Appraisal, 2 Anticipation)
    iacm/ — 4 beliefs (1 Core, 2 Appraisal, 1 Anticipation)
    csg/  — 4 beliefs (1 Core, 2 Appraisal, 1 Anticipation) — cross-function from F1
    aacm/ — 2 beliefs (2 Appraisal)

Dependency chain:
    SNEM (Depth 0) — independent, reads R³/H³ directly.
    IACM (Depth 0) — independent, reads R³/H³ directly.
    CSG  (Depth 0) — F1 primary, cross-function to F3.
    AACM (Depth 1) — reads CSG [F1 cross-function].
"""

from .snem import (
    BeatEntrainment,
    BeatOnsetPred,
    MeterHierarchy,
    MeterPositionPred,
    SelectiveGain,
)
from .iacm import (
    AttentionCapture,
    AttentionShiftPred,
    ObjectSegregation,
    PrecisionWeighting,
)
from .csg import (
    ConsonanceValenceMapping,
    ProcessingLoadPred,
    SalienceNetworkActivation,
    SensoryLoad,
)
from .aacm import (
    AestheticEngagement,
    SavoringEffect,
)

__all__ = [
    # SNEM beliefs (depth 0 — no upstream dependency)
    "BeatEntrainment",
    "MeterHierarchy",
    "SelectiveGain",
    "BeatOnsetPred",
    "MeterPositionPred",
    # IACM beliefs (depth 0 — no upstream dependency)
    "AttentionCapture",
    "ObjectSegregation",
    "PrecisionWeighting",
    "AttentionShiftPred",
    # CSG beliefs (depth 0 — F1 cross-function)
    "SalienceNetworkActivation",
    "SensoryLoad",
    "ConsonanceValenceMapping",
    "ProcessingLoadPred",
    # AACM beliefs (depth 1 — reads CSG)
    "AestheticEngagement",
    "SavoringEffect",
]
