"""F4 beliefs — 13 total (4C + 7A + 2N).

MEAMN (7): 3 Core + 3 Appraisal + 1 Anticipation — implemented in kernel v4.0
MMP (3):   2 Appraisal + 1 Anticipation
HCMC (3):  1 Core + 2 Appraisal
"""
from .meamn import (
    AutobiographicalRetrieval,
    EmotionalColoring,
    MemoryVividness,
    NostalgiaIntensity,
    RetrievalProbability,
    SelfRelevance,
    VividnessTrajectory,
)
from .mmp import MelodicRecognition, MemoryPreservation, MemoryScaffoldPred
from .hcmc import ConsolidationStrength, EpisodicBoundary, EpisodicEncoding

__all__ = [
    # MEAMN (7)
    "AutobiographicalRetrieval",
    "NostalgiaIntensity",
    "EmotionalColoring",
    "RetrievalProbability",
    "MemoryVividness",
    "SelfRelevance",
    "VividnessTrajectory",
    # MMP (3)
    "MelodicRecognition",
    "MemoryPreservation",
    "MemoryScaffoldPred",
    # HCMC (3)
    "EpisodicEncoding",
    "EpisodicBoundary",
    "ConsolidationStrength",
]
