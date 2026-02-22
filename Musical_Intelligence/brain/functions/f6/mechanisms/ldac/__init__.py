"""LDAC -- Liking-Dependent Auditory Cortex.

Associator nucleus (depth 2) in RPU, Function F6. Models how moment-to-moment
liking continuously modulates auditory cortex (R STG) processing. High IC
combined with disliking produces the lowest STG activation (maximal sensory
suppression). Pleasure gates sensory gain via top-down reward-to-perception
pathway.

Core finding: R STG continuously covaries with normalized moment-to-moment
liking (t(23)=2.56, p=0.018). IC x liking interaction in R STG
(t(23)=2.92, p=0.008). STG-NAcc functional connectivity modulated by
musical reward sensitivity. Fastest tau_decay (0.5s).

Reads: IUCP (intra-unit), RPEM (intra-unit), DAED (intra-unit/cross)
IUCP and RPEM are F6 RPU mechanisms; DAED is also F6 RPU.

R3 Ontology Mapping (post-freeze 97D):
    sensory_pleasantness:   [4]      (A, hedonic quality)
    loudness:               [8]      (B, velocity_D / sensory salience)
    spectral_flux:          [10]     (B, onset_strength / deviation detection)
    spectral_change:        [21]     (D, IC / surprise level)
    x_l0l5:                 [25:33]  (F, auditory gating proxy)

Output structure: E(4) + P(1) + F(1) = 6D
  E-layer [0:4]   Extraction           (sigmoid)  scope=internal
  P-layer [4:5]   Cognitive Present    (sigmoid)  scope=hybrid
  F-layer [5:6]   Forecast             (sigmoid)  scope=external

No M-layer (temporal integration). P and F reuse E-layer outputs directly.

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/ldac/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Associator
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    NeuroLink,
    RegionLink,
)

from .cognitive_present import compute_cognitive_present
from .extraction import compute_extraction
from .forecast import compute_forecast

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    2: "75ms (gamma)",
    3: "100ms (gamma)",
    8: "500ms (theta)",
    16: "1s (delta)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 20: "entropy",
}

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


# -- R3 feature indices (post-freeze 97D) ------------------------------------
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_SPECTRAL_FLUX = 10
_SPECTRAL_CHANGE = 21
_X_L0L5_START = 25


# -- 12 H3 Demand Specifications (all E-layer) --------------------------------
# LDAC operates on fast hedonic tracking (100ms) through slower integration (1s).
# All tuples feed the E-layer; P and F reuse E outputs (no dedicated H3).

_LDAC_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === f01: STG-liking coupling ===
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 3, 0, 2,
        "Pleasantness at 100ms L2 -- fast hedonic tracking",
        "Gold et al. 2023a"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 8, 1, 2,
        "Mean pleasantness 500ms L2 -- smoothed liking signal",
        "Gold et al. 2023a"),
    _h3(_SENSORY_PLEASANTNESS, "sensory_pleasantness", 16, 2, 2,
        "Pleasantness variability 1s L2 -- liking stability",
        "Gold et al. 2023a"),

    # === f02: Pleasure gating ===
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Loudness at 100ms L2 -- sensory salience for gating",
        "Martinez-Molina et al. 2016"),
    _h3(_LOUDNESS, "loudness", 16, 1, 2,
        "Mean loudness over 1s L2 -- sustained arousal context",
        "Martinez-Molina et al. 2016"),

    # === f03: IC x liking interaction ===
    _h3(_SPECTRAL_CHANGE, "spectral_change", 2, 0, 0,
        "IC at 75ms L0 -- surprise detection for IC x liking",
        "Gold et al. 2023a"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 8, 8, 0,
        "IC velocity at 500ms L0 -- rate of surprise change",
        "Cheung et al. 2019"),
    _h3(_SPECTRAL_CHANGE, "spectral_change", 16, 20, 2,
        "IC entropy over 1s L2 -- predictability context",
        "Cheung et al. 2019"),

    # === f04: Moment-to-moment tracking ===
    _h3(_SPECTRAL_FLUX, "spectral_flux", 3, 0, 2,
        "Spectral flux at 100ms L2 -- deviation detection",
        "Gold et al. 2023a"),
    _h3(_SPECTRAL_FLUX, "spectral_flux", 8, 2, 2,
        "Flux variability 500ms L2 -- deviation consistency",
        "Gold et al. 2023a"),

    # === Cross-layer modulation ===
    _h3(_X_L0L5_START, "x_l0l5", 3, 0, 2,
        "Auditory gating at 100ms L2 -- cross-layer modulation",
        "Martinez-Molina et al. 2016"),
    _h3(_X_L0L5_START, "x_l0l5", 16, 20, 2,
        "Gating entropy over 1s L2 -- modulation complexity",
        "Martinez-Molina et al. 2016"),
)

assert len(_LDAC_H3_DEMANDS) == 12


class LDAC(Associator):
    """Liking-Dependent Auditory Cortex -- RPU Associator (depth 2, 6D).

    Models how moment-to-moment liking continuously modulates auditory
    cortex (R STG) processing. High IC combined with disliking produces
    the lowest STG activation (maximal sensory suppression). Pleasure
    gates sensory gain via top-down reward-to-perception pathway.
    Fastest tau_decay (0.5s) reflects rapid continuous tracking.

    Gold et al. (2023a): R STG covaries with normalized moment-to-moment
    liking (t(23) = 2.56, p = 0.018). IC x liking interaction in R STG
    (t(23) = 2.92, p = 0.008). fMRI, N=24, naturalistic listening with
    continuous joystick ratings.

    Martinez-Molina et al. (2016): R STG-NAcc functional connectivity
    modulated by musical reward sensitivity (PPI group effect p = 0.05).
    fMRI, N=45.

    Cheung et al. (2019): Uncertainty x surprise interaction in bilateral
    auditory cortex replicates IC x liking in harmonic domain. fMRI, N=35.

    Dependency chain:
        LDAC reads IUCP, RPEM (intra-unit F6/RPU, depth 0-1), and
        DAED (F6 RPU, depth 0-1). Computed after all three in scheduler.

    Downstream feeds:
        -> stg_modulation belief (Core)
        -> F3 Attention ASU.sensory_gain (via forecast)
    """

    NAME = "LDAC"
    FULL_NAME = "Liking-Dependent Auditory Cortex"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 6
    UPSTREAM_READS = ("IUCP", "RPEM", "DAED")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:stg_liking_coupling", "E1:pleasure_gating",
             "E2:ic_liking_interaction", "E3:moment_to_moment"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 5,
            ("P0:stg_modulation_state",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 5, 6,
            ("F0:sensory_gating_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _LDAC_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:stg_liking_coupling", "E1:pleasure_gating",
            "E2:ic_liking_interaction", "E3:moment_to_moment",
            "P0:stg_modulation_state",
            "F0:sensory_gating_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # R STG -- primary locus of liking-dependent modulation
            RegionLink("E0:stg_liking_coupling", "R_STG", 0.85,
                       "Gold et al. 2023a"),
            # R STG -- pleasure gating of sensory gain
            RegionLink("E1:pleasure_gating", "R_STG", 0.80,
                       "Martinez-Molina et al. 2016"),
            # R STG -- IC x liking interaction hub
            RegionLink("E2:ic_liking_interaction", "R_STG", 0.85,
                       "Gold et al. 2023a"),
            # NAcc -- reward pathway coupling with STG
            RegionLink("E1:pleasure_gating", "NAcc", 0.75,
                       "Martinez-Molina et al. 2016"),
            # Bilateral AC -- IC x liking replicated in harmonic domain
            RegionLink("E2:ic_liking_interaction", "bilateral_AC", 0.70,
                       "Cheung et al. 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- reward-to-perception gating pathway
            NeuroLink("E1:pleasure_gating", "dopamine", 0.70,
                      "Martinez-Molina et al. 2016"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold et al.", 2023,
                         "R STG covaries with normalized moment-to-moment "
                         "liking (t(23) = 2.56, p = 0.018). IC x liking "
                         "interaction in R STG (t(23) = 2.92, p = 0.008). "
                         "Naturalistic listening with continuous joystick "
                         "ratings",
                         "fMRI, N=24"),
                Citation("Martinez-Molina et al.", 2016,
                         "R STG-NAcc functional connectivity modulated by "
                         "musical reward sensitivity (PPI group effect "
                         "p = 0.05). Anhedonia reduces STG-NAcc coupling",
                         "fMRI, N=45"),
                Citation("Cheung et al.", 2019,
                         "Uncertainty x surprise interaction in bilateral "
                         "auditory cortex replicates IC x liking in "
                         "harmonic domain",
                         "fMRI, N=35"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.55, 0.75),
            falsification_criteria=(
                "STG-liking coupling (E0) must increase with pleasantness; "
                "if R STG shows no covariation with moment-to-moment liking, "
                "the core LDAC finding is invalid (Gold 2023a: t=2.56, p=0.018)",
                "IC x liking interaction (E2) must show that high IC + low liking "
                "produces lowest activation; if the interaction term does not show "
                "the predicted inversion pattern, the model is invalid "
                "(Gold 2023a: t=2.92, p=0.008)",
                "Pleasure gating (E1) must modulate sensory gain; removing "
                "pleasure signal should flatten STG responsiveness "
                "(Martinez-Molina 2016: PPI p=0.05)",
                "STG modulation (P0) must track at tau_decay <= 0.5s; if "
                "tracking is slower than 1s, the continuous joystick paradigm "
                "analogy breaks down (Gold 2023a)",
                "Sensory gating prediction (F0) must predict near-future gating "
                "state; if F0 does not correlate with future P0, the forecast "
                "is uninformative",
                "IUCP/RPEM/DAED upstream must contribute; ablating all three "
                "should significantly reduce LDAC output variance",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 + upstream into 6D liking-dependent STG output.

        Delegates to 3 layer functions (extraction -> cognitive_present
        -> forecast); no temporal integration layer.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"IUCP": (B, T, D), "RPEM": (B, T, D),
                                  "DAED": (B, T, D)}``

        Returns:
            ``(B, T, 6)`` -- E(4) + P(1) + F(1)
        """
        e = compute_extraction(h3_features, r3_features, upstream_outputs)
        p = compute_cognitive_present(e)
        f = compute_forecast(e)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
