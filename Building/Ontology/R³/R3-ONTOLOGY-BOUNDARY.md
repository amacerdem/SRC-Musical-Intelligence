# R³ Ontology & Boundary Specification

**Version**: 1.0.0
**Status**: FROZEN (ontological boundaries)
**Date**: 2026-02-16
**Supersedes**: Implicit 128D design (Groups A–K, no formal boundary)

---

## 1. Formal Definition

**R³ is an Early Perceptual Front-End.**

It answers one question: **"What does the sound look like right now?"**

R³ holds per-frame (or near-frame) acoustic descriptors that can be extracted from the audio signal without listener models, temporal memory, cross-domain binding, or predictive inference. It represents the output of the peripheral auditory system and early auditory cortex — up to and including primary auditory cortex (A1) — before attentional selection, cognitive interpretation, or expectation-based processing begins.

### Boundary Sentence

> R³ = the set of acoustic descriptors extractable from a single frame (±2 neighbouring frames) of the audio signal, requiring no accumulated history, no listener model, no cross-domain feature products, and no predictive or information-theoretic context beyond the immediate spectral neighbourhood.

### What R³ Is

- A **stateless** feature extractor (no running averages, no EMA, no counters)
- A **bottom-up** signal description (stimulus-driven, not expectation-driven)
- An **intra-domain** measurement set (each feature operates within one perceptual domain)
- A **deterministic** function of the local spectrogram (same input → same output, no learned parameters)

### What R³ Is Not

- Not a listener model (no surprise, no prediction, no expectation)
- Not a temporal integrator (H³ handles temporal morphology)
- Not a feature binder (C³ handles cross-domain interactions)
- Not a cognitive representation (C³ models meaning, valence, reward)

### Biological Analogy

| Processing Stage | Anatomical Correlate | R³ Coverage |
|-----------------|---------------------|-------------|
| Cochlea → auditory nerve | Frequency decomposition, onset coding | Energy, basic timbre |
| Cochlear nucleus → SOC | Onset detection, spectral flux | Change features |
| Inferior colliculus | AM/FM rate extraction, pitch tracking | Modulation, pitch/chroma |
| Medial geniculate body | Spectral template matching | Consonance, harmonic templates |
| Primary auditory cortex (A1) | Spectral contrast, key templates | Timbre extended, harmony |
| **Beyond A1** | **Expectation, binding, prediction** | **NOT R³ → H³ / C³** |

---

## 2. Inclusion Rules

A feature belongs in R³ if and only if ALL of the following hold:

### Rule 1: Frame Locality

The feature is computable from a single frame, or at most frame t and its ±2 neighbours (±11.6 ms at 172.27 Hz frame rate). This allows:

- Instantaneous spectral shape (centroid, bandwidth, rolloff, flatness)
- Frame-to-frame derivatives (spectral flux, RMS delta, centroid delta)
- Ultra-short smoothing (≤5-frame / ~29 ms kernel, e.g., tonal_stability)

This **excludes** running averages, exponential moving averages, accumulated transition matrices, or any computation whose output depends on frames outside the ±2 window.

### Rule 2: No Listener Model

The feature does not require modelling the listener's expectations, memory, or prior experience. It describes **the signal**, not **the listener's response to the signal**.

- Allowed: "How key-like is this frame's chroma?" (template matching)
- Forbidden: "How surprising is this frame given what came before?" (expectation model)

### Rule 3: No Cross-Domain Binding

The feature operates within a single perceptual domain. It does not multiply, correlate, or combine features from different groups.

- Allowed: Consonance features computed from harmonic spectrum
- Forbidden: consonance × energy interaction products

### Rule 4: No Prediction

The feature does not estimate future states, model temporal contingencies, or compute information-theoretic quantities that require a reference distribution built over time.

- Allowed: Spectral entropy (distribution shape of current frame)
- Forbidden: Predictive entropy (variance of expected future)
- Forbidden: Surprisal (divergence from accumulated baseline)

### Rule 5: Deterministic

R³ uses no learned parameters or trained weights. Every computation is a closed-form function of the spectrogram. This preserves the glass-box property: R³'s output is fully auditable and reproducible.

---

## 3. Exclusion Rules

A feature must be removed from R³ if ANY of the following hold:

