"""Relay wrappers for C³ kernel — causal-mode adapters.

Each wrapper instantiates a production Relay nucleus, filters its
H³ demands to L0 (memory) for causal online mode, and exposes
typed P-layer + F-layer outputs for belief enrichment.
"""
from .base_wrapper import RelayKernelWrapper
from .bch_wrapper import BCHKernelWrapper, BCHOutput
from .hmce_wrapper import HMCEKernelWrapper, HMCEOutput
from .snem_wrapper import SNEMKernelWrapper, SNEMOutput
from .mmp_wrapper import MMPKernelWrapper, MMPOutput
from .daed_wrapper import DAEDKernelWrapper, DAEDOutput
from .mpg_wrapper import MPGKernelWrapper, MPGOutput

__all__ = [
    "RelayKernelWrapper",
    "BCHKernelWrapper", "BCHOutput",
    "HMCEKernelWrapper", "HMCEOutput",
    "SNEMKernelWrapper", "SNEMOutput",
    "MMPKernelWrapper", "MMPOutput",
    "DAEDKernelWrapper", "DAEDOutput",
    "MPGKernelWrapper", "MPGOutput",
]
