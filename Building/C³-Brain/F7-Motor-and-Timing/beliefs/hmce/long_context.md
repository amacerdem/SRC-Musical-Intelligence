# long_context — Appraisal Belief (HMCE)

**Category**: Appraisal (observe-only)
**Owner**: HMCE (STU-α1)

---

## Definition

"Section turning into/departing from form Z." Observes the long-timescale context encoding in middle temporal gyrus (MTG) and beyond, corresponding to transformer layers 10-12 (and layer 13 for musicians). Captures section-level and form-level musical structure — sequences of 100-300+ notes spanning 15-30+ seconds. High values indicate deep structural encoding: the listener is tracking large-scale form (sonata structure, verse-chorus patterns, thematic return).

---

## Observation Formula

```
# From HMCE E-layer:
long_context = HMCE.f03_long_context[E2]  # index [2]

# Formula: sigma(0.80 * x_coupling * autocorr)
# where x_coupling = H3[(25, 20, 1, 0)]   x_l0l5 mean at H20 (5000ms)
#       autocorr   = H3[(33, 20, 22, 0)]  x_l4l5 autocorrelation at H20 (5000ms)
```

No prediction — observe-only appraisal. The value reflects the current state of long-context encoding at the MTG level, driven by cross-feature coupling and self-similarity detection at the section timescale (H20 = 5000ms).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE E2 | f03_long_context [2] | Long context encoding (MTG) |
| HMCE E4 | f05_expertise [4] | Musician advantage modulation (d=0.32) |
| H³ | (25, 20, 1, 0) | x_l0l5 mean at H20 (foundation coupling) |
| H³ | (25, 20, 13, 0) | x_l0l5 entropy at H20 (unpredictability) |
| H³ | (33, 20, 1, 0) | x_l4l5 mean at H20 (dynamics coupling) |
| H³ | (33, 20, 22, 0) | x_l4l5 autocorrelation at H20 (self-similarity) |
| H³ | (33, 20, 19, 0) | x_l4l5 stability at H20 (temporal stability) |
| H³ | (25, 20, 22, 0) | x_l0l5 autocorrelation at H20 (section repetition) |
| H³ | (8, 20, 18, 0) | Loudness trend at H20 (long-range dynamics) |

---

## Kernel Usage

The long_context appraisal provides section/form-level context to downstream beliefs:

```python
# Phase 0 in scheduler — feeds context_depth Core Belief:
# context_depth = (1 * f01 + 2 * f02 + 3 * f03) / 6
# where f03 = long_context (weighted 3x vs short)

# Also feeds period_entrainment via HMCE blend:
# HMCE_context = 0.40 * A1 + 0.35 * STG + 0.25 * MTG
# where MTG encoding is driven by long_context features

# Feeds structure_pred anticipation belief:
# autocorrelation at H20 detects section return/departure
```

Long context is the deepest layer of the hierarchical gradient, weighted 3x in context_depth relative to short context. Musicians extend this to 300+ notes (layer 13, temporal pole), modulated by the expertise factor (d=0.32).

---

## Scientific Foundation

- **Mischler 2025**: MTG encodes 100-200 notes context, layers 10-12; musicians extend to 300+ notes at layer 13 (d=0.32, p=3.8e-08; ECoG+EEG, N=26)
- **Norman-Haignere 2022**: Non-primary STG integration window ~274ms; category-level encoding (iEEG, 18 patients, beta=0.064 oct/mm)
- **Bonetti 2024**: Hierarchical feedforward AC to hippocampus to cingulate; expertise modulates later contextual tones (BOR=2.91e-07; MEG, N=83)
- **Golesorkhi 2021**: DMN/FPN have longest autocorrelation windows (d=-0.66 to -2.03); core-periphery temporal hierarchy (MEG, N=89)
- **Fedorenko 2012**: Bilateral temporal regions sensitive to musical structure, dissociated from language (fMRI, N=12)
- **Sabat 2025**: Basic integration gradient may be hardwired; expertise may operate via attention/top-down feedback (single-unit, ferret)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
