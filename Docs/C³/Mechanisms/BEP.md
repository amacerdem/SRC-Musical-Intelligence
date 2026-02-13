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

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| B: Energy | [7]-[11] | onset_strength, loudness, rms_energy, velocity_A, velocity_D | STU (all 13), MPU (all 10), IMU (2), RPU (1) |
| D: Change | [21]-[24] | spectral_flux, onset_density, delta_loudness, delta_rms | STU (10), MPU (9), IMU (2), RPU (1) |
| A: Consonance | [0]-[6] | periodicity, fundamental_freq | STU (MDNS), RPU (SSRI) |
| C: Timbre | [12]-[20] | spectral_centroid, spectral_flatness | STU (AMSS), RPU (SSRI) |
| E: Interactions | [25]-[48] | Energy-timbre cross terms | STU (HGSIC), MPU (GSSM, NSCP), RPU (SSRI) |

Domain B (Energy) is the universal input — all 26 BEP-consuming models require energy envelope features for beat extraction. Domain D (Change) provides temporal derivatives critical for anticipatory motor timing. BEP has the narrowest primary R3 footprint of any mechanism, reflecting its specialised role in energy-temporal processing.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H6 (200 ms, 34 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M9 (acceleration), M10 (jerk), M11 (peak), M12 (trough), M13 (flux), M14 (periodicity) | Sub-beat pulse — full dynamics suite for onset detection, IOI periodicity, and metrical grid extraction at beat subdivision level |
| H9 (350 ms, 60 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M9 (acceleration), M11 (peak), M12 (trough), M14 (periodicity), M18 (trend) | Beat period — beat stability, phase consistency, motor cortex entrainment; trend captures tempo drift within beat window |
| H11 (450 ms, 78 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M11 (peak), M14 (periodicity), M18 (trend), M21 (zero_crossings) | Beat-to-bar — metric hierarchy; periodicity at bar-level, trend for tempo trajectory, zero-crossings for energy oscillation pattern |

BEP has the richest morph demand of any mechanism (12 distinct morphs), reflecting the complexity of temporal statistics needed for beat tracking.

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | STU, IMU | 15 | Beat tracking accumulates past onset evidence — causal pulse inference |
| L1 (Prediction) | MPU, STU, RPU | 12 | Motor planning is inherently predictive — anticipating upcoming beats |
| L2 (Integration) | RPU | 1 | Bidirectional sensorimotor integration for reward-coupled entrainment |

L0 (Memory) dominates in STU/IMU — beat perception reconstructs pulse from past events. L1 (Prediction) dominates in MPU — motor planning requires forward temporal models. Two STU models (HMCE, TMRM) use both L0 and L1.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| STU | 13 | ~600 |
| MPU | 10 | ~500 |
| IMU (RASN, CMAPCC) | 2 | ~40 |
| RPU (SSRI) | 1 | ~15 |
| **Total (deduplicated)** | **26** | **~800** |

BEP is the highest-demand mechanism by model count (26 models) and second-highest by tuple count.

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
