"""Scientific test fixtures for IMU experiments.

Provides structured (non-random) signals with known mathematical properties
for rigorous scientific analysis of IMU behavior.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest
import torch
from torch import Tensor

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Musical_Intelligence.brain.units.imu.unit import IMUUnit
from Musical_Intelligence.brain.units.imu.models import MODEL_CLASSES
from Tests.fixtures.generators import (
    generate_mechanism_outputs,
    generate_r3_v1,
    generate_h3_features,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SCI_B = 2       # batch size for scientific tests
SCI_T = 500     # time frames — long enough for spectral & statistical analysis
SCI_D = 49      # R³ v1 dimensions (used by brain models)
FRAME_RATE = 172.27  # Hz — inherited from R³/Cochlea

# R³ group boundaries (v1, 49D)
R3_GROUPS = {
    "Consonance":   (0, 7),
    "Energy":       (7, 12),
    "Timbre":       (12, 21),
    "Change":       (21, 25),
    "Interactions": (25, 49),
}

# Frequencies (Hz) injected per R³ group for structured_r3
R3_GROUP_FREQS = {
    "Consonance":   2.0,
    "Energy":       5.0,
    "Timbre":       1.0,
    "Change":       3.0,
    "Interactions": 0.5,
}


# ======================================================================
# IMU Model Instances
# ======================================================================

@pytest.fixture(scope="session")
def imu_unit() -> IMUUnit:
    """Session-scoped IMU unit instance."""
    return IMUUnit()


@pytest.fixture(scope="session")
def imu_models() -> List:
    """All 15 IMU model instances."""
    return [cls() for cls in MODEL_CLASSES]


@pytest.fixture(scope="session")
def alpha_models(imu_models) -> List:
    return [m for m in imu_models if m.TIER == "alpha"]


@pytest.fixture(scope="session")
def beta_models(imu_models) -> List:
    return [m for m in imu_models if m.TIER == "beta"]


@pytest.fixture(scope="session")
def gamma_models(imu_models) -> List:
    return [m for m in imu_models if m.TIER == "gamma"]


# ======================================================================
# H³ Demand Sets
# ======================================================================

@pytest.fixture(scope="session")
def all_imu_h3_demand(imu_models) -> Set[Tuple[int, int, int, int]]:
    """Union of all 15 IMU model H³ demands as 4-tuples."""
    demand: Set[Tuple[int, int, int, int]] = set()
    for model in imu_models:
        for spec in model.h3_demand:
            demand.add(spec.as_tuple())
    return demand


# ======================================================================
# Structured R³ Signals
# ======================================================================

@pytest.fixture
def structured_r3() -> Tensor:
    """Sinusoidal R³ with known frequencies per group.

    Each R³ group oscillates at a distinct frequency, allowing ground-truth
    spectral analysis of how frequencies propagate through IMU models.

    Shape: (SCI_B, SCI_T, SCI_D)  —  values in [0, 1]
    """
    t = torch.linspace(0, SCI_T / FRAME_RATE, SCI_T)  # seconds
    r3 = torch.zeros(SCI_B, SCI_T, SCI_D)

    for group_name, (start, end) in R3_GROUPS.items():
        freq = R3_GROUP_FREQS[group_name]
        for d in range(start, end):
            phase = d * 0.3  # phase offset per dimension
            signal = 0.5 + 0.4 * torch.sin(2 * math.pi * freq * t + phase)
            r3[:, :, d] = signal

    return r3


@pytest.fixture
def step_r3() -> Tensor:
    """Step function R³: 0.3 for t < T/2, 0.7 for t >= T/2.

    Shape: (SCI_B, SCI_T, SCI_D)
    Enables impulse response and transition analysis.
    """
    r3 = torch.full((SCI_B, SCI_T, SCI_D), 0.3)
    r3[:, SCI_T // 2:, :] = 0.7
    return r3


@pytest.fixture
def random_r3() -> Tensor:
    """Uniform random R³ for baseline comparisons.

    Shape: (SCI_B, SCI_T, SCI_D)
    """
    return generate_r3_v1(B=SCI_B, T=SCI_T, seed=42)


@pytest.fixture
def high_batch_r3() -> Tensor:
    """Random R³ with large batch for ergodicity tests.

    Shape: (8, SCI_T, SCI_D)
    """
    return generate_r3_v1(B=8, T=SCI_T, seed=42)


# ======================================================================
# Mechanism Outputs
# ======================================================================

@pytest.fixture
def mechanism_outputs() -> Dict[str, Tensor]:
    """All 10 mechanism outputs, random (SCI_B, SCI_T, 30)."""
    return generate_mechanism_outputs(B=SCI_B, T=SCI_T, seed=42)


@pytest.fixture
def mechanism_outputs_high_batch() -> Dict[str, Tensor]:
    """All 10 mechanism outputs, B=8."""
    return generate_mechanism_outputs(B=8, T=SCI_T, seed=42)


@pytest.fixture
def zero_mechanism_outputs() -> Dict[str, Tensor]:
    """All mechanisms output zeros — isolates R³ contribution."""
    from Tests.fixtures.generators import MECHANISM_NAMES, MECHANISM_DIM
    return {name: torch.zeros(SCI_B, SCI_T, MECHANISM_DIM) for name in MECHANISM_NAMES}


@pytest.fixture
def zero_r3() -> Tensor:
    """All-zero R³ — isolates mechanism contribution."""
    return torch.zeros(SCI_B, SCI_T, SCI_D)


# ======================================================================
# H³ Feature Generators (Controlled)
# ======================================================================

def _make_h3_constant(
    demand: Set[Tuple[int, int, int, int]], value: float
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features with a constant value for all demanded tuples."""
    return {key: torch.full((SCI_B, SCI_T), value) for key in sorted(demand)}


