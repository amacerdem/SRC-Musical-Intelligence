# Branch-Consonance

R³ Group A [0:7] Consonance — Full integration branch.
Tum R³→H³→C³ pipeline'ini izleyen ilk entegrasyon dalı.

---

## 1. R³ Source: Group A Consonance [0:7]

**Stage 1** — dogrudan mel spectrogram'dan hesaplanır, dependency yok.

| Idx | Feature | Method | Range | Source |
|-----|---------|--------|-------|--------|
| 0 | roughness | Plomp-Levelt / Sethares pairwise, CB-weighted | [0,1] | Plomp & Levelt 1965, Zwicker & Fastl 2007 |
| 1 | sethares_dissonance | Sethares 1993 2nd ed., pairwise partial beating | [0,1] | Sethares 1993, 2005 |
| 2 | helmholtz_kang | Harmonic template matching (HPS-based F0) | [0,1] | Helmholtz, Bidelman & Krishnan 2009 |
| 3 | stumpf_fusion | Harmonicity ratio (harmonic / total energy) | [0,1] | Stumpf tonal fusion theory |
| 4 | sensory_pleasantness | 0.6×(1−sethares) + 0.4×stumpf | [0,1] | Derived composite |
| 5 | inharmonicity | 1 − stumpf_fusion | [0,1] | Inverse harmonicity |
| 6 | harmonic_deviation | Partial amplitude deviation from 1/n decay | [0,1] | Spectral envelope analysis |

### Computation

- **Audio mode** (real psychoacoustics): STFT → peak picking (top-20, parabolic interpolation) → Sethares pairwise dissonance → Plomp-Levelt CB roughness → HPS F0 → Helmholtz template + Stumpf ratio
- **Mel fallback** (proxy): mel statistics (high-band variance, spectral diff, autocorrelation, low-freq ratio)
- **Dependencies**: None (Stage 1, DEPENDENCIES = ())
- **Output shape**: (B, T, 7), clamped [0, 1]

### Internal Derivation Graph

```
STFT(audio) → mag(B,T,F) → peak_picking → freqs(B,T,K), amps(B,T,K)
                                              ↓
           ┌──────────────────────────────────┼───────────────────┐
           ↓                                  ↓                   ↓
   _sethares_dissonance[1]           _roughness[0]        _estimate_f0 → f0
           ↓                                                      ↓
   1−sethares ──→ 0.6×(1−seth)                    ┌──────────────┼──────────────┐
                     +                             ↓              ↓              ↓
               0.4×stumpf ──→ pleasantness[4]   _helmholtz[2]  _stumpf[3]   _harmonic_dev[6]
                                                                  ↓
                                                        1−stumpf → inharmonicity[5]
```

---

## 2. H³ Demands — Temporal Morphology

Group A R³ features'in H³ tarafından temporal analysis'e tabi tutulduğu tüm (r3_idx, horizon, morph, law) tuple'ları.
96 model doc'undan toplandı.

### Unique H³ Tuples for r3_idx [0:6]

#### [0] roughness — 22 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 0 | 0 | M0 (value) | L2 | BCH, STAI, SDNPS, SDED, CSG |
| 0 | 3 | M0 (value) | L2 | DAED, MORMR, RPEM, IACM, AACM, PCCR, MAA, CHPI, SDD |
| 0 | 3 | M1 (mean) | L2 | BCH, STAI, SDNPS, SDED, CSG |
| 0 | 3 | M2 (std) | L2 | CSG |
| 0 | 3 | M8 (velocity) | L0 | RPEM |
| 0 | 3 | M20 (entropy) | L2 | IACM, SDD |
| 0 | 6 | M14 (period.) | L0 | SDNPS |
| 0 | 6 | M18 (trend) | L0 | BCH |
| 0 | 8 | M1 (mean) | L2 | IUCP, MCCN, SSPS, IOTMS, SSRI |
| 0 | 8 | M8 (velocity) | L0 | DAED |
| 0 | 10 | M0 (value) | L2 | TPRD, PNH, PMIM, MSPBA |
| 0 | 14 | M1 (mean) | L0 | TPRD, PNH, PMIM, MSPBA |
| 0 | 16 | M0 (value) | L2 | MEAMN, MMP, RASN, OII, VRIAP, CMAPCC, DMMS, CDEM, MAA |
| 0 | 16 | M1 (mean) | L2 | MORMR, CSG, AACM, MAA |
| 0 | 16 | M2 (std) | L2 | IUCP, MCCN, SSPS |
| 0 | 16 | M6 (skew) | L2 | IOTMS |
| 0 | 18 | M18 (trend) | L0 | PNH, PMIM, MSPBA |
| 0 | 20 | M1 (mean) | L0 | DMMS |
| 0 | 20 | M18 (trend) | L0 | MEAMN, RASN, VRIAP, CMAPCC, CDEM |
| 0 | 24 | M1 (mean) | L0 | MMP, OII |
| 0 | H3 | ref only | — | ARU: SRP, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR |

#### [1] sethares_dissonance — 5 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 1 | 0 | M0 (value) | L2 | SDED |
| 1 | 3 | M0 (value) | L2 | CSG |
| 1 | 8 | M8 (velocity) | L0 | CSG |
| 1 | 10 | M0 (value) | L2 | MSPBA |
| 1 | 14 | M8 (velocity) | L0 | MSPBA |
| 1 | 16 | M1 (mean) | L2 | CMAPCC |
| 1 | 24 | M19 (stability) | L0 | CMAPCC |
| 1 | ref only | — | — | ARU-SRP |

#### [2] helmholtz_kang — 7 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 2 | 0 | M0 (value) | L2 | BCH, STAI, SDNPS, SDED |
| 2 | 3 | M1 (mean) | L2 | BCH, STAI, ESME, SDED |
| 2 | 3 | M19 (stability) | L2 | PCCR |
| 2 | 6 | M0 (value) | L0 | PCCR |
| 2 | 8 | M1 (mean) | L0 | MDNS |
| 2 | 18 | M1 (mean) | L0 | PNH |
| 2 | ref only | — | — | ARU-SRP |

#### [3] stumpf_fusion — 15 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 3 | 0 | M0 (value) | L2 | BCH, TPRD, PNH, PMIM, MSPBA, NSCP |
| 3 | 3 | M0 (value) | L2 | NSCP |
| 3 | 3 | M1 (mean) | L2 | BCH, TPRD |
| 3 | 6 | M1 (mean) | L0 | BCH, TPRD |
| 3 | 10 | M0 (value) | L2 | PNH, PMIM, MSPBA, OII |
| 3 | 10 | M1 (mean) | L2 | OII |
| 3 | 14 | M1 (mean) | L2 | PNH, MSPBA |
| 3 | 14 | M14 (period.) | L0 | PMIM |
| 3 | 16 | M0 (value) | L2 | MMP |
| 3 | 16 | M1 (mean) | L2 | MEAMN, RASN, HCMC, CMAPCC, DMMS, CSSL, CDEM, VRIAP |
| 3 | 16 | M3 (std) | L2 | HCMC |
| 3 | 18 | M1 (mean) | L0 | OII |
| 3 | 20 | M1 (mean) | L2 | MEAMN |
| 3 | 20 | M1 (mean) | L0 | RASN, HCMC, CMAPCC, CSSL, CDEM, VRIAP |
| 3 | 24 | M1 (mean) | L0 | MEAMN, RASN, CSSL |
| 3 | 24 | M19 (stability) | L0 | MMP, HCMC |
| 3 | ref only | — | — | ARU-SRP |

#### [4] sensory_pleasantness — 19 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 4 | 3 | M0 (value) | L2 | STAI, CSG, RPEM, LDAC, PSCL, SPH, ICEM, PWUP, UDP, CHPI, MAA, NSCP(?) |
| 4 | 3 | M8 (velocity) | L2 | CSG |
| 4 | 8 | M1 (mean) | L2 | IOTMS, SSPS, MEAMR, SSRI, LDAC |
| 4 | 8 | M2 (std) | L0 | ICEM |
| 4 | 10 | M0 (value) | L2 | PNH, PMIM |
| 4 | 16 | M0 (value) | L2 | MEAMN, RASN, MMP, OII, VRIAP, CMAPCC, DMMS, CDEM |
| 4 | 16 | M1 (mean) | L2 | MORMR, IUCP, IOTMS, SSRI, DAED |
| 4 | 16 | M1 (mean) | L0 | SPH, PWUP, UDP, MAA, PSH, RIRI |
| 4 | 16 | M2 (std) | L2 | IUCP, LDAC |
| 4 | 16 | M8 (velocity) | L0 | MORMR |
| 4 | 16 | M15 (smooth.) | L0 | SSPS |
| 4 | 16 | M18 (trend) | L2 | MEAMR |
| 4 | 16 | M20 (entropy) | L0 | PWUP, UDP, CHPI, MAA |
| 4 | 18 | M19 (stability) | L0 | TPRD, PNH, PMIM, MSPBA |
| 4 | 20 | M1 (mean) | L0 | DMMS |
| 4 | 20 | M18 (trend) | L0 | MEAMN, RASN, VRIAP, CMAPCC, CDEM |
| 4 | 24 | M1 (mean) | L0 | MMP, CMAPCC |
| 4 | ref only | — | — | ARU: SRP, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR |

#### [5] inharmonicity — 9 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 5 | 0 | M0 (value) | L2 | BCH, SDNPS, SDED |
| 5 | 3 | M0 (value) | L2 | PSCL, PCCR, IACM(?) |
| 5 | 3 | M1 (mean) | L2 | SDNPS |
| 5 | 3 | M18 (trend) | L0 | BCH |
| 5 | 5 | M0 (value) | L2 | TSCP, MIAA |
| 5 | 6 | M18 (trend) | L0 | PCCR |
| 5 | 10 | M0 (value) | L2 | TPRD, PNH, PMIM, MSPBA |
| 5 | 14 | M1 (mean) | L0 | TPRD, PNH, MSPBA |
| 5 | 14 | M8 (velocity) | L0 | PMIM |
| 5 | ref only | — | — | ARU-SRP |

#### [6] harmonic_deviation — 4 unique tuples

| r3 | H | Morph | Law | Models |
|----|---|-------|-----|--------|
| 6 | 0 | M0 (value) | L2 | BCH |
| 6 | 3 | M1 (mean) | L0 | BCH |
| 6 | 10 | M0 (value) | L2 | TPRD |
| 6 | 14 | M0 (value) | L0 | PNH |
| 6 | ref only | — | — | ARU: SRP, PUPF |

### H³ Horizon Coverage

```
Horizons used by consonance branch:
H0(25ms)  H3(100ms)  H5(46ms)  H6(200ms)  H8(500ms)
H10(400ms)  H14(700ms)  H16(1s)  H18(2s)  H20(5s)  H24(36s)

Morphologies used:
M0(value) M1(mean) M2(std) M3(std-alt) M6(skew) M8(velocity)
M14(periodicity) M15(smoothness) M18(trend) M19(stability) M20(entropy)
```

---

## 3. C³ Models — Complete Census

96 model doc tarandı. **62 model** en az bir Group A consonance feature kullanıyor.

### SPU — Sensory Processing Unit (9/9)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **BCH** | α | 0,2,3,5,6 (all core) | 11 | 12D |
| **PSCL** | α | 4,5 | 2 | 12D |
| **PCCR** | α | 0,2,5 | 5 | 11D |
| **STAI** | β | 0,2,4 | 5 | 12D |
| **TSCP** | β | 5 | 1 | 10D |
| **MIAA** | β | 5 | 1 | 11D |
| **SDNPS** | γ | 0,2,5 | 6 | 10D |
| **ESME** | γ | 2 | 2 | 11D |
| **SDED** | γ | 0,1,2,5 | 6 | 10D |

**SPU consonance role**: Primary sensory encoding. BCH = brainstem hierarchy, PSCL/PCCR = cortical pitch, STAI = aesthetic integration, SDNPS/SDED = dissonance detection.

### IMU — Integrative Memory Unit (14/15)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **MEAMN** | α | 0,3,4 | 7 | 11D |
| **PNH** | α | 0,2,3,4,5,6 | 10 | 10D |
| **MMP** | α | 0,3,4 | 6 | 10D |
| **RASN** | β | 0,3,4 | 7 | 10D |
| **PMIM** | β | 0,3,4,5 | 9 | 11D |
| **OII** | β | 0,3,4 | 7 | 10D |
| **HCMC** | β | 3 | 4 | 11D |
| **RIRI** | β | 4 | 1 | 10D |
| **MSPBA** | β | 0,1,3,4,5 | 10 | 12D |
| **VRIAP** | β | 0,3,4 | 6 | 11D |
| **TPRD** | β | 0,3,4,5,6 | 8 | 10D |
| **CMAPCC** | β | 0,1,3,4 | 8 | 11D |
| **DMMS** | γ | 0,3,4 | 6 | 10D |
| **CDEM** | γ | 0,3,4 | 6 | 11D |

