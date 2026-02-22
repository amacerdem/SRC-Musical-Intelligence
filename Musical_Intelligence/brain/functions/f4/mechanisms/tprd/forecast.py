"""TPRD F-Layer -- Forecast (3D).

Three forward predictions for pitch percept, tonotopic adaptation,
and dissociation evolution:

  F0: pitch_percept_fc      -- Pitch percept prediction (50-200ms ahead) [0, 1]
  F1: tonotopic_adpt_fc     -- Tonotopic adaptation prediction (200-700ms) [0, 1]
  F2: dissociation_fc       -- Dissociation evolution forecast (0.5-2s) [0, 1]

F0 leverages fast brainstem pitch extraction (H3, 23.2ms) to predict
whether pitch clarity will strengthen or weaken. F1 tracks tonotopic
map adaptation over harmonic progression timescales (H14, 700ms).
F2 projects tonotopy-pitch divergence at phrase level (H18, 2s).

H3 consumed:
    (4, 18, 19, 0)  sensory_pleasantness stability H18 L0 -- consonance stability (phrase)
    (7, 6, 8, 0)    amplitude velocity H6 L0              -- energy change rate (beat)
    (0, 14, 1, 0)   roughness mean H14 L0                 -- avg tonotopic load (700ms)
    (5, 14, 1, 0)   inharmonicity mean H14 L0             -- avg conflict (700ms)
    (14, 6, 1, 0)   tonalness mean H6 L0                  -- beat-level pitch clarity
    (17, 6, 14, 0)  spectral_autocorrelation period H6 L0 -- beat-level harmonic periodicity
    (22, 6, 0, 0)   entropy value H6 L0                   -- spectral complexity (beat)
    (22, 14, 1, 0)  entropy mean H14 L0                   -- avg complexity (700ms)

R3 consumed:
    [0]   roughness                -- F1: tonotopic trajectory
    [5]   inharmonicity            -- F2: conflict trajectory
    [14]  tonalness                -- F0: pitch clarity trajectory
    [17]  spectral_autocorrelation -- F0: harmonic periodicity trajectory
    [22]  entropy                  -- F1+F2: complexity trajectory

See Building/C3-Brain/F4-Memory-Systems/mechanisms/tprd/TPRD-forecast.md
Tabas 2019: POR latency 36ms difference for consonant vs dissonant (MEG, N=37).
Briley 2013: adaptation paradigm revealed tonotopic vs pitch gradient.
Cheung 2019: uncertainty-surprise interaction in auditory cortex (fMRI, N=39).
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_PLEAS_STAB_PHRASE = (4, 18, 19, 0)
_AMP_VEL_200MS = (7, 6, 8, 0)
_ROUGHNESS_MEAN_700MS = (0, 14, 1, 0)
_INHARM_MEAN_700MS = (5, 14, 1, 0)
_TONAL_MEAN_200MS = (14, 6, 1, 0)
_SPEC_AUTOCORR_PERIOD_200MS = (17, 6, 14, 0)
_ENTROPY_VAL_200MS = (22, 6, 0, 0)
_ENTROPY_MEAN_700MS = (22, 14, 1, 0)

# -- R3 indices ----------------------------------------------------------------
_ROUGHNESS = 0
_INHARMONICITY = 5
_TONALNESS = 14
_SPECTRAL_AUTOCORR = 17
_ENTROPY = 22


def compute_forecast(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    t: Tuple[Tensor, Tensor, Tensor],
    m: Tuple[Tensor, Tensor],
    p: Tuple[Tensor, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """F-layer: 3D forecast from T/M/P outputs + H3/R3 context.

    F0 (pitch_percept_fc) predicts pitch clarity 50-200ms ahead
    using brainstem-level pitch signals (tonalness, spectral
    autocorrelation) and pitch state (P1). Tabas 2019: consonant
    combinations decoded faster in anterolateral HG.

    F1 (tonotopic_adpt_fc) predicts tonotopic adaptation 200-700ms
    ahead using roughness trend (H14), amplitude velocity, and
    tonotopic state (P0). Briley 2013: adaptation paradigm revealed
    tonotopic organization.

    F2 (dissociation_fc) predicts dissociation evolution 0.5-2s
    ahead using phrase-level consonance stability (H18), conflict
    trajectory, and dissociation degree (T2). Cheung 2019:
    uncertainty-surprise interaction modulates auditory cortex.

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        t: ``(T0, T1, T2)`` from extraction layer.
        m: ``(M0, M1)`` from temporal integration layer.
        p: ``(P0, P1)`` from cognitive present layer.

    Returns:
        ``(F0, F1, F2)`` each ``(B, T)``.
    """
    _t0, _t1, t2 = t
    m0, _m1 = m
    p0, p1 = p

    # -- R3 slices -------------------------------------------------------------
    tonalness = r3_features[..., _TONALNESS]             # (B, T)
    entropy = r3_features[..., _ENTROPY]                 # (B, T)

    # -- H3 lookups ------------------------------------------------------------
    pleas_stab_phrase = h3_features[_PLEAS_STAB_PHRASE]         # (B, T)
    amp_vel_200ms = h3_features[_AMP_VEL_200MS]                 # (B, T)
    roughness_mean_700ms = h3_features[_ROUGHNESS_MEAN_700MS]   # (B, T)
    inharm_mean_700ms = h3_features[_INHARM_MEAN_700MS]         # (B, T)
    tonal_mean_200ms = h3_features[_TONAL_MEAN_200MS]           # (B, T)
    spec_autocorr_period = h3_features[_SPEC_AUTOCORR_PERIOD_200MS]  # (B, T)
    entropy_mean_700ms = h3_features[_ENTROPY_MEAN_700MS]       # (B, T)

    # -- F0: Pitch Percept Forecast (50-200ms ahead) ---------------------------
    # Predicts whether pitch clarity will strengthen or weaken.
    # Uses brainstem pitch signals (tonalness, spectral autocorrelation)
    # and current pitch state (P1).
    # Tabas 2019: POR latency up to 36ms for dissonant dyads.
    f0 = torch.sigmoid(
        0.30 * p1
        + 0.25 * tonal_mean_200ms
        + 0.25 * spec_autocorr_period
        + 0.20 * tonalness
    )

    # -- F1: Tonotopic Adaptation Forecast (200-700ms ahead) -------------------
    # Predicts tonotopic map adaptation as harmonic context evolves.
    # Uses roughness trend (H14), amplitude velocity (energy change),
    # and current tonotopic state (P0).
    # Briley 2013: adaptation paradigm revealed tonotopic organization.
    f1 = torch.sigmoid(
        0.30 * p0
        + 0.25 * roughness_mean_700ms
        + 0.25 * amp_vel_200ms
        + 0.20 * entropy
    )

    # -- F2: Dissociation Evolution Forecast (0.5-2s ahead) --------------------
    # Predicts how tonotopy-pitch divergence will evolve at phrase level.
    # Uses consonance stability (H18), conflict trajectory, and
    # current dissociation degree (T2).
    # Cheung 2019: uncertainty-surprise interaction in auditory cortex.
    f2 = torch.sigmoid(
        0.25 * t2
        + 0.25 * pleas_stab_phrase
        + 0.25 * inharm_mean_700ms
        + 0.25 * entropy_mean_700ms
    )

    return f0, f1, f2
