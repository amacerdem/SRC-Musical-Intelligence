# Pipeline: State Management

**Purpose**: Documents which R3 features are stateless vs stateful, how temporal context is managed, warm-up behavior, running statistics mechanisms, and reset strategy between audio segments.

---

## 1. Stateless vs Stateful Features

### 1.1 Definition

- **Stateless**: The output at frame `t` is a pure function of the mel spectrogram at frame `t` (and possibly `t-1` for first-difference features). No memory of earlier frames is needed.
- **Stateful**: The output at frame `t` depends on a running accumulation over multiple previous frames. The feature maintains internal state that evolves over time.

### 1.2 Classification Table

| Group | Index Range | Stateless Features | Stateful Features |
|-------|:-----------:|:------------------:|:-----------------:|
| A: Consonance | [0:7] | All 7 | None |
| B: Energy | [7:12] | All 5 | None |
| C: Timbre | [12:21] | All 9 | None |
| D: Change | [21:25] | All 4 | None |
| E: Interactions | [25:49] | All 24 | None |
| **F: Pitch & Chroma** | [49:65] | All 16 | None |
| **G: Rhythm & Groove** | [65:75] | [71] groove, [72] event_density | [65-70, 73-74] tempo, beat, syncopation, metricality, isochrony, stability, regularity |
| **H: Harmony & Tonality** | [75:87] | [76-83] tonnetz, VL, HC | [75] key_clarity*, [84] tonal_stability, [85] diatonicity*, [86] irregularity* |
| **I: Information & Surprise** | [87:94] | [91] information_rate | [87-90, 92-93] All entropy/surprise features |
| **J: Timbre Extended** | [94:114] | All 20 | None |
| **K: Modulation** | [114:128] | [122-127] psychoacoustic features | [114-121] modulation spectrum + stats |

*H features marked with * are stateful only if smoothing windows are applied (e.g., running key clarity via avg_pool1d). In a strict frame-by-frame implementation they can be computed from current-frame chroma, but the smoothed variants are recommended.

### 1.3 Summary

```
Stateless:  A(7) + B(5) + C(9) + D(4) + E(24) + F(16) + J(20) + partial G,H,K
          = ~100 features (pure function of current frame or frame pair)

Stateful:   partial G(8) + partial H(4) + I(6) + partial K(8)
          = ~26 features (require temporal context)
```

---

## 2. Temporal Context Requirements

### 2.1 First-Difference Features (1 Frame Context)

These features use the difference between frame `t` and frame `t-1`. They are technically stateless (only need the previous frame, not a running accumulator) but require at least 2 frames to produce meaningful output.

| Feature | Formula | First Valid Frame |
|---------|---------|:-----------------:|
| [8] velocity_A | `sigmoid((amp[t] - amp[t-1]) * 5.0)` | Frame 1 |
| [9] acceleration_A | `sigmoid((vel[t] - vel[t-2]) * 5.0)` | Frame 2 |
| [11] onset_strength | `relu(mel[t] - mel[t-1]).sum()` | Frame 1 |
| [21] spectral_flux | `norm(mel[t] - mel[t-1])` | Frame 1 |
| [82] voice_leading_distance | `abs(chroma[t] - chroma[t-1]).sum()` | Frame 1 |
| [83] harmonic_change | `1 - cos(chroma[t], chroma[t-1])` | Frame 1 |
| [91] information_rate | `MI(mel[t], mel[t-1])` | Frame 1 |

For frame 0, a common strategy is to duplicate it (assume `frame[-1] = frame[0]`), producing zero difference.

### 2.2 Windowed Features (344 Frame Context)

These features operate on sliding windows of approximately 2.0 seconds (344 frames at 172.27 Hz):

| Feature | Window Size | Hop | First Valid Frame | Warm-up Behavior |
|---------|:-----------:|:---:|:-----------------:|-----------------|
| [65] tempo_estimate | 344 frames | 1 | 344 | Zero or unstable until full window |
| [66] beat_strength | 344 frames | 1 | 344 | Coupled to tempo estimate |
| [67] pulse_clarity | 344 frames | 1 | 344 | Coupled to tempo estimate |
| [68] syncopation_index | 688 frames* | 1 | 688 | Needs stable tempo + metrical grid |
| [73] tempo_stability | 344 frames | 86 | 344 | Sliding window variance |
| [114-119] modulation spectrum | 344 frames | 86 | 344 | Zero output until full window |

*Syncopation requires a stable tempo estimate (344 frames) plus time for the metrical grid to stabilize (~344 additional frames).

### 2.3 Running Statistics Features (Exponential Decay)

These features maintain exponentially-weighted moving averages (EMA) that asymptotically converge:

| Feature | State Variable | Decay Time (tau) | Alpha |
|---------|---------------|:----------------:|:-----:|
| [87] melodic_entropy | 12x12 transition matrix | 2.0s | 0.0029 |
| [88] harmonic_entropy | 12D chroma EMA | 2.0s | 0.0029 |
| [89] rhythmic_IC | 16-bin IOI histogram | 2.0s | 0.0029 |
| [90] spectral_surprise | 128D mel EMA | 2.0s | 0.0029 |
| [92] predictive_entropy | 128D residual variance EMA | 2.0s | 0.0029 |
| [93] tonal_ambiguity | (stateless, uses H key correlations) | - | - |

