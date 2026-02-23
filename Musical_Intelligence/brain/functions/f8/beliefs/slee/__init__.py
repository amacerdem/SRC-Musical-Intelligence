"""F8 Beliefs -- SLEE (Statistical Learning and Exposure Effects).

3 beliefs derived from SLEE mechanism output:
    1 Core:      statistical_model (tau=0.88)
    2 Appraisal: detection_accuracy, multisensory_binding
"""

from .detection_accuracy import DetectionAccuracy
from .multisensory_binding import MultisensoryBinding
from .statistical_model import StatisticalModel

__all__ = [
    "StatisticalModel",
    "DetectionAccuracy",
    "MultisensoryBinding",
]
