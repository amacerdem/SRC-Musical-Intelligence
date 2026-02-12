# Beta Upgrade Plan — Musical Intelligence v2.1

## Context

The MI project has 94 C³ cognitive model documents + 2 new models to create = **96 total** (48 Core + 48 Experimental, symmetric). 87 models are implemented in mi_beta. The goal is to systematically revise every model document to 99%+ scientific accuracy by cross-referencing with the literature, then build complete R³/H³/L³ architecture documentation, and finally update mi_beta code.

**Symmetry target:**

| Group | Units | Models |
|-------|-------|--------|
| Core-4 | SPU(9) + STU(14) + IMU(15) + ARU(10) | **48** |
| Experimental-5 | ASU(9) + NDU(9) + MPU(10) + PCU(9→**10**) + RPU(9→**10**) | **48** |
| **Total** | 9 units | **96** |

**2 new models to create:**

| Unit | Model ID | Full Name | Rationale |
|------|----------|-----------|-----------|
| PCU | PCU-β4-CHPI | Cross-Modal Harmonic Predictive Integration | Fills gap: multimodal harmonic prediction (visual-motor priming of chord expectations). Evidence: audiovisual structural connectivity in musicians, crossmodal temporal perception, cross-modal emotional congruency studies. |
| RPU | RPU-β4-SSRI | Social Synchrony Reward Integration | Fills gap: group music-making reward circuits (interpersonal neural alignment as hedonic value). Evidence: EEG of dyadic dance, social bonding neural synchronization, groove pupillometry studies. |

**Current gaps:**
- Docs/R³/ is empty — no spectral architecture docs exist
- Docs/H³/ is empty — no temporal architecture docs exist
- Docs/L³/ has only 4 files (AAC, BRAIN, SRP, VMM semantic spaces)
- Docs/Beta/ is empty — the upgrade plan will live here
- 96 docs target vs 87 models in mi_beta (9 model code gap to resolve in Phase 5)
- Model h3_demand properties are empty `()` in code — needs population after docs finalize

## Implementation Plan

### Phase 0: Setup (one-time)
1. Create `Docs/Beta/Beta_upgrade.md` — copy this plan into the project
2. Create `Docs/Beta/PROGRESS.md` — progress tracker with checkboxes for all 96 models
3. Create `Docs/R³/00-INDEX.md` — R³ architecture index (initially skeleton)
4. Create `Docs/H³/00-INDEX.md` — H³ architecture index (initially skeleton)
5. Create `Docs/R³/R3-GAP-LOG.md` — running log of R³ dimension gaps found during C³ revision
6. Create `Docs/C³/Models/PCU-β4-CHPI/CHPI.md` — new model doc (full 14-section template)
7. Create `Docs/C³/Models/RPU-β4-SSRI/SSRI.md` — new model doc (full 14-section template)
8. Update `Docs/C³/Models/00-INDEX.md` — add PCU-β4-CHPI and RPU-β4-SSRI, update totals to 96

### Phase 1: C³ Model Revision (96 models)

**Per-model workflow (repeat for each model in order below):**

