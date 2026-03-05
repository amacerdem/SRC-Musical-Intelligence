"""Run MI emotion extraction on DEAM audio files."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from Validation.infrastructure.mi_bridge import MIBridge
from Validation.v4_deam.preprocess import resample_mi_to_deam


def extract_valence_arousal(
    bridge: MIBridge,
    audio_path: Path,
    excerpt_s: float = 60.0,
) -> Dict[str, np.ndarray]:
    """Run MI on a DEAM audio file and extract valence/arousal at 2Hz.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Path to DEAM WAV file.
        excerpt_s: Duration (DEAM songs are 45-60s).

    Returns:
        Dict with 'valence_2hz' and 'arousal_2hz' arrays.
    """
    result = bridge.run(audio_path, excerpt_s=excerpt_s)

    # Ψ³ affect domain: 4D (valence, arousal, tension, energy)
    affect = result.psi.get("affect", np.zeros((result.n_frames, 4)))
    valence_172 = affect[:, 0]   # first dim = valence
    arousal_172 = affect[:, 1]   # second dim = arousal

    # Resample to 2Hz (DEAM annotation rate)
    valence_2hz = resample_mi_to_deam(valence_172)
    arousal_2hz = resample_mi_to_deam(arousal_172)

    return {
        "valence_2hz": valence_2hz,
        "arousal_2hz": arousal_2hz,
        "valence_172hz": valence_172,
        "arousal_172hz": arousal_172,
    }


def batch_extract(
    bridge: MIBridge,
    songs: List[Tuple[int, Path]],
    max_songs: int = 100,
) -> Dict[int, Dict[str, np.ndarray]]:
    """Run MI on multiple DEAM songs.

    Memory-optimized: flushes MPS/CUDA cache every 5 songs to stay
    within 8 GB RAM on MacBook Air M2.

    Args:
        bridge: MI pipeline bridge.
        songs: List of (song_id, wav_path) from preprocess.load_song_ids().
        max_songs: Maximum number of songs to process.

    Returns:
        Dict mapping song_id → valence/arousal dict (only 2 Hz arrays kept).
    """
    import gc
    import torch

    results = {}
    n = min(len(songs), max_songs)
    for i, (song_id, wav_path) in enumerate(songs[:n]):
        print(f"[V4] Processing song {song_id} ({i + 1}/{n})...")
        try:
            out = extract_valence_arousal(bridge, wav_path)
            # Keep only 2 Hz arrays — drop 172 Hz to save ~95% memory per song
            results[song_id] = {
                "valence_2hz": out["valence_2hz"],
                "arousal_2hz": out["arousal_2hz"],
            }
        except Exception as e:
            print(f"[V4] Error processing song {song_id}: {e}")
            continue

        # Flush memory every 5 songs
        if (i + 1) % 5 == 0:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            if hasattr(torch, "mps") and torch.backends.mps.is_available():
                torch.mps.empty_cache()

    return results
