"""F7 Beliefs — HGSIC (Hierarchical Groove & Sensorimotor Integration Circuit).

6 beliefs derived from HGSIC mechanism output:
    1 Core:         groove_quality (tau=0.55)
    4 Appraisal:    beat_prominence, meter_structure, auditory_motor_coupling,
                    motor_preparation
    1 Anticipation: groove_trajectory
"""

from .auditory_motor_coupling import AuditoryMotorCoupling
from .beat_prominence import BeatProminence
from .groove_quality import GrooveQuality
from .groove_trajectory import GrooveTrajectory
from .meter_structure import MeterStructure
from .motor_preparation import MotorPreparation

__all__ = [
    "GrooveQuality",
    "BeatProminence",
    "MeterStructure",
    "AuditoryMotorCoupling",
    "MotorPreparation",
    "GrooveTrajectory",
]
