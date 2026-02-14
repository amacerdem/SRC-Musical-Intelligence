"""Neural circuit definitions for the C3 brain architecture.

Defines 6 functional circuits spanning 9 cognitive units and 10 mechanisms.
Five operational circuits (CIRCUITS) are used for cross-unit pathway routing;
the sixth (IMAGERY) is emergent rather than structural.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CircuitDef:
    """A neural circuit grouping mechanisms and cognitive units.

    Attributes:
        name:        Short identifier (e.g. ``"mesolimbic"``).
        full_name:   Human-readable name (e.g. ``"Mesolimbic Reward Circuit"``).
        mechanisms:  Tuple of mechanism abbreviations assigned to this circuit.
        units:       Tuple of cognitive-unit abbreviations in this circuit.
        description: One-line functional summary.
    """

    name: str
    full_name: str
    mechanisms: Tuple[str, ...]
    units: Tuple[str, ...]
    description: str


# ── Operational circuits ─────────────────────────────────────────────

MESOLIMBIC = CircuitDef(
    name="mesolimbic",
    full_name="Mesolimbic Reward Circuit",
    mechanisms=("AED", "CPD", "C0P"),
    units=("ARU", "RPU"),
    description="Reward & pleasure processing via VTA-NAcc dopaminergic pathway.",
)

PERCEPTUAL = CircuitDef(
    name="perceptual",
    full_name="Perceptual Processing Circuit",
    mechanisms=("PPC", "TPC"),
    units=("SPU",),
    description="Hearing & pattern recognition via auditory cortex hierarchy.",
)

SENSORIMOTOR = CircuitDef(
    name="sensorimotor",
    full_name="Sensorimotor Timing Circuit",
    mechanisms=("BEP", "TMH"),
    units=("STU", "MPU"),
    description="Rhythm & movement entrainment via SMA and premotor cortex.",
)

MNEMONIC = CircuitDef(
    name="mnemonic",
    full_name="Mnemonic Processing Circuit",
    mechanisms=("MEM", "SYN"),
    units=("IMU", "PCU"),
    description="Memory consolidation & familiarity via hippocampal-cortical system.",
)

SALIENCE = CircuitDef(
    name="salience",
    full_name="Salience Detection Circuit",
    mechanisms=("ASA",),
    units=("ASU", "NDU"),
    description="Attention, novelty & arousal gating via anterior insula and ACC.",
)

# ── Emergent circuit (non-structural, excluded from CIRCUITS) ────────

IMAGERY = CircuitDef(
    name="imagery",
    full_name="Imagery Circuit",
    mechanisms=("PPC", "TPC", "MEM"),
    units=("PCU",),
    description="Emergent circuit for mental imagery and simulation (not structural).",
)

# ── Collections ──────────────────────────────────────────────────────

CIRCUITS: Tuple[CircuitDef, ...] = (
    MESOLIMBIC,
    PERCEPTUAL,
    SENSORIMOTOR,
    MNEMONIC,
    SALIENCE,
)
"""Five operational circuits used for cross-unit pathway routing."""

CIRCUIT_NAMES: Tuple[str, ...] = (
    "mesolimbic",
    "perceptual",
    "sensorimotor",
    "mnemonic",
    "salience",
    "imagery",
)
"""All six circuit names including the emergent imagery circuit."""

ALL_CIRCUITS: Tuple[CircuitDef, ...] = CIRCUITS + (IMAGERY,)
"""All six circuits (five operational + imagery)."""
