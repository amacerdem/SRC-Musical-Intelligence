"""
Cognitive Units -- UnitRunner orchestrates the 9 cognitive units.

The mi_beta brain has 9 cognitive units, each modelling a distinct
neural circuit / cognitive function:

    Core-4 VALIDATED (k >= 10 studies, meta-analytic pooled d):
        SPU  d=0.84  Spectral Processing      (perceptual)
        ARU  d=0.83  Affective Resonance       (mesolimbic)
        STU  d=0.67  Sensorimotor Timing       (sensorimotor)
        IMU  d=0.53  Integrative Memory        (mnemonic)

    Experimental-5 (k < 10):
        RPU  d=0.70  Reward Processing         (mesolimbic)
        MPU  d=0.62  Motor Planning            (sensorimotor)
        ASU  d=0.60  Auditory Salience         (salience)
        PCU  d=0.58  Predictive Coding         (mnemonic)
        NDU  d=0.55  Novelty Detection         (salience)

Execution is split into two passes:
    1. Independent pass:  SPU, STU, IMU, ASU, NDU, MPU, PCU  (no cross-unit deps)
    2. Dependent pass:    ARU, RPU  (receive cross-unit inputs via PathwayRunner)

The PathwayRunner routes signals between the two passes.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Type

from torch import Tensor

from mi_beta.contracts import BaseCognitiveUnit

from .aru import ARUUnit
from .asu import ASUUnit
from .imu import IMUUnit
from .mpu import MPUUnit
from .ndu import NDUUnit
from .pcu import PCUUnit
from .rpu import RPUUnit
from .spu import SPUUnit
from .stu import STUUnit

# ── Unit registry ─────────────────────────────────────────────────────

UNIT_CLASSES: Dict[str, Type[BaseCognitiveUnit]] = {
    "SPU": SPUUnit,
    "STU": STUUnit,
    "IMU": IMUUnit,
    "ASU": ASUUnit,
    "NDU": NDUUnit,
    "MPU": MPUUnit,
    "PCU": PCUUnit,
    "ARU": ARUUnit,
    "RPU": RPUUnit,
}

# Units that can be computed without cross-unit inputs.
INDEPENDENT_UNITS: Tuple[str, ...] = (
    "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU",
)

# Units that require cross-unit inputs from the independent pass.
DEPENDENT_UNITS: Tuple[str, ...] = ("ARU", "RPU")

ALL_UNIT_NAMES: Tuple[str, ...] = INDEPENDENT_UNITS + DEPENDENT_UNITS


def create_unit(name: str) -> BaseCognitiveUnit:
    """Instantiate a cognitive unit by name.

    Args:
        name: Unit short name (e.g. "ARU", "SPU").

    Returns:
        Instantiated BaseCognitiveUnit subclass.

    Raises:
        KeyError: If the name is not in the registry.
    """
    if name not in UNIT_CLASSES:
        raise KeyError(
            f"Unknown unit {name!r}.  "
            f"Available: {sorted(UNIT_CLASSES.keys())}"
        )
    return UNIT_CLASSES[name]()


class UnitRunner:
    """Orchestrates computation across all 9 cognitive units.

    The runner manages unit instantiation, execution ordering, and the
    two-pass compute strategy (independent then dependent).

    Args:
        active_units: Sequence of unit names to activate.  Defaults to all
            9 units.  Pass a subset to disable units during development.
    """

    def __init__(
        self,
        active_units: Optional[Tuple[str, ...]] = None,
    ) -> None:
        if active_units is None:
            active_units = ALL_UNIT_NAMES

        self._active_names: Tuple[str, ...] = active_units
        self._units: Dict[str, BaseCognitiveUnit] = {
            name: create_unit(name) for name in active_units
        }

    @property
    def active_units(self) -> Dict[str, BaseCognitiveUnit]:
        """Map of active unit name -> instance."""
        return dict(self._units)

    @property
    def independent_names(self) -> List[str]:
        """Names of active independent units (first pass)."""
        return [n for n in INDEPENDENT_UNITS if n in self._units]

    @property
    def dependent_names(self) -> List[str]:
        """Names of active dependent units (second pass)."""
        return [n for n in DEPENDENT_UNITS if n in self._units]

    @property
    def total_dim(self) -> int:
        """Total output dimensionality across all active units."""
        return sum(u.total_dim for u in self._units.values())

    def get_unit(self, name: str) -> BaseCognitiveUnit:
        """Retrieve an active unit by name.

        Raises:
            KeyError: If the unit is not active.
        """
        if name not in self._units:
            raise KeyError(
                f"Unit {name!r} is not active.  "
                f"Active: {list(self._units.keys())}"
            )
        return self._units[name]

    def compute_unit(
        self,
        unit_name: str,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Compute a single unit's output.

        Args:
            unit_name: Short name of the unit to compute.
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Optional dict of named tensors from other
                units' models, keyed by pathway_id.

        Returns:
            (B, T, unit_dim) concatenated output tensor.
        """
        unit = self.get_unit(unit_name)
        return unit.compute(
            h3_features=h3_features,
            r3_features=r3_features,
            cross_unit_inputs=cross_unit_inputs,
        )

    def compute_all_independent(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Dict[str, Tensor]:
        """Compute all independent units (first pass, no cross-unit deps).

        Runs SPU, STU, IMU, ASU, NDU, MPU, PCU in the declared order.
        These units do not read from each other, so they could run in
        parallel on separate streams.

        Args:
            h3_features: Shared H3 temporal feature bank.
            r3_features: (B, T, 49) R3 spectral features.

        Returns:
            Dict mapping unit_name -> (B, T, unit_dim) output tensor.
        """
        outputs: Dict[str, Tensor] = {}
        for name in self.independent_names:
            outputs[name] = self.compute_unit(
                unit_name=name,
                h3_features=h3_features,
                r3_features=r3_features,
                cross_unit_inputs=None,
            )
        return outputs

    def compute_dependent(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Dict[str, Tensor],
    ) -> Dict[str, Tensor]:
        """Compute dependent units (second pass, after pathway routing).

        Runs ARU and RPU, which receive cross-unit inputs from the
        PathwayRunner.

        Args:
            h3_features: Shared H3 temporal feature bank.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Dict of named tensors routed by the
                PathwayRunner from independent unit outputs.

        Returns:
            Dict mapping unit_name -> (B, T, unit_dim) output tensor.
        """
        outputs: Dict[str, Tensor] = {}
        for name in self.dependent_names:
            outputs[name] = self.compute_unit(
                unit_name=name,
                h3_features=h3_features,
                r3_features=r3_features,
                cross_unit_inputs=cross_unit_inputs,
            )
        return outputs

    def validate_all(self) -> Dict[str, List[str]]:
        """Run internal consistency checks on all active units.

        Returns:
            Dict mapping unit_name -> list of error messages.
            Units with no errors are omitted.
        """
        results: Dict[str, List[str]] = {}
        for name, unit in self._units.items():
            errors = unit.validate()
            if errors:
                results[name] = errors
        return results

    def __repr__(self) -> str:
        names = ", ".join(self._active_names)
        return (
            f"UnitRunner(units=[{names}], "
            f"total_dim={self.total_dim})"
        )


__all__ = [
    # Unit classes
    "ARUUnit",
    "ASUUnit",
    "IMUUnit",
    "MPUUnit",
    "NDUUnit",
    "PCUUnit",
    "RPUUnit",
    "SPUUnit",
    "STUUnit",
    # Runner
    "UnitRunner",
    # Registry
    "UNIT_CLASSES",
    "INDEPENDENT_UNITS",
    "DEPENDENT_UNITS",
    "ALL_UNIT_NAMES",
    "create_unit",
]
