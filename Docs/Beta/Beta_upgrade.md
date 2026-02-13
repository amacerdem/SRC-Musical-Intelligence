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

**Phase 1 Status: ✅ COMPLETE (2026-02-13)** — All 96 models revised to v2.1.0. Both new models (CHPI, SSRI) created. 7 R³ gap logs written. All changes committed.

### Phase 2: C³ Documentation Architecture (Docs/C³)

**Problem:** 96 model documents are complete but exist as isolated islands. The code has rich structural layers (`mi_beta/brain/` → units, mechanisms, pathways, regions, neurochemicals, circuits) with NO documentation counterparts. The "bridges between islands" are missing.

**Design principle:** Model docs (96 × 14-section) are the **source of truth**. All upper layers **aggregate** from models. Information flows bottom-up.

```
LAYER 0: C3-ARCHITECTURE.md
         "How does the entire system work?"
         ┃
LAYER 1: Units/ + Circuits/ + Tiers/
         "What functional units compose the brain?"
         ┃
LAYER 2: Mechanisms/ + Pathways/ + Regions/ + Neurochemicals/
         "What building blocks compose those units?"
         ┃
LAYER 3: Models/ (existing 96 docs — source of truth)
         "What does each computational model do exactly?"
         ┃
LAYER T: Contracts/ + Matrices/
         "What rules do all components obey?" (cross-cutting)
```

**Complete file tree (~61 new files):**

```
Docs/C³/
│
├── C3-ARCHITECTURE.md            ← BrainOrchestrator counterpart
│                                    Full system overview: 5-phase execution,
│                                    data flow, MI-space assembly
│                                    audio → R³ → H³ → Brain → L³ → MI-space
│                                    Dependency graph (ASCII-art)
│
├── Contracts/                    ← mi_beta/contracts/ counterpart
│   ├── 00-INDEX.md               ← 9 contract types summary
│   ├── BaseModel.md              ← Mandatory 14-section structure for every model
│   ├── BaseCognitiveUnit.md      ← Unit interface specification
│   ├── BaseMechanism.md          ← 30D mechanism contract
│   ├── LayerSpec.md              ← E/M/P/F/T/N/C output layer system
│   ├── H3DemandSpec.md           ← (r3_idx, horizon, morph, law) contract
│   ├── CrossUnitPathway.md       ← Pathway declaration contract
│   ├── BrainRegion.md            ← MNI coordinate + evidence contract
│   └── ModelMetadata.md          ← Evidence provenance contract
│
├── Mechanisms/                   ← mi_beta/brain/mechanisms/ counterpart
│   ├── 00-INDEX.md               ← 10 mechanisms, circuit assignments, 30D convention
│   │                                Per-mechanism: NAME, CIRCUIT, OUTPUT_DIM=30,
│   │                                3×10D sub-sections, which models use it
│   │
│   │  ── Mesolimbic (Reward) ──
│   ├── AED.md                    ← Affective Entrainment Dynamics
│   ├── CPD.md                    ← Chills & Peak Detection
│   ├── C0P.md                    ← Cognitive Projection
│   │
│   │  ── Perceptual ──
│   ├── PPC.md                    ← Pitch Pattern Classification
│   ├── TPC.md                    ← Tonal Pattern Classification
│   │
│   │  ── Sensorimotor ──
│   ├── BEP.md                    ← Beat-Entrained Prediction
│   ├── TMH.md                    ← Temporal-Motor Hierarchy
│   │
│   │  ── Mnemonic ──
│   ├── MEM.md                    ← Memory Encoding
│   ├── SYN.md                    ← Synaptic Consolidation
│   │
│   │  ── Salience ──
│   └── ASA.md                    ← Auditory Scene Analysis
│
├── Pathways/                     ← mi_beta/brain/pathways/ counterpart
│   ├── 00-INDEX.md               ← 5 pathways, routing rules, two-pass execution
│   ├── P1-SPU-ARU.md             ← Consonance → Pleasure (r=0.81)
│   ├── P2-STU-STU.md             ← Beat → Motor Sync (r=0.70)
│   ├── P3-IMU-ARU.md             ← Memory → Affect (r=0.55)
│   ├── P4-STU-STU.md             ← Context → Prediction (r=0.99)
│   └── P5-STU-ARU.md             ← Tempo → Emotion (r=0.60)
│
├── Regions/                      ← mi_beta/brain/regions/ counterpart
│   ├── 00-INDEX.md               ← RegionAtlas: 26 regions, MNI coordinate system
│   ├── Cortical.md               ← 12 regions (A1/HG, STG, STS, IFG, DLPFC, ...)
│   ├── Subcortical.md            ← 9 regions (NAcc, Caudate, VTA, Amygdala, ...)
│   └── Brainstem.md              ← 5 regions (IC, AN, CN, SOC, PAG)
│
├── Neurochemicals/               ← mi_beta/brain/neurochemicals/ counterpart
│   ├── 00-INDEX.md               ← 4 systems, write/read protocol
│   ├── Dopamine.md               ← DA: anticipation/consummation dissociation
│   ├── Opioid.md                 ← μ-Opioid: hedonic hotspots
│   ├── Serotonin.md              ← 5-HT: mood modulation
│   └── Norepinephrine.md         ← NE: arousal, attention gating
│
├── Circuits/                     ← CIRCUIT_NAMES counterpart (implicit in code)
│   ├── 00-INDEX.md               ← 6 circuit families, mechanism/unit map
│   ├── Mesolimbic.md             ← Reward & Pleasure (AED+CPD+C0P → ARU+RPU)
│   ├── Perceptual.md             ← Hearing & Pattern (PPC+TPC → SPU+ASU)
│   ├── Sensorimotor.md           ← Rhythm & Movement (BEP+TMH → STU+MPU)
│   ├── Mnemonic.md               ← Memory & Familiarity (MEM+SYN → IMU)
│   ├── Salience.md               ← Attention & Novelty (ASA → ASU+NDU)
│   └── Imagery.md                ← Simulation & Prediction (→ PCU)
│
├── Units/                        ← mi_beta/brain/units/ counterpart
│   ├── 00-INDEX.md               ← 9 units, execution order, dependency graph
│   │                                Per-unit: UNIT_NAME, FULL_NAME, CIRCUIT,
│   │                                POOLED_EFFECT, model list with OUTPUT_DIMs,
│   │                                total dimensionality, R³ usage profile,
│   │                                H³ demand union, mechanisms used, pathways
│   │
│   │  ── Core-4 ──
│   ├── SPU.md                    ← Spectral Processing (9 models, α1-γ3)
│   ├── STU.md                    ← Sensorimotor Timing (14 models, α1-γ5)
│   ├── IMU.md                    ← Integrative Memory (15 models, α1-γ3)
│   ├── ARU.md                    ← Affective Resonance (10 models) ⚠️ DEPENDENT
│   │
│   │  ── Experimental-5 ──
│   ├── ASU.md                    ← Auditory Salience (9 models, α1-γ3)
│   ├── NDU.md                    ← Novelty Detection (9 models, α1-γ3)
│   ├── MPU.md                    ← Motor Planning (10 models, α1-γ3)
│   ├── PCU.md                    ← Predictive Coding (10 models, α1-γ3)
│   └── RPU.md                    ← Reward Processing (10 models) ⚠️ DEPENDENT
│
├── Tiers/                        ← MODEL_TIERS counterpart
│   ├── Alpha.md                  ← α: >90% confidence, k≥10, foundational
│   ├── Beta.md                   ← β: 70-90%, k≥5, integrative
│   └── Gamma.md                  ← γ: <70%, k<5, theoretical
│
├── Matrices/                     ← Cross-cutting aggregate views
│   ├── R3-Usage.md               ← 96 model × 49 R³ feature usage matrix
│   ├── H3-Demand.md              ← 96 model × H³ tuple total demand matrix
│   ├── Region-Atlas.md           ← 26 regions × 96 model reference matrix
│   ├── Mechanism-Map.md          ← 10 mechanisms × 96 model connection matrix
│   └── Output-Space.md           ← MI-space full dimension map
│
└── Models/                       ← EXISTING (untouched, source of truth)
    ├── 00-INDEX.md               ← 96 model master index
    └── ... (96 folders, each with 14-section document)
```

**Implementation order (highest impact, least effort first):**

| Priority | Component | Files | Source |
|----------|-----------|-------|--------|
| 1 | `C3-ARCHITECTURE.md` | 1 | Code: `pipeline/brain_runner.py`, `core/constants.py` |
| 2 | `Units/` | 10 | Code: `units/*/_unit.py` + model docs aggregate |
| 3 | `Mechanisms/` | 11 | Code: `mechanisms/*.py` + model Section 5 |
| 4 | `Pathways/` | 6 | Code: `pathways/*.py` + model Section 9 |
| 5 | `Contracts/` | 9 | Code: `contracts/*.py` (formalize interface specs) |
| 6 | `Regions/` | 4 | Code: `regions/*.py` + model Section 8 aggregate |
| 7 | `Neurochemicals/` | 5 | Code: `neurochemicals/*.py` |
| 8 | `Circuits/` | 7 | Implicit in code, explicit from mechanism/unit mapping |
| 9 | `Tiers/` | 3 | Model metadata aggregate |
| 10 | `Matrices/` | 5 | Cross-model aggregate (last, needs all above) |
| | **Total** | **~61** | |

**Quality gate:** Every code component in `mi_beta/brain/` has a documentation counterpart in `Docs/C³/`. Every doc references the specific code file it mirrors. Every model doc is reachable from at least one Unit doc, one Mechanism doc, and one Circuit doc.

### Phase 3: R³ Architecture — Bidirectional Spectral Expansion (Docs/R³)

R³ is currently 49D but the architecture supports dynamic expansion via `R3FeatureRegistry` + `extensions/`.
Phase 3 is a **research-driven expansion** that works in two directions simultaneously:

- **Bottom-up (model demand):** What do the 96 C³ models need that R³ doesn't provide?
- **Top-down (DSP capability):** What can physically be measured from audio that R³ doesn't yet capture?

Target: expand R³ from 49D to **128–256D** based on evidence from both directions.

#### Aşama 3A: Keşif & Envanter (Research)

**3A-1: Model Talep Haritası (Bottom-up)**
- Compile all 57 gaps from 7 unit-specific R³ gap logs:
  - `R3-GAP-LOG-IMU.md` (13 gaps), `R3-GAP-LOG-ASU.md` (8 gaps),
  - `R3-GAP-LOG-PCU.md` (9 gaps), `R3-GAP-LOG-RPU.md` (5 gaps),
  - `R3-GAP-LOG-MPU.md` (7 gaps), `R3-GAP-LOG-NDU.md` (5 gaps),
  - `R3-GAP-LOG-ARU.md` (0 gaps — fully covered)
  - Note: SPU/STU gap logs not created (completed before gap log format)
- Categorize each gap: **real acoustic gap** vs **naming mismatch** vs **neural-level** (not R³)
- Create demand matrix: 96 models × desired features → priority ranking
- Output: `Docs/R³/R3-DEMAND-MATRIX.md`

**3A-2: DSP Yetenek Araştırması (Top-down)**
- **Local literature scan** — `Literature/r3/` (121 markdown files, 58 PDFs):
  - `psychoacoustics/` (11 files): consonance/dissonance, just intonation, Pressnitzer
  - `dsp-and-ml/` (4 files): CNN spectral features, genre classification, microtonal
  - `computational-music-theory/` (65 files): Tymoczko geometry, Neo-Riemannian, group theory
  - `spectral-music/` (7 files): spectral composition analysis
- **Web deep research** — state-of-art DSP feature extraction:
  - librosa feature set (40+ features: chroma, MFCC, spectral contrast, tonnetz)
  - essentia feature set (600+ features: psychoacoustic, tonal, rhythm, dynamics)
  - openSMILE/eGeMAPS (88 features: acoustic emotion, paralinguistics)
  - Madmom (beat/tempo/onset detection, key estimation)
  - CREPE/pYIN/SPICE (neural pitch estimation)
  - ISO 532B / Zwicker loudness model
  - AES standards for audio quality measurement
- For each candidate feature: name, computation from mel, cost, psychoacoustic basis, citations
- Output: `Docs/R³/R3-DSP-SURVEY.md`

**3A-3: Gap ↔ Feature Eşleştirme**
- Cross-reference model demands with DSP capabilities
- Identify: (a) gaps solvable by known DSP, (b) gaps needing novel methods, (c) DSP features no model yet uses but should
- Output: `Docs/R³/R3-CROSSREF.md`

#### Aşama 3B: R³ v2 Tasarımı (Architecture Design)

**3B-1: Yeni Grup Tasarımı**
- Revise or preserve existing groups A–E:
  - A: Consonance (7D → ?D) — add explicit inharmonicity model, roughness (Plomp-Levelt proper)?
  - B: Energy (5D → ?D) — add Bark-band specific loudness, dynamic range?
  - C: Timbre (9D → ?D) — add MFCC-derived, spectral contrast, spectral rolloff?
  - D: Change (4D → ?D) — critically thin, add novelty function, modulation spectrum?
  - E: Interactions (?D) — redesign cross-products for new groups
- Define new groups:
  - **F: Pitch** — F0, pitch salience, pitch class profile (chroma 12D), pitch height, vibrato
  - **G: Rhythm** — beat strength, tempo, syncopation index, metrical hierarchy, groove
  - **H: Harmony** — chord template match, key clarity, harmonic tension, tonal stability
  - **I: Information** — melodic entropy, harmonic surprisal, IC (information content), statistical surprise
  - **J+: TBD** — modulation, polyphony, spatial, ...
- Decide target dimensionality: 128D / 192D / 256D
- Output: `Docs/R³/R3-V2-DESIGN.md`

**3B-2: Interaction Redesign**
- Current E group (24D) only covers 3 product types — too mechanical
- Design principled interaction scheme for expanded space
- Options: (a) exhaustive pairwise, (b) learned interactions, (c) curated domain-expert products
- Decide: fixed vs dynamic interactions
- Output: Section in R3-V2-DESIGN.md

**3B-3: Code Dekilitleme Tasarımı**
- `R3_DIM` → computed from registry at init time (remove hardcoded 49)
- `R3FeatureSpec` → validate against `registry.total_dim` (not literal 49)
- `_R3_FEATURE_NAMES` → auto-generated from `R3FeatureRegistry.freeze()`
- Group boundaries → read from `R3FeatureMap.groups` (not hardcoded tuples)
- Backward compatibility: existing model code references `r3[idx]` — migration strategy
- Output: Section in R3-V2-DESIGN.md

#### Aşama 3C: Dokümantasyon (Architecture Docs)