def _make_h3_sinusoidal(
    demand: Set[Tuple[int, int, int, int]], freq_hz: float
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features oscillating at given frequency."""
    t = torch.linspace(0, SCI_T / FRAME_RATE, SCI_T)
    features = {}
    for i, key in enumerate(sorted(demand)):
        phase = i * 0.5
        signal = 0.5 + 0.4 * torch.sin(2 * math.pi * freq_hz * t + phase)
        features[key] = signal.unsqueeze(0).expand(SCI_B, -1)
    return features


@pytest.fixture
def h3_ones(all_imu_h3_demand) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features all = 1.0 → h3_mod = 1.0"""
    return _make_h3_constant(all_imu_h3_demand, 1.0)


@pytest.fixture
def h3_zeros(all_imu_h3_demand) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features all = 0.0 → h3_mod = 0.5^4 = 0.0625"""
    return _make_h3_constant(all_imu_h3_demand, 0.0)


@pytest.fixture
def h3_half(all_imu_h3_demand) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features all = 0.5 → h3_mod = 0.75^4 ≈ 0.3164"""
    return _make_h3_constant(all_imu_h3_demand, 0.5)


@pytest.fixture
def h3_random(all_imu_h3_demand) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features random [0,1]."""
    return generate_h3_features(B=SCI_B, T=SCI_T, demand_set=all_imu_h3_demand, seed=42)


@pytest.fixture
def h3_sinusoidal_3hz(all_imu_h3_demand) -> Dict[Tuple[int, int, int, int], Tensor]:
    """H³ features oscillating at 3 Hz."""
    return _make_h3_sinusoidal(all_imu_h3_demand, 3.0)


# ======================================================================
# Per-horizon H³ features (for consolidation analysis)
# ======================================================================

def _make_h3_per_horizon(
    demand: Set[Tuple[int, int, int, int]],
) -> Dict[int, Dict[Tuple[int, int, int, int], Tensor]]:
    """Group H³ features by horizon, with random values per group."""
    by_horizon: Dict[int, Set[Tuple[int, int, int, int]]] = {}
    for key in demand:
        h = key[1]
        by_horizon.setdefault(h, set()).add(key)

    result = {}
    for h, keys in by_horizon.items():
        gen = torch.Generator().manual_seed(h)
        result[h] = {
            key: torch.rand(SCI_B, SCI_T, generator=gen) for key in sorted(keys)
        }
    return result


@pytest.fixture
def h3_by_horizon(all_imu_h3_demand):
    """H³ features grouped by horizon with distinct random patterns."""
    return _make_h3_per_horizon(all_imu_h3_demand)


# ======================================================================
# Helper to run a model with given inputs
# ======================================================================

def run_model(model, mechanism_outputs, h3_features, r3_features):
    """Run a single model's compute() and return output tensor."""
    return model.compute(mechanism_outputs, h3_features, r3_features)


def run_imu_unit(imu_unit, mechanism_outputs, h3_features, r3_features):
    """Run full IMU unit: inject mechanisms then compute."""
    imu_unit.set_mechanism_outputs(mechanism_outputs)
    return imu_unit.compute(h3_features, r3_features)
