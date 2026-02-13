# R³ Gap Log — ASU (Auditory Salience Unit)

**Created**: 2026-02-13
**Unit**: ASU (Auditory Salience)
**Chat**: Chat 2 (BATCH 4)

---

## Gaps Found During C³ Revision

### SNEM (ASU-α1) — Selective Neural Entrainment Model

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G01 | `neural_entrainment_intensity` (ITPC measure) | Ding et al. 2025 | ITPC η²=0.14 across 1-12 Hz; measures phase coherence of entrainment | Medium — currently captured indirectly via BEP mechanism |
| ASU-G02 | `phase_locking_value` (inter-region PLV) | Yang et al. 2025 | PLV=0.76 frontal-parietal at fast tempo; measures auditory-motor coupling | Low — connectivity metric, not spectral feature |

**Notes:**
- SNEM's current R³ input mapping (~15D from Energy, Change, Interactions) is well-supported by literature
- The ITPC and PLV measures are neural response metrics, not acoustic/spectral features — they are better modeled as output dimensions rather than R³ inputs
- No strong evidence for missing R³ INPUT dimensions for SNEM

### IACM (ASU-α2) — Inharmonicity-Attention Capture Model

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G03 | `high_gamma_power_stg` (70-150 Hz power in STG) | Foo et al. 2016 | Dissonant chords → enhanced high gamma, p<0.001, 91% electrodes in STG | Low — neural response metric, not acoustic feature |
| ASU-G04 | `inharmonicity_index` (explicit inharmonicity measure) | Basinski 2025 | ApproxEntropy harmonic=0.02 vs inharmonic=0.19; currently approximated from tonalness+spectral_flatness | Medium — current R³ lacks direct inharmonicity measure; proxy via R³[14] tonalness + R³[16] spectral_flatness |

**Notes:**
- IACM's R³ mapping (~14D from Consonance, Energy, Timbre, Change, Interactions) is adequate
- The most notable gap is the lack of a direct `inharmonicity_index` in R³ — currently approximated by combining tonalness and spectral_flatness, which is reasonable but not exact
- The high gamma power measure is a neural response, not an acoustic feature — belongs in C³ output space

### CSG (ASU-α3) — Consonance-Salience Gradient

| Gap ID | Proposed R³ Feature | Source Paper | Evidence | Priority |
|--------|---------------------|-------------|----------|----------|
| ASU-G05 | `consonance_gradient` (continuous consonance level) | Fishman et al., Bravo 2017 | Phase-locked activity graded by consonance-dissonance; d=5.16 for salience | Low — adequately represented by R³[4] sensory_pleasantness + R³[0] roughness |

**Notes:**
- CSG's R³ mapping (~16D) is well-supported
- The consonance gradient is adequately represented by existing R³ features (roughness, sethares, sensory_pleasantness)
- New brain regions identified: amygdala, vmPFC, ventral striatum — extend the salience network beyond ACC/AI

### BARM (ASU-β1) — Beat Ability Regulatory Model

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G06 | R³ naming: [7] "amplitude" | Doc says `amplitude`, code is `velocity_A` | Low — project-wide naming convention (Phase 5) |
| ASU-G07 | R³ naming: [8] "loudness" | Doc says `loudness`, code is `velocity_D` | Low — project-wide naming convention (Phase 5) |
| ASU-G08 | R³ naming: [10] "spectral_flux" | Doc says `spectral_flux`, code is `onset_strength` | Low — project-wide naming convention (Phase 5) |
| ASU-G09 | R³ naming: [11] "onset_strength" | Doc says `onset_strength`, code is `rms_energy` | Low — project-wide naming convention (Phase 5) |
| ASU-G10 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide naming convention (Phase 5) |
| ASU-G11 | R³ naming: [22] "energy_change" | Doc says `energy_change`, code is `spectral_flatness` | Low — project-wide naming convention (Phase 5) |
| ASU-G12 | Code FULL_NAME mismatch | Code: "Bottom-up Attention Reflex Model" vs doc: "Beat Ability Regulatory Model" | Medium — Phase 5 code update |
| ASU-G13 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G14 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 14 tuples specified | Medium — Phase 5 code update |

**Notes:**
- BARM v2.1.0 expanded from 1→12 papers, 4→8 brain regions
- 6 R³ naming mismatches are ALL project-wide semantic-vs-computational naming convention, deferred to Phase 5
- 3 code-level mismatches (FULL_NAME, MECHANISM_NAMES, h3_demand) need Phase 5 code update
- No strong evidence for missing R³ INPUT dimensions

