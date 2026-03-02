"""V6 fMRI Encoding — fixtures."""
from __future__ import annotations

import pytest

from Validation.config.paths import OPENNEURO_EEG_FMRI_DIR


@pytest.fixture(scope="session")
def fmri_dataset_dir():
    """Path to fMRI dataset."""
    if not OPENNEURO_EEG_FMRI_DIR.exists():
        pytest.skip("OpenNeuro ds002725 not downloaded")
    return OPENNEURO_EEG_FMRI_DIR
