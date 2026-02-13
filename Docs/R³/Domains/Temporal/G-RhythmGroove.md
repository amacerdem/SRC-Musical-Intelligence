# Group G: Rhythm & Groove [65:75] -- 10D

## Overview
- **Domain**: Temporal
- **Code**: `mi_beta/ear/r3/domains/temporal/rhythm_groove.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Standard (tempo, beat, pulse) / Approximate (syncopation, groove, metricality)
- **Pipeline Stage**: 2 (depends on Group B onset_strength [11])
- **Class**: `RhythmGrooveGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 65 | tempo_estimate | Onset autocorrelation -> dominant period -> BPM | min-max [30,300]->[0,1] | ~0.5 ms | Fraisse 1982 preferred tempo | Standard |
| 66 | beat_strength | Autocorrelation value at tempo lag: `R[tempo_lag]` | natural [0,1] (R normalized) | <0.1 ms | Pulse perception strength | Standard |
| 67 | pulse_clarity | `R[tempo_lag] / median(R[lag_min:lag_max])` | sigmoid(ratio, gain=5, center=2) | <0.1 ms | Beat ambiguity (Witek 2014) | Standard |
| 68 | syncopation_index | LHL: onset weight at off-beat positions | /max_possible -> [0,1] | ~0.5 ms | Longuet-Higgins & Lee 1984 | Approximate |
| 69 | metricality_index | Multi-scale autocorrelation: nested subdivision count | /len(ratios) -> [0,1] | <0.1 ms | Grahn & Brett 2007 metrical hierarchy | Approximate |
| 70 | isochrony_nPVI | `1 - nPVI/200` from onset IOI distribution | inverse nPVI [0,1] | ~0.3 ms | Ravignani 2021 rhythmic regularity | Standard |
| 71 | groove_index | `syncopation * bass_energy * pulse_clarity` | max-norm | <0.1 ms | Madison 2006, Janata 2012 groove | Approximate |
| 72 | event_density | Onset count per second in 1s sliding window | /20 (max ~20 onset/s) | <0.1 ms | Temporal event density | Standard |
| 73 | tempo_stability | `1 - CV(local_tempo)` over 2s sliding windows | clamp(0,1) | ~0.3 ms | Temporal prediction reliability | Standard |
| 74 | rhythmic_regularity | `1 - entropy(IOI_histogram)` | 1-norm_entropy [0,1] | ~0.2 ms | Inverse rhythmic entropy (Spiech 2022) | Standard |

## Computation Pipeline

- **Input**: B[11] onset_strength (B, T) via `group_outputs['energy'][:,:,4]`
- **Dependencies**: Group B onset_strength output (required)
- **Output**: (B, T, 10) -- all values in [0,1]
- **Estimated cost**: ~2.0 ms/frame total
- **Warm-up**: 344 frames (~2.0s) for tempo/beat features; 688 frames (~4.0s) for syncopation stabilization

### Detailed Computation Flow

```
onset_strength (B, T) from B[11]
  |
  +-- Autocorrelation:
  |     oenv_c = onset - onset.mean()
  |     R = irfft(|rfft(oenv_c)|^2)          # Wiener-Khinchin
  |     R = R / R[..., 0:1]                   # normalize to [0,1]
  |
  +-- [65] tempo_estimate:
  |     lag_min = 34 (300 BPM), lag_max = 344 (30 BPM)
  |     tempo_lag = argmax(R[lag_min:lag_max]) + lag_min
  |     tempo_bpm = 60 * 172.27 / tempo_lag
  |     tempo_norm = (tempo_bpm - 30) / 270    # [0,1]
  |
  +-- [66] beat_strength:
  |     beat_str = R[tempo_lag]                # already [0,1]
  |
  +-- [67] pulse_clarity:
  |     ratio = R[tempo_lag] / median(R[lag_min:lag_max])
  |     pulse_clar = sigmoid(5 * (ratio - 2))  # center=2, gain=5
  |
  +-- [68] syncopation_index:
  |     peaks = detect_peaks(onset, threshold=0.3)
  |     beat_grid = create_metrical_grid(tempo_lag, levels=4)
  |     sync = lhl_syncopation(peaks, beat_grid) / max_possible
  |
  +-- [69] metricality_index:
  |     ratios = [1, 2, 3, 4, 6, 8]          # subdivisions
  |     count = sum(R[tempo_lag/r] > 0.1 for r in ratios)
  |     metricality = count / 6                # [0,1]
  |
  +-- [70] isochrony_nPVI:
  |     IOI = diff(nonzero(peaks))             # inter-onset intervals
  |     nPVI = 100 * mean(|IOI_k - IOI_{k+1}| / mean(IOI_k, IOI_{k+1}))
  |     isochrony = 1 - nPVI / 200             # 1=isochronous, 0=variable
  |
  +-- [71] groove_index:
  |     bass = mel[:, :16, :].mean(dim=1) / max
  |     groove = sync * bass * pulse_clar / max
  |
  +-- [72] event_density:
  |     peaks_binary = (onset > 0.3).float()
  |     density = avg_pool1d(peaks_binary, kernel=172, pad=86)
  |     density_norm = density * 172.27 / 20   # ~onset/sec / max
  |
  +-- [73] tempo_stability:
  |     local_tempos = sliding_window_argmax(R, window=344, hop=86)
  |     stability = 1 - std(local_tempos) / mean(local_tempos)
  |
  +-- [74] rhythmic_regularity:
        IOI_hist = histogram(IOI, bins=16, range=[0, 344])
        IOI_prob = IOI_hist / sum(IOI_hist)
        entropy = -sum(p * log(p)) / log(16)
        regularity = 1 - entropy               # 1=regular, 0=irregular
  |
  stack([65..74]) -> (B, T, 10) -> clamp(0, 1)
```