### STANM (ASU-β2) — Spectrotemporal Attention Network Model

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G15 | R³ naming: [8] "loudness" | Doc says `loudness`, code is `velocity_D` | Low — project-wide (Phase 5) |
| ASU-G16 | R³ naming: [10] "spectral_flux" | Doc says `spectral_flux`, code is `onset_strength` | Low — project-wide (Phase 5) |
| ASU-G17 | R³ naming: [14] "tonalness" | Doc says `tonalness`, code is `brightness_kuttruff` (real tonalness at [24]) | Low — project-wide (Phase 5) |
| ASU-G18 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide (Phase 5) |
| ASU-G19 | R³ naming: [22] "energy_change" | Doc says `energy_change`, code is `spectral_flatness` | Low — project-wide (Phase 5) |
| ASU-G20 | Code FULL_NAME slight mismatch | Code: "Spectro-Temporal Attention Network Model" (hyphen) vs doc: "Spectrotemporal Attention Network Model" | Low — Phase 5 code update |
| ASU-G21 | Code OUTPUT_DIM mismatch | Code: 10D vs doc: 11D (doc adds compensation_pred in Layer F) | Medium — Phase 5 code update |
| ASU-G22 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G23 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 16 tuples specified | Medium — Phase 5 code update |
| ASU-G24 | Code citations differ from doc | Code: Coffey 2017 + Albouy 2019 vs doc: Haiduk 2024 primary | Low — Phase 5 code update |

**Notes:**
- STANM v2.1.0 expanded from 1→12 papers, 3→8 brain regions
- 5 R³ naming mismatches are project-wide semantic-vs-computational naming convention, deferred to Phase 5
- OUTPUT_DIM mismatch (10 vs 11) is significant — doc specifies compensation_pred as 11th dimension
- No evidence for missing R³ INPUT dimensions

### AACM (ASU-β3) — Aesthetic-Attention Coupling Model

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G25 | R³ naming: [0] "roughness" | Doc says `roughness`, code is `perfect_fifth_ratio`; roughness_total is at [5] | Medium — possible index error, not just naming |
| ASU-G26 | R³ naming: [1] "sethares_dissonance" | Doc says `sethares_dissonance`, code is `euler_gradus`; both consonance measures | Low — project-wide naming (Phase 5) |
| ASU-G27 | R³ naming: [3] "pleasant" | Doc says `pleasant`, code is `stumpf_fusion`; sensory_pleasantness is at [4] | Medium — possible off-by-one index error |
| ASU-G28 | R³ naming: [7] "amplitude" | Doc says `amplitude`, code is `velocity_A` | Low — project-wide naming (Phase 5) |
| ASU-G29 | R³ naming: [8] "loudness" | Doc says `loudness`, code is `velocity_D` | Low — project-wide naming (Phase 5) |
| ASU-G30 | R³ naming: [13] "tristimulus_1" | Doc says `tristimulus_1`, code is `sharpness`; tristimulus1 at [18] | Medium — possible index error |
| ASU-G31 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide naming (Phase 5) |
| ASU-G32 | Code FULL_NAME mismatch | Code: "Auditory Attention Control Model" vs doc: "Aesthetic-Attention Coupling Model" | Medium — Phase 5 code update |
| ASU-G33 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G34 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 12 tuples specified | Medium — Phase 5 code update |

**Notes:**
- AACM v2.1.0 expanded from 1→12 papers, 3→8 brain regions
- 3 R³ index mismatches appear more severe than project-wide naming (ASU-G25: roughness at [0] vs [5]; ASU-G27: pleasant at [3] vs [4]; ASU-G30: tristimulus_1 at [13] vs [18])
- These may be genuine index mapping errors from v1.0.0→v2.0.0 migration, not just naming convention differences
- Code FULL_NAME "Auditory Attention Control Model" is completely different from doc name

### PWSM (ASU-γ1) — Precision-Weighted Salience Model

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G35 | R³ naming: [10] "spectral_flux" | Doc says `spectral_flux`, code is `onset_strength` | Low — project-wide naming convention (Phase 5) |
| ASU-G36 | R³ naming: [11] "onset_strength" | Doc says `onset_strength`, code is `rms_energy` | Low — project-wide naming convention (Phase 5) |
| ASU-G37 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide naming convention (Phase 5) |
| ASU-G38 | R³ naming: [22] "energy_change" | Doc says `energy_change`, code is `spectral_flatness` | Low — project-wide naming convention (Phase 5) |
| ASU-G39 | R³ naming: [23] "timbre_change" | Doc says `timbre_change`, code is `zero_crossing_rate` | Low — project-wide naming convention (Phase 5) |
| ASU-G40 | R³ naming: [24] "pitch_change" | Doc says `pitch_change`, code is `tonalness` | Low — project-wide naming convention (Phase 5) |
| ASU-G41 | Code FULL_NAME mismatch | Code: "Pop-out Warning Salience Model" vs doc: "Precision-Weighted Salience Model" | Medium — Phase 5 code update |
| ASU-G42 | Code OUTPUT_DIM mismatch | Code: 10D vs doc: 9D | Medium — Phase 5 code update |
| ASU-G43 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G44 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 16 tuples specified | Medium — Phase 5 code update |

