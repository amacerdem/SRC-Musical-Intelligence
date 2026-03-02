"""OpenNeuro fMRI dataset downloader."""
from __future__ import annotations

from pathlib import Path

from Validation.config.paths import OPENNEURO_EEG_FMRI_DIR, OPENNEURO_GENRE_FMRI_DIR
from Validation.infrastructure.downloader import download_openneuro


def download_ds002725(force: bool = False) -> Path:
    """Download ds002725: Simultaneous EEG-fMRI during affective music listening.

    21 subjects, TR=2s, affective music stimuli.
    ~25 GB total.
    """
    return download_openneuro("ds002725", OPENNEURO_EEG_FMRI_DIR, force=force)


def download_ds003720(force: bool = False) -> Path:
    """Download ds003720: Music genre fMRI dataset.

    5 subjects, 540 music pieces, 10 genres, TR=1.5s.
    ~40 GB total.
    """
    return download_openneuro("ds003720", OPENNEURO_GENRE_FMRI_DIR, force=force)


def download_all(force: bool = False) -> dict[str, Path]:
    """Download all fMRI datasets."""
    return {
        "ds002725": download_ds002725(force=force),
        "ds003720": download_ds003720(force=force),
    }


if __name__ == "__main__":
    print("[V6] Starting fMRI dataset downloads...")
    paths = download_all()
    for key, path in paths.items():
        print(f"  {key}: {path}")
