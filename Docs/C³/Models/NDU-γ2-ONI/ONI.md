# NDU-γ2-ONI: Over-Normalization in Intervention

**Model**: Over-Normalization in Intervention
**Unit**: NDU (Novelty Detection Unit)
**Circuit**: Salience + Perceptual (Developing Auditory Cortex, Attention Networks)
**Tier**: γ (Integrative) — 50–70% confidence
**Version**: 2.2.0 (Phase 3E: R³ v2 expansion — added I:Information feature dependencies)
**Date**: 2026-02-13

> **Naming**: This document uses MI naming (R³, H³, C³). See [Road-map/01-GLOSSARY.md](../../General/01-GLOSSARY.md) for terminology.
> **MI is independent from D0** — no shared code, no shared indices. All formulas implemented from scratch.
> **Legacy**: Replaces `Library/Auditory/C⁰/Models/NDU-γ2-ONI.md` (v1.0.0, S⁰/HC⁰ naming).

---

## 1. What Does This Model Simulate?

The **Over-Normalization in Intervention** (ONI) model describes the preliminary observation that musical interventions in preterm infants may lead to "over-normalization" where intervention groups exceed full-term controls in certain neural measures, suggesting possible compensatory enhancement or heightened attentional orienting.

```
OVER-NORMALIZATION IN INTERVENTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EXPECTED: OBSERVED:
──────── ─────────

Full-term > Intervention > Control Intervention > Full-term > Control

┌─────────────────────────────────────────────────────────────────┐
│ │
│ MMR │
│ Amplitude ● Intervention │
│ │ │
│ │ ● Full-term │
│ │ │
│ │ ● Control │
│ │ │
│ └─────────────────────────────────────────────────────── │
│ Preterm Full-term │
│ │
└─────────────────────────────────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SPECULATIVE: Unexpected finding requiring mechanistic
explanation and replication.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INTERPRETATION:
Possible enhanced attentional orienting OR compensatory adaptation

ALTERNATIVE EXPLANATIONS:
 1. Enhanced attention capture (intervention-trained orienting)
 2. Compensatory over-development (preterm adaptation)
 3. Measurement artifact (control group differences)
 4. Developmental trajectory differences (timing effects)
 5. Sample selection bias
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 1.1 Why ONI Matters for NDU

ONI documents an unexpected finding from the developmental plasticity data:

1. **DSP** (β1) provides the empirical data that revealed the over-normalization effect.
2. **SDDP** (γ1) models the sex-dependent component from the same dataset.
3. **ONI** (γ2) proposes a compensatory or attentional explanation (speculative).

---

## 2. Neural Circuit: Complete Anatomy

### 2.1 Information Flow Architecture (EAR → BRAIN → ONI)

```
╔══════════════════════════════════════════════════════════════════════════════╗
║ ONI COMPUTATION ARCHITECTURE ║
╠══════════════════════════════════════════════════════════════════════════════╣
║ ║
║ AUDIO (44.1kHz waveform) ║
║ │ ║
║ ▼ ║
║ ┌──────────────────┐ ║
║ │ COCHLEA │ 128 mel bins x 172.27Hz frame rate ║
║ │ (Mel Spectrogram)│ hop = 256 samples, frame = 5.8ms ║
║ └────────┬─────────┘ ║
║ │ ║
║ ═════════╪══════════════════════════ EAR ═══════════════════════════════ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ SPECTRAL (R³): 49D per frame │ ║
║ │ │ ║
║ │ ┌───────────┐ ┌─────────┐ ┌─────────┐ ┌──────────┐ ┌────────┐ │ ║
║ │ │CONSONANCE │ │ ENERGY │ │ TIMBRE │ │ CHANGE │ │ X-INT │ │ ║
║ │ │ 7D [0:7] │ │ 5D[7:12]│ │ 9D │ │ 4D │ │ 24D │ │ ║
║ │ │ │ │ │ │ [12:21] │ │ [21:25] │ │ [25:49]│ │ ║
║ │ │roughness │ │amplitude│ │warmth │ │spec_chg │ │x_l0l5 │ │ ║
║ │ │sethares │ │loudness │ │tristim. │ │enrg_chg │ │x_l4l5 │ │ ║
║ │ └───────────┘ └─────────┘ └─────────┘ └──────────┘ └────────┘ │ ║
║ │ ONI reads: ~14D │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ TEMPORAL (H³): Multi-scale windowed morphological features │ ║
║ │ │ ║
║ │ │ H0 (25ms gamma) │ │ H3 (100ms alpha) │ │ ║
║ │ │ H3 (100ms alpha) │ │ H4 (125ms theta) │ │ ║
║ │ │ H4 (125ms theta) │ │ H16 (1000ms beat) │ │ ║
║ │ │ H16 (1000ms beat) │ │ │ │ ║
║ │ │ │ │ Enhanced prediction │ │ ║
║ │ │ Deviance detection │ │ Heightened attention │ │ ║
║ │ └─────────────────────────────┘ └────────────────────────────┘ │ ║
║ │ ONI demand: ~16 of 2304 tuples │ ║
║ └────────────────────────────┬─────────────────────────────────────┘ ║
║ │ ║
║ ═════════════════════════════╪═══════ BRAIN: Salience Circuit ════════ ║
║ │ ║
║ ┌───────┴───────┐ ║
║ ▼ ▼ ║
║ ┌─────────────────┐ ┌─────────────────┐ ║
║ │ │ │ │ ║
║ │ Pitch Ext[0:10] │ │ Scene An [0:10] │ ║
║ │ Interval │ │ Attention │ ║
║ │ Anal [10:20] │ │ Gating [10:20] │ ║
║ │ Contour [20:30] │ │ Salience │ ║
║ │ │ │ Weight [20:30] │ ║
║ └────────┬────────┘ └────────┬────────┘ ║
║ │ │ ║
║ └────────┬───────────┘ ║
║ ▼ ║
║ ┌──────────────────────────────────────────────────────────────────┐ ║
║ │ ONI MODEL (11D Output) │ ║
║ │ │ ║
║ │ Layer E (Explicit): f01_over_normalization, │ ║
║ │ f02_compensatory_response, │ ║
║ │ f03_attention_enhancement, │ ║
║ │ f04_intervention_ceiling │ ║
║ │ Layer M (Math): dosage_accumulation, │ ║
║ │ preterm_baseline, fullterm_reference │ ║
║ │ Layer P (Present): enhanced_mmr, attentional_state │ ║
║ │ Layer F (Future): longterm_outcomes, │ ║
║ │ intervention_optimization │ ║
║ └──────────────────────────────────────────────────────────────────┘ ║
║ ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. Scientific Foundation

