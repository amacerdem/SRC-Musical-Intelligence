"""CDEM C-Layer -- Extraction (2D).

Context-dependent emotional memory features:

  C0: context_modulation    -- Cross-modal context modulation [0, 1]
  C1: arousal_suppression   -- Context-dependent arousal suppression [0, 1]

Also exposes derived signals (encoding_strength, retrieval, familiar, arousal)
consumed by downstream M/P/F layers.

H3 consumed:
    (3, 16, 1, 2)   stumpf_fusion mean H16 L2        -- binding stability 1s
    (4, 16, 0, 2)   sensory_pleasantness value H16 L2 -- current mood
    (10, 16, 0, 2)  loudness value H16 L2             -- current arousal
    (0, 16, 0, 2)   roughness value H16 L2            -- current valence (inv)
    (21, 16, 0, 2)  spectral_flux value H16 L2        -- context change rate
    (22, 16, 0, 2)  entropy value H16 L2              -- context complexity
    (12, 16, 0, 2)  warmth value H16 L2               -- context warmth
    (11, 16, 0, 2)  onset_strength value H16 L2       -- event boundary
    (7, 16, 8, 0)   amplitude velocity H16 L0         -- energy change rate

R3 consumed:
    [0]      roughness              -- C0+C1: valence proxy (1 - roughness)
    [3]      stumpf_fusion          -- C0+C1: binding strength
    [4]      sensory_pleasantness   -- encoding quality
    [7]      amplitude              -- C1: arousal correlate
    [10]     loudness               -- C1: arousal proxy
    [11]     onset_strength         -- event salience / context boundary
    [12]     warmth                 -- context warmth
    [14]     tonalness              -- pattern clarity
    [21]     spectral_flux          -- C1: context change detection
    [22]     entropy                -- C1: context complexity
    [24]     spectral_concentration -- event salience
    [25:33]  x_l0l5                 -- C0: context-memory binding
    [41:49]  x_l5l7                 -- encoding quality signal

See Building/C3-Brain/F4-Memory-Systems/mechanisms/cdem/CDEM-extraction.md
Sachs 2025: same-valence context shifts brain-state transitions 6.26s earlier.
Mitterschiffthaler 2007: sad music -> R hippocampus/amygdala (N=16, Z=3.25).
"""
from __future__ import annotations

