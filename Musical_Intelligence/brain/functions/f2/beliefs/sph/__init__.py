"""SPH beliefs — Spatiotemporal Prediction Hierarchy.

4 beliefs (1 Core, 2 Appraisal, 1 Anticipation):
    SequenceMatch          Core (τ=0.45, full Bayesian PE cycle)
    ErrorPropagation       Appraisal (observe-only)
    OscillatorySignature   Appraisal (observe-only)
    SequenceCompletion     Anticipation (forward prediction)
"""
from .error_propagation import ErrorPropagation
from .oscillatory_signature import OscillatorySignature
from .sequence_completion import SequenceCompletion
from .sequence_match import SequenceMatch

__all__ = [
    "SequenceMatch",
    "ErrorPropagation",
    "OscillatorySignature",
    "SequenceCompletion",
]