```
STEP 1: READ MODEL DOC
  → Read Docs/C³/Models/{UNIT}-{tier}{n}-{ACRONYM}/{ACRONYM}.md
  → Note: sections, evidence table, R³ mapping, H³ demand, output space, math formulas

STEP 2: READ MI_BETA CODE
  → Read mi_beta/brain/units/{unit_lower}/models/{acronym_lower}.py
  → Compare: OUTPUT_DIM, MECHANISM_NAMES, LAYERS, dimension_names, brain_regions, h3_demand
  → Note any doc-code mismatches
  → (For new models CHPI/SSRI: skip this step — code doesn't exist yet)

STEP 3: C³ DEEP LITERATURE RESEARCH (MANDATORY — 500+ papers)

  ╔══════════════════════════════════════════════════════════════════╗
  ║  THIS IS THE MOST CRITICAL STEP OF THE ENTIRE WORKFLOW.        ║
  ║  Literature/c3 contains 500+ neuroscience papers.              ║
  ║  EVERY model must be deeply cross-referenced against ALL       ║
  ║  relevant papers — not just those already cited in the doc.    ║
  ║  SKIP NOTHING. Read EVERY relevant summary individually.       ║
  ╚══════════════════════════════════════════════════════════════════╝

  3a. C³ CATALOG SEARCH (find ALL relevant papers):
    → Read Literature/catalog.json (504 C³ papers indexed)
    → Filter by unit tag (e.g., "SPU") to find all papers tagged for this unit
    → ALSO search by topic keywords relevant to this specific model
      (e.g., for BCH: "consonance", "brainstem", "FFR", "roughness", "Plomp")
    → ALSO search by author names cited in the model doc
    → ALSO search by brain region names (e.g., "inferior colliculus", "Heschl")
    → Build a COMPLETE list of ALL relevant paper IDs
    → Expected: 15-80 papers per model depending on topic breadth

  3b. READ EVERY RELEVANT C³ SUMMARY (no shortcuts):
    → For EACH relevant paper found in 3a:
      → Read Literature/c3/summaries/{paper_id}.md (492 summary files available)
      → Extract: effect sizes (r, d, η², β), sample sizes (N),
        brain regions (MNI coordinates), methods (fMRI, EEG, MEG, TMS, PET),
        key findings, statistical tests, limitations, population
    → Cross-reference findings with model's current evidence table
    → Identify:
      - Missing citations (papers that support the model but aren't cited)
      - Incorrect effect sizes (model doc vs paper summary mismatch)
      - Outdated findings (superseded by newer replication)
      - New supporting evidence (strengthens model confidence)
      - Contradictory evidence (weakens model or requires qualification)
      - New brain regions not in model (expand Section 8)
      - New R³ features implied (log to R3-GAP-LOG.md)

  3c. CHECK C³ JSON EXTRACTIONS (structured claim-level data):
    → Search Literature/c3/extractions/ (12 JSON files, v3.0 format)
    → These contain machine-readable structured data:
      - claims[] with effect sizes, p-values, confidence intervals
      - brain_regions[] with MNI coordinates (x, y, z)
      - r3_axis_mapping (which R³ dimensions the paper informs)
      - methods, sample_sizes, paradigms
    → Use these for PRECISE numerical verification of:
      - Effect sizes quoted in model doc Section 3
      - MNI coordinates quoted in model doc Section 8
      - R³ feature mappings in model doc Section 4

  3d. R³ LITERATURE (AFTER C³ — secondary but important):
    → Search Literature/r3/ (121 markdown files, 59 papers)
    → Especially relevant for:
      - ALL SPU models (spectral processing = R³ core)
      - ASU consonance/timbre models
      - Any model with strong R³ input dependencies
    → Check: psychoacoustic basis for R³ feature usage,
      computational formulas (Plomp-Levelt, spectral centroid, etc.),
      perceptual thresholds, JND values

  3e. COMPILE EVIDENCE AUDIT REPORT:
    → For each claim in the model's existing evidence table:
      ✓ Citation correct? (author, year, journal match paper summary)
      ✓ Effect size accurate? (r/d/η² match paper)
      ✓ MNI coordinates correct? (match paper/extraction)
      ✓ Sample size reported? (N=?)
      ✓ Method correctly described? (fMRI vs EEG vs behavioral)
      ✓ Statistical test identified? (t-test, ANOVA, correlation, etc.)
    → For each NEW paper found but NOT currently cited:
      ✓ Does it support, extend, or contradict the model?
      ✓ Should it be added to the evidence table?
      ✓ Does it provide stronger effect sizes or newer replication?
      ✓ Does it reveal new brain regions or mechanisms?
    → Document ALL discrepancies → feed into STEP 4 revision
    → If a paper contradicts the model, note severity:
      - Minor: qualifies a claim but doesn't invalidate model
      - Major: requires model revision (change formulas, add mechanisms)
      - Critical: model may need reclassification (tier change)

STEP 4: REVISE MODEL DOC
  → Update Section 3 (Scientific Foundation): verify/add citations, effect sizes
  → Update Section 4 (R³ Input Mapping): verify feature dependencies
  → Update Section 5 (H³ Temporal Demand): verify demand tuples with evidence
  → Update Section 6 (Output Space): ensure all dimensions are justified
  → Update Section 7 (Mathematical Formulation): verify formulas match evidence
  → Update Section 8 (Brain Regions): verify MNI coordinates against papers
  → Update Section 13 (References): ensure all cited papers exist in Literature
  → LOG any R³ gaps to Docs/R³/R3-GAP-LOG.md

STEP 5: MARK COMPLETE
  → Update Docs/Beta/PROGRESS.md: check off this model
```

