"""V7 RSA — fixtures."""
from __future__ import annotations

import pytest


@pytest.fixture(scope="session")
def rsa_stimuli(test_audio_dir):
    """Get list of audio stimuli for RSA analysis."""
    stimuli = sorted(test_audio_dir.glob("*.wav"))
    if len(stimuli) < 3:
        pytest.skip("Need at least 3 stimuli for RSA")
    return stimuli[:10]  # Use up to 10 for manageable compute
