# R³ Gap Log — PCU (Predictive Coding Unit)

**Created**: 2026-02-13
**Unit**: PCU (Predictive Coding)
**Chat**: Chat 5 (BATCH 7)

---

## Gaps Found During C³ Revision

### HTP (PCU-α1) — Hierarchical Temporal Prediction

**Status:** No R³ gaps found.
- R³ mapping uses ~20D of 49D (Energy, Timbre, Change, Interactions) — all indices verified correct
- H³ demand: 18 tuples (0.78%) — correctly specified
- Doc v2.1.0 with 16 papers — comprehensive coverage across MEG, iEEG, ECoG, EEG, single-unit, behavioral, computational
- 10 PCU-tagged catalog papers reviewed; none add critical missing evidence to HTP specifically (more relevant to other PCU submodels)
- Code-doc alignment: perfect match (OUTPUT_DIM=12, MECHANISM_NAMES, h3_demand, brain_regions)

### SPH (PCU-α2) — Spatiotemporal Prediction Hierarchy

**Status:** No critical R³ gaps. One project-wide naming note.
- R³ mapping uses ~22D of 49D — all INDEX ranges verified correct
- H³ demand: 16 tuples (0.69%) — correctly specified
- Doc v2.1.0 with 11 papers (5 empirical MEG/iEEG + 2 single-neuron/iEEG + 1 MEG + 3 reviews)
- Code-doc mismatch expected (code at v2.0.0, doc at v2.1.0 — Phase 5 reconciliation)
- Code: OUTPUT_DIM=11, MECHANISM_NAMES=("PPC",) → Doc: OUTPUT_DIM=14, MECHANISMS=("PPC","TPC","MEM") — code needs Phase 5 update
- **NOTE (project-wide):** R³ feature names in docs use semantic labels (e.g., "amplitude", "loudness", "spectral_flux") while code uses computational names (velocity_A, velocity_D, onset_strength). Index ranges [0:7], [7:12], [12:21], [21:25], [25:49] are CORRECT. Interaction features use "x_l0l5" notation in docs vs "cons_x_energy" naming in code. This is consistent across ALL batches — Phase 5 should reconcile naming.

### ICEM (PCU-α3) — Information Content Emotion Model

**Status:** No R³ gaps found. Minor paper count correction (12→11).
- R³ mapping uses ~18D of 49D — indices verified correct
- H³ demand: 15 tuples (0.65%) — correctly specified
- Doc v2.1.0 with 11 papers (10 empirical + 1 theoretical) — comprehensive across psychophysiology, fMRI, PET, EEG
- Corrected paper count in header and Section 12 (was 12, actually 11)
- Code at v2.0.0 (OUTPUT_DIM=11, MECHANISMS=("AED","C0P")) → needs Phase 5 update to 13D with ("PPC","TPC","MEM")

### PWUP (PCU-β1) — Precision-Weighted Uncertainty Processing

**Status:** Two R³ index mismatches found (same project-wide naming issue).
- R³ mapping uses ~14D of 49D — Energy + Change + Interactions
- H³ demand: 14 tuples (0.61%) — correctly specified
- Doc v2.1.0 with 12 papers — comprehensive across EEG, MEG, behavioral, fMRI
- Code at v2.0.0 (OUTPUT_DIM=10 matches doc, MECHANISM_NAMES=("PPC",)) → needs Phase 5 update to ("PPC","TPC","MEM")

#### Index Mismatches (same project-wide naming convention):
1. **R³[14] "tonalness"** — Doc references R³[14] as `tonalness`. Actual R³[14] is `brightness_kuttruff` (Group C: Timbre). Real `tonalness` is at R³[24] (Group D: Change). **Action needed**: Remap to R³[24] in Phase 5.
2. **R³[5] "periodicity"** — Doc references R³[5] as `periodicity`. Actual R³[5] is `roughness_total` (Group A: Consonance). No `periodicity` feature exists in the 49D R³ space. **Action needed**: Determine correct mapping in Phase 5 (closest: spectral autocorrelation derived from tristimulus or onset patterns).

### WMED (PCU-β2) — Working Memory-Entrainment Dissociation