**Processing order (dependency-resolved, α→β→γ within each unit):**

#### BATCH 1: SPU (Spectral Processing — foundational, 9 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 1 | SPU-α1-BCH | BCH.md | REVISE |
| 2 | SPU-α2-PSCL | PSCL.md | REVISE |
| 3 | SPU-α3-PCCR | PCCR.md | REVISE |
| 4 | SPU-β1-STAI | STAI.md | REVISE |
| 5 | SPU-β2-TSCP | TSCP.md | REVISE |
| 6 | SPU-β3-MIAA | MIAA.md | REVISE |
| 7 | SPU-γ1-SDNPS | SDNPS.md | REVISE |
| 8 | SPU-γ2-ESME | ESME.md | REVISE |
| 9 | SPU-γ3-SDED | SDED.md | REVISE |

#### BATCH 2: STU (Sensorimotor Timing, 14 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 10 | STU-α1-HMCE | HMCE.md | REVISE |
| 11 | STU-α2-AMSC | AMSC.md | REVISE |
| 12 | STU-α3-MDNS | MDNS.md | REVISE |
| 13 | STU-β1-AMSS | AMSS.md | REVISE |
| 14 | STU-β2-TPIO | TPIO.md | REVISE |
| 15 | STU-β3-EDTA | EDTA.md | REVISE |
| 16 | STU-β4-ETAM | ETAM.md | REVISE |
| 17 | STU-β5-HGSIC | HGSIC.md | REVISE |
| 18 | STU-β6-OMS | OMS.md | REVISE |
| 19 | STU-γ1-TMRM | TMRM.md | REVISE |
| 20 | STU-γ2-NEWMD | NEWMD.md | REVISE |
| 21 | STU-γ3-MTNE | MTNE.md | REVISE |
| 22 | STU-γ4-PTGMP | PTGMP.md | REVISE |
| 23 | STU-γ5-MPFS | MPFS.md | REVISE |

#### BATCH 3: IMU (Integrative Memory, 15 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 24 | IMU-α1-MEAMN | MEAMN.md | REVISE |
| 25 | IMU-α2-PNH | PNH.md | REVISE |
| 26 | IMU-α3-MMP | MMP.md | REVISE |
| 27 | IMU-β1-RASN | RASN.md | REVISE |
| 28 | IMU-β2-PMIM | PMIM.md | REVISE |
| 29 | IMU-β3-OII | OII.md | REVISE |
| 30 | IMU-β4-HCMC | HCMC.md | REVISE |
| 31 | IMU-β5-RIRI | RIRI.md | REVISE |
| 32 | IMU-β6-MSPBA | MSPBA.md | REVISE |
| 33 | IMU-β7-VRIAP | VRIAP.md | REVISE |
| 34 | IMU-β8-TPRD | TPRD.md | REVISE |
| 35 | IMU-β9-CMAPCC | CMAPCC.md | REVISE |
| 36 | IMU-γ1-DMMS | DMMS.md | REVISE |
| 37 | IMU-γ2-CSSL | CSSL.md | REVISE |
| 38 | IMU-γ3-CDEM | CDEM.md | REVISE |

#### BATCH 4: ASU (Auditory Salience, 9 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 39 | ASU-α1-SNEM | SNEM.md | REVISE |
| 40 | ASU-α2-IACM | IACM.md | REVISE |
| 41 | ASU-α3-CSG | CSG.md | REVISE |
| 42 | ASU-β1-BARM | BARM.md | REVISE |
| 43 | ASU-β2-STANM | STANM.md | REVISE |
| 44 | ASU-β3-AACM | AACM.md | REVISE |
| 45 | ASU-γ1-PWSM | PWSM.md | REVISE |
| 46 | ASU-γ2-DGTP | DGTP.md | REVISE |
| 47 | ASU-γ3-SDL | SDL.md | REVISE |

#### BATCH 5: NDU (Novelty Detection, 9 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 48 | NDU-α1-MPG | MPG.md | REVISE |
| 49 | NDU-α2-SDD | SDD.md | REVISE |
| 50 | NDU-α3-EDNR | EDNR.md | REVISE |
| 51 | NDU-β1-DSP | DSP.md | REVISE |
| 52 | NDU-β2-CDMR | CDMR.md | REVISE |
| 53 | NDU-β3-SLEE | SLEE.md | REVISE |
| 54 | NDU-γ1-SDDP | SDDP.md | REVISE |
| 55 | NDU-γ2-ONI | ONI.md | REVISE |
| 56 | NDU-γ3-ECT | ECT.md | REVISE |

