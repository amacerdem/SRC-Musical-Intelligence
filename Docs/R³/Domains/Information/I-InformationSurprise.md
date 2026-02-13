# Group I: Information & Surprise [87:94] -- 7D

## Overview
- **Domain**: Information
- **Code**: `mi_beta/ear/r3/domains/information/info_surprise.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Approximate (melodic/harmonic entropy are chroma-based proxies, not full IDyOM)
- **Pipeline Stage**: 3 (depends on F chroma, G onset, H key correlations)
- **Class**: `InformationSurpriseGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 87 | melodic_entropy | Entropy of chroma transition distribution (EMA) | /log(12) + warm-up | ~0.3 ms | IDyOM melodic IC (Pearce 2005) | Approximate |
| 88 | harmonic_entropy | KL(chroma_t \|\| chroma_avg) -> exp mapping | 1-exp(-KL) + warm-up | ~0.2 ms | Chord transition surprise (Gold 2019) | Approximate |
| 89 | rhythmic_information_content | -log(p(IOI_current)) from running IOI histogram | /log(16) + warm-up | ~0.2 ms | Rhythmic surprise (Spiech 2022) | Standard |
| 90 | spectral_surprise | KL(mel_t \|\| mel_avg) -> exp mapping | 1-exp(-KL) + warm-up | ~0.3 ms | Mismatch negativity (Friston) | Standard |
| 91 | information_rate | MI(mel_t; mel_{t-1}) = H_t + H_{t-1} - 2*H_joint | /log(128) | ~0.2 ms | Mutual info per frame (Weineck 2022) | Standard |
| 92 | predictive_entropy | 0.5 * log(2*pi*e * running_var.mean()) / log(128) | clamp + warm-up | ~0.2 ms | Predictive coding uncertainty (Friston) | Standard |
| 93 | tonal_ambiguity | Entropy of softmax(key_correlations * 5) | /log(24) -> [0,1] | ~0.1 ms | Key uncertainty | Standard |

## Computation Pipeline

- **Input**: mel (B, 128, T) + group_outputs from F, G, H
- **Dependencies**:
  - F[49:61] chroma for [87] melodic_entropy, [88] harmonic_entropy, [93] tonal_ambiguity
  - B[11] onset_strength (via G) for [89] rhythmic_information_content
  - H key correlations for [93] tonal_ambiguity (shared computation)
- **Output**: (B, T, 7) -- all values in [0,1]
- **Estimated cost**: ~2.0 ms/frame total
- **Warm-up**: 344 frames (2.0s) -- linear confidence ramp on all features

### Common Running Statistics

```
alpha = 1 - exp(-1 / (2.0 * 172.27)) = ~0.0029

For each frame t:
  confidence = min(1.0, t / 344)

  # Mel running average (for [88], [90], [92]):
  mel_avg_t = (1 - alpha) * mel_avg_{t-1} + alpha * mel_prob_t

  # Chroma running average (for [88]):
  chroma_avg_t = (1 - alpha) * chroma_avg_{t-1} + alpha * chroma_t

  # Transition counts (for [87]):
  transition_counts_t = (1 - alpha) * transition_counts_{t-1}
  transition_counts_t[from_pc, to_pc] += alpha

  # Running variance (for [92]):
  residual = mel_prob_t - mel_avg_t
  mel_var_t = (1 - alpha) * mel_var_{t-1} + alpha * residual^2
```

### Detailed Computation Flow

```
mel (B, 128, T), chroma (B, T, 12) from F, onset (B, T) from B
  |
  +-- [87] melodic_entropy:
  |     dominant_pc_t = argmax(chroma_t)              # (B,)
  |     dominant_pc_prev = argmax(chroma_{t-1})       # (B,)
  |     transition = dominant_pc_prev * 12 + dominant_pc_t  # 144 transitions
  |
  |     # Update running transition histogram (12x12 matrix)
  |     transition_counts *= (1 - alpha)
  |     transition_counts[dominant_pc_prev, dominant_pc_t] += alpha
  |
  |     # Conditional entropy for current source PC
  |     row = transition_counts[dominant_pc_prev, :]
  |     row_prob = row / row.sum()
  |     H = -(row_prob * log(row_prob)).sum() / log(12)
  |     melodic_entropy = H * confidence
  |
  +-- [88] harmonic_entropy:
  |     chroma_avg = EMA(chroma, alpha)                # running chroma avg
  |     KL = sum(chroma_t * log(chroma_t / chroma_avg))  # KL divergence
  |     harmonic_entropy = (1 - exp(-KL)) * confidence
  |
  +-- [89] rhythmic_information_content:
  |     # Current IOI from onset peaks
  |     current_IOI = frames_since_last_onset
  |     IOI_quantized = round(current_IOI / beat_period * 4) / 4  # 16th-note quantize
  |
  |     # Running IOI histogram (16 bins, EMA)
  |     IOI_hist *= (1 - alpha)
  |     IOI_hist[IOI_quantized] += alpha
  |
  |     p_IOI = IOI_hist[IOI_quantized] / IOI_hist.sum()
  |     rhythmic_IC = -log(p_IOI) / log(16) * confidence
  |
  +-- [90] spectral_surprise:
  |     mel_prob_t = mel_t / sum(mel_t)                # normalize
  |     mel_avg = EMA(mel_prob, alpha)                  # running avg (128D)
  |     KL = sum(mel_prob_t * log(mel_prob_t / mel_avg))
  |     spectral_surprise = (1 - exp(-KL)) * confidence
  |
  +-- [91] information_rate:
  |     H_t = entropy(mel_prob_t)                       # current entropy
  |     H_prev = entropy(mel_prob_{t-1})                # previous entropy
  |     H_joint = entropy((mel_prob_t + mel_prob_{t-1}) / 2)  # approx joint
  |     MI = H_t + H_prev - 2 * H_joint                # mutual information
  |     information_rate = MI / log(128)
  |
  +-- [92] predictive_entropy:
  |     residual = mel_prob_t - mel_avg                  # prediction error
  |     residual_var = EMA(residual^2, alpha)            # running error variance
  |     pred_H = 0.5 * log(2*pi*e * residual_var.mean()) / log(128)
  |     predictive_entropy = pred_H.clamp(0, 1) * confidence
  |
  +-- [93] tonal_ambiguity:
        key_corrs = matmul(chroma, key_profiles.T)      # (B, T, 24)
        key_probs = softmax(key_corrs * 5.0, dim=-1)    # temperature=5
        H = -(key_probs * log(key_probs)).sum(-1) / log(24)
        tonal_ambiguity = H.clamp(0, 1)
        # Note: no warm-up needed (instantaneous given chroma)
  |
  stack([87..93]) -> (B, T, 7) -> clamp(0, 1)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.log`, `torch.exp`, KL divergence computation,
  `torch.argmax`, `F.softmax`, entropy functions, EMA state management