---

## 3. Running Statistics: Exponential Decay (tau=2.0s)

### 3.1 EMA Formula

All Group I running statistics share the same exponential moving average mechanism:

```python
# Decay factor computation
alpha = 1 - exp(-1 / (tau * frame_rate))
# With tau = 2.0s, frame_rate = 172.27 Hz:
alpha = 1 - exp(-1 / (2.0 * 172.27))
alpha = 1 - exp(-0.002903)
alpha ≈ 0.0029
```

The EMA update rule:

```python
# Running mean
p_bar_t = (1 - alpha) * p_bar_{t-1} + alpha * p_t

# Running variance
sigma_bar_t = (1 - alpha) * sigma_bar_{t-1} + alpha * (p_t - p_bar_t)^2
```

### 3.2 Why tau = 2.0s

The choice of tau = 2.0s (~344 frames) was a deliberate design decision (R3-V2-DESIGN.md Decision 3):

| tau | Frames | Behavior | Problem |
|:---:|:------:|----------|---------|
| 1.0s | 172 | ~1 musical measure | Too noisy -- high variance in entropy estimates |
| **2.0s** | **344** | **~2 musical measures** | **Balance: temporal resolution vs stability** |
| 4.0s | 688 | ~4 musical measures | Too slow for melodic entropy; good for harmony |

The 2.0s window roughly corresponds to a typical musical phrase length at moderate tempos (120 BPM = 2 measures of 4/4).

### 3.3 Effective Memory

The EMA has an effective memory of approximately `1/alpha ≈ 344` frames. After `5/alpha ≈ 1720` frames (~10 seconds), a given frame's contribution has decayed to less than 1% of its original weight.

```
Contribution of frame at time t-k:
  weight(k) = alpha * (1 - alpha)^k

Half-life:
  k_half = -ln(2) / ln(1 - alpha) ≈ 238 frames ≈ 1.38s

99% forgotten after:
  k_99 = -ln(0.01) / ln(1 - alpha) ≈ 1587 frames ≈ 9.2s
```

---

## 4. Warm-Up Behavior

### 4.1 Confidence Ramp

Features that depend on running statistics are unreliable during the initial warm-up period. The I group uses a linear confidence ramp:

```python
confidence_t = min(1.0, t / (tau * frame_rate))
# = min(1.0, t / 344)

output_t = raw_feature_t * confidence_t
```

This produces:
- Frame 0: `confidence = 0.0` (output = 0)
- Frame 172 (~1.0s): `confidence = 0.5` (output = 50% of raw)
- Frame 344 (~2.0s): `confidence = 1.0` (output = 100% of raw)

### 4.2 Warm-Up Timeline

```
Frame:  0         172        344        688        1000
        |          |          |          |          |
Time:   0.0s      1.0s       2.0s       4.0s       5.8s
        |          |          |          |          |
A-E:    ██████████████████████████████████████████████  (immediate)
F:      ██████████████████████████████████████████████  (immediate)
J:      ██████████████████████████████████████████████  (immediate)
K mod:  ░░░░░░░░░░░░░░░░░░░░██████████████████████████  (344 frames)
G tempo:░░░░░░░░░░░░░░░░░░░░██████████████████████████  (344 frames)
G sync: ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░████████  (688 frames)
I ent:  ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████████████  (344 ramp)
I surp: ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██████████████████████████  (344 ramp)

Legend:  ██ = fully valid    ▒▒ = partial (confidence ramp)    ░░ = zero/invalid
```

### 4.3 Per-Feature Warm-Up Summary

| Feature / Group | Warm-Up Duration | Behavior During Warm-Up |
|----------------|:----------------:|------------------------|
| A-E (v1 groups) | 0 frames | Immediately valid (frame-level computation) |
| F: Pitch & Chroma | 0 frames | Immediately valid |
| G[65-67]: tempo, beat, pulse | 344 frames (2.0s) | Autocorrelation window not full; output unstable |
| G[68]: syncopation | 688 frames (4.0s) | Requires stable tempo + metrical grid |
| G[69-74]: other rhythm | 344 frames (2.0s) | IOI-based features need onset accumulation |
| H: Harmony & Tonality | 0 frames | Immediately valid (per-frame chroma computation) |
| I[87-88]: melodic/harmonic entropy | 344 frames (2.0s) | Linear confidence ramp: `min(1.0, t/344)` |
| I[89]: rhythmic IC | 344 frames (2.0s) | Linear confidence ramp + IOI histogram stabilization |
| I[90]: spectral surprise | 344 frames (2.0s) | Running mel average not converged; confidence ramp |
| I[91]: information rate | 1 frame | Immediate (frame-pair comparison) |
| I[92]: predictive entropy | 344 frames (2.0s) | Running variance not converged; confidence ramp |
| I[93]: tonal ambiguity | 0 frames | Immediate (uses current-frame key correlations) |
| J: Timbre Extended | 0 frames | Immediately valid |
| K[114-119]: modulation spectrum | 344 frames (2.0s) | Zero output until first full window |
| K[120-121]: mod centroid/bandwidth | 344 frames (2.0s) | Derived from modulation spectrum |
| K[122-127]: psychoacoustic | 0 frames | Immediately valid (per-frame computation) |

