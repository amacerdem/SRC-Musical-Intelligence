"""NeuroLink -- Declarative mapping from nucleus output dims to neurochemicals.

Each ``NeuroLink`` declares that a specific output dimension of a nucleus
affects a specific neurochemical channel. The orchestrator uses these
declarations to accumulate the neurochemical state tensor: ``(B, T, 4)``
with channels ``[DA, NE, OPI, 5HT]``.

Three effect types:
- ``produce``: Sets the channel value (used by Relays at Depth 0).
- ``amplify``: Scales the channel value upward.
- ``inhibit``: Scales the channel value downward.
"""
from __future__ import annotations

from dataclasses import dataclass


# Neurochemical channel indices (matches TERMINOLOGY.md Section 15.1)
DA: int = 0    # Dopamine — reward prediction error
NE: int = 1    # Norepinephrine — exploration-exploitation balance
OPI: int = 2   # Endorphins — hedonic evaluation
_5HT: int = 3  # Serotonin — temporal discount rate

CHANNEL_NAMES = ("DA", "NE", "OPI", "5HT")
NUM_CHANNELS = 4

_VALID_EFFECTS = frozenset({"produce", "amplify", "inhibit"})


@dataclass(frozen=True)
class NeuroLink:
    """Maps one output dimension to one neurochemical channel.

    Attributes:
        dim_name:  Name of the output dimension (must match a name in
                   the nucleus's ``LAYERS`` dim_names).
        channel:   Neurochemical channel index: 0=DA, 1=NE, 2=OPI, 3=5HT.
        effect:    How this dimension affects the channel:
                   ``"produce"`` (set), ``"amplify"`` (scale up),
                   ``"inhibit"`` (scale down).
        weight:    Effect magnitude scale in ``[0, 1]``.
        citation:  Evidence source (e.g. ``"Schultz 1997"``).
    """

    dim_name: str
    channel: int
    effect: str
    weight: float
    citation: str

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def __post_init__(self) -> None:
        if not self.dim_name:
            raise ValueError("NeuroLink: dim_name must be non-empty")
        if not 0 <= self.channel < NUM_CHANNELS:
            raise ValueError(
                f"NeuroLink {self.dim_name!r}: channel must be in "
                f"[0, {NUM_CHANNELS}), got {self.channel}"
            )
        if self.effect not in _VALID_EFFECTS:
            raise ValueError(
                f"NeuroLink {self.dim_name!r}: effect must be one of "
                f"{sorted(_VALID_EFFECTS)}, got {self.effect!r}"
            )
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(
                f"NeuroLink {self.dim_name!r} → {CHANNEL_NAMES[self.channel]}: "
                f"weight must be in [0, 1], got {self.weight}"
            )
        if not self.citation:
            raise ValueError(
                f"NeuroLink {self.dim_name!r} → {CHANNEL_NAMES[self.channel]}: "
                f"citation must be non-empty"
            )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @property
    def channel_name(self) -> str:
        """Human-readable channel name (``'DA'``, ``'NE'``, etc.)."""
        return CHANNEL_NAMES[self.channel]
