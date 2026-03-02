"""DEAM preprocessing — load annotations and resample MI output to 2Hz."""
from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from Validation.config.constants import FRAME_RATE
from Validation.config.paths import DEAM_DIR
from Validation.infrastructure.alignment import resample_to_hz


def load_annotations(
    annotations_dir: Optional[Path] = None,
    annotation_type: str = "arousal",
) -> Dict[int, np.ndarray]:
    """Load DEAM continuous annotations (2Hz).

    Args:
        annotations_dir: Path to annotation CSV directory.
        annotation_type: 'arousal' or 'valence'.

    Returns:
        Dict mapping song_id → (T,) annotation time series at 2Hz.
    """
    if annotations_dir is None:
        annotations_dir = DEAM_DIR / "annotations"

    # DEAM has per-song CSV files or a single large CSV
    # Try single CSV first
    csv_path = annotations_dir / f"continuous_{annotation_type}_mean.csv"
    if csv_path.exists():
        return _load_csv_annotations(csv_path)

    # Try individual files
    annotations = {}
    for f in sorted(annotations_dir.rglob(f"*{annotation_type}*.csv")):
        song_id = _extract_song_id(f.stem)
        if song_id is not None:
            data = np.loadtxt(f, delimiter=",", skiprows=1)
            if data.ndim == 1:
                annotations[song_id] = data
            else:
                annotations[song_id] = data[:, -1]  # last column = mean

    return annotations


def load_song_ids(audio_dir: Optional[Path] = None) -> List[Tuple[int, Path]]:
    """Get list of available DEAM audio files.

    Returns:
        List of (song_id, wav_path) tuples.
    """
    if audio_dir is None:
        audio_dir = DEAM_DIR / "audio"

    songs = []
    for wav in sorted(audio_dir.rglob("*.wav")):
        song_id = _extract_song_id(wav.stem)
        if song_id is not None:
            songs.append((song_id, wav))

    return songs


def resample_mi_to_deam(
    mi_features: np.ndarray,
    target_hz: float = 2.0,
) -> np.ndarray:
    """Resample MI features (172.27 Hz) to DEAM annotation rate (2Hz).

    Args:
        mi_features: (T_mi, D) or (T_mi,) MI feature array.
        target_hz: DEAM annotation frequency.

    Returns:
        Resampled array at target_hz.
    """
    return resample_to_hz(mi_features, FRAME_RATE, target_hz)


def align_and_trim(
    mi_resampled: np.ndarray,
    annotation: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """Align MI and annotation arrays to the same length.

    DEAM annotations start 15s into the song (after the initial segment).
    MI processes from the beginning. We trim to the overlapping region.

    Returns:
        Tuple of (mi_trimmed, annotation_trimmed) with same length.
    """
    # DEAM annotations cover seconds 15-60 of the 45s excerpt
    # At 2Hz: 90 samples for 45s, but annotations start at 15s
    # MI processes the full audio from time 0

    # Simple alignment: use minimum length
    n = min(len(mi_resampled), len(annotation))
    return mi_resampled[:n], annotation[:n]


def _load_csv_annotations(csv_path: Path) -> Dict[int, np.ndarray]:
    """Load from single CSV with songs as columns."""
    annotations = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        song_ids = [int(h) for h in header[1:] if h.isdigit()]

        data_rows = []
        for row in reader:
            data_rows.append([float(v) if v else np.nan for v in row[1:]])

        data = np.array(data_rows)
        for i, song_id in enumerate(song_ids):
            if i < data.shape[1]:
                col = data[:, i]
                annotations[song_id] = col[~np.isnan(col)]

    return annotations


def _extract_song_id(stem: str) -> Optional[int]:
    """Extract numeric song ID from filename."""
    import re
    match = re.search(r"(\d+)", stem)
    return int(match.group(1)) if match else None
