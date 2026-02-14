"""Synthetic data generators for the MI test suite.

Provides deterministic (seeded) generators for every stage of the MI pipeline.
All generators produce tensors with values in [0, 1] and correct shapes to
satisfy the contracts defined in Musical_Intelligence.contracts.

Generator summary:
    generate_mel            -> (B, n_mels, T)   mel spectrogram
    generate_r3             -> (B, T, D)         R3 spectral features (128D)
    generate_r3_v1          -> (B, T, 49)        R3 v1 spectral features (49D)
    generate_h3_features    -> Dict[4-tuple, (B, T)]  sparse H3 features
    generate_minimal_demand -> Set[4-tuple]      random demand set
    generate_mechanism_outputs -> Dict[str, (B, T, 30)]  all 10 mechanisms
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, Set, Tuple

import torch
from torch import Tensor


# ======================================================================
# Constants
# ======================================================================

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

AUDIO_DIR: Path = _PROJECT_ROOT / "Test-Audio"
"""Path to the Test-Audio/ directory containing reference audio files."""

SWAN_LAKE_PATH: Path = (
    AUDIO_DIR
    / "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
    " - Pyotr Ilyich Tchaikovsky.wav"
)
"""Path to the Swan Lake reference audio file used for benchmarking."""

# H3 dimension constants (from Musical_Intelligence.ear.h3.constants)
_N_R3_V1 = 49       # R3 v1 feature count
_N_R3_V2 = 128      # R3 v2 feature count
_N_HORIZONS = 32    # H3 horizon count (H0-H31)
_N_MORPHS = 24      # H3 morph count (M0-M23)
_N_LAWS = 3         # H3 law count (L0-L2)

# Brain mechanism names (from Musical_Intelligence.brain.mechanisms)
MECHANISM_NAMES: Tuple[str, ...] = (
    "PPC", "TPC", "BEP", "ASA", "TMH",
    "MEM", "SYN", "AED", "CPD", "C0P",
)
"""All 10 mechanism identifiers in canonical order."""

MECHANISM_DIM: int = 30
"""Output dimensionality per mechanism (C3 convention)."""

# Default random seed for reproducibility
_DEFAULT_SEED: int = 42


# ======================================================================
# Mel spectrogram generator
# ======================================================================

def generate_mel(
    B: int,
    T: int,
    n_mels: int = 128,
    seed: int = _DEFAULT_SEED,
) -> Tensor:
    """Generate a synthetic mel spectrogram tensor.

    Produces a random tensor mimicking log1p-normalised mel output from
    the Cochlea stage. Values are uniformly distributed in [0, 1].

    Args:
        B:      Batch size.
        T:      Number of time frames.
        n_mels: Number of mel frequency bins (default 128).
        seed:   Random seed for reproducibility.

    Returns:
        Tensor of shape ``(B, n_mels, T)`` with values in ``[0, 1]``.
    """
    gen = torch.Generator().manual_seed(seed)
    return torch.rand(B, n_mels, T, generator=gen)


# ======================================================================
# R3 spectral feature generators
# ======================================================================

def generate_r3(
    B: int,
    T: int,
    D: int = 128,
    seed: int = _DEFAULT_SEED,
) -> Tensor:
    """Generate a synthetic R3 spectral feature tensor (v2, 128D).

    Produces a random tensor mimicking normalised R3 output from the
    11-group spectral extraction pipeline.

    Args:
        B:    Batch size.
        T:    Number of time frames.
        D:    Feature dimensionality (default 128).
        seed: Random seed for reproducibility.

    Returns:
        Tensor of shape ``(B, T, D)`` with values in ``[0, 1]``.
    """
    gen = torch.Generator().manual_seed(seed)
    return torch.rand(B, T, D, generator=gen)


def generate_r3_v1(
    B: int,
    T: int,
    seed: int = _DEFAULT_SEED,
) -> Tensor:
    """Generate a synthetic R3 v1 spectral feature tensor (49D).

    Produces a random tensor mimicking the legacy 49-dimensional R3 space
    used by Brain models. The 49 features correspond to the original 5
    semantic groups: Consonance[0:7], Energy[7:12], Timbre[12:21],
    Change[21:25], Interactions[25:49].

    Args:
        B:    Batch size.
        T:    Number of time frames.
        seed: Random seed for reproducibility.

    Returns:
        Tensor of shape ``(B, T, 49)`` with values in ``[0, 1]``.
    """
    return generate_r3(B, T, D=_N_R3_V1, seed=seed)


# ======================================================================
# H3 temporal feature generator
# ======================================================================

def generate_h3_features(
    B: int,
    T: int,
    demand_set: Set[Tuple[int, int, int, int]],
    seed: int = _DEFAULT_SEED,
) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Generate synthetic H3 temporal features for a given demand set.

    Produces a sparse dictionary of random (B, T) tensors, one per demanded
    4-tuple. This bypasses the actual H3 extraction pipeline and is useful
    for testing Brain components in isolation.

    Args:
        B:          Batch size.
        T:          Number of time frames.
        demand_set: Set of ``(r3_idx, horizon, morph, law)`` 4-tuples
                    specifying which features to generate.
        seed:       Random seed for reproducibility.

    Returns:
        Dict mapping each 4-tuple to a ``(B, T)`` tensor in ``[0, 1]``.
    """
    gen = torch.Generator().manual_seed(seed)
    features: Dict[Tuple[int, int, int, int], Tensor] = {}
    for key in sorted(demand_set):
        features[key] = torch.rand(B, T, generator=gen)
    return features


