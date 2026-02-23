"""F8 Beliefs -- EDNR (Expertise-Dependent Network Reorganization).

2 beliefs derived from EDNR mechanism output:
    1 Core:      network_specialization (tau=0.95)
    1 Appraisal: within_connectivity
"""

from .network_specialization import NetworkSpecialization
from .within_connectivity import WithinConnectivity

__all__ = [
    "NetworkSpecialization",
    "WithinConnectivity",
]
