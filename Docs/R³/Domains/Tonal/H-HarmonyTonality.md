# Group H: Harmony & Tonality [75:87] -- 12D

## Overview
- **Domain**: Tonal
- **Code**: `mi_beta/ear/r3/domains/tonal/harmony_tonality.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Standard (key_clarity, tonnetz, harmonic_change) / Approximate (tonal_stability, syntactic_irregularity)
- **Pipeline Stage**: 2 (depends on Group F chroma output)
- **Class**: `HarmonyTonalityGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 75 | key_clarity | `max(corr(chroma, 24_key_profiles))` | min-max [0.3,0.95]->[0,1] | ~1.0 ms | Krumhansl-Kessler 1982 tonal hierarchy | Standard |
| 76 | tonnetz_fifth_x | `sum(c_k * sin(k * 7pi/6))` | (x+1)/2 -> [0,1] | ~0.1 ms (all) | Harte 2006 circle-of-fifths | Standard |
| 77 | tonnetz_fifth_y | `sum(c_k * cos(k * 7pi/6))` | (x+1)/2 | (shared) | " | Standard |
| 78 | tonnetz_minor_x | `sum(c_k * sin(k * 3pi/6))` | (x+1)/2 | (shared) | Minor-third relations | Standard |
| 79 | tonnetz_minor_y | `sum(c_k * cos(k * 3pi/6))` | (x+1)/2 | (shared) | " | Standard |
| 80 | tonnetz_major_x | `sum(c_k * sin(k * 4pi/6))` | (x+1)/2 | (shared) | Major-third relations | Standard |
| 81 | tonnetz_major_y | `sum(c_k * cos(k * 4pi/6))` | (x+1)/2 | (shared) | " | Standard |
| 82 | voice_leading_distance | `sum(\|chroma_t - chroma_{t-1}\|) / 2` | /2.0 (max L1 of normalized) | <0.1 ms | Tymoczko voice-leading parsimony | Standard |
| 83 | harmonic_change | `1 - cos(chroma_t, chroma_{t-1})` | natural [0,1] | <0.1 ms | HCDF harmonic change detection | Standard |
| 84 | tonal_stability | `key_clarity * (1 - smooth(harmonic_change))` | product [0,1] | <0.1 ms | Krumhansl stability concept | Approximate |
| 85 | diatonicity | `1 - (active_PCs - 7) / 5` | linear clamp [0,1] | <0.1 ms | Tymoczko macroharmony | Approximate |
| 86 | syntactic_irregularity | `1 - exp(-KL(chroma \|\| best_key_template))` | exp mapping [0,1] | ~0.1 ms | Lerdahl 2001 tonal tension | Approximate |

## Computation Pipeline

- **Input**: F[49:61] chroma (B, T, 12) via `group_outputs['pitch_chroma'][:,:,:12]`
- **Dependencies**: Group F chroma output (required)
- **Output**: (B, T, 12) -- all values in [0,1]
- **Estimated cost**: ~2.0 ms/frame total (dominated by key correlation)
- **Warm-up**: None (all features are instantaneous given chroma)

### Detailed Computation Flow

```
chroma (B, T, 12) from Group F
  |
  +-- Key Clarity [75]:
  |     key_profiles (24, 12) = 12 major + 12 minor Krumhansl-Kessler
  |     corrs = matmul(chroma, key_profiles.T)     # (B, T, 24)
  |     key_clarity = max(corrs, dim=-1)            # best match
  |     key_clarity_norm = (kc - 0.3) / 0.65       # empirical range
  |     best_key_idx = argmax(corrs, dim=-1)        # for syntactic irreg.
  |
  +-- Tonnetz [76:81] (6D):
  |     tonnetz_matrix (12, 6) = sin/cos projections
  |     tonnetz = matmul(chroma, tonnetz_matrix)     # (B, T, 6)
  |     tonnetz_norm = (tonnetz + 1) / 2             # [-1,1] -> [0,1]
  |
  +-- Voice-Leading Distance [82]:
  |     vl = |chroma_t - chroma_{t-1}|.sum(-1) / 2  # L1 / max
  |     (frame 0 padded by duplicating frame 1)
  |
  +-- Harmonic Change [83]:
  |     sim = cosine_similarity(chroma_t, chroma_{t-1})
  |     hc = 1 - sim                                 # cosine distance
  |     (frame 0 padded)
  |
  +-- Tonal Stability [84]:
  |     hc_smooth = avg_pool1d(hc, kernel=172, pad=86)  # 1s window
  |     tonal_stability = key_clarity * (1 - hc_smooth)
  |
  +-- Diatonicity [85]:
  |     active_pcs = (chroma > 0.05).float().sum(-1)  # 0-12 count
  |     diatonicity = (1 - (active_pcs - 7) / 5).clamp(0, 1)
  |     # 7 PCs = full diatonic -> 1.0
  |     # 12 PCs = fully chromatic -> 0.0
  |
  +-- Syntactic Irregularity [86]:
        best_template = key_profiles[best_key_idx]    # (B, T, 12)
        tp = best_template / sum(best_template)       # normalize
        cp = chroma.clamp(min=1e-8)
        KL = sum(cp * (log(cp) - log(tp)))            # KL divergence
        irregularity = (1 - exp(-KL)).clamp(0, 1)
  |
  cat([75..86]) -> (B, T, 12)
```