**Not using A**: CSSL uses [3] only (stumpf_fusion for binding) — counted above.
IMU-β5-RIRI: minimal [4] only.

**IMU consonance role**: Memory valence encoding. Roughness = valence proxy (inverse). Stumpf = binding coherence. Pleasantness = encoding reward. Long horizons (H16–H24) dominate — memory operates on slow timescales.

### RPU — Reward Processing Unit (10/10)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **DAED** | α | 0,4 | 4 | 8D |
| **MORMR** | α | 0,4 | 5 | 7D |
| **RPEM** | α | 0,4 | 4 | 8D |
| **IUCP** | β | 0,4 | 4 | 6D |
| **MCCN** | β | 0 | 2 | 7D |
| **MEAMR** | β | 4 | 2 | 6D |
| **SSRI** | β | 0,4 | 3 | 11D |
| **LDAC** | γ | 0,4 | 5 | 6D |
| **IOTMS** | γ | 0,4 | 5 | 5D |
| **SSPS** | γ | 0,4 | 4 | 6D |

**RPU consonance role**: Dopamine modulation. Roughness = tension/displeasure signal. Pleasantness = hedonic reward. Medium horizons (H3–H16) — reward reacts to moment-to-moment changes.

### ARU — Affective Response Unit (8/10)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **SRP** | α | 0,1,2,3,4,5,6 (all 7) | R³ direct | 12D |
| **PUPF** | β | 0,4,6 | R³ direct | 10D |
| **CLAM** | β | 0,4 | R³ direct | 10D |
| **MAD** | β | 0,4 | R³ direct | 9D |
| **NEMAC** | β | 0,4 | R³ direct | 10D |
| **DAP** | γ | 0,4 | R³ direct | 8D |
| **CMAT** | γ | 0,4 | R³ direct | 8D |
| **TAR** | γ | 0,4 | R³ direct | 8D |

**Not using A**: AAC, VMM — no consonance references.

**ARU consonance role**: Affective valence. SRP uses ALL 7 features for opioid proxy, wanting/liking. Others use roughness (inverse valence) + pleasantness (direct hedonic). Most ARU models consume consonance via R³ directly rather than H³ — instantaneous affect.

### PCU — Predictive Coding Unit (7/10)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **SPH** | α | 4 | 2 | 11D |
| **ICEM** | α | 4 | 2 | 10D |
| **PWUP** | β | 4 | 3 | 10D |
| **UDP** | β | 4 | 3 | 9D |
| **CHPI** | β | 0,4 | 5 | 11D |
| **MAA** | γ | 0,4 | 5 | 9D |
| **PSH** | γ | 4 | 1 | 8D |

**Not using A**: HTP (α, uses B/D/F/H only), WMED, IGFE.

**PCU consonance role**: Prediction precision modulation. Sensory_pleasantness = consonance quality for prediction confidence. CHPI/MAA add roughness as tension signal. Entropy (M20) morphology common — predictability of consonance.

### ASU — Attentional Salience Unit (4/9)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **IACM** | α | 0 | 2 | 11D |
| **CSG** | α | 0,1,4 | 9 | 12D |
| **AACM** | β | 0 | 2 | 10D |
| **PWSM** | γ | 4 | ref only | 9D |

**Not using A**: SNEM, BARM, STANM, DGTP, SDL — temporal/energy focus.

**ASU consonance role**: Salience gradient. CSG = consonance-salience gradient (ana model). Roughness + pleasantness drive attentional capture via H³ change detection.

### NDU — Novelty Detection Unit (3/9)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **SDD** | α | 0 | 2 | 10D |
| **EDNR** | α | 4 | 2 | 9D |
| **MPG** | α | ref only | 0 | 11D |

**Not using A**: DSP, CDMR, SLEE, SDDP, ONI, ECT.

**NDU consonance role**: Surprise detection. Roughness entropy (M20) for spectral unpredictability. Pleasantness for novelty-reward coupling.

### STU — Structural Temporal Unit (1/14)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **MDNS** | α | 2 | 1 | 10D |

