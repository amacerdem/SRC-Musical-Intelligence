"""Run MI's F2 prediction error on melodic corpora.

Extracts prediction error (PE) from MI's F2 (Prediction) function
for comparison with IDyOM's information content.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from Validation.config.constants import FRAME_RATE
from Validation.infrastructure.mi_bridge import MIBridge


def extract_mi_prediction_error(
    bridge: MIBridge,
    audio_path: Path,
) -> np.ndarray:
    """Run MI on audio and extract prediction error time series.

    The F2 (Prediction) function generates prediction errors that are
    analogous to IDyOM's information content — both measure surprise.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Path to WAV file.

    Returns:
        (T,) prediction error time series.
    """
    result = bridge.run(audio_path, excerpt_s=None)

    # F2 prediction error is captured in the beliefs tensor
    # The prediction-related beliefs (indices vary by implementation)
    # Use the full belief tensor variance as a proxy for prediction error
    beliefs = result.beliefs  # (T, 131)

    # Prediction error proxy: frame-to-frame belief change magnitude
    if beliefs.shape[0] > 1:
        pe = np.sqrt(np.sum(np.diff(beliefs, axis=0) ** 2, axis=1))
        # Pad to match original length
        pe = np.concatenate([[pe[0]], pe])
    else:
        pe = np.zeros(beliefs.shape[0])

    return pe


def extract_per_note_pe(
    bridge: MIBridge,
    melody: Dict,
    audio_path: Path,
) -> np.ndarray:
    """Extract MI prediction error at each note onset.

    Args:
        bridge: MI pipeline bridge.
        melody: Melody dict with 'onsets' in seconds.
        audio_path: Corresponding WAV file.

    Returns:
        (N_notes-1,) PE at each note onset (excluding first).
    """
    pe_timeseries = extract_mi_prediction_error(bridge, audio_path)

    onsets = melody.get("onsets")
    if onsets is None:
        # Estimate onsets from durations
        durations = melody["durations"]
        onsets = np.cumsum(np.concatenate([[0], durations[:-1]])) * 0.5

    # Sample PE at note onsets (skip first note as IDyOM does)
    pe_at_notes = []
    for onset_s in onsets[1:]:
        frame_idx = int(onset_s * FRAME_RATE)
        frame_idx = min(frame_idx, len(pe_timeseries) - 1)
        pe_at_notes.append(pe_timeseries[frame_idx])

    return np.array(pe_at_notes)


def run_mi_on_corpus(
    bridge: MIBridge,
    melody_audio_pairs: List[Tuple[Dict, Path]],
) -> List[Dict]:
    """Run MI prediction error extraction on a full corpus.

    Args:
        bridge: MI pipeline bridge.
        melody_audio_pairs: List of (melody_dict, wav_path) from corpora.melodies_to_audio().

    Returns:
        List of dicts with 'pe' (per-note PE), 'melody_name'.
    """
    results = []
    for melody, audio_path in melody_audio_pairs:
        print(f"[V2-MI] Processing {melody['name']}...")
        pe = extract_per_note_pe(bridge, melody, audio_path)
        results.append({
            "pe": pe,
            "melody_name": melody["name"],
        })
    return results