**3C-1: Master Architecture Doc**
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` — full R³ v2 specification:
  - Design rationale (why expand, what evidence)
  - Complete dimension inventory (old 49 + new)
  - Per-dimension: name, group, index, computation, range, psychoacoustic basis, citations
  - Extension protocol (how to add more groups in future)

**3C-2: Per-group Detailed Specs**
- `Docs/R³/A-CONSONANCE.md` — revised consonance group
- `Docs/R³/B-ENERGY.md` — revised energy group
- `Docs/R³/C-TIMBRE.md` — revised timbre group
- `Docs/R³/D-CHANGE.md` — expanded change group
- `Docs/R³/E-INTERACTIONS.md` — redesigned interactions
- `Docs/R³/F-PITCH.md` — new pitch group
- `Docs/R³/G-RHYTHM.md` — new rhythm group
- `Docs/R³/H-HARMONY.md` — new harmony group
- `Docs/R³/I-INFORMATION.md` — new information-theoretic group
- Additional groups as determined by 3B-1

**3C-3: Per-unit R³ Mapping Docs**
- `Docs/R³/mappings/{UNIT}-R3-MAP.md` (9 files, one per unit)
- Each mapping: model → R³ indices → mathematical relationship → citation
- Updated for expanded R³ space

**3C-4: Literature Cross-Reference**
- `Docs/R³/R3-LITERATURE.md` — links every R³ dimension to:
  - Primary psychoacoustic paper (basis)
  - DSP implementation reference (computation)
  - Literature/r3/ local file (if available)

#### Aşama 3D: Uygulama (Code — deferred to Phase 6)

Code changes are documented in Phase 3 but **implemented in Phase 6**:
- Remove R3_DIM=49 hardcoding → dynamic from registry
- New `BaseSpectralGroup` subclasses for groups F, G, H, I...
- Update `R3FeatureSpec`, `_R3_FEATURE_NAMES`, group boundaries
- Integration tests with expanded R³
- Benchmark: computation cost per frame at new dimensionality

#### Veri Kaynakları

| Source | Location | Content |
|--------|----------|---------|
| R³ Gap Logs (7 files) | `Docs/R³/R3-GAP-LOG-{UNIT}.md` | 57 gaps from Phase 1 model revision |
| Literature/r3 PDFs | `Literature/r3/` (5 subdirs, 121 md) | Psychoacoustics, DSP, spectral music, computational theory |
| Existing R³ code | `mi_beta/ear/r3/` (5 groups) | Current 49D implementation |
| C³ model docs (96) | `Docs/C³/Models/` | R³ usage per model (Section 4) |
| Web research | librosa, essentia, openSMILE, Madmom, CREPE docs | State-of-art feature extraction |

#### Çıktılar (~20+ dosya)

```
Docs/R³/
├── R3-SPECTRAL-ARCHITECTURE.md    ← Master doc (R³ v2 full spec)
├── R3-DEMAND-MATRIX.md            ← Bottom-up: 96 models × desired features
├── R3-DSP-SURVEY.md               ← Top-down: all feasible DSP features
├── R3-CROSSREF.md                 ← Gap ↔ Feature matching
├── R3-V2-DESIGN.md                ← Architecture decisions + rationale
├── R3-LITERATURE.md               ← Per-dimension literature links
├── A-CONSONANCE.md                ← Group A spec (revised)
├── B-ENERGY.md                    ← Group B spec (revised)
├── C-TIMBRE.md                    ← Group C spec (revised)
├── D-CHANGE.md                    ← Group D spec (expanded)
├── E-INTERACTIONS.md              ← Group E spec (redesigned)
├── F-PITCH.md                     ← Group F spec (NEW)
├── G-RHYTHM.md                    ← Group G spec (NEW)
├── H-HARMONY.md                   ← Group H spec (NEW)
├── I-INFORMATION.md               ← Group I spec (NEW)
├── R3-GAP-LOG.md                  ← Template (existing)
├── R3-GAP-LOG-{UNIT}.md (7)       ← Unit gap logs (existing from Phase 1)
└── mappings/
    ├── SPU-R3-MAP.md              ← SPU model → R³ mapping
    ├── STU-R3-MAP.md
    ├── IMU-R3-MAP.md
    ├── ASU-R3-MAP.md
    ├── NDU-R3-MAP.md
    ├── MPU-R3-MAP.md
    ├── PCU-R3-MAP.md
    ├── ARU-R3-MAP.md
    └── RPU-R3-MAP.md
```

#### Aşama 3E: Model Doc Güncelleme (96 Model Section 4 Revision)

After R³ v2 design is finalized (3B) and architecture docs are written (3C), **all 96 model documents must be updated** to reference the expanded R³ space:

**Per-model update workflow:**
```
For each of the 96 models in Docs/C³/Models/:

1. READ current Section 4 (R³ Input Mapping)
   → Note which R³ indices the model currently reads
   → Check against R3-GAP-LOG for this unit's gaps

2. CONSULT R³ v2 design (R3-V2-DESIGN.md)
   → Are there new dimensions this model should read?
   → Have existing dimensions been renumbered/renamed?
   → Does the model's gap from Phase 1 now have an R³ solution?

3. CONSULT unit mapping (mappings/{UNIT}-R3-MAP.md)
   → What does the unit-level mapping recommend?

4. UPDATE Section 4:
   → Add new R³ dimension references (e.g., F:Pitch features for pitch-dependent models)
   → Update indices if existing dimensions renumbered
   → Fix naming discrepancies (semantic ↔ computational names resolved)
   → Add mathematical relationships for new dimensions
   → Add citations for new R³ feature dependencies

5. UPDATE Section 12.1 (Doc-Code Mismatches) if applicable:
   → Note new R³ dimensions not yet in code (deferred to Phase 6)

6. BUMP version: v2.1.0 → v2.2.0 (R³ expansion update)
```

**Parallel execution:** Can be split across multiple chats by unit (same pattern as Phase 1):

| Chat | Unit(s) | Models | Estimated Scope |
|------|---------|--------|-----------------|
| 1 | SPU + STU | 9 + 14 = 23 | Many new R³ refs (spectral/timing core) |
| 2 | IMU + ASU + NDU | 15 + 9 + 9 = 33 | Moderate new R³ refs |
| 3 | MPU + PCU | 10 + 10 = 20 | Moderate new R³ refs (motor + prediction) |
| 4 | ARU + RPU | 10 + 10 = 20 | Fewest changes (dependent units, pathway-driven) |

**Key decisions per unit:**
- **SPU models**: Should directly read new Pitch (F) and possibly Harmony (H) groups
- **STU models**: Should read new Rhythm (G) group, possibly Information (I)
- **IMU models**: Broad — may read Pitch, Rhythm, Harmony, Information
- **ASU models**: Should read new features that provide salience signals
- **NDU models**: Should read Information (I) for surprisal/entropy features
- **MPU models**: Should read Rhythm (G) for motor-relevant features
- **PCU models**: Should read Information (I) for prediction-relevant features
- **ARU/RPU models**: Primarily receive via pathways, but may add direct R³ reads

**Quality gate:** Every model's Section 4 references only valid R³ v2 indices. Every model that had a Phase 1 R³ gap now either (a) references a new R³ dimension that fills the gap, or (b) documents why the gap remains (neural-level, architectural, etc.). All 96 models at v2.2.0.

#### Phase 3 Parallel Chat Assignment

Phase 3A (Research) runs across **3 parallel chats**. Each chat produces one deliverable independently. After all 3 complete, a single session merges results into 3A-3 (Crossref) → 3B (Design) → 3C (Docs) → 3E (Model Updates).

| Chat | Assignment | Input Sources | Output |
|------|-----------|---------------|--------|
| Chat R1 | **Bottom-up: Model Demand Analysis** | 96 model docs (Section 4), 7 R³ gap logs, C³ Matrices/R3-Usage.md | `Docs/R³/R3-DEMAND-MATRIX.md` |
| Chat R2 | **Top-down: Local Literature + Psychoacoustic DSP** | Literature/r3/ (121 files), existing R³ code (5 groups), psychoacoustic theory | `Docs/R³/R3-DSP-SURVEY-THEORY.md` |
| Chat R3 | **Top-down: Web Research + Computational DSP** | Web (librosa, essentia, openSMILE, Madmom, CREPE, ISO), AES/ASA standards | `Docs/R³/R3-DSP-SURVEY-TOOLS.md` |

```
         ┌──────────┐  ┌──────────┐  ┌──────────┐
         │ Chat R1  │  │ Chat R2  │  │ Chat R3  │
         │ Bottom-up│  │ Lit+Psych│  │ Web+DSP  │
         │ 96 model │  │ 121 files│  │ toolkits │
         └────┬─────┘  └────┬─────┘  └────┬─────┘
              │              │              │
              │     PARALLEL (3A)           │
              └──────────┬──┴──────────────┘
                         ▼
                   ┌───────────┐
                   │  MERGE    │  ← Single session
                   │ 3A-3→3B  │
                   │ →3C→3E   │
                   └───────────┘
```

#### Chat R1 Prompt: Bottom-up Model Demand Analysis

```
Sen Phase 3A-1 Chat R1'sin: R³ Model Talep Analizi.

## Proje
/Volumes/SRC-9/SRC Musical Intelligence

## Görev
96 C³ modelin R³ ihtiyaçlarını analiz et ve talep matrisi oluştur.

## Adımlar

### 1. Gap Log'ları Oku ve Konsolide Et
7 gap log dosyasını oku:
- Docs/R³/R3-GAP-LOG-IMU.md (13 gap)
- Docs/R³/R3-GAP-LOG-ASU.md (8 gap)
- Docs/R³/R3-GAP-LOG-PCU.md (9 gap)
- Docs/R³/R3-GAP-LOG-RPU.md (5 gap)
- Docs/R³/R3-GAP-LOG-MPU.md (7 gap)
- Docs/R³/R3-GAP-LOG-NDU.md (5 gap)
- Docs/R³/R3-GAP-LOG-ARU.md (0 gap)

