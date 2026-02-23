"""Global test configuration — markers, session-scope fixtures."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch

# ---------------------------------------------------------------------------
# Ensure Musical_Intelligence package is importable
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Custom markers
# ---------------------------------------------------------------------------

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "smoke: Smoke Test 001")
    config.addinivalue_line("markers", "slow: Tests > 10s")
    config.addinivalue_line("markers", "integration: Cross-layer tests")


# ---------------------------------------------------------------------------
# Session-scope fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def device() -> torch.device:
    return torch.device("cpu")


@pytest.fixture(scope="session")
def batch_size() -> int:
    return 2


@pytest.fixture(scope="session")
def time_steps() -> int:
    """T=100 ≈ 0.58 s at 172.27 Hz frame rate."""
    return 100