| Violation | Example | Destination |
|-----------|---------|-------------|
| Requires running average / EMA | spectral_surprise (KL vs mel_avg) | C³ |
| Requires accumulated counts | melodic_entropy (transition matrix) | C³ |
| Requires running variance | predictive_entropy (log var(mel)) | C³ |
| Measures cross-domain product | amp × roughness, flux × sethares | C³ input layer |
| Represents temporal redundancy | information_rate (MI between frames) | H³ velocity morph |
| Proxies another group's output | tonal_ambiguity (1 − key_clarity) | Remove (redundant) |
| Depends on Stage 3 cascading | rhythmic_info_content (from rhythm_groove) | C³ |

### The EMA Test

If a feature's implementation contains any of these patterns, it violates Rule 1:

```python
# VIOLATION: temporal state
self._mel_avg = (1 - alpha) * self._mel_avg + alpha * mel_t
self._mel_var = (1 - alpha) * self._mel_var + alpha * residual.pow(2)
self._transition_counts[b, prev, curr] += 1
self._frame_count += 1
confidence = min(1.0, self._frame_count / _WARMUP_FRAMES)
```

Any feature gated by a `confidence` ramp or requiring a warmup period is inherently non-frame-local.

---

## 4. Current Architecture (Before)

### 128D across 11 Groups, 3-Stage DAG

| Group | Name | Range | Dim | Stage | Dependencies | Domain |
|-------|------|-------|-----|-------|-------------|--------|
| A | Consonance | [0, 7) | 7 | 1 | — | Psychoacoustic |
| B | Energy | [7, 12) | 5 | 1 | — | Spectral |
| C | Timbre | [12, 21) | 9 | 1 | — | Spectral |
| D | Change | [21, 25) | 4 | 1 | — | Temporal |
| **E** | **Interactions** | **[25, 49)** | **24** | **2** | **cons, energy, timbre, change** | **Cross-domain** |
| F | Pitch/Chroma | [49, 65) | 16 | 1 | — | Tonal |
| G | Rhythm/Groove | [65, 75) | 10 | 2 | energy | Temporal |
| H | Harmony | [75, 87) | 12 | 2 | pitch_chroma | Tonal |
| **I** | **Information** | **[87, 94)** | **7** | **3** | **pitch_chroma, rhythm_groove, harmony** | **Information** |
| J | Timbre Extended | [94, 114) | 20 | 1 | — | Spectral |
| K | Modulation | [114, 128) | 14 | 1 | — | Psychoacoustic |

**Bold** = groups that violate the boundary rules and must be dissolved.

---

## 5. Dissolution Decisions

### 5.1 Group E — Interactions (24D) → DISSOLVE

**Violation**: Rule 3 (cross-domain binding)

All 24 features are element-wise products of features from different groups:

| Features | Formula | Violation |
|----------|---------|-----------|
| amp_x_roughness … amp_x_stumpf (4D) | Energy[0] × Consonance[0:4] | Cross-domain |
| vel_x_roughness … vel_x_stumpf (4D) | Energy[1] × Consonance[0:4] | Cross-domain |
| flux_x_roughness … flux_x_stumpf (4D) | Change[0] × Consonance[0:4] | Cross-domain |
| ent_x_roughness … ent_x_stumpf (4D) | Change[1] × Consonance[0:4] | Cross-domain |
| rough_x_warmth … seth_x_sharpness (4D) | Consonance[0:2] × Timbre[0:2] | Cross-domain |
| helm_x_tonalness … stumpf_x_autocorr (4D) | Consonance[2:4] × Timbre[2:6] | Cross-domain |

**Destination**: C³ input layer. Each C³ model that needs interaction terms will compute them as `r3[:, i] * r3[:, j]` in its own Extraction layer. This is trivial (one line per interaction) and eliminates 24 dimensions from R³.

**C³ impact**: 46 of 96 models currently consume interaction features. Their Extraction layers must add the relevant products. No model logic changes — only the source of the interaction terms moves from R³ output to C³ input computation.

### 5.2 Group I — Information (7D) → DISSOLVE

**Violation**: Rules 1, 2, and 4 (temporal state, listener model, prediction)

