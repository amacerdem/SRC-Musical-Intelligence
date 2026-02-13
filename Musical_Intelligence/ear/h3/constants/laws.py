"""H3 law constants -- 3 temporal perspectives (Memory, Prediction, Integration).

Defines the three causal laws that determine attention-window placement and
the shared exponential-decay constant governing the attention kernel.

Source of truth
---------------
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md  Section 6
- Docs/H3/Registry/LawCatalog.md       authoritative law catalog
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Number of laws
# ---------------------------------------------------------------------------
N_LAWS: int = 3

# ---------------------------------------------------------------------------
# Law indices
# ---------------------------------------------------------------------------
LAW_MEMORY: int = 0
"""L0 -- Memory (past -> present).  Causal exponential decay looking backward
from the current frame."""

LAW_PREDICTION: int = 1
"""L1 -- Prediction (present -> future).  Anticipatory exponential projection
forward from the current frame."""

LAW_INTEGRATION: int = 2
"""L2 -- Integration (past <-> future).  Bidirectional symmetric exponential
centered on the current frame."""

# ---------------------------------------------------------------------------
# LAW_NAMES -- human-readable names
# ---------------------------------------------------------------------------
LAW_NAMES: tuple[str, ...] = ("memory", "prediction", "integration")

# ---------------------------------------------------------------------------
# Attention kernel decay constant
# ---------------------------------------------------------------------------
ATTENTION_DECAY: float = 3.0
"""Shared decay constant for the exponential attention kernel.

Kernel formula:  A(dt) = exp(-ATTENTION_DECAY * |dt| / H)

At the window boundary (|dt| = H):
    A(H) = exp(-3) = 0.0498  (~5% of peak weight)

Half-life:  H * ln(2) / ATTENTION_DECAY = 0.231 * H
"""
