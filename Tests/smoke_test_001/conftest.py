"""Smoke Test 001 — shared fixtures for all 11 layers.

Session-scope fixtures that are expensive to compute (R³, H³, mechanism
instances, belief instances) are created once and shared across all test
modules.
"""
from __future__ import annotations

import importlib
from typing import Any, Dict, List, Set, Tuple

import pytest
import torch
from torch import Tensor

# ======================================================================
# Helper: dynamic collection of mechanism / belief instances
# ======================================================================

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")

_MECHANISM_MODULES = {
    fn: f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
    for fn in _FUNCTION_IDS
}

_BELIEF_MODULES = {
    fn: f"Musical_Intelligence.brain.functions.{fn}.beliefs"
    for fn in _FUNCTION_IDS
}


def _collect_instances(module_map: Dict[str, str], base_class: type) -> List[Any]:
    """Import modules and collect instances of *base_class* from __all__."""
    instances: List[Any] = []
    for fn, mod_path in module_map.items():
        try:
            mod = importlib.import_module(mod_path)
        except Exception:
            continue
        for name in getattr(mod, "__all__", []):
            cls = getattr(mod, name, None)
            if cls is None:
                continue
            try:
                if isinstance(cls, type) and issubclass(cls, base_class):
                    instances.append(cls())
            except Exception:
                continue
    return instances


# ======================================================================
# Mel / R³ / H³ fixtures (session scope — expensive)
# ======================================================================

@pytest.fixture(scope="session")
def synthetic_mel(batch_size: int, time_steps: int) -> Tensor:
    """Random mel spectrogram (B, 128, T) in [0, 1]."""
    torch.manual_seed(42)
    return torch.rand(batch_size, 128, time_steps)


@pytest.fixture(scope="session")
def r3_extractor():
    """R³ extractor singleton."""
    from Musical_Intelligence.ear.r3.extractor import R3Extractor
    return R3Extractor()


@pytest.fixture(scope="session")
def r3_output(r3_extractor, synthetic_mel):
    """R³ extraction result — R3Output dataclass."""
    return r3_extractor.extract(synthetic_mel)


@pytest.fixture(scope="session")
def r3_features(r3_output) -> Tensor:
    """Dense R³ features tensor (B, T, 97)."""
    return r3_output.features


@pytest.fixture(scope="session")
def h3_extractor():
    """H³ extractor singleton."""
    from Musical_Intelligence.ear.h3.extractor import H3Extractor
    return H3Extractor()


# ======================================================================
# Mechanism fixtures (session scope)
# ======================================================================

@pytest.fixture(scope="session")
def all_mechanisms() -> List[Any]:
    """All mechanism instances from F1-F9 (Relay + Encoder + Associator + ...)."""
    from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase
    return _collect_instances(_MECHANISM_MODULES, _NucleusBase)


@pytest.fixture(scope="session")
def all_relays(all_mechanisms) -> List[Any]:
    """Depth-0 relay mechanisms only."""
    from Musical_Intelligence.contracts.bases.nucleus import Relay
    return [m for m in all_mechanisms if isinstance(m, Relay)]


@pytest.fixture(scope="session")
def all_encoders(all_mechanisms) -> List[Any]:
    """Depth-1 encoder mechanisms only."""
    from Musical_Intelligence.contracts.bases.nucleus import Encoder
    return [m for m in all_mechanisms if isinstance(m, Encoder)]


@pytest.fixture(scope="session")
def all_associators(all_mechanisms) -> List[Any]:
    """Depth-2 associator mechanisms only."""
    from Musical_Intelligence.contracts.bases.nucleus import Associator
    return [m for m in all_mechanisms if isinstance(m, Associator)]


@pytest.fixture(scope="session")
def mechanism_dims(all_mechanisms) -> Dict[str, int]:
    """Mechanism NAME → OUTPUT_DIM mapping."""
    return {m.NAME: m.OUTPUT_DIM for m in all_mechanisms}


# ======================================================================
# H³ demand collection + extraction
# ======================================================================

@pytest.fixture(scope="session")
def all_demands(all_mechanisms) -> Set[Tuple[int, int, int, int]]:
    """Union of all mechanism h3_demands as 4-tuples."""
    demands: Set[Tuple[int, int, int, int]] = set()
    for m in all_mechanisms:
        for spec in m.h3_demand:
            demands.add(spec.as_tuple())
    return demands


@pytest.fixture(scope="session")
def h3_output(h3_extractor, r3_features, all_demands):
    """H³ extraction result — H3Output dataclass."""
    return h3_extractor.extract(r3_features, all_demands)


@pytest.fixture(scope="session")
def h3_features(h3_output) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Sparse H³ features dict: (r3_idx, H, M, L) → (B, T)."""
    return h3_output.features


# ======================================================================
# Belief fixtures (session scope)
# ======================================================================

@pytest.fixture(scope="session")
def all_beliefs() -> List[Any]:
    """All 131 belief instances from F1-F9."""
    from Musical_Intelligence.contracts.bases.belief import _BeliefBase
    return _collect_instances(_BELIEF_MODULES, _BeliefBase)


@pytest.fixture(scope="session")
def all_core_beliefs(all_beliefs) -> List[Any]:
    """36 CoreBelief instances."""
    from Musical_Intelligence.contracts.bases.belief import CoreBelief
    return [b for b in all_beliefs if isinstance(b, CoreBelief)]


@pytest.fixture(scope="session")
def all_appraisal_beliefs(all_beliefs) -> List[Any]:
    """65 AppraisalBelief instances."""
    from Musical_Intelligence.contracts.bases.belief import AppraisalBelief
    return [b for b in all_beliefs if isinstance(b, AppraisalBelief)]


@pytest.fixture(scope="session")
def all_anticipation_beliefs(all_beliefs) -> List[Any]:
    """30 AnticipationBelief instances."""
    from Musical_Intelligence.contracts.bases.belief import AnticipationBelief
    return [b for b in all_beliefs if isinstance(b, AnticipationBelief)]


# ======================================================================
# Per-function belief lists (for count validation)
# ======================================================================

@pytest.fixture(scope="session")
def beliefs_by_function(all_beliefs) -> Dict[str, List[Any]]:
    """Group beliefs by FUNCTION attribute."""
    by_fn: Dict[str, List[Any]] = {}
    for b in all_beliefs:
        fn = getattr(b, "FUNCTION", "unknown")
        by_fn.setdefault(fn, []).append(b)
    return by_fn


# ======================================================================
# Synthetic H³ helper for individual relay testing
# ======================================================================

def make_synthetic_h3(
    mechanism,
    batch_size: int = 2,
    time_steps: int = 50,
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Create synthetic H³ features dict for a single mechanism's demands."""
    torch.manual_seed(7)
    h3: Dict[Tuple[int, int, int, int], Tensor] = {}
    for spec in mechanism.h3_demand:
        key = spec.as_tuple()
        h3[key] = torch.rand(batch_size, time_steps)
    return h3