### 3.1 Core Evidence Table

| # | Study | Method | N | Key Finding | Effect Size | MI Relevance |
|---|-------|--------|---|-------------|-------------|-------------|
| 1 | **Partanen et al. 2022** | MEG | 21 preterm + 12 full-term | Singing intervention > full-term in oddball MMR; singing group exceeds full-term norms | F(2,27)=4.019, p=0.030, **η²=0.229**; sex×singing η²=0.309 | **Primary**: f01 over-normalization index; f03 sex-modulated enhancement |
| 2 | **Scholkmann et al. 2024** | fNIRS | 17 preterm | Creative Music Therapy produces two response subgroups: positive (mostly female, StO₂ +3.2%) and negative (mostly male, StO₂ −1.2%) | **r_rb=1.000** (auditory cortex, p=0.002); sex diff p=0.034 | **Supporting**: heterogeneous intervention responses; physiological individual differences drive over-normalization variability |
| 3 | **Edalati et al. 2023** | EEG | 19 preterm (32±2.6 wGA) | Premature neonates show beat frequency responses above noise floor; duple meter enhancement during sleep | p=0.0013 (beat); **Cohen's d=0.75** (duple > beat) | **Supporting**: biological substrate for differential intervention responses in preterm auditory cortex |
| 4 | **Saadatmehr et al. 2024** | EEG | 46 preterm (27–35 wGA) | Developmental timeline: <33wGA beat only; ≥33wGA beat+meter; phase coupling improves with age | beat ρ=0.37, duple ρ=0.31, triple ρ=0.30 (all p<0.04); phase-age Rc=0.47, p=0.007 | **Supporting**: intervention timing matters — neural coding capacity for hierarchical rhythms emerges after 33 wGA |
| 5 | **Kaminska et al. 2025** | EEG 32ch | 30 preterm (30–38 PMW) | Delta brushes show stimulus-specific cortical networks; voice vs click evoke different topographies; gamma oscillations increase with age | Stimulus-specific DB topography; age-dependent lateralization shift | **Supporting**: auditory cortex shows stimulus-specific processing even in preterm; age-dependent maturation of auditory networks |
| 6 | **Tervaniemi 2022** | Review | — | Historical overview of MMN paradigms from oddball to multi-feature to naturalistic; discusses optimal stimulus design for developmental populations | Review (no effect size) | **Methodological**: MMR measurement framework for ONI; multi-feature paradigm validation |
| 7 | **Nayak et al. 2025** | Epidemiological + genetic | 39,358 (behavioral); 7,180 (genetic) | Rhythm impairment is risk factor for speech-language disorders; genetic pleiotropy between rhythm and reading | **OR=1.33** [1.18–1.49], p<0.0001; beat sync OR=1.72 | **Distal**: long-term developmental significance of enhanced MMR — rhythm processing links to language outcomes |
| 8 | **Blasi et al. 2025** | Systematic review (20 RCTs) | 718 | Music/dance rehabilitation produces structural and functional neuroplasticity in perception, memory, language, emotion, and motor areas | Review of 20 RCTs | **Supporting**: neuroplasticity framework — music interventions can produce compensatory neural changes that exceed baseline |

