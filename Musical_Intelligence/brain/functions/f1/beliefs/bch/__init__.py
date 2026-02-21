"""F1 Beliefs — BCH (Brainstem Consonance Hierarchy).

4 beliefs derived from BCH mechanism output:
    1 Core:         harmonic_stability (τ=0.3)
    2 Appraisal:    interval_quality, harmonic_template_match
    1 Anticipation: consonance_trajectory
"""

from .consonance_trajectory import ConsonanceTrajectory
from .harmonic_stability import HarmonicStability
from .harmonic_template_match import HarmonicTemplateMatch
from .interval_quality import IntervalQuality

__all__ = [
    "HarmonicStability",
    "IntervalQuality",
    "HarmonicTemplateMatch",
    "ConsonanceTrajectory",
]
