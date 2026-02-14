"""Cognitive units sub-package — 9 units, 96 models, 1006D total.

Units
-----
SPU : Spectral Processing Unit (perceptual, 99D)
STU : Sensorimotor Timing Unit (sensorimotor, 148D)
IMU : Integrative Memory Unit (mnemonic, 159D)
ASU : Auditory Salience Unit (salience, 94D)
NDU : Novelty Detection Unit (salience, 94D)
MPU : Motor Planning Unit (sensorimotor, 104D)
PCU : Predictive Coding Unit (mnemonic, 94D)
ARU : Affective Resonance Unit (mesolimbic, 120D)
RPU : Reward Processing Unit (mesolimbic, 94D)
"""
from __future__ import annotations

from .aru import ARUUnit
from .asu import ASUUnit
from .imu import IMUUnit
from .mpu import MPUUnit
from .ndu import NDUUnit
from .pcu import PCUUnit
from .rpu import RPUUnit
from .spu import SPUUnit
from .stu import STUUnit

__all__ = [
    "SPUUnit",
    "STUUnit",
    "IMUUnit",
    "ASUUnit",
    "NDUUnit",
    "MPUUnit",
    "PCUUnit",
    "ARUUnit",
    "RPUUnit",
]
