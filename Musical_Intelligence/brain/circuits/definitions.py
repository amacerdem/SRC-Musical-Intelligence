"""Neural circuit definitions for the C3 brain architecture.

Defines 6 functional circuits spanning 9 cognitive units. Five operational
circuits (CIRCUITS) are used for cross-unit pathway routing; the sixth
(IMAGERY) is emergent rather than structural.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class CircuitDef:
    """A neural circuit grouping cognitive units.

    Attributes:
        name:        Short identifier (e.g. ``"mesolimbic"``).
        full_name:   Human-readable name (e.g. ``"Mesolimbic Reward Circuit"``).
        units:       Tuple of cognitive-unit abbreviations in this circuit.
        description: One-line functional summary.
    """

    name: str
    full_name: str
    units: Tuple[str, ...]
    description: str


# ── Operational circuits ─────────────────────────────────────────────

MESOLIMBIC = CircuitDef(
    name="mesolimbic",
    full_name="Mesolimbic Reward Circuit",
    units=("ARU", "RPU"),
    description="Reward & pleasure processing via VTA-NAcc dopaminergic pathway.",
)

PERCEPTUAL = CircuitDef(
    name="perceptual",
    full_name="Perceptual Processing Circuit",
    units=("SPU",),
    description="Hearing & pattern recognition via auditory cortex hierarchy.",
)

SENSORIMOTOR = CircuitDef(
    name="sensorimotor",
    full_name="Sensorimotor Timing Circuit",
    units=("STU", "MPU"),
    description="Rhythm & movement entrainment via SMA and premotor cortex.",
)

MNEMONIC = CircuitDef(
    name="mnemonic",
    full_name="Mnemonic Processing Circuit",
    units=("IMU", "PCU"),
    description="Memory consolidation & familiarity via hippocampal-cortical system.",
)

SALIENCE = CircuitDef(
    name="salience",
    full_name="Salience Detection Circuit",
    units=("ASU", "NDU"),
    description="Attention, novelty & arousal gating via anterior insula and ACC.",
)

# ── Emergent circuit (non-structural, excluded from CIRCUITS) ────────

IMAGERY = CircuitDef(
    name="imagery",
    full_name="Imagery Circuit",
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