**Status:** No R³ gaps found. Minor paper count correction (12→11).
- R³ mapping uses ~15D of 49D — Energy + Change + Interactions
- H³ demand: 16 tuples (0.69%) — correctly specified
- Doc v2.1.0 with 11 papers (EEG + MEG + behavioral + reviews)
- Corrected paper count in header, Section 3.2, Section 12, and Section 14 (was 12, actually 11 — "Noboa multi-finding" counted as separate paper)
- Code at v2.0.0 (OUTPUT_DIM=10, doc says 11D, MECHANISM_NAMES=("MEM","AED")) → needs Phase 5 update to 11D with ("PPC","TPC","MEM")

### UDP (PCU-β3) — Uncertainty-Driven Pleasure

**Status:** 4 R³ index/name mismatches found; 2 minor potential features noted.
- R³ mapping uses ~17D of 49D — Consonance + Energy + Timbre + Change + Interactions
- H³ demand: 16 tuples (0.69%) — correctly specified
- Doc v2.1.0 with 12 papers — comprehensive across behavioral, fMRI, PET, EEG, psychophysiology, computational
- Code at v2.0.0 (OUTPUT_DIM=10 matches doc, MECHANISM_NAMES=("C0P",), FULL_NAME="Uncertainty-Driven Prediction" vs doc "Uncertainty-Driven Pleasure") → needs Phase 5 update to ("PPC","TPC","MEM")

#### Index Mismatches (Doc vs Code R³ Registry)

1. **R³[5] "periodicity"** — Doc Section 4.1 and 5.1 reference R³[5] as `periodicity`. Actual R³[5] is `roughness_total` (Group A: Consonance). No `periodicity` feature exists in the 49D R³ space. **Action needed**: Determine correct R³ mapping in Phase 5.

2. **R³[10] "spectral_flux"** — Doc Section 4.1 and 5.1 reference R³[10] as `spectral_flux`. Actual R³[10] is `onset_strength` (Group B: Energy). Real spectral_flux is at R³[21] (Group D: Change). **Action needed**: Remap to R³[21] for spectral_flux, or use R³[10] onset_strength as an event detection proxy.

3. **R³[14] "tonalness"** — Doc Section 4.1 references R³[14] as `tonalness`. Actual R³[14] is `brightness_kuttruff` (Group C: Timbre). Real `tonalness` is at R³[24] (Group D: Change). **Action needed**: Remap to R³[24] in Phase 5.

4. **R³[21] "spectral_change"** — Doc Section 4.1 and 5.1 reference R³[21] as `spectral_change`. Actual R³[21] is `spectral_flux` (Group D: Change). The name `spectral_change` does not exist in R³. **Action needed**: Rename to `spectral_flux` throughout. The function (frame-to-frame spectral change) is the same; only the name is wrong.

#### Potential Missing Features

1. **Information content (IC)**: Cheung 2019, Gold 2019, and Gold 2023 all use IDyOM-derived information content (surprise) and entropy as the primary predictors of pleasure. R³ has no note-level IC feature — this belongs to the MEM mechanism or a dedicated sequence model, not static R³ spectral features. **Severity: None for R³** — correctly handled by MEM mechanism's prediction buffer and long-term memory.

2. **1/f spectral slope**: Borges et al. 2019 show that 1/f scaling of neural activity predicts music pleasure. The R³ space does not include a 1/f spectral slope feature. However, 1/f slope of the *audio* is partially captured by `spectral_flatness` (R³[22]). **Severity: Minor** — 1/f scaling of neural EEG is not an audio feature.

3. **Key clarity / tonal stability**: Mencke 2019 uses MIR-derived key clarity (d=3.0 tonal vs atonal). Doc maps this to `tonalness` (R³[14], but see index error above — actual tonalness at R³[24]). Tonalness (harmonic-to-noise ratio) is a reasonable but imperfect proxy for key clarity (Krumhansl-Schmuckler key-profile correlation). **Severity: Minor**.

#### Summary: 4 index/name mismatches need correction. Two minor potential features (1/f slope, key clarity) are adequately proxied by existing R³ dimensions.

### CHPI (PCU-β4) — Cross-Modal Harmonic Predictive Integration [NEW]

**Status:** Same project-wide R³ naming convention issues. Document comprehensive (18 papers, 11D, 20 H³ tuples).
- R³ mapping uses ~22D of 49D — Consonance + Energy + Timbre + Change + Interactions
- H³ demand: 20 tuples (0.87%) — correctly specified
- Doc v2.1.0 with 18 papers — extensive cross-domain synthesis (DTI, fMRI, MEG, EEG, behavioral, psychophysiology, computational)
- NEW model — no code file exists yet (Phase 5 will create)
- Section 12 parenthetical fixed (was missing Chang 2025 from the 18-paper list)
- 1 external citation: Paraskevopoulos 2015 (NOT in C³ catalog, flagged in doc, supported by Paraskevopoulos 2022 which IS in catalog)

