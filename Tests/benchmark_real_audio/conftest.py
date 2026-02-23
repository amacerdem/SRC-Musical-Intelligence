"""Benchmark Real Audio — pytest fixtures for 11 deep tests.

Session-scope fixtures for R³/H³ extractors, mechanisms, and demand sets.
Shared constants and helpers live in helpers.py (importable by test modules).
"""
from __future__ import annotations

import importlib
import pathlib
import sys
from typing import Any, Dict, List, Set, Tuple

import pytest
from torch import Tensor

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

_TEST_AUDIO_DIR = _PROJECT_ROOT / "Test-Audio"

# Import shared helpers (after sys.path is set)
from Tests.benchmark_real_audio.helpers import load_audio_file


# ---------------------------------------------------------------------------
# Custom markers
# ---------------------------------------------------------------------------
def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "benchmark: Real audio benchmark")
    config.addinivalue_line("markers", "slow: Tests > 30s")
    config.addinivalue_line("markers", "memory: Memory profiling tests")


# ---------------------------------------------------------------------------
# Session-scope fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def audio_dir() -> pathlib.Path:
    if not _TEST_AUDIO_DIR.exists():
        pytest.skip(f"Test-Audio directory not found: {_TEST_AUDIO_DIR}")
    return _TEST_AUDIO_DIR


@pytest.fixture(scope="session")
def r3_extractor():
    """R³ extractor singleton."""
    try:
        from Musical_Intelligence.ear.r3.extractor import R3Extractor
        return R3Extractor()
    except Exception as e:
        pytest.skip(f"R³ extractor unavailable: {e}")


@pytest.fixture(scope="session")
def h3_extractor():
    """H³ extractor singleton."""
    try:
        from Musical_Intelligence.ear.h3.extractor import H3Extractor
        return H3Extractor()
    except Exception as e:
        pytest.skip(f"H³ extractor unavailable: {e}")


@pytest.fixture(scope="session")
def all_mechanisms() -> List[Any]:
    """All mechanism instances from F1-F9."""
    try:
        from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase
        instances = _collect_mechanism_instances(_NucleusBase)
        if not instances:
            pytest.skip("No mechanisms found")
        return instances
    except Exception as e:
        pytest.skip(f"Mechanism collection failed: {e}")


@pytest.fixture(scope="session")
def all_relays(all_mechanisms) -> List[Any]:
    from Musical_Intelligence.contracts.bases.nucleus import Relay
    return [m for m in all_mechanisms if isinstance(m, Relay)]


@pytest.fixture(scope="session")
def h3_demand_set(all_mechanisms) -> Set[Tuple[int, int, int, int]]:
    """Union of all mechanism h3_demands as 4-tuples."""
    demands: Set[Tuple[int, int, int, int]] = set()
    for m in all_mechanisms:
        for spec in m.h3_demand:
            demands.add(spec.as_tuple())
    return demands


@pytest.fixture(scope="session")
def bach_mel() -> Tuple[Tensor, Tensor, float]:
    return load_audio_file("bach")


@pytest.fixture(scope="session")
def swan_mel() -> Tuple[Tensor, Tensor, float]:
    return load_audio_file("swan")


@pytest.fixture(scope="session")
def herald_mel() -> Tuple[Tensor, Tensor, float]:
    return load_audio_file("herald")


# ---------------------------------------------------------------------------
# Helper: collect mechanisms (reuse smoke test pattern)
# ---------------------------------------------------------------------------
_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")


def _collect_mechanism_instances(base_class: type) -> List[Any]:
    instances: List[Any] = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls is None:
                    continue
                try:
                    if isinstance(cls, type) and issubclass(cls, base_class):
                        instances.append(cls())
                except Exception:
                    continue
        except Exception:
            # Fallback: individual subpackages
            pkg_dir = _PROJECT_ROOT / "Musical_Intelligence" / "brain" / "functions" / fn / "mechanisms"
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                sub_mod_path = f"{mod_path}.{sub.name}"
                try:
                    sub_mod = importlib.import_module(sub_mod_path)
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr is None:
                        continue
                    try:
                        if (isinstance(attr, type)
                                and issubclass(attr, base_class)
                                and attr is not base_class
                                and not attr_name.startswith("_")):
                            instances.append(attr())
                    except Exception:
                        continue
    return instances