| # | Feature | Violation | Destination |
|---|---------|-----------|-------------|
| [87] | melodic_entropy | Accumulated 12×12 transition count matrix | **C³** — models that track tonal transitions |
| [88] | harmonic_entropy | KL(chroma_t ∥ chroma_avg) requires running EMA | **C³** — harmonic expectation models |
| [89] | rhythmic_info_content | Proxy for rhythm_groove[7] (event_density) | **Remove** — redundant, already in Group G |
| [90] | spectral_surprise | KL(mel_t ∥ mel_avg) requires running EMA | **C³** — prediction/surprise models |
| [91] | information_rate | MI(mel_t ; mel_{t-1}), see §5.2.1 | **H³** — velocity morph |
| [92] | predictive_entropy | 0.5·log(2πe·var(mel)) requires running variance | **C³** — prediction models |
| [93] | tonal_ambiguity | 1 − key_clarity (trivial proxy) | **Remove** — use harmony[0] directly |

**Total freed**: 7D (4 → C³, 1 → H³, 2 → removed as redundant)

#### 5.2.1 Information Rate — Boundary Case

The current implementation computes MI(mel_t; mel_{t-1}) using only frames t and t−1, which is technically ±1 frame (Rule 1 passes). However:

1. **Conceptually**, mutual information measures temporal redundancy — "how much does knowing frame t−1 reduce uncertainty about frame t?" This is a **relationship between frames**, not a **property of a frame**.
2. **Practically**, spectral_flux (Group D, [21]) already captures frame-to-frame spectral change via L2 norm. Information_rate adds an information-theoretic perspective on the same underlying phenomenon.
3. **Optimally**, MI is more valuable when computed at multiple temporal horizons (100ms, 500ms, 1s), which is H³'s domain.

**Decision**: Move to H³ as a velocity morph of spectral entropy. The ±1 frame version can be reimplemented in Change group if future analysis shows it provides unique discriminative power beyond spectral_flux.

### 5.3 Borderline Feature Analysis — Groups That Stay

#### 5.3.1 Group H — Harmony (12D, [75:87]) → STAYS

Despite the user's concern about `key_clarity` being "cognitive," code inspection confirms all 12 features are frame-local:

| Feature | Computation | ±Frame | Verdict |
|---------|-------------|--------|---------|
| key_clarity [75] | max(corr(chroma_t, 24 key templates)) | 0 | Frame-local template match |
| tonnetz (6D) [76:82] | chroma_t @ tonnetz_matrix | 0 | Algebraic transform |
| voice_leading_distance [82] | L1(chroma_t − chroma_{t−1}) | ±1 | Frame derivative |
| harmonic_change [83] | 1 − cos_sim(chroma_t, chroma_{t−1}) | ±1 | Frame derivative |
| tonal_stability [84] | key_clarity × (1 − avg_pool(hc, k=5)) | ±2 | 29ms window, within cochlear integration |
| diatonicity [85] | count(active_PCs > 0.05) | 0 | Frame-local |
| syntactic_irregularity [86] | KL(chroma_t ∥ best_key_template) | 0 | Frame-local (template, NOT running avg) |

Key distinction: `key_clarity` uses a **fixed template library** (Krumhansl-Kessler), not a learned or accumulated model. This is analogous to the medial geniculate body's pre-wired tonotopic organization. No prediction, no memory, no listener model. **R³-appropriate.**

In contrast, `harmonic_entropy` (Group I, [88]) computes KL against a **running chroma average** — that's the crucial difference that makes one R³ and the other C³.

#### 5.3.2 Group G — Rhythm/Groove (10D, [65:75]) → STAYS (with refactoring note)

**Issue**: Current implementation computes whole-clip autocorrelation and broadcasts scalar results to all frames:

```python
O = torch.fft.rfft(oenv, n=fft_size, dim=-1)  # whole clip FFT
R = torch.fft.irfft(O * O.conj(), n=fft_size, dim=-1)  # whole clip autocorr
...
result[:, :, 0] = tempo.unsqueeze(-1).expand_as(...)  # broadcast to all T
```

This violates Rule 1 (frame locality) in implementation but NOT in concept — beat tracking and tempo estimation are peripheral auditory processes (brainstem, inferior colliculus).

**Decision**: Rhythm features stay in R³ because:
1. 52+ models need tempo_estimate, 46+ need beat_strength
2. Beat tracking is subcortical/brainstem processing (pre-cognitive)
3. The concepts are R³-appropriate; only the implementation needs fixing

