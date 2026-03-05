"""V5 EEG Encoding — fixtures."""
from __future__ import annotations

import pytest

from Validation.config.paths import NMED_T_DIR


@pytest.fixture(scope="session")
def nmed_t_dir():
    """Path to NMED-T dataset.

    Accepts either:
    - MAT format: cleaned_eeg/songXX_Imputed.mat files (Stanford download)
    - MNE format: sub-XX/ directories with .set/.fif files (pre-converted)
    """
    if not NMED_T_DIR.exists():
        pytest.skip("NMED-T dataset not downloaded")

    # Check for MAT files (direct Stanford download)
    mat_files = list((NMED_T_DIR / "cleaned_eeg").glob("song*_Imputed.mat")) \
        if (NMED_T_DIR / "cleaned_eeg").exists() else []

    # Check for MNE sub-* directories
    sub_dirs = [d for d in NMED_T_DIR.iterdir()
                if d.is_dir() and d.name.startswith("sub")]

    if not mat_files and not sub_dirs:
        pytest.skip("NMED-T dataset not downloaded (no MAT or sub-* dirs)")

    return NMED_T_DIR
