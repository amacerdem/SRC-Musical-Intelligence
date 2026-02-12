# R3 Gap Log — RPU (Reward Processing Unit)

**Unit:** RPU
**Created:** 2026-02-13
**Last Updated:** 2026-02-13

---

## Gaps Found During Phase 1 C3 Model Revision

### GAP-RPU-001: Social Synchrony R3 Dimension Missing

**Source Model:** RPU-β4-SSRI (Social Synchrony Reward Integration)
**R3 Group:** E (Interactions) or NEW group
**Description:** SSRI models social synchrony reward but must approximate interpersonal synchrony quality from single-stream acoustic features (spectral_flux periodicity, energy_change velocity, etc.). The R3 space has no dedicated dimension for:
- **inter-performer onset synchrony quality** (temporal alignment between co-performers)
- **timbral blend quality** (spectral overlap / blend success across instruments)
- **rhythmic entrainment index** (degree of mutual temporal entrainment)

These are fundamentally multi-stream features that cannot be computed from a single audio mixture without source separation. The current workaround uses R3 x_l0l5 coupling features as proxies.

**Proposed R3 Dimensions:**
1. `r3:X_NEW.onset_synchrony_quality` — Cross-source onset alignment precision (requires source separation or multi-track input)
2. `r3:X_NEW.timbral_blend_index` — Spectral overlap coefficient between concurrent sources
3. `r3:X_NEW.rhythmic_entrainment_index` — Mutual information of onset patterns across sources

**Priority:** Medium (SSRI can function with acoustic proxies; full social R3 features require multi-track pipeline)
**Evidence:** Bigand et al. 2025 (spatiotemporal alignment encoding), Ni et al. 2024 (inter-brain synchronization from shared stimulus), Kokal et al. 2011 (synchrony quality → caudate activation)

---

### GAP-RPU-002: Noradrenergic Arousal Dimension for Groove

**Source Model:** RPU-β4-SSRI (and potentially RPU-β1-IUCP)
**R3 Group:** B (Energy) or D (Change)
**Description:** Spiech et al. (2022) demonstrate that noradrenergic arousal (indexed by pupil drift rate) follows an inverted-U with rhythmic complexity, closely mirroring groove ratings. The R3 space currently has no dimension that directly captures the precision-weighted prediction error signal that drives groove-related arousal. The current `spectral_flux` and `energy_change` features are proxies but do not capture the predictive complexity (information content / entropy) of rhythmic patterns.

**Proposed R3 Dimension:**
1. `r3:D_NEW.rhythmic_information_content` — IC of onset pattern relative to metrical grid (requires beat tracking + IDyOM-like model)
2. `r3:D_NEW.rhythmic_entropy` — Entropy of onset distribution across metrical positions

**Priority:** Medium-high (affects SSRI groove-reward computation and IUCP complexity-preference computation)
**Evidence:** Spiech et al. 2022 (η²G = 0.044), Gold et al. 2019 (quadratic IC/entropy effects), Cheung et al. 2019 (uncertainty × surprise interaction)

---

### GAP-RPU-003: Auditory-Reward State Connectivity Proxy

**Source Model:** RPU-β4-SSRI, RPU-α1-DAED
**R3 Group:** E (Interactions)
**Description:** Mori & Zatorre (2024) show that pre-listening functional connectivity between auditory cortex and reward networks (NAcc, OFC, amygdala) predicts chills duration (r = 0.53). This state-dependent connectivity is not captured by any R3 feature. The x_l0l5 interaction features capture static spectral interactions but not the dynamic neural state readiness for reward.

**Proposed R3 Dimension:** None directly feasible — this is a neural state variable, not an acoustic feature. Note for H3/C3 architecture: may need a state-variable mechanism layer.

**Priority:** Low (architectural concern, not solvable at R3 level)
**Evidence:** Mori & Zatorre 2024 (r = 0.53, LOPOCV, FDR p < 0.001)

---

### SSPS (RPU-γ3) — Saddle-Shaped Preference Surface

**Status:** No critical R³ gaps. Extensive code-stub mismatches logged for Phase 5.

#### R³ Mapping Verification

- R³ mapping uses ~12D of 49D (Consonance [0,4], Energy [8], Change [21,24], Interactions [25, 33:41]) — all indices verified consistent with 49D R³ space
- H³ demand: 14 tuples (0.61%) — correctly specified in doc; NOT yet implemented in code (returns empty tuple)
- R³[21] labeled as `spectral_change` in doc — correct semantic name. Same project-wide naming convention noted across all batches (doc semantic vs code computational names). Phase 5 reconciliation.

