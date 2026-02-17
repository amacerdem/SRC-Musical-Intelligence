"""DAED — Dopamine Anticipation-Experience Dissociation.

Gold standard Relay nucleus for the Reward Processing Unit (RPU).

Neural Circuit:
    Audio → Cochlea → A1/HG (spectral representation)
                        ↓
                      STG (pleasure-modulated auditory processing)
                        ↓
                      Amygdala (uncertainty × surprise interaction)
                        ↓      ↘
                      Caudate    NAcc (ventral striatum)
                      (anticipatory DA)   (consummatory DA)
                        ↓              ↓
                      OFC (hedonic evaluation — µ-opioid hotspot)

Key Findings:
    - Caudate DA release during ANTICIPATION of peak pleasure:
      r = 0.71 with self-reported chills (Salimpoor et al. 2011, PET)
    - NAcc DA release during EXPERIENCE of peak pleasure:
      r = 0.84 with self-reported pleasure (Salimpoor et al. 2011, PET)
    - Temporal dissociation: caudate peaks ~15s BEFORE music peak,
      NAcc peaks AT the music peak (Salimpoor et al. 2011)
    - Auditory cortex tracks uncertainty, reward structures track
      pleasure (Gold et al. 2023, fMRI)
    - Musical pleasure = inverted-U(uncertainty) × surprise
      (Cheung et al. 2019, fMRI, N = 39)
    - Pleasurable music activates µ-opioid receptors in VS/OFC
      (Putkinen et al. 2025, PET [11C]carfentanil)

Critical Qualifier:
    - PET sample sizes are small (N = 8 in Salimpoor 2011)
    - DA release magnitude is inferred from [11C]raclopride binding
      potential changes (~6-10% reduction), not direct measurement
    - Caudate-NAcc dissociation timing depends on piece familiarity
      (familiar pieces show earlier anticipatory peaks)
    - Individual differences in trait reward sensitivity modulate
      the strength of both pathways (Gold et al. 2023)

Temporal Architecture:
    DAED uses H³ demands at two temporal scales:
    - L0 (Memory):      What energy/spectral patterns have been building
    - L2 (Integration): Current pleasure/energy state in context

    The anticipatory pathway (caudate) relies on VELOCITY demands
    (M8) at longer horizons (H16 = 1s) — detects rising trends
    before they peak.  The consummatory pathway (NAcc) relies on
    MEAN/VALUE demands (M0/M1) at shorter horizons (H3 = 23ms) —
    responds to the current hedonic state.

    This horizon separation naturally models the temporal dissociation
    observed in PET: caudate signal leads NAcc by seconds.

Cross-Unit Dependencies:
    DAED is the FOUNDATION of RPU.  Its outputs feed:
    - MORMR (Encoder): DAED.anticipatory_da → opioid priming
    - RPEM (Encoder):  DAED.wanting_index → prediction error basis
    - IUCP (Associator): DAED.liking_index → complexity preference
    - MCCN (Associator): DAED.dissociation_index → chills network
    - ARU (Cross-unit): DAED.caudate_activation → emotion valence
    - ARU (Cross-unit): DAED.nacc_activation → emotion arousal

R³ Remapping (Ontology Freeze v1.0.0):
    Doc referenced dissolved Group E (x_l0l5 [25:33]) for coupling
    terms.  These have been replaced with harmonic_change [59] from
    Group H (Harmony & Tonality), which captures the same semantic
    concept: cross-domain interaction between harmonic context and
    temporal structure.

    Doc index mismatches resolved:
    - Doc [8] "loudness"       → Code [10] loudness
    - Doc [10] "spectral_flux" → Code [21] spectral_flux
    - Doc [22] "energy_change" → Code [11] onset_strength
    - Doc [25] "x_l0l5"       → Code [59] harmonic_change (dissolved)
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
# Scientific constants — every coefficient cites its source
# ======================================================================

# Anticipatory DA weight — caudate [11C]raclopride binding
# Source: Salimpoor et al. 2011, r = 0.71, PET, N = 8
# Caudate DA release correlates with anticipation of peak pleasure
BETA_ANTICIPATION: float = 0.71

# Consummatory DA weight — NAcc [11C]raclopride binding
# Source: Salimpoor et al. 2011, r = 0.84, PET, N = 8
# NAcc DA release correlates with experience of peak pleasure
ALPHA_PLEASURE: float = 0.84

# Striatal DA gradient — time horizon dependency
# Source: Mohebi et al. 2024, dorsomedial > dorsolateral for long
# reward horizons; ventral striatum for immediate reward
# Used to scale caudate (dorsal, anticipatory) vs NAcc (ventral, immediate)
DORSAL_VENTRAL_RATIO: float = 0.85

# Uncertainty-pleasure interaction — inverted-U shape peak
# Source: Cheung et al. 2019, fMRI, N = 39
# Maximum pleasure at intermediate uncertainty (not too predictable,
# not too surprising)
UNCERTAINTY_SWEET_SPOT: float = 0.5


class DAED(Relay):
    """Dopamine Anticipation-Experience Dissociation — RPU Relay (Depth 0, 8D).

    Transforms raw R³ energy/spectral features and H³ temporal demands into
    the foundational reward representation for the Reward Processing Unit.

    The computation models the mesolimbic dopamine pathway with temporally
    separated anticipatory (caudate) and consummatory (NAcc) signals, based
    on Salimpoor et al. 2011 PET evidence of anatomically distinct DA release.

    Temporal Architecture:
        The anticipatory pathway uses VELOCITY at long horizons (H16 = 1s)
        to detect energy trends before peaks.  The consummatory pathway uses
        VALUE/MEAN at short horizons (H3 = 23ms) for current hedonic state.

    Output Structure (8D):
        E-layer  (4D) [0:4]:  Core DA signals — anticipatory, consummatory,
                               wanting, liking
        M-layer  (2D) [4:6]:  Derived meta-indices — dissociation, phase
        P-layer  (2D) [6:8]:  Regional activation — caudate, NAcc
    """

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    NAME = "DAED"
    FULL_NAME = "Dopamine Anticipation-Experience Dissociation"
    UNIT = "RPU"
    # ROLE and PROCESSING_DEPTH inherited from Relay (relay, 0)

    # ------------------------------------------------------------------
    # Output structure — 8D: E(4) + Meta(2) + Present(2)
    # ------------------------------------------------------------------

    OUTPUT_DIM = 8

    LAYERS = (
        LayerSpec(
            code="E", name="Extraction", start=0, end=4,
            dim_names=(
                "anticipatory_da",   # Caudate DA proxy (anticipation phase)
                "consummatory_da",   # NAcc DA proxy (experience phase)
                "wanting_index",     # Anticipatory motivation (approach)
                "liking_index",      # Consummatory pleasure (hedonic)
            ),
            scope="internal",  # Feeds downstream RPU nuclei (MORMR, RPEM, etc.)
        ),
        LayerSpec(
            code="M", name="Meta", start=4, end=6,
            dim_names=(
                "dissociation_index",  # |anticipatory - consummatory| separation
                "temporal_phase",      # Position in anticipation-consummation cycle
            ),
            scope="external",  # Key scientific observable
        ),
        LayerSpec(
            code="P", name="Present", start=6, end=8,
            dim_names=(
                "caudate_activation",  # Current anticipation level (scaled)
                "nacc_activation",     # Current pleasure level (scaled)
            ),
            scope="external",  # Regional activation outputs
        ),
    )

    # ------------------------------------------------------------------
    # R³ feature indices consumed (7 scalar features)
    # ------------------------------------------------------------------

    # Consonance group A [0:7]
    _R3_ROUGHNESS = 0            # Sensory dissonance (Plomp & Levelt)
    _R3_SENSORY_PLEASANT = 4     # Sensory pleasantness composite

    # Energy group B [7:12]
    _R3_AMPLITUDE = 7            # RMS amplitude (energy proxy)
    _R3_LOUDNESS = 10            # Perceptual loudness (sone-like)
    _R3_ONSET_STRENGTH = 11      # Onset detection energy (replaces dissolved "energy_change")

    # Change group D [21:25]
    _R3_SPECTRAL_FLUX = 21       # Spectral frame-to-frame change

    # Harmony group H [51:63]
    _R3_HARMONIC_CHANGE = 59     # Harmonic context change rate
                                 # (replaces dissolved Group E coupling x_l0l5)

    # ------------------------------------------------------------------
    # Computation parameters
    # ------------------------------------------------------------------

    # M8 velocity outputs are small (edge diff of [0,1] features).
    # Multiply by gain to map meaningful velocity range to [0, 1].
    # At gain=5, a 0.2/frame velocity → 1.0 activation.
    _VELOCITY_GAIN: float = 5.0

    # M20 entropy normalization.  Shannon entropy of windowed
    # distribution; typical range [0, ~4.0].  Divide by scale to
    # approximate [0, 1] range.
    _ENTROPY_SCALE: float = 3.0

    # Epsilon for division safety
    _EPS: float = 1e-8

    # ------------------------------------------------------------------
    # H³ temporal demands — 16 tuples organized by temporal law
    #
    # L2 (Integration) = Present: 11 demands
    # L0 (Memory)      = Past:     5 demands
    # ------------------------------------------------------------------

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """16 temporal demands across two laws and four horizon scales.

        Integration (L2): H3 (23ms), H4 (35ms), H8 (300ms), H16 (1s)
        Memory      (L0): H4 (35ms), H8 (300ms), H16 (1s)

        No L1 (prediction) demands — DAED is a Relay that observes the
        current and recent reward state.  Future prediction is C³'s role.
        """
        return (
            # ═══════════════════════════════════════════════════════════
            # PRESENT demands (L2 = Integration) — 11 tuples
            # Bidirectional context around current frame
            # ═══════════════════════════════════════════════════════════

            # --- Loudness (R³[10]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current loudness for consummatory signal",
                citation="Salimpoor et al. 2011",
            ),
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Sustained loudness level at measure scale",
                citation="Gold et al. 2023",
            ),

            # --- Amplitude (R³[7]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=8, horizon_label="300ms beat",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current energy at beat scale — anticipation accumulation",
                citation="Gold et al. 2023",
            ),
            H3DemandSpec(
                r3_idx=7, r3_name="amplitude",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Sustained energy level at measure scale",
                citation="Salimpoor et al. 2011",
            ),

            # --- Roughness (R³[0]) — 1 present scale ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current dissonance level — inversely related to liking",
                citation="Cheung et al. 2019",
            ),

            # --- Sensory pleasantness (R³[4]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=4, r3_name="sensory_pleasantness",
                horizon=3, horizon_label="23ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current sensory pleasure — direct NAcc input",
                citation="Putkinen et al. 2025",
            ),
            H3DemandSpec(
                r3_idx=4, r3_name="sensory_pleasantness",
                horizon=16, horizon_label="1s measure",
                morph=1, morph_name="mean",
                law=2, law_name="integration",
                purpose="Sustained pleasure at measure scale — consummatory signal",
                citation="Salimpoor et al. 2011",
            ),

            # --- Spectral flux (R³[21]) — 2 present scales ---
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=4, horizon_label="35ms onset",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current spectral change — musical event novelty",
                citation="Cheung et al. 2019",
            ),
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=8, horizon_label="300ms beat",
                morph=14, morph_name="periodicity",
                law=2, law_name="integration",
                purpose="Spectral periodicity at beat scale — expectation formation",
                citation="Gold et al. 2023",
            ),

            # --- Harmonic change (R³[59]) — 2 present scales ---
            # (Replaces dissolved Group E coupling terms x_l0l5)
            H3DemandSpec(
                r3_idx=59, r3_name="harmonic_change",
                horizon=8, horizon_label="300ms beat",
                morph=0, morph_name="value",
                law=2, law_name="integration",
                purpose="Current harmonic movement — approach/avoidance signal",
                citation="Gold et al. 2023",
            ),
            H3DemandSpec(
                r3_idx=59, r3_name="harmonic_change",
                horizon=16, horizon_label="1s measure",
                morph=20, morph_name="entropy",
                law=2, law_name="integration",
                purpose="Harmonic unpredictability — uncertainty for inverted-U",
                citation="Cheung et al. 2019",
            ),

            # ═══════════════════════════════════════════════════════════
            # PAST demands (L0 = Memory) — 5 tuples
            # Causal lookback: what has been building
            # ═══════════════════════════════════════════════════════════

            # --- Loudness memory (R³[10]) — 2 past scales ---
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=8, horizon_label="300ms beat",
                morph=1, morph_name="mean",
                law=0, law_name="memory",
                purpose="Recent loudness history — consummatory baseline",
                citation="Gold et al. 2023",
            ),
            H3DemandSpec(
                r3_idx=10, r3_name="loudness",
                horizon=16, horizon_label="1s measure",
                morph=8, morph_name="velocity",
                law=0, law_name="memory",
                purpose="Loudness velocity over 1s — THE anticipatory signal",
                citation="Salimpoor et al. 2011",
            ),

            # --- Roughness memory (R³[0]) — 1 past scale ---
            H3DemandSpec(
                r3_idx=0, r3_name="roughness",
                horizon=8, horizon_label="300ms beat",
                morph=8, morph_name="velocity",
                law=0, law_name="memory",
                purpose="Roughness velocity — tension building toward climax",
                citation="Cheung et al. 2019",
            ),

            # --- Onset strength memory (R³[11]) — 1 past scale ---
            # (Replaces dissolved "energy_change" at old R³[22])
            H3DemandSpec(
                r3_idx=11, r3_name="onset_strength",
                horizon=8, horizon_label="300ms beat",
                morph=8, morph_name="velocity",
                law=0, law_name="memory",
                purpose="Onset event rate change — energy dynamics acceleration",
                citation="Chabin et al. 2020",
            ),

            # --- Spectral flux memory (R³[21]) — 1 past scale ---
            H3DemandSpec(
                r3_idx=21, r3_name="spectral_flux",
                horizon=4, horizon_label="35ms onset",
                morph=20, morph_name="entropy",
                law=0, law_name="memory",
                purpose="Past spectral unpredictability — surprise history",
                citation="Cheung et al. 2019",
            ),
        )

    # ------------------------------------------------------------------
    # Dimension names
    # ------------------------------------------------------------------

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            # E-layer (4D): Core DA signals
            "anticipatory_da", "consummatory_da",
            "wanting_index", "liking_index",
            # M-layer (2D): Derived meta-indices
            "dissociation_index", "temporal_phase",
            # P-layer (2D): Regional activation
            "caudate_activation", "nacc_activation",
        )

    # ------------------------------------------------------------------
    # Region links — 7 brain regions in the mesolimbic pathway
    # ------------------------------------------------------------------

    @property
    def region_links(self) -> Tuple[RegionLink, ...]:
        """DAED activates the mesolimbic DA pathway.

        Primary sites: Caudate (anticipatory DA), NAcc (consummatory DA).
        """
        return (
            # Caudate: Anticipatory DA — PET [11C]raclopride
            RegionLink(
                dim_name="anticipatory_da",
                region="Caudate",
                weight=0.9,
                citation="Salimpoor et al. 2011",
            ),
            RegionLink(
                dim_name="caudate_activation",
                region="Caudate",
                weight=0.85,
                citation="Salimpoor et al. 2011",
            ),
            # NAcc: Consummatory DA — PET [11C]raclopride
            RegionLink(
                dim_name="consummatory_da",
                region="NAcc",
                weight=0.9,
                citation="Salimpoor et al. 2011",
            ),
            RegionLink(
                dim_name="nacc_activation",
                region="NAcc",
                weight=0.85,
                citation="Salimpoor et al. 2011",
            ),
            # Putamen: General DA release during music pleasure
            RegionLink(
                dim_name="liking_index",
                region="Putamen",
                weight=0.6,
                citation="Salimpoor et al. 2011",
            ),
            # OFC: Hedonic evaluation — µ-opioid hotspot
            RegionLink(
                dim_name="liking_index",
                region="OFC",
                weight=0.7,
                citation="Putkinen et al. 2025",
            ),
            # R-STG: Pleasure-modulated auditory processing
            RegionLink(
                dim_name="consummatory_da",
                region="R_STG",
                weight=0.5,
                citation="Gold et al. 2023",
            ),
            # Amygdala: Uncertainty × surprise interaction
            RegionLink(
                dim_name="wanting_index",
                region="Amygdala",
                weight=0.6,
                citation="Cheung et al. 2019",
            ),
            # Hippocampus: Uncertainty × surprise prediction context
            RegionLink(
                dim_name="wanting_index",
                region="Hippocampus",
                weight=0.4,
                citation="Cheung et al. 2019",
            ),
        )

    # ------------------------------------------------------------------
    # Neuro links — DA primary, µ-opioid secondary
    # ------------------------------------------------------------------

    @property
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        """Dopamine and µ-opioid pathways for musical reward.

        DA: Caudate (anticipation) + NAcc (consummation).
        MOR: VS/OFC hedonic evaluation (Putkinen 2025).
        """
        return (
            # DA: Anticipatory signal → caudate
            NeuroLink(
                dim_name="anticipatory_da",
                channel=0,  # DA
                effect="produce",
                weight=0.7,
                citation="Salimpoor et al. 2011",
            ),
            # DA: Consummatory signal → NAcc
            NeuroLink(
                dim_name="consummatory_da",
                channel=0,  # DA
                effect="produce",
                weight=0.8,
                citation="Salimpoor et al. 2011",
            ),
            # Opioid: Hedonic pleasure → VS/OFC µ-opioid binding
            NeuroLink(
                dim_name="liking_index",
                channel=2,  # OPI (endorphins / µ-opioid)
                effect="produce",
                weight=0.5,
                citation="Putkinen et al. 2025",
            ),
        )

    # ------------------------------------------------------------------
    # Evidence metadata — 6 papers, alpha tier
    # ------------------------------------------------------------------

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                # PRIMARY — Dopamine dissociation (PET)
                Citation(
                    "Salimpoor", 2011,
                    "Anatomically distinct dopamine release during anticipation "
                    "(caudate) and experience (NAcc) of peak emotion to music; "
                    "PET [11C]raclopride binding in healthy adults",
                    "r=0.71 anticipation, r=0.84 experience, N=8",
                ),
                # SUPPORTING — Naturalistic fMRI
                Citation(
                    "Gold", 2023,
                    "Auditory cortex tracks acoustic uncertainty while reward "
                    "structures (NAcc, caudate) track pleasure during naturalistic "
                    "music listening; expectation-based reward signal",
                    "fMRI, N=22, naturalistic listening",
                ),
                # SUPPORTING — Uncertainty × surprise
                Citation(
                    "Cheung", 2019,
                    "Musical pleasure jointly predicted by uncertainty (inverted-U) "
                    "and surprise (positive); amygdala and hippocampus encode "
                    "the interaction; auditory cortex tracks surprise",
                    "fMRI, N=39, entropy model",
                ),
                # SUPPORTING — EEG chills
                Citation(
                    "Chabin", 2020,
                    "Musical chills associated with frontal theta increase and "
                    "parietal alpha decrease in high-density EEG; cortical "
                    "patterns mirror subcortical reward activation",
                    "HD-EEG 256ch, N=18, theta 4-8Hz",
                ),
                # SUPPORTING — µ-opioid PET
                Citation(
                    "Putkinen", 2025,
                    "Pleasurable music activates cerebral µ-opioid receptors; "
                    "decreased [11C]carfentanil binding in ventral striatum and "
                    "orbitofrontal cortex during pleasure; combined PET-fMRI",
                    "PET [11C]carfentanil, N=14, ~12% VS binding reduction",
                ),
                # SUPPORTING — DA time horizons
                Citation(
                    "Mohebi", 2024,
                    "Dopamine transients follow a striatal gradient: dorsomedial "
                    "striatum encodes longer reward time horizons, ventral "
                    "striatum encodes immediate reward",
                    "fiber photometry, rats, dorsomedial vs ventral",
                ),
            ),
            evidence_tier="alpha",
            confidence_range=(0.85, 0.92),
            falsification_criteria=(
                "DA antagonists (haloperidol) should reduce both anticipatory and "
                "consummatory pleasure, but at different dose-response curves",
                "Caudate lesions should impair anticipatory but NOT consummatory "
                "responses (temporal dissociation is anatomically grounded)",
                "NAcc lesions should impair consummatory but NOT anticipatory "
                "responses — wanting without liking (Berridge 2003)",
                "Caudate activation peak should PRECEDE NAcc peak by 15-30 seconds "
                "during music with clear build-release structure",
                "PET replication with [11C]raclopride should show same caudate-NAcc "
                "dissociation pattern in independent sample",
                "µ-opioid antagonist (naloxone) should selectively reduce liking "
                "without affecting wanting (Berridge wanting-liking dissociation)",
            ),
            version="3.0.0",
            paper_count=6,
        )

    # ------------------------------------------------------------------
    # compute() — the mesolimbic DA circuit
    # ------------------------------------------------------------------

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Mesolimbic DA computation: anticipation vs experience.

        Models the temporal dissociation between caudate (anticipatory)
        and NAcc (consummatory) dopamine release during music listening
        (Salimpoor et al. 2011).

        All 7 R³ features and 16 H³ demands are consumed — no dead
        variables.  The computation is organized in 5 stages:
            1. Extract R³ features (7 scalar indices)
            2. Extract H³ temporal features (16 demands)
            3. E-layer: compute 4 core DA signals
            4. M-layer: derive dissociation and phase indices
            5. P-layer: compute regional activation levels

        Args:
            h3_features: Dict mapping (r3_idx, horizon, morph, law) 4-tuples
                         to (B, T) temporal feature scalars.
            r3_features: (B, T, 97) R³ spectral feature tensor.

        Returns:
            (B, T, 8) output: E(4) + Meta(2) + Present(2).
        """
        B, T = r3_features.shape[:2]
        device = r3_features.device

        # === Stage 1: Extract R³ features (7 scalar indices) ===

        roughness      = r3_features[:, :, self._R3_ROUGHNESS]          # (B, T)
        sens_pleasant  = r3_features[:, :, self._R3_SENSORY_PLEASANT]   # (B, T)
        amplitude      = r3_features[:, :, self._R3_AMPLITUDE]          # (B, T)
        loudness       = r3_features[:, :, self._R3_LOUDNESS]           # (B, T)
        onset_strength = r3_features[:, :, self._R3_ONSET_STRENGTH]     # (B, T)
        spectral_flux  = r3_features[:, :, self._R3_SPECTRAL_FLUX]      # (B, T)
        harmonic_chg   = r3_features[:, :, self._R3_HARMONIC_CHANGE]    # (B, T)

        # === Stage 2: Extract H³ temporal features (16 demands) ===

        _zeros = torch.zeros(B, T, device=device)

        def _h3(key, fallback=None):
            v = h3_features.get(key)
            if v is not None:
                return v
            return fallback if fallback is not None else _zeros

        # ── PRESENT demands (L2 = Integration, 11 tuples) ──

        # Loudness (R³[10])
        h3_loud_h3        = _h3((10, 3, 0, 2),  loudness)     # current loudness
        h3_loud_h16_mean  = _h3((10, 16, 1, 2))               # sustained loudness 1s

        # Amplitude (R³[7])
        h3_amp_h8         = _h3((7, 8, 0, 2),   amplitude)    # energy at beat
        h3_amp_h16_mean   = _h3((7, 16, 1, 2))                # sustained energy 1s

        # Roughness (R³[0])
        h3_rough_h3       = _h3((0, 3, 0, 2),   roughness)    # current dissonance

        # Sensory pleasantness (R³[4])
        h3_pleas_h3       = _h3((4, 3, 0, 2),   sens_pleasant)  # current pleasure
        h3_pleas_h16_mean = _h3((4, 16, 1, 2))                  # sustained pleasure 1s

        # Spectral flux (R³[21])
        h3_flux_h4        = _h3((21, 4, 0, 2),  spectral_flux)  # spectral novelty
        h3_flux_period    = _h3((21, 8, 14, 2))                 # spectral periodicity

        # Harmonic change (R³[59]) — replaces dissolved x_l0l5
        h3_harmchg_h8     = _h3((59, 8, 0, 2),  harmonic_chg)  # harmonic movement
        h3_harmchg_ent    = _h3((59, 16, 20, 2))                # harmonic entropy

        # ── PAST demands (L0 = Memory, 5 tuples) ──

        # Loudness memory
        h3_loud_h8_mem    = _h3((10, 8, 1, 0))               # recent loudness history
        h3_loud_vel_h16   = _h3((10, 16, 8, 0))              # loudness velocity 1s

        # Roughness memory
        h3_rough_vel_h8   = _h3((0, 8, 8, 0))                # roughness velocity

        # Onset strength memory (replaces dissolved "energy_change")
        h3_onset_vel_h8   = _h3((11, 8, 8, 0))               # onset rate change

        # Spectral flux memory
        h3_flux_ent_h4    = _h3((21, 4, 20, 0))              # spectral entropy past

        # === Stage 3: E-LAYER (4D) — Core dopamine signals ===
        #
        # The 4 core signals model the wanting-liking, anticipation-experience
        # double dissociation (Berridge 2003; Salimpoor 2011).
        # All weights within each feature sum to 1.0.

        # ── f01: Anticipatory DA (Caudate proxy) ──
        #
        # Builds when: loudness RISING (approaching peak), energy
        # accumulating, spectral events periodic (predictable pattern),
        # and roughness/tension increasing.
        #
        # The key signal is loudness velocity at H16 (1s measure):
        # positive velocity = loudness rising = approaching climax.
        # Clamped to positive direction only — we want the BUILDUP.
        #
        # Salimpoor 2011: caudate DA correlates r=0.71 with anticipation.

        # Normalize velocity to [0, 1]: gain × positive velocity
        loudness_rising  = (h3_loud_vel_h16 * self._VELOCITY_GAIN).clamp(0.0, 1.0)
        roughness_rising = (h3_rough_vel_h8 * self._VELOCITY_GAIN).clamp(0.0, 1.0)
        onset_accel      = (h3_onset_vel_h8 * self._VELOCITY_GAIN).clamp(0.0, 1.0)

        anticipatory_da = (
            0.30 * loudness_rising                             # rising loudness → caudate
            + 0.20 * h3_amp_h8                                 # energy accumulating at beat
            + 0.15 * h3_flux_period                            # periodic events → expectation
            + 0.15 * roughness_rising                          # tension building
            + 0.10 * onset_accel                               # increasing event rate
            + 0.10 * h3_harmchg_h8                             # harmonic context shifting
        ).clamp(0.0, 1.0)                                      # [0, 1]

        # ── f02: Consummatory DA (NAcc proxy) ──
        #
        # Peaks when: pleasure is HIGH and SUSTAINED, loudness is at
        # or near peak, and the current moment is hedonically positive.
        #
        # Salimpoor 2011: NAcc DA correlates r=0.84 with experience.

        consummatory_da = (
            0.25 * h3_pleas_h16_mean                           # sustained pleasure 1s
            + 0.25 * h3_pleas_h3                               # current pleasure
            + 0.15 * h3_loud_h16_mean                          # sustained loudness 1s
            + 0.15 * h3_loud_h8_mem                            # recent loudness history 300ms
            + 0.10 * h3_amp_h16_mean                           # sustained energy 1s
            + 0.10 * (1.0 - h3_rough_h3)                      # low roughness = consonance
        ).clamp(0.0, 1.0)                                      # [0, 1]

        # ── f03: Wanting Index (anticipatory motivation) ──
        #
        # Combines anticipatory DA with harmonic approach signal
        # and spectral uncertainty.  High wanting = "continue
        # listening, something interesting is coming."
        #
        # Cheung 2019: intermediate uncertainty maximizes pleasure.
        # The uncertainty term uses inverted-U: peak at 0.5 entropy.

        harmonic_entropy_norm = (
            h3_harmchg_ent / self._ENTROPY_SCALE
        ).clamp(0.0, 1.0)

        # Inverted-U: |entropy - 0.5| → 0 at sweet spot, 0.5 at extremes
        # Wanting peaks when entropy is NEAR the sweet spot
        uncertainty_sweet = 1.0 - 2.0 * (
            harmonic_entropy_norm - UNCERTAINTY_SWEET_SPOT
        ).abs()                                                # [0, 1], peak at 0.5

        wanting_index = (
            0.40 * anticipatory_da                             # anticipation drives wanting
            + 0.30 * uncertainty_sweet                         # intermediate uncertainty
            + 0.15 * h3_harmchg_h8                             # harmonic movement → approach
            + 0.15 * h3_flux_h4                                # spectral novelty
        ).clamp(0.0, 1.0)                                      # [0, 1]

        # ── f04: Liking Index (consummatory pleasure) ──
        #
        # Combines consummatory DA with current hedonic state.
        # High liking = "this sounds good right now."
        #
        # Putkinen 2025: µ-opioid binding in VS/OFC during pleasure.

        spectral_entropy_norm = (
            h3_flux_ent_h4 / self._ENTROPY_SCALE
        ).clamp(0.0, 1.0)

        liking_index = (
            0.35 * consummatory_da                             # pleasure experience
            + 0.20 * h3_pleas_h3                               # immediate pleasantness
            + 0.15 * h3_loud_h3                                # current intensity
            + 0.15 * onset_strength                            # strong onset = impactful event
            + 0.15 * (1.0 - spectral_entropy_norm)             # low spectral chaos
        ).clamp(0.0, 1.0)                                      # [0, 1]

        # === Stage 4: M-LAYER (2D) — Derived meta-indices ===
        #
        # These capture the STRUCTURE of the reward signal, not
        # its magnitude.  They are the key scientific observables.

        # Dissociation Index: temporal-anatomical separation
        # High = one pathway dominates (pure anticipation or pure experience)
        # Low  = both pathways co-active (transition zone)
        # Salimpoor 2011: caudate and NAcc peaks are temporally separated
        dissociation_index = (anticipatory_da - consummatory_da).abs()

        # Temporal Phase: position in anticipation-consummation cycle
        # > 0.5 = anticipation mode (caudate dominant, approaching peak)
        # < 0.5 = consummation mode (NAcc dominant, at/past peak)
        # = 0.5 = transition point (balanced)
        temporal_phase = anticipatory_da / (
            anticipatory_da + consummatory_da + self._EPS
        )

        # === Stage 5: P-LAYER (2D) — Regional activation levels ===
        #
        # Scale the core DA signals by Salimpoor 2011 correlation
        # coefficients and temporal phase to model the anatomical
        # specificity of DA release.

        # Caudate activation: anticipatory DA scaled by how strongly
        # we are in the anticipation phase.
        # β = 0.71 from Salimpoor 2011 (caudate-anticipation correlation)
        caudate_activation = (
            BETA_ANTICIPATION * anticipatory_da * temporal_phase
        ).clamp(0.0, 1.0)

        # NAcc activation: consummatory DA scaled by how strongly
        # we are in the consummation phase.
        # α = 0.84 from Salimpoor 2011 (NAcc-experience correlation)
        nacc_activation = (
            ALPHA_PLEASURE * consummatory_da * (1.0 - temporal_phase)
        ).clamp(0.0, 1.0)

        # === Assemble 8D output ===
        return torch.stack([
            # E-layer (4D): Core DA signals
            anticipatory_da, consummatory_da, wanting_index, liking_index,
            # M-layer (2D): Meta-indices
            dissociation_index, temporal_phase,
            # P-layer (2D): Regional activation
            caudate_activation, nacc_activation,
        ], dim=-1)  # (B, T, 8)