**Required refactoring** (not an ontological change):
- Replace whole-clip autocorrelation with sliding-window analysis (~2–4 second windows)
- Make all rhythm features **frame-varying** instead of clip-constant
- This aligns implementation with the boundary rules without changing the architecture

#### 5.3.3 Groups A, B, C, D, F, J, K → STAY (no issues)

All features in these 7 groups are Stage 1 (no dependencies), frame-local, and single-domain. They are unambiguously R³-appropriate.

**Known quality issues** (not ontological — defer to implementation roadmap):
- D[24] `distribution_concentration`: HHI×N bug (uniform and concentrated both → 1.0)
- C[12] `warmth`: duplicate of A[3] `stumpf_fusion` in concept
- C[13] `sharpness`: uses ~7kHz cutoff, should be Kuttruff 1.5kHz for `brightness`
- G[73] `tempo_stability`: placeholder (always returns 1.0)

---

## 6. New Dimension Map

### 6.1 Post-Dissolution Structure

After dissolving Groups E (24D) and I (7D), the core R³ is **97D** across **9 groups** in a **2-stage DAG** (Stage 3 disappears entirely):

| Group | Name | New Range | Dim | Stage | Dependencies |
|-------|------|-----------|-----|-------|-------------|
| A | Consonance | [0, 7) | 7 | 1 | — |
| B | Energy | [7, 12) | 5 | 1 | — |
| C | Timbre | [12, 21) | 9 | 1 | — |
| D | Change | [21, 25) | 4 | 1 | — |
| F | Pitch/Chroma | [25, 41) | 16 | 1 | — |
| G | Rhythm/Groove | [41, 51) | 10 | 2 | energy |
| H | Harmony | [51, 63) | 12 | 2 | pitch_chroma |
| J | Timbre Extended | [63, 83) | 20 | 1 | — |
| K | Modulation | [83, 97) | 14 | 1 | — |

### 6.2 Available Capacity

If the output tensor remains 128D for backward compatibility:

- **97D used** (core groups)
- **31D available** for gap-filling from measurement inventory

### 6.3 Recommended Gap Fills (from R3-MEASUREMENT-INVENTORY.md)

Priority order based on model demand frequency:

| Priority | Measurement | Demand | Dim | Target Group |
|----------|-------------|--------|-----|-------------|
| P1 | RMS delta (frame energy change) | 42 models | 1 | D (Change) |
| P1 | Spectral bandwidth | 34 models | 1 | C (Timbre) |
| P1 | Kuttruff brightness (1.5kHz cutoff) | 32 models | 1 | C (Timbre) — fix [13] |
| P1 | Spectral centroid delta | 28 models | 1 | D (Change) |
| P1 | Brightness delta | 24 models | 1 | D (Change) |
| P2 | Harmonic-to-noise ratio | 22 models | 1 | A (Consonance) |
| P2 | Spectral irregularity | 20 models | 1 | C (Timbre) |
| P2 | Dynamic range (peak/RMS) | 18 models | 1 | B (Energy) |
| P2 | Spectral rolloff | 16 models | 1 | C (Timbre) |
| P2 | Spectral skewness | 14 models | 1 | C (Timbre) |
| P2 | Spectral kurtosis | 14 models | 1 | C (Timbre) |
| P3 | Spectral crest | 12 models | 1 | C (Timbre) |
| P3 | Zero-crossing rate | 10 models | 1 | B (Energy) |
| P3 | Sub-band energy ratios (4D) | 8 models | 4 | B (Energy) |
| — | Reserve | — | 14 | Future discoveries |

This fills 18D of the 31D gap, leaving 13D as reserve for future acoustic measurements that may emerge from Phase 5+ model refinements or new literature.

**Note**: Specific feature selection and implementation are NOT frozen. Only the boundary rules (§2–3) are frozen. New features can be added to any group as long as they satisfy all five inclusion rules.

---

## 7. Impact on C³ and H³

### 7.1 C³ Models — Interaction Terms

**46 of 96 models** currently consume Group E interaction features. After dissolution:

- Each model's Extraction layer computes the needed products internally
- Implementation: `interaction_ij = r3_input[:, :, i] * r3_input[:, :, j]`
- No model logic changes; only the computation source moves from R³ output to C³ input
- Model input dimension from R³ decreases by 24, but effective feature space is identical (models compute what they need)

