"""TPRD T-Layer -- Tonotopic-Pitch Extraction (3D).

Non-standard first layer: T (Tonotopic) instead of E (Extraction).
Three features modeling tonotopic vs pitch representation dissociation:

  T0: tonotopic_encoding       -- Tonotopic encoding strength (primary HG) [0, 1]
  T1: pitch_representation     -- Pitch representation strength (nonprimary HG) [0, 1]
  T2: dissociation_degree      -- Tonotopy-pitch representation divergence [0, 1]

H3 consumed:
    (0, 10, 0, 2)   roughness value H10 L2              -- current tonotopic beating (400ms)
    (5, 10, 0, 2)   inharmonicity value H10 L2          -- tonotopy-pitch conflict (400ms)
    (3, 0, 0, 2)    stumpf_fusion value H0 L2           -- immediate pitch fusion (5.8ms)
    (3, 3, 1, 2)    stumpf_fusion mean H3 L2            -- brainstem pitch fusion (23.2ms)
    (14, 0, 0, 2)   tonalness value H0 L2               -- immediate pitch salience (5.8ms)
    (14, 3, 1, 2)   tonalness mean H3 L2                -- brainstem pitch salience (23.2ms)
    (17, 3, 14, 2)  spectral_autocorrelation period H3 L2 -- harmonic periodicity (23.2ms)
    (10, 10, 0, 2)  loudness value H10 L2               -- attention weight (400ms)
    (6, 10, 0, 2)   harmonic_deviation value H10 L2     -- harmonic template mismatch (400ms)

R3 consumed:
    [0]   roughness                -- T0: tonotopic beating proxy
    [1]   sethares_dissonance      -- T2: spectral dissonance (tonotopic quality)
    [3]   stumpf_fusion            -- T1: pitch fusion quality
    [4]   sensory_pleasantness     -- T1+T2: consonance integration
    [5]   inharmonicity            -- T2: tonotopy-pitch conflict signal
    [6]   harmonic_deviation       -- T2: harmonic template error
    [7]   amplitude                -- T0: overall signal energy
    [10]  loudness                 -- T0: attention weighting
    [14]  tonalness                -- T0+T1: pitch clarity / F0 salience
    [17]  spectral_autocorrelation -- T1: harmonic periodicity for pitch extraction
    [22]  entropy                  -- T0: spectral complexity (tonotopic map load)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/tprd/TPRD-extraction.md
Briley 2013: medial HG tonotopic, anterolateral HG pitch chroma.
Norman-Haignere 2013: pitch regions respond to resolved harmonics.
Basinski 2025: inharmonicity drives P3a (representational conflict).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_VAL_400MS = (0, 10, 0, 2)
_INHARM_VAL_400MS = (5, 10, 0, 2)
_FUSION_VAL_COCHLEAR = (3, 0, 0, 2)
_FUSION_MEAN_BRAINSTEM = (3, 3, 1, 2)
_TONAL_VAL_COCHLEAR = (14, 0, 0, 2)
_TONAL_MEAN_BRAINSTEM = (14, 3, 1, 2)
_SPEC_AUTOCORR_PERIOD_BRAINSTEM = (17, 3, 14, 2)
_LOUDNESS_VAL_400MS = (10, 10, 0, 2)
_HARM_DEV_VAL_400MS = (6, 10, 0, 2)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_SETHARES = 1
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_INHARMONICITY = 5
_HARMONIC_DEV = 6
_AMPLITUDE = 7
_LOUDNESS = 10
_TONALNESS = 14
_SPECTRAL_AUTOCORR = 17
_ENTROPY = 22


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
) -> Tuple[Tensor, Tensor, Tensor]:
    """T-layer: 3D tonotopic-pitch extraction from H3 + R3 features.

    T0 (tonotopic_encoding) captures frequency-map processing strength
    in primary Heschl's gyrus. High roughness with low tonalness
    indicates spectral (not pitch) encoding dominance, plus entropy
    weighted by amplitude reflects spectral complexity under energy.

    T1 (pitch_representation) captures F0 extraction strength in
    nonprimary (anterolateral) HG. Pitch salience averaged across
    cochlear and brainstem horizons, combined with tonalness weighted
    by spectral autocorrelation (harmonic periodicity).

    T2 (dissociation_degree) quantifies the divergence between
    tonotopic and pitch representations. Uses the absolute difference
    between T0 and T1, inharmonicity (non-integer partials), and
    prediction error from harmonic template mismatch.

    Briley 2013: medial HG tonotopic, anterolateral HG pitch chroma
    F(1,28)=29.865, p<0.001; dipole difference L p=0.024, R p=0.047.
    Norman-Haignere 2013: pitch regions respond to resolved harmonics.
    Basinski 2025: inharmonic sounds generate stronger P3a (p=0.010).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.

    Returns:
        ``(T0, T1, T2)`` each ``(B, T)``.
    """
    # -- R3 slices -------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]             # (B, T)
    inharmonicity = r3_features[..., _INHARMONICITY]     # (B, T)
    amplitude = r3_features[..., _AMPLITUDE]             # (B, T)
    tonalness = r3_features[..., _TONALNESS]             # (B, T)
    spectral_autocorr = r3_features[..., _SPECTRAL_AUTOCORR]  # (B, T)
    entropy = r3_features[..., _ENTROPY]                 # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    inharm_val = h3_features[_INHARM_VAL_400MS]                   # (B, T)
    tonal_cochlear = h3_features[_TONAL_VAL_COCHLEAR]             # (B, T)
    tonal_brainstem = h3_features[_TONAL_MEAN_BRAINSTEM]          # (B, T)
    spec_autocorr_period = h3_features[_SPEC_AUTOCORR_PERIOD_BRAINSTEM]  # (B, T)
    harm_dev_val = h3_features[_HARM_DEV_VAL_400MS]               # (B, T)

    # -- Derived intermediates -------------------------------------------------
    # Pitch salience: average of cochlear and brainstem tonalness
    pitch_sal = 0.50 * tonal_cochlear + 0.50 * tonal_brainstem  # (B, T)

    # Prediction error proxy: harmonic deviation as template mismatch
    pred_error = harm_dev_val  # (B, T)

    # T0: Tonotopic encoding -- primary HG frequency-map processing
    # f31 = sigma(0.35*roughness*(1-tonalness) + 0.35*entropy*amplitude)
    # Briley 2013: pure-tone responses centered on medial HG.
    # Fishman 2001: phase-locked oscillatory activity in A1/HG.
    t0 = torch.sigmoid(
        0.35 * roughness * (1.0 - tonalness)
        + 0.35 * entropy * amplitude
    )

    # T1: Pitch representation -- nonprimary (anterolateral) HG F0 extraction
    # f32 = sigma(0.40*pitch_sal.mean() + 0.30*tonalness*spectral_autocorr)
    # Briley 2013: pitch chroma F(1,28)=29.865, p<0.001 in anterolateral HG.
    # Norman-Haignere 2013: pitch regions driven by resolved harmonics.
    t1 = torch.sigmoid(
        0.40 * pitch_sal
        + 0.30 * tonalness * spectral_autocorr
    )

    # T2: Dissociation degree -- tonotopy-pitch divergence
    # f33 = sigma(0.30*|f31-f32| + 0.25*inharmonicity + 0.25*pred_error.mean())
    # Basinski 2025: inharmonicity drives P3a (p=0.010, N=30).
    t2 = torch.sigmoid(
        0.30 * (t0 - t1).abs()
        + 0.25 * inharmonicity
        + 0.25 * pred_error
    )

    return t0, t1, t2