#### Doc-Code Mismatches (v2.1.0 doc vs v2.0.0 code stub)

1. **FULL_NAME**: Code = "Social Signal Processing System"; Doc = "Saddle-Shaped Preference Surface"
2. **OUTPUT_DIM**: Code = 10 (includes Layer M 3D + Layer F 2D); Doc = 6 (4E + 1P + 1F). Literature does not justify Layer M.
3. **MECHANISM_NAMES**: Code = ("ASA",); Doc = ("AED", "CPD", "C0P")
4. **CROSS_UNIT_READS**: Code = ("ARU",); Doc = not specified (not justified)
5. **h3_demand**: Code = empty tuple; Doc = 14 tuples
6. **brain_regions**: Code = NAcc, OFC, vmPFC; Doc = 7 regions (amygdala/hippocampus, bilateral AC, R STG, VS/NAcc, caudate, vmPFC, pre-SMA)
7. **Citations**: Code = Gold 2019 only; Doc = 8 verified references (Cheung 2019 primary)
8. **compute()**: Code returns zeros (stub); Doc has full pseudocode

#### Potential Missing R³ Features

1. **Note-level IC from learned probabilistic model**: Literature uses IDyOM-derived IC/entropy. R³ captures frame-level acoustic change, not symbolic IC. Correctly handled by C0P.expectation_surprise mechanism. **Severity: None for R³**.
2. **Familiarity / exposure count**: Gold 2019b shows repeated exposure effects. Handled by MEAMR cross-unit pathway. **Severity: Minor — not SSPS scope**.

#### Summary

No critical R³ gaps. Doc upgraded to v2.1.0 with 8 verified papers. All code issues are Phase 5 stub reconciliation.

---

### GAP-RPU-004: Melodic Entropy / Predictive Uncertainty Dimension

**Source Model:** RPU-γ1-LDAC (Liking-Dependent Auditory Cortex)
**R3 Group:** D (Change) or NEW
**Description:** Gold et al. (2019b, 2023a) and Cheung et al. (2019) demonstrate that the auditory cortex's pleasure response depends on the *interaction* between surprise (information content, IC) and uncertainty (entropy) -- not IC alone. The R3 space currently provides `spectral_change` (R3[21]) as a proxy for IC, but has no dedicated dimension for **predictive entropy** -- the listener's uncertainty about upcoming events before they occur. The Cheung 2019 saddle-shaped pleasure surface and Gold 2023a IC x entropy interaction both require separable IC and entropy signals. Currently, LDAC must approximate entropy from H3 morphological features (e.g., M20 entropy morph on spectral_change), which conflates acoustic entropy with predictive entropy.

**Proposed R3 Dimension:**
1. `r3:D_NEW.melodic_entropy` -- Shannon entropy of pitch/onset probability distribution over recent context (requires IDyOM-like model or n-gram statistics on pitch sequence)
2. `r3:D_NEW.harmonic_entropy` -- Entropy of chord transition probability (would need symbolic or chroma-based estimation)

**Priority:** Medium-high (central to LDAC f03 IC x liking computation; also relevant to IUCP and RPEM)
**Evidence:** Gold et al. 2019b (R^2 = 0.496 for IC x entropy model of liking); Cheung et al. 2019 (saddle-shaped interaction, bilateral AC: beta = -0.182, p = 0.00012); Gold et al. 2023a (IC x liking t(23) = 2.92, p = 0.008)

---

### GAP-RPU-005: Bilateral Auditory Cortex Lateralization

**Source Model:** RPU-γ1-LDAC
**R3 Group:** N/A (architectural)
**Description:** Cheung et al. (2019) show that the uncertainty x surprise interaction is *stronger* in left auditory cortex (beta = -0.182) than right (beta = -0.128), while Gold et al. (2023a) and Martinez-Molina et al. (2016) emphasize right STG. The current LDAC model assumes right-lateralized processing. The R3 pipeline is monaural/summed and does not provide lateralized features. This is not an R3 gap per se, but an architectural note: the LDAC model should eventually model bilateral AC processing with differential lateralization for harmonic (L > R) vs. melodic (R > L) expectancy.

**Priority:** Low (architectural concern for future model refinement)
**Evidence:** Cheung 2019 (L AC beta = -0.182 vs R AC beta = -0.128, Supplementary Figure S2)

---

