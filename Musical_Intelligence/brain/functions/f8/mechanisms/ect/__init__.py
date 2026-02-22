"""ECT -- Expertise Compartmentalization Trade-off.

Associator nucleus (depth 2) in NDU, Function F8. Models the expertise
compartmentalization trade-off: musical expertise increases within-network
efficiency at the cost of reduced between-network connectivity
(Paraskevopoulos 2022: 106 within vs 192 between edges). The trade-off
ratio captures the cost-benefit balance. Network flexibility (Wu-Chung 2025)
moderates whether training produces cognitive benefit.

Core finding: Paraskevopoulos et al. (2022) found musicians show 106
within-network edges vs 192 between-network edges in non-musicians
(p < 0.001 FDR). IFG area 47m is the highest-degree supramodal hub
across 5/6 network states. Moller et al. (2021) provided the first
behavioral evidence: musicians show reduced benefit from visual cues in
audiovisual binding (BCG: t(42.3) = 3.06, p = 0.004), demonstrating the
functional cost of compartmentalization.

Reads: EDNR (intra-unit), CDMR (intra-unit), SLEE (intra-unit)
All three are F8 NDU mechanisms at depth 0-1.

R3 Ontology Mapping (post-freeze 97D):
    x_l0l5:             [25:33]  (F, within-network coupling)
    x_l4l5:             [33:41]  (G, pattern-feature binding)
    x_l5l6:             [41:49]  (H, cross-network connectivity)
    spectral_change:    [21]     (D, reconfiguration capacity proxy)
    amplitude:          [7]      (B, task demand / velocity_A)
    loudness:           [8]      (B, attention allocation / velocity_D)
    pitch_change:       [23]     (D, specialization tracking)
    brightness:         [13]     (C, tonal adaptation / brightness_kuttruff)

Output structure: E(4) + M(3) + P(2) + F(3) = 12D
  E-layer [0:4]   Extraction           (sigmoid/ratio)  scope=internal
  M-layer [4:7]   Temporal Integration (sigmoid)         scope=internal
  P-layer [7:9]   Cognitive Present    (sigmoid)         scope=hybrid
  F-layer [9:12]  Forecast             (sigmoid)         scope=external

See Building/C3-Brain/F8-Learning-and-Plasticity/mechanisms/ect/
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
from .temporal_integration import compute_temporal_integration

# -- Horizon labels ------------------------------------------------------------
_H_LABELS = {
    3: "100ms (gamma)",
    4: "125ms (gamma)",
    8: "500ms (theta)",
    16: "1s (delta)",
}

# -- Morph labels --------------------------------------------------------------
_M_LABELS = {
    0: "value", 1: "mean", 2: "std", 8: "velocity",
    18: "trend", 20: "entropy",
}

# -- Law labels ----------------------------------------------------------------
_L_LABELS = {0: "memory", 1: "forward", 2: "integration"}


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


# -- R3 feature indices (post-freeze 97D) -------------------------------------
_X_L0L5_START = 25               # F group (within-network coupling)
_X_L4L5_START = 33               # G group (pattern-feature binding)
_X_L5L6_START = 41               # H group (cross-network connectivity)
_SPECTRAL_CHANGE = 21            # D group (reconfiguration capacity proxy)
_AMPLITUDE = 7                   # B group (velocity_A / task demand)
_LOUDNESS = 8                    # B group (velocity_D / attention)
_PITCH_CHANGE = 23               # D group (specialization tracking)
_BRIGHTNESS = 13                 # C group (brightness_kuttruff)


# -- 18 H3 Demand Specifications (E:10 + M:2 + P:4 + F:2) --------------------
# All 18 tuples are unique across layers.

_ECT_H3_DEMANDS: Tuple[H3DemandSpec, ...] = (
    # === E-layer: Extraction (tuples 0-9) ===

    # #0: Mean within-network coupling 1s
    _h3(_X_L0L5_START, "x_l0l5", 16, 1, 2,
        "Mean within-network coupling 1s -- within efficiency baseline",
        "Paraskevopoulos 2022"),
    # #1: Mean pattern binding 1s
    _h3(_X_L4L5_START, "x_l4l5", 16, 1, 2,
        "Mean pattern binding 1s -- within-network binding strength",
        "Paraskevopoulos 2022"),
    # #2: Mean cross-network connectivity 1s
    _h3(_X_L5L6_START, "x_l5l6", 16, 1, 2,
        "Mean cross-network connectivity 1s -- between-network baseline",
        "Paraskevopoulos 2022"),
    # #3: Cross-network entropy 1s
    _h3(_X_L5L6_START, "x_l5l6", 16, 20, 2,
        "Cross-network entropy 1s -- between-network diversity",
        "Paraskevopoulos 2022"),
    # #4: Reconfiguration at 100ms
    _h3(_SPECTRAL_CHANGE, "spectral_change", 3, 0, 2,
        "Reconfiguration at 100ms -- flexibility proxy",
        "Wu-Chung 2025"),
    # #5: Reconfiguration speed 125ms
    _h3(_SPECTRAL_CHANGE, "spectral_change", 4, 8, 0,
        "Reconfiguration speed 125ms -- flexibility velocity",
        "Wu-Chung 2025"),
    # #6: Within-network coupling 100ms
    _h3(_X_L0L5_START, "x_l0l5", 3, 0, 2,
        "Within-network coupling 100ms -- instantaneous coupling",
        "Papadaki 2023"),
    # #7: Coupling variability 100ms
    _h3(_X_L0L5_START, "x_l0l5", 3, 2, 2,
        "Coupling variability 100ms -- coupling stability",
        "Papadaki 2023"),
    # #8: Cross-network binding 100ms
    _h3(_X_L5L6_START, "x_l5l6", 3, 0, 2,
        "Cross-network binding 100ms -- instantaneous isolation",
        "Moller 2021"),
    # #9: Cross-network variability 100ms
    _h3(_X_L5L6_START, "x_l5l6", 3, 2, 2,
        "Cross-network variability 100ms -- isolation stability",
        "Moller 2021"),

    # === M-layer: Temporal Integration (tuples 10-11) ===

    # #10: Pattern binding trend 1s
    _h3(_X_L4L5_START, "x_l4l5", 16, 18, 0,
        "Pattern binding trend 1s -- specialization accumulation",
        "Leipold 2021"),
    # #11: Demand entropy 500ms
    _h3(_AMPLITUDE, "amplitude", 8, 20, 2,
        "Demand entropy 500ms -- task demand variability",
        "Olszewska 2021"),

    # === P-layer: Cognitive Present (tuples 12-15) ===

    # #12: Pattern binding at 100ms
    _h3(_X_L4L5_START, "x_l4l5", 3, 0, 2,
        "Pattern binding at 100ms -- instantaneous binding state",
        "Papadaki 2023"),
    # #13: Pitch specialization at 100ms
    _h3(_PITCH_CHANGE, "pitch_change", 3, 0, 2,
        "Pitch specialization at 100ms -- domain specificity",
        "Leipold 2021"),
    # #14: Mean pitch specialization 1s
    _h3(_PITCH_CHANGE, "pitch_change", 16, 1, 2,
        "Mean pitch specialization 1s -- sustained specialization",
        "Leipold 2021"),
    # #15: Attention allocation at 100ms
    _h3(_LOUDNESS, "loudness", 3, 0, 2,
        "Attention allocation at 100ms -- processing demand context",
        "Papadaki 2023"),

    # === F-layer: Forecast (tuples 16-17) ===

    # #16: Task demand at 100ms
    _h3(_AMPLITUDE, "amplitude", 3, 0, 2,
        "Task demand at 100ms -- efficiency context",
        "Moller 2021"),
    # #17: Tonal adaptation at 100ms
    _h3(_BRIGHTNESS, "brightness", 3, 0, 2,
        "Tonal adaptation at 100ms -- flexibility context",
        "Wu-Chung 2025"),
)

assert len(_ECT_H3_DEMANDS) == 18

# -- Upstream dimension defaults -----------------------------------------------
_EDNR_DIM = 10
_CDMR_DIM = 11
_SLEE_DIM = 13


class ECT(Associator):
    """Expertise Compartmentalization Trade-off -- NDU Associator (depth 2, 12D).

    Models the expertise compartmentalization trade-off where musical
    expertise increases within-network efficiency at the cost of reduced
    between-network connectivity. The trade-off ratio captures the
    cost-benefit balance, while network flexibility moderates whether
    training produces cognitive benefit.

    Paraskevopoulos et al. (2022): 106 within-network edges M > NM vs
    192 between-network edges NM > M (p < 0.001 FDR). IFG area 47m is
    highest-degree supramodal hub (5/6 network states). MEG, N=25.

    Moller et al. (2021): Musicians show reduced benefit from visual cues
    in audiovisual binding (BCG: t(42.3) = 3.06, p = 0.004). Reduced
    cross-modal structural connectivity (IFOF FA). fMRI+DTI, N=44.

    Wu-Chung et al. (2025): Music creativity benefits depend on baseline
    network flexibility; higher flexibility leads to more cognitive benefit
    from training. fMRI, N=30.

    Dependency chain:
        ECT reads EDNR (NDU depth 0), CDMR (NDU depth 1),
        SLEE (NDU depth 1). Computed after all three in scheduler.

    Downstream feeds:
        -> compartmentalization_state belief (Appraisal)
        -> transfer_capacity belief (Anticipation)
        -> specialization_trajectory belief (Anticipation)
    """

    NAME = "ECT"
    FULL_NAME = "Expertise Compartmentalization Trade-off"
    UNIT = "NDU"
    FUNCTION = "F8"
    OUTPUT_DIM = 12
    UPSTREAM_READS = ("EDNR", "CDMR", "SLEE")

    LAYERS = (
        LayerSpec(
            "E", "Extraction", 0, 4,
            ("f01:within_efficiency", "f02:between_reduction",
             "f03:trade_off_ratio", "f04:flexibility_index"),
            scope="internal",
        ),
        LayerSpec(
            "M", "Temporal Integration", 4, 7,
            ("training_history", "network_state", "task_memory"),
            scope="internal",
        ),
        LayerSpec(
            "P", "Cognitive Present", 7, 9,
            ("within_binding", "network_isolation"),
            scope="hybrid",
        ),
        LayerSpec(
            "F", "Forecast", 9, 12,
            ("transfer_limit", "efficiency_opt", "flexibility_recovery"),
            scope="external",
        ),
    )

    # -- Abstract property implementations -------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return _ECT_H3_DEMANDS

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01:within_efficiency", "f02:between_reduction",
            "f03:trade_off_ratio", "f04:flexibility_index",
            "training_history", "network_state", "task_memory",
            "within_binding", "network_isolation",
            "transfer_limit", "efficiency_opt", "flexibility_recovery",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            # IFG (area 47m) -- supramodal hub for expertise effects
            RegionLink("f01:within_efficiency", "IFG_47m", 0.85,
                       "Paraskevopoulos 2022"),
            # Bilateral STG -- within-network connectivity
            RegionLink("f01:within_efficiency", "bilateral_STG", 0.80,
                       "Leipold 2021"),
            # IFG -- between-network reduction hub
            RegionLink("f02:between_reduction", "IFG_47m", 0.80,
                       "Paraskevopoulos 2022"),
            # Heschl's Gyrus -- localized CT correlations
            RegionLink("within_binding", "HG", 0.75,
                       "Moller 2021"),
            # IFOF white matter -- structural connectivity for AV binding
            RegionLink("network_isolation", "IFOF", 0.80,
                       "Moller 2021"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            # BDNF -- neuroplasticity modulator for flexibility
            NeuroLink("f04:flexibility_index", "BDNF", 0.65,
                      "Wu-Chung 2025"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Paraskevopoulos et al.", 2022,
                         "Musicians show 106 within-network edges vs 192 "
                         "between-network edges in non-musicians (p < 0.001 "
                         "FDR). IFG area 47m is highest-degree supramodal "
                         "hub across 5/6 network states",
                         "MEG, N=25"),
                Citation("Moller et al.", 2021,
                         "Musicians show reduced benefit from visual cues "
                         "in audiovisual binding (BCG: t(42.3) = 3.06, "
                         "p = 0.004). Reduced cross-modal structural "
                         "connectivity (IFOF FA cluster p < 0.001)",
                         "fMRI+DTI, N=44"),
                Citation("Leipold et al.", 2021,
                         "Robust effects of musicianship on interhemispheric "
                         "and intrahemispheric connectivity (pFWE < 0.05), "
                         "independent of absolute pitch",
                         "fMRI, N=153"),
                Citation("Wu-Chung et al.", 2025,
                         "Music creativity benefits depend on baseline "
                         "network flexibility; higher flexibility leads to "
                         "more cognitive benefit from training",
                         "fMRI, N=30"),
                Citation("Papadaki et al.", 2023,
                         "Network strength and global efficiency correlate "
                         "with interval recognition (rho = 0.36, p = 0.02) "
                         "in aspiring professionals",
                         "fMRI, N=42"),
                Citation("Olszewska et al.", 2021,
                         "Training-induced brain reorganization involves "
                         "dynamic reconfiguration of neural connections",
                         "review"),
                Citation("Blasi et al.", 2025,
                         "Music/dance rehabilitation produces neuroplasticity "
                         "in perception, memory, and motor areas, suggesting "
                         "recovery is possible",
                         "systematic review"),
            ),
            evidence_tier="gamma",
            confidence_range=(0.50, 0.70),
            falsification_criteria=(
                "Within-efficiency (f01) must increase with musical training "
                "duration; if within-network coupling shows no expertise "
                "gradient, the compartmentalization model is invalid "
                "(Paraskevopoulos 2022: 106 vs 192 edges, p < 0.001)",
                "Between-reduction (f02) must covary with expertise level; "
                "if between-network connectivity is unchanged by training, "
                "the trade-off model is unsupported "
                "(Paraskevopoulos 2022: 47 vs 15 multilinks)",
                "Trade-off ratio (f03) must predict behavioral cost; if "
                "high compartmentalization does not predict reduced cross-"
                "modal transfer, the functional consequence is unconfirmed "
                "(Moller 2021: BCG t = 3.06, p = 0.004)",
                "Flexibility index (f04) must moderate training benefit; "
                "if removing flexibility does not change the training outcome, "
                "the recovery pathway is unsupported "
                "(Wu-Chung 2025: flexibility x training interaction)",
                "Transfer limitation (F-layer) must predict cross-domain "
                "performance; if transfer_limit does not correlate with "
                "actual cross-modal performance, the prediction is uninformative",
                "EDNR/CDMR/SLEE upstream must contribute; ablating all three "
                "should significantly reduce ECT output variance",
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
        """Transform R3/H3 + upstream into 12D compartmentalization output.

        Delegates to 4 layer functions (extraction -> temporal_integration
        -> cognitive_present -> forecast) and stacks results.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"EDNR": (B, T, 10), "CDMR": (B, T, 11),
                                  "SLEE": (B, T, 13)}``

        Returns:
            ``(B, T, 12)`` -- E(4) + M(3) + P(2) + F(3)
        """
        upstream_outputs = upstream_outputs or {}
        B, T = r3_features.shape[0], r3_features.shape[1]
        device = r3_features.device

        # -- Upstream (graceful degradation with zeros) ------------------------
        ednr = upstream_outputs.get(
            "EDNR", torch.zeros(B, T, _EDNR_DIM, device=device),
        )
        cdmr = upstream_outputs.get(
            "CDMR", torch.zeros(B, T, _CDMR_DIM, device=device),
        )
        slee = upstream_outputs.get(
            "SLEE", torch.zeros(B, T, _SLEE_DIM, device=device),
        )

        e = compute_extraction(h3_features, r3_features, ednr, cdmr, slee)
        m = compute_temporal_integration(
            h3_features, r3_features, e, ednr, cdmr, slee,
        )
        p = compute_cognitive_present(
            h3_features, r3_features, e, m, ednr, cdmr, slee,
        )
        f = compute_forecast(h3_features, e, m, p, ednr, cdmr, slee)

        output = torch.stack([*e, *m, *p, *f], dim=-1)
        return output.clamp(0.0, 1.0)
