# BEP — Beat Entrainment Processing

| Field | Value |
|-------|-------|
| NAME | BEP |
| FULL_NAME | Beat Entrainment Processing |
| CIRCUIT | Sensorimotor (rhythm & movement) |
| OUTPUT_DIM | 30 |
| HORIZONS | H6 (200 ms), H9 (350 ms), H11 (450 ms) |

## Description

Beat Entrainment Processing models the sensorimotor coupling between auditory beat perception and motor cortex entrainment. When humans hear rhythmic music, premotor and supplementary motor areas (SMA) synchronise to the beat even without overt movement — "neural entrainment to the beat" (Grahn & Brett 2007). BEP quantifies the strength and precision of this coupling across three closely spaced horizons within the beat-level temporal window.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H6 (200 ms) | Sub-beat pulse: onset regularity and inter-onset-interval (IOI) periodicity establishing the metrical grid's finest level. Corresponds to sub-beat subdivisions at moderate tempi (120 BPM). |
| 10-19 | H9 (350 ms) | Beat period: beat-period stability, phase consistency, motor cortex entrainment strength. ~171 BPM, near the upper end of comfortable tapping tempo. Aligns with preferred tempo range (van Noorden & Moelants 1999). |
| 20-29 | H11 (450 ms) | Beat-to-bar: transition from individual beats to metric grouping. ~133 BPM tactus tempo. SMA activation reflecting metric hierarchy processing (Chen et al. 2008). |

## H3 Demand

To be populated in Phase 6. Will declare demands for energy, onset strength, and periodicity R3 features at H6, H9, and H11 to measure beat-level entrainment precision and motor coupling.

## Models Using This Mechanism

### STU (Sensorimotor Timing Unit)
- **HMCE** — Hierarchical Musical Context Encoding
- **AMSC** — Auditory-Motor Synchronisation Circuit
- **AMSS** — Auditory-Motor Synchronisation System
- **MDNS** — Motor-Driven Neural Sequencing
- **NEWMD** — Neural Entrainment and Working Memory Dynamics
- **EDTA** — Entrainment-Driven Temporal Alignment
- **ETAM** — Entrainment and Temporal Attention Model
- **HGSIC** — Hierarchical Groove and Sensorimotor Integration Circuit
- **TMRM** — Temporal Memory and Rhythm Model
- **OMS** — Oscillatory Motor Synchronisation
- **MPFS** — Motor Planning and Feedforward Sequencing
- **MTNE** — Motor-Temporal Neural Entrainment
- **PTGMP** — Predictive Timing and Groove Motor Processing

### MPU (Motor Planning Unit)
- **PEOM** — Predictive Error and Oscillatory Model
- **MSR** — Motor Sequencing and Rhythm
- **GSSM** — Groove and Sensorimotor Synchronisation Model
- **NSCP** — Neural Sequencing and Coupling Processor
- **DDSMI** — Dynamic Decision-making in Sensorimotor Integration
- **SPMC** — Sensory-Predictive Motor Controller
- **STC** — Sensorimotor Timing Circuit
- **VRMSME** — Vestibular-Rhythmic Motor-Sensory Model of Entrainment
- **ASAP** — Auditory-Sensorimotor Alignment Processor
- **CTBB** — Cortico-Thalamic Beat Binding

### IMU (Integrative Memory Unit)
- **CMAPCC** — Cross-Modal Associative Processing in Cortical Circuits
- **RASN** — Rhythm and Associative Sequence Network

### RPU (Regulatory Processing Unit)
- **IOTMS** — Integration of Timing and Motor Signals

## Neuroscientific Basis

- Grahn & Brett (2007): fMRI showing SMA, premotor, and basal ganglia activation during beat perception.
- Large & Palmer (2002): Neural oscillator model of beat tracking — entrainment as coupled oscillation.
- Chen et al. (2008): Listening to musical rhythms recruits motor regions of the brain.
- Zatorre et al. (2007): Motor-auditory interaction during rhythm perception and production.
- van Noorden & Moelants (1999): Resonance theory of tempo perception; preferred tempo ~120 BPM.

## Code Reference

`mi_beta/brain/mechanisms/bep.py`
