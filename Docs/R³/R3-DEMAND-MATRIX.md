# R³ Talep Matrisi — Bottom-Up Model Demand Analysis

> **Phase**: 3A-1 (Chat R1)
> **Scope**: 96 C³ models across 9 units
> **Sources**: 7 R³ Gap Logs, R3-Usage.md (94-model matrix), 5 R³ code files, 96 model docs (Section 4)
> **Created**: 2026-02-13
> **Status**: DRAFT — awaiting Chat R2 (top-down DSP) and Chat R3 (synthesis)

---

## Bölüm 1: Konsolide Gap Tablosu

All gaps from 7 unit-level R³ gap logs, categorized by type:

- **ACOUSTIC**: Genuine missing spectral/acoustic feature that could be added to R³
- **NAMING**: Project-wide doc-vs-code naming mismatch (indices correct, names differ)
- **NEURAL**: Brain-level metric (EEG, fMRI, connectivity) — NOT an acoustic feature
- **ARCH**: Architectural concern (multi-track, participant-level, etc.)

### 1.1 ACOUSTIC Gaps (Missing R³ Features)

| # | Gap ID | Unit | Source Model(s) | Proposed Feature | Evidence | Severity | Proposed Group |
|---|--------|------|-----------------|------------------|----------|----------|----------------|
| 1 | IMU-MEAMN-1 | IMU | MEAMN | nostalgia_acoustic_signature | Sakakibara 2025 r=0.985-0.995 | Minor | — (composite) |
| 2 | IMU-MEAMN-2 | IMU | MEAMN | tonal_space_trajectory | Janata 2009 MPFC toroidal tracking | Minor | H: Harmony |
| 3 | IMU-MMP-1 | IMU | MMP | arousal_potential (calm/energetic) | Scarratt 2025 N=57 fMRI | Minor | — (composite of B) |
| 4 | IMU-RASN-1 | IMU | RASN | metricality_index | Grahn & Brett 2007 N=27 fMRI | Minor | G: Rhythm |
| 5 | IMU-PMIM-1 | IMU | PMIM, HCMC, MSPBA | predictive_entropy (chord-level) | Cheung 2019, Gold 2019/2023 | Minor | I: Information |
| 6 | IMU-TPRD-1 | IMU | TPRD | pitch_chroma (cyclical) | Briley 2013 EEG adaptation | Minor | F: Pitch |
| 7 | IMU-TPRD-2 | IMU | TPRD | harmonic_resolvability | Norman-Haignere 2013 | Minor | F: Pitch |
| 8 | IMU-DMMS-1 | IMU | DMMS | melodic_contour_direction | Sena Moore 2025 MCRF | Minor | F: Pitch |
| 9 | IMU-CSSL-1 | IMU | CSSL | isochrony_nPVI | Burchardt 2025, Ravignani 2021 | Minor | G: Rhythm |
| 10 | IMU-RIRI-1 | IMU | RIRI | groove_index | Li 2025 locomotion biomechanics | Minor | G: Rhythm |
| 11 | IMU-VRIAP-1 | IMU | VRIAP | relaxation_index (composite) | Arican & Soyman 2025 tau=-0.536 | Minor | — (composite of B,C) |
| 12 | ASU-G04 | ASU | IACM | inharmonicity_index | Basinski 2025 ApEn 0.02 vs 0.19 | Medium | F: Pitch |
| 13 | ASU-G05 | ASU | CSG | consonance_gradient | Fishman, Bravo 2017 d=5.16 | Low | — (covered by A) |
| 14 | NDU-001 | NDU | SDD, CDMR | syntactic_irregularity_level | Kim 2021 MEG F(2,36)=6.526 | Medium | H: Harmony |
| 15 | NDU-002 | NDU | SDD | perceptual_ambiguity_level | Kim 2021 MEG F(2,36)=12.373 | Medium | H: Harmony |
| 16 | NDU-003 | NDU | CDMR, SLEE | cortical_entrainment_index | Bridwell 2017 r=0.65 | Low | — (may be H³) |
| 17 | NDU-004 | NDU | CDMR, EDNR | perceived_musical_roundness | Wöhrle 2024 η²p=0.592 | Low | H: Harmony |
| 18 | MPU-1 | MPU | PEOM | syncopation_index | Grahn & Brett 2007; Witek 2014 | Medium | G: Rhythm |
| 19 | MPU-2 | MPU | PEOM | metrical_structure_complexity | Grahn & Brett 2007 | Medium | G: Rhythm |
| 20 | MPU-6 | MPU | GSSM | locomotion_periodicity (0.5-2 Hz) | Yamashita 2025 stride time CV | Medium | G: Rhythm |
| 21 | PCU-PWUP-1 | PCU | PWUP | R³[14] tonalness→brightness_kuttruff | Index mismatch | Medium | — (remap) |
| 22 | PCU-PWUP-2 | PCU | PWUP, UDP | R³[5] periodicity→roughness_total | No periodicity in 49D | Medium | F: Pitch |
| 23 | PCU-UDP-1 | PCU | UDP | 1/f_spectral_slope | Borges 2019 1/f scaling | Minor | H: Harmony |
| 24 | PCU-UDP-2 | PCU | UDP | key_clarity / tonal_stability | Mencke 2019 d=3.0 | Minor | H: Harmony |
| 25 | RPU-001a | RPU | SSRI | onset_synchrony_quality | Bigand 2025, Kokal 2011 | Medium | — (multi-track) |
| 26 | RPU-001b | RPU | SSRI | timbral_blend_index | Bigand 2025 | Medium | — (multi-track) |
| 27 | RPU-001c | RPU | SSRI | rhythmic_entrainment_index | Ni 2024, Kokal 2011 | Medium | — (multi-track) |
| 28 | RPU-002a | RPU | SSRI, IUCP | rhythmic_information_content | Spiech 2022, Gold 2019 | Med-high | I: Information |
| 29 | RPU-002b | RPU | SSRI, IUCP | rhythmic_entropy | Spiech 2022, Cheung 2019 | Med-high | I: Information |
| 30 | RPU-004a | RPU | LDAC, IUCP, RPEM | melodic_entropy | Gold 2019b R²=0.496, Cheung 2019 | Med-high | I: Information |
| 31 | RPU-004b | RPU | LDAC | harmonic_entropy | Gold 2019b, Cheung 2019 | Med-high | I: Information |

