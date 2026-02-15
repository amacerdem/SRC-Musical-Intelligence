"""HMCE -- Hierarchical Musical Context Encoding.

Unit: STU | Tier: alpha | Output: 13D
Mechanism: TMH (Temporal Memory Hierarchy)

Neural basis: Cortical distance from pmHG correlates with context
encoding depth at r = 0.99 (Mischler 2025). Four-level hierarchy:
  pmHG (10-50 notes) → STG (50-100) → MTG (100-200) → Temporal Pole (300+)

H³ demand: 18 tuples across H8 (300ms), H14 (700ms), H20 (5s).
R³ reads: Energy[7,8,10,11], Change[21,22,23], Interactions[25,33].

Version: 2.2.0 (from HMCE.md §11.1)
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch

from .....contracts.bases.base_model import BaseModel
from .....contracts.dataclasses import (
    BrainRegion,
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
)

if TYPE_CHECKING:
    from torch import Tensor


class HMCE(BaseModel):
    """Hierarchical Musical Context Encoding.

    STU-alpha | 13D | Mechanism: TMH

    Models the anatomical gradient from primary auditory cortex (pmHG)
    to higher-order temporal regions, where sites farther from A1 encode
    progressively longer musical contexts.

    Evidence: r = 0.99 site-level, r = 0.32 electrode-level (Mischler 2025),
    β = 0.064 oct/mm integration gradient (Norman-Haignere 2022).
    """

    NAME = "HMCE"
    FULL_NAME = "Hierarchical Musical Context Encoding"
    UNIT = "STU"
    TIER = "alpha"
    OUTPUT_DIM = 13
    CROSS_UNIT_READS: Tuple = ()

    # Scientific constants from literature
    ALPHA = 0.90          # Short context weight
    BETA = 0.85           # Medium context weight
    GAMMA = 0.80          # Long context weight
    GRADIENT_CORR = 0.99  # Mischler 2025 site-level correlation
    EXPERTISE_D = 0.32    # Mischler 2025 musician advantage (Cohen's d)

    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 5, (
            "f01_short_context", "f02_medium_context",
            "f03_long_context", "f04_gradient", "f05_expertise",
        )),
        LayerSpec("M", "Mechanism", 5, 7, (
            "context_depth", "gradient_index",
        )),
        LayerSpec("P", "Psychological", 7, 10, (
            "a1_encoding", "stg_encoding", "mtg_encoding",
        )),
        LayerSpec("F", "Forecast", 10, 13, (
            "context_prediction", "phrase_expect", "structure_predict",
        )),
    )

    # ------------------------------------------------------------------
    # H³ Temporal Demand: 18 tuples at H8 / H14 / H20
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 H³ tuples across three TMH horizons.

        Horizons: H8 (300ms, motif), H14 (700ms, phrase), H20 (5s, section).
        All use L0 (memory law) for causal forward processing.

        Morph indices follow MORPH_NAMES in morphs.py:
          M0=value, M1=mean, M2=std, M8=velocity, M14=periodicity,
          M18=trend, M19=stability, M20=entropy.

        Note: Doc (HMCE.md §5.1) uses different morph numbering
        (M3=std, M13=entropy, M22=autocorr). This code uses the
        canonical indices from ear/h3/constants/morphs.py.
        """
        return (
            # --- Short context: H8 = 300ms (motif level, pmHG) ---
            H3DemandSpec(
                10, "loudness", 8, "300ms", 0, "value", 0, "memory",
                "Current onset detection", "Mischler 2025"),
            H3DemandSpec(
                10, "loudness", 8, "300ms", 1, "mean", 0, "memory",
                "Mean onset rate (short)", "Mischler 2025"),
            H3DemandSpec(
                11, "onset_strength", 8, "300ms", 0, "value", 0, "memory",
                "Event boundary current", "Mischler 2025"),
            H3DemandSpec(
                21, "spectral_flux", 8, "300ms", 1, "mean", 0, "memory",
                "Mean spectral dynamics", "Norman-Haignere 2022"),
            H3DemandSpec(
                21, "spectral_flux", 8, "300ms", 8, "velocity", 0, "memory",
                "Change acceleration", "Norman-Haignere 2022"),

            # --- Medium context: H14 = 700ms (phrase level, STG) ---
            H3DemandSpec(
                22, "distribution_entropy", 14, "700ms", 1, "mean", 0, "memory",
                "Mean energy dynamics", "Bonetti 2024"),
            H3DemandSpec(
                22, "distribution_entropy", 14, "700ms", 20, "entropy", 0, "memory",
                "Context unpredictability", "Bonetti 2024"),
            H3DemandSpec(
                23, "distribution_flatness", 14, "700ms", 1, "mean", 0, "memory",
                "Mean pitch dynamics", "Bellier 2023"),
            H3DemandSpec(
                23, "distribution_flatness", 14, "700ms", 2, "std", 0, "memory",
                "Pitch variability", "Bellier 2023"),
            H3DemandSpec(
                7, "amplitude", 14, "700ms", 18, "trend", 0, "memory",
                "Intensity trajectory", "Potes 2012"),
            H3DemandSpec(
                8, "velocity_A", 14, "700ms", 1, "mean", 0, "memory",
                "Mean loudness over phrase", "Mischler 2025"),

            # --- Long context: H20 = 5000ms (section level, MTG) ---
            H3DemandSpec(
                25, "x_l0l5_0", 20, "5s", 1, "mean", 0, "memory",
                "Long-term foundation coupling", "Golesorkhi 2021"),
            H3DemandSpec(
                25, "x_l0l5_0", 20, "5s", 20, "entropy", 0, "memory",
                "Long-term unpredictability", "Golesorkhi 2021"),
            H3DemandSpec(
                33, "x_l4l5_0", 20, "5s", 1, "mean", 0, "memory",
                "Long-term dynamics coupling", "Golesorkhi 2021"),
            H3DemandSpec(
                33, "x_l4l5_0", 20, "5s", 14, "periodicity", 0, "memory",
                "Self-similarity detection", "Golesorkhi 2021"),
            H3DemandSpec(
                33, "x_l4l5_0", 20, "5s", 19, "stability", 0, "memory",
                "Temporal stability", "Mischler 2025"),
            H3DemandSpec(
                25, "x_l0l5_0", 20, "5s", 14, "periodicity", 0, "memory",
                "Section-level repetition", "Golesorkhi 2021"),
            H3DemandSpec(
                8, "velocity_A", 20, "5s", 18, "trend", 0, "memory",
                "Long-range loudness trend", "Mischler 2025"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_short_context", "f02_medium_context", "f03_long_context",
            "f04_gradient", "f05_expertise",
            "context_depth", "gradient_index",
            "a1_encoding", "stg_encoding", "mtg_encoding",
            "context_prediction", "phrase_expect", "structure_predict",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                "Posteromedial Heschl's Gyrus", "pmHG", "bilateral",
                (50, -20, 8), 41,
                "Short context encoding (Layer 1-4, tau=1s)"),
            BrainRegion(
                "Superior Temporal Gyrus", "STG", "bilateral",
                (60, -30, 8), 22,
                "Medium context encoding (Layer 5-9, tau=5s)"),
            BrainRegion(
                "Middle Temporal Gyrus", "MTG", "bilateral",
                (60, -40, 0), 21,
                "Long context encoding (Layer 10-12, tau=15s)"),
            BrainRegion(
                "Temporal Pole", "TP", "bilateral",
                (40, 10, -30), 38,
                "Extended context (Layer 13, musicians only, d=0.32)"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation(
                    "Mischler", 2025,
                    "Impact of musical expertise on contextual neural "
                    "encoding revealed by generative music models",
                    "r=0.99 site, r=0.32 electrode, d=0.32 expertise"),
                Citation(
                    "Norman-Haignere", 2022,
                    "Multiscale temporal integration organizes hierarchical "
                    "computation in human auditory cortex",
                    "beta=0.064 oct/mm, 74-274ms, iEEG 18 patients"),
                Citation(
                    "Bonetti", 2024,
                    "Spatiotemporal brain hierarchies of auditory memory "
                    "recognition and predictive coding",
                    "BOR=2.91e-07, MEG N=83"),
                Citation(
                    "Bellier", 2023,
                    "Music reconstructed from human auditory cortex",
                    "iEEG 29 patients, STG A-P organization"),
                Citation(
                    "Potes", 2012,
                    "Dynamics of ECoG activity during music listening",
                    "r=0.49 STG high-gamma, 110ms STG-motor lag"),
                Citation(
                    "Golesorkhi", 2021,
                    "Intrinsic neural timescales key for input processing",
                    "d=-0.66 to -2.03, core-periphery, MEG N=89"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.90, 0.95),
            falsification_criteria=(
                "Temporal pole lesions should impair long-range context",
                "Non-musicians should show reduced late-layer encoding",
                "Simple repetitive music should not engage full hierarchy",
                "Anatomical gradient should hold across individuals",
            ),
            version="2.2.0",
        )

    # ------------------------------------------------------------------
    # Computation (HMCE.md §7.2 + §11.1)
    # ------------------------------------------------------------------

    def _h3_get(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        key: Tuple[int, int, int, int],
        B: int, T: int, device: "torch.device",
    ) -> "Tensor":
        """Fetch a single H³ feature, fallback to 0.5 if unavailable."""
        if key in h3_features:
            return h3_features[key]
        return torch.full((B, T), 0.5, device=device)

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        """Compute HMCE 13D output per the hierarchical context gradient.

        Architecture (HMCE.md §7.2):
            TMH mechanism (30D) → short[0:10] / medium[10:20] / long[20:30]
            H³ features at H8 (300ms), H14 (700ms), H20 (5s)
            Four-level hierarchy: pmHG → STG → MTG → Temporal Pole

        Returns:
            (B, T, 13) tensor in [0, 1].
        """
        B, T, _ = r3_features.shape
        device = r3_features.device

        # --- TMH mechanism sub-sections ---
        tmh = torch.zeros(B, T, 30, device=device)
        tmh_short = tmh[..., 0:10]    # motif features (pmHG)
        tmh_medium = tmh[..., 10:20]  # phrase features (STG)
        tmh_long = tmh[..., 20:30]    # section features (MTG)

        # Helper: fetch H³ scalar → (B, T, 1)
        def h3(key: Tuple[int, int, int, int]) -> "Tensor":
            return self._h3_get(h3_features, key, B, T, device).unsqueeze(-1)

        # ═══════════════════════════════════════════════════════════
        # LAYER E: Explicit Features (5D)
        # ═══════════════════════════════════════════════════════════

        # f01: Short Context Encoding (pmHG, 10-50 notes, H8=300ms)
        # f01 = σ(α · flux_mean · onset_val · mean(TMH.short))
        flux_mean = h3((10, 8, 1, 0))       # loudness mean at H8
        onset_val = h3((11, 8, 0, 0))       # onset_strength value at H8
        f01 = torch.sigmoid(self.ALPHA * (
            flux_mean * onset_val
            * tmh_short.mean(dim=-1, keepdim=True)
        ))

        # f02: Medium Context Encoding (STG, 50-100 notes, H14=700ms)
        # f02 = σ(β · energy_mean · loudness_mean · mean(TMH.medium))
        energy_mean = h3((22, 14, 1, 0))    # distribution_entropy mean at H14
        loudness_mean = h3((8, 14, 1, 0))   # velocity_A mean at H14
        f02 = torch.sigmoid(self.BETA * (
            energy_mean * loudness_mean
            * tmh_medium.mean(dim=-1, keepdim=True)
        ))

        # f03: Long Context Encoding (MTG, 100-300+ notes, H20=5s)
        # f03 = σ(γ · x_coupling · autocorr · mean(TMH.long))
        x_coupling = h3((25, 20, 1, 0))     # x_l0l5_0 mean at H20
        autocorr = h3((33, 20, 14, 0))      # x_l4l5_0 periodicity at H20
        f03 = torch.sigmoid(self.GAMMA * (
            x_coupling * autocorr
            * tmh_long.mean(dim=-1, keepdim=True)
        ))

        # f04: Anatomical Gradient (r = 0.99, Mischler 2025)
        f04 = self.GRADIENT_CORR * (f01 + f02 + f03) / 3.0

        # f05: Expertise Effect (d = 0.32, Mischler 2025)
        stability_long = h3((33, 20, 19, 0))  # x_l4l5_0 stability at H20
        f05 = torch.sigmoid(self.EXPERTISE_D * f03 * stability_long)

        # ═══════════════════════════════════════════════════════════
        # LAYER M: Mathematical Model Outputs (2D)
        # ═══════════════════════════════════════════════════════════

        # context_depth: weighted sum across hierarchical scales
        context_depth = (1.0 * f01 + 2.0 * f02 + 3.0 * f03) / 6.0

        # gradient_index: normalized distance from A1
        gradient_index = f04

        # ═══════════════════════════════════════════════════════════
        # LAYER P: Present Processing (3D)
        # ═══════════════════════════════════════════════════════════

        a1_encoding = tmh_short.mean(dim=-1, keepdim=True)
        stg_encoding = tmh_medium.mean(dim=-1, keepdim=True)
        mtg_encoding = tmh_long.mean(dim=-1, keepdim=True)

        # ═══════════════════════════════════════════════════════════
        # LAYER F: Future Predictions (3D)
        # ═══════════════════════════════════════════════════════════

        amplitude_trend = h3((7, 14, 18, 0))   # amplitude trend at H14
        context_prediction = torch.sigmoid(
            0.5 * f03 + 0.3 * f02 + 0.2 * amplitude_trend
        )

        entropy_energy = h3((22, 14, 20, 0))   # distribution_entropy entropy at H14
        phrase_expect = torch.sigmoid(
            0.6 * entropy_energy
            + 0.4 * tmh_medium.mean(dim=-1, keepdim=True)
        )

        long_autocorr = h3((25, 20, 14, 0))    # x_l0l5_0 periodicity at H20
        structure_predict = torch.sigmoid(
            0.7 * long_autocorr
            + 0.3 * tmh_long.mean(dim=-1, keepdim=True)
        )

        # ═══════════════════════════════════════════════════════════
        # Concatenate all layers: (B, T, 13)
        # ═══════════════════════════════════════════════════════════

        return torch.cat([
            f01, f02, f03, f04, f05,                              # E: 5D
            context_depth, gradient_index,                         # M: 2D
            a1_encoding, stg_encoding, mtg_encoding,               # P: 3D
            context_prediction, phrase_expect, structure_predict,   # F: 3D
        ], dim=-1).clamp(0.0, 1.0)