#### BATCH 6: MPU (Motor Planning, 10 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 57 | MPU-α1-PEOM | PEOM.md | REVISE |
| 58 | MPU-α2-MSR | MSR.md | REVISE |
| 59 | MPU-α3-GSSM | GSSM.md | REVISE |
| 60 | MPU-β1-ASAP | ASAP.md | REVISE |
| 61 | MPU-β2-DDSMI | DDSMI.md | REVISE |
| 62 | MPU-β3-VRMSME | VRMSME.md | REVISE |
| 63 | MPU-β4-SPMC | SPMC.md | REVISE |
| 64 | MPU-γ1-NSCP | NSCP.md | REVISE |
| 65 | MPU-γ2-CTBB | CTBB.md | REVISE |
| 66 | MPU-γ3-STC | STC.md | REVISE |

#### BATCH 7: PCU (Predictive Coding, 10 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 67 | PCU-α1-HTP | HTP.md | REVISE |
| 68 | PCU-α2-SPH | SPH.md | REVISE |
| 69 | PCU-α3-ICEM | ICEM.md | REVISE |
| 70 | PCU-β1-PWUP | PWUP.md | REVISE |
| 71 | PCU-β2-WMED | WMED.md | REVISE |
| 72 | PCU-β3-UDP | UDP.md | REVISE |
| 73 | **PCU-β4-CHPI** | **CHPI.md** | **NEW** |
| 74 | PCU-γ1-IGFE | IGFE.md | REVISE |
| 75 | PCU-γ2-MAA | MAA.md | REVISE |
| 76 | PCU-γ3-PSH | PSH.md | REVISE |

#### BATCH 8: ARU (Affective Resonance — dependent unit, 10 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 77 | ARU-α1-SRP | SRP.md | REVISE |
| 78 | ARU-α2-AAC | AAC.md | REVISE |
| 79 | ARU-α3-VMM | VMM.md | REVISE |
| 80 | ARU-β1-PUPF | PUPF.md | REVISE |
| 81 | ARU-β2-CLAM | CLAM.md | REVISE |
| 82 | ARU-β3-MAD | MAD.md | REVISE |
| 83 | ARU-β4-NEMAC | NEMAC.md | REVISE |
| 84 | ARU-γ1-DAP | DAP.md | REVISE |
| 85 | ARU-γ2-CMAT | CMAT.md | REVISE |
| 86 | ARU-γ3-TAR | TAR.md | REVISE |

#### BATCH 9: RPU (Reward Processing — dependent unit, 10 models)
| # | Model ID | File | Status |
|---|----------|------|--------|
| 87 | RPU-α1-DAED | DAED.md | REVISE |
| 88 | RPU-α2-MORMR | MORMR.md | REVISE |
| 89 | RPU-α3-RPEM | RPEM.md | REVISE |
| 90 | RPU-β1-IUCP | IUCP.md | REVISE |
| 91 | RPU-β2-MCCN | MCCN.md | REVISE |
| 92 | RPU-β3-MEAMR | MEAMR.md | REVISE |
| 93 | **RPU-β4-SSRI** | **SSRI.md** | **NEW** |
| 94 | RPU-γ1-LDAC | LDAC.md | REVISE |
| 95 | RPU-γ2-IOTMS | IOTMS.md | REVISE |
| 96 | RPU-γ3-SSPS | SSPS.md | REVISE |

**Quality gate after Phase 1:** Every model doc has verified evidence tables, correct R³ mappings, justified H³ demands, and all citations traced to Literature/.

### Phase 2: R³ Architecture (Docs/R³)

After all 96 models are revised, consolidate R³ findings:

1. **Review R3-GAP-LOG.md** — compile all gaps found during Phase 1
2. **Create `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md`** — master architecture document:
   - Current 49D space (5 groups: consonance, energy, timbre, change, interactions)
   - Proposed expansions (new groups/dimensions from gap log)
   - Per-dimension specification: name, computation, range, psychoacoustic basis, unit
