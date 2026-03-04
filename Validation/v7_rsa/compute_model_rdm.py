"""Compute MI Representational Dissimilarity Matrices (RDMs).

For a set of stimuli, computes the pairwise dissimilarity of MI's
131-belief representations. The resulting RDM captures MI's internal
similarity structure.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
from scipy.spatial.distance import pdist, squareform

from Validation.infrastructure.mi_bridge import MIBridge


def compute_belief_rdm(
    bridge: MIBridge,
    audio_paths: List[Path],
    excerpt_s: float = 30.0,
    metric: str = "euclidean",
) -> np.ndarray:
    """Compute RDM from MI's 131-belief representations.

    For each stimulus, computes mean belief vector, then pairwise
    dissimilarity across all stimuli.

    Uses euclidean distance because post-sigmoid beliefs cluster near 0.5,
    making correlation distance very small. Euclidean distance captures the
    absolute magnitude of cognitive-state differences between stimuli.

    Args:
        bridge: MI pipeline bridge.
        audio_paths: List of stimulus audio paths.
        excerpt_s: Max duration per stimulus.
        metric: Distance metric ('euclidean', 'correlation', 'cosine').

    Returns:
        (N, N) RDM matrix (symmetric, zero diagonal).
    """
    belief_vectors = []
    for path in audio_paths:
        print(f"[V7] Computing beliefs for {path.name}...")
        result = bridge.run(path, excerpt_s=excerpt_s)
        # Mean belief vector across time
        belief_vectors.append(result.beliefs.mean(axis=0))

    X = np.stack(belief_vectors)  # (N_stimuli, 131)

    # Compute pairwise distances
    distances = pdist(X, metric=metric)
    rdm = squareform(distances)

    return rdm


def compute_ram_rdm(
    bridge: MIBridge,
    audio_paths: List[Path],
    excerpt_s: float = 30.0,
) -> np.ndarray:
    """Compute RDM from MI's 26-region activation patterns.

    Args:
        bridge: MI pipeline bridge.
        audio_paths: Stimulus paths.
        excerpt_s: Max duration.

    Returns:
        (N, N) RDM from region activation patterns.
    """
    ram_vectors = []
    for path in audio_paths:
        result = bridge.run(path, excerpt_s=excerpt_s)
        ram_vectors.append(result.ram.mean(axis=0))

    X = np.stack(ram_vectors)  # (N_stimuli, 26)
    distances = pdist(X, metric="correlation")
    return squareform(distances)


def compute_neuro_rdm(
    bridge: MIBridge,
    audio_paths: List[Path],
    excerpt_s: float = 30.0,
) -> np.ndarray:
    """Compute RDM from MI's neurochemical profiles.

    Returns:
        (N, N) RDM from 4D neurochemical state.
    """
    neuro_vectors = []
    for path in audio_paths:
        result = bridge.run(path, excerpt_s=excerpt_s)
        neuro_vectors.append(result.neuro.mean(axis=0))

    X = np.stack(neuro_vectors)  # (N_stimuli, 4)
    distances = pdist(X, metric="euclidean")
    return squareform(distances)


def compute_r3_rdm(
    bridge: MIBridge,
    audio_paths: List[Path],
    excerpt_s: float = 30.0,
) -> np.ndarray:
    """Compute RDM from R³ acoustic features only (baseline).

    Returns:
        (N, N) RDM from 97D spectral features.
    """
    r3_vectors = []
    for path in audio_paths:
        result = bridge.run(path, excerpt_s=excerpt_s)
        r3_vectors.append(result.r3.mean(axis=0))

    X = np.stack(r3_vectors)  # (N_stimuli, 97)
    distances = pdist(X, metric="correlation")
    return squareform(distances)
