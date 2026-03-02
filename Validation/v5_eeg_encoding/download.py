"""NMED-T EEG dataset downloader (Stanford Digital Repository)."""
from __future__ import annotations

from pathlib import Path

from Validation.config.paths import NMED_T_DIR


def download_nmed_t(force: bool = False) -> Path:
    """Download NMED-T dataset from Stanford Digital Repository.

    NMED-T: 20 subjects, 128-channel EEG, tempo-varied naturalistic music.
    ~39 GB total. Requires manual acceptance of Stanford DUA.

    Returns:
        Path to dataset directory.
    """
    NMED_T_DIR.mkdir(parents=True, exist_ok=True)
    marker = NMED_T_DIR / ".download_complete"

    if marker.exists() and not force:
        print("[NMED-T] Already downloaded")
        return NMED_T_DIR

    print(
        "[NMED-T] This dataset requires manual download from Stanford Digital Repository.\n"
        "  URL: https://purl.stanford.edu/jn859kj8079\n"
        "  1. Accept the Data Use Agreement\n"
        "  2. Download files to: {}\n".format(NMED_T_DIR)
    )

    return NMED_T_DIR


if __name__ == "__main__":
    download_nmed_t()
