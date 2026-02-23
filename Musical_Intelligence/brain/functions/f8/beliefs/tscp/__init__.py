"""F8 Beliefs -- TSCP (Training-Specific Cortical Plasticity).

2 beliefs derived from TSCP mechanism output:
    1 Core:      trained_timbre_recognition (tau=0.90)
    1 Appraisal: plasticity_magnitude
"""

from .plasticity_magnitude import PlasticityMagnitude
from .trained_timbre_recognition import TrainedTimbreRecognition

__all__ = [
    "TrainedTimbreRecognition",
    "PlasticityMagnitude",
]
