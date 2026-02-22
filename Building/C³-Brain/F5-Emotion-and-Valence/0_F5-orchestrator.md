# F5 -- Emotion & Valence

**Function**: F5 Emotion & Valence
**Models**: 12 (10 ARU complete unit + 2 non-ARU F5-primary: MAA[PCU], STAI[SPU]) + 3 secondary (ICEM[PCU]*, MEAMN[IMU]*, CDEM[IMU]*)
**Beliefs**: 14 (4 Core + 8 Appraisal + 2 Anticipation)
**Total output**: 142D (all 12 models)
**H3 demands**: ~283 tuples total (SRP ~124, AAC ~50, VMM 7, PUPF 21, CLAM 12, MAD 9, NEMAC 13, DAP 6, CMAT 9, TAR 21, MAA 14, STAI 14)
**Phase**: 2 (reads F1-F3 beliefs + MEAMN relay)
**Relay**: SRP (ARU-a1) -- F6 primary, provides reward pathway
**Implemented**: SRP relay partial (kernel v4.0), no F5 mechanism models yet

---

## 1. What F5 Does

F5 processes the EMOTIONAL dimension of music -- perceived emotion (happy/sad), felt emotion (arousal/chills), autonomic responses (heart rate, skin conductance), nostalgia-affect coupling, and aesthetic valence. It bridges sensory processing (F1-F3) with reward (F6).

F5 is in **Phase 2**: it reads F1-F3 beliefs plus the MEAMN relay. The SRP relay (a-tier) reads R3/H3 directly; b-models read a outputs + F1-F3 beliefs; g-models read a+b. F5 receives cross-function inputs from PCU(ICEM), IMU(MEAMN, CDEM).

### Key Neuroscience Circuits

- **Autonomic-Affective Pathway**: Amygdala + hypothalamus + brainstem -> physiological arousal
- **Valence-Mode Circuit**: vmPFC + NAcc + auditory cortex -> major/minor mode detection
- **Nostalgia-Affect Circuit**: Hippocampus + mPFC + striatum -> nostalgia-wellbeing
- **Chills/Frisson Pathway**: NAcc + insula + orbitofrontal cortex -> peak emotional experiences

```
Audio -> R3 (97D) ---+--------------------------------------------
H3 tuples -----------+
F1-F3 beliefs -------+
                     |
                     v
Depth 0:  SRP  (19D, relay)  <- striatal reward pathway [F6 primary]
          AAC  (14D)         <- autonomic-affective coupling
          VMM  (12D)         <- valence-mode mapping
                     |
                     v
Depth 1:  PUPF (12D)  <- psycho-neuro-pharmacological framework [F2 primary]
          CLAM (11D)  <- closed-loop affective modulation
          MAD  (11D)  <- musical anhedonia disconnection [F10 primary]
          NEMAC(11D)  <- nostalgia-enhanced memory-affect [F4 primary]
          STAI (12D)  <- spectral-temporal aesthetic integration
                     |
                     v
Depth 2:  DAP  (10D)  <- developmental affective plasticity [F11 primary]
          CMAT (10D)  <- cross-modal affective transfer
          TAR  (10D)  <- therapeutic affective resonance
          MAA  (10D)  <- multifactorial atonal appreciation
```

---

## 2. Complete Model Inventory

| # | Model | Unit | Tier | Depth | Output | H3 | Beliefs | Primary Fn | Status |
|---|-------|------|------|-------|--------|-----|---------|-----------|--------|
| 1 | **SRP** | ARU | a | 0 | 19D | ~124 | 0 (F6 beliefs) | F6 | relay partial |
| 2 | AAC | ARU | a | 0 | 14D | ~50 | 4 (1C+2A+1N) | F5 | pending |
| 3 | VMM | ARU | a | 0 | 12D | 7 | 6 (2C+4A) | F5 | pending |
| 4 | PUPF | ARU | b | 1 | 12D | 21 | 0 | F2 | pending |
| 5 | CLAM | ARU | b | 1 | 11D | 12 | 0 | F5 | pending |
| 6 | MAD | ARU | b | 1 | 11D | 9 | 0 | F10 | pending |
| 7 | NEMAC | ARU | b | 1 | 11D | 13 | 4 (1C+2A+1N) | F4 | pending |
| 8 | STAI | SPU | b | 1 | 12D | 14 | 0 | F5 | pending |
| 9 | DAP | ARU | g | 2 | 10D | 6 | 0 | F11 | pending |
| 10 | CMAT | ARU | g | 2 | 10D | 9 | 0 | F5 | pending |
| 11 | TAR | ARU | g | 2 | 10D | 21 | 0 | F5 | pending |
| 12 | MAA | PCU | g | 2 | 10D | 14 | 0 | F5 | pending |

