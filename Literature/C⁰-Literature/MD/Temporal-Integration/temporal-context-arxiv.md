# temporal-context-arxiv

## Citation
Hasson, U., Yang, E., Vallines, I., Heeger, D. J., & Rubin, N. (2008). A hierarchy of temporal receptive windows in human cortex. *Journal of Neuroscience*, 28(10), 2539-2550. https://doi.org/10.1523/JNEUROSCI.5487-07.2008

**Review:** Honey, C. J., et al. (2012). Slow cortical dynamics and the accumulation of information over long timescales. *Neuron*, 76(2), 423-434.

---

## Abstract

The brain integrates information across multiple timescales to understand complex, temporally extended stimuli such as speech and music. This hierarchical organization reflects a fundamental principle: early sensory areas process information over brief timescales (tens to hundreds of milliseconds), while higher-order areas integrate over increasingly longer timescales (seconds to minutes). This temporal context hierarchy enables the brain to extract meaning from ongoing streams of sensory input, supporting language comprehension, music perception, and narrative understanding.

---

## Key Findings

### Temporal Receptive Windows (TRWs)

1. **Definition**
   - Duration over which cortical area integrates information
   - Analogous to spatial receptive fields
   - Increases along cortical hierarchy
   - Determines temporal context sensitivity

2. **Measurement Approach**
   - Scramble movie at different timescales
   - Measure reliability of neural response
   - Longer TRW = sensitivity to longer context
   - Inter-subject correlation method

3. **Hierarchical Organization**
   - Primary sensory areas: ~100-300 ms
   - Association areas: 1-5 s
   - Default mode network: 10-30 s
   - Narrative processing: minutes

### Auditory Temporal Hierarchy

1. **Early Auditory Cortex**
   - Integration window: ~50-200 ms
   - Spectrotemporal features
   - Phoneme-level processing
   - Rapid temporal modulations

2. **Superior Temporal Sulcus**
   - Integration window: ~1-3 s
   - Word and phrase processing
   - Prosodic contour tracking
   - Sentence-level integration

3. **Frontal and Parietal Areas**
   - Integration window: ~5-30 s
   - Discourse-level processing
   - Narrative structure
   - Event boundary detection

### Intrinsic Neural Timescales

1. **Autocorrelation Decay**
   - Measure of intrinsic temporal dynamics
   - Increases up cortical hierarchy
   - Reflects local circuit properties
   - Predicts functional TRW

2. **Gradient Across Cortex**
   - Sensory areas: fast timescales
   - Association areas: slow timescales
   - Reflects connectivity and recurrence
   - Supports multi-scale processing

---

## Relevance to H⁰ Temporal Processing

### HC⁰ Mechanisms

| Mechanism | Relevance | Key Finding |
|-----------|-----------|-------------|
| **TIH** | Critical | Temporal integration hierarchy |
| **TGC** | High | Temporal gain at different scales |
| **OSC** | High | Oscillations reflect timescales |
| **ATT** | Moderate | Attention modulates integration |

### HR⁰ Mechanisms

| Mechanism | Integration Window | Cortical Level |
|-----------|-------------------|----------------|
| **RTI** | ~2.5 s | Secondary auditory |
| **LTI** | ~30 s | Association cortex |
| **XTI** | ~8 s | Temporal-parietal |
| **GTI** | ~60 s | Prefrontal, DMN |
| **FTO** | ~120 s | Extended narrative |

### Music-Specific Applications

1. **Beat Processing**
   - Short integration: note-level (100-500 ms)
   - Medium integration: phrase-level (2-8 s)
   - Long integration: section-level (30-120 s)

2. **Harmonic Processing**
   - Local: chord identity (500 ms)
   - Regional: progression (4-8 s)
   - Global: tonal center (30-60 s)

3. **Form Perception**
   - Motive recognition: 2-4 s
   - Theme processing: 15-30 s
   - Movement structure: 2-5 min

---

## Key Equations

### Temporal Receptive Window
```
TRW = ∫₀^∞ t × w(t) dt / ∫₀^∞ w(t) dt
```
Where:
- w(t) = temporal weighting function
- TRW = center of mass of integration

### Inter-Subject Correlation
```
ISC = corr(y_i(t), mean(y_j≠i(t)))
```
Where:
- y_i(t) = neural response of subject i
- ISC reflects stimulus-driven response

### Intrinsic Timescale
```
τ = ∫₀^∞ t × AC(t) dt
```
Where:
- AC(t) = autocorrelation function
- τ = intrinsic neural timescale

---

## Implications for SRC⁹-Composer

1. **Hierarchical Feature Extraction**
   - R⁰ spectral: short timescale features
   - HC⁰: medium timescale integration
   - HR⁰: long timescale structure

2. **Multi-Scale Architecture**
   - Parallel processing at multiple timescales
   - Information accumulation across layers
   - Context-dependent representations

3. **Window Design**
   - RTI window: 2.5 s (Pöppel present)
   - LTI window: 30 s (Jones attending)
   - GTI window: 60 s (formal functions)
   - FTO window: 120 s (sonata theory)

4. **Validation Targets**
   - Neural TRW as ground truth
   - ISC as alignment metric
   - Intrinsic timescale matching

---

## References

1. Hasson, U., et al. (2008). Journal of Neuroscience, 28(10), 2539-2550.
2. Honey, C. J., et al. (2012). Neuron, 76(2), 423-434.
3. Lerner, Y., et al. (2011). Journal of Neuroscience, 31(8), 2906-2915.
4. Chien, H. Y. S., & Honey, C. J. (2020). NeuroImage, 206, 116272.
5. Baldassano, C., et al. (2017). Neuron, 95(3), 709-721.

---

*H⁰ Literature Database | Temporal-Integration Category | Last Updated: February 2026*
