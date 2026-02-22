"""F5 mechanisms — 12 models (142D total).

Relay (D0):      SRP(19D) | AAC(14D) | VMM(12D)
Encoder (D1):    PUPF(12D) | CLAM(11D) | MAD(11D) | NEMAC(11D) | STAI(12D)
Associator (D2): DAP(10D) | CMAT(10D) | TAR(10D) | MAA(10D)
"""
from .srp import SRP
from .aac import AAC
from .vmm import VMM
from .pupf import PUPF
from .clam import CLAM
from .mad import MAD
from .nemac import NEMAC
from .stai import STAI
from .dap import DAP
from .cmat import CMAT
from .tar import TAR
from .maa import MAA

__all__ = [
    "SRP", "AAC", "VMM",
    "PUPF", "CLAM", "MAD", "NEMAC", "STAI",
    "DAP", "CMAT", "TAR", "MAA",
]
