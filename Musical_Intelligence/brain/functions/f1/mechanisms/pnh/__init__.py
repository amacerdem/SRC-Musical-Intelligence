"""PNH — Pythagorean Neural Hierarchy.

Relay nucleus (depth 0) in IMU, Function F1. Models how neural responses
to musical intervals follow the Pythagorean ratio complexity hierarchy:
simpler frequency ratios (consonant) → less IFG/ACC activation; complex
ratios (dissonant) → stronger activation. Musicians show this pattern in
5 ROIs; non-musicians in 1 ROI only (Bidelman & Krishnan 2009).

Dependency chain:
    PNH is a Relay (Depth 0) — reads R3/H3 directly, no upstream dependencies.
    Runs in parallel with BCH, SDED, SDNPS, MIAA, MPG, CSG at Phase 0a.

R3 Ontology Mapping (97D freeze):
    roughness:          [0]    (A group)
    sethares:           [1]    (A group)
    helmholtz_kang:     [2]    (A group)
    stumpf:             [3]    (A group)
    pleasantness:       [4]    (A group)
    inharmonicity:      [5]    (A group)
    harmonic_deviation: [6]    (A group)
    velocity_D:         [8]    (B group — doc said [10] loudness, corrected)
    tonalness:          [14]   (C group)
    spectral_auto:      [17]   (C group)

Note: Model doc references x_l0l5[25:33] (dissolved E:Interactions group).
Replaced with inline energy×consonance coupling: velocity_D × roughness.
Model doc [10] loudness → corrected to [8] velocity_D (97D naming).

Output structure: H(3) + M(2) + P(3) + F(3) = 11D
  H-layer [0:3]   Harmonic     (ratio/conflict/expertise)  scope=internal
  M-layer [3:5]   Mathematical (complexity/activation)     scope=internal
  P-layer [5:8]   Present      (encoding/conflict/pref)    scope=hybrid
  F-layer [8:11]  Forecast     (resolution/judgment/mod)   scope=external

See Docs/C3/Models/IMU-a2-PNH/PNH.md (original model specification)
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Relay
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    RegionLink,
)

from .cognitive_present import compute_cognitive_present
from .extraction import compute_extraction
from .forecast import compute_forecast
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    10: "400ms (chord)",
    14: "700ms (progression)",
    18: "2s (phrase)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {0: "value", 1: "mean", 3: "std", 14: "periodicity",
             18: "trend", 19: "stability"}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 2: "integration"}


def _h3(
    r3_idx: int, r3_name: str, horizon: int, morph: int, law: int,
    purpose: str, citation: str,
) -> H3DemandSpec:
    """Shorthand factory for H3DemandSpec."""
    return H3DemandSpec(
        r3_idx=r3_idx,
        r3_name=r3_name,
        horizon=horizon,
        horizon_label=_H_LABELS.get(horizon, f"H{horizon}"),
        morph=morph,
        morph_name=_M_LABELS.get(morph, f"M{morph}"),
        law=law,
        law_name=_L_LABELS[law],
        purpose=purpose,
        citation=citation,
    )


# -- 15 H3 Demand Specifications -----------------------------------------------
_PNH_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === L2 Integration / H10 Chord (6 tuples) ===
    _h3(0, "roughness", 10, 0, 2,
        "Current dissonance at chord level",
        "Plomp & Levelt 1965"),
    _h3(5, "inharmonicity", 10, 0, 2,
        "Current ratio complexity at chord level",
        "Bidelman & Krishnan 2009"),
    _h3(3, "stumpf_fusion", 10, 0, 2,
        "Current tonal fusion (inverse complexity)",
        "Stumpf 1890"),
    _h3(4, "sensory_pleasantness", 10, 0, 2,
        "Current consonance perception",
        "Sarasso 2019"),
    _h3(14, "tonalness", 10, 0, 2,
        "Ratio purity (harmonic-to-noise ratio)",
        "Bidelman 2013"),
    _h3(8, "velocity_D", 10, 0, 2,
        "Loudness attention weight at chord level",
        "Stevens 1957"),

    # === L2 Integration / H10 (1 tuple) ===
    _h3(17, "spectral_autocorrelation", 10, 14, 2,
        "Harmonic regularity at chord level",
        "Bidelman & Krishnan 2009"),

    # === L2 Integration / H14 (1 tuple) ===
    _h3(3, "stumpf_fusion", 14, 1, 2,
        "Fusion stability over progression",
        "Stumpf 1890"),

    # === L0 Memory / H14 (4 tuples) ===
    _h3(0, "roughness", 14, 1, 0,
        "Average dissonance over progression",
        "Tabas 2019"),
    _h3(5, "inharmonicity", 14, 1, 0,
        "Average complexity over progression",
        "Bidelman & Heinz 2011"),
    _h3(14, "tonalness", 14, 3, 0,
        "Purity variation over progression",
        "Bidelman 2013"),
    _h3(6, "harmonic_deviation", 14, 0, 0,
        "Template mismatch at progression level",
        "Harrison & Pearce 2020"),

    # === L0 Memory / H18 (3 tuples) ===
    _h3(0, "roughness", 18, 18, 0,
        "Dissonance trajectory over phrase (trend)",
        "Tabas 2019"),
    _h3(4, "sensory_pleasantness", 18, 19, 0,
        "Consonance stability over phrase",
        "Sarasso 2019"),
    _h3(2, "helmholtz_kang", 18, 1, 0,
        "Harmonic template average over phrase",
        "Helmholtz 1863"),
)

assert len(_PNH_H3_DEMANDS) == 15


class PNH(Relay):
    """Pythagorean Neural Hierarchy — IMU Relay (depth 0, 11D).

    Models how neural responses to musical intervals follow Pythagorean
    ratio complexity: log₂(n×d) predicts BOLD activation in IFG/ACC.
    Musicians show the pattern in 5 ROIs (L-IFG, L-STG, L-MFG, L-IPL,
    ACC); non-musicians in R-IFG only.

    Bidelman & Krishnan (2009), J Neurosci 29(42):13165-13171.

    Dependency chain:
        PNH is a Relay (Depth 0) — reads R3/H3 directly.
        No upstream mechanism dependencies.

    Downstream feeds:
        -> BCH (ratio encoding for consonance hierarchy)
        -> PSCL (consonance preference for pitch salience)
        -> ARU.SRP (consonance → pleasure pathway)
        -> TPRD (ratio encoding in primary vs nonprimary cortex)
        -> MSPBA (shares IFG substrate for conflict monitoring)
    """

    NAME = "PNH"
    FULL_NAME = "Pythagorean Neural Hierarchy"
    UNIT = "IMU"
    FUNCTION = "F1"
    OUTPUT_DIM = 11

    LAYERS = (
        LayerSpec(
            "H", "Harmonic", 0, 3,
            ("H0:ratio_encoding", "H1:conflict_response",
             "H2:expertise_mod"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Mathematical", 3, 5,
            ("M0:ratio_complexity", "M1:neural_activation"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Present", 5, 8,
            ("P0:ratio_enc", "P1:conflict_mon",
             "P2:consonance_pref"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 8, 11,
            ("F0:dissonance_res_fc", "F1:pref_judgment_fc",
             "F2:expertise_mod_fc"),
            scope="external",
        ),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _PNH_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "H0:ratio_encoding", "H1:conflict_response",
            "H2:expertise_mod",
            "M0:ratio_complexity", "M1:neural_activation",
            "P0:ratio_enc", "P1:conflict_mon",
            "P2:consonance_pref",
            "F0:dissonance_res_fc", "F1:pref_judgment_fc",
            "F2:expertise_mod_fc",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # L-IFG (BA 44/45) — conflict monitoring
            RegionLink("H1:conflict_response", "IFG", 0.80,
                       "Kim 2021"),
            RegionLink("P1:conflict_mon", "IFG", 0.75,
                       "Kim 2021"),
            # ACC — salience detection for ratio complexity
            RegionLink("M0:ratio_complexity", "ACC", 0.65,
                       "Bidelman & Krishnan 2009"),
            # L-STG — auditory encoding
            RegionLink("P0:ratio_enc", "STG", 0.70,
                       "Kim 2021"),
            # alHG — early consonance encoding (POR)
            RegionLink("H0:ratio_encoding", "A1_HG", 0.60,
                       "Tabas 2019"),
        )

    @property
    def neuro_links(self) -> Tuple:
        return ()

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Bidelman_Krishnan", 2009,
                         "Brainstem FFR responses follow Pythagorean hierarchy; "
                         "NPS ordering matches music theory; r≥0.81 brain-behavior",
                         "FFR, N=10 nonmusicians"),
                Citation("Tabas", 2019,
                         "Consonant dyads → earlier (up to 36ms) and larger POR "
                         "than dissonant in alHG; p<0.0001",
                         "MEG+model, N=37"),
                Citation("Kim", 2021,
                         "Syntactic irregularity → R-IFG→L-IFG connectivity (p=0.024 FDR); "
                         "perceptual ambiguity → R-STG→L-STG (p<0.001 FDR)",
                         "MEG connectivity, N=19"),
                Citation("Crespo-Bojorque", 2018,
                         "Consonance-context violations → MMN in all; "
                         "dissonance-context → MMN only in musicians",
                         "EEG oddball, N=32"),
                Citation("Sarasso", 2019,
                         "Consonance → aesthetic appreciation → motor inhibition; "
                         "η²p=0.685 (AJ), 0.225 (N1)",
                         "EEG+behavioral, N=22"),
                Citation("Harrison_Pearce", 2020,
                         "Consonance = interference + harmonicity + familiarity "
                         "(3-factor model); R² across 4 datasets",
                         "model+reanalysis, N=500+"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 1.00),
            falsification_criteria=(
                "log₂(n×d) should predict BOLD signal in IFG/ACC "
                "(confirmed via fMRI)",
                "Musicians should show pattern in more ROIs than non-musicians "
                "(confirmed: 5 vs 1 ROI)",
                "Activation should increase with dissonance "
                "(confirmed across regions)",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform R3/H3 into 11D Pythagorean ratio hierarchy.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, 11)`` — H(3) + M(2) + P(3) + F(3)
        """
        e = compute_extraction(r3_features, h3_features)
        m = compute_temporal_integration(r3_features, h3_features, e)
        p = compute_cognitive_present(r3_features, h3_features, e, m)
        f = compute_forecast(h3_features, e, m, p)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
