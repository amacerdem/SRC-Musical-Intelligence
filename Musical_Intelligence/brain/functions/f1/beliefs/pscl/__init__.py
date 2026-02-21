"""F1 Beliefs — PSCL (Pitch Salience in Cortical Lateralization).

2 beliefs derived from PSCL mechanism output:
    1 Core:         pitch_prominence (τ=0.35)
    1 Anticipation: pitch_continuation
"""

from .pitch_continuation import PitchContinuation
from .pitch_prominence import PitchProminence

__all__ = [
    "PitchProminence",
    "PitchContinuation",
]