**Secondary (cross-function):**

| # | Model | Unit | Primary | F5 Contribution |
|---|-------|------|---------|-----------------|
| * | ICEM | PCU-a3 | F2 | Information content -> emotional arousal |
| * | MEAMN | IMU-a1 | F4 | Emotional coloring of memories |
| * | CDEM | IMU-g3 | F4 | Context-dependent emotional memory |

---

## 3. Complete Belief Inventory (14)

| # | Belief | Cat | t | Owner | Mechanism Source | Status |
|---|--------|-----|---|-------|------------------|--------|
| 1 | `perceived_happy` | C | 0.55 | VMM | mode_detection + valence pathway | pending |
| 2 | `perceived_sad` | C | 0.55 | VMM | mode_detection + valence pathway | pending |
| 3 | `emotional_arousal` | C | 0.5 | AAC | autonomic_coupling + driving_signal | pending |
| 4 | `nostalgia_affect` | C | 0.65 | NEMAC | nostalgia_link + memory-affect | pending |
| 5 | `mode_detection` | A | -- | VMM | major/minor classification | pending |
| 6 | `emotion_certainty` | A | -- | VMM | valence confidence | pending |
| 7 | `happy_pathway` | A | -- | VMM | major-mode activation | pending |
| 8 | `sad_pathway` | A | -- | VMM | minor-mode activation | pending |
| 9 | `chills_intensity` | A | -- | AAC | frisson peak detection | pending |
| 10 | `ans_dominance` | A | -- | AAC | sympathetic/parasympathetic balance | pending |
| 11 | `self_referential_nostalgia` | A | -- | NEMAC | self-referential processing | pending |
| 12 | `wellbeing_enhancement` | A | -- | NEMAC | nostalgia-wellbeing coupling | pending |
| 13 | `driving_signal` | N | -- | AAC | arousal trajectory prediction | pending |
| 14 | `nostalgia_peak_pred` | N | -- | NEMAC | nostalgia peak prediction | pending |

---

## 4. Observe Formula -- placeholder

No F5 mechanism models implemented yet. SRP relay is partial (kernel v4.0).
F5 Core beliefs have MODERATE t (0.5-0.65), reflecting emotion's moderate temporal
persistence -- faster than memory (F4: 0.7-0.85) but slower than attention (F3: 0.25-0.4).

Multi-scale horizons (to be defined per Core belief):
```
perceived_happy:     TBD (moderate band, ~1-8s characteristic)
perceived_sad:       TBD (moderate band, ~1-8s characteristic)
emotional_arousal:   TBD (moderate band, ~0.5-4s characteristic)
nostalgia_affect:    TBD (macro band, ~4-16s characteristic)
```

---

## 5. Multi-Scale Horizons (all F5 Core Beliefs)

| Core Belief | T_char | Horizons | Band |
|-------------|--------|----------|------|
| perceived_happy | ~2s | TBD | Moderate |
| perceived_sad | ~2s | TBD | Moderate |
| emotional_arousal | ~1s | TBD | Moderate |
| nostalgia_affect | ~8s | TBD | Macro |

---

## 6. Dependency Graph

