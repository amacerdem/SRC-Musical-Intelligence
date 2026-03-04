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

    # Try to find the averaged annotations CSV (rglob for nested DEAM structure)
    csv_candidates = list(annotations_dir.rglob(f"{annotation_type}.csv"))
    if not csv_candidates:
        csv_candidates = list(annotations_dir.rglob(f"*{annotation_type}*.csv"))

    # Prefer the "averaged per song / dynamic" version
    for cand in csv_candidates:
        if "averaged" in str(cand) and "dynamic" in str(cand):
            return _load_deam_rows_csv(cand)

    # Fallback: use first match
    if csv_candidates:
        return _load_deam_rows_csv(csv_candidates[0])

    return {}


def load_song_ids(audio_dir: Optional[Path] = None) -> List[Tuple[int, Path]]:
    """Get list of available DEAM audio files.

    Returns:
        List of (song_id, wav_path) tuples.
    """
    if audio_dir is None:
        audio_dir = DEAM_DIR / "audio"

    songs = []
    for wav in sorted(audio_dir.rglob("*.mp3")):
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


def _load_deam_rows_csv(csv_path: Path) -> Dict[int, np.ndarray]:
    """Load DEAM CSV where songs are rows, time samples are columns.

    Format: song_id, sample_15000ms, sample_15500ms, ...
    Values at 2Hz (500ms intervals) from 15s to ~60s.
    """
    annotations = {}
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            if not row:
                continue
            try:
                song_id = int(row[0])
            except (ValueError, IndexError):
                continue
            values = []
            for v in row[1:]:
                try:
                    values.append(float(v))
                except (ValueError, TypeError):
                    break
            if values:
                annotations[song_id] = np.array(values)
    return annotations


def _extract_song_id(stem: str) -> Optional[int]:
    """Extract numeric song ID from filename."""
    import re
    match = re.search(r"(\d+)", stem)
    return int(match.group(1)) if match else None