Her gap için: GAP-ID, model, eksik feature, önerilen R³ grubu, öncelik.
Gap'leri 3 kategoriye ayır:
- ACOUSTIC: Gerçek akustik özellik eksikliği (R³'e eklenebilir)
- NAMING: İsimlendirme uyumsuzluğu (mevcut feature var ama adı farklı)
- NEURAL: Neural-seviye metrik (R³ olamaz, model/mekanizma seviyesinde çözülmeli)

### 2. 96 Model Doc Section 4 Tara
Her modelin Section 4 (R³ Input Mapping) kısmını oku.
Docs/C³/Models/ altında 96 model klasörü var.
Her model için kaydet:
- Hangi R³ indekslerini okuyor (0-48)
- R³ bağımlılığının gücü (critical / important / minor)
- Eksik ama ihtiyaç duyulan feature kategorisi (pitch? rhythm? harmony? information?)

### 3. C³ Matrices R3-Usage Oku
Docs/C³/Matrices/R3-Usage.md dosyasını oku — mevcut kullanım haritası.

### 4. Mevcut R³ Kodunu Oku (referans)
mi_beta/ear/r3/ altındaki 5 grubun feature_names listesini oku:
- psychoacoustic/consonance.py → 7 feature
- dsp/energy.py → 5 feature
- dsp/timbre.py → 9 feature
- dsp/change.py → 4 feature
- cross_domain/interactions.py → 24 feature
(Bu 49 feature'ın tam listesini al.)

### 5. Talep Matrisi Oluştur
Docs/R³/R3-DEMAND-MATRIX.md dosyasını yaz. İçeriği:

1. **Konsolide Gap Tablosu**: Tüm 57 gap, kategorize edilmiş
2. **Birim Bazlı Talep Özeti**: Her unit için hangi yeni R³ gruplarına ihtiyaç var
3. **Feature Talep Sıralaması**: En çok talep edilen eksik feature'lar (kaç model istiyor)
4. **96 Model × Mevcut 49D Kullanım Matrisi**: Hangi model hangi feature'ı okuyor
5. **96 Model × İstenen Yeni Feature Matrisi**: Her model için önerilen yeni R³ bağlantıları
6. **Öncelik Sıralaması**: Hangi yeni grup/feature en çok modele fayda sağlar

Format: Her tablo markdown table. Veriye dayalı, yorum minimal.

## Kurallar
- Sadece OKUMA ve YAZMA yap — mevcut dosyaları DEĞİŞTİRME
- Tek çıktı dosyası: Docs/R³/R3-DEMAND-MATRIX.md
- Literature/ ve mi_beta/ READ-ONLY
- İşin bitince progress dosyasını güncelle
```

#### Chat R2 Prompt: Local Literature + Psychoacoustic DSP Survey

```
Sen Phase 3A-2 Chat R2'sin: Yerel Literatür ve Psikoakustik DSP Araştırması.

## Proje
/Volumes/SRC-9/SRC Musical Intelligence

## Görev
Literature/r3/ klasöründeki 121 markdown dosyasını ve mevcut R³ kodunu inceleyerek,
psikoakustik temelli ses ölçüm yöntemlerinin kapsamlı bir envanterini oluştur.

## Adımlar

### 1. Mevcut R³ Kodunu Anla (referans çerçeve)
mi_beta/ear/r3/ altındaki 5 grubu oku:
- psychoacoustic/consonance.py → 7D, hangi DSP yöntemleri kullanılıyor?
- dsp/energy.py → 5D
- dsp/timbre.py → 9D
- dsp/change.py → 4D
- cross_domain/interactions.py → 24D
Bu mevcut 49D'nin hem güçlü hem zayıf yanlarını not et.

### 2. Literature/r3/ Taraması
5 alt klasördeki 121 dosyayı tara:

**psychoacoustics/** (11 dosya):
- Consonance & Dissonance (Plomp-Levelt, Sethares, Helmholtz)
- Just Intonation (JI primer, Fundamental Principles)
- Pressnitzer 2000 (continuous perception)
- Neural correlates (elife-neural)
Her dosyadan: hangi ölçülebilir akustik özellik tanımlanıyor? Hesaplama yöntemi?

**dsp-and-ml/** (4 dosya):
- CNN spectral features survey
- Genre classification spectral features
- Modulation-based classification
- Microtonal transcription (Benetos 2015)
Her dosyadan: hangi feature set kullanılıyor? Mel'den hesaplanabilir mi?

**spectral-music/** (7 dosya):
- Spectral composition theory (Anderson, Chung, Fineberg, Stanford)
- Microtonal pitch organization
Her dosyadan: spectral müziğin hangi boyutları R³'e katkı sağlar?

**computational-music-theory/** (65 dosya):
- Tymoczko Geometry of Music (24 part) → tonal geometry, voice leading
- Neo-Riemannian theory (32 part) → transformational theory
- Balzano group theory → pitch class structure
- Julian Hook, Steven Rings, Lewin → transformational music theory
Her dosyadan: hangi hesaplanabilir müzikal boyut tanımlanıyor?

### 3. Feature Envanteri Oluştur
Her aday feature için:

| Alan | İçerik |
|------|--------|
| Feature Adı | snake_case isim |
| Kategori | Consonance/Energy/Timbre/Change/Pitch/Rhythm/Harmony/Information |
| Önerilen R³ Grubu | A-I (mevcut veya yeni) |
| Tanım | 1 cümle: ne ölçer? |
| Psikoakustik Temeli | Hangi algısal fenomene karşılık gelir? |
| Hesaplama Yöntemi | Mel spectrogram'dan nasıl hesaplanır? (formül veya algoritma) |
| Beklenen Aralık | [min, max] ve birim |
| Kaynak | Literature/r3/ dosya adı ve sayfa/bölüm referansı |
| Mevcut R³'te Var mı? | Evet (hangi index) / Hayır / Kısmen (proxy olarak) |
| Mel'den Hesaplanabilirlik | Doğrudan / Dolaylı (ara adım gerekli) / Mümkün değil |

### 4. Teorik Gruplar İçin Derinlik Analizi
Özellikle şu alanlarda derin analiz yap:
- **Consonance genişlemesi**: Plomp-Levelt modeli tam uygulanabilir mi? Sethares timbre-dependent dissonance? Roughness (Vassilakis 2005)?
- **Pitch boyutu**: Chroma (12D pitch class profile) mel'den nasıl? Tonnetz koordinatları?
- **Harmony boyutu**: Tymoczko'nun voice-leading geometry'si mel'den hesaplanabilir mi?
- **Information boyutu**: Shannon entropy zaten var (change grubunda) ama IDyOM-tarzı melodic/harmonic surprisal?

### 5. Çıktı Dosyası
Docs/R³/R3-DSP-SURVEY-THEORY.md dosyasını yaz. İçeriği:

1. **Executive Summary**: Kaç aday feature bulundu, kategoriler
2. **Mevcut R³ Güçlü/Zayıf Yanları**: Mevcut 49D'nin eleştirisi (literature temelli)
3. **Aday Feature Tablosu**: Yukarıdaki formatta tüm aday features
4. **Grup Bazlı Derinlik Analizi**: Her potansiyel yeni grup (F-I) için detaylı analiz
5. **Hesaplanabilirlik Matrisi**: Her feature için mel→feature hesaplanabilirlik değerlendirmesi
6. **Kaynak Referans Tablosu**: Literature/r3/ dosya → feature bağlantıları

## Kurallar
- Sadece OKUMA ve YAZMA — mevcut dosyaları DEĞİŞTİRME
- Tek çıktı dosyası: Docs/R³/R3-DSP-SURVEY-THEORY.md
- Literature/ ve mi_beta/ READ-ONLY
- Özellikle 121 markdown dosyasının İÇERİĞİNİ oku, sadece adlarını listele değil
- Her iddia için kaynak belirt (dosya adı + bölüm)
```

#### Chat R3 Prompt: Web Research + Computational DSP Survey

```
Sen Phase 3A-2 Chat R3'sin: Web Araştırması ve Hesaplamalı DSP Araştırması.

## Proje
/Volumes/SRC-9/SRC Musical Intelligence

## Görev
Web'den derin araştırma yaparak, modern ses analizi toolkit'lerinin ve
standartların sunduğu tüm hesaplanabilir özelliklerin kapsamlı envanterini oluştur.
Odak: mel spectrogram'dan hesaplanabilir, gerçek zamanlı (frame-level) özellikler.

## Adımlar

### 1. Mevcut R³ Kodunu Anla (referans çerçeve)
mi_beta/ear/r3/ altındaki 5 grubu oku:
- psychoacoustic/consonance.py → 7D
- dsp/energy.py → 5D
- dsp/timbre.py → 9D
- dsp/change.py → 4D
- cross_domain/interactions.py → 24D
Bu mevcut 49D'nin teknik uygulamasını anla.
Özellikle: input format (mel spectrogram B,128,T), output format (B,T,dim), [0,1] aralığı.

### 2. Web Araştırması: DSP Toolkit'ler
Her toolkit için web'den araştır ve feature set'ini çıkar:

**librosa** (Python audio analysis):
- Spectral features: centroid, bandwidth, contrast, rolloff, flatness, tonnetz
- Rhythm features: tempo, beat_frames, onset_strength, tempogram
- Pitch: piptrack, pyin (probabilistic YIN)
- Tonal: chroma_stft, chroma_cqt, chroma_cens
- MFCC: 13-40 coefficients
- Özellikle `librosa.feature` modülünün TAMAMI

**essentia** (C++/Python comprehensive):
- 600+ audio descriptor (tüm kategoriler)
- Tonal: key, chord, HPCP, tuning
- Rhythm: BPM, beats, onset rate, beat loudness
- Spectral: 30+ descriptor
- SFX: pitch salience, inharmonicity, dissonance (Essentia modeli)
- Lowlevel: spectral complexity, silence rate, dynamic complexity

**openSMILE / eGeMAPS** (emotion/paralinguistic):
- 88 eGeMAPS features: F0, jitter, shimmer, formants, HNR, spectral slopes
- ComParE feature set: 6373 features (büyük ama functional subset relevant)
- Özellikle: F0 statistics, loudness, spectral features, voice quality

**Madmom** (beat/onset specialist):
- Beat tracking (DBN, multi-model)
- Onset detection (spectral flux variants, CNN-based)
- Tempo estimation (autocorrelation, comb filter)
- Key estimation
- Note/pitch tracking

**CREPE / SPICE / pYIN** (neural pitch):
- CREPE: CNN-based monophonic pitch estimation, confidence score
- SPICE: CREPE successor, polyphonic capable
- pYIN: probabilistic YIN with HMM smoothing

**ISO / AES Standards**:
- ISO 532B: Zwicker loudness model (specific loudness per Bark band)
- ISO 226: Equal-loudness contours
- AES17: Audio measurement standards
- ITU-R BS.1770: Loudness measurement (LUFS)

### 3. Feature Sınıflandırma
Her feature için değerlendir:

| Alan | İçerik |
|------|--------|
| Feature Adı | Toolkit'teki orijinal isim |
| Toolkit | librosa / essentia / openSMILE / Madmom / CREPE / ISO |
| Kategori | Pitch / Rhythm / Harmony / Timbre / Energy / Change / Quality / Modulation |
| Boyut | Skaler (1D) / Vektör (nD) / Matris |
| Çerçeve | Frame-level (per-hop) / Segment-level / Global |
| Input | Mel spectrogram / Raw audio / CQT / STFT / diğer |
| Mel'den Türetilebilir mi? | Doğrudan / STFT geri dönüşüm ile / Hayır (raw audio gerekli) |
| Hesaplama Maliyeti | Düşük (<1ms/frame) / Orta (1-10ms) / Yüksek (>10ms) / GPU gerekli |
| R³ Uygunluğu | Yüksek / Orta / Düşük (neden?) |
| Önerilen R³ Grubu | A-I veya yeni |

### 4. Özellikle Araştırılacak Konular
Web'den derin araştır:
- **Chroma features**: 12D pitch class profile hesaplama yöntemleri (STFT vs CQT vs mel-based)
- **Pitch salience**: Mel spectrogram'dan F0 ve pitch confidence çıkarma
- **Syncopation index**: Witek et al. 2014 syncopation measure, hesaplama algoritması
- **Groove features**: Madison 2006, Janata 2012 groove operationalization
- **Harmonic tension**: Lerdahl 2001 tonal tension model, Herremans 2017 computational implementation
- **Information content**: IDyOM (Pearce 2005/2018) — mel'den yaklaşık IC hesaplanabilir mi?
- **Modulation spectrum**: Temporal modulation features (4-16 Hz AM for speech/music)
- **Spectral contrast**: Octave-band contrast (Jiang 2002)

### 5. Çıktı Dosyası
Docs/R³/R3-DSP-SURVEY-TOOLS.md dosyasını yaz. İçeriği:

1. **Executive Summary**: Toolkit sayısı, toplam feature sayısı, R³'e uygun olanlar
2. **Toolkit Bazlı Feature Tabloları**: Her toolkit için tam feature listesi + değerlendirme
3. **Mel-Uyumlu Feature Kataloğu**: Sadece mel spectrogram'dan (veya mel'den türetilebilir input'tan) hesaplanabilir olanlar
4. **Hesaplama Maliyeti Analizi**: Frame-level real-time uygunluk değerlendirmesi
5. **Önerilen Yeni R³ Grupları**: Her grup (F-I) için toolkit-temelli feature önerileri
6. **Karşılaştırma Matrisi**: Toolkit × Feature kategorisi matrisi (hangi toolkit ne sağlıyor)
7. **Implementation Referansları**: Her önerilen feature için kaynak kodu / API referansı

## Kurallar
- Web araştırması için WebSearch ve WebFetch kullan
- Mevcut dosyaları DEĞİŞTİRME
- Tek çıktı dosyası: Docs/R³/R3-DSP-SURVEY-TOOLS.md
- mi_beta/ READ-ONLY
- Tüm web kaynaklarını URL ile referans ver
- Özellikle "mel spectrogram'dan hesaplanabilir mi?" sorusuna her feature için net cevap ver
- Gerçek zamanlı (172 Hz frame rate, ~5.8ms/frame) çalışabilirlik değerlendir
```

#### Phase 3 Execution Order

```
Week 1: Parallel Research (3 chats)
├── Chat R1: Model Demand Analysis → R3-DEMAND-MATRIX.md
├── Chat R2: Literature DSP Survey → R3-DSP-SURVEY-THEORY.md
└── Chat R3: Web DSP Survey → R3-DSP-SURVEY-TOOLS.md

Week 2: Merge & Design (single session)
├── 3A-3: Merge 3 outputs → R3-CROSSREF.md
├── 3B-1: Design new groups → R3-V2-DESIGN.md
├── 3B-2: Design interactions
└── 3B-3: Design code changes

Week 3: Documentation (single or parallel)
├── 3C: Architecture docs (~20 files)
└── 3C: Per-unit mappings (9 files)

Week 4: Model Updates (4 parallel chats)
├── Chat M1: SPU + STU (23 models) → Section 4 update
├── Chat M2: IMU + ASU + NDU (33 models) → Section 4 update
├── Chat M3: MPU + PCU (20 models) → Section 4 update
└── Chat M4: ARU + RPU (20 models) → Section 4 update
```

### Phase 4: H³ Architecture (Docs/H³) ✅ COMPLETE

H³ transforms R³ spectral features into temporal morphological descriptors via 4-tuples `(r3_idx, horizon, morph, law)`. With R³ v2 expansion (49D→128D), H³ theoretical space grows from 112,896 to 294,912 dimensions. Actual usage remains sparse (~2.9% occupancy, ~8,600 tuples across 96 models).

**Delivered**: 73 files, ~13,000 lines, 12 directories + 96 model H³ section updates (R³ v2 projected expansion).

#### 4.0 Directory Architecture

```
Docs/H³/
├── 00-INDEX.md                              Master index
├── H3-TEMPORAL-ARCHITECTURE.md              Definitive architecture doc
├── CHANGELOG.md                             Version history
├── EXTENSION-GUIDE.md                       Developer extension guide
│
├── Registry/                                Canonical reference tables
│   ├── 00-INDEX.md
│   ├── HorizonCatalog.md                    32 horizons: ms, frames, band, musical meaning
│   ├── MorphCatalog.md                      24 morphs: formula, category, MORPH_SCALE
│   ├── LawCatalog.md                        3 laws: kernel formula, direction, usage
│   └── DemandAddressSpace.md                4-tuple space, flat index, sparsity
│
├── Bands/                                   Primary axis (= R³ Domains/)
│   ├── 00-INDEX.md                          Cross-band comparison
│   ├── Micro/                               H0-H7 (~6ms-250ms): Sensory processing
│   │   ├── 00-INDEX.md
│   │   ├── H0-H5-SubBeat.md                Onset, attack, spectral transient
│   │   └── H6-H7-BeatSubdivision.md        Short note, beat subdivision
│   ├── Meso/                                H8-H15 (~300ms-800ms): Beat/phrase
│   │   ├── 00-INDEX.md
│   │   ├── H8-H11-BeatPeriod.md            Quarter note tempo range, BEP core
│   │   └── H12-H15-Phrase.md               Motif, measure, SYN entry
│   ├── Macro/                               H16-H23 (~1s-25s): Section
│   │   ├── 00-INDEX.md
│   │   ├── H16-H17-Measure.md              TMH entry, bridge phrase-section
│   │   └── H18-H23-Section.md              MEM, C0P primary, long-term encoding
│   └── Ultra/                               H24-H31 (~36s-981s): Movement/piece
│       ├── 00-INDEX.md
│       ├── H24-H28-Movement.md              Exposition to standard movement
│       └── H29-H31-Piece.md                 Full work, maximum context
│
├── Morphology/                              Cross-cutting morph documentation
│   ├── 00-INDEX.md
│   ├── Distribution.md                      M0-M7 (value, mean, std, median, max, range, skew, kurt)
│   ├── Dynamics.md                          M8-M13, M15, M18, M21 (velocity, accel, trend)
│   ├── Rhythm.md                            M14, M17, M22 (periodicity, shape_period, peaks)
│   ├── Information.md                       M20 (Shannon entropy)
│   ├── Symmetry.md                          M16, M19, M23 (curvature, stability, symmetry)
│   └── MorphScaling.md                      MORPH_SCALE calibration (gain/bias per morph)
│
├── Laws/                                    Cross-cutting law documentation
│   ├── 00-INDEX.md
│   ├── L0-Memory.md                         Past->present (causal, exp decay)
│   ├── L1-Prediction.md                     Present->future (anticipatory)
│   └── L2-Integration.md                    Past<->future (bidirectional)
│
├── Contracts/                               Interface specifications
│   ├── 00-INDEX.md
│   ├── H3Extractor.md                       Orchestrator: demand->extraction->output
│   ├── DemandTree.md                        Sparse routing: horizon-keyed demands
│   ├── EventHorizon.md                      Horizon wrapper: frames, ms, seconds
│   ├── MorphComputer.md                     24-morph dispatch
│   └── AttentionKernel.md                   A(dt) = exp(-3|dt|/H)
│
├── Pipeline/                                Execution architecture
│   ├── 00-INDEX.md
│   ├── ExecutionModel.md                    Demand aggregation -> horizon loop -> morph
│   ├── SparsityStrategy.md                  Sparse computation rationale + analysis
│   ├── Performance.md                       Per-horizon cost, GPU strategy
│   └── WarmUp.md                            Horizon-dependent warm-up requirements
│
├── Demand/                                  Per-unit H³ demand (= R³ Mappings/)
│   ├── 00-INDEX.md                          Cross-unit comparison, grand total
│   ├── SPU-H3-DEMAND.md                     9 models, PPC/TPC, micro-macro (~450 tuples)
│   ├── STU-H3-DEMAND.md                     14 models, BEP/TMH, all bands (~900 tuples)
│   ├── IMU-H3-DEMAND.md                     15 models, MEM/TMH, macro-ultra (~1,200 tuples)
│   ├── ASU-H3-DEMAND.md                     9 models, ASA, micro-meso (~360 tuples)
│   ├── NDU-H3-DEMAND.md                     9 models, ASA/PPC/TMH, all bands (~400 tuples)
│   ├── MPU-H3-DEMAND.md                     10 models, BEP, micro-meso (~500 tuples)
│   ├── PCU-H3-DEMAND.md                     10 models, all mechanisms, all bands (~500 tuples)
│   ├── ARU-H3-DEMAND.md                     10 models, AED/CPD/C0P, macro (~500 tuples)
│   └── RPU-H3-DEMAND.md                     10 models, AED/CPD/C0P/TMH/BEP (~400 tuples)
│
├── Expansion/                               R³ v2 impact on H³
│   ├── 00-INDEX.md
│   ├── R3v2-H3-Impact.md                    49D->128D: space expansion, demand, code changes
│   ├── F-PitchChroma-Temporal.md            [49:65] chroma evolution, pitch trajectory
│   ├── G-RhythmGroove-Temporal.md           [65:75] tempo stability, groove evolution
│   ├── H-HarmonyTonality-Temporal.md        [75:87] harmonic rhythm, key trajectory
│   ├── I-InformationSurprise-Temporal.md    [87:94] entropy rate, surprise dynamics
│   ├── J-TimbreExtended-Temporal.md         [94:114] MFCC evolution, contrast dynamics
│   └── K-ModulationPsychoacoustic-Temporal.md [114:128] modulation evolution
│
├── Standards/                               Quality & compliance
│   ├── 00-INDEX.md
│   ├── MorphQualityTiers.md                 Per-morph quality assessment
│   └── TemporalResolutionStandards.md       Min window sizes, numerical stability
│
├── Validation/                              Testing & benchmarks
│   ├── 00-INDEX.md
│   ├── AcceptanceCriteria.md                Per-morph/horizon output validation
│   └── BenchmarkPlan.md                     Morph accuracy, scaling tests
│
├── Literature/                              Academic references
│   ├── 00-INDEX.md
│   └── H3-LITERATURE.md                     Temporal processing references
│
└── Migration/                               Version migration
    ├── 00-INDEX.md
    ├── V1-to-V2.md                          49D->128D H3 migration guide
    └── DemandSpec-Update.md                 r3_idx 0-48 -> 0-127
```

#### 4.1 R³ v2 Expansion Impact on H³

R³ v2 adds 79 new features [49:128] that serve as H³ temporal demand targets. New estimated demand:

| R³ Group | Features | Temporal Priority | Key H³ Horizons | Est. New Tuples |
|----------|:--------:|:-----------------:|:---------------:|:---------------:|
| F: Pitch [49:65] | 16D | HIGH | H3-H16 (meso-macro) | ~800-1200 |
| G: Rhythm [65:75] | 10D | HIGH | H12-H22 (meso-macro) | ~400-600 |
| H: Harmony [75:87] | 12D | HIGH | H12-H22 (meso-macro) | ~500-800 |
| I: Information [87:94] | 7D | MEDIUM-HIGH | H6-H22 (meso-macro) | ~300-500 |
| J: Timbre Ext [94:114] | 20D | MEDIUM | H6-H18 (meso) | ~400-700 |
| K: Modulation [114:128] | 14D | MEDIUM | H16-H25 (macro) | ~200-400 |
| **Total new** | **79D** | | | **~2,600-4,200** |

**Updated H³ system totals**:
- Theoretical space: 128 x 32 x 24 x 3 = **294,912** (was 112,896)
- Estimated actual: ~5,200 (existing) + ~3,400 (R³ v2) = **~8,600 tuples**
- Occupancy: **~2.9%** (was ~4.6% — denominator grows faster)

#### 4.2 Sub-Phase Execution Order

| Sub-Phase | Description | Files | Lines | Depends On |
|:---------:|-------------|:-----:|:-----:|:----------:|
| **4A** | Foundation: ARCHITECTURE, INDEX, CHANGELOG | 4 | ~770 | None |
| **4B** | Registry: HorizonCatalog, MorphCatalog, LawCatalog, DemandAddress | 4 | ~770 | 4A |
| **4C** | Bands: 4 bands x (index + 2 horizon docs) | 11 | ~1,970 | 4B |
| **4D** | Morphology + Laws: 7 morph docs + 4 law docs | 11 | ~1,470 | 4B (parallel with 4C) |
| **4E** | Contracts + Pipeline: 6 interface + 5 execution docs | 11 | ~1,430 | 4C, 4D |
| **4F** | Demand: 9 per-unit demand + index | 10 | ~2,050 | 4E |
| **4G** | Expansion: R³ v2 impact + 6 per-group temporal docs | 8 | ~1,410 | 4F |
| **4H** | Standards + Validation + Literature + Migration | 11 | ~1,440 | All prior |
| **4I** | Cross-references: update C³ docs to link H³ | ~6 | ~200 | All prior |

```
Dependency Graph:
4A -> 4B -> 4C ─┐
          └─ 4D ┤-> 4E -> 4F -> 4G -> 4H -> 4I
```

**Quality gates:**
1. Every H³ demand tuple has a purpose, citation, and link to its R³ feature
2. All 32 horizons documented with ms, frames, musical meaning, mechanism mapping
3. All 24 morphs documented with formula, category, MORPH_SCALE calibration
4. All 3 laws documented with kernel formula and usage pattern
5. Per-unit demand docs cover all 96 models
6. R³ v2 expansion docs specify new temporal demands for all 6 new groups (F-K)
7. H3DemandSpec r3_idx range updated from [0:48] to [0:127]

### Phase 5: L³ Architecture (Docs/L³) ✅ COMPLETE

L³ (Lexical LOGOS Lattice) is MI's **semantic interpretation layer** — the final stage in the Audio → R³ → H³ → C³ → **L³** → MI-space pipeline. It transforms unified Brain output (26D in mi_beta, variable depending on active units/models) into **104 dimensions of meaning** across 8 epistemological groups (α→θ), organized in 2 computation phases. Zero learned parameters — every dimension has a citation.

**Problem:** R³, H³, and C³ all had complete modular documentation architectures (71, 73, 160+ files respectively). L³ had only **4 flat files** — 3 deprecated per-model semantic spaces (SRP, AAC, VMM) + 1 active unified doc (BRAIN-SEMANTIC-SPACE, 999 lines). This made L³ the only undocumented layer in the pipeline.

**Delivered:** 69 files, ~10,350 lines, 13 subdirectories + 2 sub-directories under Groups/, mirroring H³/C³/R³ patterns.

#### 5.0 L³ Core Architecture

```
Input: MusicalBrain (26D variable)
  Shared(4D) Reward(9D) Affect(6D) Autonomic(5D) Integration(2D)
                          ↓
  Phase 1 — Independent (read only BrainOutput):
    α Computation     HOW computed?              6D (variable)
    β Neuroscience    WHERE in brain?            14D (variable)
    γ Psychology      WHAT subjectively?         13D
    δ Validation      HOW to test?               12D
  Phase 1b — Stateful:
    ε Learning        HOW does listener learn?   19D (EMA, Markov, Welford, ring buffer)
                          ↓
  Phase 2 — Dependent (ε→ζ→η, ε+ζ→θ):
    ζ Polarity        WHICH direction? [-1,+1]   12D
    η Vocabulary      WHAT word? (64 gradation)  12D
    θ Narrative       HOW to describe?           16D
                          ↓
  Output: L3Output (B, T, 104D variable)
  Total: 6+14+13+12+19+12+12+16 = 104D per frame
```

**Key architectural features:**
- **8-level Epistemological Ladder:** Each group answers one progressively deeper question (computation → language)
- **2-Phase Dependency:** Phase 1 groups read only Brain output; Phase 2 chain through ε→ζ→η→θ
- **Variable Dimensionality:** α (per-unit attribution) and β (per-region activation) auto-configure based on active units/models
- **Stateful Computation:** Only ε maintains state (EMA accumulators ×3 timescales, Markov 8×8 transition matrix, Welford online variance, ring buffer size 50)
- **64-Gradation Vocabulary:** η quantizes 12 polarity axes into 64 levels with 96 descriptive terms (JND-aligned, Weber/Stevens)
- **Narrative Sentence Structure:** θ produces 4-slot sentences (subject + predicate + modifier + connector, each 4D, softmax temp=3.0)
- **9 Per-Unit Adapters:** Each Brain unit has a semantic adapter mapping model outputs to group inputs (all currently stubs in mi_beta)

#### 5.1 Directory Architecture

```
Docs/L³/
├── 00-INDEX.md                              Master index
├── L3-SEMANTIC-ARCHITECTURE.md              Definitive architecture doc (~800 lines)
├── CHANGELOG.md                             Version history (v1.0→v2.0→v2.1)
├── EXTENSION-GUIDE.md                       Developer guide (add groups/dims/adapters)
│
├── Registry/                                Canonical reference tables
│   ├── 00-INDEX.md
│   ├── DimensionCatalog.md                  All 104 dimensions: index, group, name, range, formula
│   ├── GroupMap.md                           8 groups: index range, dim, phase, dependencies
│   └── NamingConventions.md                 Greek letters, snake_case, range conventions
│
├── Epistemology/                            L³-UNIQUE: 8-level framework theory
│   ├── 00-INDEX.md                          Framework overview
│   ├── Computation.md                       Level 1 (α): HOW computed?
│   ├── Neuroscience.md                      Level 2 (β): WHERE in brain?
│   ├── Psychology.md                        Level 3 (γ): WHAT does it mean?
│   ├── Validation.md                        Level 4 (δ): HOW to test?
│   ├── Learning.md                          Level 5 (ε): HOW does listener learn?
│   ├── Polarity.md                          Level 6 (ζ): WHICH direction?
│   ├── Vocabulary.md                        Level 7 (η): WHAT word?
│   └── Narrative.md                         Level 8 (θ): HOW to describe?
│
├── Groups/                                  Per-group detailed specifications
│   ├── 00-INDEX.md                          Cross-group comparison table
│   ├── Independent/                         Phase 1 groups
│   │   ├── 00-INDEX.md
│   │   ├── Alpha.md                         α: per-unit attribution + certainty (variable D)
│   │   ├── Beta.md                          β: 8 regions + 3 NTs + 3 circuits (variable D)
│   │   ├── Gamma.md                         γ: reward(3) + ITPRA(2) + aesthetics(3) + emotion(2) + chills(3)
│   │   ├── Delta.md                         δ: physiological(4) + neural(3) + behavioral(2) + temporal(3)
│   │   └── Epsilon.md                       ε: STATEFUL; EMA×3, Markov 8×8, Welford, ring buffer
│   └── Dependent/                           Phase 2 groups
│       ├── 00-INDEX.md
│       ├── Zeta.md                          ζ: 12 bipolar axes [-1,+1], reward/learning/aesthetic
│       ├── Eta.md                           η: 64-gradation quantization, 96 terms, get_terms()
│       └── Theta.md                         θ: subject(4) + predicate(4) + modifier(4) + connector(4)
│
├── Vocabulary/                              L³-UNIQUE: 64-gradation system
│   ├── 00-INDEX.md
│   ├── TermCatalog.md                       96 terms (12 axes × 8 bands) — matches eta.py
│   ├── GradationSystem.md                   64-level design + JND rationale (Weber/Stevens)
│   └── AxisDefinitions.md                   12 polarity axes: neg↔pos, source, formula, citation
│
├── Contracts/                               Interface specifications
│   ├── 00-INDEX.md                          5 contracts overview
│   ├── BaseSemanticGroup.md                 ABC: LEVEL, GROUP_NAME, OUTPUT_DIM, compute()
│   ├── SemanticGroupOutput.md               Dataclass: group_name, level, tensor(B,T,D)
│   ├── BaseModelSemanticAdapter.md          Per-unit adapter ABC: UNIT_NAME, adapt()
│   ├── L3Orchestrator.md                    Orchestrator: group ordering, phases, reset()
│   └── EpsilonStateContract.md              State: 6 EMA, 2 Welford, Markov 8×8, ring 50
│
├── Pipeline/                                Execution architecture
│   ├── 00-INDEX.md
│   ├── DependencyDAG.md                     brain→α,β,γ,δ,ε→ζ→η→θ
│   ├── ExecutionModel.md                    Phase 1 → 1b → 2a → 2b → 2c sequence
│   ├── StateManagement.md                   Epsilon lifecycle: init → accumulate → reset
│   └── Performance.md                       Per-group cost, memory (ε state: ~B×230 floats)
│
├── Adapters/                                L³-UNIQUE: Per-unit semantic mapping
│   ├── 00-INDEX.md                          Cross-unit adapter comparison (all "stub")
│   ├── SPU-L3-ADAPTER.md                    Spectral → semantic
│   ├── STU-L3-ADAPTER.md                    Timing → semantic
│   ├── IMU-L3-ADAPTER.md                    Memory → semantic
│   ├── ASU-L3-ADAPTER.md                    Salience → semantic
│   ├── NDU-L3-ADAPTER.md                    Novelty → semantic
│   ├── MPU-L3-ADAPTER.md                    Motor → semantic
│   ├── PCU-L3-ADAPTER.md                    Prediction → semantic
│   ├── ARU-L3-ADAPTER.md                    Affect → semantic
│   └── RPU-L3-ADAPTER.md                    Reward → semantic
│
├── Standards/                               Quality & compliance
│   ├── 00-INDEX.md
│   ├── CitationQuality.md                   Per-dimension audit: citation, N, method, status
│   └── PsychometricAlignment.md             GEMS, SDT, Russell circumplex, Osgood, ITPRA
│
├── Validation/                              Testing & benchmarks
│   ├── 00-INDEX.md
│   ├── AcceptanceCriteria.md                Per-group: shape, range [0,1]/[-1,+1], NaN check
│   └── BenchmarkPlan.md                     δ vs SCR/HR, γ vs ratings, η vs GEMS
│
├── Literature/                              Academic references
│   ├── 00-INDEX.md
│   └── L3-LITERATURE.md                     Per-dimension cross-ref (104D, 40+ papers)
│
├── Migration/                               Version migration
│   ├── 00-INDEX.md
│   ├── V1-to-V2.md                          Per-model → unified Brain migration
│   └── DeprecatedFiles.md                   Archive inventory + replacement mapping
│
└── Archive/                                 Deprecated files
    ├── 00-INDEX.md
    ├── L3-SRP-SEMANTIC-SPACE.md             v1.x SRP-only (DEPRECATED)
    ├── L3-AAC-SEMANTIC-SPACE.md             v1.x AAC-only (DEPRECATED)
    ├── L3-VMM-SEMANTIC-SPACE.md             v1.x VMM-only (DEPRECATED)
    └── L3-BRAIN-SEMANTIC-SPACE.md           v2.0 unified (archived, decomposed into modular)
```

#### 5.2 Code-to-Documentation Mapping

| Documentation File | Code File | Role |
|-------------------|-----------|------|
| `00-INDEX.md` | `mi_beta/language/__init__.py` | Package entry point |
| `Groups/Independent/Alpha.md` | `mi_beta/language/groups/alpha.py` | α group: per-unit attribution |
| `Groups/Independent/Beta.md` | `mi_beta/language/groups/beta.py` | β group: brain region mapping |
| `Groups/Independent/Gamma.md` | `mi_beta/language/groups/gamma.py` | γ group: psychological meaning |
| `Groups/Independent/Delta.md` | `mi_beta/language/groups/delta.py` | δ group: validation predictions |
| `Groups/Independent/Epsilon.md` | `mi_beta/language/groups/epsilon.py` (336 lines) | ε group: STATEFUL learning |
| `Groups/Dependent/Zeta.md` | `mi_beta/language/groups/zeta.py` (145 lines) | ζ group: polarity mapping |
| `Groups/Dependent/Eta.md` | `mi_beta/language/groups/eta.py` (176 lines) | η group: vocabulary (96 terms) |
| `Groups/Dependent/Theta.md` | `mi_beta/language/groups/theta.py` | θ group: narrative structure |
| `Contracts/BaseSemanticGroup.md` | `mi_beta/contracts/base_semantic_group.py` (169 lines) | Group ABC contract |
| `Contracts/BaseModelSemanticAdapter.md` | `mi_beta/language/adapters/_base_adapter.py` (15 lines) | Adapter ABC |
| `Contracts/L3Orchestrator.md` | `mi_beta/language/groups/__init__.py` (141 lines) | Orchestrator |
| `Adapters/{UNIT}-L3-ADAPTER.md` (×9) | `mi_beta/language/adapters/{unit}_adapter.py` | Per-unit adapters (all stubs) |
| `Registry/DimensionCatalog.md` | `mi_beta/core/types.py` (L3Output, SemanticGroupOutput) | Output type definitions |

#### 5.3 Sub-Phase Execution Order

| Sub-Phase | Description | Files | Est. Lines | Depends On |
|:---------:|-------------|:-----:|:----------:|:----------:|
| **5A** | Foundation: INDEX, ARCHITECTURE, CHANGELOG, EXTENSION-GUIDE, Registry (4) | 8 | ~1,810 | None |
| **5B** | Epistemology (9) + Groups (11): per-level theory + per-group specs | 20 | ~3,140 | 5A |
| **5C** | Vocabulary (4) + Contracts (6): 96 terms, 5 interface specs | 10 | ~1,250 | 5A, 5B |
| **5D** | Pipeline (5) + Adapters (10): DAG, execution, 9 per-unit adapters | 15 | ~1,590 | 5A, 5B, 5C |
| **5E** | Standards (3) + Validation (3) + Literature (2): audit, benchmarks, refs | 8 | ~1,150 | 5A, 5B |
| **5F** | Migration (3) + Archive (5): v1→v2 guide, 4 deprecated file copies | 8 | ~1,410 | All prior |
| **5G** | Cross-references: update Beta_upgrade.md, verify internal links | ~3 edits | ~200 | All prior |
| | **Total** | **69** | **~10,350** | |

```
Dependency Graph:
5A → 5B → 5C → 5D ─┐
               └─ 5E ┤→ 5F → 5G
```

5D and 5E run in parallel after 5C completes.

#### 5.4 Sub-Phase Details

**Sub-phase 5A — Foundation (Root + Registry): 8 files, ~1,810 lines**

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 1 | `Docs/L³/00-INDEX.md` | ~140 | Master index: overview, 104D summary, directory tree, code mapping |
| 2 | `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` | ~800 | Definitive architecture: 8 groups, phases, all formulas, full dimension inventory |
| 3 | `Docs/L³/CHANGELOG.md` | ~80 | Version history: v1.0 (per-model) → v2.0 (unified Brain) → v2.1 (modular docs) |
| 4 | `Docs/L³/EXTENSION-GUIDE.md` | ~300 | Developer guide: how to add groups, axes, vocabulary terms, adapters |
| 5 | `Docs/L³/Registry/00-INDEX.md` | ~40 | Registry overview with quick reference table |
| 6 | `Docs/L³/Registry/DimensionCatalog.md` | ~250 | All 104 dimensions: global index, group, name, range, formula, citation |
| 7 | `Docs/L³/Registry/GroupMap.md` | ~120 | 8 groups: index range [α0:6, β6:20, ...104], phase, deps, code file |
| 8 | `Docs/L³/Registry/NamingConventions.md` | ~80 | Greek letters, snake_case dims, range conventions |

Source: `L³-BRAIN-SEMANTIC-SPACE.md` (sections 1-3, 7) + `mi_beta/language/groups/__init__.py`
Quality gate: DimensionCatalog lists all 104D with correct index ranges summing to 104. GroupMap maps to code files.

**Sub-phase 5B — Epistemology (9) + Groups (11) = 20 files, ~3,140 lines**

*Epistemology/ — 8-level interpretive framework theory:*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 9 | `Epistemology/00-INDEX.md` | ~120 | 8-level ladder: level, question, audience, citations |
| 10 | `Epistemology/Computation.md` | ~100 | Level 1 (α): white-box attribution, Bayesian precision |
| 11 | `Epistemology/Neuroscience.md` | ~150 | Level 2 (β): brain region mapping, neurotransmitter dynamics |
| 12 | `Epistemology/Psychology.md` | ~130 | Level 3 (γ): ITPRA, circumplex, wanting/liking, aesthetics |
| 13 | `Epistemology/Validation.md` | ~120 | Level 4 (δ): physiological predictions, neural correlates |
| 14 | `Epistemology/Learning.md` | ~200 | Level 5 (ε): predictive coding, Schmidhuber, Markov, IDyOM, Wundt |
| 15 | `Epistemology/Polarity.md` | ~120 | Level 6 (ζ): semantic differential (Osgood), circumplex (Russell) |
| 16 | `Epistemology/Vocabulary.md` | ~150 | Level 7 (η): prototype theory (Rosch), semantic fields (Trier) |
| 17 | `Epistemology/Narrative.md` | ~150 | Level 8 (θ): sentence structure, cohesion (Halliday), narrative (Almén) |

*Groups/ — Per-group computation specifications:*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 18 | `Groups/00-INDEX.md` | ~100 | Cross-group table: dim, phase, stateful?, deps |
| 19 | `Groups/Independent/00-INDEX.md` | ~60 | Phase 1 overview |
| 20 | `Groups/Independent/Alpha.md` | ~150 | α: per-unit attribution + certainty + bipolar (variable D) |
| 21 | `Groups/Independent/Beta.md` | ~200 | β: 8 regions + 3 neurotransmitters + 3 circuits (variable D) |
| 22 | `Groups/Independent/Gamma.md` | ~180 | γ: reward(3D) + ITPRA(2D) + aesthetics(3D) + emotion(2D) + chills(3D) = 13D |
| 23 | `Groups/Independent/Delta.md` | ~160 | δ: physiological(4D) + neural(3D) + behavioral(2D) + temporal(3D) = 12D |
| 24 | `Groups/Independent/Epsilon.md` | ~350 | ε: STATEFUL 19D; EMA×3 timescales, Markov 8×8, Welford, ring buffer 50, ITPRA-5D |
| 25 | `Groups/Dependent/00-INDEX.md` | ~60 | Phase 2 overview: ε→ζ→η, ε+ζ→θ dependency chain |
| 26 | `Groups/Dependent/Zeta.md` | ~180 | ζ: 12 bipolar axes [-1,+1], reward/learning/aesthetic categories |
| 27 | `Groups/Dependent/Eta.md` | ~200 | η: 64-gradation quantization, 96 terms (12×8), get_terms() |
| 28 | `Groups/Dependent/Theta.md` | ~200 | θ: subject(4D) + predicate(4D) + modifier(4D) + connector(4D) = 16D |

Source: `L³-BRAIN-SEMANTIC-SPACE.md` (sections 2, 4, 5, 6) + code files `alpha.py` through `theta.py`
Quality gate: Every group doc has complete dimension table + all formulas + code mapping. Epsilon covers all 5 state components. Alpha/Beta document variable-D behavior.

**Sub-phase 5C — Vocabulary (4) + Contracts (6) = 10 files, ~1,250 lines**

*Vocabulary/ — 64-gradation descriptor system:*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 29 | `Vocabulary/00-INDEX.md` | ~60 | System overview: 12 axes × 8 bands × 8 gradations |
| 30 | `Vocabulary/TermCatalog.md` | ~200 | Complete 12×8 term table (96 terms) — MUST match `eta.py` AXIS_TERMS |
| 31 | `Vocabulary/GradationSystem.md` | ~150 | 64-level quantization: JND (Weber/Stevens), bit budget (72 bits) |
| 32 | `Vocabulary/AxisDefinitions.md` | ~180 | 12 axes: neg pole ↔ pos pole, source dimension, formula, citation |

*Contracts/ — Interface specifications:*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 33 | `Contracts/00-INDEX.md` | ~60 | 5 contracts overview |
| 34 | `Contracts/BaseSemanticGroup.md` | ~150 | ABC: LEVEL, GROUP_NAME, OUTPUT_DIM, compute(), dimension_names, validate() |
| 35 | `Contracts/SemanticGroupOutput.md` | ~80 | Dataclass: group_name, level, tensor(B,T,D), dimension_names |
| 36 | `Contracts/BaseModelSemanticAdapter.md` | ~100 | Adapter ABC: UNIT_NAME, adapt(UnitOutput) → Dict[str, Tensor] |
| 37 | `Contracts/L3Orchestrator.md` | ~150 | Orchestrator: OrderedDict, phase execution, reset(), total_dim property |
| 38 | `Contracts/EpsilonStateContract.md` | ~120 | State layout: 6 EMA tensors, 6 variance tensors, Welford(3), Markov(2), ring(3), prev_pleasure(1) |

Source: `eta.py` AXIS_TERMS, `base_semantic_group.py`, `epsilon.py` state components
Quality gate: TermCatalog matches `eta.py` AXIS_TERMS exactly (96 terms, zero drift). Every contract maps to a code file.

**Sub-phase 5D — Pipeline (5) + Adapters (10) = 15 files, ~1,590 lines**

*Pipeline/ — Execution architecture:*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 39 | `Pipeline/00-INDEX.md` | ~50 | Pipeline overview |
| 40 | `Pipeline/DependencyDAG.md` | ~120 | ASCII dependency graph: brain→α,β,γ,δ,ε→ζ→η→θ |
| 41 | `Pipeline/ExecutionModel.md` | ~150 | Phase 1 (parallel) → Phase 1b (stateful ε) → Phase 2a (ζ) → 2b (η) → 2c (θ) |
| 42 | `Pipeline/StateManagement.md` | ~150 | Epsilon lifecycle: lazy init → accumulate per frame → reset between audio files |
| 43 | `Pipeline/Performance.md` | ~100 | Per-group compute cost, memory (ε state: ~B×230 floats), total latency |

*Adapters/ — Per-unit semantic mapping (L³-UNIQUE):*

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 44 | `Adapters/00-INDEX.md` | ~120 | Cross-unit comparison table, status column (all "stub" currently) |
| 45 | `Adapters/SPU-L3-ADAPTER.md` | ~100 | SPU: consonance→beauty, timbre→complexity, pitch→novelty |
| 46 | `Adapters/STU-L3-ADAPTER.md` | ~100 | STU: beat→groove, tempo→arousal, sync→engagement |
| 47 | `Adapters/IMU-L3-ADAPTER.md` | ~100 | IMU: familiarity→stability, recall→imagination |
| 48 | `Adapters/ASU-L3-ADAPTER.md` | ~100 | ASU: novelty→surprise, attention→engagement |
| 49 | `Adapters/NDU-L3-ADAPTER.md` | ~100 | NDU: deviation→surprise, PE→tension, entropy→complexity |
| 50 | `Adapters/MPU-L3-ADAPTER.md` | ~100 | MPU: groove→groove, movement→motion |
| 51 | `Adapters/PCU-L3-ADAPTER.md` | ~100 | PCU: prediction_error→surprise, certainty→stability |
| 52 | `Adapters/ARU-L3-ADAPTER.md` | ~100 | ARU: pleasure→valence, tension→tension, chills→beauty |
| 53 | `Adapters/RPU-L3-ADAPTER.md` | ~100 | RPU: DA→wanting, opioid→liking, reward_PE→reward_pe |

Source: `mi_beta/language/groups/__init__.py` + `mi_beta/language/adapters/*.py` + `Docs/C³/Units/*.md`
Quality gate: DAG matches `L3Orchestrator.compute()` execution order. All 9 adapters status = "stub" (matching code). Each adapter maps unit dims to semantic inputs.

**Sub-phase 5E — Standards (3) + Validation (3) + Literature (2) = 8 files, ~1,150 lines**

| # | File | Lines | Description |
|---|------|:-----:|-------------|
| 54 | `Standards/00-INDEX.md` | ~40 | Standards overview |
| 55 | `Standards/CitationQuality.md` | ~200 | Per-dimension audit: citation, effect size, N, method, status |
| 56 | `Standards/PsychometricAlignment.md` | ~150 | Alignment with GEMS, SDT, Russell circumplex, Osgood, ITPRA, Berridge |
| 57 | `Validation/00-INDEX.md` | ~50 | Validation strategy |
| 58 | `Validation/AcceptanceCriteria.md` | ~150 | Per-group: shape, range [0,1]/[-1,+1], NaN/Inf checks |
| 59 | `Validation/BenchmarkPlan.md` | ~200 | δ vs real SCR/HR, γ vs emotion ratings, η vs GEMS |
| 60 | `Literature/00-INDEX.md` | ~60 | Literature organization |
| 61 | `Literature/L3-LITERATURE.md` | ~300 | Per-dimension cross-ref: all 104 dims, 40+ papers |

Source: `L³-BRAIN-SEMANTIC-SPACE.md` section 8 (references) + published psychometric instruments
Quality gate: CitationQuality audits all 40+ papers from BRAIN doc. L3-LITERATURE covers all 104 dimensions.

**Sub-phase 5F — Migration (3) + Archive (5) = 8 files, ~1,410 lines**

| # | Action | File | Lines | Description |
|---|--------|------|:-----:|-------------|
| 62 | CREATE | `Migration/00-INDEX.md` | ~40 | Migration overview |
| 63 | CREATE | `Migration/V1-to-V2.md` | ~150 | Per-model → unified Brain migration guide |
| 64 | CREATE | `Migration/DeprecatedFiles.md` | ~80 | Archive inventory + replacement mapping table |
| 65 | CREATE | `Archive/00-INDEX.md` | ~40 | Archive overview with deprecation dates |
| 66 | COPY | `Archive/L3-SRP-SEMANTIC-SPACE.md` | ~600 | v1.x SRP-only (DEPRECATED, source preserved) |
| 67 | COPY | `Archive/L3-AAC-SEMANTIC-SPACE.md` | ~800 | v1.x AAC-only (DEPRECATED, source preserved) |
| 68 | COPY | `Archive/L3-VMM-SEMANTIC-SPACE.md` | ~200 | v1.x VMM-only (DEPRECATED, source preserved) |
| 69 | COPY | `Archive/L3-BRAIN-SEMANTIC-SPACE.md` | ~999 | v2.0 unified (archived, decomposed into modular docs) |

Source: Existing deprecated files + modular docs as target mapping
Quality gate: All 4 deprecated/source files archived with no content loss. V1-to-V2 documents every change.

**Sub-phase 5G — Cross-References and Integration: ~3 edits, ~200 lines**

| File Updated | Change |
|-------------|--------|
| `Docs/Beta/Beta_upgrade.md` | Replace Phase 5 stub with complete architecture (this section) |
| `Docs/Beta/Beta_upgrade.md` | Add 9 L³ entries to Critical File Paths table |
| `Docs/Beta/Beta_upgrade.md` | Mark Phase 5 complete in verification checklist |

Quality gate: Zero broken links. R³→H³→C³→L³ chain documented in all architecture docs.

#### 5.5 Data Sources

| Source | Location | Content |
|--------|----------|---------|
| L³ BRAIN doc | `Docs/L³/L³-BRAIN-SEMANTIC-SPACE.md` (999 lines) | Primary source: 8 groups, 104D, formulas, references |
| L³ deprecated docs (3) | `Docs/L³/L³-{SRP,AAC,VMM}-SEMANTIC-SPACE.md` | v1.x per-model semantic spaces |
| L³ orchestrator code | `mi_beta/language/groups/__init__.py` (141 lines) | L3Orchestrator: phase execution, dependency ordering |
| L³ group code (8) | `mi_beta/language/groups/{alpha..theta}.py` | Per-group computation: formulas, state, dims |
| L³ adapter code (9) | `mi_beta/language/adapters/{unit}_adapter.py` | Per-unit semantic adapters (all stubs) |
| L³ contracts | `mi_beta/contracts/base_semantic_group.py` (169 lines) | BaseSemanticGroup ABC + SemanticGroupOutput |
| Adapter base | `mi_beta/language/adapters/_base_adapter.py` (15 lines) | BaseModelSemanticAdapter ABC |
| H³/C³/R³ docs | `Docs/{H³,C³,R³}/` | Pattern reference for modular documentation architecture |

#### 5.6 Quality Gates

1. Every L³ semantic group has a specification doc with inputs, computation, and output meaning
2. All 104 dimensions documented with name, range, formula, and primary citation
3. 96 vocabulary terms match `eta.py:AXIS_TERMS` exactly (zero drift)
4. All 9 adapter docs map unit outputs to semantic group inputs
5. Epsilon state contract specifies all 5 component types with shapes and lifecycle
6. Pipeline dependency DAG matches `L3Orchestrator.compute()` execution order
7. Psychometric alignment covers Russell/Osgood/GEMS/ITPRA/Berridge/Berlyne
8. Literature bibliography includes 40+ papers with per-dimension citation map
9. Migration guide documents v1.x→v2.x dimension mapping and code migration

**Phase 5 Status: ✅ COMPLETE (2026-02-13)** — 69 files written across 13 subdirectories (~10,350 lines). All quality gates passed.

### Phase 6: Documentation & Code Validation (Pre-Implementation Audit)

**391 documentation files + 94 code implementations must be 100% cross-validated before any code changes.** This is the firewall between documentation design (Phases 1-5) and code implementation (Phase 7). No code is written or modified in Phase 6 — only docs are read, compared, and corrected where necessary.

**Problem:** Phases 1-5 produced 391 documentation files across 4 architectural layers (C³, R³, H³, L³). Some docs describe v2 features not yet in code (R³ 128D, H³ v2 demand space). Some code attributes were intentionally deferred. Before implementing Phase 7, we must know the **exact delta** between docs and code — categorized as EXPECTED (fix in Phase 7) vs DOC-BUG (fix now).

**Scope:** 391 .md files (C³:159, R³:71, H³:73, L³:69, Beta:14, other:5) + 94 model implementations in `mi_beta/` + all infrastructure code (constants, contracts, registries).

#### 6.0 Discrepancy Categories

All findings from sub-phases 6A-6H are categorized into three types:

| Category | Meaning | Action |
|----------|---------|--------|
| **EXPECTED** | Code intentionally behind docs (designed in Phases 2-5, deferred to Phase 7) | Catalog in registry, fix in Phase 7 |
| **DOC-BUG** | Documentation error (wrong count, broken link, stale reference) | Fix immediately in Phase 6 |
| **CODE-BUG** | Code inconsistency unrelated to doc phases (e.g., duplicate constants) | Catalog in registry, fix in Phase 7 |

#### 6.1 Sub-Phase Execution Order

| Sub-Phase | Description | Scope | Depends On |
|:---------:|-------------|-------|:----------:|
| **6A** | Structural Inventory: every code file has a doc, vice versa | 94 models + all components | None |
| **6B** | C³ Model Attribute Validation: 94 models × 10 attributes | 940 individual checks | 6A |
| **6C** | C³ Cross-Reference Validation: models↔units↔mechanisms↔circuits↔pathways | ~50 aggregate checks | 6A |
| **6D** | R³ Architecture Consistency: features, groups, naming, dimension sums | `constants.py` vs `Docs/R³/` | 6A |
| **6E** | H³ Architecture Consistency: horizons, morphs, laws, MORPH_SCALE | `constants.py` vs `Docs/H³/` | 6A |
| **6F** | L³ Architecture Consistency: groups, vocabulary, adapters, orchestrator | `language/` vs `Docs/L³/` | 6A |
| **6G** | Cross-Layer Pipeline Validation: R³→H³→C³→L³ chain, version refs | all layers | 6B-6F |
| **6H** | Index & Link Integrity: 00-INDEX completeness, internal link resolution | all 391 files | 6A |
| **6I** | Discrepancy Registry Creation + Doc Fixes | synthesis of 6A-6H | All prior |

#### 6.2 Sub-Phase Details

**Sub-phase 6A — Structural Inventory (code ↔ doc existence)**

For every code component, verify a documentation counterpart exists (and vice versa):

| Code Component | Code Count | Doc Location | Doc Count | Expected Gap |
|---|:---:|---|:---:|---|
| `mi_beta/brain/units/*/models/*.py` | 94 | `Docs/C³/Models/{ID}/` | 96 dirs | 2 doc-only (CHPI, SSRI) |
| `mi_beta/brain/mechanisms/*.py` | 10 | `Docs/C³/Mechanisms/*.md` | 10 | None |
| `mi_beta/brain/pathways/p*.py` | 5 | `Docs/C³/Pathways/P*.md` | 5 | None |
| `mi_beta/brain/regions/*.py` | 3 | `Docs/C³/Regions/*.md` | 3 | None |
| `mi_beta/brain/neurochemicals/*.py` | 4 | `Docs/C³/Neurochemicals/*.md` | 4 | None |
| `mi_beta/ear/r3/*/` | 5 groups | `Docs/R³/Domains/*.md` | 9+ | 6 doc-only (v2 groups F-K) |
| `mi_beta/language/groups/*.py` | 8 | `Docs/L³/Groups/*/*.md` | 8 | None |
| `mi_beta/language/adapters/*_adapter.py` | 9 | `Docs/L³/Adapters/*-L3-ADAPTER.md` | 9 | None |
| `mi_beta/contracts/*.py` | 12 | `Docs/C³/Contracts/` + `Docs/L³/Contracts/` | 14 | overlap check |

Output: Inventory table in `Docs/Beta/VALIDATION-ARCHITECTURE.md`.

**Sub-phase 6B — C³ Model Attribute Validation (94 models × 10 attributes = 940 checks)**

For each of the 94 implemented models, extract class attributes from Python code and compare with the corresponding model document:

| # | Attribute | Code Source | Doc Source (Section) | Known Pattern |
|---|-----------|-------------|---------------------|---------------|
| 1 | `OUTPUT_DIM` | class constant | Sec 6: Output Space | gamma: code=10, doc=9 (EXPECTED) |
| 2 | `MECHANISM_NAMES` | class constant | Sec 5: H³ Temporal Demand | ASU all: code=("ASA",), doc=("BEP","ASA") (EXPECTED) |
| 3 | `FULL_NAME` | class constant | Sec 1: header subtitle | many mismatches (EXPECTED) |
| 4 | `NAME` | class constant | Model ID acronym | should match exactly |
| 5 | `UNIT` | class constant | directory prefix (e.g., "ASU") | must match exactly |
| 6 | `TIER` | class constant | tier in model ID (alpha/beta/gamma) | must match exactly |
| 7 | `h3_demand` | property `return ()` | Sec 5: demand tuple table | ALL empty in code (EXPECTED) |
| 8 | `dimension_names` | property tuple | Sec 6: dimension list | should match names+count |
| 9 | `brain_regions` | property tuple | Sec 8: MNI table | coords, abbreviations, BA |
| 10 | `LAYERS` | class LayerSpec tuple | Sec 6: E/M/P/F layer table | structure, dim ranges |

**Per-model validation procedure:**
```
For each of 94 models in mi_beta/brain/units/*/models/*.py:

1. IMPORT model class, extract: NAME, FULL_NAME, UNIT, TIER,
   OUTPUT_DIM, MECHANISM_NAMES, LAYERS, h3_demand, dimension_names, brain_regions

2. READ corresponding doc: Docs/C³/Models/{UNIT}-{tier}{n}-{ACRONYM}/{ACRONYM}.md
   Extract: Section 1 name, Section 5 mechanisms, Section 5 h3_demand,
   Section 6 OUTPUT_DIM + dims, Section 8 regions

3. COMPARE each of 10 attributes:
   → PASS: exact match
   → EXPECTED: known discrepancy (h3_demand empty, gamma OUTPUT_DIM, ASU mechanisms)
   → DOC-BUG: doc error (wrong count, broken reference)
   → CODE-BUG: unexpected code error

4. RECORD result in VALIDATION-C3-MODELS.md row
```

Output: `Docs/Beta/VALIDATION-C3-MODELS.md` — 94-row × 10-column validation matrix.

**Sub-phase 6C — C³ Cross-Reference Validation (~50 aggregate checks)**

Verify that aggregate documentation correctly references its member components:

| Check Category | Source A | Source B | Specific Checks |
|---|---|---|---|
| Unit model counts | `Docs/C³/Units/00-INDEX.md` | `Docs/C³/Models/` directory scan | Count per unit: SPU=9, STU=14, IMU=15, ASU=9, NDU=9, MPU=10, PCU=10, ARU=10, RPU=10 = 96 |
| Unit member lists | `Docs/C³/Units/{UNIT}.md` model table | `Docs/C³/Models/{UNIT}-*/` dirs | Each unit doc lists correct models |
| Mechanism users | `Docs/C³/Mechanisms/{MECH}.md` user table | Model `MECHANISM_NAMES` code | Models listed as users actually use that mechanism |
| Circuit membership | `Docs/C³/Circuits/{CIRCUIT}.md` | `constants.py` CIRCUIT_NAMES | Circuits doc references valid mechanisms and units |
| Pathway routing | `Docs/C³/Pathways/P{N}*.md` | `mi_beta/brain/pathways/p{n}*.py` | Source/target units, correlation values match |
| Matrices data | `Docs/C³/Matrices/R3-Usage.md` etc. | Individual model Section 4 data | Aggregate matrices sum correctly |
| Tier membership | `Docs/C³/Tiers/{TIER}.md` | Model TIER attributes | Models listed under correct tier |

**Critical known issue:** Code has TWO circuit constant tuples:
- `CIRCUIT_NAMES` (line 112 of constants.py): 6 entries including "imagery"
- `CIRCUITS` (line 210 of constants.py): 5 entries WITHOUT "imagery"
→ Flag as **CODE-BUG**: reconcile in Phase 7A.

**Known unit count discrepancy:** `Units/00-INDEX.md` may list PCU=9, RPU=9 (code counts), while `Models/` has PCU=10, RPU=10 (including doc-only CHPI, SSRI).
→ Flag as **DOC-BUG** if index doesn't acknowledge doc-only models; or **EXPECTED** if it correctly notes "9 code + 1 doc-only".

**Sub-phase 6D — R³ Architecture Consistency**

| # | Check | Source A (Code) | Source B (Docs) | Expected Result |
|---|-------|----------------|-----------------|-----------------|
| 1 | R3_DIM | `constants.py` = 49 | `R3-SPECTRAL-ARCHITECTURE.md` = 128 | EXPECTED: v1=49 code, v2=128 docs |
| 2 | Group A bounds | `R3_CONSONANCE = (0, 7)` | `Registry/DimensionCatalog.md` [0:7] | PASS |
| 3 | Group B bounds | `R3_ENERGY = (7, 12)` | `Registry/DimensionCatalog.md` [7:12] | PASS |
| 4 | Group C bounds | `R3_TIMBRE = (12, 21)` | `Registry/DimensionCatalog.md` [12:21] | PASS |
| 5 | Group D bounds | `R3_CHANGE = (21, 25)` | `Registry/DimensionCatalog.md` [21:25] | PASS |
| 6 | Group E bounds | `R3_INTERACTIONS = (25, 49)` | `Registry/DimensionCatalog.md` [25:49] | PASS |
| 7 | Feature names [0:49] | `dimension_map.py` 49 names | `Registry/DimensionCatalog.md` | Must match exactly |
| 8 | Groups F-K | Not in code | `Docs/R³/Domains/` | EXPECTED: v2-only, Phase 7C |
| 9 | Dimension sum v1 | 7+5+9+4+24 = 49 ✓ | Doc A+B+C+D+E sums | PASS |
| 10 | Dimension sum v2 | N/A | 7+5+9+4+24+16+10+12+7+20+14 = 128 | Verify doc-internal |
| 11 | Per-unit mappings | Model Section 4 r3 indices | `Mappings/{UNIT}-R3-MAP.md` | Cross-check |
| 12 | Known naming discrepancies | `dimension_map.py` names | Doc semantic labels | 6 known (see MEMORY.md) |

**Known R³ naming mismatches** (identified in Phase 1, deferred to Phase 7):
- [5] periodicity → roughness_total
- [7] amplitude → velocity_A
- [8] loudness → velocity_D
- [10] spectral_flux → onset_strength
- [14] tonalness → brightness_kuttruff
- [21] spectral_change → spectral_flux

**Sub-phase 6E — H³ Architecture Consistency**

| # | Check | Source A (Code) | Source B (Docs) | Expected Result |
|---|-------|----------------|-----------------|-----------------|
| 1 | N_HORIZONS | `constants.py` = 32 | `Registry/HorizonCatalog.md` rows | 32 entries |
| 2 | HORIZON_MS | `constants.py` 32-tuple | `HorizonCatalog.md` ms column | EXACT value match |
| 3 | N_MORPHS | `constants.py` = 24 | `Registry/MorphCatalog.md` rows | 24 entries |
| 4 | MORPH_NAMES | `constants.py` 24-tuple | `MorphCatalog.md` name column | EXACT name match |
| 5 | N_LAWS | `constants.py` = 3 | `Registry/LawCatalog.md` rows | 3 entries |
| 6 | LAW_NAMES | `constants.py` 3-tuple | `LawCatalog.md` name column | EXACT name match |
| 7 | H3_TOTAL_DIM | `constants.py` = 2304 | `H3-TEMPORAL-ARCHITECTURE.md` | code=2304, doc v2=294,912 (EXPECTED) |
| 8 | MORPH_SCALE | `constants.py` 24-tuple (gain,bias) | `Morphology/MorphScaling.md` | 24 pairs match |
| 9 | ATTENTION_DECAY | `constants.py` = 3.0 | `Contracts/AttentionKernel.md` | PASS |
| 10 | HORIZON_FRAMES | computed from MS | `HorizonCatalog.md` frame column | computed match |
| 11 | h3_flat_index | `constants.py` h*72+m*3+l | `Pipeline/ExecutionModel.md` | formula match |
| 12 | Per-unit demands | Model h3_demand (ALL empty) | `Demand/{UNIT}-H3-DEMAND.md` | EXPECTED: empty code |

**Sub-phase 6F — L³ Architecture Consistency**

| # | Check | Source A (Code) | Source B (Docs) | Expected Result |
|---|-------|----------------|-----------------|-----------------|
| 1 | Group count | `L3Orchestrator` 8 groups | `Registry/GroupMap.md` 8 rows | PASS |
| 2 | Group order | OrderedDict keys: α,β,γ,δ,ε,ζ,η,θ | `Pipeline/ExecutionModel.md` | PASS |
| 3 | Per-group OUTPUT_DIM | Each group class constant | `GroupMap.md` dim column | Must match |
| 4 | Total dims | sum(OUTPUT_DIM) = 104 | Docs: 6+14+13+12+19+12+12+16=104 | PASS |
| 5 | AXIS_NAMES | `eta.py` 12-tuple | `Vocabulary/AxisDefinitions.md` 12 axes | EXACT match |
| 6 | AXIS_TERMS | `eta.py` 12×8 dict = 96 terms | `Vocabulary/TermCatalog.md` 96 entries | ZERO drift |
| 7 | N_GRADATIONS | `eta.py` = 64 | `Vocabulary/GradationSystem.md` | PASS |
| 8 | N_BANDS | `eta.py` = 8 | `Vocabulary/GradationSystem.md` | PASS |
| 9 | POLARITY_AXES | `zeta.py` 12 dicts (name/neg/pos) | `Vocabulary/AxisDefinitions.md` | EXACT match |
| 10 | Epsilon state | `epsilon.py` all state tensors | `Contracts/EpsilonStateContract.md` | 5 components match |
| 11 | Epsilon hyperparams | ALPHA_SHORT/MEDIUM/LONG, N_STATES, BUFFER_SIZE | `Groups/Independent/Epsilon.md` | values match |
| 12 | Adapters (9) | All return `{"tensor": unit_output.tensor}` | `Adapters/` docs status="stub" | PASS (all stubs) |
| 13 | BaseSemanticGroup | ABC attrs: LEVEL, GROUP_NAME, DISPLAY_NAME, OUTPUT_DIM | `Contracts/BaseSemanticGroup.md` | attr list match |
| 14 | Orchestrator compute() | Phase 1→1b→2a→2b→2c | `Pipeline/DependencyDAG.md` | order match |
| 15 | Orchestrator reset() | resets epsilon only | `Pipeline/StateManagement.md` | PASS |

**Sub-phase 6G — Cross-Layer Pipeline Validation**

End-to-end pipeline consistency across all 4 layers:

| # | Check | Layers | Description |
|---|-------|--------|-------------|
| 1 | R³→C³ indices | R³, C³ | Model Section 4 r3 indices within [0, R3_DIM-1] per version |
| 2 | H³ demand validity | H³, C³ | Model Section 5 tuples: r3_idx<R3_DIM, horizon<32, morph<24, law<3 |
| 3 | C³→L³ dims | C³, L³ | L³ adapter docs reference correct unit output dimensionality |
| 4 | Pipeline chain | All | Audio→Cochlea→R³(49/128D)→H³(2304D)→Brain(variable)→L³(104D)→MI-space |
| 5 | Version alignment | All | R³ v2.0.0, H³ v2.0.0, L³ v2.1.0 — referenced consistently |
| 6 | UNIT_EXECUTION_ORDER | C³ code | `constants.py` matches `Docs/C³/Units/00-INDEX.md` order |
| 7 | MODEL_TIERS | C³ code | `constants.py` ("alpha","beta","gamma") matches `Docs/C³/Tiers/` |
| 8 | Pathway routing | C³ code | 5 pathways match `Docs/C³/Pathways/` source→target |

**Sub-phase 6H — Index & Link Integrity**

| # | Check | Scope | Description |
|---|-------|-------|-------------|
| 1 | 00-INDEX completeness | 56 index files | Every 00-INDEX.md lists ALL files in its directory (no missing, no extra) |
| 2 | C³ root index gap | `Docs/C³/` | Has `C3-ARCHITECTURE.md` but no `00-INDEX.md` — decide: add or document as intentional |
| 3 | Internal links | All .md files | All relative `[text](path)` links resolve to existing files |
| 4 | Orphaned files | All dirs | No files unreachable from any 00-INDEX or architecture doc |
| 5 | File naming consistency | All | Model dirs follow `{UNIT}-{tier}{n}-{ACRONYM}` pattern |
| 6 | upgrade_beta/ index | `Docs/R³/upgrade_beta/` | Working docs — intentionally no 00-INDEX (verify) |
| 7 | Beta/Prompts/ index | `Docs/Beta/Prompts/` | Execution metadata — intentionally no 00-INDEX (verify) |

**Sub-phase 6I — Discrepancy Registry Creation + Doc Fixes**

Create `Docs/Beta/DISCREPANCY-REGISTRY.md` with three sections:

**EXPECTED Discrepancies** (~15 categories, fix in Phase 7):

| ID | Category | Scope | Description | Fix Phase |
|---|---|---|---|---|
| E01 | h3_demand empty | 94 models | All models return `()` in code, docs have populated tuples | 7B |
| E02 | gamma OUTPUT_DIM | ~26 models | Code=10, doc=9 for all gamma-tier models | 7B |
| E03 | ASU MECHANISM_NAMES | 9 models | Code=("ASA",), doc=("BEP","ASA") | 7B |
| E04 | FULL_NAME mismatches | ~30+ models | Code FULL_NAME ≠ doc Section 1 header | 7B |
| E05 | R3_DIM 49→128 | constants.py | Code=49, docs=128 (v2 expansion) | 7C |
| E06 | R³ groups F-K | 6 groups | Exist in docs, not in code | 7C |
| E07 | H3_TOTAL_DIM | constants.py | Code=2304, doc v2=294,912 | 7D |
| E08 | Model files missing | 2 models | CHPI.py, SSRI.py doc-only | 7A |
| E09 | L³ adapter stubs | 9 adapters | All return raw tensor, docs describe real mapping | 7E |
| E10 | R³ naming mismatches | 6 features | Code names ≠ doc semantic labels (see Phase 1) | 7C |
| E11 | CIRCUITS vs CIRCUIT_NAMES | constants.py | 5 vs 6 entries (missing "imagery") | 7A |
| E12 | dimension_names drift | ~20 models | Minor code↔doc name differences | 7B |

**DOC-BUG Items** (fix immediately in Phase 6):
- Found during 6A-6H execution — listed per sub-phase with fix description.

**CODE-BUG Items** (fix in Phase 7):
- CIRCUITS/CIRCUIT_NAMES inconsistency (E11)
- Any unexpected code errors found during validation

#### 6.3 Dependency Graph

```
6A (Structural Inventory)
 ├──→ 6B (C³ Model Attributes) ──→ 6C (C³ Cross-Refs) ─┐
 ├──→ 6D (R³ Consistency) ──────────────────────────────┤
 ├──→ 6E (H³ Consistency) ──────────────────────────────┤→ 6G (Pipeline) → 6H (Links) → 6I (Registry+Fixes)
 └──→ 6F (L³ Consistency) ──────────────────────────────┘
```

6B, 6D, 6E, 6F can run in parallel after 6A. Then 6C and 6G after their inputs. Then 6H and 6I.

#### 6.4 Deliverables

| # | File | Purpose | Est. Lines |
|---|------|---------|:----------:|
| 1 | `Docs/Beta/VALIDATION-C3-MODELS.md` | 94-model × 10 attribute comparison matrix | ~400 |
| 2 | `Docs/Beta/VALIDATION-ARCHITECTURE.md` | R³/H³/L³/cross-layer validation results | ~300 |
| 3 | `Docs/Beta/VALIDATION-INDEXES.md` | 00-INDEX completeness audit (56 indexes) | ~150 |
| 4 | `Docs/Beta/DISCREPANCY-REGISTRY.md` | All discrepancies: EXPECTED + DOC-BUG + CODE-BUG | ~200 |
| 5 | Various doc fixes | DOC-BUG corrections found during 6A-6H | variable |

#### 6.5 Quality Gates

1. Structural inventory covers all 94 code models + 96 doc models + all mechanisms/pathways/regions/neurochemicals
2. Every C³ model attribute checked: 94 × 10 = 940 checks, each classified as PASS / EXPECTED / DOC-BUG / CODE-BUG
3. All C³ aggregate cross-references verified (Units, Mechanisms, Circuits, Pathways, Tiers, Matrices)
4. R³ feature names [0:49] and group boundaries [A-E] verified EXACT against `constants.py` and `dimension_map.py`
5. H³ HORIZON_MS (32 values), MORPH_NAMES (24), LAW_NAMES (3), MORPH_SCALE (24×2) verified EXACT against `constants.py`
6. L³ vocabulary: 96 terms verified against `eta.py` AXIS_TERMS — **zero drift** (character-for-character match)
7. Cross-layer pipeline chain validated end-to-end (R³→H³→C³→L³ index ranges and version references)
8. All 56 `00-INDEX.md` files verified for directory completeness (no missing files, no phantom entries)
9. `DISCREPANCY-REGISTRY.md` created with every discrepancy categorized — no uncategorized items
10. All DOC-BUG items fixed in-place — **zero remaining doc errors** before Phase 7 begins

**Phase 6 completes when:** DISCREPANCY-REGISTRY.md is finalized and all DOC-BUG items are resolved. The registry becomes the exact specification for Phase 7 code changes.

---

### Phase 7: mi_beta Implementation (Code Update)

Only after Phase 6 validation confirms 100% documentation consistency. The `DISCREPANCY-REGISTRY.md` from Phase 6 defines the **exact delta** between docs and code. Phase 7 systematically closes every EXPECTED discrepancy and CODE-BUG.

**Scope:** 94 model files updated, 2 new model files created, R³ expanded 49D→128D, H³ demand range updated, 9 L³ adapter stubs replaced, constants reconciled, full test suite created.

#### 7.0 Architecture Overview

```
Phase 7 transforms mi_beta code to match v2 documentation:

  R³:  49D → 128D (6 new spectral groups F-K)
  H³:  r3_idx range 0-48 → 0-127 (demand tuples for expanded features)
  C³:  94 models → 96 models (CHPI + SSRI), all attributes synced
  L³:  9 stub adapters → 9 real semantic mappers

  Constants: R3_DIM=49→128, CIRCUITS 5→6, group boundaries expanded
  Tests: ~10 new test files covering all layers
```

#### 7.1 Sub-Phase Execution Order

| Sub-Phase | Description | Files Changed | Est. Scope | Depends On |
|:---------:|-------------|:------------:|:----------:|:----------:|
| **7A** | Foundation: CHPI.py + SSRI.py + CIRCUITS fix + registries | ~6 | ~800 lines | None |
| **7B** | C³ Model Sync: 94 models × h3_demand + attribute fixes | 94 | ~4,700 lines | 7A |
| **7C** | R³ v2 Expansion: 49D→128D, new groups F-K, registry | ~15 | ~3,000 lines | 7A |
| **7D** | H³ Code Updates: demand aggregation for R³ v2 | ~5 | ~500 lines | 7C |
| **7E** | L³ Adapter Implementation: 9 stubs → real semantic mapping | 9 | ~900 lines | 7B |
| **7F** | Cross-Unit Updates: pathways, regions, neurochemicals | ~10 | ~500 lines | 7B |
| **7G** | Test Suite: unit + integration + benchmark tests | ~10 | ~2,000 lines | 7A-7F |
| **7H** | Validation Run: pytest + full pipeline + output verification | — | — | 7G |

#### 7.2 Sub-Phase Details

**Sub-phase 7A — Foundation (6 files, ~800 lines)**

| # | Action | File | Description |
|---|--------|------|-------------|
| 1 | CREATE | `mi_beta/brain/units/pcu/models/chpi.py` | PCU-β4-CHPI from `Docs/C³/Models/PCU-β4-CHPI/CHPI.md` spec |
| 2 | CREATE | `mi_beta/brain/units/rpu/models/ssri.py` | RPU-β4-SSRI from `Docs/C³/Models/RPU-β4-SSRI/SSRI.md` spec |
| 3 | UPDATE | `mi_beta/brain/units/pcu/__init__.py` | Register CHPI model in unit |
| 4 | UPDATE | `mi_beta/brain/units/rpu/__init__.py` | Register SSRI model in unit |
| 5 | FIX | `mi_beta/core/constants.py` | Reconcile `CIRCUITS` (5) with `CIRCUIT_NAMES` (6) — add "imagery" to `CIRCUITS` |
| 6 | UPDATE | `mi_beta/core/constants.py` | Update model count comments if any |

Each new model file follows the exact `BaseModel` pattern:
```python
class CHPI(BaseModel):
    NAME = "CHPI"
    FULL_NAME = "Cross-Modal Harmonic Predictive Integration"
    UNIT = "PCU"
    TIER = "beta"
    OUTPUT_DIM = ...  # from doc Section 6
    MECHANISM_NAMES = ("PPC", "TPC", "MEM")  # from doc Section 5
    LAYERS = (LayerSpec("E",...), LayerSpec("M",...), LayerSpec("P",...), LayerSpec("F",...))
    # h3_demand, dimension_names, brain_regions from doc Sections 5, 6, 8
```

Quality gate: Both models instantiate, produce correct OUTPUT_DIM, pass BaseModel contract validation.

**Sub-phase 7B — C³ Model Attribute Sync (94 models, 9 batches)**

For each model, apply fixes specified in DISCREPANCY-REGISTRY.md:

| Priority | Attribute | Scope | Change | Registry ID |
|:--------:|-----------|:-----:|--------|:-----------:|
| 1 | `h3_demand` | 94 models | Populate from doc Section 5 (all currently empty) | E01 |
| 2 | `OUTPUT_DIM` | ~26 gamma | Fix 10→9 where doc says 9 | E02 |
| 3 | `MECHANISM_NAMES` | 9 ASU | Fix ("ASA",)→("BEP","ASA") | E03 |
| 4 | `FULL_NAME` | ~30+ | Sync with doc Section 1 header | E04 |
| 5 | `dimension_names` | ~20 | Sync with doc Section 6 | E12 |
| 6 | `brain_regions` | verify | Verify MNI coords match doc Section 8 | — |
| 7 | `LAYERS` | verify | Verify layer spec matches doc Section 6 | — |

**Processing order (same batches as Phase 1):**

| Batch | Unit | Models | Key Changes |
|:-----:|------|:------:|-------------|
| 1 | SPU | 9 | h3_demand population, minor FULL_NAME sync |
| 2 | STU | 14 | h3_demand population, minor FULL_NAME sync |
| 3 | IMU | 15 | h3_demand population, minor FULL_NAME sync |
| 4 | ASU | 9 | h3_demand + **MECHANISM_NAMES fix** ("ASA"→"BEP","ASA") + **gamma OUTPUT_DIM fix** (10→9) |
| 5 | NDU | 9 | h3_demand population, minor attribute sync |
| 6 | MPU | 10 | h3_demand population, minor attribute sync |
| 7 | PCU | 9+1 | h3_demand + **new CHPI model integration** (from 7A) |
| 8 | ARU | 10 | h3_demand population, minor attribute sync |
| 9 | RPU | 9+1 | h3_demand + **new SSRI model integration** (from 7A) |

**Per-batch workflow:**
```
For each model in batch:
  1. READ model doc Section 5 → extract h3_demand tuples
  2. READ model doc Section 6 → verify OUTPUT_DIM, dimension_names
  3. READ model doc Section 1 → verify FULL_NAME
  4. EDIT model .py file → populate h3_demand property
  5. EDIT model .py file → fix any EXPECTED discrepancies from registry
  6. VERIFY: model instantiates, OUTPUT_DIM matches, h3_demand is non-empty
```

Quality gate: All 94+2 models have non-empty h3_demand. All EXPECTED discrepancies E01-E04, E12 resolved. `DISCREPANCY-REGISTRY.md` E-column items checked off.

**Sub-phase 7C — R³ v2 Expansion (49D → 128D, ~15 files, ~3,000 lines)**

Step-by-step implementation of the R³ v2 architecture designed in Phase 3:

| Step | Action | File(s) | Description |
|:----:|--------|---------|-------------|
| 1 | CREATE | `mi_beta/ear/r3/tonal/__init__.py` | New tonal subdirectory |
| 2 | CREATE | `mi_beta/ear/r3/tonal/pitch.py` | **Group F: Pitch & Chroma (16D)** [49:65] |
| 3 | CREATE | `mi_beta/ear/r3/tonal/harmony.py` | **Group H: Harmony & Tonality (12D)** [75:87] |
| 4 | CREATE | `mi_beta/ear/r3/temporal/__init__.py` | New temporal subdirectory |
| 5 | CREATE | `mi_beta/ear/r3/temporal/rhythm.py` | **Group G: Rhythm & Groove (10D)** [65:75] |
| 6 | CREATE | `mi_beta/ear/r3/information/__init__.py` | New information subdirectory |
| 7 | CREATE | `mi_beta/ear/r3/information/surprise.py` | **Group I: Information & Surprise (7D)** [87:94] |
| 8 | CREATE | `mi_beta/ear/r3/dsp/timbre_extended.py` | **Group J: Timbre Extended (20D)** [94:114] |
| 9 | CREATE | `mi_beta/ear/r3/psychoacoustic/modulation.py` | **Group K: Modulation & Psychoacoustic (14D)** [114:128] |
| 10 | UPDATE | `mi_beta/core/constants.py` | R3_DIM: 49→128; add R3_PITCH=(49,65), R3_RHYTHM=(65,75), R3_HARMONY=(75,87), R3_INFORMATION=(87,94), R3_TIMBRE_EXT=(94,114), R3_MODULATION=(114,128) |
| 11 | UPDATE | `mi_beta/core/dimension_map.py` | Extend `_R3_FEATURE_NAMES` from 49→128 entries |
| 12 | UPDATE | `mi_beta/ear/r3/__init__.py` | R3FeatureRegistry: discover new subdirectories |
| 13 | VERIFY | All existing code | Indices 0-48 UNCHANGED (backward compatible) |
| 14 | UPDATE | Model r3_indices | Update 96 model docs Section 4 → code r3 references |
| 15 | BENCH | Performance | Per-frame cost at 128D vs 49D (target: <2× increase) |

Each new group follows `BaseSpectralGroup` contract:
```python
class PitchGroup(BaseSpectralGroup):
    GROUP_NAME = "pitch"
    DISPLAY_NAME = "F: Pitch & Chroma"
    OUTPUT_DIM = 16
    INDEX_RANGE = (49, 65)

    def compute(self, mel_spectrogram: Tensor) -> Tensor:
        # 16D pitch features from mel: F0, salience, chroma[12], vibrato, inharmonicity
        ...
```

Quality gate: R3_DIM=128. All group boundaries contiguous [0:7:12:21:25:49:65:75:87:94:114:128]. Existing tests still pass with indices 0-48.

**Sub-phase 7D — H³ Code Updates (~5 files, ~500 lines)**

| Step | Action | File | Description |
|:----:|--------|------|-------------|
| 1 | UPDATE | `mi_beta/core/constants.py` | H3_TOTAL_DIM stays 2304 (structure unchanged: 32×24×3) |
| 2 | UPDATE | `mi_beta/core/demand_aggregator.py` | Accept r3_idx in [0, 127] (was [0, 48]) |
| 3 | UPDATE | `mi_beta/contracts/demand_spec.py` | Validate r3_idx < R3_DIM (now 128) |
| 4 | VERIFY | `mi_beta/ear/h3/` | H³ extraction handles expanded R³ features |
| 5 | TEST | Demand aggregation | New R³ v2 demands (r3_idx ≥ 49) aggregate correctly |

Quality gate: H³ processes demands for all 128 R³ features. Existing demands (r3_idx 0-48) unchanged.

**Sub-phase 7E — L³ Adapter Implementation (9 files, ~900 lines)**

Replace each stub adapter with real semantic mapping logic:

| Adapter | Current (stub) | Target Implementation | Key Mappings |
|---------|---------------|----------------------|-------------|
| `spu_adapter.py` | `{"tensor": tensor}` | Feature extraction + semantic projection | consonance→beauty, timbre→complexity, pitch→novelty |
| `stu_adapter.py` | `{"tensor": tensor}` | Rhythm/timing semantic extraction | beat→groove, tempo→arousal, sync→engagement |
| `imu_adapter.py` | `{"tensor": tensor}` | Memory semantic extraction | familiarity→stability, recall→imagination |
| `asu_adapter.py` | `{"tensor": tensor}` | Salience semantic extraction | novelty→surprise, attention→engagement |
| `ndu_adapter.py` | `{"tensor": tensor}` | Novelty semantic extraction | deviation→surprise, PE→tension, entropy→complexity |
| `mpu_adapter.py` | `{"tensor": tensor}` | Motor semantic extraction | groove→groove, movement→motion |
| `pcu_adapter.py` | `{"tensor": tensor}` | Prediction semantic extraction | prediction_error→surprise, certainty→stability |
| `aru_adapter.py` | `{"tensor": tensor}` | Affect semantic extraction | pleasure→valence, tension→tension, chills→beauty |
| `rpu_adapter.py` | `{"tensor": tensor}` | Reward semantic extraction | DA→wanting, opioid→liking, reward_PE→reward_pe |

Each adapter follows the mapping spec from `Docs/L³/Adapters/{UNIT}-L3-ADAPTER.md`.

Quality gate: All 9 adapters produce non-trivial output (not raw tensor passthrough). L³ orchestrator produces meaningful 104D output.

**Sub-phase 7F — Cross-Unit Updates (~10 files, ~500 lines)**

| Component | Files | Changes |
|-----------|:-----:|---------|
| Pathways | 5 | Weight refinement from revised Phase 1 evidence |
| Regions | 3 | MNI coordinate updates from verified Section 8 data |
| Neurochemicals | 4 | Coefficient refinement (BETA_NACC, BETA_CAUDATE, etc.) |

Quality gate: All pathways route correctly with updated weights. Region registry matches doc Section 8 data.

**Sub-phase 7G — Test Suite (~10 files, ~2,000 lines)**

| # | Test File | Scope | Key Assertions |
|---|-----------|-------|----------------|
| 1 | `tests/test_model_instantiation.py` | 96 models | Each loads, OUTPUT_DIM matches, h3_demand non-empty |
| 2 | `tests/test_model_attributes.py` | 96 models | NAME, UNIT, TIER, FULL_NAME, MECHANISM_NAMES match docs |
| 3 | `tests/test_r3_output.py` | R³ | 128D output, group boundaries contiguous, feature names |
| 4 | `tests/test_r3_backward_compat.py` | R³ | Indices 0-48 produce same results as pre-expansion |
| 5 | `tests/test_h3_extraction.py` | H³ | Demand aggregation, r3_idx 0-127, horizon/morph/law validity |
| 6 | `tests/test_l3_output.py` | L³ | 104D output, group ordering, 96 vocabulary terms match |
| 7 | `tests/test_l3_adapters.py` | L³ | 9 adapters produce non-trivial semantic mappings |
| 8 | `tests/test_pathways.py` | C³ | 5 pathways route source→target with correct dims |
| 9 | `tests/test_pipeline.py` | E2E | Audio→R³→H³→Brain→L³→MI-space full pipeline |
| 10 | `tests/test_benchmark.py` | Perf | Frame processing time < 2× baseline at 128D |

Quality gate: All tests pass. No regressions from pre-Phase-7 baseline.

**Sub-phase 7H — Validation Run (final verification)**

| Step | Command | Expected |
|:----:|---------|----------|
| 1 | `pytest tests/ -v` | 100% pass, 0 failures |
| 2 | `python -m mi_beta` | Runs without errors |
| 3 | Output dimension check | R³=128D, H³=sparse, Brain=variable, L³=104D |
| 4 | Performance check | Frame rate ≥ 86 Hz (half of 172 Hz real-time) |
| 5 | DISCREPANCY-REGISTRY check | All EXPECTED + CODE-BUG items marked RESOLVED |

Quality gate: Full pipeline runs end-to-end. All tests pass. All discrepancies resolved.

#### 7.3 Dependency Graph

```
7A (Foundation) ──→ 7B (Model Sync) ──→ 7E (L³ Adapters) ──┐
                │                   └──→ 7F (Cross-Unit) ───┤
                └──→ 7C (R³ v2) ──→ 7D (H³ Update) ────────┤→ 7G (Tests) → 7H (Validation)
```

7B and 7C can run in parallel after 7A. 7E+7F depend on 7B. 7D depends on 7C. 7G depends on all.

#### 7.4 Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| R³ 128D breaks existing model r3 references | HIGH | Backward compatibility: indices 0-48 unchanged |
| gamma OUTPUT_DIM change (10→9) breaks downstream | MEDIUM | Update all consumers (L³ groups, mechanisms) simultaneously |
| h3_demand population causes import errors | LOW | Validate each model individually in batch order |
| L³ adapter implementation changes semantic output | MEDIUM | Snapshot pre-change L³ output, compare post-change |
| Performance regression at 128D | MEDIUM | Benchmark per step, target <2× increase |

**Rollback strategy:** Git branch per sub-phase. If 7C (R³ expansion) fails, revert to 7B state. Each sub-phase is independently testable.

#### 7.5 Quality Gates (9)

1. 96 model files exist (94 updated + CHPI + SSRI), all instantiate correctly
2. All 94+2 `h3_demand` properties populated from doc Section 5 (non-empty)
3. All `OUTPUT_DIM` / `MECHANISM_NAMES` / `FULL_NAME` match docs exactly
4. `R3_DIM=128` with indices 0-48 backward-compatible (existing tests pass)
5. All 6 new R³ groups (F-K) produce correct-dimension output from mel spectrogram
6. L³ 9 adapters produce meaningful semantic mappings (not raw tensor passthrough)
7. `CIRCUITS` constant reconciled with `CIRCUIT_NAMES` (both 6 entries with "imagery")
8. `pytest tests/ -v` — 100% pass, 0 failures, 0 errors
9. `python -m mi_beta` — end-to-end pipeline runs without errors

**Phase 7 completes when:** All tests pass, full pipeline runs, and every item in DISCREPANCY-REGISTRY.md is marked RESOLVED.

## Critical File Paths

| File | Role |
|------|------|
| `Docs/C³/Models/00-INDEX.md` | Master model index (96 models) |
| `Docs/C³/C3-ARCHITECTURE.md` | Top-level C³ architecture overview |
| `Docs/C³/Units/00-INDEX.md` | Unit registry and execution order |
| `Docs/C³/Mechanisms/00-INDEX.md` | Mechanism registry and circuit assignments |
| `Docs/C³/Pathways/00-INDEX.md` | Cross-unit pathway registry |
| `Docs/Beta/PROGRESS.md` | Progress tracker (checkboxes) |
| `Docs/Beta/Beta_upgrade.md` | This plan (in-project copy) |
| `Docs/R³/R3-GAP-LOG-*.md` | Per-unit R³ gap logs (7 files) |
| `Literature/catalog.json` | Paper index (504 C³ + 59 R³) |
| `Literature/c3/summaries/` | Paper summaries (492 files) |
| `Literature/c3/extractions/` | Structured extractions (12 JSON) |
| `Literature/r3/` | R³ literature (121 markdown) |
| `mi_beta/core/constants.py` | Single source of truth for all constants |
| `mi_beta/core/dimension_map.py` | R³ feature names and MI-space mapping |
| `mi_beta/contracts/base_model.py` | Model contract (what every model must implement) |
| `mi_beta/brain/` | Code architecture that C³ docs mirror |
| `Docs/L³/00-INDEX.md` | L³ master index (68 files, 13 subdirectories) |
| `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` | L³ definitive architecture document |
| `Docs/L³/Registry/DimensionCatalog.md` | All 104 L³ dimensions with formulas |
| `Docs/L³/Contracts/L3Orchestrator.md` | L³ execution pipeline contract |
| `Docs/L³/Vocabulary/TermCatalog.md` | 96 vocabulary terms (12 axes × 8 bands) |
| `Docs/L³/Adapters/00-INDEX.md` | Per-unit semantic adapter registry |
| `mi_beta/contracts/base_semantic_group.py` | L³ group ABC contract |
| `mi_beta/language/groups/__init__.py` | L3Orchestrator implementation |
| `mi_beta/language/adapters/` | Per-unit semantic adapters (9 stubs) |
| **Phase 6 Validation Deliverables** | |
| `Docs/Beta/VALIDATION-C3-MODELS.md` | 94-model × 10 attribute comparison matrix |
| `Docs/Beta/VALIDATION-ARCHITECTURE.md` | R³/H³/L³/cross-layer validation results |
| `Docs/Beta/VALIDATION-INDEXES.md` | 00-INDEX completeness audit (56 indexes) |
| `Docs/Beta/DISCREPANCY-REGISTRY.md` | All discrepancies: EXPECTED / DOC-BUG / CODE-BUG |
| **Phase 7 Implementation Targets** | |
| `mi_beta/brain/units/pcu/models/chpi.py` | New model: PCU-β4-CHPI (Phase 7A) |
| `mi_beta/brain/units/rpu/models/ssri.py` | New model: RPU-β4-SSRI (Phase 7A) |
| `mi_beta/ear/r3/tonal/pitch.py` | R³ v2 Group F: Pitch & Chroma (Phase 7C) |
| `mi_beta/ear/r3/temporal/rhythm.py` | R³ v2 Group G: Rhythm & Groove (Phase 7C) |
| `mi_beta/ear/r3/tonal/harmony.py` | R³ v2 Group H: Harmony & Tonality (Phase 7C) |
| `mi_beta/ear/r3/information/surprise.py` | R³ v2 Group I: Info & Surprise (Phase 7C) |
| `mi_beta/ear/r3/dsp/timbre_extended.py` | R³ v2 Group J: Timbre Extended (Phase 7C) |
| `mi_beta/ear/r3/psychoacoustic/modulation.py` | R³ v2 Group K: Modulation (Phase 7C) |
| `tests/` | Phase 7G test suite (unit + integration + benchmark) |

## Resume Protocol for AI Agents

When resuming this work:

```
1. READ Docs/Beta/PROGRESS.md
   → Check phase status

2. READ Docs/Beta/Beta_upgrade.md
   → Find current phase and next steps

3. CHECK which phase we're in:
   → Phase 1: C³ Model Revision        → ✅ COMPLETE (96/96)
   → Phase 2: C³ Documentation Arch    → Check if Docs/C³/ subdirs exist
   → Phase 3: R³ Architecture          → Check if Docs/R³/ architecture docs exist
   → Phase 4: H³ Architecture          → Check if Docs/H³/ architecture docs exist
   → Phase 5: L³ Architecture          → Check if Docs/L³/ is complete
   → Phase 6: mi_beta Code Update      → Only after all docs phases done

4. For Phase 2: Read mi_beta/brain/ code + model docs → create aggregate docs
   For Phase 3+: Follow phase-specific instructions above

5. COMMIT after completing each Phase 2 component (e.g., Units/, Mechanisms/)
   with message: "Add C³ {component} documentation — Phase 2"
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

## Parallel Chat Assignment (Phase 1 Remaining — 73 models)

**Status:** BATCH 1 (SPU, 9 models) and BATCH 2 (STU, 14 models) are COMPLETE (23/96).
**Remaining:** 73 models across 7 batches, assigned to 7 parallel chats.

| Chat | Batch | Unit | Models | Range | Progress File |
|------|-------|------|--------|-------|---------------|
| Chat 1 | BATCH 3 | IMU (Integrative Memory) | 15 | #24-#38 | `Docs/Beta/PROGRESS-BATCH3-IMU.md` |
| Chat 2 | BATCH 4 | ASU (Auditory Salience) | 9 | #39-#47 | `Docs/Beta/PROGRESS-BATCH4-ASU.md` |
| Chat 3 | BATCH 5 | NDU (Novelty Detection) | 9 | #48-#56 | `Docs/Beta/PROGRESS-BATCH5-NDU.md` |
| Chat 4 | BATCH 6 | MPU (Motor Planning) | 10 | #57-#66 | `Docs/Beta/PROGRESS-BATCH6-MPU.md` |
| Chat 5 | BATCH 7 | PCU (Predictive Coding) | 10 | #67-#76 | `Docs/Beta/PROGRESS-BATCH7-PCU.md` |
| Chat 6 | BATCH 8 | ARU (Affective Resonance) | 10 | #77-#86 | `Docs/Beta/PROGRESS-BATCH8-ARU.md` |
| Chat 7 | BATCH 9 | RPU (Reward Processing) | 10 | #87-#96 | `Docs/Beta/PROGRESS-BATCH9-RPU.md` |

### Parallel Execution Rules

1. **Each chat ONLY edits files in its assigned unit's model folders** (e.g., Chat 1 only touches `Docs/C³/Models/IMU-*/`)
2. **Each chat updates ONLY its own progress file** (e.g., `PROGRESS-BATCH3-IMU.md`)
3. **Do NOT edit the master `PROGRESS.md`** — will be updated centrally after all chats complete
4. **Write R³ gaps to unit-specific gap files**: `Docs/R³/R3-GAP-LOG-{UNIT}.md` (e.g., `R3-GAP-LOG-IMU.md`)
5. **Do NOT git commit** — commits will be done centrally after merge
6. **`Literature/` and `mi_beta/` are READ-ONLY** — read for research, never modify
7. **Follow the per-model workflow** (STEP 1-5) from the "Phase 1: C³ Model Revision" section above for EVERY model

### Chat Prompt Template

Each chat receives this prompt (replace N with chat number):

```
Docs/Beta/Beta_upgrade.md dosyasını oku. "Parallel Chat Assignment" tablosuna bak.
Sen Chat {N}'sin. Tablodaki batch'ini, modellerini ve progress dosyanı bul.

Görevin: Per-model workflow'un 5 adımını (STEP 1-5) batch'indeki HER model için sırayla uygula.

Kurallar:
- Sadece kendi unit klasöründeki model dosyalarını düzenle
- Her model bittikten sonra kendi progress dosyanı güncelle (PROGRESS-BATCH{B}-{UNIT}.md)
- R³ gap'leri Docs/R³/R3-GAP-LOG-{UNIT}.md dosyasına yaz
- Master PROGRESS.md'yi güncelleme
- Git commit yapma
- Literature/ ve mi_beta/ sadece oku, düzenleme
```

## Verification

After full completion:
- [x] 96 model docs (48 Core + 48 Experimental) all with verified evidence ✅ Phase 1
- [x] Every model doc Section 3 has verified effect sizes matching Literature ✅ Phase 1
- [x] Every model doc Section 4 maps to valid R³ indices (current or expanded) ✅ Phase 1
- [x] Every model doc Section 5 has H³ demands with citations ✅ Phase 1
- [x] Every model doc Section 8 has MNI coordinates verified against papers ✅ Phase 1
- [ ] Docs/C³/ has complete documentation architecture mirroring mi_beta/brain/ (Phase 2)
- [ ] Every code component in mi_beta/brain/ has a documentation counterpart (Phase 2)
- [ ] Docs/R³/ has complete spectral architecture: demand matrix + DSP survey + v2 design + per-group specs + per-unit mappings (Phase 3A-3C)
- [ ] All 96 model docs Section 4 updated for R³ v2 expanded space, bumped to v2.2.0 (Phase 3E)
- [ ] Docs/H³/ has complete temporal architecture with per-unit demands (Phase 4)
- [x] Docs/L³/ has complete semantic architecture with per-unit mappings (Phase 5) ✅ 69 files across 13 subdirectories
- [ ] `pytest tests/ -v` passes (Phase 6)
- [ ] `python -m mi_beta` runs without errors (Phase 6)