**Not using A**: HMCE, AMSC, AMSS, TPIO, EDTA, ETAM, HGSIC, OMS, TMRM, NEWMD, MTNE, PTGMP, MPFS.

**STU consonance role**: Minimal. Only MDNS uses helmholtz for interval quality. STU focuses on temporal structure, not spectral quality.

### MPU — Motor Planning Unit (1/10)

| Model | Tier | A[0:6] Used | H³ Tuples (A only) | Output |
|-------|------|-------------|---------------------|--------|
| **NSCP** | γ | 3 | 1 | 9D |

**Not using A**: PEOM, MSR, GSSM, ASAP, DDSMI, VRMSME, SPMC, CTBB, STC.

**MPU consonance role**: Minimal. NSCP uses stumpf for motor consonance coupling. Motor planning is rhythm-driven, not consonance-driven.

---

## 4. Feature Usage Statistics

### Per-Feature Consumption

| R³ Idx | Feature | Models (H³) | Models (ref) | Total | Primary Users |
|--------|---------|-------------|-------------|-------|---------------|
| **0** | roughness | 38 | 8 (ARU) | **46** | IMU, RPU, SPU |
| **1** | sethares_dissonance | 4 | 1 | **5** | CSG, SDED, MSPBA, CMAPCC |
| **2** | helmholtz_kang | 7 | 1 | **8** | BCH, STAI, SDNPS, PCCR, PNH |
| **3** | stumpf_fusion | 19 | 1 | **20** | IMU (binding), BCH, TPRD |
| **4** | sensory_pleasantness | 38 | 8 (ARU) | **46** | IMU, RPU, PCU |
| **5** | inharmonicity | 11 | 1 | **12** | SPU (pitch/timbre), IMU |
| **6** | harmonic_deviation | 3 | 2 | **5** | BCH, TPRD, PNH, PUPF |

### Dominant Pair: roughness[0] + pleasantness[4]

Bu ikili **46 model** tarafından kullanılır — tüm consonance branch'in %75'i.
- roughness: inverse valence, tension, dissonance
- pleasantness: direct hedonic, reward, comfort

### Secondary Features

- **stumpf_fusion[3]**: 20 model — IMU'da "binding coherence" olarak kritik
- **inharmonicity[5]**: 12 model — SPU'da instrument/pitch identity
- **helmholtz_kang[2]**: 8 model — SPU'da harmonic template matching
- **sethares[1], harmonic_dev[6]**: 5 model — niche uses

---

## 5. H³ Temporal Scale Distribution

### Per-Feature Horizon Patterns

```
roughness[0]:
  Fast   H0–H3 (25–100ms)  : BCH, STAI, SDNPS, SDED, CSG, DAED, MORMR, RPEM, IACM, AACM, PCCR, SDD
  Medium H6–H8 (200–500ms) : BCH, SDNPS, DAED, IUCP, MCCN, SSPS, IOTMS, SSRI
  Chord  H10–H14 (400–700ms): TPRD, PNH, PMIM, MSPBA
  Slow   H16–H24 (1–36s)   : MEAMN, MMP, RASN, OII, VRIAP, CMAPCC, DMMS, CDEM, MORMR, CSG, AACM, MAA

stumpf_fusion[3]:
  Fast   H0–H6 (25–200ms)  : BCH, TPRD, NSCP
  Chord  H10–H14 (400–700ms): PNH, PMIM, MSPBA, OII
  Slow   H16–H24 (1–36s)   : MEAMN, RASN, HCMC, CMAPCC, DMMS, CSSL, CDEM, VRIAP, MMP

sensory_pleasantness[4]:
  Fast   H3 (100ms)         : STAI, CSG, RPEM, LDAC, PSCL, SPH, ICEM, PWUP, UDP, CHPI, MAA
  Medium H8 (500ms)         : IOTMS, SSPS, MEAMR, SSRI, LDAC, ICEM
  Chord  H10 (400ms)        : PNH, PMIM
  Slow   H16–H24 (1–36s)   : MEAMN, MMP, RASN, OII, VRIAP, CMAPCC, DMMS, CDEM, + RPU, PCU
```

### Temporal Layering Pattern

```
SPU: Fast (H0–H6)  — Sensory detection, brainstem
RPU: Medium (H3–H16) — Moment-to-moment reward
ASU: Mixed (H0–H16) — Salience + attention
IMU: Slow (H10–H24) — Memory encoding, consolidation
PCU: Medium (H3–H16) — Prediction precision
NDU: Fast (H3) — Surprise/novelty
```

