"""F9 Beliefs -- DDSMI (Dual-brain Decoding of Social Musical Interaction).

2 beliefs derived from DDSMI mechanism output:
    1 Core:      social_coordination (tau=0.60)
    1 Appraisal: resource_allocation
"""

from .resource_allocation import ResourceAllocation
from .social_coordination import SocialCoordination

__all__ = [
    "SocialCoordination",
    "ResourceAllocation",
]
