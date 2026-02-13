# Phase 5: Pipeline — End-to-End MI Processing

**Phase**: P5
**Depends on**: P1 (contracts), P2 (ear), P3 (brain), P4 (semantics)
**Output**: 6 Python files
**Gate**: G5 — MIPipeline produces (B, T, 1366) from audio waveform

---

## Overview

The pipeline connects all layers into a single end-to-end system:

```
Audio waveform (44100 Hz)
  │
  ▼ Cochlea
128-mel spectrogram (B, 128, T) @ 172.27 Hz
  │
  ▼ R³ Extractor
R³ features (B, T, 128)
  │
  ▼ H³ Extractor
H³ features: Dict[4-tuple → (B, T) scalar]
  │
  ▼ Brain Orchestrator
Brain output (B, T, 1006)
  │
  ▼ L³ Orchestrator
L³ output (B, T, 104)
  │
  ▼ Assembly
MI-space (B, T, 1366) = cat([mel_summary(128), R³(128), Brain(1006), L³(104)])
```

---

## P5.1 — Cochlea

### `ear/cochlea/__init__.py`

**Purpose**: Package init, re-exports.

---

### `ear/cochlea/constants.py`

**Purpose**: Audio processing constants.

**Primary Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` — frame rate, hop size, mel bins
- `Docs/Vision/MI-VISION.md` — sample rate, 1366D MI-space definition

**Related Docs**:
- `Docs/R³/Pipeline/Performance.md` — timing budget (5.8 ms/frame)

**Depends On**: Nothing.

**Exports**: Constants

**Key Constraints**:
- `SAMPLE_RATE = 44100`
- `HOP_LENGTH = 256`
- `N_FFT = 2048`
- `N_MELS = 128`
- `FRAME_RATE = SAMPLE_RATE / HOP_LENGTH` → 172.265625 Hz
- `FRAME_DURATION_MS = 1000 / FRAME_RATE` → ~5.804 ms
- `MI_SPACE_DIM = 1366` (128 + 128 + 1006 + 104)

**Verification Checklist**:
- [ ] FRAME_RATE ≈ 172.27 Hz
- [ ] MI_SPACE_DIM == 1366
- [ ] All values match architecture docs

---

### `ear/cochlea/mel_transform.py`

**Purpose**: Convert audio waveform to 128-mel spectrogram.

**Primary Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` — mel spectrogram specification

**Related Docs**:
- `Docs/R³/Pipeline/Performance.md` — real-time constraints

**Depends On**: `ear/cochlea/constants.py`

**Exports**: `MelTransform`

**Key Constraints**:
- Input: `(B, samples)` raw audio at 44100 Hz
- Output: `(B, 128, T)` log-mel spectrogram
- Uses `torchaudio.transforms.MelSpectrogram` or equivalent
- Log compression: `log1p(mel)` or `20 * log10(mel + eps)`
- T = ceil(samples / HOP_LENGTH)

**Verification Checklist**:
- [ ] Output shape (B, 128, T) with correct T
- [ ] Log compression applied
- [ ] Deterministic output

---

## P5.2 — Pipeline

### `pipeline/__init__.py`

**Purpose**: Package init.

---

### `pipeline/config.py`

**Purpose**: Pipeline configuration and mode selection.

**Primary Docs**:
- `Docs/Vision/MI-VISION.md` — three modes: ANALYZE, COMPOSE, HYBRID

**Depends On**: `ear/cochlea/constants.py`

**Exports**: `PipelineConfig`, `PipelineMode`

**Key Constraints**:
- Modes: ANALYZE (encode only, default), COMPOSE (decode), HYBRID (co-creative)
- Initial implementation: ANALYZE mode only
- Config fields: sample_rate, hop_length, n_mels, device, dtype

**Verification Checklist**:
- [ ] Three modes defined
- [ ] Default mode is ANALYZE
- [ ] Config uses cochlea constants

---

### `pipeline/mi_pipeline.py`

**Purpose**: End-to-end Audio → 1,366D MI-space.

**Primary Docs**:
- `Docs/Vision/MI-VISION.md` — MI-space definition, bidirectional architecture
- `Docs/MI Architecture/MI-Doc/MI-DOC-ARCHITECTURE.md` — layer integration

**Related Docs**:
- `Docs/R³/R3-SPECTRAL-ARCHITECTURE.md` — R³ layer
- `Docs/H³/H3-TEMPORAL-ARCHITECTURE.md` — H³ layer
- `Docs/C³/C3-ARCHITECTURE.md` — C³ layer
- `Docs/L³/L3-SEMANTIC-ARCHITECTURE.md` — L³ layer
- `Docs/Beta/DISCREPANCY-REGISTRY.md` — known issues

**Depends On**: ALL previous phases:
- `ear/cochlea/mel_transform.py`
- `ear/r3/extractor.py`
- `ear/h3/extractor.py`
- `brain/orchestrator.py`
- `semantics/orchestrator.py`
- `pipeline/config.py`

**Exports**: `MIPipeline`

**Key Constraints**:
- Constructor: receives PipelineConfig
- Method: `analyze(audio: Tensor) → MIOutput`
  1. mel = MelTransform(audio) → (B, 128, T)
  2. r3 = R3Extractor.extract(mel) → (B, T, 128)
  3. h3 = H3Extractor.extract(r3, demand) → Dict[4-tuple, (B,T)]
  4. brain = BrainOrchestrator.compute(h3, r3) → (B, T, 1006)
  5. l3 = L3Orchestrator.compute(brain) → (B, T, 104)
  6. mi_space = torch.cat([mel_summary, r3, brain, l3], dim=-1) → (B, T, 1366)
- mel_summary: reduce mel (B,128,T) → (B,T,128) via transpose or mean pooling
- MI-space composition: Cochlea(128) + R³(128) + C³(1006) + L³(104) = 1366D
- Must handle H³ demand aggregation from all 96 models
- Method: `reset()` → delegates to L3Orchestrator.reset() for epsilon state

**Verification Checklist**:
- [ ] Output shape (B, T, 1366)
- [ ] Output = cat([cochlea_128, r3_128, brain_1006, l3_104])
- [ ] reset() clears stateful components
- [ ] Works with variable-length audio input
- [ ] Deterministic for same input

---

## Verification Gate G5

```python
from Musical_Intelligence.pipeline import MIPipeline, PipelineConfig
import torch

config = PipelineConfig()
pipeline = MIPipeline(config)

# Generate 3 seconds of audio at 44100 Hz
audio = torch.randn(1, 44100 * 3)
output = pipeline.analyze(audio)

assert output.shape[0] == 1  # batch
assert output.shape[2] == 1366  # MI-space dimension
assert output.shape[1] > 0  # at least 1 frame

# Verify composition
T = output.shape[1]
cochlea_slice = output[:, :, :128]
r3_slice = output[:, :, 128:256]
brain_slice = output[:, :, 256:1262]
l3_slice = output[:, :, 1262:1366]

assert cochlea_slice.shape[-1] == 128
assert r3_slice.shape[-1] == 128
assert brain_slice.shape[-1] == 1006
assert l3_slice.shape[-1] == 104

# Test reset
pipeline.reset()
output2 = pipeline.analyze(audio)
assert output2.shape == output.shape

print("G5 PASSED: MIPipeline produces (B,T,1366) MI-space from audio")
```
