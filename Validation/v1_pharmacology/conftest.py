"""V1 Pharmacology — fixtures for pharmacological simulation tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from Validation.v1_pharmacology.simulate import PharmacologicalSimulator
from Validation.v1_pharmacology.targets import (
    FERRERI_TARGETS,
    LAENG_TARGETS,
    MALLIK_TARGETS,
)


@pytest.fixture(scope="session")
def pharma_sim(mi_bridge) -> PharmacologicalSimulator:
    """Session-scoped pharmacological simulator."""
    return PharmacologicalSimulator(mi_bridge)


@pytest.fixture(scope="session")
def test_stimulus(test_audio_dir) -> Path:
    """Pick a suitable test stimulus for pharmacological simulation.

    Uses Bach Cello Suite — a well-structured piece that reliably
    engages reward and emotional processing.
    """
    path = test_audio_dir / "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav"
    if not path.exists():
        pytest.skip("Bach audio not available")
    return path


@pytest.fixture(scope="session")
def ferreri_results(pharma_sim, test_stimulus):
    """Run Ferreri et al. 2019 battery: levodopa, risperidone, placebo."""
    return pharma_sim.simulate_battery(test_stimulus, FERRERI_TARGETS)


@pytest.fixture(scope="session")
def mallik_results(pharma_sim, test_stimulus):
    """Run Mallik et al. 2017 battery: naltrexone, placebo."""
    return pharma_sim.simulate_battery(test_stimulus, MALLIK_TARGETS)


@pytest.fixture(scope="session")
def laeng_results(pharma_sim, test_stimulus):
    """Run Laeng et al. 2021 battery: naltrexone, placebo."""
    return pharma_sim.simulate_battery(test_stimulus, LAENG_TARGETS)
