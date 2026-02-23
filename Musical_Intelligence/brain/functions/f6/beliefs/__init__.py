"""F6 Reward and Motivation — Beliefs.

16 beliefs organized by mechanism:
    srp/  — 11 beliefs (5 Core, 3 Appraisal, 3 Anticipation)
    daed/ —  5 beliefs (4 Appraisal, 1 Anticipation)

Dependency chain:
    SRP  (Depth 0) — independent.
    DAED (Depth 0) — independent; wanting_ramp feeds wanting.predict() as context.
    SRP beliefs require SRP mechanism only.
    DAED beliefs require DAED mechanism only.
"""

from .daed import (
    DaCaudate,
    DaNacc,
    DissociationIndex,
    TemporalPhase,
    WantingRamp,
)
from .srp import (
    ChillsProximity,
    HarmonicTension,
    Liking,
    PeakDetection,
    Pleasure,
    PredictionError,
    PredictionMatch,
    ResolutionExpectation,
    RewardForecast,
    Tension,
    Wanting,
)

__all__ = [
    # SRP Core beliefs
    "Wanting",
    "Liking",
    "Pleasure",
    "PredictionError",
    "Tension",
    # SRP Appraisal beliefs
    "PredictionMatch",
    "PeakDetection",
    "HarmonicTension",
    # SRP Anticipation beliefs
    "ChillsProximity",
    "ResolutionExpectation",
    "RewardForecast",
    # DAED Appraisal beliefs
    "DaCaudate",
    "DaNacc",
    "DissociationIndex",
    "TemporalPhase",
    # DAED Anticipation beliefs
    "WantingRamp",
]
