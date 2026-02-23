"""F9 Social -- Beliefs.

10 beliefs organized by mechanism:
    nscp/  -- 2 beliefs (1 Core, 1 Anticipation)
    ssri/  -- 6 beliefs (5 Appraisal, 1 Anticipation)
    ddsmi/ -- 2 beliefs (1 Core, 1 Appraisal)

All mechanisms are independent (depth 0).
"""

from .ddsmi import ResourceAllocation, SocialCoordination
from .nscp import CatchinessPred, NeuralSynchrony
from .ssri import (
    CollectivePleasurePred,
    EntrainmentQuality,
    GroupFlow,
    SocialBonding,
    SocialPredictionError,
    SynchronyReward,
)

__all__ = [
    # NSCP beliefs (depth 0)
    "NeuralSynchrony",
    "CatchinessPred",
    # SSRI beliefs (depth 0)
    "SynchronyReward",
    "SocialBonding",
    "GroupFlow",
    "EntrainmentQuality",
    "SocialPredictionError",
    "CollectivePleasurePred",
    # DDSMI beliefs (depth 0)
    "SocialCoordination",
    "ResourceAllocation",
]
