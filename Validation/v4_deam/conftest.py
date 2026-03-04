"""V4 DEAM — fixtures for continuous emotion validation."""
from __future__ import annotations

import pytest

from Validation.config.paths import DEAM_DIR


@pytest.fixture(scope="session")
def deam_audio_dir():
    """Path to DEAM audio directory."""
    audio_dir = DEAM_DIR / "audio"
    if not audio_dir.exists() or not list(audio_dir.rglob("*.mp3")):
        pytest.skip("DEAM audio not downloaded. Run: python -m v4_deam.download")
    return audio_dir


@pytest.fixture(scope="session")
def deam_annotations_dir():
    """Path to DEAM annotations directory."""
    ann_dir = DEAM_DIR / "annotations"
    if not ann_dir.exists():
        pytest.skip("DEAM annotations not downloaded. Run: python -m v4_deam.download")
    return ann_dir