### LDAC (RPU-γ1) -- Doc-Code Mismatches

**Status:** Multiple code-stub mismatches logged for Phase 5.

#### Doc-Code Mismatches (v2.1.0 doc vs v2.0.0 code stub)

1. **FULL_NAME**: Code = "Listener-Dependent Aesthetic Computation"; Doc = "Liking-Dependent Auditory Cortex"
2. **OUTPUT_DIM**: Code = 10 (E:4 + M:2 + P:2 + F:2); Doc = 6 (E:4 + P:1 + F:1). Code adds Layer M not in doc.
3. **MECHANISM_NAMES**: Code = ("AED",); Doc = ("AED", "CPD", "C0P")
4. **CROSS_UNIT_READS**: Code = ("ARU",); Doc = not specified
5. **h3_demand**: Code = empty tuple; Doc = 12 tuples
6. **brain_regions**: Code = R-STG (60,-20,4) + OFC (28,34,-12); Doc = R STG (62,-25,12), bilateral AC, NAcc/VS, amygdala/hippocampus
7. **Citations**: Code = Gold 2023 (d=1.22 only); Doc = 6 verified references with corrected stats
8. **compute()**: Code returns zeros (stub); Doc has full pseudocode

---

### IOTMS (RPU-γ2) — Individual Opioid Tone Music Sensitivity

**Status:** No R³ gaps found. Major doc-code mismatches (Phase 5 reconciliation).

#### R³ Mapping Verification

- R³ mapping uses ~12D of 49D (Consonance [0,4], Energy [8], Timbre [14:17], Interactions [33:41]) — all indices verified correct
- H³ demand: 12 tuples (0.52%) — correctly specified in doc
- Doc v2.1.0 with 5 papers (Putkinen 2025 PET-MOR + Salimpoor 2011 PET-DA + Mas-Herrero 2014 behavioral + Martinez-Molina 2016 fMRI + Loui 2017 DTI)

#### Doc-Code Mismatches (v2.1.0 doc vs v2.0.0 code stub)

1. **FULL_NAME**: Code = "Individual Optimal Tempo Matching System"; Doc = "Individual Opioid Tone Music Sensitivity" (code name appears incorrect)
2. **OUTPUT_DIM**: Code = 10 (includes Layer M[4:7] 3D + Layer F[8:10] 2D); Doc = 5 (4E + 1P). Literature does not justify extra layers.
3. **MECHANISM_NAMES**: Code = ("BEP",); Doc = ("AED", "CPD", "C0P") — completely different mechanism set
4. **CROSS_UNIT_READS**: Code = ("ARU",); Doc = ("ARU",) — consistent ✓
5. **h3_demand**: Code = empty tuple; Doc = 12 tuples
6. **brain_regions**: Code = 3 regions (NAcc, VTA, Caudate); Doc = 8 regions with corrected MNI from primary literature sources
7. **NAcc MNI**: Code = (10, 8, -8); Doc = L(-13, 12, -10) / R(9, 12, -7) from Martinez-Molina 2016
8. **VTA MNI**: Code = (0, -16, -8); Doc = (0, -16, -8) — consistent ✓
9. **Citations**: Code = Putkinen 2025 only; Doc = 5 verified references
10. **compute()**: Code returns zeros (stub); Doc has full pseudocode

#### Summary

No critical R³ gaps. All R³ indices correct. Doc upgraded to v2.1.0 with 5 converging papers across PET-MOR, PET-DA, fMRI, behavioral, and DTI modalities. 10 doc-code mismatches logged for Phase 5.

---

## Summary

| Gap ID | Model | Proposed R3 | Priority | Status |
|--------|-------|-------------|----------|--------|
| GAP-RPU-001 | SSRI | Social synchrony features (3 dims) | Medium | Open |
| GAP-RPU-002 | SSRI, IUCP | Rhythmic IC/entropy (2 dims) | Medium-high | Open |
| GAP-RPU-003 | SSRI, DAED | State connectivity (architectural) | Low | Open -- not R3-level |
| (none) | SSPS | No R³ gaps found | N/A | Closed |
| GAP-RPU-004 | LDAC, IUCP, RPEM | Melodic/harmonic entropy (2 dims) | Medium-high | Open |
| GAP-RPU-005 | LDAC | Bilateral AC lateralization (architectural) | Low | Open -- architectural |
| (none) | IOTMS | No R³ gaps; 10 doc-code mismatches for Phase 5 | Phase 5 | Logged |