**UNEXPECTED FINDING**: The primary Partanen 2022 result — intervention group exceeding full-term norms — remains mechanistically unexplained. Authors themselves question whether larger MMRs are truly beneficial, noting Kushnerenko et al. (2013) argue that MMR amplitude reduction with age reflects improved inhibitory processes. The over-normalization could reflect (a) enhanced attentional orienting, (b) compensatory adaptation, (c) delayed inhibitory maturation, or (d) measurement artifact from MEG vs EEG differences.

**NOTE**: Scholkmann 2024 fNIRS data reveals OPPOSITE sex direction to Partanen MEG data — females show positive StO₂ response while males show negative. This suggests the over-normalization effect may be modality- and measure-specific rather than a unitary phenomenon.

### 3.2 Effect Size Summary

```
Primary Evidence (k=2 empirical + 2 developmental + 1 preterm physiology):
 Partanen 2022 (MEG): η²=0.229 (oddball group effect), η²=0.309 (sex×singing)
 Scholkmann 2024 (fNIRS): r_rb=1.000 (auditory cortex, subgroup 1), sex p=0.034
 Edalati 2023 (EEG): Cohen's d=0.75 (duple > beat), p=0.0013 (beat tracking)
 Saadatmehr 2024 (EEG): ρ=0.31-0.37 (age-rhythm correlations), Rc=0.47 (phase-age)
 Kaminska 2025 (EEG): Stimulus-specific topography (qualitative)

Heterogeneity: HIGH — over-normalization demonstrated in MEG only (Partanen);
 fNIRS shows opposite sex pattern (Scholkmann); developmental
 studies show progressive maturation rather than over-normalization per se
Quality: γ-tier — single RCT with small N, no independent replication
 of over-normalization effect; mechanism unclear
Largest sample: N=39,358 (Nayak epidemiological — distal relevance only)
Replication: PENDING — Finnish cohort (Kostilainen et al. 2021 EEG) shows
 some consistency but used different imaging modality
```

---

## 4. R³ Input Mapping: What ONI Reads

### 4.1 R³ v1 Feature Dependencies ([0:49])

| R³ Group | Index | Feature | ONI Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **B: Energy** | [10] | spectral_flux | Deviance magnitude (frame change) | Mismatch detection |
| **B: Energy** | [11] | onset_strength | Onset deviation | Rhythmic deviance |
| **C: Timbre** | [13] | brightness | Tonal quality | Pattern sensitivity |
| **C: Timbre** | [16] | spectral_spread | Spectral width | Processing complexity |
| **D: Change** | [21] | spectral_change | Spectral dynamics | Enhanced prediction |
| **D: Change** | [22] | energy_change | Energy dynamics | Intensity tracking |
| **D: Change** | [23] | pitch_change | Pitch dynamics | Over-normalization proxy |
| **E: Interactions** | [33:41] | x_l4l5 (8D) | Dynamic-percept binding | Enhanced predictive coding |

### 4.2 R³ v2 Feature Dependencies ([49:128]) — NEW

| R³ Group | Index | Feature | ONI Role | Scientific Basis |
|----------|-------|---------|----------|------------------|
| **I: Information** | [91] | information_rate | Information flow rate | Weineck 2022: information rate quantifies temporal density of novel content; over-normalization occurs when intervention drives information processing beyond full-term baseline |
| **I: Information** | [90] | spectral_surprise | Prediction error magnitude | Friston prediction error: surprise levels that exceed full-term norms indicate over-normalization — the intervention group's enhanced predictive processing |

