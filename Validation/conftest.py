"""Root pytest configuration and session-scoped fixtures for MI Validation."""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Also ensure Validation root is importable
VALIDATION_ROOT = Path(__file__).resolve().parent
if str(VALIDATION_ROOT) not in sys.path:
    sys.path.insert(0, str(VALIDATION_ROOT))

from Validation.config.paths import TEST_AUDIO, ensure_dirs


# ── Markers ──

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "v1: Pharmacology validation")
    config.addinivalue_line("markers", "v2: IDyOM benchmark")
    config.addinivalue_line("markers", "v3: Krumhansl tonal profiles")
    config.addinivalue_line("markers", "v4: DEAM continuous emotion")
    config.addinivalue_line("markers", "v5: EEG encoding models")
    config.addinivalue_line("markers", "v6: fMRI encoding models")
    config.addinivalue_line("markers", "v7: RSA analysis")
    config.addinivalue_line("markers", "slow: Tests > 60s")
    config.addinivalue_line("markers", "requires_download: Needs external dataset")


# ── Session fixtures ──

@pytest.fixture(scope="session", autouse=True)
def _ensure_output_dirs():
    """Create all output directories at session start."""
    ensure_dirs()


@pytest.fixture(scope="session")
def mi_bridge():
    """Session-scoped MI pipeline bridge (expensive init ~5-10s)."""
    from Validation.infrastructure.mi_bridge import MIBridge
    return MIBridge()


@pytest.fixture(scope="session")
def test_audio_dir() -> Path:
    """Path to Test-Audio directory."""
    if not TEST_AUDIO.exists():
        pytest.skip(f"Test-Audio directory not found: {TEST_AUDIO}")
    return TEST_AUDIO


@pytest.fixture(scope="session")
def bach_audio(test_audio_dir) -> Path:
    """Path to Bach Cello Suite audio."""
    path = test_audio_dir / "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav"
    if not path.exists():
        pytest.skip(f"Bach audio not found: {path}")
    return path


@pytest.fixture(scope="session")
def bach_result(mi_bridge, bach_audio):
    """Pre-computed MI result for Bach Cello Suite (30s excerpt)."""
    return mi_bridge.run(bach_audio, excerpt_s=30.0)


@pytest.fixture(scope="session")
def herald_audio(test_audio_dir) -> Path:
    """Path to Herald of the Change audio."""
    path = test_audio_dir / "Herald of the Change - Hans Zimmer.wav"
    if not path.exists():
        pytest.skip(f"Herald audio not found: {path}")
    return path


@pytest.fixture(scope="session")
def result_cache():
    """Session-scoped result cache."""
    from Validation.infrastructure.cache import ResultCache
    return ResultCache()
