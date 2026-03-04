"""V7 RSA — fixtures."""
from __future__ import annotations

import re

import pytest


@pytest.fixture(scope="session")
def rsa_stimuli(test_audio_dir):
    """Get list of unique audio stimuli for RSA analysis.

    Deduplicates files that have hash-suffixed variants (e.g.
    'Cello_Suite_..._9fb7a346.wav' is a duplicate of the original).
    """
    all_wavs = sorted(test_audio_dir.glob("*.wav"))

    # Filter out hash-suffixed duplicates (filename ending in _<hex8>.wav)
    unique = []
    for path in all_wavs:
        if re.search(r"_[0-9a-f]{8}\.wav$", path.name):
            continue
        unique.append(path)

    if len(unique) < 3:
        pytest.skip("Need at least 3 unique stimuli for RSA")
    return unique[:10]