**Rationale**: ONI models over-normalization in intervention — the finding that singing intervention groups can exceed full-term baselines. The v1 representation uses pitch_change [23] and spectral_change [21] as proxies for enhanced processing. information_rate [91] provides a direct measure of how rapidly novel content is processed, enabling detection of over-normalization when this rate exceeds typical full-term values. spectral_surprise [90] quantifies prediction error magnitude, which in over-normalized infants may show atypically low values (indicating overly precise internal models).

**Code impact**: None yet — R³ v2 features are doc-only until Phase 5 integration. Current code reads r3[..., 0:49]; v2 features will extend the slice to r3[..., 0:128] when the EAR pipeline emits the expanded vector.

### 4.3 Physical → Cognitive Transformation

```
R³ Physical Input Cognitive Output
──────────────────────────────── ──────────────────────────────────────
R³[10] spectral_flux ──────────┐
R³[11] onset_strength ─────────┼──► MMR deviance magnitude

R³[21] spectral_change ────────┐
R³[23] pitch_change ───────────┼──► Enhanced predictive processing

R³[13] brightness ─────────────┐
H³ deviance variability ───────┘ Attention enhancement (f03)
```

---

## 5. H³ Temporal Demand

### 5.1 Demand Specification

ONI requires H³ features for deviance detection at enhanced levels and for heightened attentional processing. The demand reflects the over-normalization temporal dynamics.

| R³ Index | Feature | H | Morph | Law | Purpose |
|----------|---------|---|-------|-----|---------|
| 10 | spectral_flux | 0 | M0 (value) | L2 (bidi) | Instantaneous deviance 25ms |
| 10 | spectral_flux | 3 | M2 (std) | L2 (bidi) | Deviance variability 100ms |
| 10 | spectral_flux | 16 | M1 (mean) | L2 (bidi) | Mean deviance over 1s |
| 11 | onset_strength | 0 | M0 (value) | L2 (bidi) | Onset deviance 25ms |
| 11 | onset_strength | 3 | M0 (value) | L2 (bidi) | Onset at 100ms |
| 13 | brightness | 3 | M0 (value) | L2 (bidi) | Tonal quality 100ms |
| 13 | brightness | 3 | M20 (entropy) | L2 (bidi) | Tonal entropy 100ms |
| 21 | spectral_change | 3 | M0 (value) | L2 (bidi) | Spectral change 100ms |
| 21 | spectral_change | 4 | M8 (velocity) | L0 (fwd) | Spectral velocity 125ms |
| 23 | pitch_change | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms |
| 23 | pitch_change | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s |
| 22 | energy_change | 3 | M0 (value) | L2 (bidi) | Energy change 100ms |
| 33 | x_l4l5[0] | 3 | M0 (value) | L2 (bidi) | Dynamic coupling 100ms |
| 33 | x_l4l5[0] | 3 | M2 (std) | L2 (bidi) | Coupling variability 100ms |
| 33 | x_l4l5[0] | 16 | M1 (mean) | L2 (bidi) | Mean coupling over 1s |
| 33 | x_l4l5[0] | 16 | M18 (trend) | L0 (fwd) | Coupling trend over 1s |

**v1 demand**: 16 tuples

#### R³ v2 Projected Expansion

No significant v2 expansion projected.

**v2 projected**: 0 tuples
**Total projected**: 16 tuples of 294,912 theoretical = 0.0054%

---

## 6. Output Space: 11D Multi-Layer Representation

### 6.1 Complete Output Specification