**Total ACOUSTIC gaps: 31** (10 Minor, 12 Medium, 5 Medium-high, 3 Low, 1 covered)

### 1.2 NAMING Gaps (Doc-vs-Code Mismatch — Phase 5)

Project-wide naming convention: docs use semantic labels, code uses computational names. **All index ranges are correct.**

| R³ Index | Doc Label | Code Name | Affected Units |
|----------|-----------|-----------|----------------|
| [0] | roughness | perfect_fifth_ratio | PCU (CHPI), ASU (AACM) |
| [5] | periodicity | roughness_total | PCU (PWUP, UDP, CHPI), IMU (RASN) |
| [6] | harmonic_change | consonance_mean | PCU (CHPI) |
| [7] | amplitude | velocity_A | ASU (BARM, DGTP, SDL, AACM) |
| [8] | loudness | velocity_D | ASU (BARM, STANM, DGTP, SDL, AACM) |
| [9] | spectral_centroid | loudness | PCU (CHPI) |
| [10] | spectral_flux | onset_strength | ASU (BARM, STANM, PWSM, DGTP, SDL), PCU (UDP, CHPI) |
| [11] | onset_strength | rms_energy | ASU (BARM, PWSM, DGTP) |
| [13] | tristimulus_1 | sharpness | ASU (AACM) |
| [14] | tonalness | brightness_kuttruff | ASU (STANM), PCU (PWUP, UDP, CHPI) |
| [18] | pitch_salience | tristimulus3 | ASU (SDL) |
| [21] | spectral_change | spectral_flux | ASU (all 9), PCU (UDP, CHPI) |
| [22] | energy_change | spectral_flatness | ASU (BARM, STANM, PWSM), PCU (CHPI) |
| [23] | timbre_change / roughness_change | zero_crossing_rate | ASU (PWSM), PCU (CHPI) |
| [24] | pitch_change | tonalness | ASU (PWSM, DGTP) |

**Total NAMING entries: ~64** (concentrated in ASU 50+ and PCU 9+)
**Resolution**: Phase 5 doc-code reconciliation. No R³ expansion needed.

### 1.3 NEURAL Gaps (Not R³-Level)

| # | Unit | Source Model(s) | Feature | Why Not R³ |
|---|------|-----------------|---------|------------|
| 1 | IMU | RASN | neural_entrainment_strength | Brain-side EEG ITPC, not acoustic |
| 2 | IMU | HCMC, OII | theta-gamma PAC | Neural binding mechanism |
| 3 | IMU | HCMC | replay_detection | Stochastic neural event |
| 4 | IMU | MMP | grey_matter_density | Participant-level structural |
| 5 | IMU | CMAPCC | white_matter_integrity | Participant-level structural |
| 6 | IMU | CMAPCC | mu_suppression_index | Neural response metric |
| 7 | IMU | DMMS | dopaminergic_signaling | Neurochemical process |
| 8 | IMU | CSSL | corollary_discharge | Motor-auditory feedback |
| 9 | ASU | SNEM | neural_entrainment_ITPC | Brain-side phase coherence |
| 10 | ASU | SNEM | phase_locking_value | Inter-region connectivity |
| 11 | ASU | IACM | high_gamma_power_STG | Neural response metric |
| 12 | MPU | PEOM | phase-amplitude_coupling | Neural oscillatory mechanism |
| 13 | MPU | MSR | high_frequency_PLV | Neural synchrony metric |
| 14 | MPU | MSR | P2_amplitude_novelty | ERP component |
| 15 | MPU | GSSM | stimulation_phase_coupling | Neuromodulation parameter |
| 16 | RPU | SSRI, DAED | auditory-reward_connectivity | Neural state variable |
| 17 | RPU | LDAC | bilateral_AC_lateralization | Architectural concern |

**Total NEURAL gaps: 17** — correctly excluded from R³. Handled by C³ mechanisms (BEP, MEM, SYN) or participant-level variables.

### 1.4 Summary by Unit

| Unit | ACOUSTIC | NAMING | NEURAL | Total |
|------|----------|--------|--------|-------|
| SPU | 0 | 0 | 0 | 0 |
| STU | 0 | 0 | 0 | 0 |
| IMU | 11 | 0 | 8 | 19 |
| ASU | 2 | ~50 | 3 | ~55 |
| NDU | 4 | 0 | 0 | 4 |
| MPU | 3 | 0 | 4 | 7 |
| PCU | 4 | ~9 | 0 | ~13 |
| ARU | 0 | 0 | 0 | 0 |
| RPU | 7 | 0 | 2 | 9 |
| **Total** | **31** | **~59** | **17** | **~107** |

---

## Bölüm 2: Birim Bazlı Talep Özeti

### 2.1 SPU — Spectral Processing Unit (9 models)

**Mevcut R³ Profili**: A:Consonance (dominant, 8/9) + C:Timbre (primary, 5/9)
**Eksik Boyut Talebi**: Yok — SPU mevcut 49D R³ ile tam örtüşüyor.
**Yeni Grup Talebi**:
- F:Pitch → **Yüksek**. SPU'nun çekirdek alanı pitch işleme. Mevcut Consonance grubundaki roughness/harmonicity indirekt proxy. Dedike pitch_chroma, pitch_salience, harmonic_resolvability SPU modellerinin (PSCL, PCCR, TPRD) doğrudan kullanacağı boyutlar.
- G:Rhythm → Düşük. SPU temporal yapı işlemiyor.
- H:Harmony → Orta. BCH, STAI harmonik yapıdan faydalanır.
- I:Information → Düşük. SPU bilgi-teorik özellikler kullanmıyor.

### 2.2 STU — Sensorimotor Timing Unit (14 models)

