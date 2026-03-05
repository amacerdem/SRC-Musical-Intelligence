"""Run MI's prediction error on melodic corpora.

Extracts C³ information-content belief (#25) from MI's full pipeline for
comparison with IDyOM's information content.  Both measure melodic surprise:
IDyOM via conditional probability, MI via Bayesian belief update on the
"current event is unexpected" hypothesis (F2/ICEM).
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from Validation.config.constants import FRAME_RATE
from Validation.infrastructure.mi_bridge import MIBridge

# C³ belief index for information_content (F2/ICEM, Core, τ=0.35)
_IC_BELIEF_IDX = 25


def extract_mi_prediction_error(
    bridge: MIBridge,
    audio_path: Path,
) -> np.ndarray:
    """Run MI on audio and extract information-content time series.

    Uses C³ belief #25 (information_content) which is the Bayesian posterior
    for "the current event is unexpected".  This is MI's direct analogue of
    IDyOM's information content: both quantify melodic surprise, but MI
    derives it from acoustic features via the full R³→H³→C³ pipeline while
    IDyOM uses conditional pitch probabilities.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Path to WAV file.

    Returns:
        (T,) information-content time series at 172 Hz.
    """
    result = bridge.run(audio_path, excerpt_s=None)
    ic = result.beliefs[:, _IC_BELIEF_IDX]  # (T,)
    return np.asarray(ic, dtype=np.float64)


def extract_per_note_pe(
    bridge: MIBridge,
    melody: Dict,
    audio_path: Path,
) -> np.ndarray:
    """Extract MI information content at each note onset.

    For each onset, takes the *peak* IC in a small window around the
    onset time, which is more robust than a single-frame sample.

    Args:
        bridge: MI pipeline bridge.
        melody: Melody dict with 'onsets' in seconds.
        audio_path: Corresponding WAV file.

    Returns:
        (N_notes-1,) IC at each note onset (excluding first).
    """
    ic_timeseries = extract_mi_prediction_error(bridge, audio_path)
    T = len(ic_timeseries)

    onsets = melody.get("onsets")
    if onsets is None:
        durations = melody["durations"]
        onsets = np.cumsum(np.concatenate([[0], durations[:-1]])) * 0.5

    # Window: ±3 frames (~17 ms each side) around note onset
    half_win = 3
    ic_at_notes = []
    for onset_s in onsets[1:]:
        frame_idx = int(onset_s * FRAME_RATE)
        lo = max(0, frame_idx - half_win)
        hi = min(T, frame_idx + half_win + 1)
        ic_at_notes.append(float(ic_timeseries[lo:hi].max()))

    return np.array(ic_at_notes)


def run_mi_on_corpus(
    bridge: MIBridge,
    melody_audio_pairs: List[Tuple[Dict, Path]],
) -> List[Dict]:
    """Run MI information content extraction on a full corpus.

    Memory-optimized: flushes cache every 10 melodies for 8 GB RAM.

    Args:
        bridge: MI pipeline bridge.
        melody_audio_pairs: List of (melody_dict, wav_path) from corpora.melodies_to_audio().

    Returns:
        List of dicts with 'pe' (per-note IC), 'melody_name'.
    """
    import gc
    import torch

    results = []
    n = len(melody_audio_pairs)
    for i, (melody, audio_path) in enumerate(melody_audio_pairs):
        print(f"[V2-MI] Processing {melody['name']} ({i + 1}/{n})...")
        pe = extract_per_note_pe(bridge, melody, audio_path)
        results.append({
            "pe": pe,
            "melody_name": melody["name"],
        })
        # Flush memory every 10 melodies
        if (i + 1) % 10 == 0:
            gc.collect()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
    return results
