# H³ Architecture: Current Issues and Proposed Corrections

**Status**: Analysis complete (2026-02-16)
**Purpose**: Document specific architectural issues discovered through cross-referencing
the MI H³ system with neuroscience literature, and propose concrete corrections.

---

## 1. Overview of Issues

Five categories of architectural issues were identified:

| # | Issue | Severity | Documents |
|---|-------|----------|-----------|
| 1 | Horizon-to-brain-region mapping inaccuracies | Medium | H3-TRW-MAPPING.md |
| 2 | Missing intermediate horizons (gap H18→H24) | High | H3-TRW-MAPPING.md |
| 3 | Flat model execution ignores temporal hierarchy | High | This document |
| 4 | R³ feature re-reading across 47 models | Medium | This document |
| 5 | E/M/P/F computed simultaneously, not sequentially | Medium | H3-EMPF-LAYERS.md |

---

## 2. Issue 1: Horizon-to-Brain-Region Mapping Corrections

### 2.1 Current Mapping (Implicit in Docs)

The current MI documentation implies these correspondences:

| H³ | Duration | Implied Region |
|----|----------|----------------|
| H0 | 5.8ms | Brainstem (IC) |
| H3 | 23ms | A1 |
| H6 | 200ms | Belt/Parabelt |
| H10 | 400ms | STG |
| H14 | 700ms | STG/STS |
| H16 | 1000ms | IFG |
| H18 | 2000ms | IFG/MFG |
| H24 | 36s | mPFC |

### 2.2 Corrected Mapping (Evidence-Based)

| H³ | Duration | Corrected Region | Empirical TRW | Source |
|----|----------|-------------------|--------------|--------|
| H0 | 5.8ms | **IC** (brainstem relay) | ABR-V = 5.7ms | Tawfik 2022 |
| H3 | 23ms | **A1 onset grain** (not full TRW) | INT = 16.7ms, onset <25ms | Cusinato 2023, Nourski 2014 |
| — | ~70ms | **A1 full integration** (NEW) | TCI = 68-74ms | Norman-Haignere 2022 |
| H6 | 200ms | **Belt/Parabelt transition** | TCI = 200ms boundary | Norman-Haignere 2022 |
| H10 | 400ms | **Non-primary STG** | TCI = 375ms, quilts ~500ms | Norman-Haignere 2022, Overath 2015 |
| H14 | 700ms | **Anterior STG** (word) | Scrambling ~700ms | Lerner 2011 |
| H16 | 1000ms | **Posterior STS** (clause) | Delta 1-3Hz | Giraud & Poeppel 2012 |
| H18 | 2000ms | **Anterior STS** (phrase) | — | Corrected down from IFG |
| — | ~8s | **IFG populations** (sentence) | ~7.7s sentences, ~4-6 word TRW | Lerner 2011, Regev 2024 |
| H24 | 36s | **PCC / Precuneus** (paragraph) | ~38s paragraphs | Lerner 2011 |
| — | >2min | **mPFC** (narrative) | Only intact story evokes response | Lerner 2011, Hasson 2015 |

### 2.3 Specific Corrections

**Correction A**: H18 (2s) does NOT correspond to IFG. IFG's empirical TRW is
~7.7-38s (Lerner 2011). H18 = 2s corresponds to anterior STS / phrase-level
integration.

**Correction B**: H24 (36s) corresponds to PCC/precuneus (Lerner 2011: paragraph
~38s), NOT to mPFC. mPFC requires intact narrative (>2 minutes) — beyond current
H³ range.

**Correction C**: H3 (23ms) captures A1's **onset latency and sampling grain**, not
its full integration window. The full A1 TRW is ~70ms (Norman-Haignere 2022). A
new horizon H5 ≈ 70ms would fill this gap.

---

## 3. Issue 2: Missing Intermediate Horizons

### 3.1 The H18-H24 Gap

