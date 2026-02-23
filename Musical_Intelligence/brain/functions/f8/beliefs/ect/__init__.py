"""F8 Beliefs -- ECT (Efficiency-Compartmentalization Trade-off).

2 beliefs derived from ECT mechanism output:
    1 Appraisal:    compartmentalization_cost
    1 Anticipation: transfer_limitation
"""

from .compartmentalization_cost import CompartmentalizationCost
from .transfer_limitation import TransferLimitation

__all__ = [
    "CompartmentalizationCost",
    "TransferLimitation",
]
