# neural-timing-arxiv

## Citation
Paton, J. J., & Buonomano, D. V. (2018). The Neural Basis of Timing: Distributed Mechanisms for Diverse Functions. *Neuron*, 98(4), 687-705. https://doi.org/10.1016/j.neuron.2018.03.045

**Review Article:** Hass, J., & Durstewitz, D. (2016). Time at the center, or time at the side? Assessing current models of time perception. *Current Opinion in Behavioral Sciences*, 8, 238-244.

---

## Abstract

Timing is critical to most forms of learning, behavior, and sensory-motor processing. Converging evidence supports the notion that timing relies on intrinsic and general properties of neurons and neural circuits—that is, the brain uses its natural cellular and network dynamics to solve a diversity of temporal computations. This review synthesizes evidence from neurophysiology, computational modeling, and psychophysics demonstrating that multiple circuits and mechanisms underlie the ability to tell time across different timescales (milliseconds to hours) and functional contexts (motor timing, interval perception, temporal prediction).

---

## Key Findings

### Distributed Timing Mechanisms

1. **No Dedicated Clock**
   - Multiple circuits contribute to timing
   - Context and task-dependent mechanisms
   - Timing emerges from network dynamics
   - Different timescales engage different systems

2. **Population Clocks**
   - Time encoded in dynamically changing activity patterns
   - Neural trajectories through state space
   - Reproducible sequences for timing
   - Recurrent network dynamics

3. **Timescale Hierarchy**
   - Subsecond: Cerebellum, sensory cortex
   - Seconds: Basal ganglia, PFC
   - Minutes-hours: Hippocampus, striatal dopamine
   - Circadian: SCN, molecular clocks

### Subsecond Timing

1. **Sensory Processing**
   - Coincidence detection in auditory brainstem
   - Temporal integration windows in cortex
   - Duration tuning in auditory cortex
   - Gap detection and temporal order

2. **Motor Timing**
   - Cerebellar-dependent timing
   - Supplementary motor area activation
   - Basal ganglia for sequential timing
   - Timing in motor cortex preparatory activity

3. **Neural Mechanisms**
   - Synaptic dynamics (facilitation, depression)
   - Intrinsic time constants
   - Network reverberations
   - Ramping activity

### Suprasecond Timing

1. **Interval Timing (1-60s)**
   - Striatal "clock" neurons
   - Dopaminergic modulation
   - Working memory involvement
   - Scalar timing property (Weber's law)

2. **Key Brain Regions**
   - Dorsolateral striatum
   - Prefrontal cortex
   - Supplementary motor area
   - Insula for interoceptive timing

3. **Computational Models**
   - Pacemaker-accumulator
   - State-dependent networks
   - Ramping models
   - Drift-diffusion models

---

## Theoretical Frameworks

### Population Coding of Time

1. **State-Dependent Networks**
   - Time as trajectory through neural space
   - Recurrent dynamics generate temporal patterns
   - Different read-outs for different intervals
   - Flexible and context-dependent

2. **Ramping Activity**
   - Monotonic increase toward threshold
   - Common in timing tasks
   - Found in PFC, LIP, striatum
   - May reflect accumulation or urgency

### Predictive Timing

1. **Temporal Expectations**
   - Hazard rate computations
   - Foreperiod effects
   - Beat-based vs. duration-based timing
   - Modulates sensory processing

2. **Neural Implementation**
   - Delta oscillations for temporal prediction
   - Motor system involvement
   - Attention and timing interaction
   - Cerebellar forward models

---

## Relevance to H⁰ Temporal Processing

### HC⁰ Mechanisms

| Mechanism | Relevance | Key Finding |
|-----------|-----------|-------------|
| **ITM** | Critical | Interval timing mechanisms detailed |
| **PTM** | High | Predictive timing frameworks |
| **NPL** | High | Neural phase-locking for timing |
| **TGC** | Moderate | Temporal gain control mechanisms |

### HR⁰ Mechanisms

| Mechanism | Relevance | Key Finding |
|-----------|-----------|-------------|
| **RTI** | High | Short-term integration (~2.5s) |
| **LTI** | High | Extended temporal integration |
| **GTI** | Moderate | Global temporal patterns |

### Timescale Mapping

| Timescale | Brain Region | H⁰ Mechanism |
|-----------|--------------|--------------|
| 10-100 ms | Cerebellum, A1 | OSC, TGC |
| 100-1000 ms | Basal ganglia, SMA | ITM, PTM |
| 1-10 s | PFC, striatum | RTI, LTI |
| 10-60 s | Hippocampus, PFC | GTI, FTO |

---

## Key Equations

### Weber's Law for Time
```
σ_T / T = k (Weber fraction)
```
Where:
- σ_T = standard deviation of time estimate
- T = interval duration
- k ≈ 0.1-0.2 for humans

### Ramping Model
```
r(t) = r_0 + β × t + ε(t)
```
Where:
- r(t) = firing rate at time t
- r_0 = baseline rate
- β = ramping slope
- ε(t) = noise

### State-Dependent Network
```
dx/dt = f(x, W) + I(t)
```
Where:
- x = network state
- W = recurrent weights
- f = nonlinear dynamics
- I(t) = input

---

## Implications for SRC⁹-Composer

1. **Multi-Scale Timing**
   - Different mechanisms for different timescales
   - Hierarchical organization in HR⁰

2. **Population Code Approach**
   - R⁰_temporal as population timing code
   - State-space trajectories for temporal patterns

3. **Prediction Integration**
   - Temporal prediction in HC⁰ mechanisms
   - Hazard rate computation for expectation

4. **Feature Extraction**
   - Duration-tuned responses as features
   - Ramping signals for temporal structure

---

## References

1. Paton, J. J., & Buonomano, D. V. (2018). Neuron, 98(4), 687-705.
2. Merchant, H., et al. (2013). Nature Reviews Neuroscience, 14(10), 692-703.
3. Hass, J., & Durstewitz, D. (2016). Current Opinion in Behavioral Sciences, 8, 238-244.
4. Coull, J. T., et al. (2011). Neuropsychopharmacology, 36(1), 98-113.
5. Jazayeri, M., & Shadlen, M. N. (2010). Nature Neuroscience, 13(8), 1020-1026.

---

*H⁰ Literature Database | Time-Perception Category | Last Updated: February 2026*