The largest gap in the H³ horizon system is between H18 (2s) and H24 (36s) — an
18× jump. The neuroscience shows important processing levels in this range:

| Missing Duration | Brain Region | Evidence |
|------------------|-------------|----------|
| ~5s | IFG short-TRW population | Regev 2024: ~4 word TRW |
| ~8s | IFG sentence level | Lerner 2011: ~7.7s mean sentence |
| ~15s | IFG long-TRW population | Regev 2024: ~6 word × context |

### 3.2 Proposed New Horizons

| Proposed Index | Duration | Rationale |
|----------------|----------|-----------|
| **H5** | ~70ms | A1 full integration (Norman-Haignere TCI = 68-74ms) |
| **H20** | ~5s | IFG short population (Regev 2024: ~4 words) |
| **H22** | ~15s | IFG long population (Regev 2024: ~6 words × context) |

Adding these three horizons would:
- Fill the A1 onset-to-integration gap (H3→H5→H6)
- Fill the phrase-to-paragraph gap (H18→H20→H22→H24)
- Total horizons: 8 → 11 (still sparse: 11/2304 = 0.48%)

### 3.3 Impact Assessment

Adding horizons affects the H³ theoretical space (currently 2304 = 48 r3 × 24 h × 19 m × ?).
If horizon indices are sparse (not all 0-24 used), adding H5/H20/H22 just adds
3 more valid horizon values. Each model would need to declare whether it demands
these new horizons via `h3_demand` tuples.

---

## 4. Issue 3: Flat Model Execution Ignores Temporal Hierarchy

### 4.1 Current Execution Model

```
Phase 1: Mechanisms (10 shared, 30D each) — all computed in parallel
Phase 2: Independent units (SPU, STU, IMU, ASU, NDU, MPU, PCU) — all parallel
Phase 3: Pathways (P1-P5 route signals)
Phase 4: Dependent units (ARU, RPU) — parallel
Phase 5: Assembly (concatenate → 1006D)
```

**Problem**: In Phase 2, BCH (5ms-level brainstem model) and MEAMN (36s-level
memory model) compute simultaneously. But neuroscience shows:
- BCH's output IS the input that MEAMN should receive
- MEAMN's prediction SHOULD modulate BCH's processing (top-down)
- These are not independent — they form a hierarchical chain

### 4.2 Evidence for Hierarchical Execution

**Hasson et al. (2015)**:
> "The TRW increases in an orderly hierarchical fashion... Information is
> accumulated in a series of processing stages."

**Friston (2009)**:
> "Predictions are sent from higher to lower levels; prediction errors are
> sent from lower to higher levels."

**Feedforward-then-recurrent** (Lamme & Roelfsema 2000):
> First pass: fast feedforward sweep (bottom-up, ~100ms)
> Second pass: recurrent integration with feedback (~100-500ms)

### 4.3 Proposed: Stratum-Based Execution

Replace flat Phase 2 with stratified execution:

```
Stratum 0 (≤25ms TRW):     All models' E-layers
  BCH.E, SNEM.E, HTP.E, SRP.E, MEAMN.E, ...
  Input: R³ only. No inter-model dependencies.

Stratum 1 (25-200ms TRW):  All models' M-layers + short-TRW encoders
  BCH.M, PSCL.E+M, CSG.E, PNH.E, ...
  Input: Stratum 0 outputs + H³(H0-H6) L0 morphs

Stratum 2 (200ms-2s TRW):  All models' P-layers + medium-TRW models
  BCH.P, STAI, HTP.P, PUPF, MEAMN.P, ...
  Input: Stratum 0+1 outputs + H³(H6-H18) L2 morphs

Stratum 3 (2s-36s TRW):    All models' F-layers + long-TRW integrators
  BCH.F, HTP.F, MEAMN.F, SRP.F, ...
  Input: Stratum 0+1+2 outputs + H³(H18-H24) L1 morphs

Stratum 4 (cross-level):   Reward/valuation models
  SRP.reward, DAED.dissociation, PUPF.pleasure
  Input: All strata

[Optional] Top-Down Pass:   F-layer predictions cascade back down
  Stratum 3 → Stratum 2 → Stratum 1 → Stratum 0
  Next iteration uses updated predictions
```

