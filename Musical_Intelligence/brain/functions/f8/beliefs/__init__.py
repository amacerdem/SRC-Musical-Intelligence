"""F8 Learning and Plasticity -- Beliefs.

14 beliefs organized by mechanism:
    tscp/ -- 2 beliefs (1 Core, 1 Appraisal)
    esme/ -- 5 beliefs (1 Core, 3 Appraisal, 1 Anticipation)
    ednr/ -- 2 beliefs (1 Core, 1 Appraisal)
    slee/ -- 3 beliefs (1 Core, 2 Appraisal)
    ect/  -- 2 beliefs (1 Appraisal, 1 Anticipation)

All mechanisms are independent (depth 0).
"""

from .ect import CompartmentalizationCost, TransferLimitation
from .ednr import NetworkSpecialization, WithinConnectivity
from .esme import (
    ExpertiseEnhancement,
    ExpertiseTrajectory,
    PitchMmn,
    RhythmMmn,
    TimbreMmn,
)
from .slee import DetectionAccuracy, MultisensoryBinding, StatisticalModel
from .tscp import PlasticityMagnitude, TrainedTimbreRecognition

__all__ = [
    # TSCP beliefs (depth 0)
    "TrainedTimbreRecognition",
    "PlasticityMagnitude",
    # ESME beliefs (depth 0)
    "ExpertiseEnhancement",
    "PitchMmn",
    "RhythmMmn",
    "TimbreMmn",
    "ExpertiseTrajectory",
    # EDNR beliefs (depth 0)
    "NetworkSpecialization",
    "WithinConnectivity",
    # SLEE beliefs (depth 0)
    "StatisticalModel",
    "DetectionAccuracy",
    "MultisensoryBinding",
    # ECT beliefs (depth 0)
    "CompartmentalizationCost",
    "TransferLimitation",
]