---

## 5. Modulation Spectrum: 344-Frame Window

### 5.1 Window Parameters

```python
WINDOW_SIZE = 344   # ~2.0s at 172.27 Hz
HOP_SIZE = 86       # ~0.5s, 75% overlap
FFT_SIZE = 512      # Zero-padded for frequency resolution
```

### 5.2 Computation Pattern

```python
# Mel temporal envelope per band
mel_env = mel.abs()                            # (B, 128, T)

# Sliding window extraction
windows = mel_env.unfold(-1, WINDOW_SIZE, HOP_SIZE)  # (B, 128, N_win, 344)

# Windowing + FFT
windowed = windows * hann_window                # (B, 128, N_win, 344)
fft_mag = torch.fft.rfft(windowed, n=FFT_SIZE).abs()  # (B, 128, N_win, 257)

# Target modulation rates -> FFT bin indices
# freq_resolution = 172.27 / 512 = 0.336 Hz
target_rates = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]  # Hz
target_bins = [1, 3, 6, 12, 24, 48]               # FFT bin indices

# Average across mel bands for each target rate
mod_energy = fft_mag[:, :, :, target_bins].mean(dim=1)  # (B, N_win, 6)

# Interpolate back to frame-level (N_win -> T)
mod_frame = F.interpolate(mod_energy, size=T, mode='linear')
```

### 5.3 Window Schedule

```
Frame:     0    86   172   258   344   430   516   602   688
           |    |    |     |     |     |     |     |     |
Window 0:  [══════════════════════]
                                  ^-- first valid output at frame 344
Window 1:       [══════════════════════]
Window 2:            [══════════════════════]
Window 3:                  [══════════════════════]
...

Between windows: linear interpolation of modulation energies
```

---

## 6. Reset Strategy Between Audio Segments

### 6.1 When to Reset

Running state must be reset when:
1. **New audio file**: A different audio source begins processing.
2. **Seek/jump**: Playback position jumps discontinuously.
3. **Silence gap**: Extended silence (> 2s) may warrant soft reset.
4. **Model evaluation boundary**: When processing independent audio segments for evaluation.

### 6.2 State Variables to Reset

```python
class InformationSurpriseGroup:
    def reset(self):
        """Reset all running state for a new audio segment."""
        self._mel_avg = None          # 128D running average mel
        self._mel_var = None          # 128D running variance
        self._chroma_avg = None       # 12D running average chroma
        self._transition_counts = None # 12x12 transition matrix
        self._frame_count = 0         # Frame counter for confidence ramp

class ModulationPsychoacousticGroup:
    def reset(self):
        """Reset modulation spectrum state."""
        self._last_fft_result = None  # Cached FFT output
        self._window_buffer = None    # Accumulated frames for next window
```

### 6.3 Reset Protocol

```python
class R3Extractor:
    def reset(self):
        """Reset all stateful groups for a new audio segment."""
        for group in self.groups:
            if hasattr(group, 'reset'):
                group.reset()
```

This should be called by the pipeline controller whenever a new audio segment begins. The call propagates to all groups that implement `reset()`. Stateless groups (A-E, F, J) do not need reset methods.

### 6.4 Soft Reset vs Hard Reset

**Hard reset** (recommended for new audio files):
- All running statistics set to `None` or zero.
- Frame counter reset to 0.
- Warm-up ramp begins from scratch.
- Modulation window buffer cleared.

**Soft reset** (potential for seek/jump within same audio):
- Running statistics preserved but decay rate temporarily increased (higher alpha).
- Frame counter set to a partial value (e.g., 172 instead of 0) to reduce warm-up time.
- Modulation buffer partially retained if seek distance < window size.

The current recommendation is to always use hard reset. Soft reset is a Phase 6+ optimization.

---

## 7. Summary: State Management Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    R3Extractor                            │
│                                                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Stateless   │  │  Windowed   │  │  Running     │     │
│  │  Groups      │  │  Groups     │  │  Statistics  │     │
│  │  A,B,C,D,E  │  │  G tempo    │  │  I entropy   │     │
│  │  F,J         │  │  K mod      │  │  I surprise  │     │
│  │  H (partial) │  │             │  │  I predict   │     │
│  │              │  │             │  │              │     │
│  │  No state    │  │  Window     │  │  EMA state   │     │
│  │  No reset    │  │  buffer     │  │  alpha=0.0029│     │
│  │  No warm-up  │  │  344 frame  │  │  Confidence  │     │
│  │              │  │  warm-up    │  │  ramp 344fr  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                          │
│  reset() ──> clears window buffers + EMA state           │
│              resets frame counter to 0                    │
│              warm-up begins anew                          │
└──────────────────────────────────────────────────────────┘
```