#### R³ Index Issues (project-wide naming convention — same as all other PCU models):
- R³[0] doc "roughness" → actual: perfect_fifth_ratio
- R³[5] doc "periodicity" → actual: roughness_total
- R³[6] doc "harmonic_change" → actual: consonance_mean
- R³[9] doc "spectral_centroid" → actual: loudness
- R³[10] doc "spectral_flux" → actual: onset_strength
- R³[14] doc "tonalness" → actual: brightness_kuttruff (real tonalness at R³[24])
- R³[21] doc "spectral_change" → actual: spectral_flux
- R³[22] doc "energy_change" → actual: spectral_flatness
- R³[23] doc "roughness_change" → actual: zero_crossing_rate

All indices use the same semantic labels as other PCU models. Phase 5 reconciliation will align names across all docs.

### IGFE (PCU-γ1) — Individual Gamma Frequency Enhancement

**Status:** Same project-wide R³ naming convention issues. No critical gaps.
- R³ mapping uses ~14D of 49D — Consonance + Energy + Timbre + Interactions
- H³ demand: 18 tuples (0.78%) — correctly specified
- Doc v2.1.0 with 10 papers — γ-tier (3 direct gamma-cognition + 2 gamma mechanisms + 3 entrainment-cognition + 2 cortical entrainment)
- Code at v2.0.0 (OUTPUT_DIM=10, doc says 9D; MECHANISM_NAMES=("TPC",), doc says ("PPC","TPC","MEM"); FULL_NAME="Imagery-Guided Feature Enhancement" vs doc "Individual Gamma Frequency Enhancement") → needs Phase 5 update

### MAA (PCU-γ2) — Multifactorial Atonal Appreciation

**Status:** Same project-wide R³ naming convention issues. No critical gaps.
- Doc v2.1.0 with 12 papers — γ-tier (behavioral, fMRI, PET, EEG, psychophysiology)
- 10D output, paper count verified (12 in Section 13, 12 in Section 12)
- Code at v2.0.0 (OUTPUT_DIM=10 ✓; MECHANISM_NAMES=("ASA",), doc says ("PPC","TPC","MEM"); FULL_NAME="Musical Agentic Attention" vs doc "Multifactorial Atonal Appreciation") → needs Phase 5 update

### PSH (PCU-γ3) — Prediction Silencing Hypothesis

**Status:** Same project-wide R³ naming convention issues. Code already at v2.1.0.
- Doc v2.1.0 with 12 papers — γ-tier (MEG, EEG, computational, reviews)
- 10D output, paper count verified (12 in Section 13, 12 in Section 12)
- Code at v2.1.0 ✓ (OUTPUT_DIM=10 ✓; MECHANISM_NAMES=("PPC","TPC","MEM") ✓; FULL_NAME matches ✓; h3_demand populated with 18 tuples; paper_count=12; 4 brain regions)
- ONLY PCU model where code matches doc at v2.1.0

---

## Summary

| Model | Gaps Found | Priority Gaps |
|-------|------------|---------------|
| HTP | 0 | None — all R³ indices verified correct |
| SPH | 0 critical, 1 project-wide note | R³ naming convention: doc labels vs code names (indices correct) |
| ICEM | 0 R³ gaps, 1 minor count fix | Paper count corrected 12→11 |
| PWUP | 2 index mismatches | R³[14] tonalness→brightness_kuttruff, R³[5] periodicity→roughness_total |
| WMED | 0 R³ gaps, 1 minor count fix | Paper count corrected 12→11 |
| UDP | 4 index mismatches + 2 minor | 4 index/name corrections + FULL_NAME mismatch |
| CHPI | 9 naming issues (project-wide) | Same R³ naming convention; 1 external citation; Sec 12 fixed |
| IGFE | 0 critical, project-wide naming | Code OUTPUT_DIM mismatch (10 vs doc 9), FULL_NAME wrong |
| MAA | 0 critical, project-wide naming | FULL_NAME mismatch in code |
| PSH | 0 critical, project-wide naming | Code already at v2.1.0 (only PCU model fully synced) |
| **Total** | **5 models with index issues, all project-wide** | **Phase 5 reconciliation needed for naming + code sync** |