```
                          R3 (97D) + H3
                              |
            +-----------------+------------------+
            v                 v                  v
         SRP (a1)          AAC (a2)           VMM (a3)
         19D relay         14D                12D
            |                |                  |
     +------+------+   +----+----+        +----+----+
     v      v      v   v         v        v         v
  PUPF(b1) CLAM(b2) MAD(b3)  NEMAC(b4)  STAI(b5)
   12D      11D     11D       11D        12D
     |        |      |         |          |
     +---+----+------+---------+----------+
         v         v           v          v
      DAP(g1)   CMAT(g2)   TAR(g3)    MAA(g4)
       10D        10D        10D       10D
```

### Key Dependencies

| Model | Reads From |
|-------|-----------|
| SRP (a1) | R3/H3 directly (relay) -- provides reward pathway to F6 |
| AAC (a2) | R3/H3 directly -- autonomic-affective coupling |
| VMM (a3) | R3/H3 directly -- valence-mode mapping |
| PUPF (b1) | SRP; psycho-neuro-pharmacological framework (F2 cross-fn) |
| CLAM (b2) | AAC, SRP; closed-loop affective modulation |
| MAD (b3) | SRP, AAC; musical anhedonia disconnection (F10 cross-fn) |
| NEMAC (b4) | MEAMN relay (F4), AAC; nostalgia-memory-affect coupling (F4 cross-fn) |
| STAI (b5) | VMM, AAC; spectral-temporal aesthetic integration |
| DAP (g1) | NEMAC, DMMS (F4 cross-fn); developmental affective plasticity (F11 cross-fn) |
| CMAT (g2) | VMM, AAC, CLAM; cross-modal affective transfer |
| TAR (g3) | CLAM, MAD, AAC; therapeutic affective resonance |
| MAA (g4) | VMM, STAI; multifactorial atonal appreciation |

---

## 7. Unit Architecture

### ARU -- Aesthetic-Reward Unit (10 primary F5 models)

ARU is the **DOMINANT UNIT** for F5, housing 10 of 12 primary models.
ARU is shared with F6 (SRP is F6-primary). Unlike F4 (single-unit IMU),
F5 draws from 3 units: ARU (10), PCU (1 -- MAA), SPU (1 -- STAI).

```
ARU models in F5:    SRP --- AAC --- VMM
                      |        |       |
                    PUPF --- CLAM --- MAD --- NEMAC
                      |        |       |        |
                    DAP  --- CMAT --- TAR
```

Non-ARU models in F5:
- **PCU** (Predictive Coding Unit): MAA (multifactorial atonal appreciation)
- **SPU** (Spectral Processing Unit): STAI (spectral-temporal aesthetic integration)

F5 also receives cross-function contributions from:
- **PCU** (Predictive Coding Unit): ICEM (information content -> emotional arousal)
- **IMU** (Integrative Memory Unit): MEAMN (emotional coloring), CDEM (emotional memory)

---

## 8. Documentation Structure

```
F5-Emotion-and-Valence/
+-- 0_F5-orchestrator.md                  <- this file
+-- collections.md                         <- full model inventory
+-- mechanisms/
|   +-- 0_mechanisms-orchestrator.md       <- all 12 models documented
|   +-- srp/ (4 layer docs)
|   +-- aac/ (4 layer docs)
|   +-- vmm/ (4 layer docs)
|   +-- pupf/ (4 layer docs)
|   +-- clam/ (4 layer docs)
|   +-- mad/ (4 layer docs)
|   +-- nemac/ (4 layer docs)
|   +-- stai/ (4 layer docs)
|   +-- dap/ (4 layer docs)
|   +-- cmat/ (4 layer docs)
|   +-- tar/ (4 layer docs)
|   +-- maa/ (4 layer docs)
+-- beliefs/
    +-- 0_beliefs_orchestrator.md
    +-- vmm/ (6 belief docs)
    +-- aac/ (4 belief docs)
    +-- nemac/ (4 belief docs)
```

**1 a-tier relay partial (SRP, ~124 H3 tuples).** Pending: 2 a (AAC, VMM) + 4 b (PUPF, CLAM, MAD, NEMAC) + 1 b non-ARU (STAI) + 4 g (DAP, CMAT, TAR, MAA) -- ~159 H3 tuples remaining.
