from __future__ import annotations

from enum import Enum
from typing import Dict, FrozenSet


class R3Domain(Enum):
    PSYCHOACOUSTIC = "Psychoacoustic"
    SPECTRAL = "Spectral"
    TONAL = "Tonal"
    TEMPORAL = "Temporal"
    INFORMATION = "Information"
    CROSS_DOMAIN = "CrossDomain"


R3_DOMAIN_MAP: Dict[R3Domain, FrozenSet[str]] = {
    R3Domain.PSYCHOACOUSTIC: frozenset({"A", "K"}),
    R3Domain.SPECTRAL:       frozenset({"B", "C", "J"}),
    R3Domain.TONAL:          frozenset({"F", "H"}),
    R3Domain.TEMPORAL:       frozenset({"D", "G"}),
    R3Domain.INFORMATION:    frozenset({"I"}),
    R3Domain.CROSS_DOMAIN:   frozenset({"E"}),
}

# Dimension totals per domain (derived from group boundaries)
_DOMAIN_DIMS: Dict[R3Domain, int] = {
    R3Domain.PSYCHOACOUSTIC: 21,   # A(7) + K(14)
    R3Domain.SPECTRAL:       34,   # B(5) + C(9) + J(20)
    R3Domain.TONAL:          28,   # F(16) + H(12)
    R3Domain.TEMPORAL:       14,   # D(4) + G(10)
    R3Domain.INFORMATION:     7,   # I(7)
    R3Domain.CROSS_DOMAIN:   24,   # E(24)
}

assert len(R3_DOMAIN_MAP) == 6
assert sum(_DOMAIN_DIMS.values()) == 128
_all_letters = frozenset().union(*R3_DOMAIN_MAP.values())
assert _all_letters == frozenset("ABCDEFGHIJK")
assert len(_all_letters) == 11
del _all_letters
