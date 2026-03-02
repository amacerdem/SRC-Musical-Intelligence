"""V5 EEG Encoding — fixtures."""
from __future__ import annotations

import pytest

from Validation.config.paths import NMED_T_DIR


@pytest.fixture(scope="session")
def nmed_t_dir():
    """Path to NMED-T dataset."""
    if not NMED_T_DIR.exists() or not list(NMED_T_DIR.iterdir()):
        pytest.skip("NMED-T dataset not downloaded")
    return NMED_T_DIR
