"""F6 mechanisms — 10 models (70D total).

Relay (D0):      DAED(8D) | MORMR(7D) | RPEM(8D)
Encoder (D1):    IUCP(6D) | MCCN(7D) | MEAMR(6D) | SSRI(11D)
Associator (D2): LDAC(6D) | IOTMS(5D) | SSPS(6D)
"""
from .daed import DAED
from .mormr import MORMR
from .rpem import RPEM
from .iucp import IUCP
from .mccn import MCCN
from .meamr import MEAMR
from .ssri import SSRI
from .ldac import LDAC
from .iotms import IOTMS
from .ssps import SSPS

__all__ = [
    "DAED", "MORMR", "RPEM",
    "IUCP", "MCCN", "MEAMR", "SSRI",
    "LDAC", "IOTMS", "SSPS",
]