---

## 6. Cross-Unit Dependency Graph

```
R³ Group A [0:7]
    │
    ├──→ H³ temporal analysis (unique tuples ~80)
    │       │
    │       └──→ All 62 models receive H³ features
    │
    ├──────────────────────────────────────────────────────────────────────┐
    ↓                                                                     ↓
SPU (9 models)                                                   ARU (8 models)
    │ BCH.hierarchy → consonance belief                          │ SRP uses all 7
    │ BCH.consonance_signal → consonance belief                  │ direct R³
    │ BCH.template_match → consonance belief                     │ reward compute
    │                                                            │
    ├──→ PSCL.salience → STU.HMCE                               ├──→ Reward belief
    ├──→ PCCR.chroma → IMU.MEAMN                                ├──→ HYBRID output
    ├──→ STAI.aesthetic → ARU.SRP                                └──→ DA modulation
    │
    ↓
RPU (10 models)                     PCU (7 models)
    │ DAED.wanting/liking           │ CHPI/MAA tension+consonance
    │ → consonance belief           │ → precision engine
    │ (DA modulation)               │ → prediction quality
    │                               │
    ↓                               ↓
IMU (14 models)                 ASU (4 models)
    │ MEAMN.memory/emotion      │ CSG consonance-salience gradient
    │ → familiarity belief      │ → salience belief
    │ → reward (emotion mod)    │
    │                           ↓
    ↓                       NDU (3 models)    STU (1)    MPU (1)
Familiarity belief          │ SDD surprise    MDNS       NSCP
                            │ → salience
```

### Critical Pathways

1. **Consonance → Belief**: R³[0:7] → BCH → consonance belief (SPU primary pathway)
2. **Consonance → Reward**: R³[0,4] → RPU.DAED → DA gain → reward formula
3. **Consonance → Memory**: R³[0,3,4] → IMU.MEAMN → familiarity → reward (inverted-U)
4. **Consonance → Salience**: R³[0,4] → ASU.CSG → salience belief → reward gating
5. **Consonance → Prediction**: R³[4] → PCU → precision engine → Bayesian gain

---

## 7. Implementation Priority

### Phase 1 — Core Pipeline (α models)

```
R³ Group A → H³ (core tuples) → BCH → Consonance Belief
                                       ↓
                              DAED → DA gain
                              MEAMN → Familiarity (partial)
                              CSG → Salience (partial)
                                       ↓
                              Reward
```

**Required models**: BCH, DAED, MEAMN, CSG, SRP
**Required H³ tuples**: ~40 (core α models only)

### Phase 2 — Extended Pipeline (β models)

**Additional models**: STAI, PSCL, PCCR, TSCP, IUCP, MORMR, RPEM, MCCN, SSRI, MEAMR, RASN, PMIM, OII, HCMC, MSPBA, TPRD, CHPI, PWUP, SPH

### Phase 3 — Full Branch (γ models)

**Remaining**: SDNPS, ESME, SDED, LDAC, IOTMS, SSPS, DMMS, CSSL, CDEM, CMAPCC, VRIAP, RIRI, MAA, PSH, AACM, PWSM, SDD, EDNR, MDNS, NSCP, DAP, CMAT, TAR, PUPF, CLAM, MAD, NEMAC

---

## 8. Test Plan

### Branch Verification

1. **R³ Unit Test**: Group A 7D output, audio vs mel-fallback consistency
2. **H³ Unit Test**: All ~80 unique consonance tuples produce valid morphologies
3. **Integration Test**: R³→H³→BCH→Consonance belief produces valid [0,1] values
4. **Cross-Unit Test**: BCH output flows correctly to DAED, MEAMN, CSG, SRP
5. **Reward Test**: Consonance-driven reward is positive for consonant music, lower for dissonant
6. **Regression Test**: Swan Lake, Bach, Herald — compare against Alpha-Test v3.1 baselines

### Success Criteria

- 0 NaN in full pipeline
- Consonance belief range: min variance > 0.01 (not collapsed)
- BCH hierarchy: P1 > P5 > P4 > M3 > m6 > TT ordering preserved
- Reward: 100% positive frames (matching v3.1 baseline)
