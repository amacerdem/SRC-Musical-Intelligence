"""Shared pytest configuration and fixtures for the MI test suite.

Provides reusable fixtures for synthetic data generation and component
instantiation across all test categories (unit, integration, validation).

Fixture scoping strategy:
    - session:  Expensive objects (extractors, orchestrator, demand sets)
    - function: Cheap tensors that may be mutated by tests
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Set, Tuple

import pytest
import torch
from torch import Tensor

# ---------------------------------------------------------------------------
# Path setup -- ensure Musical_Intelligence is importable
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Musical_Intelligence.ear.h3.extractor import H3Extractor
from Musical_Intelligence.brain.orchestrator import BrainOrchestrator, UNIT_ORDER

from Tests.fixtures.generators import (
    generate_mel,
    generate_r3,
    generate_r3_v1,
    generate_h3_features,
    generate_minimal_demand,
)


# ======================================================================
# Pytest markers
# ======================================================================

def pytest_configure(config: pytest.Config) -> None:
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (> 10s)")
    config.addinivalue_line("markers", "gpu: marks tests requiring CUDA")
    config.addinivalue_line("markers", "audio: marks tests requiring real audio files")


# ======================================================================
# Device and batch size
# ======================================================================

@pytest.fixture(scope="session")
def device() -> torch.device:
    """Computation device (CPU)."""
    return torch.device("cpu")


@pytest.fixture(scope="session")
def batch_size() -> int:
    """Default batch size for tests."""
    return 1


# ======================================================================
# Synthetic mel spectrogram
# ======================================================================

@pytest.fixture
def synthetic_mel(batch_size: int) -> Tensor:
    """Random mel spectrogram tensor.

    Shape: (B, 128, T) with T=100, values in [0, 1].
    Mimics log1p-normalised mel output from Cochlea (n_mels=128 is mel bins, not R3 dim).
    """
    return generate_mel(B=batch_size, T=100, n_mels=128)


# ======================================================================
# Synthetic R3 features (97D, post-dissolution)
# ======================================================================

@pytest.fixture
def synthetic_r3(batch_size: int) -> Tensor:
    """Random R3 spectral feature tensor (v2, 97D).

    Shape: (B, T, 97) with T=100, values in [0, 1].
    """
    return generate_r3(B=batch_size, T=100, D=97)


# ======================================================================
# Synthetic R3 features (49D, legacy v1)
# ======================================================================

@pytest.fixture
def synthetic_r3_v1(batch_size: int) -> Tensor:
    """Random R3 spectral feature tensor (v1, 49D).

    Shape: (B, T, 49) with T=100, values in [0, 1].
    Used by Brain models that reference the original 49D R3 space.
    """
    return generate_r3_v1(B=batch_size, T=100)


# ======================================================================
# Synthetic H3 features
# ======================================================================

@pytest.fixture(scope="session")
def minimal_demand_set() -> Set[Tuple[int, int, int, int]]:
    """A minimal set of 50 random H3 demand 4-tuples.

    Covers a representative spread across R3 indices, horizons,
    morphs, and laws for lightweight testing.
    """
    return generate_minimal_demand(n=50)


@pytest.fixture(scope="session")
def h3_extractor() -> H3Extractor:
    """Session-scoped H3Extractor instance.

    Expensive due to internal pipeline and executor initialization.
    """
    return H3Extractor()


@pytest.fixture
def synthetic_h3(
    h3_extractor: H3Extractor,
    batch_size: int,
    minimal_demand_set: Set[Tuple[int, int, int, int]],
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H3 features extracted from synthetic R3 v1 data.

    Returns the sparse feature dictionary mapping 4-tuples to (B, T) tensors.
    Uses a minimal demand set (50 tuples) for fast execution.
    """
    # H3 extractor expects (B, T, 97) but operates on v1 49D indices.
    # We generate (B, T, 49) and the demand set references indices 0-48.
    r3_v1 = generate_r3_v1(B=batch_size, T=100)
    output = h3_extractor.extract(r3_v1, minimal_demand_set)
    return output.features


# ======================================================================
# Brain orchestrator
# ======================================================================

@pytest.fixture(scope="session")
def brain_orchestrator() -> BrainOrchestrator:
    """Session-scoped BrainOrchestrator instance.

    Initialises all 10 mechanisms, 9 cognitive units (96 models),
    and 5 pathways. Expensive -- shared across all tests in a session.
    """
    return BrainOrchestrator()


# ======================================================================
# Aggregated H3 demand (all models + mechanisms)
# ======================================================================

@pytest.fixture(scope="session")
def all_h3_demands(
    brain_orchestrator: BrainOrchestrator,
) -> Set[Tuple[int, int, int, int]]:
    """Complete set of H3 demand 4-tuples from all models and mechanisms.

    Aggregates h3_demand from:
    - All 96 models across 9 cognitive units (via h3_demand_tuples())
    - All 10 mechanisms (via h3_demand property)

    This represents the full demand set the Brain would request from H3.
    """
    demand: Set[Tuple[int, int, int, int]] = set()

    # Collect from all units -> all models
    for unit_name in UNIT_ORDER:
        unit = brain_orchestrator._units[unit_name]
        demand |= unit.h3_demand

    # Collect from all mechanisms
    for mech_name, mech in brain_orchestrator._mechanism_runner._mechanisms.items():
        demand |= mech.h3_demand

    return demand