**Mevcut R³ Profili**: B:Energy (dominant, 13/14) + D:Change (primary, 10/14)
**Eksik Boyut Talebi**: Doğrudan gap log'da belirtilmemiş ama G:Rhythm grubundan en çok faydalanacak birim.
**Yeni Grup Talebi**:
- F:Pitch → Düşük. Sadece MDNS melodic decoding için kullanır.
- G:Rhythm → **Çok Yüksek**. 14 modelden ~12'si syncopation, metricality, isochrony, groove özelliklerinden faydalanır. STU'nun beat/tempo/ritim işleme alanı G grubunun birincil tüketicisi olacak.
- H:Harmony → Düşük. STU harmonik yapı işlemiyor.
- I:Information → Düşük-Orta. HGSIC ve ETAM ritimik bilgi-içeriğinden faydalanabilir.

### 2.3 IMU — Integrative Memory Unit (15 models)

**Mevcut R³ Profili**: Tüm gruplardan yaygın tüketim (en geniş dağılımlı bağımsız birim)
**Eksik Boyut Talebi**: 11 ACOUSTIC gap — en fazla eksik boyut talebi olan birim.
**Yeni Grup Talebi**:
- F:Pitch → Orta. TPRD (pitch_chroma, harmonic_resolvability), DMMS (melodic_contour), PNH (Pythagorean hierarchy).
- G:Rhythm → Orta. RASN (metricality), RIRI (groove, isochrony), CSSL (isochrony_nPVI).
- H:Harmony → Orta-Yüksek. MSPBA (syntactic_irregularity), MEAMN (tonal_space), PNH.
- I:Information → **Yüksek**. PMIM, HCMC, MSPBA hepsi predictive_entropy ve information_content'den faydalanır.

### 2.4 ASU — Auditory Salience Unit (9 models)

**Mevcut R³ Profili**: B:Energy (primary, 8/9) + C:Timbre (primary, 7/9)
**Eksik Boyut Talebi**: 2 ACOUSTIC gap (inharmonicity_index, consonance_gradient) + ~50 NAMING mismatch
**Yeni Grup Talebi**:
- F:Pitch → Orta. IACM (inharmonicity_index), CSG (consonance_gradient).
- G:Rhythm → Düşük-Orta. SNEM, BARM, DGTP beat-salience işler ama mevcut B grubu yeterli.
- H:Harmony → Düşük.
- I:Information → Düşük.

### 2.5 NDU — Novelty Detection Unit (9 models)

**Mevcut R³ Profili**: D:Change (dominant, 9/9) + E:Interactions (primary, 7/9)
**Eksik Boyut Talebi**: 4 ACOUSTIC gap — syntactic_irregularity, perceptual_ambiguity, musical_roundness, entrainment_index
**Yeni Grup Talebi**:
- F:Pitch → Düşük. Sadece SDD pitch deviance.
- G:Rhythm → Düşük. NDU ritimik yapı değil sapma işler.
- H:Harmony → **Yüksek**. SDD, CDMR, SLEE, EDNR harmonik syntax sapması/bütünlük tespiti yapıyor.
- I:Information → Orta-Yüksek. SDD, CDMR, SLEE predictive surprise/entropy kullanabilir.

### 2.6 MPU — Motor Planning Unit (10 models)

**Mevcut R³ Profili**: B:Energy (dominant, 10/10) + D:Change (primary, 8/10)
**Eksik Boyut Talebi**: 3 ACOUSTIC gap — syncopation, metrical_complexity, locomotion_periodicity
**Yeni Grup Talebi**:
- F:Pitch → Düşük.
- G:Rhythm → **Çok Yüksek**. PEOM (syncopation, metricality), GSSM (locomotion_periodicity, groove), MSR, ASAP, DDSMI, SPMC, STC hepsi ritmik yapı kullanıyor.
- H:Harmony → Düşük.
- I:Information → Düşük.

### 2.7 PCU — Predictive Coding Unit (10 models, incl. CHPI)

**Mevcut R³ Profili**: A:Consonance (primary, 7/9) + E:Interactions (primary, 7/9) + C:Timbre (substantial, 5/9)
**Eksik Boyut Talebi**: 4 ACOUSTIC gap — periodicity, 1/f slope, key_clarity, index remapping
**Yeni Grup Talebi**:
- F:Pitch → Orta. SPH (pitch height), CHPI (cross-modal harmonic).
- G:Rhythm → Düşük.
- H:Harmony → Orta-Yüksek. UDP (key_clarity, 1/f slope), HTP, ICEM, CHPI harmonik öngörü yapıyor.
- I:Information → **Yüksek**. UDP, HTP, ICEM, WMED, CHPI hepsi predictive uncertainty/entropy'den faydalanır. PCU'nun çekirdek işlevi öngörü hatası — bilgi-teorik boyutlar kritik.

### 2.8 ARU — Affective Resonance Unit (10 models)