- **Pre-computed matrices**: None (key_profiles reused from Group H)
- **Warm-up requirements**: 344 frames (2.0s) for all features with running
  statistics. `confidence = min(1.0, t / 344)` applied as a multiplier.
- **State buffers** (initialized on first call, not in __init__):
  - `_mel_avg` (B, 128): running average mel spectrum
  - `_mel_var` (B, 128): running prediction error variance
  - `_chroma_avg` (B, 12): running average chroma
  - `_transition_counts` (B, 12, 12): running pitch transition histogram
  - `_IOI_hist` (B, 16): running IOI histogram
  - `_frame_count` (int): warm-up frame counter

### Frame-by-Frame vs Vectorized Processing

The running statistics require sequential frame processing (each frame depends
on the previous frame's state). For batch efficiency, this is implemented as
a vectorized EMA using `torch.cumsum` with exponential weights:

```python
# Vectorized EMA for T frames:
weights = alpha * (1 - alpha) ** torch.arange(T-1, -1, -1)
running_avg = (mel_prob * weights.unsqueeze(0)).cumsum(dim=-1)
```

However, for real-time inference (T=1 per call), the sequential state update
is used directly.

### Tonal Ambiguity Shared Computation

Feature [93] tonal_ambiguity recomputes key correlations from chroma. In the
Stage-aware pipeline, this computation is shared with Group H's key_clarity.
The extractor can pass `group_outputs['harmony_tonality']` which contains
the key correlation values, avoiding redundant matmul.

## Phase 6 Notes

Group I is entirely new in R3 v2. No Phase 6 revision is planned.

### Quality Limitations

1. **melodic_entropy [87]**: This is a chroma-based transition entropy, not
   a full IDyOM implementation. IDyOM uses long-range Markov models and
   viewpoints (Pearce 2005) which cannot be replicated from frame-level
   mel spectrograms. Our approximation captures local pitch-class transition
   surprise but misses:
   - Long-range melodic structure
   - Multiple viewpoints (interval, contour, etc.)
   - Learned statistical regularities from a corpus

2. **harmonic_entropy [88]**: Uses KL divergence from running chroma average
   as a proxy for chord transition probability. Full chord identification
   and transition model would require explicit chord recognition.

3. **rhythmic_IC [89]**: Depends on accurate onset detection and tempo
   estimation from upstream groups. Errors propagate.

### Experimental Validation Required

| Feature | Validation Test | Expected Quality |
|---------|----------------|-----------------|
| melodic_entropy [87] | Correlation with IDyOM melodic IC on annotated corpus | Low-Medium (local-only approximation) |
| harmonic_entropy [88] | Correlation with expert harmonic analysis surprise | Medium (chroma KL is a reasonable proxy) |
| rhythmic_IC [89] | Correlation with rhythmic surprise ratings | Medium (depends on onset quality) |
| spectral_surprise [90] | Correlation with MEG/EEG mismatch negativity | Medium (KL from mel is standard) |
| tonal_ambiguity [93] | Discrimination of tonal vs atonal passages | High (entropy of key fits is well-motivated) |

## References

### Primary Papers
- Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal 27, 379-423.
- Pearce, M. T. (2005). The construction and evaluation of statistical models of melodic structure. PhD thesis, City University London.
- Pearce, M. T. & Wiggins, G. A. (2012). Auditory expectation: The information dynamics of music perception and cognition. Topics in Cognitive Science 4(4), 625-652.
- Gold, B. P. et al. (2019). Musical reward prediction errors engage the nucleus accumbens and motivate learning. PNAS 116(8), 3310-3315.
- Cheung, V. K. M. et al. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. Current Biology 29(23), 4084-4092.
- Spiech, C. et al. (2022). Rhythmic information content and neural synchronization. Cognition 226, 105180.
- Friston, K. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience 11(2), 127-138.
- Dubnov, S. (2006). Spectral anticipation. Computer Music Journal 30(2), 63-83.
- Weineck, K. et al. (2022). Neural correlates of spectral flux. NeuroImage 261.

### Toolkit Implementations
- IDyOM (Information Dynamics of Music) -- Marcus Pearce, not mel-compatible
- `librosa.feature.spectral_flatness` -- related spectral surprise
- Custom implementations required for all Group I features (no direct toolkit equivalents)