### Onset Autocorrelation Algorithm

The tempo estimation uses the Wiener-Khinchin theorem for efficient
autocorrelation via FFT:

```python
# Center the onset envelope
oenv_c = onset - onset.mean(dim=-1, keepdim=True)

# Autocorrelation via FFT
spectrum = torch.fft.rfft(oenv_c)
power_spectrum = spectrum.abs().pow(2)
R = torch.fft.irfft(power_spectrum)

# Normalize
R = R / R[..., 0:1].clamp(min=1e-8)
```

The tempo search range [30, 300] BPM corresponds to lag range [34, 344] frames
at 172.27 Hz frame rate.

### LHL Syncopation Model

The Longuet-Higgins & Lee (1984) syncopation model:
1. Detect onset peaks above threshold (0.3)
2. Construct a 4-level metrical grid aligned to estimated tempo
3. Assign metrical weights: bar=0, beat=1, sub-beat=2, sub-sub-beat=3
4. For each onset, compute syncopation = max(0, weight[onset_pos] - weight[next_strong_beat])
5. Sum and normalize by maximum possible syncopation

### Groove Composite

Groove index combines three factors known to predict perceived groove:
- **Syncopation**: Off-beat accents create expectation violation (Witek 2014)
- **Bass energy**: Low-frequency content drives physical entrainment
- **Pulse clarity**: Clear beat enables synchronization

The product `sync * bass * clarity` means all three must be present for
high groove. This is consistent with Madison (2006) and Janata (2012).

## PyTorch Implementation Notes

- **Key operations**: `torch.fft.rfft` / `torch.fft.irfft` (autocorrelation),
  `torch.argmax`, `F.avg_pool1d` (event density, tempo stability),
  `torch.sigmoid`, `torch.nonzero`, `torch.diff`, `torch.histc`
- **Pre-computed matrices**: None
- **Warm-up requirements**:
  - Tempo/beat [65-67]: Valid after 344 frames (autocorrelation window)
  - Syncopation [68]: Valid after ~688 frames (tempo + grid stabilization)
  - IOI features [70,74]: Valid after sufficient onset events (context-dependent)
- **Constants**:
  - `FRAME_RATE = 172.27` Hz
  - `LAG_MIN = 34` frames (300 BPM)
  - `LAG_MAX = 344` frames (30 BPM)
  - `PEAK_THRESHOLD = 0.3`

### Batch Processing Considerations

The IOI-based features ([70] isochrony, [74] regularity) require onset
peak detection followed by interval computation. This is inherently
sequential per batch element. For GPU efficiency, these are computed using
sliding window statistics rather than explicit IOI extraction, approximating
the interval distribution from onset density patterns.

## Phase 6 Notes

Group G is entirely new in R3 v2. No Phase 6 revision is planned.

### Experimental Validation Required

| Feature | Validation Test | Expected Quality |
|---------|----------------|-----------------|
| tempo_estimate [65] | BPM estimation accuracy on Ballroom, GTZAN | >=70% (autocorrelation method) |
| beat_strength [66] | Correlation with annotated beat positions | Medium (frame-level, not beat-level) |
| syncopation_index [68] | Correlation with Witek 2014 syncopation ratings | Medium (LHL approximation from mel onset) |
| groove_index [71] | Prediction of behavioral groove ratings | Low-Medium (composite proxy; weights need calibration) |
| metricality_index [69] | Discrimination between simple/complex meters | Medium |
| isochrony_nPVI [70] | Correlation with annotated IOI regularity | Medium (onset detection accuracy limits) |

## References

### Primary Papers
- Fraisse, P. (1982). Rhythm and tempo. In The Psychology of Music, 1st ed. (Deutsch, ed.). Academic Press.
- Longuet-Higgins, H. C. & Lee, C. S. (1984). The rhythmic interpretation of monophonic music. Music Perception 1(4), 424-441.
- Witek, M. A. G. et al. (2014). Effects of polyphonic context, instrumentation, and metrical structure on syncopation in music. Music Perception 32(2), 201-217.
- Grahn, J. A. & Brett, M. (2007). Rhythm and beat perception in motor areas of the brain. J. Cognitive Neuroscience 19(5), 893-906.
- Madison, G. (2006). Experiencing groove induced by music: consistency and phenomenology. Music Perception 24(2), 201-208.
- Janata, P. et al. (2012). Sensorimotor coupling in music and the psychology of the groove. J. Exp. Psych: General 141(1), 54-75.
- Ravignani, A. et al. (2021). The evolution of rhythmic cognition. Trends in Cognitive Sciences 25(2), 159-170.
- Grabe, E. & Low, E. L. (2002). Durational variability in speech and the Rhythm Class Hypothesis. In Papers in Laboratory Phonology 7.
- Spiech, C. et al. (2022). Rhythmic information content and neural synchronization. Cognition 226.

### Toolkit Implementations
- `librosa.beat.beat_track` -- onset-based beat tracking
- `librosa.feature.tempogram` -- tempo estimation via autocorrelation
- `essentia.RhythmExtractor2013` -- comprehensive rhythm analysis
- `essentia.BeatTrackerDegara` -- beat position detection
- `madmom.features.beats` -- DBN-based beat tracking (neural, not mel-compatible)
