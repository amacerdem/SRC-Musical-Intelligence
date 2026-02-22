# medium_context — Appraisal Belief (HMCE)

**Category**: Appraisal (observe-only)
**Owner**: HMCE (STU-α1)

---

## Definition

"Current phrase-sequence follows pattern Y." Observes the medium-timescale context encoding in superior temporal gyrus (STG), corresponding to transformer layers 5-9. Captures phrase-level musical patterns — sequences of 50-100 notes spanning ~5 seconds. High values indicate that the STG is actively encoding phrase structure, cadential patterns, and harmonic progressions at the sentence-of-music timescale.

---

## Observation Formula

```
# From HMCE E-layer:
medium_context = HMCE.f02_medium_context[E1]  # index [1]

# Formula: sigma(0.85 * energy_mean * loudness_mean)
# where energy_mean   = H3[(22, 14, 1, 0)]   energy_change mean at H14 (700ms)
#       loudness_mean  = H3[(8, 14, 1, 0)]    loudness mean at H14 (700ms)
```

No prediction — observe-only appraisal. The value reflects the current state of medium-context encoding at the STG level, driven by energy dynamics and loudness at the beat/phrase timescale (H14 = 700ms).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE E1 | f02_medium_context [1] | Medium context encoding (STG) |
| H³ | (22, 14, 1, 0) | Energy change mean at H14 |
| H³ | (22, 14, 13, 0) | Energy change entropy at H14 |
| H³ | (23, 14, 1, 0) | Pitch change mean at H14 |
| H³ | (23, 14, 3, 0) | Pitch change std at H14 |
| H³ | (7, 14, 18, 0) | Amplitude trend at H14 |
| H³ | (8, 14, 1, 0) | Loudness mean at H14 |
| R³ [7] | amplitude | Intensity dynamics |
| R³ [8] | loudness | Perceptual intensity |

---

## Kernel Usage

The medium_context appraisal provides phrase-level context to downstream beliefs:

```python
# Phase 0 in scheduler — feeds context_depth Core Belief:
# context_depth = (1 * f01 + 2 * f02 + 3 * f03) / 6
# where f02 = medium_context (weighted 2x vs short)

# Also feeds period_entrainment via HMCE blend:
# HMCE_context = 0.40 * A1 + 0.35 * STG + 0.25 * MTG
# where STG encoding is driven by medium_context features

# Feeds phrase_boundary_pred anticipation belief:
# entropy_energy at H14 signals unpredictability → boundary detection
```

Medium context is the middle layer of the hierarchical gradient, weighted 2x in context_depth relative to short context. It bridges local motif encoding and global structure tracking.

---

## Scientific Foundation

- **Mischler 2025**: STG encodes 50-100 notes context, corresponding to transformer layers 5-9 (ECoG, r=0.99 site-level; ~10mm from pmHG)
- **Norman-Haignere 2022**: Intermediate auditory cortex integration window ~136ms; spectrotemporal to category transition (iEEG, 18 patients)
- **Bellier 2023**: STG anterior-posterior gradient for music; posterior=onset, anterior=sustained (iEEG, 29 patients, F=25.09)
- **Potes 2012**: STG high-gamma tracks music intensity (r=0.43-0.58); STG to motor cortex lag 110ms (ECoG, N=8)
- **Wöhrle 2024**: Context accumulates over 4-chord progressions; N1m diverges progressively (MEG, N=30, eta_p^2=0.101)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
