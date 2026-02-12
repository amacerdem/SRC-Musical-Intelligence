"""
MI-Beta Brain Mechanisms -- Atomic computational units within cognitive models.
================================================================================

This package contains the 10 mechanism implementations used by the brain's
cognitive models.  Each mechanism is a BaseMechanism subclass that reads H3
temporal features and R3 spectral features and produces a fixed 30-D output.

Mechanisms are grouped by neural circuit:

    Mesolimbic (reward & pleasure):
        AED  -- Affective Entrainment Dynamics  (H6, H16)
        CPD  -- Chills & Peak Detection         (H9, H16, H18)
        C0P  -- Cognitive Projection            (H18, H19, H20)

    Perceptual (hearing & pattern):
        PPC  -- Pitch Processing Chain          (H0, H3, H6)
        TPC  -- Timbre Processing Chain         (H6, H12, H16)

    Sensorimotor (rhythm & movement):
        BEP  -- Beat Entrainment Processing     (H6, H9, H11)
        TMH  -- Temporal Memory Hierarchy       (H16, H18, H20, H22)

    Mnemonic (memory & familiarity):
        MEM  -- Memory Encoding / Retrieval     (H18, H20, H22, H25)
        SYN  -- Syntactic Processing            (H12, H16, H18)

    Salience (attention & novelty):
        ASA  -- Auditory Scene Analysis         (H3, H6, H9)

MechanismRunner
---------------
The MechanismRunner class takes a ModelRegistry after scan() and computes
all mechanisms needed by the active models.  It caches outputs so that
mechanisms shared across multiple models are computed only once.

Usage::

    from mi_beta.core.registry import ModelRegistry
    from mi_beta.brain.mechanisms import MechanismRunner

    registry = ModelRegistry()
    registry.scan()

    runner = MechanismRunner(registry)
    outputs = runner.run(h3_features, r3_features)
    # outputs["AED"] -> (B, T, 30)
    # outputs["CPD"] -> (B, T, 30)
    # ...
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional, Set, Tuple, Type

import torch
from torch import Tensor

from mi_beta.contracts import BaseMechanism

# ── Mechanism imports ──────────────────────────────────────────────────
from .aed import AED
from .asa import ASA
from .bep import BEP
from .c0p import C0P
from .cpd import CPD
from .mem import MEM
from .ppc import PPC
from .syn import SYN
from .tmh import TMH
from .tpc import TPC

logger = logging.getLogger(__name__)

# ── Public API ─────────────────────────────────────────────────────────

__all__ = [
    # Mechanism classes
    "AED",
    "ASA",
    "BEP",
    "C0P",
    "CPD",
    "MEM",
    "PPC",
    "SYN",
    "TMH",
    "TPC",
    # Runner
    "MechanismRunner",
    # Helpers
    "ALL_MECHANISMS",
    "MECHANISM_BY_NAME",
    "MECHANISM_BY_CIRCUIT",
]

# ── Mechanism catalogue ───────────────────────────────────────────────

ALL_MECHANISMS: Tuple[Type[BaseMechanism], ...] = (
    AED, ASA, BEP, C0P, CPD, MEM, PPC, SYN, TMH, TPC,
)

MECHANISM_BY_NAME: Dict[str, Type[BaseMechanism]] = {
    cls.NAME: cls for cls in ALL_MECHANISMS
}

MECHANISM_BY_CIRCUIT: Dict[str, Tuple[Type[BaseMechanism], ...]] = {
    "mesolimbic":   (AED, CPD, C0P),
    "perceptual":   (PPC, TPC),
    "sensorimotor": (BEP, TMH),
    "mnemonic":     (MEM, SYN),
    "salience":     (ASA,),
}


# =====================================================================
# MechanismRunner
# =====================================================================

class MechanismRunner:
    """Computes all needed mechanisms and caches outputs for sharing.

    The runner inspects the active models in a ModelRegistry to determine
    which mechanisms are required, instantiates them once, executes their
    ``compute()`` methods, and stores the results in a name-keyed dict.
    If multiple models reference the same mechanism, it is computed once
    and shared.

    Lifecycle::

        # 1. Build runner from registry (determines needed mechanisms)
        runner = MechanismRunner(registry)

        # 2. Run all mechanisms for a batch
        outputs = runner.run(h3_features, r3_features)

        # 3. Access outputs by name
        aed_out = outputs["AED"]      # (B, T, 30)
        cpd_out = outputs["CPD"]      # (B, T, 30)

        # 4. (Optional) Clear cache for next batch
        runner.clear_cache()

    Thread safety:
        NOT thread-safe.  Each thread should use its own MechanismRunner.
    """

    def __init__(self, registry: "ModelRegistry") -> None:  # noqa: F821
        """Initialise the runner from a ModelRegistry.

        Scans the registry's active models to determine which mechanisms
        are needed, then instantiates each required mechanism once.

        Args:
            registry: A ModelRegistry that has already been scanned.
                      Only active (enabled) models are inspected.
        """
        self._registry = registry

        # Collect mechanism names from active models
        needed_names: Set[str] = set()
        for model in registry.active_models():
            mechanism_names = getattr(model, "MECHANISM_NAMES", ())
            for name in mechanism_names:
                needed_names.add(name)

        # Instantiate needed mechanisms (one instance per name)
        self._mechanisms: Dict[str, BaseMechanism] = {}
        for name in sorted(needed_names):
            cls = MECHANISM_BY_NAME.get(name)
            if cls is not None:
                self._mechanisms[name] = cls()
            else:
                logger.warning(
                    "MechanismRunner: model requests mechanism %r but no "
                    "implementation found in MECHANISM_BY_NAME",
                    name,
                )

        # Output cache: populated by run(), cleared by clear_cache()
        self._cache: Dict[str, Tensor] = {}

        logger.info(
            "MechanismRunner: %d mechanisms needed, %d available",
            len(needed_names),
            len(self._mechanisms),
        )

    # ── Properties ────────────────────────────────────────────────────

    @property
    def mechanism_names(self) -> List[str]:
        """Sorted list of mechanism names that this runner will compute."""
        return sorted(self._mechanisms.keys())

    @property
    def mechanism_count(self) -> int:
        """Number of mechanisms managed by this runner."""
        return len(self._mechanisms)

    @property
    def is_cached(self) -> bool:
        """True if the cache contains computed outputs."""
        return len(self._cache) > 0

    @property
    def total_h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Union of all H3 demands from managed mechanisms.

        Returns the minimal set of H3 4-tuples that the H3 engine must
        compute to satisfy all mechanisms in this runner.
        """
        demand: Set[Tuple[int, int, int, int]] = set()
        for mech in self._mechanisms.values():
            demand.update(mech.h3_demand)
        return demand

    # ── Execution ─────────────────────────────────────────────────────

    def run(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Dict[str, Tensor]:
        """Compute all mechanisms and return cached outputs.

        If the cache already contains results (from a previous call
        without ``clear_cache()``), returns the cached outputs immediately.
        Call ``clear_cache()`` before ``run()`` if you need fresh
        computation for a new batch.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} H3
                temporal feature dict.  Must contain at least the tuples
                required by the mechanisms (see ``total_h3_demand``).
            r3_features: (B, T, 49) R3 spectral features.

        Returns:
            {mechanism_name: (B, T, OUTPUT_DIM)} dict of mechanism outputs.
        """
        if self._cache:
            return self._cache

        for name, mech in self._mechanisms.items():
            try:
                output = mech.compute(h3_features, r3_features)
                self._cache[name] = output
            except Exception:
                logger.exception(
                    "MechanismRunner: mechanism %s raised an error", name
                )
                # Provide zero fallback so downstream models don't crash
                B, T, _ = r3_features.shape
                self._cache[name] = torch.zeros(
                    B, T, mech.OUTPUT_DIM, device=r3_features.device
                )

        return self._cache

    def get(self, name: str) -> Optional[Tensor]:
        """Get a single mechanism's cached output.

        Args:
            name: Mechanism name (e.g. "AED", "CPD").

        Returns:
            (B, T, OUTPUT_DIM) tensor if cached, None otherwise.

        Raises:
            KeyError: If the mechanism name is not managed by this runner.
        """
        if name not in self._mechanisms:
            raise KeyError(
                f"Mechanism {name!r} not managed by this runner. "
                f"Available: {self.mechanism_names}"
            )
        return self._cache.get(name)

    def clear_cache(self) -> None:
        """Clear all cached mechanism outputs.

        Call this before ``run()`` when processing a new batch.
        """
        self._cache.clear()

    # ── Validation ────────────────────────────────────────────────────

    def validate(self) -> List[str]:
        """Validate all managed mechanisms.

        Returns:
            List of error messages (empty if all mechanisms are valid).
        """
        errors: List[str] = []
        for name, mech in self._mechanisms.items():
            mech_errors = mech.validate()
            for err in mech_errors:
                errors.append(f"{name}: {err}")
        return errors

    # ── Introspection ─────────────────────────────────────────────────

    def summary(self) -> Dict[str, object]:
        """Return a summary dict for debugging / logging."""
        return {
            "mechanism_count": self.mechanism_count,
            "mechanisms": self.mechanism_names,
            "total_h3_demand": len(self.total_h3_demand),
            "cached": self.is_cached,
            "by_circuit": {
                circuit: [cls.NAME for cls in classes]
                for circuit, classes in MECHANISM_BY_CIRCUIT.items()
            },
        }

    def __repr__(self) -> str:
        cached_str = "cached" if self.is_cached else "not cached"
        return (
            f"MechanismRunner("
            f"mechanisms={self.mechanism_count}, "
            f"{cached_str})"
        )
