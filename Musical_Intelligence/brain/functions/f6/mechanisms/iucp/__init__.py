"""IUCP -- Inverted-U Complexity Preference.

Encoder nucleus (depth 1) in RPU, Function F6. Models the Berlyne (1971)
inverted-U complexity-preference function using Gold 2019's empirical
parametrization. Two independent inverted-U curves are computed for information
content (IC) and entropy, then combined via an interaction term to produce the
optimal complexity zone signal.

Core transform: 4.0 * x * (1.0 - x) -- quadratic peaking at x=0.5.

Reads: RPEM (intra-circuit via relay_outputs), DAED (intra-circuit via relay_outputs)

R3 Ontology Mapping (post-freeze 97D):
    roughness:                  [0]      (A, harmonic complexity)
    sensory_pleasantness:       [4]      (A, hedonic baseline)
    loudness:                   [8]      (B, perceptual weight -- velocity_D)
    spectral_flux:              [21]     (D, information content / surprise)
    distribution_concentration: [24]     (D, spectral focus / timbral complexity)
    x_l4l5:                     [33:41]  (G, IC-entropy coupling surface)

Output structure: E(4) + P(1) + F(1) = 6D
  E-layer [0:4]  Extraction        (sigmoid)  scope=internal
  P-layer [4:5]  Cognitive Present (sigmoid)  scope=hybrid
  F-layer [5:6]  Forecast          (sigmoid)  scope=external

See Building/C3-Brain/F6-Reward-and-Motivation/mechanisms/iucp/
"""
from __future__ import annotations

from typing import Dict, Tuple

import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import Encoder
from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    CrossUnitPathway,
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
    4: "125ms (theta)",
    8: "500ms (delta)",
    16: "1s (beat)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "prediction", 2: "integration"}


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
_ROUGHNESS = 0
_SENSORY_PLEASANTNESS = 4
_LOUDNESS = 8
_SPECTRAL_FLUX = 21
_DIST_CONCENTRATION = 24


# -- 14 H3 Demand Specifications -----------------------------------------------
# Inverted-U complexity preference requires IC (spectral_flux), entropy
# (concentration), coupling (x_l4l5), and hedonic signals across multi-scale
# temporal windows. All L2 (integration/bidirectional).

_IUCP_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-Layer: IC + Entropy + Interaction + Optimal (14 tuples) ===
    # 0: IC at 125ms theta timescale
    _h3(21, "spectral_flux", 4, 0, 2,
        "IC at 125ms theta timescale",
        "Gold 2019"),
    # 1: IC entropy at 500ms
    _h3(21, "spectral_flux", 8, 20, 2,
        "IC entropy at 500ms",
        "Gold 2019"),
    # 2: Mean IC over 1s -- primary IC input for inverted-U
    _h3(21, "spectral_flux", 16, 1, 2,
        "Mean IC over 1s -- primary IC input for inverted-U",
        "Gold 2019"),
    # 3: Concentration at 125ms
    _h3(24, "distribution_concentration", 4, 0, 2,
        "Concentration at 125ms",
        "Gold 2019"),
    # 4: Concentration std at 500ms
    _h3(24, "distribution_concentration", 8, 2, 2,
        "Concentration std at 500ms",
        "Gold 2019"),
    # 5: Concentration entropy 1s -- primary entropy input
    _h3(24, "distribution_concentration", 16, 20, 2,
        "Concentration entropy 1s -- primary entropy input",
        "Gold 2019"),
    # 6: Mean roughness 500ms -- harmonic complexity
    _h3(0, "roughness", 8, 1, 2,
        "Mean roughness 500ms -- harmonic complexity",
        "Gold 2019"),
    # 7: Roughness variability 1s
    _h3(0, "roughness", 16, 2, 2,
        "Roughness variability 1s",
        "Gold 2023b"),
    # 8: Mean loudness 1s -- perceptual weighting
    _h3(8, "loudness", 16, 1, 2,
        "Mean loudness 1s -- perceptual weighting",
        "Gold 2023b"),
    # 9: Mean pleasantness 1s -- hedonic baseline
    _h3(4, "sensory_pleasantness", 16, 1, 2,
        "Mean pleasantness 1s -- hedonic baseline",
        "Gold 2019"),
    # 10: Pleasantness variability 1s -- hedonic fluctuation
    _h3(4, "sensory_pleasantness", 16, 2, 2,
        "Pleasantness variability 1s -- hedonic fluctuation",
        "Gold 2019"),
    # 11: IC-perceptual coupling 500ms
    _h3(33, "x_l4l5", 8, 1, 2,
        "IC-perceptual coupling 500ms",
        "Cheung 2019"),
    # 12: Coupling variability 1s
    _h3(33, "x_l4l5", 16, 2, 2,
        "Coupling variability 1s",
        "Cheung 2019"),
    # 13: Coupling entropy 1s -- interaction uncertainty
    _h3(33, "x_l4l5", 16, 20, 2,
        "Coupling entropy 1s -- interaction uncertainty",
        "Cheung 2019"),
)

