# peak_detection -- Appraisal Belief (SRP)

**Category**: Appraisal (observe-only)
**Owner**: SRP (ARU-alpha1)

---

## Definition

"Musical peak/climax happening now." Observes whether the current moment qualifies as a musical peak -- a convergence of acoustic and reward signals that triggers chills/frisson. Peak detection is a threshold-crossing event: DA + opioid + ANS activation must converge above a threshold for a peak to register. You can have DA without peaks, but not peaks without DA.

Peaks occur at ~3.7 per excerpt on average (Salimpoor 2011), with an inter-peak refractory period of ~10-30s (Grewe 2009). This is not neural exhaustion but the time needed to build new predictions -- a peak requires a fresh anticipation-buildup cycle.

---

## Observation Formula

```
# From SRP M-layer (Musical meaning):
peak_detection = SRP.peak_detection[M15]  # index [15]

# Range: [0, 1]
# 0 = no peak
# 1 = maximum peak/climax

# Computed from Sloboda 1991 chill triggers:
# - Melodic appoggiaturas (dissonance -> resolution)
# - Dramatic crescendos (most common trigger -- Panksepp 1995)
# - Onset of unexpected harmonies
# - Chord progressions descending circle of fifths to tonic
# - Moments of modulation (key changes)
# - Melodies in human vocal register (~300-3000 Hz)

# Acoustic detection:
# peak_candidate = sigma(0.3*onset_surge + 0.3*consonance_resolution + 0.2*energy_peak + 0.2*spectral_change)
# where:
#   onset_surge = R3[11] (onset_strength) -> H3 velocity > threshold
#   consonance_resolution = delta(consonance_mean) > 0 (dissonance->consonance transition)
#   energy_peak = R3[7] (amplitude) at local maximum
#   spectral_change = R3[21] (spectral_flux) spike

# Refractory gate:
# if time_since_last_peak < 10s: peak_detection *= decay_factor
# Implements ~10-30s behavioral refractory (Grewe 2009)
```

No prediction -- observe-only appraisal.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| SRP M15 | peak_detection [15] | Primary peak/climax flag |
| SRP N1 | da_nacc [1] | NAcc DA must be high for peak |
| SRP N2 | opioid_proxy [2] | Opioid convergence required |
| SRP T9 | tension [9] | Prior tension required (buildup) |
| R3 [11] | onset_strength | Transient energy (attack) |
| R3 [7] | amplitude | Energy level |
| R3 [0:7] | consonance group | Resolution detection |
| R3 [21] | spectral_flux | Spectral change trigger |

---

## Kernel Usage

The peak_detection appraisal serves as a binary-like flag for experiential logging and clinical monitoring:

```python
# In scheduler output assembly:
# peak_detection flags chill/frisson moments
# Used by output logger and RAM for brainstem/midbrain activation
# Refractory period ensures peaks are sparse and meaningful
```

Peak detection does not feed back into the reward computation (it is an output, not an input). It is consumed by:
1. **Output logger**: Records peak moments for experience analysis
2. **RAM**: Triggers brainstem + midbrain (VTA, PAG) region activation
3. **F10 Clinical**: Chills frequency and intensity as therapeutic markers

---

## Scientific Foundation

- **Salimpoor 2011**: ~3.7 chills per excerpt on average (PET, N=8)
- **Sloboda 1991**: Musical triggers of chills -- appoggiaturas, crescendos, harmonic changes (survey, N=83)
- **Panksepp 1995**: Dramatic crescendos are the most common chill trigger; vocal range melodies (300-3000 Hz)
- **Grewe 2009**: Inter-chill refractory ~10-30s; listening to music as a re-creative process (N=38)
- **de Fleurian & Pearce 2021**: 55-90% of listeners report musical chills at least sometimes (systematic review)
- **Chabin et al. 2020**: HD-EEG reveals theta increase in OFC, decreased theta in SMA+STG during chills (N=18)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/srp_relay.py`
