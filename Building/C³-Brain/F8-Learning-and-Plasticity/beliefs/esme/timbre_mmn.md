# timbre_mmn -- Appraisal Belief (ESME)

**Category**: Appraisal (observe-only)
**Owner**: ESME (SPU-gamma2)

---

## Definition

"Instrument sound not as trained." Observes the pre-attentive detection of timbral deviants -- the mismatch negativity response to spectral envelope changes that violate the learned instrument template. This signal is enhanced for the listener's trained instrument timbre: a violinist's auditory cortex generates stronger timbre MMN when violin-specific spectral features deviate from the expected template, compared to deviations in trumpet or other instrument timbres.

---

## Observation Formula

```
# From ESME E-layer + P-layer:
timbre_mmn = 0.60 * f03_timbre_mmn + 0.40 * timbre_deviance_detection

# f03 = sigma(0.40 * timbre_change_std
#            + 0.30 * tristimulus_deviation)
#   timbre_change_std = H3[(24, 8, 3, 0)]  -- timbre_change std 300ms fwd
#   tristimulus_deviation = std([trist1, trist2, trist3])
#     trist1 = H3[(18, 2, 0, 2)]  -- tristimulus1 value 17ms bidi
#     trist2 = H3[(19, 2, 0, 2)]  -- tristimulus2 value 17ms bidi
#     trist3 = H3[(20, 2, 0, 2)]  -- tristimulus3 value 17ms bidi

# timbre_deviance_detection = sigma(timbre_change_std)
#   Current timbre deviance: |current_envelope - template_envelope|
```

No prediction -- observe-only appraisal. The value reflects the current magnitude of timbral mismatch processing.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| ESME E2 | f03_timbre_mmn [2] | Timbre MMN amplitude |
| ESME P2 | timbre_deviance_detection [7] | Current timbre deviance signal |
| H3 | (24, 8, 3, 0) | Timbre change std at 300ms |
| H3 | (18, 2, 0, 2) | Tristimulus1 value at 17ms |
| H3 | (19, 2, 0, 2) | Tristimulus2 value at 17ms |
| H3 | (20, 2, 0, 2) | Tristimulus3 value at 17ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F1 Sensory | Timbre mismatch feeds spectral processing / timbral_character |
| TSCP | Expertise-weighted timbre plasticity feedback loop |
| expertise_enhancement (Core) | Feeds into max(f01, f02, f03) for expertise modulation |

---

## Scientific Foundation

- **Pantev et al. 2001**: Timbre-specific N1m enhancement -- violinists show enhanced cortical response to violin tones but NOT trumpet or pure tones (MEG, N=17, F(1,15)=28.55, p=.00008)
- **Santoyo et al. 2023**: Musicians show enhanced theta phase-locking for timbre-based musical streams -- even without pitch cues (EEG, N=23)
- **Vuust et al. 2012**: Genre-specific timbral expertise -- instrumentalists show enhanced timbre deviance detection for trained spectral profiles

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/esme/esme.py` (Phase 5)