### Key Profile Construction

The Krumhansl-Kessler probe-tone ratings define 24 key profiles (12 major + 12 minor):

```
Major template: [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
Minor template: [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

For each of 12 pitch classes (C, Db, D, ..., B):
  major_profile[shift] = roll(major_template, shift)
  minor_profile[shift] = roll(minor_template, shift)

Result: key_profiles (24, 12) -- register_buffer
```

Key clarity is the Pearson correlation between the chroma vector and the
best-matching key profile. The Krumhansl-Schmuckler algorithm computes all
24 correlations simultaneously via `torch.matmul(chroma, key_profiles.T)`.

### Tonnetz Matrix Construction

The Harte 2006 tonnetz projection encodes three musical interval relationships:

```python
k = arange(12).float()
M = zeros(12, 6)
M[:, 0] = sin(k * 7 * pi / 6)  # fifth_x:  circle of fifths
M[:, 1] = cos(k * 7 * pi / 6)  # fifth_y
M[:, 2] = sin(k * 3 * pi / 6)  # minor_x:  minor third cycle
M[:, 3] = cos(k * 3 * pi / 6)  # minor_y
M[:, 4] = sin(k * 4 * pi / 6)  # major_x:  major third cycle
M[:, 5] = cos(k * 4 * pi / 6)  # major_y
```

Each pair (x, y) represents a circular embedding. The angular intervals
(7pi/6, 3pi/6, 4pi/6) correspond to the pitch-class distances for perfect
fifths (7 semitones), minor thirds (3 semitones), and major thirds (4 semitones).

## PyTorch Implementation Notes

- **Key operations**: `torch.matmul` (key correlation 24x12, tonnetz 12x6),
  `torch.roll` (key profile construction), `F.cosine_similarity`,
  `F.avg_pool1d` (tonal stability smoothing), KL divergence computation
- **Pre-computed matrices**:
  - `key_profiles` (24, 12): Krumhansl-Kessler ratings -- `register_buffer`
  - `tonnetz_matrix` (12, 6): Harte projection -- `register_buffer`
- **Warm-up requirements**: None (but key_clarity quality improves with
  longer context; single-frame chroma may be noisy)
- **Dependency injection**: Uses `compute_with_deps(mel, group_outputs)` to
  receive F group chroma via the Stage-aware extractor pipeline

### Shared Computation

The key correlation matrix `corrs (B, T, 24)` is computed once and used by:
- `key_clarity` [75]: max of correlations
- `syntactic_irregularity` [86]: best key template selection via argmax
- Group I `tonal_ambiguity` [93]: softmax entropy of correlations (passed
  via group_outputs or recomputed)

## Phase 6 Notes

Group H is entirely new in R3 v2. No Phase 6 revision is planned.

### Quality Considerations

- **Key clarity** depends on mel-chroma quality. Below 200 Hz, mel resolution
  limits pitch class discrimination, which may reduce key detection accuracy
  for bass-heavy music.
- **Tonnetz** provides position in tonal space but not trajectory. Tonal
  trajectory (Janata 2009) would require temporal context (H3 layer).
- **Tonal stability** is a composite feature (key_clarity x harmonic_change
  rate). The 1-second smoothing window (172 frames) may be too short for
  slow harmonic progressions.
- **Syntactic irregularity** uses a simple KL divergence from the best-fit
  diatonic template. A more sophisticated model (Lerdahl's full tonal tension
  hierarchy) would require hierarchical analysis beyond frame-level processing.

### Experimental Validation Required

| Feature | Validation Test | Expected Quality |
|---------|----------------|-----------------|
| key_clarity [75] | Key detection accuracy on GTZAN, Isophonics | >=80% with mel-chroma |
| tonnetz [76:81] | Chord recognition via tonnetz clustering | Medium (chroma quality limits) |
| harmonic_change [83] | Correlation with expert chord annotations | High (standard HCDF metric) |
| tonal_stability [84] | Modulation detection in classical music | Medium (composite proxy) |
| syntactic_irregularity [86] | Correlation with expert tension ratings | Low-Medium (simple KL proxy) |

## References

### Primary Papers
- Krumhansl, C. L. & Kessler, E. J. (1982). Tracing the dynamic changes in perceived tonal organization in a spatial representation. Psychological Review 89(4), 334-368.
- Harte, C. et al. (2006). Detecting harmonic change in musical audio. Proc. ACM Multimedia, 21-26.
- Tymoczko, D. (2011). A Geometry of Music: Harmony and Counterpoint in the Extended Common Practice. Oxford UP.
- Lerdahl, F. (2001). Tonal Pitch Space. Oxford University Press.
- Balzano, G. J. (1980). The group-theoretic description of 12-fold and microtonal pitch systems. Computer Music Journal 4(4).
- Janata, P. (2009). The neural architecture of music-evoked autobiographical memories. Cerebral Cortex 19(11).

### Toolkit Implementations
- `librosa.feature.tonnetz` -- tonnetz from chroma
- `essentia.Key` -- Krumhansl-Schmuckler key detection
- `essentia.HPCP` -- high-quality chroma for key analysis
- `madmom.features.key` -- DBN-based key recognition