**Mevcut R³ Profili**: Tüm gruplardan yaygın tüketim (cross-unit pathway'ler aracılığıyla)
**Eksik Boyut Talebi**: 0 ACOUSTIC gap — ARU mevcut 49D ile tam örtüşüyor.
**Yeni Grup Talebi**:
- Tüm yeni gruplardan dolaylı faydalanma. ARU bağımlı birim (P1, P3, P5 pathway). Yeni R³ boyutları otomatik olarak ARU'ya akacak.
- I:Information → Orta. PUPF prediction-uncertainty-pleasure coupling.

### 2.9 RPU — Reward Processing Unit (10 models, incl. SSRI)

**Mevcut R³ Profili**: A:Consonance (8/9) + B:Energy (8/9) + E:Interactions (8/9)
**Eksik Boyut Talebi**: 7 ACOUSTIC gap — social synchrony (3), rhythmic IC/entropy (2), melodic/harmonic entropy (2)
**Yeni Grup Talebi**:
- F:Pitch → Düşük.
- G:Rhythm → Orta. SSRI (rhythmic_entrainment), IUCP (complexity), IOTMS (tempo).
- H:Harmony → Orta. RPEM, LDAC, SSPS, MCCN harmonik öngörü hatası/ödül.
- I:Information → **Çok Yüksek**. LDAC (melodic_entropy), IUCP (rhythmic_IC × entropy), RPEM (prediction error), SSRI (rhythmic IC), SSPS (IC × entropy saddle surface), MCCN. RPU'nun ödül hesaplaması bilgi-teorik değişkenlere kritik bağımlı.

---

## Bölüm 3: Feature Talep Sıralaması

Tüm gap log'lar ve model doc Section 4 analizlerinden derlenen eksik boyut talepleri, talep eden model sayısına göre sıralanmış:

### 3.1 Tier 1 — Yüksek Talep (≥10 model)

| Sıra | Önerilen Feature | Grup | Talep Eden Modeller | Model Sayısı | Öncelik |
|------|------------------|------|---------------------|:---:|---------|
| 1 | **melodic_entropy** (pitch transition uncertainty) | I | LDAC, IUCP, RPEM, SSPS, MCCN, SSRI, UDP, HTP, ICEM, WMED, CHPI, PMIM, HCMC, MSPBA, SDD, CDMR, SLEE, PUPF | 18 | Med-high |
| 2 | **syncopation_index** (beat offset from metrical grid) | G | PEOM, MSR, GSSM, ASAP, DDSMI, SPMC, STC, HMCE, AMSC, EDTA, ETAM, HGSIC, OMS, RASN, RIRI, SNEM, BARM | 17 | Medium |
| 3 | **metricality_index** (integer-ratio regularity) | G | PEOM, GSSM, ASAP, SPMC, STC, HMCE, AMSC, EDTA, ETAM, OMS, RASN, SNEM, BARM, DGTP | 14 | Medium |
| 4 | **harmonic_entropy** (chord transition uncertainty) | I | LDAC, IUCP, SSPS, MCCN, UDP, HTP, ICEM, CHPI, MSPBA, PMIM, HCMC, SDD, CDMR | 13 | Med-high |

### 3.2 Tier 2 — Orta Talep (5-9 model)

| Sıra | Önerilen Feature | Grup | Talep Eden Modeller | Model Sayısı | Öncelik |
|------|------------------|------|---------------------|:---:|---------|
| 5 | **rhythmic_information_content** | I | SSRI, IUCP, LDAC, RPEM, SSPS, PEOM, GSSM, HGSIC | 8 | Med-high |
| 6 | **groove_index** (movement-inducing quality) | G | RIRI, GSSM, HGSIC, MPFS, ETAM, OMS, SSRI | 7 | Minor |
| 7 | **syntactic_irregularity** (harmonic violation degree) | H | SDD, CDMR, SLEE, MSPBA, PMIM | 5 | Medium |
| 8 | **pitch_chroma** (cyclical octave-equivalence) | F | TPRD, PCCR, PSCL, MDNS, MEAMN | 5 | Minor |
| 9 | **tonal_stability** / key_clarity | H | UDP, MEAMN, STAI, CHPI, SLEE | 5 | Minor |
| 10 | **isochrony_nPVI** (rhythmic regularity) | G | CSSL, RIRI, RASN, OMS, AMSC | 5 | Minor |

### 3.3 Tier 3 — Düşük Talep (2-4 model)

| Sıra | Önerilen Feature | Grup | Talep Eden Modeller | Model Sayısı | Öncelik |
|------|------------------|------|---------------------|:---:|---------|
| 11 | **melodic_contour_direction** | F | DMMS, CSSL, MDNS | 3 | Minor |
| 12 | **harmonic_resolution_potential** | H | CDMR, EDNR, MSPBA | 3 | Low |
| 13 | **inharmonicity_index** (explicit) | F | IACM, PNH | 2 | Medium |
| 14 | **harmonic_resolvability** | F | TPRD, PNH | 2 | Minor |
| 15 | **rhythmic_entropy** | I | SSRI, IUCP | 2 | Med-high |

### 3.4 Tier 4 — Tekil Talep (1 model) veya Özel Gereksinim

| Sıra | Önerilen Feature | Grup | Talep Eden Model | Öncelik | Not |
|------|------------------|------|------------------|---------|-----|
| 16 | **perceptual_ambiguity_level** | H | SDD | Medium | Mevcut spectral özelliklerden türetilebilir |
| 17 | **1/f_spectral_slope** | H | UDP | Minor | Audio 1/f ≠ neural 1/f |
| 18 | **locomotion_periodicity** (0.5-2 Hz) | G | GSSM | Medium | ÖNERİ: energy envelope autocorrelation |
| 19 | **onset_synchrony_quality** | — | SSRI | Medium | Multi-track gerektirir |
| 20 | **timbral_blend_index** | — | SSRI | Medium | Multi-track gerektirir |
| 21 | **rhythmic_entrainment_index** | — | SSRI | Medium | Multi-track gerektirir |
| 22 | **nostalgia_acoustic_signature** | — | MEAMN | Minor | CNN-embedding proxy, R³ scope dışı |
| 23 | **arousal_potential** (composite) | — | MMP, VRIAP | Minor | ÖNERİ: B grubu composite'i |

### 3.5 Talep Dağılımı Özeti

```
               Model Sayısı
melodic_entropy    ████████████████████ 18
syncopation_index  ███████████████████  17
metricality_index  ████████████████     14
harmonic_entropy   ███████████████      13
rhythmic_IC        ██████████           8
groove_index       █████████            7
syntactic_irreg    ███████              5
pitch_chroma       ███████              5
tonal_stability    ███████              5
isochrony_nPVI     ███████              5
contour_direction  █████                3
resolution_pot     █████                3
inharmonicity_idx  ████                 2
harm_resolvability ████                 2
rhythmic_entropy   ████                 2
```

---

## Bölüm 4: 96 Model × 5 Mevcut Grup Kullanım Matrisi

Kaynak: `Docs/C³/Matrices/R3-Usage.md` + CHPI (PCU-β4) ve SSRI (RPU-β4) eklemeleri.

### Gösterim
- **X** = Grup aktif olarak kullanılıyor
- **.** = Grup kullanılmıyor
- Yeni modeller (*) ile işaretli

### SPU (9 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 1 | BCH | α1 | X | . | . | . | . |
| 2 | PSCL | α2 | X | . | X | . | . |
| 3 | PCCR | α3 | X | . | . | . | . |
| 4 | STAI | β1 | X | . | X | . | X |
| 5 | TSCP | β2 | . | . | X | . | . |
| 6 | MIAA | β3 | X | . | X | . | . |
| 7 | SDNPS | γ1 | X | . | . | . | . |
| 8 | ESME | γ2 | X | . | X | . | . |
| 9 | SDED | γ3 | X | . | . | . | . |

### STU (14 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 10 | HMCE | α1 | . | X | . | X | . |
| 11 | AMSC | α2 | . | X | . | X | . |
| 12 | MDNS | α3 | X | X | . | . | . |
| 13 | AMSS | β1 | . | X | X | . | . |
| 14 | TPIO | β2 | . | . | X | . | . |
| 15 | EDTA | β3 | . | X | . | X | . |
| 16 | ETAM | β4 | . | X | . | X | . |
| 17 | HGSIC | β5 | . | X | . | X | X |
| 18 | OMS | β6 | . | X | . | X | . |
| 19 | TMRM | γ1 | . | X | . | X | . |
| 20 | NEWMD | γ2 | . | X | . | X | . |
| 21 | MTNE | γ3 | . | X | . | . | . |
| 22 | PTGMP | γ4 | . | X | . | . | . |
| 23 | MPFS | γ5 | . | X | . | X | . |

### IMU (15 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 24 | MEAMN | α1 | X | X | X | . | X |
| 25 | PNH | α2 | X | . | . | . | . |
| 26 | MMP | α3 | X | X | X | . | . |
| 27 | RASN | β1 | . | X | . | X | . |
| 28 | PMIM | β2 | X | X | . | X | X |
| 29 | OII | β3 | . | X | . | X | . |
| 30 | HCMC | β4 | X | X | X | . | X |
| 31 | RIRI | β5 | X | X | . | . | . |
| 32 | MSPBA | β6 | X | . | . | X | X |
| 33 | VRIAP | β7 | . | X | X | . | . |
| 34 | TPRD | β8 | X | . | X | . | . |
| 35 | CMAPCC | β9 | . | X | X | X | . |
| 36 | DMMS | γ1 | X | X | . | . | X |
| 37 | CSSL | γ2 | X | . | X | . | . |
| 38 | CDEM | γ3 | X | X | X | . | X |

### ASU (9 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 39 | SNEM | α1 | . | X | . | . | . |
| 40 | IACM | α2 | X | X | X | . | . |
| 41 | CSG | α3 | X | . | X | . | . |
| 42 | BARM | β1 | . | X | X | X | . |
| 43 | STANM | β2 | . | X | X | X | . |
| 44 | AACM | β3 | . | X | X | . | . |
| 45 | PWSM | γ1 | . | X | X | X | . |
| 46 | DGTP | γ2 | . | X | . | X | . |
| 47 | SDL | γ3 | . | X | X | . | . |

### NDU (9 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 48 | MPG | α1 | . | . | . | X | X |
| 49 | SDD | α2 | X | . | X | X | . |
| 50 | EDNR | α3 | . | X | . | X | X |
| 51 | DSP_ | β1 | . | . | . | X | X |
| 52 | CDMR | β2 | . | . | . | X | X |
| 53 | SLEE | β3 | X | . | . | X | X |
| 54 | SDDP | γ1 | . | . | X | X | . |
| 55 | ONI | γ2 | . | X | . | X | X |
| 56 | ECT | γ3 | . | . | . | X | X |

### MPU (10 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 57 | PEOM | α1 | . | X | . | X | . |
| 58 | MSR | α2 | . | X | . | X | . |
| 59 | GSSM | α3 | . | X | . | X | X |
| 60 | ASAP | β1 | . | X | . | X | . |
| 61 | DDSMI | β2 | . | X | . | X | . |
| 62 | VRMSME | β3 | . | X | . | . | . |
| 63 | SPMC | β4 | . | X | . | X | . |
| 64 | NSCP | γ1 | . | X | . | . | X |
| 65 | CTBB | γ2 | . | X | . | X | . |
| 66 | STC | γ3 | . | X | . | X | . |

### PCU (10 model, CHPI yeni*)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 67 | HTP | α1 | X | X | X | X | X |
| 68 | SPH | α2 | X | . | X | . | . |
| 69 | ICEM | α3 | X | X | . | . | X |
| 70 | PWUP | β1 | X | . | . | . | X |
| 71 | WMED | β2 | . | X | . | X | X |
| 72 | UDP | β3 | X | . | . | X | X |
| 73 | CHPI* | β4 | X | X | X | X | X |
| 74 | IGFE | γ1 | . | . | X | . | . |
| 75 | MAA | γ2 | X | X | X | . | X |
| 76 | PSH | γ3 | X | . | X | . | X |

### ARU (10 model)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 77 | SRP | α1 | X | X | X | X | X |
| 78 | AAC | α2 | X | X | X | X | X |
| 79 | VMM | α3 | X | X | X | . | X |
| 80 | PUPF | β1 | X | X | . | X | X |
| 81 | CLAM | β2 | . | X | . | X | . |
| 82 | MAD | β3 | X | X | X | . | X |
| 83 | NEMAC | β4 | X | X | X | . | X |
| 84 | DAP | γ1 | X | X | . | . | . |
| 85 | CMAT | γ2 | . | X | X | . | X |
| 86 | TAR | γ3 | . | X | X | . | . |

### RPU (10 model, SSRI yeni*)

| # | Model | Tier | A | B | C | D | E |
|---|-------|------|:-:|:-:|:-:|:-:|:-:|
| 87 | DAED | α1 | X | X | . | X | X |
| 88 | MORMR | α2 | X | X | X | . | X |
| 89 | RPEM | α3 | X | X | . | X | X |
| 90 | IUCP | β1 | X | . | . | X | X |
| 91 | MCCN | β2 | X | X | X | . | X |
| 92 | MEAMR | β3 | X | X | X | . | X |
| 93 | SSRI* | β4 | X | X | X | X | X |
| 94 | LDAC | γ1 | X | X | X | . | X |
| 95 | IOTMS | γ2 | . | X | . | X | . |
| 96 | SSPS | γ3 | X | X | X | . | X |

### Mevcut Grup Tüketim Özeti (96 model)

| R³ Grubu | Boyut | Kullanan Model | % |
|----------|-------|:-:|:-:|
| A: Consonance | 0-6 (7D) | 69 | 72% |
| B: Energy | 7-11 (5D) | 81 | 84% |
| C: Timbre | 12-20 (9D) | 55 | 57% |
| D: Change | 21-24 (4D) | 57 | 59% |
| E: Interactions | 25-48 (24D) | 54 | 56% |

---

## Bölüm 5: 96 Model × Önerilen Yeni Grup Talep Matrisi

### Önerilen Yeni Gruplar

| Grup | Etiket | Önerilen Boyut | Kaynak |
|------|--------|:-:|--------|
| F | Pitch | 5D | pitch_chroma, melodic_contour, harmonic_resolvability, inharmonicity_index, pitch_salience_F0 |
| G | Rhythm | 5D | syncopation_index, metricality_index, isochrony_nPVI, groove_index, locomotion_periodicity |
| H | Harmony | 5D | syntactic_irregularity, tonal_stability, harmonic_resolution_potential, perceptual_ambiguity, spectral_1f_slope |
| I | Information | 4D | melodic_entropy, harmonic_entropy, rhythmic_information_content, rhythmic_entropy |

**Toplam önerilen: 19D yeni boyut** (49D mevcut → 68D minimum genişleme)

### Gösterim
- **X** = Model bu gruptan doğrudan faydalanır (gap log veya Section 4 analizinden)
- **x** = Model dolaylı faydalanır (cross-unit pathway veya düşük öncelik)
- **.** = Talep yok

### SPU (9 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 1 | BCH | α1 | X | . | x | . |
| 2 | PSCL | α2 | X | . | . | . |
| 3 | PCCR | α3 | X | . | . | . |
| 4 | STAI | β1 | x | . | X | . |
| 5 | TSCP | β2 | . | . | . | . |
| 6 | MIAA | β3 | X | . | . | . |
| 7 | SDNPS | γ1 | X | . | . | . |
| 8 | ESME | γ2 | X | . | . | . |
| 9 | SDED | γ3 | x | . | . | . |

### STU (14 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 10 | HMCE | α1 | . | X | . | . |
| 11 | AMSC | α2 | . | X | . | . |
| 12 | MDNS | α3 | X | . | . | . |
| 13 | AMSS | β1 | . | x | . | . |
| 14 | TPIO | β2 | . | . | . | . |
| 15 | EDTA | β3 | . | X | . | . |
| 16 | ETAM | β4 | . | X | . | x |
| 17 | HGSIC | β5 | . | X | . | x |
| 18 | OMS | β6 | . | X | . | . |
| 19 | TMRM | γ1 | . | X | . | . |
| 20 | NEWMD | γ2 | . | X | . | . |
| 21 | MTNE | γ3 | . | x | . | . |
| 22 | PTGMP | γ4 | . | x | . | . |
| 23 | MPFS | γ5 | . | X | . | . |

### IMU (15 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 24 | MEAMN | α1 | x | . | X | . |
| 25 | PNH | α2 | X | . | x | . |
| 26 | MMP | α3 | . | . | . | . |
| 27 | RASN | β1 | . | X | . | . |
| 28 | PMIM | β2 | . | . | x | X |
| 29 | OII | β3 | . | . | . | . |
| 30 | HCMC | β4 | . | . | . | X |
| 31 | RIRI | β5 | . | X | . | . |
| 32 | MSPBA | β6 | . | . | X | X |
| 33 | VRIAP | β7 | . | . | . | . |
| 34 | TPRD | β8 | X | . | . | . |
| 35 | CMAPCC | β9 | . | . | . | . |
| 36 | DMMS | γ1 | X | . | . | . |
| 37 | CSSL | γ2 | . | X | . | . |
| 38 | CDEM | γ3 | . | . | . | . |

### ASU (9 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 39 | SNEM | α1 | . | X | . | . |
| 40 | IACM | α2 | X | . | . | . |
| 41 | CSG | α3 | x | . | . | . |
| 42 | BARM | β1 | . | X | . | . |
| 43 | STANM | β2 | . | . | . | . |
| 44 | AACM | β3 | . | . | . | . |
| 45 | PWSM | γ1 | . | . | . | . |
| 46 | DGTP | γ2 | . | X | . | . |
| 47 | SDL | γ3 | . | . | . | . |

### NDU (9 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 48 | MPG | α1 | . | . | . | x |
| 49 | SDD | α2 | x | . | X | X |
| 50 | EDNR | α3 | . | . | X | . |
| 51 | DSP_ | β1 | . | . | . | x |
| 52 | CDMR | β2 | . | . | X | X |
| 53 | SLEE | β3 | . | . | X | X |
| 54 | SDDP | γ1 | . | . | . | . |
| 55 | ONI | γ2 | . | . | . | . |
| 56 | ECT | γ3 | . | . | . | x |

### MPU (10 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 57 | PEOM | α1 | . | X | . | . |
| 58 | MSR | α2 | . | X | . | . |
| 59 | GSSM | α3 | . | X | . | . |
| 60 | ASAP | β1 | . | X | . | . |
| 61 | DDSMI | β2 | . | X | . | . |
| 62 | VRMSME | β3 | . | . | . | . |
| 63 | SPMC | β4 | . | X | . | . |
| 64 | NSCP | γ1 | . | x | . | . |
| 65 | CTBB | γ2 | . | X | . | . |
| 66 | STC | γ3 | . | X | . | . |

### PCU (10 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 67 | HTP | α1 | x | . | x | X |
| 68 | SPH | α2 | X | . | . | . |
| 69 | ICEM | α3 | . | . | . | X |
| 70 | PWUP | β1 | x | . | . | x |
| 71 | WMED | β2 | . | . | . | X |
| 72 | UDP | β3 | . | . | X | X |
| 73 | CHPI* | β4 | X | . | X | X |
| 74 | IGFE | γ1 | . | . | . | . |
| 75 | MAA | γ2 | . | . | . | . |
| 76 | PSH | γ3 | . | . | . | . |

### ARU (10 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 77 | SRP | α1 | x | x | x | x |
| 78 | AAC | α2 | x | x | x | x |
| 79 | VMM | α3 | x | . | x | . |
| 80 | PUPF | β1 | . | . | . | X |
| 81 | CLAM | β2 | . | . | . | . |
| 82 | MAD | β3 | . | . | . | . |
| 83 | NEMAC | β4 | . | . | . | . |
| 84 | DAP | γ1 | . | . | . | . |
| 85 | CMAT | γ2 | . | . | . | . |
| 86 | TAR | γ3 | . | . | . | . |

### RPU (10 model)

| # | Model | Tier | F:Pitch | G:Rhythm | H:Harmony | I:Info |
|---|-------|------|:-:|:-:|:-:|:-:|
| 87 | DAED | α1 | . | . | . | x |
| 88 | MORMR | α2 | . | . | x | . |
| 89 | RPEM | α3 | . | . | . | X |
| 90 | IUCP | β1 | . | x | . | X |
| 91 | MCCN | β2 | . | . | x | X |
| 92 | MEAMR | β3 | . | . | . | . |
| 93 | SSRI* | β4 | . | X | . | X |
| 94 | LDAC | γ1 | . | . | x | X |
| 95 | IOTMS | γ2 | . | x | . | . |
| 96 | SSPS | γ3 | . | . | x | X |

### Yeni Grup Talep Özeti

| Yeni Grup | Doğrudan (X) | Dolaylı (x) | Toplam | Birincil Birimler |
|-----------|:---:|:---:|:---:|-------------------|
| F: Pitch (5D) | 16 | 11 | 27 | SPU (7), IMU (3), PCU (2), ASU (2) |
| G: Rhythm (5D) | 25 | 8 | 33 | STU (10), MPU (9), IMU (3), ASU (3) |
| H: Harmony (5D) | 12 | 10 | 22 | NDU (4), PCU (3), IMU (2), RPU (4) |
| I: Information (4D) | 22 | 10 | 32 | RPU (6), PCU (5), IMU (3), NDU (3) |

---

## Bölüm 6: Sonuç ve Öneriler

### 6.1 Mevcut Durum Değerlendirmesi

Mevcut 49D R³ uzayı 96 modelin **%72-84'ünün** temel ihtiyaçlarını karşılamaktadır. Energy (B, 84%) en yaygın kullanılan grup, Interactions (E, 56%) en az kullanılan. Ancak:

1. **Bilgi-teorik boyutlar kritik eksik**: 18 model melodic_entropy, 13 model harmonic_entropy talep ediyor. RPU (ödül) ve PCU (öngörü) birimleri bilgi-teorik değişkenler olmadan tam kapasitede çalışamıyor.

2. **Ritmik yapı boyutları eksik**: 17 model syncopation, 14 model metricality talep ediyor. STU (14 model) ve MPU (10 model) birimleri mevcut onset_strength + spectral_flux ile ritmi dolaylı olarak işliyor — dedike ritmik özellikler doğruluğu artıracak.

3. **Pitch boyutları kısmen eksik**: SPU'nun çekirdek alanı pitch olmasına rağmen, mevcut R³ Consonance grubunda dedike pitch_chroma, F0 salience ve melodic_contour yok.

4. **Harmonik syntax boyutları eksik**: NDU ve IMU modelleri harmonik kural ihlali tespiti yapıyor ama R³'te syntactic_irregularity boyutu yok.

### 6.2 Senaryo Analizi

#### Senaryo A: Minimum Genişleme (49D → 57D, +8D)

Sadece Tier 1 + Tier 2 yüksek öncelikli boyutlar:

| Grup | Eklenen Boyutlar | Yeni D |
|------|------------------|:---:|
| G: Rhythm | syncopation_index, metricality_index | +2 |
| I: Information | melodic_entropy, harmonic_entropy, rhythmic_IC | +3 |
| H: Harmony | syntactic_irregularity, tonal_stability | +2 |
| F: Pitch | pitch_chroma | +1 |
| **Toplam** | | **+8D** |

**Etki**: 96 modelden ~35'inin (%36) doğrudan R³ girdisi iyileşir. Maliyet/fayda oranı en yüksek senaryo.

#### Senaryo B: Orta Genişleme (49D → 68D, +19D)

Bölüm 5'te tanımlanan 4 yeni grubun tamamı:

| Grup | Boyutlar | Yeni D |
|------|----------|:---:|
| F: Pitch | pitch_chroma, melodic_contour, harmonic_resolvability, inharmonicity_index, pitch_salience_F0 | +5 |
| G: Rhythm | syncopation_index, metricality_index, isochrony_nPVI, groove_index, locomotion_periodicity | +5 |
| H: Harmony | syntactic_irregularity, tonal_stability, harmonic_resolution_potential, perceptual_ambiguity, spectral_1f_slope | +5 |
| I: Information | melodic_entropy, harmonic_entropy, rhythmic_IC, rhythmic_entropy | +4 |
| **Toplam** | | **+19D** |

**Etki**: 96 modelden ~55'inin (%57) R³ girdisi iyileşir. Makul maliyet, kapsamlı kapsama.

#### Senaryo C: Maksimum Genişleme (49D → ~128D, +~79D)

Senaryo B + mevcut grupların genişlemesi + ÖNERİ boyutları:

| Kategori | Detay | Yeni D |
|----------|-------|:---:|
| F-I Yeni Gruplar | Senaryo B | +19 |
| A: Consonance genişleme | ÖNERİ: partial_tone_resolution, combination_tone_strength, cultural_consonance_weight | +3 |
| B: Energy genişleme | ÖNERİ: spectral_centroid_velocity, energy_envelope_regularity, bass_energy_ratio | +3 |
| C: Timbre genişleme | ÖNERİ: attack_time, decay_rate, vibrato_rate, vibrato_depth, formant_clarity | +5 |
| D: Change genişleme | ÖNERİ: spectral_flux_2nd_order, onset_density, offset_density, tempo_local | +4 |
| E: Interactions genişleme | ÖNERİ: F×G, F×I, G×H, G×I cross-group products | +24 |
| J: Social (multi-track) | ÖNERİ: onset_synchrony, timbral_blend, rhythmic_entrainment (SSRI multi-track) | +3 |
| K: Composite | ÖNERİ: arousal_potential, relaxation_index, nostalgia_proxy, familiarity_proxy | +4 |
| Rezerv | Gelecek genişleme alanı | +13 |
| **Toplam** | | **~+79D** |

**Etki**: Tüm 96 modele kapsamlı R³ girdisi. Yüksek maliyet — her yeni boyut DSP hesaplama ve H³ talep artışı getirir.

### 6.3 Tavsiye

**Senaryo B (49D → 68D, +19D) önerilir.** Gerekçe:

1. **Tier 1-2 feature'lar kanıt-temelli**: Her biri birden fazla model docu + gap log + empirik literature tarafından destekleniyor.
2. **4 yeni grup simetrik**: F(5D), G(5D), H(5D), I(4D) = 19D ekstra.
3. **Mevcut kod yapısıyla uyumlu**: `mi_beta.ear.r3` altına 4 yeni grup modülü eklenir (pitch.py, rhythm.py, harmony.py, information.py).
4. **E: Interactions grubu genişleme gerektirecek**: 4 yeni grubun cross-group interaction'ları (F×A, G×B, H×A, I×D vb.) eklendiğinde 68D → ~100-128D aralığına çıkar. Bu genişleme Chat R2 (top-down DSP) analizi ile birlikte belirlenecek.
5. **Multi-track özellikler (J: Social) ertelenir**: SSRI'nin 3 multi-track feature'ı mevcut single-stream pipeline ile uyumsuz. Phase 4+ konusu.

### 6.4 Implementasyon Bağımlılıkları

| Bağımlılık | Açıklama | Chat |
|------------|----------|------|
| DSP fizibilitesi | Her önerilen boyutun mel-spectrogram'dan hesaplanabilirliği | R2 (top-down) |
| H³ genişleme | Yeni R³ boyutları yeni H³ tuple'lar gerektirir (r3_idx alanı genişler) | R2 |
| E grubu yeniden yapılandırma | Cross-group interaction'lar yeni grupları kapsamalı | R3 (sentez) |
| Code modülleri | pitch.py, rhythm.py, harmony.py, information.py | Phase 4+ |
| Model doc güncellemesi | 96 model Section 4 R³ mapping'leri güncellenmeli | Phase 5 |
| Naming reconciliation | Mevcut ~64 NAMING mismatch Phase 5'te çözülmeli | Phase 5 |

### 6.5 Açık Sorular (Chat R3 İçin)

1. **IDyOM bağımlılığı**: melodic_entropy ve harmonic_entropy hesaplaması öğrenilmiş istatistiksel model (IDyOM) gerektirir. R³'ün frame-level akustik pipeline'ına bir sequence-level model nasıl entegre edilecek?
2. **Groove hesaplaması**: groove_index birden fazla alt-feature'ın (syncopation × bass_energy × metricality) kompoziti mi, yoksa bağımsız boyut mu?
3. **Interaction genişleme stratejisi**: 9 mevcut + 4 yeni = 13 grup. Tüm çapraz-grup interaction'lar C(13,2)=78 çift gerektirir. Hangileri hesaplanacak?
4. **128D vs 256D hedef**: Phase 3 planı "128-256D" diyor. Bottom-up analiz ~68-128D öneriyor. Üst sınır top-down DSP kapasitesine bağlı.

---

## Ekler

### Ek A: Kaynak Dosya Referansları

| Dosya | İçerik |
|-------|--------|
| `mi_beta/ear/r3/psychoacoustic/consonance.py` | A grubu: 7D (roughness → harmonic_deviation) |
| `mi_beta/ear/r3/dsp/energy.py` | B grubu: 5D (amplitude → onset_strength) |
| `mi_beta/ear/r3/dsp/timbre.py` | C grubu: 9D (warmth → tristimulus3) |
| `mi_beta/ear/r3/dsp/change.py` | D grubu: 4D (spectral_flux → distribution_concentration) |
| `mi_beta/ear/r3/cross_domain/interactions.py` | E grubu: 24D (x_amp_roughness → x_stumpf_autocorr) |
| `Docs/C³/Matrices/R3-Usage.md` | 94-model × 5-grup kullanım matrisi |
| `Docs/R³/R3-GAP-LOG-{UNIT}.md` | 7 birim gap log'u (IMU, ASU, NDU, MPU, PCU, ARU, RPU) |

### Ek B: Grup Kodu — Feature İsim Eşleştirmesi

**Not**: Dimension_map isimleri (R3-Usage.md'deki) ve grup kodu isimleri (code'daki) farklıdır. Bu bilinen proje-geneli sorundur (Phase 5).

| Idx | Dimension Map (R3-Usage) | Group Code (mi_beta) | Grup |
|-----|--------------------------|----------------------|------|
| 0 | perfect_fifth_ratio | roughness | A |
| 1 | euler_gradus | sethares_dissonance | A |
| 2 | harmonicity | helmholtz_kang | A |
| 3 | stumpf_fusion | stumpf_fusion | A |
| 4 | sensory_pleasantness | sensory_pleasantness | A |
| 5 | roughness_total | inharmonicity | A |
| 6 | consonance_mean | harmonic_deviation | A |
| 7 | velocity_A | amplitude | B |
| 8 | velocity_D | velocity_A | B |
| 9 | loudness | acceleration_A | B |
| 10 | onset_strength | loudness | B |
| 11 | rms_energy | onset_strength | B |
| 12 | warmth | warmth | C |
| 13 | sharpness | sharpness | C |
| 14 | brightness_kuttruff | tonalness | C |
| 15 | brightness | clarity | C |
| 16 | spectral_centroid | spectral_smoothness | C |
| 17 | spectral_bandwidth | spectral_autocorrelation | C |
| 18 | tristimulus1 | tristimulus1 | C |
| 19 | tristimulus2 | tristimulus2 | C |
| 20 | tristimulus3 | tristimulus3 | C |
| 21 | spectral_flux | spectral_flux | D |
| 22 | spectral_flatness | distribution_entropy | D |
| 23 | zero_crossing_rate | distribution_flatness | D |
| 24 | tonalness | distribution_concentration | D |
| 25-48 | (24 interaction features) | (24 cross-group products) | E |
