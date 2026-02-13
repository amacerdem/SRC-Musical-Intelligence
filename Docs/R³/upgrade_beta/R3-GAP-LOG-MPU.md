# R³ Gap Log — MPU (Motor Planning Unit)

This file records R³ spectral feature gaps discovered during Phase 1 C³ revision of MPU models.

---

## MPU-α1-PEOM (Period Entrainment Optimization Model)

### Gap 1: Syncopation Index
- **Source**: Grahn & Brett 2007 — integer ratio rhythms with regular perceptual accents induce beat more strongly than non-metric or complex metric rhythms
- **Current R³ coverage**: No syncopation or metrical regularity dimension exists in 49D R³
- **Proposed**: A syncopation index (e.g., Longuet-Higgins & Lee 1984, or Witek et al. 2014 syncopation measure) would capture beat induction strength
- **Impact**: PEOM and other beat-related models (BEP mechanism) would benefit from explicit syncopation input

### Gap 2: Metrical Structure Complexity
- **Source**: Grahn & Brett 2007 — distinction between metric simple, metric complex, and non-metric rhythms drives differential brain activation
- **Current R³ coverage**: No explicit metrical complexity dimension
- **Proposed**: Metrical strength/complexity measure (e.g., based on autocorrelation periodicity of onset patterns)
- **Impact**: Would inform period locking difficulty and entrainment success

### Gap 3: Phase-Amplitude Coupling Feature
- **Source**: Fujioka et al. 2012 — beta oscillation modulation by rhythmic frequency suggests phase-amplitude coupling is important
- **Current R³ coverage**: No PAC-related spectral feature
- **Proposed**: Beta-band power modulation index or PAC strength as R³ feature
- **Impact**: Relevant for BEP mechanism and all motor timing models

---

## MPU-α2-MSR (Musician Sensorimotor Reorganization)

### Gap 4: High-Frequency PLV Feature (40-60 Hz)
- **Source**: L. Zhang et al. 2015 — musicians show enhanced PLV at 40-60 Hz (d≈1.13)
- **Current R³ coverage**: R³ has no explicit PLV or neural synchrony measure in the 49D space
- **Proposed**: A gamma-band PLV proxy or 40 Hz steady-state auditory-evoked potential feature
- **Impact**: MSR and BEP mechanism would benefit from a direct PLV-related input feature rather than relying on x_l0l5 as a proxy

### Gap 5: P2 Amplitude / Novelty Feature
- **Source**: L. Zhang et al. 2015 — musicians show reduced P2 (d≈1.16), interpreted as top-down inhibition
- **Current R³ coverage**: No explicit novelty/saliency dimension; loudness_entropy is used as proxy
- **Proposed**: A neural novelty index derived from onset-to-onset spectral change patterns
- **Impact**: MSR's f05_p2_suppression currently uses loudness_entropy as a proxy; a dedicated novelty feature would improve accuracy

---

## MPU-α3-GSSM (Gait-Synchronized Stimulation Model)

### Gap 6: Gait Phase / Motor Periodicity Feature
- **Source**: Yamashita et al. 2025 — gait-synchronized tACS phase-locked to heel strike; stride time CV is the primary outcome
- **Current R³ coverage**: R³ has spectral_flux and onset_strength but no explicit motor periodicity or gait-cycle feature
- **Proposed**: A locomotion periodicity index (e.g., dominant periodicity in the 0.5–2 Hz range corresponding to typical gait cadence) derived from energy envelope autocorrelation
- **Impact**: GSSM currently approximates gait phase using spectral_flux periodicity at H16; a dedicated motor-band periodicity feature would more directly capture gait-relevant temporal structure

### Gap 7: Stimulation Phase-Coupling Index
- **Source**: Kitatani et al. 2020 & Koganemaru et al. 2019 — gait-synchronized brain stimulation requires real-time phase estimation
- **Current R³ coverage**: No phase-locking value (PLV) or inter-area coherence feature in R³
- **Proposed**: A real-time phase-coupling proxy between low-frequency energy fluctuations and onset patterns
- **Impact**: GSSM's f07_phase_synchronization relies on BEP beat entrainment as proxy; a direct phase-coupling feature would better capture stimulation-gait alignment

---
