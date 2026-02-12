# doelling-2015-acoustic-tracking

## Citation
Doelling, K. B., & Poeppel, D. (2015). Cortical entrainment to music and its modulation by expertise. *Proceedings of the National Academy of Sciences*, 112(45), E6233-E6242. https://doi.org/10.1073/pnas.1508431112

---

## Abstract

Neural oscillations in auditory cortex have been shown to track the amplitude envelope of speech in a remarkably faithful way. Here we tested whether low-frequency (<8 Hz; delta-theta) oscillations similarly entrain to music and whether experience modifies such a cortical phenomenon. We recorded magnetoencephalography (MEG) while musicians and non-musicians listened to piano melodies spanning a wide tempo range (from 1 to 8 notes per second). In contrast to non-musicians, the data from musicians showed that entrainment is enhanced by years of musical training at all presented tempi. Our data suggest a framework in which the brain exploits temporal regularities in music to accurately parse individual notes using lower frequencies (entrainment) and higher frequencies for temporal and content-based predictions.

---

## Key Findings

### Cortical Entrainment to Music

1. **Delta-Theta Tracking**
   - Low-frequency oscillations (<8 Hz) track musical rhythms
   - Phase-locking to note onsets in auditory cortex
   - Entrainment strength scales with rhythmic regularity
   - Similar mechanisms to speech envelope tracking

2. **Tempo Sensitivity**
   - Tested tempi from 1 to 8 notes per second (60-480 BPM)
   - Optimal entrainment around 2-4 Hz (natural musical tempo range)
   - Entrainment decreases at extreme tempi
   - Individual differences in preferred tempo range

3. **Musical Expertise Effects**
   - Musicians show enhanced entrainment vs. non-musicians
   - Years of training correlate with entrainment strength
   - Effect present across all tested tempi
   - Suggests plasticity in temporal processing circuits

### Neural Oscillation Hierarchy

1. **Low Frequencies (Delta-Theta, <8 Hz)**
   - Track beat and measure-level structure
   - Parse individual notes from continuous stream
   - Support temporal chunking of musical phrases
   - Phase resets to rhythmic boundaries

2. **High Frequencies (Beta, 15-30 Hz)**
   - Coupled to behavioral performance
   - Predict upcoming events
   - Content-based predictions (pitch, timbre)
   - Stronger in musicians during anticipation

3. **Cross-Frequency Coupling**
   - Theta phase modulates gamma amplitude
   - Hierarchical organization of temporal processing
   - Supports multi-scale rhythm representation
   - Enhanced coupling in musical expertise

---

## Methods

### Participants
- 17 musicians (>10 years training)
- 17 non-musicians (no formal training)
- Age-matched groups
- Normal hearing confirmed

### Stimuli
- Piano melodies at 7 different tempi
- Isochronous note sequences
- Controlled for spectral content
- 3-minute blocks per condition

### MEG Recording
- 157-channel whole-head MEG system
- Source localization to auditory cortex
- Phase-locking value (PLV) analysis
- Inter-trial coherence (ITC) metrics

### Analysis
- Frequency-specific phase extraction
- Hilbert transform for envelope
- Coherence between stimulus and neural response
- Group comparison via permutation tests

---

## Relevance to H⁰ Temporal Processing

### HC⁰ Mechanisms

| Mechanism | Relevance | Key Finding |
|-----------|-----------|-------------|
| **OSC** | Critical | Delta-theta oscillations track musical rhythm |
| **TGC** | High | Tempo-dependent gain modulation |
| **TIH** | High | Multi-scale temporal integration hierarchy |
| **ATT** | Moderate | Attention modulates entrainment strength |

### HR⁰ Mechanisms

| Mechanism | Relevance | Key Finding |
|-----------|-----------|-------------|
| **RTI** | High | Short-term rhythm integration (~2.5s) |
| **LTI** | Moderate | Phrase-level temporal structure |
| **PST** | High | Grouping structure parsing |

### Temporal Windows
- **Beat level**: 250-500 ms (2-4 Hz delta-theta)
- **Measure level**: 1-2 s (0.5-1 Hz delta)
- **Phrase level**: 4-8 s (0.125-0.25 Hz infra-slow)

---

## Key Equations

### Phase-Locking Value (PLV)
```
PLV = |1/N Σ exp(iφ(t_n))|
```
Where:
- φ(t_n) = phase difference between stimulus and neural signal at trial n
- N = number of trials
- PLV ranges from 0 (no phase-locking) to 1 (perfect phase-locking)

### Inter-Trial Coherence
```
ITC(f) = |1/N Σ exp(iφ_k(f))|
```
Where:
- φ_k(f) = phase at frequency f for trial k
- Measures consistency of phase across trials

---

## Implications for SRC⁹-Composer

1. **R⁰ Spectral Features**
   - Validates importance of rhythmic envelope extraction
   - Supports beat-tracking algorithm design

2. **HC⁰ Oscillatory Mechanisms**
   - Provides neural basis for OSC feature extraction
   - Expertise effects inform individual difference modeling

3. **HR⁰ Temporal Integration**
   - Entrainment frequencies map to RTI/LTI timescales
   - Supports multi-scale temporal representation

4. **Training Paradigm**
   - Musical expertise effects suggest training curriculum design
   - Plasticity evidence supports learned representations

---

## Related Papers

1. Doelling, K. B., et al. (2014). Acoustic landmarks drive delta-theta oscillations. *NeuroImage*, 85, 761-768.
2. Luo, H., & Poeppel, D. (2007). Phase patterns of neuronal responses. *Neuron*, 54(6), 1001-1010.
3. Giraud, A. L., & Poeppel, D. (2012). Cortical oscillations and speech processing. *Nature Reviews Neuroscience*, 13(2), 100-111.
4. Nozaradan, S., et al. (2011). Tagging the neuronal entrainment to beat and meter. *Journal of Neuroscience*, 31(28), 10234-10240.

---

*H⁰ Literature Database | Neural-Oscillations Category | Last Updated: February 2026*
