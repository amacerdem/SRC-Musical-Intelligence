"""DEAM dataset downloader — 1,802 songs with continuous emotion annotations."""
from __future__ import annotations

from pathlib import Path

from Validation.config.paths import DEAM_DIR
from Validation.infrastructure.downloader import download_and_extract


# DEAM URLs (University of Geneva)
DEAM_ANNOTATIONS_URL = "https://cvml.unige.ch/databases/DEAM/DEAM_Annotations.zip"
DEAM_AUDIO_URL = "https://cvml.unige.ch/databases/DEAM/DEAM_audio.zip"


def download_annotations(force: bool = False) -> Path:
    """Download DEAM annotation files (valence/arousal at 2Hz)."""
    return download_and_extract(
        DEAM_ANNOTATIONS_URL,
        DEAM_DIR / "annotations",
        force=force,
    )


def download_audio(force: bool = False) -> Path:
    """Download DEAM audio excerpts (~1.3 GB)."""
    return download_and_extract(
        DEAM_AUDIO_URL,
        DEAM_DIR / "audio",
        force=force,
    )


def download_all(force: bool = False) -> dict[str, Path]:
    """Download complete DEAM dataset."""
    return {
        "annotations": download_annotations(force=force),
        "audio": download_audio(force=force),
    }


if __name__ == "__main__":
    print("[DEAM] Starting download...")
    paths = download_all()
    for key, path in paths.items():
        print(f"  {key}: {path}")