### 7.2 C³ Models — Information Features

**~20 of 96 models** currently consume Group I features. Redistribution:

| Feature | New Owner | Implementation |
|---------|-----------|----------------|
| melodic_entropy | C³ models (e.g., TEP, MER) | Each model maintains its own transition counter in compute() |
| harmonic_entropy | C³ models (e.g., HAC, HCE) | Each model maintains its own chroma EMA |
| spectral_surprise | C³ models (e.g., SPM, PEM) | Each model maintains mel baseline + KL |
| predictive_entropy | C³ models (e.g., PEM, PRE) | Each model maintains running variance |
| tonal_ambiguity | C³ models | Use 1 − harmony.key_clarity directly |
| rhythmic_info_content | C³ models | Use rhythm_groove.event_density directly |

**Key insight**: Each C³ model now owns its own temporal statistics, which means different models can have **different integration windows** and **different baseline decay rates**. This is actually more biologically accurate — different brain regions maintain different temporal contexts.

### 7.3 H³ — New Morphology Target

`information_rate` becomes an H³ velocity morph:

- **R³ source**: spectral entropy (Group D, [22]) or spectral flux (Group D, [21])
- **H³ demand**: `(r3_idx=22, horizon=delta, morph=velocity, law=memory)`
- **Computation**: H³ computes dH/dt at the requested horizon, yielding a richer multi-scale version of what information_rate approximated

### 7.4 Index Renumbering

After dissolution, all R³ indices shift. Every C³ model's `r3_demand` mapping must be updated:

| Old Group | Old Range | New Range | Shift |
|-----------|-----------|-----------|-------|
| A Consonance | [0, 7) | [0, 7) | 0 |
| B Energy | [7, 12) | [7, 12) | 0 |
| C Timbre | [12, 21) | [12, 21) | 0 |
| D Change | [21, 25) | [21, 25) | 0 |
| F Pitch/Chroma | [49, 65) | [25, 41) | −24 |
| G Rhythm/Groove | [65, 75) | [41, 51) | −24 |
| H Harmony | [75, 87) | [51, 63) | −24 |
| J Timbre Extended | [94, 114) | [63, 83) | −31 |
| K Modulation | [114, 128) | [83, 97) | −31 |

This is a one-time migration. All `r3_demand` tuples in 96 C³ model files, H³ demand specs, and any downstream consumers must be updated atomically.

---

## 8. Freeze Policy

### What Is Frozen (this document)

1. **The definition** (§1): R³ is an Early Perceptual Front-End
2. **The five inclusion rules** (§2): frame-local, no listener model, no cross-domain binding, no prediction, deterministic
3. **The exclusion rules** (§3): no EMA, no accumulated counts, no running variance, no cross-domain products
4. **The dissolution decisions** (§5): Group E and Group I are permanently removed from R³
5. **The boundary sentence**: immutable reference for future feature proposals

### What Can Still Evolve

1. **Feature count**: New features can be added (up to 128D or beyond) if they pass all five inclusion rules
2. **Feature quality**: Algorithms can be upgraded (e.g., proxy → standard → reference)
3. **Bug fixes**: Known issues (concentration bug, sharpness cutoff, tempo_stability placeholder) can be fixed
4. **Group internal structure**: Features can be rearranged within groups
5. **New groups**: New groups can be added if they satisfy all inclusion rules

### Feature Proposal Gate

Any proposed new R³ feature must pass this checklist before admission:

- [ ] Computable from frame t and at most ±2 neighbours?
- [ ] No running average, EMA, or accumulated state?
- [ ] No cross-domain feature products?
- [ ] No prediction, surprise, or expectation modelling?
- [ ] No learned parameters or trained weights?
- [ ] At least 4 C³ models demand it? (pragmatic threshold)
- [ ] Not redundant with an existing feature? (correlation < 0.95)

If any box is unchecked, the feature belongs in H³ (temporal) or C³ (cognitive), not R³.

---

## Appendix A: Complete Feature Inventory (Before vs After)

### Dissolved — Group E (24 features)