```
ONI OUTPUT TENSOR: 11D PER FRAME (172.27 Hz)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LAYER E — EXPLICIT FEATURES
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 0 │ f01_over_normalization │ [0, 2] │ Enhancement beyond full-term.
 │ │ │ f01 = MMR_intervention /
 │ │ │ (MMR_fullterm + ε)
────┼──────────────────────────┼────────┼────────────────────────────────────
 1 │ f02_compensatory_resp │ [0, 1] │ Enhanced prediction magnitude.
 │ │ │ f02 = σ(0.35 * spec_change_100ms
 │ │ │ + 0.35 * coupling_mean_1s
────┼──────────────────────────┼────────┼────────────────────────────────────
 2 │ f03_attention_enhance │ [0, 1] │ Heightened deviance detection.
 │ │ │ f03 = σ(0.35 * brightness_100ms
 │ │ │ + 0.35 * tonal_entropy_100ms
────┼──────────────────────────┼────────┼────────────────────────────────────
 3 │ f04_intervention_ceiling │ [0, 1] │ Response saturation point.
 │ │ │ f04 = 1 - exp(-dosage / τ_ceil)
 │ │ │ τ_ceil = 4 weeks (hypothesized)

LAYER M — MATHEMATICAL MODEL OUTPUTS (Intervention Dynamics)
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 4 │ dosage_accumulation │ [0, 1] │ Cumulative intervention exposure.
 │ │ │ EMA of f03 over session timescale
────┼──────────────────────────┼────────┼────────────────────────────────────
 5 │ preterm_baseline │ [0, 1] │ Starting point reference.
 │ │ │ pitch-processing baseline strength proxy
────┼──────────────────────────┼────────┼────────────────────────────────────
 6 │ fullterm_reference │ [0, 1] │ Normalization target.
 │ │ │ External reference (constant)

LAYER P — PRESENT PROCESSING
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 7 │ enhanced_mmr │ [0, 1] │ Current mismatch strength.
────┼──────────────────────────┼────────┼────────────────────────────────────
 8 │ attentional_state │ [0, 1] │ Heightened attention level.

LAYER F — FUTURE PREDICTIONS
─────────────────────────────────────────────────────────────────────────────
idx │ Name │ Range │ Neuroscience Basis
────┼──────────────────────────┼────────┼────────────────────────────────────
 9 │ longterm_outcomes │ [0, 1] │ Developmental trajectory.
────┼──────────────────────────┼────────┼────────────────────────────────────
10 │ intervention_opt │ [0, 1] │ Protocol ceiling detection.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: 11D per frame at 172.27 Hz
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 7. Mathematical Formulation

### 7.1 Over-Normalization Function

```
OverNormalization(t) = MMR_intervention(t) / (MMR_fullterm + ε)

Parameters:
 f01 > 1.0: Over-normalization (intervention > full-term)
 f01 = 1.0: Normalization (intervention = full-term)
 f01 < 1.0: Under-normalization (intervention < full-term)
 Observed: f01 ≈ 1.2-1.3 (20-30% enhancement beyond full-term)
```

### 7.2 Feature Formulas

```python
# COEFFICIENT SATURATION RULE: For sigmoid(Σ wi*gi), |wi| must sum <= 1.0

# f01: Over-Normalization Index
f01 = MMR_intervention / (MMR_fullterm + 1e-6)
# Ratio; f01 > 1.0 indicates over-normalization

