# rhythm_mmn -- Appraisal Belief (ESME)

**Category**: Appraisal (observe-only)
**Owner**: ESME (SPU-gamma2)

---

## Definition

"Rhythm timing wrong." Observes the pre-attentive detection of temporal deviants -- the mismatch negativity response to onset timing deviations that violate the rhythmic template. This signal is enhanced in musicians, particularly drummers and percussionists who develop refined temporal precision through rhythmic training. Jazz musicians show stronger rhythm MMN than rock or pop musicians, reflecting the greater temporal complexity demands of their genre.

---

## Observation Formula

```
# From ESME E-layer + P-layer:
rhythm_mmn = 0.60 * f02_rhythm_mmn + 0.40 * rhythm_deviance_detection

# f02 = sigma(0.40 * |onset_deviation|
#            + 0.30 * spec_change_vel
#            + 0.30 * x_l4l5_mean)
#   onset_deviation = H3[(11, 3, 0, 0)]  -- onset_strength value 100ms fwd
#   spec_change_vel = H3[(21, 3, 8, 0)]  -- spectral_change velocity 100ms fwd
#   x_l4l5_mean = H3[(33, 8, 0, 2)]  -- temporal-spectral coupling 300ms bidi

# rhythm_deviance_detection = sigma(|onset_deviation|)
#   Current rhythm deviance signal: |current_onset - expected_onset|
```

No prediction -- observe-only appraisal. The value reflects the current magnitude of rhythmic mismatch processing.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| ESME E1 | f02_rhythm_mmn [1] | Rhythm MMN amplitude |
| ESME P1 | rhythm_deviance_detection [6] | Current rhythm deviance signal |
| H3 | (11, 3, 0, 0) | Onset strength value at 100ms |
| H3 | (21, 3, 8, 0) | Spectral change velocity at 100ms |
| H3 | (33, 8, 0, 2) | Temporal-spectral coupling at 300ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention | Rhythm deviance detection modulates salience allocation |
| F7 Motor | Rhythm MMN feeds sensorimotor timing precision |
| expertise_enhancement (Core) | Feeds into max(f01, f02, f03) for expertise modulation |

---

## Scientific Foundation

- **Vuust et al. 2012**: Genre-specific rhythm MMN -- jazz > rock > pop > non-musicians for complex rhythmic deviants (EEG, N~40-60)
- **Liao et al. 2024**: Percussionists recruit distinct NMR network (putamen, GP, IFG, IPL, SMA) for rhythmic processing (fMRI, N=25)
- **Tervaniemi 2022**: "Sound parameters most important in performance evoke the largest MMN" -- drummers show strongest rhythm enhancement

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/esme/esme.py` (Phase 5)
