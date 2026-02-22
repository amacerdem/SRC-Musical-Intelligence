"""MSPBA S-Layer -- Extraction (3D).

Syntactic processing signals from H3/R3 features modelling musical syntax
in Broca's area (IFG BA 44/45):

  S0: musical_syntax      -- mERAN response strength [0, 1]
  S1: harmonic_prediction -- Harmonic prediction strength (BA 45) [0, 1]
  S2: broca_activation    -- Domain-general Broca's activation [0, 1]

S0 tracks the mERAN (music-specific early right anterior negativity) --
the neural signature of harmonic syntax violation. Prediction error x
energy-consonance coupling (x_l0l5) x roughness. Maess et al. 2001:
mERAN localized in BA 44 (p=0.005, MEG, N=28).

S1 measures harmonic expectation strength from accumulated context.
Harmony context x regularity (1-entropy) x tonal fusion (stumpf).
Patel 2003: SSIRH shared syntactic resources.

S2 captures domain-general syntactic processing load in Broca's area.
Structural expectation x familiarity proxy x consonance.
Tachibana et al. 2024: bilateral BA 45 for musical syntax (fNIRS, N=20).

H3 consumed:
    (0, 10, 0, 2)   roughness value H10 L2          -- current dissonance
    (0, 14, 1, 0)   roughness mean H14 L0           -- average dissonance
    (1, 10, 0, 2)   sethares_dissonance value H10 L2 -- beating dissonance
    (1, 14, 8, 0)   sethares_dissonance velocity H14 L0 -- dissonance change
    (3, 10, 0, 2)   stumpf_fusion value H10 L2      -- tonal fusion
    (3, 14, 1, 2)   stumpf_fusion mean H14 L2       -- fusion stability
    (5, 10, 0, 2)   inharmonicity value H10 L2      -- harmonic deviation
    (22, 10, 0, 2)  entropy value H10 L2            -- harmonic unpredictability
    (10, 10, 0, 2)  loudness value H10 L2           -- attention gating
    (11, 10, 0, 2)  onset_strength value H10 L2     -- chord onset detection

R3 consumed:
    [0]      roughness
    [1]      sethares_dissonance
    [2]      helmholtz_kang
    [3]      stumpf_fusion
    [4]      sensory_pleasantness
    [5]      inharmonicity
    [6]      harmonic_deviation
    [10]     loudness
    [11]     onset_strength
    [22]     entropy
    [23]     spectral_flux
    [25:33]  x_l0l5
    [33:41]  x_l4l5
    [41:49]  x_l5l7

Relay consumed:
    PNH.ratio_encoding (P0 index 5 from PNH 11D output)

See Building/C3-Brain/F4-Memory-Systems/mechanisms/mspba/MSPBA-extraction.md
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

# -- H3 tuples ----------------------------------------------------------------
_ROUGHNESS_VAL_H10 = (0, 10, 0, 2)       # roughness value H10 L2
_ROUGHNESS_MEAN_H14 = (0, 14, 1, 0)      # roughness mean H14 L0
_SETHARES_VAL_H10 = (1, 10, 0, 2)        # sethares_dissonance value H10 L2
_SETHARES_VEL_H14 = (1, 14, 8, 0)        # sethares_dissonance velocity H14 L0
_STUMPF_VAL_H10 = (3, 10, 0, 2)          # stumpf_fusion value H10 L2
_STUMPF_MEAN_H14 = (3, 14, 1, 2)         # stumpf_fusion mean H14 L2
_INHARM_VAL_H10 = (5, 10, 0, 2)          # inharmonicity value H10 L2
_ENTROPY_VAL_H10 = (22, 10, 0, 2)        # entropy value H10 L2
_LOUDNESS_VAL_H10 = (10, 10, 0, 2)       # loudness value H10 L2
_ONSET_VAL_H10 = (11, 10, 0, 2)          # onset_strength value H10 L2

# -- R3 feature indices (post-freeze 97D) -------------------------------------
_ROUGHNESS = 0
_SETHARES_DISSONANCE = 1
_HELMHOLTZ_KANG = 2
_STUMPF_FUSION = 3
_SENSORY_PLEASANTNESS = 4
_INHARMONICITY = 5
_HARMONIC_DEVIATION = 6
_LOUDNESS = 10
_ONSET_STRENGTH = 11
_ENTROPY = 22
_SPECTRAL_FLUX = 23
_X_L0L5_START = 25
_X_L0L5_END = 33
_X_L4L5_START = 33
_X_L4L5_END = 41
_X_L5L7_START = 41
_X_L5L7_END = 49

# -- Upstream relay index ------------------------------------------------------
_PNH_RATIO_ENCODING = 5  # PNH P0:ratio_encoding (index 5 in PNH 11D output)


def compute_extraction(
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    relay_outputs: Dict[str, Tensor],
) -> Tuple[Tensor, Tensor, Tensor]:
    """S-layer: 3D syntactic processing extraction from H3/R3 + relay.

    S0 (musical_syntax) reflects the mERAN response -- prediction error
    x coupling disruption (x_l0l5) x roughness. All three factors must
    co-occur for a strong mERAN signal.
    Maess et al. 2001: mERAN in BA 44 (MEG, N=28, p=0.005).

    S1 (harmonic_prediction) reflects harmonic expectation strength from
    accumulated context. Harmony context x regularity (1-entropy) x tonal
    fusion. Position 5 violation produces 2x mERAN vs position 3.
    Patel 2003: SSIRH shared syntactic resources.

    S2 (broca_activation) reflects domain-general syntactic processing load.
    Structural expectation x familiarity x consonance.
    Tachibana et al. 2024: bilateral BA 45 activation (fNIRS, N=20).

    Args:
        h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        r3_features: ``(B, T, 97)`` R3 feature tensor.
        relay_outputs: ``{"PNH": (B, T, 11)}``

    Returns:
        ``(S0, S1, S2)`` each ``(B, T)``.
    """
    # -- H3 features -------------------------------------------------------------
    roughness_val = h3_features[_ROUGHNESS_VAL_H10]          # (B, T)
    roughness_mean = h3_features[_ROUGHNESS_MEAN_H14]        # (B, T)
    sethares_val = h3_features[_SETHARES_VAL_H10]            # (B, T)
    stumpf_val = h3_features[_STUMPF_VAL_H10]                # (B, T)
    stumpf_mean = h3_features[_STUMPF_MEAN_H14]              # (B, T)
    inharm_val = h3_features[_INHARM_VAL_H10]                # (B, T)
    entropy_val = h3_features[_ENTROPY_VAL_H10]              # (B, T)
    loudness_val = h3_features[_LOUDNESS_VAL_H10]            # (B, T)
    onset_val = h3_features[_ONSET_VAL_H10]                  # (B, T)

    # -- R3 slices ---------------------------------------------------------------
    roughness = r3_features[..., _ROUGHNESS]                 # (B, T)
    helmholtz = r3_features[..., _HELMHOLTZ_KANG]            # (B, T)
    stumpf = r3_features[..., _STUMPF_FUSION]                # (B, T)
    pleasantness = r3_features[..., _SENSORY_PLEASANTNESS]   # (B, T)
    entropy = r3_features[..., _ENTROPY]                     # (B, T)
    x_l0l5 = r3_features[..., _X_L0L5_START:_X_L0L5_END]   # (B, T, 8)
    x_l4l5 = r3_features[..., _X_L4L5_START:_X_L4L5_END]   # (B, T, 8)
    x_l5l7 = r3_features[..., _X_L5L7_START:_X_L5L7_END]   # (B, T, 8)

    # -- Upstream relay: PNH ratio encoding --------------------------------------
    pnh = relay_outputs["PNH"]                               # (B, T, 11)
    ratio_encoding = pnh[..., _PNH_RATIO_ENCODING]           # (B, T)

    # -- Derived signals ---------------------------------------------------------
    # Prediction error proxy: roughness x entropy x onset gating
    pred_error = roughness_val * entropy_val * onset_val     # (B, T)
    # Coupling disruption: mean of pitch-dissonance interactions
    coupling_mean = x_l0l5.mean(dim=-1)                      # (B, T)
    # Temporal violation: mean of temporal interaction features
    temporal_viol = x_l4l5.mean(dim=-1)                      # (B, T)
    # Harmonic structure: mean of harmonic structure features
    harmonic_struct = x_l5l7.mean(dim=-1)                    # (B, T)
    # Harmony context: accumulated tonal context from ratio encoding + fusion
    harmony = 0.50 * ratio_encoding + 0.50 * stumpf_mean    # (B, T)
    # Structural expectation proxy: consonance stability
    struct_expect = pleasantness * stumpf_val                # (B, T)
    # Familiarity proxy: tonal regularity (inverse entropy)
    familiarity = 1.0 - entropy                              # (B, T)

    # -- S0: Musical Syntax (mERAN response strength) ----------------------------
    # f25 = sigma(0.35 * pred_error.mean * x_l0l5.mean * roughness)
    # Violation + coupling disruption + dissonance = mERAN
    # Maess et al. 2001: mERAN localized in BA 44 (p=0.005, MEG, N=28)
    s0 = torch.sigmoid(
        0.35 * pred_error * coupling_mean * roughness
    )

    # -- S1: Harmonic Prediction (BA 45 context accumulation) --------------------
    # f26 = sigma(0.30 * harmony.mean * (1-entropy) * stumpf_fusion)
    # Context + regularity + fusion = expectation
    # Patel 2003: SSIRH shared syntactic resources
    s1 = torch.sigmoid(
        0.30 * harmony * familiarity * stumpf
    )

    # -- S2: Broca's Activation (domain-general syntactic load) ------------------
    # f27 = sigma(0.35 * struct_expect.mean * familiarity.mean * (1-sethares))
    # Tachibana et al. 2024: bilateral BA 45 for musical syntax (fNIRS, N=20)
    sethares = r3_features[..., _SETHARES_DISSONANCE]        # (B, T)
    s2 = torch.sigmoid(
        0.35 * struct_expect * familiarity * (1.0 - sethares)
    )

    return s0, s1, s2
