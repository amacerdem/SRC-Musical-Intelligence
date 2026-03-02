"""Compute baseline RDMs for RSA comparison."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
from scipy.spatial.distance import pdist, squareform

from Validation.infrastructure.audio_loader import load_audio


def compute_acoustic_rdm(
    audio_paths: List[Path],
    n_features: int = 13,
) -> np.ndarray:
    """Compute RDM from MFCC acoustic features (baseline).

    Args:
        audio_paths: Stimulus audio paths.
        n_features: Number of MFCCs.

    Returns:
        (N, N) acoustic RDM.
    """
    import librosa

    vectors = []
    for path in audio_paths:
        audio, sr = load_audio(path, mono=True)
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=n_features)
        vectors.append(mfcc.mean(axis=1))

    X = np.stack(vectors)
    distances = pdist(X, metric="correlation")
    return squareform(distances)


def compute_spectral_rdm(
    audio_paths: List[Path],
    n_bands: int = 40,
) -> np.ndarray:
    """Compute RDM from mel-spectrogram features.

    Args:
        audio_paths: Stimulus audio paths.
        n_bands: Number of mel bands.

    Returns:
        (N, N) spectral RDM.
    """
    import librosa

    vectors = []
    for path in audio_paths:
        audio, sr = load_audio(path, mono=True)
        mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_bands)
        mel_db = librosa.power_to_db(mel, ref=np.max)
        vectors.append(mel_db.mean(axis=1))

    X = np.stack(vectors)
    distances = pdist(X, metric="correlation")
    return squareform(distances)


def compute_genre_rdm(
    labels: List[str],
) -> np.ndarray:
    """Compute categorical RDM from genre labels.

    Same genre = 0, different genre = 1.

    Args:
        labels: Genre label per stimulus.

    Returns:
        (N, N) binary RDM.
    """
    n = len(labels)
    rdm = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            rdm[i, j] = 0.0 if labels[i] == labels[j] else 1.0
    return rdm