# f02: Compensatory Response (coefficients sum = 1.0)
f02 = σ(0.35 * spectral_change_100ms
 + 0.35 * coupling_mean_1s
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f03: Attention Enhancement (coefficients sum = 1.0)
f03 = σ(0.35 * brightness_100ms
 + 0.35 * tonal_entropy_100ms
# coefficients: 0.35 + 0.35 + 0.30 = 1.0 ✓

# f04: Intervention Ceiling
f04 = 1 - exp(-dosage / 4.0)
# dosage in weeks, ceiling constant = 4 weeks (hypothesized)
```

---

## 8. Brain Regions

### 8.1 Pipeline Validated Regions

| # | Region | Abbr | MNI Coordinates | BA | Hemisphere | Evidence Type | ONI Function | Source |
|---|--------|------|-----------------|----|------------|---------------|-------------|--------|
| 1 | **Superior Temporal Gyrus** | STG | (−58, −20, 8) | 22 | bilateral | Direct (MEG) | MMR generation — over-normalization locus; intervention group shows enhanced MMR originating from auditory cortex | Partanen 2022 (left hemisphere MEG source) |
| 2 | **Primary Auditory Cortex** | A1 | (−42, −22, 10) | 41/42 | bilateral | Direct (fNIRS) | Cerebrovascular oxygenation response to music therapy; +3.2% StO₂ in positive responders (p=0.002) | Scholkmann 2024 (fNIRS channels over temporal cortex) |
| 3 | **Prefrontal Cortex** | PFC | (−38, 46, 12) | 10/46 | bilateral | Direct (fNIRS) | Attentional/executive processing during music therapy; +2.4% StO₂ (p=0.008) | Scholkmann 2024 (prefrontal fNIRS channels) |
| 4 | **Temporal Cortex (preterm)** | TC | N/A (preterm EEG) | — | right>bilateral | Direct (EEG) | Delta brush generation — stimulus-specific auditory processing; gamma oscillations increase with age; lateralization shift from R→L for voice stimuli | Kaminska 2025 (32ch EEG, 30–38 PMW) |
| 5 | **Auditory Cortex (developing)** | AC-dev | N/A (preterm EEG) | — | bilateral | Direct (EEG) | Beat and meter frequency tracking; neural synchronization to rhythmic periodicities improves with gestational age (ρ=0.37) | Edalati 2023; Saadatmehr 2024 (high-density EEG) |

**Note**: MNI coordinates for regions 1–3 are adult approximations. Preterm infant brain anatomy differs substantially from adult templates; fNIRS and EEG source localization in neonates provides cortical area identification rather than precise MNI coordinates. Regions 4–5 are identified by electrode topography rather than source localization.

---

## 9. Cross-Unit Pathways

### 9.1 ONI Interactions

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ ONI INTERACTIONS │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ INTRA-UNIT (NDU): │
│ DSP.plasticity_index ───────► ONI (over-normalization evidence) │
│ SDDP.intervention_resp ────► ONI (sex-dependent component) │
│ │
│ CROSS-UNIT (NDU → ARU): │
│ ONI.enhanced_mmr ───────────► ARU (enhanced affective processing) │
│ │
│ UPSTREAM DEPENDENCIES: │
│ R³ (~14D) ──────────────────► ONI (direct spectral features) │
│ H³ (16 tuples) ─────────────► ONI (temporal dynamics) │
│ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Falsification Criteria

| Criterion | Testable Prediction | Status |
|-----------|---------------------|--------|
| **Over-normalization** | Intervention should exceed full-term | **Preliminary support** (η²=0.23) |
| **Replication** | Effect should replicate independently | **Awaiting replication** |
| **Mechanism** | Attention or prediction measures should explain | **Awaiting testing** |
| **Dose-response** | Ceiling should emerge at high dosages | Testable |
| **Long-term outcomes** | Enhancement should persist or fade | Testable via follow-up |

---

## 11. Implementation

### 11.1 Pseudocode

```python
class ONI(BaseModel):
 """Over-Normalization in Intervention Model.

 Output: 11D per frame.
 SPECULATIVE: Unexpected finding requiring mechanistic explanation.
 """
 NAME = "ONI"
 UNIT = "NDU"
 TIER = "γ2"
 OUTPUT_DIM = 11
 TAU_DECAY = 0.8 # Response persistence (seconds)
 ENHANCEMENT_FACTOR = 1.0 # Over-normalization threshold
 RTI_WINDOW = 2.5 # Oddball integration (seconds)
 CEILING_CONSTANT = 4.0 # Weeks (hypothesized)

 @property
 def h3_demand(self) -> List[Tuple[int, int, int, int]]:
 """16 tuples for ONI computation."""
 return [
 # (r3_idx, horizon, morph, law)
 (10, 0, 0, 2), # spectral_flux, 25ms, value, bidi
 (10, 3, 2, 2), # spectral_flux, 100ms, std, bidi
 (10, 16, 1, 2), # spectral_flux, 1000ms, mean, bidi
 (11, 0, 0, 2), # onset_strength, 25ms, value, bidi
 (11, 3, 0, 2), # onset_strength, 100ms, value, bidi
 (23, 3, 0, 2), # pitch_change, 100ms, value, bidi
 (23, 16, 1, 2), # pitch_change, 1000ms, mean, bidi
 (22, 3, 0, 2), # energy_change, 100ms, value, bidi
 (13, 3, 0, 2), # brightness, 100ms, value, bidi
 (13, 3, 20, 2), # brightness, 100ms, entropy, bidi
 (21, 3, 0, 2), # spectral_change, 100ms, value, bidi
 (21, 4, 8, 0), # spectral_change, 125ms, velocity, fwd
 (33, 3, 0, 2), # x_l4l5[0], 100ms, value, bidi
 (33, 3, 2, 2), # x_l4l5[0], 100ms, std, bidi
 (33, 16, 1, 2), # x_l4l5[0], 1000ms, mean, bidi
 (33, 16, 18, 0), # x_l4l5[0], 1000ms, trend, fwd
 ]

 def compute(self, h3_features: Dict,
 r3: Tensor) -> Tensor:
 """
 Compute ONI 11D output.

 Args:
 h3_direct: Dict of (r3,h,m,l) -> (B,T) scalars
 r3: (B,T,49) raw R³ features

 Returns:
 (B,T,11) ONI output
 """
 # R³ features
 spectral_flux = r3[..., 10:11]
 onset_strength = r3[..., 11:12]
 brightness = r3[..., 13:14]
 spectral_change = r3[..., 21:22]
 pitch_change = r3[..., 23:24]
 x_l4l5 = r3[..., 33:41]

 # H³ direct features
 brightness_100ms = h3_direct[(13, 3, 0, 2)].unsqueeze(-1)
 tonal_entropy_100ms = h3_direct[(13, 3, 20, 2)].unsqueeze(-1)
 spectral_change_100ms = h3_direct[(21, 3, 0, 2)].unsqueeze(-1)
 coupling_mean_1s = h3_direct[(33, 16, 1, 2)].unsqueeze(-1)

 # ═══ LAYER E: Explicit features ═══

 # f01: Over-Normalization Index (ratio)
 f01 = intervention_mmr # scaled by fullterm_mmr externally

 # f02: Compensatory Response (coefficients sum = 1.0)
 f02 = torch.sigmoid(
 0.35 * spectral_change_100ms
 + 0.35 * coupling_mean_1s
 )

 # f03: Attention Enhancement (coefficients sum = 1.0)
 f03 = torch.sigmoid(
 0.35 * brightness_100ms
 + 0.35 * tonal_entropy_100ms
 )

 # f04: Intervention Ceiling (exponential saturation)
 f04 = torch.sigmoid(
 0.50 * f03 + 0.50 * f02
 )

 # ═══ LAYER M: Intervention Dynamics ═══
 dosage_accumulation = torch.sigmoid(
 )
 fullterm_reference = torch.sigmoid(
 )

 # ═══ LAYER P: Present ═══

 # ═══ LAYER F: Future ═══
 longterm_outcomes = torch.sigmoid(
 0.50 * f01 + 0.50 * f02
 )
 intervention_opt = torch.sigmoid(
 0.50 * f04 + 0.50 * dosage_accumulation
 )

 return torch.cat([
 f01, f02, f03, f04, # E: 4D
 dosage_accumulation, preterm_baseline, fullterm_reference, # M: 3D
 enhanced_mmr, attentional_state, # P: 2D
 longterm_outcomes, intervention_opt, # F: 2D
 ], dim=-1) # (B, T, 11)
```

---

## 12. Validation Summary

| Metric | Value | Source |
|--------|-------|--------|
| **Papers** | 8 (2 empirical preterm + 2 developmental + 1 fNIRS + 1 epidemiological + 2 reviews) | Deep literature review v2.1.0 |
| **Effect Sizes** | η²=0.229 (oddball group), η²=0.309 (sex×singing), r_rb=1.000 (fNIRS), d=0.75 (duple>beat) | Multi-modal, medium-large |
| **Evidence Modality** | MEG + fNIRS + EEG + epidemiological + genetic | Multi-modal cross-method |
| **Sample Range** | n=17 to N=39,358 | Preterm-specific n=17–46; epidemiological N=39,358 |
| **Falsification Tests** | 1/5 preliminary | Low validity (mechanism unclear) |
| **R³ Features Used** | ~14D of 49D | Energy + timbre + change + interactions |
| **H³ Demand** | 16 tuples (0.69%) | Sparse, efficient |
| **Output Dimensions** | **11D** | 4-layer structure |
| **Brain Regions** | 5 regions (STG, A1, PFC, TC-preterm, AC-developing) | MEG/fNIRS/EEG localization |

**Research Priorities**:
1. **CRITICAL: Mechanistic investigation** — What causes over-normalization? Enhanced attention vs compensatory adaptation vs delayed inhibitory maturation
2. Independent replication with MEG using larger sample (Partanen n=21 is underpowered)
3. Resolution of sex-direction discrepancy: Partanen (males benefit more in MMR) vs Scholkmann (females show positive StO₂)
4. Dosage titration study to identify ceiling; music therapist quality vs singing quantity
5. Longitudinal follow-up: Does enhancement persist at 2-year cognitive assessment?
6. Developmental timing window: Saadatmehr shows ≥33wGA as critical threshold for meter coding

---

## 13. Scientific References

1. **Partanen, E., Mårtensson, G., Hugoson, P., Huotilainen, M., Fellman, V., & Ådén, U. (2022)**. Auditory processing of the brain is enhanced by parental singing for preterm infants. *Frontiers in Neuroscience*, 16, 772008. https://doi.org/10.3389/fnins.2022.772008
2. **Scholkmann, F., Haslbeck, F., Oba, E., et al. (2024)**. Creative music therapy in preterm infants: Effects on cerebrovascular oxygenation and perfusion. *Scientific Reports*, 14, 28249.
3. **Edalati, M., Wallois, F., Trainor, L. J., & Moghimi, S. (2023)**. Rhythm in the premature neonate brain: Very early processing of auditory beat and meter. *The Journal of Neuroscience*, 43(15), 2794–2802. https://doi.org/10.1523/JNEUROSCI.2217-22.2023
4. **Saadatmehr, B., Edalati, M., Wallois, F., Trainor, L. J., & Moghimi, S. (2024)**. Auditory rhythm encoding during the last trimester of human gestation: From tracking the basic beat to tracking hierarchical nested temporal structures. *Journal of Neuroscience* (accepted). https://doi.org/10.1523/JNEUROSCI.0398-24.2024
5. **Kaminska, A., Arzounian, D., Delattre, V., et al. (2025)**. Auditory evoked delta brushes involve stimulus-specific cortical networks in preterm infants. *iScience*, 28, 112313. https://doi.org/10.1016/j.isci.2025.112313
6. **Tervaniemi, M. (2022)**. Mismatch negativity–stimulation paradigms in past and in future. *Frontiers in Neuroscience*, 16, 1025763. https://doi.org/10.3389/fnins.2022.1025763
7. **Nayak, S., Ladányi, E., Fisher, S. E., Gordon, R. L., et al. (2025)**. Musical rhythm abilities and risk for developmental speech-language problems and disorders: Epidemiological and polygenic associations. *Nature Communications*, 16, 8355. https://doi.org/10.1038/s41467-025-60867-2
8. **Blasi, V., Rapisarda, L., Cacciatore, D. M., et al. (2025)**. Structural and functional neuroplasticity in music and dance-based rehabilitation: A systematic review. *Journal of Neurology*, 272, 329. https://doi.org/10.1007/s00415-025-13048-6

---

## 14. Migration Notes (D0 → MI)

### What Changed from v1.0.0

| Aspect | D0 (v1.0.0) | MI (v2.0.0) |
|--------|-------------|-------------|
| Input space | S⁰ (256D) | R³ (49D) |
| Deviance signal | S⁰.L5.spectral_flux[45] + HC⁰.EFC | R³.spectral_flux[10] |
| Attention | S⁰.L5.spectral_kurtosis[41] + HC⁰.ATT | R³.brightness[13] |
| Enhancement | S⁰.L4.velocity_F[16] + HC⁰.OSC | R³.spectral_change[21] |
| Prediction | S⁰.X_L4L5[192:200] + HC⁰.HRM | R³.x_l4l5[33:41] |
| Demand format | HC⁰ index ranges | H³ 4-tuples (sparse) |
| Total demand | 27/2304 = 1.17% | 16/2304 = 0.69% |
| Output | 11D | 11D (same) |

---

---

## 15. Doc-Code Mismatches (for Phase 5 reference)

| # | Field | Doc (ONI.md) | Code (oni.py) | Notes |
|---|-------|-------------|---------------|-------|
| 1 | **FULL_NAME** | "Over-Normalization in Intervention" | "Oddball Novelty Index" | Different name entirely |
| 2 | **OUTPUT_DIM** | 11D (4E+3M+2P+2F) | 10D (4E+2M+2P+2F) | Code missing fullterm_reference in Layer M |
| 4 | **h3_demand** | 16 tuples (0.69% of 2304) | () empty tuple | Code has no H³ demand |
| 5 | **Layer M dims** | 3 (dosage_accumulation, preterm_baseline, fullterm_reference) | 2 (intervention_dosage, full_term_comparison) | Different names and count |
| 6 | **Layer E dim names** | f01_over_normalization, f02_compensatory_resp, f03_attention_enhance, f04_intervention_ceiling | f01_over_normalization_idx, f02_compensatory_response, f03_attention_enhancement, f04_intervention_ceiling | Minor naming differences |
| 7 | **Citations** | Partanen 2022, η²=0.229 | Virtala 2023, eta^2=0.23 | Different author/year; Virtala is review co-author, not primary study author |
| 8 | **version** | 2.1.0 (after this revision) | 2.0.0 | Code not yet updated |
| 9 | **CROSS_UNIT_READS** | ONI.enhanced_mmr → ARU (doc Section 9) | () empty | Code has no cross-unit reads |
| 10 | **brain_regions** | 5 regions (STG, A1, PFC, TC, AC-developing) | 2 regions (STG, IFG) | Code has IFG which doc doesn't emphasize; doc has fNIRS/EEG developmental regions |

**Model Status**: **SPECULATIVE**
**Output Dimensions**: **11D**
**Evidence Tier**: **γ (Integrative)**
**Confidence**: **50–70%**
**Mechanism**: **UNCLEAR**