assert len(_IUCP_H3_DEMANDS) == 14


class IUCP(Encoder):
    """Inverted-U Complexity Preference -- RPU Encoder (depth 1, 6D).

    Models the Berlyne (1971) inverted-U complexity-preference function using
    Gold 2019's empirical parametrization. Two independent inverted-U curves
    are computed for information content (IC) and entropy, then combined via
    an interaction term to produce the optimal complexity zone signal.

    The core transform 4.0 * x * (1.0 - x) produces a quadratic that peaks
    at x=0.5, implementing the Berlyne optimal complexity principle: medium
    complexity maximizes liking.

    Gold et al. (2019): IC quadratic beta_quad = -0.09 (p < 0.001),
    R-squared = 26.3% (Study 1, N=43); replicated beta_quad = -0.18,
    R-squared = 41.6% (Study 2, N=27). Entropy quadratic beta_quad = -0.06
    (p = 0.003), R-squared = 19.1% (Study 1); replicated beta_quad = -0.25,
    R-squared = 34.9% (Study 2).

    Gold et al. (2023b): VS + STG fMRI evidence for preference signal.
    F(1,22) = 4.83, p = 0.039, N=24.

    Cheung et al. (2019): Saddle-shaped preference surface. IC x entropy
    interaction partial eta-squared = 0.07. NAcc reflects uncertainty (not
    surprise). Amygdala + hippocampus + STG reflect interaction. fMRI, N=39+40.

    Dependency chain:
        IUCP is an Encoder (Depth 1) -- reads RPEM + DAED relay outputs.
        Computed after RPEM and DAED in F6 pipeline.

    Downstream feeds:
        -> optimal_complexity belief (Core, tau=TBD)
        -> DAED preference drives DA anticipation
        -> RPEM preference modulates RPE
    """

    NAME = "IUCP"
    FULL_NAME = "Inverted-U Complexity Preference"
    UNIT = "RPU"
    FUNCTION = "F6"
    OUTPUT_DIM = 6
    UPSTREAM_READS = ("RPEM", "DAED")
    CROSS_UNIT_READS = (
        CrossUnitPathway(
            pathway_id="RPU_RPEM__RPU_IUCP__prediction_error",
            name="RPEM prediction error to IUCP complexity assessment",
            source_unit="RPU",
            source_model="RPEM",
            source_dims=("prediction_error",),
            target_unit="RPU",
            target_model="IUCP",
            correlation="r=0.65",
            citation="Gold 2019",
        ),
        CrossUnitPathway(
            pathway_id="RPU_DAED__RPU_IUCP__wanting",
            name="DAED wanting/liking to IUCP preference context",
            source_unit="RPU",
            source_model="DAED",
            source_dims=("wanting_index",),
            target_unit="RPU",
            target_model="IUCP",
            correlation="r=0.55",
            citation="Gold 2023b",
        ),
    )

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("E0:ic_liking_curve", "E1:entropy_liking_curve",
             "E2:ic_entropy_interaction", "E3:optimal_complexity"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 4, 5,
            ("P0:current_preference_state",),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 5, 6,
            ("F0:optimal_zone_pred",),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _IUCP_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "E0:ic_liking_curve", "E1:entropy_liking_curve",
            "E2:ic_entropy_interaction", "E3:optimal_complexity",
            "P0:current_preference_state",
            "F0:optimal_zone_pred",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # VS (ventral striatum) -- reward signal tracks average liking
            RegionLink("P0:current_preference_state", "VS", 0.80,
                       "Gold 2023b"),
            # STG -- IC processing and preference coding
            RegionLink("E0:ic_liking_curve", "STG", 0.75,
                       "Gold 2023b"),
            # Amygdala -- IC x entropy interaction surface
            RegionLink("E2:ic_entropy_interaction", "amygdala", 0.80,
                       "Cheung 2019"),
            # Hippocampus -- IC x entropy interaction, memory context
            RegionLink("E2:ic_entropy_interaction", "hippocampus", 0.75,
                       "Cheung 2019"),
            # NAcc -- anticipatory reward from optimal zone prediction
            RegionLink("F0:optimal_zone_pred", "NAcc", 0.75,
                       "Cheung 2019"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # Dopamine -- preference drives DA via DAED anticipation
            NeuroLink("P0:current_preference_state", "dopamine", 0.70,
                      "Gold 2023b"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Gold et al.", 2019,
                         "Predictability and surprise jointly modulate "
                         "auditory cortical processing and aesthetic pleasure. "
                         "IC quadratic beta=-0.09 (p<0.001), R2=26.3% "
                         "(Study 1, N=43); replicated beta=-0.18, R2=41.6% "
                         "(Study 2, N=27)",
                         "fMRI, N=43+27"),
                Citation("Gold et al.", 2023,
                         "VS + STG fMRI evidence for preference signal. "
                         "F(1,22)=4.83, p=0.039. Ventral striatum reward "
                         "signal tracks average liking",
                         "fMRI, N=24"),
                Citation("Cheung et al.", 2019,
                         "Saddle-shaped preference surface: IC x entropy "
                         "interaction partial eta2=0.07. NAcc reflects "
                         "uncertainty. Amygdala + hippocampus + STG reflect "
                         "interaction",
                         "fMRI, N=39+40"),
                Citation("Berlyne", 1971,
                         "Aesthetics and psychobiology: inverted-U complexity "
                         "preference function. Medium complexity maximizes "
                         "hedonic value",
                         "theory"),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.90),
            falsification_criteria=(
                "IC liking curve (E0) must show inverted-U with peak at "
                "medium IC; if linear relationship, the quadratic model is "
                "invalid (Gold 2019: beta_quad < 0, p < 0.001)",
                "Entropy liking curve (E1) must show inverted-U with peak at "
                "medium entropy; if entropy has no quadratic effect, model is "
                "invalid (Gold 2019: beta_quad = -0.06, p = 0.003)",
                "IC x entropy interaction (E2) must show saddle surface; high "
                "entropy should shift optimal IC downward (Cheung 2019: "
                "partial eta2 = 0.07)",
                "Current preference state (P0) must predict VS BOLD signal; "
                "if no correlation with ventral striatum, reward link is "
                "invalid (Gold 2023b: F(1,22) = 4.83, p = 0.039)",
                "Optimal zone prediction (F0) must predict future liking "
                "within tau_decay = 2.0s; if prediction horizon is shorter, "
                "the forecast model needs recalibration",
                "Disrupting IC x entropy interaction should reduce amygdala "
                "and hippocampus activation (Cheung 2019, testable via "
                "entropy-matched IC manipulation)",
            ),
            version="1.0.0",
        )

    # -- Compute ---------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Transform R3/H3 + RPEM/DAED relay outputs into 6D complexity preference.

        Delegates to 3 layer functions (extraction -> cognitive_present ->
        forecast) and stacks results. No M-layer (temporal integration) for
        IUCP -- the inverted-U operates on instantaneous complexity signals.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"RPEM": (B, T, D), "DAED": (B, T, D)}``

        Returns:
            ``(B, T, 6)`` -- E(4) + P(1) + F(1)
        """
        e = compute_extraction(h3_features, r3_features, relay_outputs)
        p = compute_cognitive_present(e)
        f = compute_forecast(e)

        output = torch.stack([*e, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