from typing import Dict, NamedTuple, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_STUMPF_MEAN_1S = (3, 16, 1, 2)
_PLEAS_VAL_1S = (4, 16, 0, 2)
_LOUD_VAL_1S = (10, 16, 0, 2)
_ROUGH_VAL_1S = (0, 16, 0, 2)
_FLUX_VAL_1S = (21, 16, 0, 2)
_ENTROPY_VAL_1S = (22, 16, 0, 2)
_WARMTH_VAL_1S = (12, 16, 0, 2)
_ONSET_VAL_1S = (11, 16, 0, 2)
_AMP_VEL_1S = (7, 16, 8, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_AMPLITUDE = 7
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_WARMTH = 12
_TONALNESS = 14
_SPECTRAL_FLUX = 21
_ENTROPY = 22
_SPECTRAL_CONCENTRATION = 24
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L5L7_START = 41
_X_L5L7_END = 49


class ExtractionResult(NamedTuple):
    """C-layer outputs plus derived signals for downstream layers."""

    c0: Tensor  # context_modulation   (B, T)
    c1: Tensor  # arousal_suppression  (B, T)
    # -- derived signals reused by M/P/F layers --
    encoding_strength: Tensor  # (B, T) -- hippocampal encoding signal
    retrieval: Tensor          # (B, T) -- binding-based retrieval proxy
    familiar: Tensor           # (B, T) -- familiarity proxy
    arousal: Tensor            # (B, T) -- arousal proxy


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> ExtractionResult:
    """C-layer: 2D extraction + derived signals from H3/R3 features.

    C0 (context_modulation): cross-modal context shapes memory encoding.
    Uses energy-consonance interaction (x_l0l5) as the context-memory
    binding signal, consonance times familiarity for mood-congruent
    encoding, and stumpf times retrieval for context-dependent retrieval.
    Sachs 2025: same-valence context transitions 6.26s earlier (fMRI, N=39).

    C1 (arousal_suppression): context dampens the arousal response.
    Uses arousal times loudness (raw arousal signal), entropy times
    inverse binding (contextual complexity), and flux times amplitude
    (context change rate).
    Mitterschiffthaler 2007: sad music -> R hippocampus/amygdala (N=16).

    Also computes encoding_strength (C2 from spec doc), retrieval,
    familiar, and arousal as derived signals consumed by M/P/F layers.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        :class:`ExtractionResult` with ``c0``, ``c1`` each ``(B, T)``
        plus derived signals.
    """
    # -- H3 features --
    stumpf_mean_1s = h3_features[_STUMPF_MEAN_1S]       # (B, T)
    pleas_val_1s = h3_features[_PLEAS_VAL_1S]            # (B, T)
    loud_val_1s = h3_features[_LOUD_VAL_1S]              # (B, T)
    rough_val_1s = h3_features[_ROUGH_VAL_1S]            # (B, T)
    flux_val_1s = h3_features[_FLUX_VAL_1S]              # (B, T)
    entropy_val_1s = h3_features[_ENTROPY_VAL_1S]        # (B, T)
    warmth_val_1s = h3_features[_WARMTH_VAL_1S]          # (B, T)
    onset_val_1s = h3_features[_ONSET_VAL_1S]            # (B, T)
    amp_vel_1s = h3_features[_AMP_VEL_1S]                # (B, T)

    # -- R3 features --
    roughness = r3_features[..., _ROUGHNESS]              # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]             # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]              # (B, T)
    loudness = r3_features[..., _LOUDNESS]                # (B, T)
    warmth = r3_features[..., _WARMTH]                    # (B, T)
    flux = r3_features[..., _SPECTRAL_FLUX]               # (B, T)
    entropy = r3_features[..., _ENTROPY]                  # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]  # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]  # (B, T, 8)

    # -- Derived signals (shared across layers) --
    # Retrieval: binding stability proxy from H3 stumpf + R3 stumpf
    retrieval = 0.50 * stumpf_mean_1s + 0.50 * stumpf

    # Familiarity: warmth-based familiarity proxy (warm = familiar)
    familiar = torch.sigmoid(warmth_val_1s * warmth)

    # Arousal: loudness-based arousal signal
    arousal = torch.sigmoid(loud_val_1s * loudness)

    # Encoding strength (doc C2): hippocampal + mPFC consolidation
    # Cheung 2019: uncertainty x surprise -> amygdala/hippocampus
    encoding_strength = torch.sigmoid(
        0.40 * arousal * x_l5l7.mean(dim=-1)
        + 0.30 * (1.0 - roughness) * warmth
        + 0.30 * pleas_val_1s * stumpf
    )

    # Expectancy: prediction-related signal for context binding
    expectancy = torch.sigmoid(onset_val_1s * pleas_val_1s)

    # -- C0: Context Modulation --
    # Hippocampus + ACC multi-modal binding
    # Sachs 2025: tempoparietal brain-state transitions track emotion
    c0 = torch.sigmoid(
        0.35 * x_l0l5.mean(dim=-1) * encoding_strength
        + 0.35 * (1.0 - roughness) * familiar
        + 0.30 * stumpf * retrieval
    )

    # -- C1: Arousal Suppression --
    # Amygdala arousal gated by context
    # Mitterschiffthaler 2007: sad music -> R hippocampus/amygdala
    c1 = torch.sigmoid(
        0.40 * arousal * loudness
        + 0.30 * entropy * (1.0 - stumpf)
        + 0.30 * flux * amplitude
    )

    return ExtractionResult(
        c0=c0,
        c1=c1,
        encoding_strength=encoding_strength,
        retrieval=retrieval,
        familiar=familiar,
        arousal=arousal,
    )
