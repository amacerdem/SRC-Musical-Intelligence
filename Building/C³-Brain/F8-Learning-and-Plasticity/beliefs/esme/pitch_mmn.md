# pitch_mmn -- Appraisal Belief (ESME)

**Category**: Appraisal (observe-only)
**Owner**: ESME (SPU-gamma2)

---

## Definition

"Pitch deviates from expectation." Observes the pre-attentive detection of pitch deviants -- the mismatch negativity response to pitch changes that violate the auditory template. This signal is enhanced in musicians, particularly singers and violinists who develop refined pitch discrimination through vocal/string training. The effect is a gradient: strongest in the trained pitch domain, with general enhancement over non-musicians.

---

## Observation Formula

```
# From ESME E-layer + P-layer:
pitch_mmn = 0.60 * f01_pitch_mmn + 0.40 * pitch_deviance_detection

# f01 = sigma(0.40 * |pitch_change_vel|
#            + 0.30 * |helmholtz_diff|
#            + 0.30 * onset_val)
#   pitch_change_vel = H3[(23, 3, 8, 0)]  -- pitch_change velocity 100ms fwd
#   helmholtz_diff = |helmholtz_val - helmholtz_mean|  -- consonance deviance
#   onset_val = H3[(11, 3, 0, 0)]  -- onset_strength value 100ms fwd

# pitch_deviance_detection = sigma(|pitch_change_vel|)
#   Current pitch deviance signal: |current_pitch - template_pitch|
```

No prediction -- observe-only appraisal. The value reflects the current magnitude of pitch mismatch processing.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| ESME E0 | f01_pitch_mmn [0] | Pitch MMN amplitude |
| ESME P0 | pitch_deviance_detection [5] | Current pitch deviance signal |
| H3 | (23, 3, 8, 0) | Pitch change velocity at 100ms |
| H3 | (2, 0, 0, 2) | Helmholtz consonance value at 25ms |
| H3 | (2, 3, 1, 2) | Helmholtz consonance mean at 100ms |
| H3 | (11, 3, 0, 0) | Onset strength value at 100ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F3 Attention | Pitch deviance detection modulates salience allocation |
| expertise_enhancement (Core) | Feeds into max(f01, f02, f03) for expertise modulation |
| Precision engine | Pitch MMN magnitude informs prediction precision |

---

## Scientific Foundation

- **Koelsch et al. 1999**: Violinists show MMN to 0.75% pitch deviants in major chord triads; MMN absent in non-musicians (EEG, N~20/group)
- **Wagner et al. 2018**: Pre-attentive harmonic interval MMN = -0.34 uV at 173ms for major third deviants (EEG, N=15, p=0.003)
- **Tervaniemi 2022**: Pitch MMN paradigm -- domain-specific enhancement gradient

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/esme/esme.py` (Phase 5)
