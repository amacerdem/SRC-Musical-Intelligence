"""V6 fMRI Encoding — fixtures."""
from __future__ import annotations

import os

import pytest

from Validation.config.paths import OPENNEURO_EEG_FMRI_DIR

# NIfTI loading + nilearn smoothing + ROI extraction needs ~6-7 GB.
# Skip on machines with ≤ 8 GB physical RAM to prevent OOM / pink screen.
_MIN_RAM_GB = 12


def _system_ram_gb() -> float:
    """Return total physical RAM in GB (macOS / Linux)."""
    try:
        mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        return mem / (1024 ** 3)
    except (ValueError, OSError):
        return 0.0


@pytest.fixture(scope="session")
def fmri_dataset_dir():
    """Path to fMRI dataset — skips when RAM < 12 GB."""
    ram = _system_ram_gb()
    if ram > 0 and ram < _MIN_RAM_GB:
        pytest.skip(
            f"V6 fMRI requires ≥{_MIN_RAM_GB} GB RAM "
            f"(this machine has {ram:.0f} GB)"
        )
    if not OPENNEURO_EEG_FMRI_DIR.exists():
        pytest.skip("OpenNeuro ds002725 not downloaded")
    return OPENNEURO_EEG_FMRI_DIR