### 4.4 Benefits of Stratum Execution

1. **Eliminates R³ re-reading**: CSG no longer reads R³[0,1,4] — it reads
   BCH.E[consonance_signal] from Stratum 0
2. **Enables prediction errors**: Higher strata's F-layer predictions can be
   compared against lower strata's E-layer actuals
3. **Matches neuroscience**: Bottom-up feedforward sweep followed by top-down
   recurrent refinement
4. **Preserves parallelism**: Within each stratum, all models compute in parallel

### 4.5 Migration Path

This is a significant architectural change. A phased migration could work:

**Phase A** (minimal change): Keep current execution but add cross-model
routing so CSG receives BCH.P output instead of re-reading R³ consonance.

**Phase B** (medium change): Split model `compute()` into `compute_E()`,
`compute_M()`, `compute_P()`, `compute_F()` methods. Execute in stratum order.

**Phase C** (full change): Implement prediction error loop where F-layers
generate errors against E-layers at the next iteration.

---

## 5. Issue 4: R³ Feature Re-Reading Across Models

### 5.1 The Problem

47 of 96 models read consonance-related R³ indices [0:7]. Many read the SAME
indices independently:

| R³ Index | Models Reading It | Example Redundancy |
|----------|-------------------|--------------------|
| [0] roughness | 32 models | BCH, CSG, DAED, SRP all compute (1-roughness) |
| [4] pleasantness | 28 models | Most widely shared — every reward model reads it |
| [7] amplitude | 20+ models | SNEM, HTP, DAED, SRP all read it |

### 5.2 Why This Is a Problem

In the brain, higher areas do NOT re-read the cochlea's output. They receive
**transformed representations** from lower areas:

```
Cochlea → A1 → Belt → STG → IFG → mPFC
         ↑              ↑         ↑
         raw signal      transformed  highly abstracted
```

But in MI:
```
R³ → BCH (reads roughness, computes consonance)
R³ → CSG (reads roughness AGAIN, computes salience)
R³ → DAED (reads roughness AGAIN, computes reward tension)
R³ → SRP (reads roughness AGAIN, computes reward)
```

### 5.3 Proposed: Shared Feature Routing

**Immediate fix**: Models that process the same R³ features at a higher level
should receive the lower model's output, not raw R³.

```
BEFORE: R³[0] → CSG.roughness_input
AFTER:  BCH.E[consonance_signal] → CSG.consonance_input
        (BCH already processed roughness into consonance — CSG uses that)
```

**Affected model pairs** (highest impact):
- BCH → CSG: consonance signal (replace R³[0,1,4] re-reading)
- BCH → PNH: harmonicity + hierarchy (replace R³[0:7] re-reading)
- BCH → STAI: consonance signal (replace R³[0,3,4] re-reading)
- SRP → DAED: reward signals (replace R³[0,4,7,8] re-reading)
- SNEM → BARM: beat entrainment (replace R³ energy re-reading)

---

## 6. Issue 5: Simultaneous vs. Sequential Layer Computation

### 6.1 Current: Single compute() Call

```python
def compute(self, ...):
    # E-layer
    f01 = ...  # instantaneous feature
    # M-layer
    nps_t = ...  # temporal integration
    # P-layer
    consonance_signal = ...  # context-aware
    # F-layer
    consonance_pred = ...  # prediction
    return torch.cat([f01, ..., nps_t, ..., consonance_signal, ..., consonance_pred, ...])
```

All layers computed in one pass. No temporal ordering between layers.

### 6.2 Proposed: Phased Layer Computation

