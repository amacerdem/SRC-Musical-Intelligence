"""F6 Beliefs — SRP (Subjective Reward Processing).

11 beliefs derived from SRP mechanism output (19D):
    5 Core:         wanting (t=0.6), liking (t=0.65), pleasure (t=0.7),
                    prediction_error (t=0.5), tension (t=0.55)
    3 Appraisal:    prediction_match, peak_detection, harmonic_tension
    3 Anticipation: chills_proximity, resolution_expectation, reward_forecast
"""

from .chills_proximity import ChillsProximity
from .harmonic_tension import HarmonicTension
from .liking import Liking
from .peak_detection import PeakDetection
from .pleasure import Pleasure
from .prediction_error import PredictionError
from .prediction_match import PredictionMatch
from .resolution_expectation import ResolutionExpectation
from .reward_forecast import RewardForecast
from .tension import Tension
from .wanting import Wanting

__all__ = [
    # Core beliefs
    "Wanting",
    "Liking",
    "Pleasure",
    "PredictionError",
    "Tension",
    # Appraisal beliefs
    "PredictionMatch",
    "PeakDetection",
    "HarmonicTension",
    # Anticipation beliefs
    "ChillsProximity",
    "ResolutionExpectation",
    "RewardForecast",
]
