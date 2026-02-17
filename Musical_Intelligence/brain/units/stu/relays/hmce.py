"""HMCE — Hierarchical Musical Context Encoding.

Gold standard Relay nucleus for the Sensorimotor Timing Unit (STU).

Neural Circuit:
    Audio → Cochlea → pmHG / A1 (short context, τ ≈ 74ms)
                        ↓
                      Posterior STG (medium context, τ ≈ 136ms)
                        ↓
                      MTG / Anterior STG (long context, τ ≈ 274ms)
                        ↓
                      IFG (BA44/45) — syntactic irregularity
                        ↓
                      Hippocampus — memory-based predictions
                        ↓
                      ACC — prediction monitoring

Key Findings:
    - Hierarchical temporal receptive windows in auditory cortex:
      A1 (short) → STG (medium) → MTG (long) (Hasson et al. 2008)
    - Anatomical gradient r = 0.99 across 6 site groups for context
      encoding depth along posterior-anterior axis (Mischler et al. 2025)
    - Electrode-level correlation r = 0.32, p = 1.5e-05 (Mischler 2025)
    - Independent replication: β = 0.064 oct/mm frequency preference
      gradient (Norman-Haignere et al. 2022)
    - BOR = 2.91e-07 for hierarchical AC → hippocampus → cingulate
      pathway (Bonetti et al. 2024, MEG)

Critical Qualifier:
    - Mischler r = 0.99 is from only n = 6 site groups (4 df);
      electrode-level r = 0.32 (N = 189 electrodes) is more robust
    - Sabat et al. 2025: integration windows may be invariant to
      context length (15-150ms constant) — gradient may be hardwired
      rather than context-adaptive
    - Basic hierarchy may operate via attention rather than window
      expansion (attentional gradient vs temporal gradient)

Temporal Architecture:
    All demands use L0 (memory law) — causal lookback for context
    encoding at three hierarchical levels:
    - Short context (H8 = 300ms):  Onset/spectral features in A1
    - Medium context (H14):        Energy/loudness patterns in STG
    - Long context (H20):          Structural patterns in MTG

R³ Remapping (Ontology Freeze v1.0.0):
    - Doc [8] "loudness"   → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
    - Doc [25] "x_l0l5"   → Code [42] beat_strength (dissolved)
    - Doc [33] "x_l4l5"   → Code [60] tonal_stability (dissolved)
    - v2 [65] tempo_estimate → Code [41] tempo_estimate
    - v2 [68] syncopation  → Code [44] syncopation_index
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
    NeuroLink,
    RegionLink,
)

# ======================================================================
# Scientific constants
# ======================================================================

# Anatomical gradient correlation — site-group level
# Source: Mischler et al. 2025, r = 0.99, n = 6 sites, 4 df
GRADIENT_R_SITE: float = 0.99

# Anatomical gradient correlation — electrode level (more robust)
# Source: Mischler et al. 2025, r = 0.32, p = 1.5e-05, N = 189
GRADIENT_R_ELECTRODE: float = 0.32

# Frequency preference gradient
# Source: Norman-Haignere et al. 2022, β = 0.064 oct/mm
FREQ_GRADIENT_BETA: float = 0.064

# Hierarchical pathway Bayes factor
# Source: Bonetti et al. 2024, BOR = 2.91e-07, MEG
BONETTI_BOR: float = 2.91e-7

# Context encoding time constants (Mischler 2025)
TAU_SHORT: float = 0.074    # A1: 74ms
TAU_MEDIUM: float = 0.136   # STG: 136ms
TAU_LONG: float = 0.274     # MTG: 274ms

# Expertise effect size — musicians vs non-musicians
# Source: Mischler et al. 2025, d = 0.32 (long context advantage)
EXPERTISE_D: float = 0.32


class HMCE(Relay):
    """Hierarchical Musical Context Encoding — STU Relay (Depth 0, 13D).

    Transforms raw R³ spectral/rhythm features and H³ temporal demands
    into the foundational temporal context representation for the
    Sensorimotor Timing Unit.

    Models the hierarchical temporal receptive window (TRW) organization
    of auditory cortex: A1 (short) → STG (medium) → MTG (long), with
    each level encoding progressively longer temporal contexts.

    Output Structure (13D):
        E-layer  (5D) [0:5]:   Context levels + gradient + expertise
        M-layer  (2D) [5:7]:   Context depth, gradient index
        P-layer  (3D) [7:10]:  Regional encoding (A1, STG, MTG)
        F-layer  (3D) [10:13]: Context/phrase/structure predictions
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "HMCE"
    FULL_NAME = "Hierarchical Musical Context Encoding"
    UNIT = "STU"

    # ------------------------------------------------------------------
    # Output structure — 13D: E(5) + M(2) + P(3) + F(3)
    # ------------------------------------------------------------------

    OUTPUT_DIM = 13

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=5,
            dim_names=(
                "short_context",         # A1 onset detection (~74ms)
                "medium_context",        # STG energy patterns (~136ms)
                "long_context",          # MTG structural patterns (~274ms)
                "gradient",              # Anatomical gradient (r=0.99)
                "expertise",             # Musician advantage (d=0.32)
            ),
            scope="internal",
        ),
        LayerSpec(
            code="M", name="Meta", start=5, end=7,
            dim_names=(
                "context_depth",         # Weighted depth: (1×s + 2×m + 3×l)/6
                "gradient_index",        # Same as gradient (external alias)
            ),
            scope="external",
        ),
        LayerSpec(
            code="P", name="Present", start=7, end=10,
            dim_names=(
                "a1_encoding",           # Primary auditory cortex activity
                "stg_encoding",          # Superior temporal gyrus activity
                "mtg_encoding",          # Middle temporal gyrus activity
            ),
            scope="external",
        ),
        LayerSpec(
            code="F", name="Future", start=10, end=13,
            dim_names=(
                "context_prediction",    # Next context state prediction
                "phrase_expect",         # Phrase boundary expectation
                "structure_predict",     # Large-scale structural prediction
            ),
            scope="hybrid",
        ),
    )

    # ------------------------------------------------------------------
    # R³ feature indices consumed (11 scalar features)
    # ------------------------------------------------------------------

    # Energy group B [7:12]
    _R3_AMPLITUDE = 7
    _R3_LOUDNESS = 10
    _R3_ONSET_STRENGTH = 11

    # Change group D [21:25]
    _R3_SPECTRAL_FLUX = 21
    _R3_DISTRIBUTION_ENTROPY = 22
    _R3_DISTRIBUTION_FLATNESS = 23
    _R3_DISTRIBUTION_CONCENTRATION = 24

    # Rhythm group G [41:51]
    _R3_TEMPO_ESTIMATE = 41
    _R3_BEAT_STRENGTH = 42         # replaces dissolved x_l0l5
    _R3_SYNCOPATION_INDEX = 44

    # Harmony group H [51:63]
    _R3_TONAL_STABILITY = 60       # replaces dissolved x_l4l5

    # ------------------------------------------------------------------
    _VELOCITY_GAIN: float = 5.0
    _EPS: float = 1e-8

    # ------------------------------------------------------------------
    # H³ temporal demands — 18 tuples, ALL L0 (memory = causal lookback)
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """18 temporal demands at three hierarchical context levels.

        Short  (H8 = 300ms):  5 tuples — onset/spectral features
        Medium (H14):         6 tuples — energy/distribution patterns
        Long   (H20):         7 tuples — structural/tonal patterns
        """
        return (
            # ═══════════════════════════════════════════════════════════
            # SHORT CONTEXT (H8 = 300ms) — A1 onset detection, 5 tuples
            # ═══════════════════════════════════════════════════════════

            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=8, horizon_label="300ms beat",
                morph=0, morph_name="value",
                law=0, law_name="memory",
                purpose="Spectral onset value at A1 timescale",
                citation="Mischler et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=8, horizon_label="300ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean spectral onset at A1 timescale",
                citation="Mischler et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=8, horizon_label="300ms beat",
                morph=0, morph_name="value",
                law=0, law_name="memory",
                purpose="Onset detection strength at A1 timescale",
                citation="Potes et al. 2012",
            ),
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=8, horizon_label="300ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean onset strength at A1 timescale",
                citation="Potes et al. 2012",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=8, horizon_label="300ms beat",
                morph=8, morph_name="velocity",
                law=0, law_name="memory",
                purpose="Spectral onset velocity — tempo dynamics at A1",
                citation="Bellier et al. 2023",
            ),

            # ═══════════════════════════════════════════════════════════
            # MEDIUM CONTEXT (H14) — STG energy patterns, 6 tuples
            # ═══════════════════════════════════════════════════════════

            H3DemandSpec(
                r3_idx=22, r3_name="distribution_entropy",
                horizon=14, horizon_label="H14 phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Spectral entropy — energy distribution at STG scale",
                citation="Golesorkhi et al. 2021",
            ),
            H3DemandSpec(
                r3_idx=22, r3_name="distribution_entropy",
                horizon=14, horizon_label="H14 phrase",
                morph=14, morph_name="periodicity",
                law=0, law_name="memory",
                purpose="Entropy periodicity — rhythmic spectral patterns",
                citation="Wöhrle et al. 2024",
            ),
            H3DemandSpec(
                r3_idx=23, r3_name="distribution_flatness",
                horizon=14, horizon_label="H14 phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Spectral flatness — tonal vs noise balance",
                citation="Golesorkhi et al. 2021",
            ),
            H3DemandSpec(
                r3_idx=23, r3_name="distribution_flatness",
                horizon=14, horizon_label="H14 phrase",
                morph=3, morph_name="skewness",
                law=0, law_name="memory",
                purpose="Flatness skewness — spectral asymmetry at STG",
                citation="Bellier et al. 2023",
            ),
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=14, horizon_label="H14 phrase",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Amplitude trend — energy direction at STG scale",
                citation="Mischler et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=14, horizon_label="H14 phrase",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean loudness at STG timescale",
                citation="Ye et al. 2025",
            ),

            # ═══════════════════════════════════════════════════════════
            # LONG CONTEXT (H20) — MTG structural patterns, 7 tuples
            # ═══════════════════════════════════════════════════════════

            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=20, horizon_label="H20 section",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean beat strength at MTG timescale (replaces x_l0l5)",
                citation="Bonetti et al. 2024",
            ),
            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=20, horizon_label="H20 section",
                morph=14, morph_name="periodicity",
                law=0, law_name="memory",
                purpose="Beat periodicity at section level — rhythmic structure",
                citation="Bonetti et al. 2024",
            ),
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=20, horizon_label="H20 section",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Mean tonal stability at MTG (replaces x_l4l5)",
                citation="Mischler et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=20, horizon_label="H20 section",
                morph=20, morph_name="entropy",
                law=0, law_name="memory",
                purpose="Tonal entropy — harmonic unpredictability at section",
                citation="Fedorenko et al. 2012",
            ),
            H3DemandSpec(
                r3_idx=60, r3_name="tonal_stability",
                horizon=20, horizon_label="H20 section",
                morph=2, morph_name="std",
                law=0, law_name="memory",
                purpose="Tonal variability — harmonic change at section",
                citation="Kim et al. 2021",
            ),
            H3DemandSpec(
                r3_idx=42, r3_name="beat_strength",
                horizon=20, horizon_label="H20 section",
                morph=20, morph_name="entropy",
                law=0, law_name="memory",
                purpose="Beat entropy — rhythmic complexity at section",
                citation="Wöhrle et al. 2024",
            ),
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=20, horizon_label="H20 section",
                morph=18, morph_name="trend",
                law=0, law_name="memory",
                purpose="Loudness trend at section scale — dynamic arc",
                citation="Honey et al. 2012",
            ),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "short_context", "medium_context", "long_context",
            "gradient", "expertise",
            "context_depth", "gradient_index",
            "a1_encoding", "stg_encoding", "mtg_encoding",
            "context_prediction", "phrase_expect", "structure_predict",
        )

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        return (
            RegionLink(dim_name="short_context", region="A1_HG",
                       weight=0.9, citation="Mischler et al. 2025"),
            RegionLink(dim_name="a1_encoding", region="A1_HG",
                       weight=0.85, citation="Potes et al. 2012"),
            RegionLink(dim_name="medium_context", region="STG_posterior",
                       weight=0.85, citation="Bellier et al. 2023"),
            RegionLink(dim_name="stg_encoding", region="STG_posterior",
                       weight=0.8, citation="Foo et al. 2016"),
            RegionLink(dim_name="long_context", region="MTG",
                       weight=0.8, citation="Hasson et al. 2008"),
            RegionLink(dim_name="mtg_encoding", region="MTG",
                       weight=0.75, citation="Honey et al. 2012"),
            RegionLink(dim_name="structure_predict", region="IFG",
                       weight=0.6, citation="Fedorenko et al. 2012"),
            RegionLink(dim_name="context_prediction", region="Hippocampus",
                       weight=0.5, citation="Bonetti et al. 2024"),
            RegionLink(dim_name="gradient_index", region="ACC",
                       weight=0.4, citation="Bonetti et al. 2024"),
        )

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        return (
            NeuroLink(dim_name="context_prediction", channel=0,  # DA
                      effect="produce", weight=0.3,
                      citation="Bonetti et al. 2024"),
            NeuroLink(dim_name="structure_predict", channel=3,  # 5HT
                      effect="amplify", weight=0.2,
                      citation="Honey et al. 2012"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Mischler", 2025,
                         "Hierarchical temporal encoding gradient r=0.99 (6 sites), "
                         "r=0.32 (189 electrodes); musician expertise d=0.32",
                         "r=0.99 site, r=0.32 electrode, d=0.32 expertise"),
                Citation("Norman-Haignere", 2022,
                         "Independent replication of frequency preference gradient "
                         "β=0.064 oct/mm in human auditory cortex",
                         "β=0.064 oct/mm"),
                Citation("Bonetti", 2024,
                         "Hierarchical AC→hippocampus→cingulate pathway for musical "
                         "prediction; BOR=2.91e-07 MEG evidence",
                         "BOR=2.91e-07, MEG"),
                Citation("Bellier", 2023,
                         "STG anterior-posterior functional dissociation F=25.09; "
                         "anterior = complex, posterior = onset",
                         "F=25.09, ECoG"),
                Citation("Potes", 2012,
                         "STG high gamma r=0.49 with onset detection, 110ms lag",
                         "r=0.49, ECoG, 110ms"),
                Citation("Golesorkhi", 2021,
                         "Temporal hierarchy effect sizes d=-0.66 to d=-2.03 across "
                         "cortical regions",
                         "d=-0.66 to -2.03"),
                Citation("Ye", 2025,
                         "3-tiered thalamocortical temporal hierarchy r=0.93",
                         "r=0.93, fMRI"),
                Citation("Wohrle", 2024,
                         "Context accumulation in auditory cortex eta2p=0.101",
                         "eta2p=0.101"),
                Citation("Foo", 2016,
                         "Anterior STG dissonance-selective; posterior non-selective. "
                         "Chi2=8.6 anterior sensitivity",
                         "chi2=8.6, ECoG"),
                Citation("Briley", 2013,
                         "Medial-anterolateral shift for complex pitch F=29.865; "
                         "7-8mm gradient",
                         "F=29.865, EEG"),
                Citation("Fedorenko", 2012,
                         "IFG activation for musical structure processing; "
                         "shared with language syntactic processing",
                         "fMRI, structure > scrambled"),
                Citation("Kim", 2021,
                         "IFG vs STG dissociation for musical syntax F=12.37",
                         "F=12.37, fMRI"),
                Citation("Sabat", 2025,
                         "CONSTRAINT: 15-150ms windows invariant to context; "
                         "gradient may be hardwired not adaptive",
                         "15-150ms invariant window"),
                Citation("Hasson", 2008,
                         "Foundational TRW hierarchy in cortex: posterior=short, "
                         "anterior=long temporal receptive windows",
                         "foundational theory"),
                Citation("Honey", 2012,
                         "Slow cortical dynamics track narrative structure at "
                         "multiple timescales",
                         "fMRI, narrative timescales"),
            ),
            evidence_tier="alpha",
            confidence_range=(0.88, 0.94),
            falsification_criteria=(
                "Non-musician encoding at long context should be reduced "
                "(CONFIRMED: Mischler 2025, d=0.32)",
                "Anatomical gradient should hold across stimulus types "
                "(CONFIRMED: Norman-Haignere 2022 independent replication)",
                "Integration windows may be invariant to context length "
                "(CHALLENGED: Sabat 2025, 15-150ms constant)",
                "Anterior-posterior STG gradient for complexity "
                "(CONFIRMED: Foo 2016, Bellier 2023)",
            ),
            version="3.0.0",
            paper_count=15,
        )

    # ------------------------------------------------------------------
    # compute() — hierarchical temporal encoding
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Hierarchical context encoding: A1 → STG → MTG gradient.

        Three context levels model the temporal receptive window hierarchy:
        A1 encodes onsets (short), STG encodes patterns (medium),
        MTG encodes structure (long).

        Args:
            h3_features: Dict mapping (r3_idx, h, m, l) to (B, T) tensors.
            r3_features: (B, T, 97) R³ features.

        Returns:
            (B, T, 13) output.
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # === R³ features (11) ===
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]
        loudness       = r3_features[:, :, self._R3_LOUDNESS]
        onset_strength = r3_features[:, :, self._R3_ONSET_STRENGTH]
        spectral_flux  = r3_features[:, :, self._R3_SPECTRAL_FLUX]
        dist_entropy   = r3_features[:, :, self._R3_DISTRIBUTION_ENTROPY]
        dist_flatness  = r3_features[:, :, self._R3_DISTRIBUTION_FLATNESS]
        dist_conc      = r3_features[:, :, self._R3_DISTRIBUTION_CONCENTRATION]
        tempo_est      = r3_features[:, :, self._R3_TEMPO_ESTIMATE]
        beat_strength  = r3_features[:, :, self._R3_BEAT_STRENGTH]
        syncopation    = r3_features[:, :, self._R3_SYNCOPATION_INDEX]
        tonal_stab     = r3_features[:, :, self._R3_TONAL_STABILITY]

        _zeros = torch.zeros(B, T, device=device)
        _neutral = torch.full((B, T), 0.5, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # === H³ features (18 demands) ===

        # Short context H8 (5 tuples)
        h3_flux_val_h8   = _h3((21, 8, 0, 0), spectral_flux)
        h3_flux_mean_h8  = _h3((21, 8, 1, 0))
        h3_onset_val_h8  = _h3((11, 8, 0, 0), onset_strength)
        h3_onset_mean_h8 = _h3((11, 8, 1, 0))
        h3_flux_vel_h8   = _h3((21, 8, 8, 0))

        # Medium context H14 (6 tuples)
        h3_ent_mean_h14   = _h3((22, 14, 1, 0))
        h3_ent_period_h14 = _h3((22, 14, 14, 0))
        h3_flat_mean_h14  = _h3((23, 14, 1, 0))
        h3_flat_skew_h14  = _h3((23, 14, 3, 0))
        h3_amp_trend_h14  = _h3((7, 14, 18, 0), _neutral)
        h3_loud_mean_h14  = _h3((10, 14, 1, 0))

        # Long context H20 (7 tuples)
        h3_beat_mean_h20   = _h3((42, 20, 1, 0))
        h3_beat_period_h20 = _h3((42, 20, 14, 0))
        h3_tonal_mean_h20  = _h3((60, 20, 1, 0))
        h3_tonal_ent_h20   = _h3((60, 20, 20, 0))
        h3_tonal_std_h20   = _h3((60, 20, 2, 0))
        h3_beat_ent_h20    = _h3((42, 20, 20, 0))
        h3_loud_trend_h20  = _h3((10, 20, 18, 0), _neutral)

        # Velocity normalization
        flux_vel_norm = (h3_flux_vel_h8 * self._VELOCITY_GAIN).abs().clamp(0.0, 1.0)

        # === E-LAYER (5D) ===

        # f01: Short context — A1 onset detection (τ ≈ 74ms)
        short_context = (
            0.25 * h3_flux_val_h8
            + 0.25 * h3_flux_mean_h8
            + 0.20 * h3_onset_val_h8
            + 0.15 * h3_onset_mean_h8
            + 0.15 * flux_vel_norm
        ).clamp(0.0, 1.0)

        # f02: Medium context — STG energy patterns (τ ≈ 136ms)
        medium_context = (
            0.20 * h3_ent_mean_h14
            + 0.20 * h3_loud_mean_h14
            + 0.20 * h3_flat_mean_h14
            + 0.15 * h3_ent_period_h14
            + 0.15 * h3_amp_trend_h14
            + 0.10 * dist_conc
        ).clamp(0.0, 1.0)

        # f03: Long context — MTG structural patterns (τ ≈ 274ms)
        long_context = (
            0.20 * h3_beat_mean_h20
            + 0.20 * h3_tonal_mean_h20
            + 0.15 * h3_beat_period_h20
            + 0.15 * h3_tonal_ent_h20
            + 0.15 * h3_loud_trend_h20
            + 0.15 * syncopation
        ).clamp(0.0, 1.0)

        # f04: Gradient — anatomical posterior-anterior gradient (r=0.99)
        gradient = (short_context + medium_context + long_context) / 3.0

        # f05: Expertise — musician advantage in long context (d=0.32)
        expertise = (
            EXPERTISE_D * long_context * h3_tonal_mean_h20
        ).clamp(0.0, 1.0)

        # === M-LAYER (2D) ===
        context_depth = (
            1.0 * short_context + 2.0 * medium_context + 3.0 * long_context
        ) / 6.0
        gradient_index = gradient

        # === P-LAYER (3D) — Regional encoding ===
        a1_encoding = (
            short_context * (0.6 * h3_onset_val_h8 + 0.4 * onset_strength)
        ).clamp(0.0, 1.0)

        stg_encoding = (
            medium_context * (0.5 * h3_loud_mean_h14 + 0.5 * dist_entropy)
        ).clamp(0.0, 1.0)

        mtg_encoding = (
            long_context * (0.5 * h3_tonal_mean_h20 + 0.5 * h3_beat_mean_h20)
        ).clamp(0.0, 1.0)

        # === F-LAYER (3D) — Predictions ===
        context_prediction = (
            0.40 * gradient
            + 0.30 * h3_ent_period_h14
            + 0.30 * tempo_est
        ).clamp(0.0, 1.0)

        phrase_expect = (
            0.35 * h3_flat_skew_h14
            + 0.35 * h3_tonal_std_h20
            + 0.30 * beat_strength
        ).clamp(0.0, 1.0)

        structure_predict = (
            0.30 * long_context
            + 0.25 * h3_beat_ent_h20
            + 0.25 * h3_tonal_ent_h20
            + 0.20 * h3_beat_period_h20
        ).clamp(0.0, 1.0)

        return torch.stack([
            short_context, medium_context, long_context, gradient, expertise,
            context_depth, gradient_index,
            a1_encoding, stg_encoding, mtg_encoding,
            context_prediction, phrase_expect, structure_predict,
        ], dim=-1)
