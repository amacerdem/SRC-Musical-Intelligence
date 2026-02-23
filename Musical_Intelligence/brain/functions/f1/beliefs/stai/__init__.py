"""F1 Beliefs — STAI (Spectral-Temporal Aesthetic Integration).

3 beliefs derived from STAI mechanism output:
    1 Core:         aesthetic_quality (t=0.4)
    1 Appraisal:    spectral_temporal_synergy
    1 Anticipation: reward_response_pred
"""

from .aesthetic_quality import AestheticQuality
from .reward_response_pred import RewardResponsePred
from .spectral_temporal_synergy import SpectralTemporalSynergy

__all__ = [
    "AestheticQuality",
    "SpectralTemporalSynergy",
    "RewardResponsePred",
]