**Notes:**
- PWSM v2.1.0 expanded from 1→12 papers, 2→8 brain regions
- 6 R³ naming mismatches are ALL project-wide semantic-vs-computational naming convention, deferred to Phase 5
- 4 code-level mismatches (FULL_NAME, OUTPUT_DIM, MECHANISM_NAMES, h3_demand) need Phase 5 code update
- OUTPUT_DIM mismatch (10 vs 9) — code has 10D, doc specifies 9D
- No strong evidence for missing R³ INPUT dimensions

### DGTP (ASU-γ2) — Domain-General Temporal Processing

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G45 | R³ naming: [7] "amplitude" | Doc says `amplitude`, code is `velocity_A` | Low — project-wide naming convention (Phase 5) |
| ASU-G46 | R³ naming: [8] "loudness" | Doc says `loudness`, code is `velocity_D` | Low — project-wide naming convention (Phase 5) |
| ASU-G47 | R³ naming: [10] "spectral_flux" | Doc says `spectral_flux`, code is `onset_strength` | Low — project-wide naming convention (Phase 5) |
| ASU-G48 | R³ naming: [11] "onset_strength" | Doc says `onset_strength`, code is `rms_energy` | Low — project-wide naming convention (Phase 5) |
| ASU-G49 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide naming convention (Phase 5) |
| ASU-G50 | R³ naming: [24] "pitch_change" | Doc says `pitch_change`, code is `tonalness` | Low — project-wide naming convention (Phase 5) |
| ASU-G51 | Code FULL_NAME mismatch | Code: "Deviance-Gated Temporal Processing" vs doc: "Domain-General Temporal Processing" | Medium — Phase 5 code update |
| ASU-G52 | Code OUTPUT_DIM mismatch | Code: 10D vs doc: 9D | Medium — Phase 5 code update |
| ASU-G53 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G54 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 9 tuples specified | Medium — Phase 5 code update |

**Notes:**
- DGTP v2.1.0 expanded from 2→12 papers, 4→8 brain regions
- 6 R³ naming mismatches are ALL project-wide semantic-vs-computational naming convention, deferred to Phase 5
- 4 code-level mismatches (FULL_NAME, OUTPUT_DIM, MECHANISM_NAMES, h3_demand) need Phase 5 code update
- OUTPUT_DIM mismatch (10 vs 9) — code has 10D, doc specifies 9D
- No strong evidence for missing R³ INPUT dimensions

### SDL (ASU-γ3) — Salience-Dependent Lateralization

| Gap ID | Issue | Details | Priority |
|--------|-------|---------|----------|
| ASU-G55 | R³ naming: [7] "amplitude" | Doc says `amplitude`, code is `velocity_A` | Low — project-wide naming convention (Phase 5) |
| ASU-G56 | R³ naming: [8] "loudness" | Doc says `loudness`, code is `velocity_D` | Low — project-wide naming convention (Phase 5) |
| ASU-G57 | R³ naming: [10] "spectral_flux" | Doc says `spectral_flux`, code is `onset_strength` | Low — project-wide naming convention (Phase 5) |
| ASU-G58 | R³ naming: [15] "spectral_centroid" | Doc says `spectral_centroid`, code matches — no mismatch | Low — verified |
| ASU-G59 | R³ naming: [18] "pitch_salience" | Doc says `pitch_salience`, code is `tristimulus3` | Low — project-wide naming convention (Phase 5) |
| ASU-G60 | R³ naming: [21] "spectral_change" | Doc says `spectral_change`, code is `spectral_flux` | Low — project-wide naming convention (Phase 5) |
| ASU-G61 | Code FULL_NAME mismatch | Code: "Stimulus-Driven Listening" vs doc: "Salience-Dependent Lateralization" | Medium — Phase 5 code update |
| ASU-G62 | Code OUTPUT_DIM mismatch | Code: 10D vs doc: 9D | Medium — Phase 5 code update |
| ASU-G63 | Code MECHANISM_NAMES mismatch | Code: `("ASA",)` vs doc: `("BEP", "ASA")` | Medium — Phase 5 code update |
| ASU-G64 | Code h3_demand empty | Code: `h3_demand = ()` vs doc: 18 tuples specified | Medium — Phase 5 code update |

**Notes:**
- SDL v2.1.0 expanded from 1→12 papers, 3→8 brain regions
- 5 R³ naming mismatches are project-wide semantic-vs-computational naming convention, deferred to Phase 5
- R³[15] spectral_centroid is correctly named in both doc and code — verified
- 4 code-level mismatches (FULL_NAME, OUTPUT_DIM, MECHANISM_NAMES, h3_demand) need Phase 5 code update
- OUTPUT_DIM mismatch (10 vs 9) — code has 10D, doc specifies 9D
- No strong evidence for missing R³ INPUT dimensions