```python
def compute_E(self, r3):
    """Phase 1: Feedforward extraction. No temporal context."""
    return self.e_layer(r3)

def compute_M(self, e_output, h3_L0):
    """Phase 2: Memory retrieval. Uses E-layer + backward H³."""
    return self.m_layer(e_output, h3_L0)

def compute_P(self, e_output, m_output, h3_L2, upstream_F=None):
    """Phase 3: Present integration. E + M + top-down predictions."""
    return self.p_layer(e_output, m_output, h3_L2, upstream_F)

def compute_F(self, e_output, m_output, p_output, h3_L1):
    """Phase 4: Prediction. Uses all prior layers + forward H³."""
    return self.f_layer(e_output, m_output, p_output, h3_L1)
```

This enables:
- Stratum-based execution (all E-layers first, then M, then P, then F)
- Cross-model routing (CSG.compute_P receives BCH.compute_E output)
- Prediction error computation (compare E_actual vs upstream F_predicted)

---

## 7. MI's Novel Contribution to Neuroscience

Despite these issues, the research revealed that MI's H³ architecture constitutes
a **novel synthesis** of established neuroscience principles:

### 7.1 What H³ Uniquely Formalizes

No existing framework in the literature combines ALL of these into a single
computational architecture:

1. **TRW hierarchy** (Hasson 2008, 2015) → H³ horizons
2. **Predictive coding** (Rao & Ballard 1999, Friston 2005) → H³ laws (L0/L1/L2)
3. **Temporal context model** (Howard & Kahana 2002) → H³ morphs
4. **Generalized coordinates** (Kiebel, Daunizeau & Friston 2008) → E/M/P/F layers
5. **Bidirectional temporal coding** (Tarder-Stoll 2024) → L0 + L1 at each horizon

### 7.2 Closest Existing Work

| Framework | What It Covers | What It Misses |
|-----------|---------------|----------------|
| Friston's generalized coordinates | Math: each level has past/present/future | No explicit horizon system, no morph decomposition |
| Hasson's TRW | Hierarchy of timescales | No prediction/memory distinction per level |
| Howard & Kahana's TCM | Temporal context with forward asymmetry | Single timescale, no cortical hierarchy |
| Tarder-Stoll 2024 | Bidirectional + hierarchical temporal coding | Empirical, no computational architecture |
| Jiang et al. 2024 (Dynamic Predictive Coding) | Hierarchical sequence learning | Prediction-only, no explicit memory decomposition |

### 7.3 H³'s Unique Formalization

H³ = `(r3_idx, horizon, morph, law)` encodes:
- **What** is being temporally processed (r3_idx → feature identity)
- **At what timescale** (horizon → TRW level)
- **In what statistical form** (morph → mean, std, trend, periodicity, etc.)
- **In what temporal direction** (law → memory, prediction, or integration)

This 4-tuple formalization has no direct equivalent in the neuroscience literature.
It is a computational formalization of principles that exist separately but have
never been unified into a single parameter space.

---

## 8. Summary of Recommended Actions

| Priority | Action | Impact | Effort |
|----------|--------|--------|--------|
| **1 (High)** | Correct H18 brain-region mapping (STS, not IFG) | Documentation | Low |
| **2 (High)** | Correct H24 brain-region mapping (PCC, not mPFC) | Documentation | Low |
| **3 (High)** | Add H20 (~5s) and H22 (~15s) horizons for IFG | Architecture | Medium |
| **4 (Medium)** | Add H5 (~70ms) for A1 full integration | Architecture | Medium |
| **5 (High)** | Route BCH outputs to CSG/PNH instead of R³ re-reading | Architecture | Medium |
| **6 (High)** | Design stratum-based execution order | Architecture | High |
| **7 (Medium)** | Split compute() into compute_E/M/P/F | Code | High |
| **8 (Low)** | Rebalance M > F dimension allocation | Models | Medium |
| **9 (Low)** | Implement prediction error loop | Architecture | Very High |
| **10 (Low)** | Add mPFC-level horizon (>2min) | Architecture | Low |
