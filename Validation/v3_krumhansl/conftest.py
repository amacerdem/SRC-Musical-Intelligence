"""V3 Krumhansl — fixtures for tonal hierarchy validation."""
from __future__ import annotations

import pytest

from Validation.v3_krumhansl.generate_contexts import generate_tonal_context
from Validation.v3_krumhansl.extract_mi_profiles import extract_tonal_profile
from Validation.v3_krumhansl.profiles import MAJOR_PROFILE, MINOR_PROFILE


@pytest.fixture(scope="session")
def c_major_probes():
    """Generate C major context+probe stimuli."""
    return generate_tonal_context(key="C", mode="major")


@pytest.fixture(scope="session")
def c_minor_probes():
    """Generate C minor context+probe stimuli."""
    return generate_tonal_context(key="C", mode="minor")


@pytest.fixture(scope="session")
def mi_major_profile(mi_bridge, c_major_probes, module_data):
    """MI's tonal profile for C major."""
    profile = extract_tonal_profile(mi_bridge, c_major_probes)
    module_data.setdefault("v3", {})["mi_major"] = profile
    return profile


@pytest.fixture(scope="session")
def mi_minor_profile(mi_bridge, c_minor_probes, module_data):
    """MI's tonal profile for C minor."""
    profile = extract_tonal_profile(mi_bridge, c_minor_probes)
    module_data.setdefault("v3", {})["mi_minor"] = profile
    return profile


@pytest.fixture(scope="session")
def kk_major_profile():
    """Krumhansl-Kessler C major profile."""
    return MAJOR_PROFILE


@pytest.fixture(scope="session")
def kk_minor_profile():
    """Krumhansl-Kessler C minor profile."""
    return MINOR_PROFILE