3. **Per-group detailed docs:**
   - `Docs/R³/A-CONSONANCE.md` — 7D consonance group spec
   - `Docs/R³/B-ENERGY.md` — 5D energy group spec
   - `Docs/R³/C-TIMBRE.md` — 9D timbre group spec
   - `Docs/R³/D-CHANGE.md` — 4D change group spec
   - `Docs/R³/E-INTERACTIONS.md` — 24D interactions group spec
   - `Docs/R³/F-{NEW_GROUP}.md` — any new groups from gap analysis
4. **Per-unit R³ mapping docs:**
   - `Docs/R³/mappings/SPU-R3-MAP.md` — which R³ dims SPU models use & why
   - `Docs/R³/mappings/STU-R3-MAP.md` — etc for each unit
   - Each mapping doc shows: model → R³ indices → mathematical relationship → citation
5. **Cross-reference with Literature/r3/**:
   - Link psychoacoustics papers to consonance/timbre dimensions
   - Link computational music theory to interaction dimensions
   - Link DSP papers to energy/change dimensions

**Quality gate:** Every R³ dimension has a psychoacoustic basis, computation formula, expected range, and at least one literature citation.

### Phase 3: H³ Architecture (Docs/H³)

1. **Create `Docs/H³/H3-TEMPORAL-ARCHITECTURE.md`** — master temporal architecture:
   - 32 horizons with musical meaning (sub-beat → piece)
   - 24 morphs with statistical definitions
   - 3 laws (memory, prediction, integration)
   - Demand aggregation explanation
   - Sparsity analysis (what % of 2304D is actually used)
2. **Per-horizon-band docs:**
   - `Docs/H³/H0-H5-SUB-BEAT.md` — 5.8ms to 46.4ms
   - `Docs/H³/H6-H11-BEAT.md` — 200ms to 450ms
   - `Docs/H³/H12-H17-PHRASE.md` — 525ms to 1500ms
   - `Docs/H³/H18-H23-SECTION.md` — 2s to 25s
   - `Docs/H³/H24-H31-FORM.md` — 36s to 981s
3. **Per-unit H³ demand docs:**
   - `Docs/H³/demands/SPU-H3-DEMAND.md` — all H³ tuples SPU models need
   - etc for each unit
   - Each demand doc: model → (r3_idx, horizon, morph, law) → purpose → citation
4. **Global demand matrix visualization**

**Quality gate:** Every H³ demand tuple has a purpose, citation, and links to the specific R³ feature it operates on.

### Phase 4: L³ Architecture (Docs/L³)

1. **Create `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md`** — master semantic architecture:
   - 8 semantic groups (alpha through theta)
   - Dynamic dimensionality explanation
   - Per-group specification (inputs, computation, output meaning)
2. **Update existing L³ files** (AAC, BRAIN, SRP, VMM semantic spaces)
3. **Per-unit L³ mapping docs:**
   - `Docs/L³/mappings/SPU-L3-MAP.md` — how SPU outputs map to semantic meaning
   - etc for each unit
4. **Cross-unit semantic integration doc:**
   - `Docs/L³/L3-CROSS-UNIT-INTEGRATION.md` — how units combine in semantic space

**Quality gate:** Every L³ semantic group has defined inputs, computation method, and output meaning linked to C³ models.

### Phase 5: mi_beta Code Update (LAST)

Only after Phases 1-4 are complete:

1. **Create 9 missing model files** (96 docs - 87 code = 9 gap, including CHPI and SSRI)
2. **Per-model code updates** (based on revised docs):
   - Populate h3_demand tuples from revised Section 5
   - Verify OUTPUT_DIM, LAYERS, dimension_names match revised Section 6
   - Update brain_regions from revised Section 8
   - Update compute() logic if mathematical formulation changed
3. **R³ expansion** (if Phase 2 identified new dimensions):
   - Update mi_beta/core/constants.py (R3_DIM, group boundaries)
   - Update mi_beta/core/dimension_map.py (_R3_FEATURE_NAMES)
   - Add new feature extractors in mi_beta/ear/r3/
4. **H³ updates** (if demand patterns changed)
5. **L³ updates** (if semantic groups changed)
6. **Update 00-INDEX.md** with final totals
7. **Run tests:** `pytest tests/ -v`
8. **Validation run:** `python -m mi_beta`

## Critical File Paths

| File | Role |
|------|------|
| `Docs/C³/Models/00-INDEX.md` | Master model index (96 models) |
| `Docs/Beta/PROGRESS.md` | Progress tracker (checkboxes) |
| `Docs/Beta/Beta_upgrade.md` | This plan (in-project copy) |
| `Docs/R³/R3-GAP-LOG.md` | Running log of R³ gaps |
| `Literature/catalog.json` | Paper index (504 C³ + 59 R³) |
| `Literature/c3/summaries/` | Paper summaries (492 files) |
| `Literature/c3/extractions/` | Structured extractions (12 JSON) |
| `Literature/r3/` | R³ literature (121 markdown) |
| `mi_beta/core/constants.py` | Single source of truth for all constants |
| `mi_beta/core/dimension_map.py` | R³ feature names and MI-space mapping |
| `mi_beta/contracts/base_model.py` | Model contract (what every model must implement) |

## Resume Protocol for AI Agents

When resuming this work:

```
1. READ Docs/Beta/PROGRESS.md
   → Find the last completed model (checked off)
   → The NEXT unchecked model is where to resume

2. READ Docs/R³/R3-GAP-LOG.md
   → Understand accumulated R³ gaps so far

3. CHECK which phase we're in:
   → If unchecked C³ models remain → Phase 1 (continue model revision)
   → If all C³ done but R³ docs missing → Phase 2
   → If R³ done but H³ docs missing → Phase 3
   → If H³ done but L³ incomplete → Phase 4
   → If all docs done → Phase 5 (mi_beta code update)

4. FOLLOW the per-model workflow (5 steps) for the current model

5. COMMIT after each unit batch (9-15 models) with message:
   "Revise {UNIT} models ({n} models) — Phase 1 C³ update"
```

## New Model Specifications

### PCU-β4-CHPI: Cross-Modal Harmonic Predictive Integration

**Unit:** PCU (Predictive Coding)
**Tier:** β (70-90% confidence, cross-domain synthesis)
**Circuit:** Imagery (Auditory Cortex, IFG, STS, Hippocampus)
**Mechanisms:** PPC + TPC + MEM

**Description:** Models how the brain predicts harmonic progressions through cross-modal integration of visual (notation/instrument), motor (fingering patterns), and temporal (beat) information. Harmonic expectation is not purely auditory but integrates multi-sensory predictive signals — particularly visual perception of voice-leading constraints and motor patterns associated with chord transitions.

**Gap filled:** PCU currently emphasizes temporal/sequential prediction but lacks cross-modal predictive grounding. Musicians' superior harmonic prediction requires multimodal explanation.

**Supporting evidence:**
- Audiovisual structural connectivity in musicians (enhanced AC-visual cortex connectivity)
- Crossmodal temporal perception (intersensory redundancy hypothesis)
- Cross-modal emotional congruency (fronto-limbic integration)

### RPU-β4-SSRI: Social Synchrony Reward Integration

**Unit:** RPU (Reward Processing)
**Tier:** β (70-90% confidence, cross-domain synthesis)
**Circuit:** Mesolimbic (NAcc, VTA, vmPFC, OFC, Amygdala)
**Mechanisms:** AED + CPD + C0P

**Description:** Models the neural mechanisms by which interpersonal neural synchronization and behavioral coordination during group music-making generates hedonic reward through prefrontal-limbic pathways. Captures the unique reward signal of "group flow" — where pleasure derives from synchronized intention, timing, and emotional expression with others.

**Gap filled:** RPU currently treats reward as individual biochemistry (dopamine/opioids) without social mechanisms. Group music-making is universal but has no dedicated RPU model.

**Supporting evidence:**
- EEG of dyadic dance (distinct neural signatures for social musical-motor coordination)
- Social bonding neural synchronization (prefrontal synchronization during group bonding)
- Groove pupillometry (noradrenergic arousal, precision-weighted prediction error)

## Verification

After full completion:
- 96 model docs (48 Core + 48 Experimental) all with verified evidence
- Every model doc Section 3 has verified effect sizes matching Literature
- Every model doc Section 4 maps to valid R³ indices (current or expanded)
- Every model doc Section 5 has H³ demands with citations
- Every model doc Section 8 has MNI coordinates verified against papers
- Docs/R³/ has complete spectral architecture with per-group specs
- Docs/H³/ has complete temporal architecture with per-unit demands
- Docs/L³/ has complete semantic architecture with per-unit mappings
- `pytest tests/ -v` passes
- `python -m mi_beta` runs without errors
