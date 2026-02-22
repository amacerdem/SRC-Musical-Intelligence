"""F1 Beliefs — PCCR (Pitch Chroma Cortical Representation).

2 beliefs derived from PCCR mechanism output:
    1 Core:      pitch_identity (τ=0.4)
    1 Appraisal: octave_equivalence

Dependency chain:
    BCH (Depth 0) → PSCL (Depth 1) → PCCR (Depth 2) → beliefs
"""

from .octave_equivalence import OctaveEquivalence
from .pitch_identity import PitchIdentity

__all__ = [
    "PitchIdentity",
    "OctaveEquivalence",
]
