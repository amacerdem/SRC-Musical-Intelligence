# short_context — Appraisal Belief (HMCE)

**Category**: Appraisal (observe-only)
**Owner**: HMCE (STU-α1)

---

## Definition

"Current motif/phrase (10-50 notes): X." Observes the short-timescale context encoding in primary auditory cortex (pmHG / A1), corresponding to transformer layers 1-4. Captures the immediate motif-level musical context — what has just happened within the last ~1 second. High values indicate strong local feature encoding of recent spectral and onset events.

---

## Observation Formula

```
# From HMCE E-layer:
short_context = HMCE.f01_short_context[E0]  # index [0]

# Formula: sigma(0.90 * flux_mean * onset_val)
# where flux_mean  = H3[(10, 8, 1, 0)]   spectral_flux mean at H8 (300ms)
#       onset_val  = H3[(11, 8, 0, 0)]   onset_strength value at H8 (300ms)
```

No prediction — observe-only appraisal. The value reflects the current state of short-context encoding at the pmHG level, driven by spectral flux and onset strength at the syllable/motif timescale (H8 = 300ms).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| HMCE E0 | f01_short_context [0] | Short context encoding (pmHG) |
| H³ | (10, 8, 1, 0) | Spectral flux mean at H8 |
| H³ | (11, 8, 0, 0) | Onset strength value at H8 |
| H³ | (21, 8, 1, 0) | Spectral change mean at H8 |
| H³ | (21, 8, 8, 0) | Spectral change velocity at H8 |
| R³ [10] | spectral_flux (onset_strength) | Onset/transition detection |
| R³ [11] | onset_strength | Event boundary marking |

---

## Kernel Usage

The short_context appraisal provides motif-level context information to downstream beliefs:

```python
# Phase 0 in scheduler — feeds context_depth Core Belief:
# context_depth = (1 * f01 + 2 * f02 + 3 * f03) / 6
# where f01 = short_context

# Also feeds period_entrainment via HMCE blend:
# HMCE_context = 0.40 * A1 + 0.35 * STG + 0.25 * MTG
# where A1 encoding is driven by short_context features
```

Short context establishes the bottom layer of the hierarchical gradient. It provides the motif-level feature base upon which medium and long context build.

---

## Scientific Foundation

- **Mischler 2025**: pmHG encodes 10-50 notes context, corresponding to transformer layers 1-4 (ECoG, r=0.99 site-level gradient)
- **Norman-Haignere 2022**: Primary auditory cortex integration window ~74ms (iEEG, 18 patients, beta=0.064 oct/mm)
- **Briley 2013**: Medial HG (tonotopic) encodes basic features; 7-8mm anterolateral shift to pitch chroma (EEG source, N=15, F=29.865)
- **Sabat 2025**: Primary cortex integration windows ~15ms, invariant to stimulus context (single-unit, ferret)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/hmce_relay.py`