# ======================================================================
# Minimal demand set generator
# ======================================================================

def generate_minimal_demand(
    n: int = 50,
    seed: int = _DEFAULT_SEED,
) -> Set[Tuple[int, int, int, int]]:
    """Generate a minimal set of random H3 demand 4-tuples.

    Samples ``n`` unique 4-tuples from the theoretical H3 address space
    (49 R3 indices x 32 horizons x 24 morphs x 3 laws). Uses the v1 R3
    index range (0-48) for compatibility with Brain models.

    The sampling strategy ensures coverage across:
    - Multiple R3 feature groups (Consonance, Energy, Timbre, Change, Interactions)
    - Multiple horizon bands (micro, meso, macro)
    - Multiple morph categories (Level, Dispersion, Shape, Dynamics, Rhythm)
    - All three temporal laws (memory, prediction, integration)

    Args:
        n:    Number of demand tuples to generate (default 50).
        seed: Random seed for reproducibility.

    Returns:
        Set of ``n`` unique ``(r3_idx, horizon, morph, law)`` 4-tuples.
    """
    rng = random.Random(seed)
    demand: Set[Tuple[int, int, int, int]] = set()

    # Ensure at least one tuple from each law
    for law in range(_N_LAWS):
        r3_idx = rng.randint(0, _N_R3_V1 - 1)
        horizon = rng.randint(0, _N_HORIZONS - 1)
        morph = rng.randint(0, _N_MORPHS - 1)
        demand.add((r3_idx, horizon, morph, law))

    # Fill remaining with random samples
    while len(demand) < n:
        r3_idx = rng.randint(0, _N_R3_V1 - 1)
        horizon = rng.randint(0, _N_HORIZONS - 1)
        morph = rng.randint(0, _N_MORPHS - 1)
        law = rng.randint(0, _N_LAWS - 1)
        demand.add((r3_idx, horizon, morph, law))

    return demand


# ======================================================================
# Mechanism output generator
# ======================================================================

def generate_mechanism_outputs(
    B: int,
    T: int,
    seed: int = _DEFAULT_SEED,
) -> Dict[str, Tensor]:
    """Generate synthetic mechanism output tensors for all 10 mechanisms.

    Produces a dictionary mapping each mechanism name to a random
    ``(B, T, 30)`` tensor, mimicking the cached output of
    ``MechanismRunner.run()``.

    The 10 mechanisms are:
        PPC (Pre-attentive Pitch Computation)
        TPC (Tonal Pitch Computation)
        BEP (Beat Entrainment Processing)
        ASA (Auditory Scene Analysis)
        TMH (Temporal Memory Hierarchy)
        MEM (Memory Encoding Mechanism)
        SYN (Synaptic Neuroplasticity)
        AED (Affective Evaluation of Dynamics)
        CPD (Contrastive Prediction Dynamics)
        C0P (Cortical Oscillatory Processing)

    Args:
        B:    Batch size.
        T:    Number of time frames.
        seed: Random seed for reproducibility.

    Returns:
        Dict mapping mechanism name to ``(B, T, 30)`` tensor in ``[0, 1]``.
    """
    gen = torch.Generator().manual_seed(seed)
    outputs: Dict[str, Tensor] = {}
    for name in MECHANISM_NAMES:
        outputs[name] = torch.rand(B, T, MECHANISM_DIM, generator=gen)
    return outputs
