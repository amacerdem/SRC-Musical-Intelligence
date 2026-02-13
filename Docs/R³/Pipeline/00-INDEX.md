# R3 Pipeline -- Index

**Scope**: Execution pipeline documentation for the R3 spectral feature extraction system.
**Status**: Current (v1, 49D sequential) with Phase 6 planned changes (v2, 128D DAG-ordered) annotated throughout.

---

## Pipeline Documents

| # | Document | Subject |
|---|----------|---------|
| 1 | [DependencyDAG.md](DependencyDAG.md) | Group dependency graph, stage ordering, GPU parallelization |
| 2 | [Normalization.md](Normalization.md) | [0,1] normalization contract, methods, per-group choices, known issues |
| 3 | [Performance.md](Performance.md) | Frame-level budget, per-group costs, real-time feasibility |
| 4 | [StateManagement.md](StateManagement.md) | Stateful vs stateless features, warm-up, running statistics, reset |

---

## Pipeline Summary

The R3 pipeline transforms a log-mel spectrogram into a fixed-dimensional feature vector at every audio frame:

```
Audio (44.1kHz)
      |
      | STFT (n_fft=2048, hop=256)
      v
Mel Spectrogram (B, 128, T) @ 172.27 Hz
      |
      | R3Extractor.extract()
      v
R3Output (B, T, 49)   -- v1 current
R3Output (B, T, 128)  -- v2 Phase 6
```

### Key Parameters

| Parameter | Value | Derivation |
|-----------|-------|-----------|
| Sample rate | 44,100 Hz | Standard audio |
| STFT hop length | 256 samples | ~5.8 ms per frame |
| Frame rate | 172.27 Hz | 44100 / 256 |
| Frame budget | 5.8 ms | 1 / 172.27 Hz |
| Mel bins | 128 | Standard mel filterbank |
| R3 dimensions (v1) | 49 | Groups A-E |
| R3 dimensions (v2) | 128 | Groups A-K |
| Groups (v1) | 5 | Consonance, Energy, Timbre, Change, Interactions |
| Groups (v2) | 11 | + Pitch, Rhythm, Harmony, Information, Timbre Ext., Modulation |

### Current vs Phase 6

| Aspect | Current (v1) | Phase 6 (v2) |
|--------|-------------|--------------|
| Execution order | Sequential (no dependency awareness) | 3-stage DAG |
| Parallelism | None | GPU multi-stream per stage |
| Dependency injection | None (proxies used) | `compute_with_deps(mel, outputs)` |
| Stateful features | Groups A-E are stateless | Groups I, K require running state |
| Warm-up handling | Not applicable | Linear confidence ramp over 344 frames |
| Total latency | ~0.5ms (49D, sequential) | ~2.5ms amortized (128D, parallel) |

---

## Related Documentation

- **Contracts/**: Interface specifications for BaseSpectralGroup, Registry, Extractor
- **R3-V2-DESIGN.md**: Full architecture design (Section 3: Pipeline, Section 5: Code changes)
- **Domains/**: Per-domain feature specifications
- **Standards/**: Naming and format conventions
