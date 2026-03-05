"""Run MI emotion extraction on DEAM audio files.

Hybrid approach: blends R³ acoustic features (energy, onset, spectral flux)
with Ψ³ cognitive affect (DA/NE/OPI neurochemistry).  DEAM arousal is
primarily acoustic-driven (Eerola & Vuoskoski 2011: energy r≈0.65), so
R³ carries the primary signal; Ψ³ adds cognitive modulation.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

from Validation.infrastructure.mi_bridge import MIBridge
from Validation.v4_deam.preprocess import resample_mi_to_deam

# R³ feature indices (from R3-ONTOLOGY-BOUNDARY)
_R3_ROUGHNESS = 5         # Group A — sensory dissonance
_R3_LOUDNESS = 10         # Group B — perceived loudness
_R3_ONSET_STRENGTH = 11   # Group B — transient salience
_R3_TONALNESS = 14        # Group C — harmonic clarity
_R3_SPECTRAL_FLUX = 21    # Group D — timbral change rate


def _norm_01(x: np.ndarray) -> np.ndarray:
    """Min-max normalize to [0, 1].  Pearson r is scale-invariant, but
    normalization is needed before weighted combination."""
    mn, mx = x.min(), x.max()
    return (x - mn) / (mx - mn + 1e-8)


def extract_valence_arousal(
    bridge: MIBridge,
    audio_path: Path,
    excerpt_s: float = 60.0,
) -> Dict[str, np.ndarray]:
    """Run MI on a DEAM audio file and extract valence/arousal at 2Hz.

    Uses hybrid R³ + Ψ³ extraction:
    - Arousal: 0.40×loudness + 0.25×onset_strength + 0.15×spectral_flux
              + 0.20×Ψ³_arousal (NE/OPI)
    - Valence: 0.35×Ψ³_valence (DA) + 0.30×tonalness + 0.35×consonance

    Args:
        bridge: MI pipeline bridge.
        audio_path: Path to DEAM WAV file.
        excerpt_s: Duration (DEAM songs are 45-60s).

    Returns:
        Dict with 'valence_2hz' and 'arousal_2hz' arrays.
    """
    result = bridge.run(audio_path, excerpt_s=excerpt_s)

    # --- Ψ³ affect domain: 4D (valence, arousal, tension, dominance) ---
    affect = result.psi.get("affect", np.zeros((result.n_frames, 4)))
    psi_valence = affect[:, 0]   # 0.9×DA + 0.1×OPI
    psi_arousal = affect[:, 1]   # 0.7×NE + 0.3×OPI

    # --- R³ acoustic features at 172 Hz ---
    r3 = result.r3  # (T, 97)
    loudness = r3[:, _R3_LOUDNESS]
    onset_strength = r3[:, _R3_ONSET_STRENGTH]
    spectral_flux = r3[:, _R3_SPECTRAL_FLUX]
    roughness = r3[:, _R3_ROUGHNESS]
    tonalness = r3[:, _R3_TONALNESS]

    # --- Hybrid arousal: acoustic energy dominates (Eerola & Vuoskoski 2011) ---
    arousal_172 = (
        0.40 * _norm_01(loudness)
        + 0.25 * _norm_01(onset_strength)
        + 0.15 * _norm_01(spectral_flux)
        + 0.20 * _norm_01(psi_arousal)
    )

    # --- Hybrid valence: cognitive + consonance (Pallesen et al. 2005) ---
    consonance = 1.0 - roughness  # low roughness → pleasant
    valence_172 = (
        0.35 * _norm_01(psi_valence)
        + 0.30 * _norm_01(tonalness)
        + 0.35 * _norm_01(consonance)
    )

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