```
[25] amp_x_roughness          → C³ input layer
[26] amp_x_sethares           → C³ input layer
[27] amp_x_helmholtz          → C³ input layer
[28] amp_x_stumpf             → C³ input layer
[29] vel_x_roughness          → C³ input layer
[30] vel_x_sethares           → C³ input layer
[31] vel_x_helmholtz          → C³ input layer
[32] vel_x_stumpf             → C³ input layer
[33] flux_x_roughness         → C³ input layer
[34] flux_x_sethares          → C³ input layer
[35] flux_x_helmholtz         → C³ input layer
[36] flux_x_stumpf            → C³ input layer
[37] ent_x_roughness          → C³ input layer
[38] ent_x_sethares           → C³ input layer
[39] ent_x_helmholtz          → C³ input layer
[40] ent_x_stumpf             → C³ input layer
[41] rough_x_warmth           → C³ input layer
[42] rough_x_sharpness        → C³ input layer
[43] seth_x_warmth            → C³ input layer
[44] seth_x_sharpness         → C³ input layer
[45] helm_x_tonalness         → C³ input layer
[46] helm_x_clarity           → C³ input layer
[47] stumpf_x_smoothness      → C³ input layer
[48] stumpf_x_autocorr        → C³ input layer
```

### Dissolved — Group I (7 features)

```
[87] melodic_entropy           → C³ (transition-tracking models)
[88] harmonic_entropy          → C³ (harmonic expectation models)
[89] rhythmic_info_content     → Removed (redundant with G[72] event_density)
[90] spectral_surprise         → C³ (prediction/surprise models)
[91] information_rate          → H³ (velocity morph of spectral entropy)
[92] predictive_entropy        → C³ (prediction models)
[93] tonal_ambiguity           → Removed (trivial proxy of H[75] key_clarity)
```

### Retained — 97 Features (9 Groups)

```
Group A — Consonance [0:7]
  [0] roughness, [1] sethares_dissonance, [2] helmholtz_kang,
  [3] stumpf_fusion, [4] sensory_pleasantness, [5] inharmonicity,
  [6] harmonic_deviation

Group B — Energy [7:12]
  [7] amplitude, [8] velocity_A, [9] acceleration_A,
  [10] loudness, [11] onset_strength

Group C — Timbre [12:21]
  [12] warmth, [13] sharpness, [14] tonalness, [15] clarity,
  [16] spectral_smoothness, [17] spectral_autocorrelation,
  [18] tristimulus1, [19] tristimulus2, [20] tristimulus3

Group D — Change [21:25]
  [21] spectral_flux, [22] distribution_entropy,
  [23] distribution_flatness, [24] distribution_concentration

Group F — Pitch/Chroma [25:41]
  [25] chroma_C .. [36] chroma_B,
  [37] pitch_height, [38] pitch_class_entropy,
  [39] pitch_salience, [40] inharmonicity_index

Group G — Rhythm/Groove [41:51]
  [41] tempo_estimate, [42] beat_strength, [43] pulse_clarity,
  [44] syncopation_index, [45] metricality_index, [46] isochrony_nPVI,
  [47] groove_index, [48] event_density, [49] tempo_stability,
  [50] rhythmic_regularity

Group H — Harmony [51:63]
  [51] key_clarity,
  [52] tonnetz_fifth_x, [53] tonnetz_fifth_y,
  [54] tonnetz_minor_x, [55] tonnetz_minor_y,
  [56] tonnetz_major_x, [57] tonnetz_major_y,
  [58] voice_leading_distance, [59] harmonic_change,
  [60] tonal_stability, [61] diatonicity, [62] syntactic_irregularity

Group J — Timbre Extended [63:83]
  [63] mfcc_1 .. [75] mfcc_13,
  [76] spectral_contrast_1 .. [82] spectral_contrast_7

Group K — Modulation [83:97]
  [83] modulation_0_5Hz, [84] modulation_1Hz, [85] modulation_2Hz,
  [86] modulation_4Hz, [87] modulation_8Hz, [88] modulation_16Hz,
  [89] modulation_centroid, [90] modulation_bandwidth,
  [91] sharpness_zwicker, [92] fluctuation_strength,
  [93] loudness_a_weighted, [94] alpha_ratio,
  [95] hammarberg_index, [96] spectral_slope_0_500
```

---

*This document defines the ontological boundaries of R³. It is the constitutional reference for all future feature proposals, implementation decisions, and architectural debates. The boundary rules (§2–3) and dissolution decisions (§5) are frozen at v1.0.0. Implementation details evolve freely within these boundaries.*
