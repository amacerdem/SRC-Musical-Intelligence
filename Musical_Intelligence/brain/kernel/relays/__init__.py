"""Relay wrappers for C³ kernel — causal-mode adapters.

Each wrapper instantiates a production Relay nucleus, filters its
H³ demands to L0 (memory) for causal online mode, and exposes
typed P-layer + F-layer outputs for belief enrichment.

9 relays (1 per unit):
    BCH (SPU), HMCE (STU), SNEM (ASU), MEAMN (IMU),
    DAED (RPU), MPG (NDU), SRP (ARU), PEOM (MPU), HTP (PCU)
"""
from .base_wrapper import RelayKernelWrapper
from .bch_wrapper import BCHKernelWrapper, BCHOutput
from .hmce_wrapper import HMCEKernelWrapper, HMCEOutput
from .snem_wrapper import SNEMKernelWrapper, SNEMOutput
from .meamn_wrapper import MEAMNKernelWrapper, MEAMNOutput
from .daed_wrapper import DAEDKernelWrapper, DAEDOutput
from .mpg_wrapper import MPGKernelWrapper, MPGOutput
from .srp_wrapper import SRPKernelWrapper, SRPOutput
from .peom_wrapper import PEOMKernelWrapper, PEOMOutput
from .htp_wrapper import HTPKernelWrapper, HTPOutput

__all__ = [
    "RelayKernelWrapper",
    "BCHKernelWrapper", "BCHOutput",
    "HMCEKernelWrapper", "HMCEOutput",
    "SNEMKernelWrapper", "SNEMOutput",
    "MEAMNKernelWrapper", "MEAMNOutput",
    "DAEDKernelWrapper", "DAEDOutput",
    "MPGKernelWrapper", "MPGOutput",
    "SRPKernelWrapper", "SRPOutput",
    "PEOMKernelWrapper", "PEOMOutput",
    "HTPKernelWrapper", "HTPOutput",
]
