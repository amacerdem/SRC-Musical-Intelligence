# attention_capture — Core Belief (IACM)

**Category**: Core (full Bayesian PE)
**tau**: 0.25
**Owner**: IACM (ASU-alpha2)
**Multi-Scale**: 4 horizons, T_char = 400ms

---

## Definition

"Inharmonic sound captures involuntary attention." Tracks how strongly inharmonic spectral events recruit involuntary attention via the P3a mechanism. High values indicate a salient inharmonic event has triggered an attention switch — the brain is reorienting to an unexpected spectral event.

---

## Multi-Scale Horizons

```
H3(25ms)  H5(46ms)  H7(250ms)  H10(400ms)
```

T_char = 400ms reflects the characteristic timescale of the P3a ERP component. Short horizons (H3, H5) capture the onset of inharmonic events; H7 spans the P3a peak latency; H10 captures the full attention capture and reorientation cycle.

---

## Observation Formula

```
energy = 0.6 * amplitude + 0.4 * onset
h3_change = max(|vel_amp|, |vel_onset|, |vel_flux|)  # beat scale
            * 0.60 + phrase_scale * 0.40

# 4-signal mixing (with relays):
base = 0.25 * energy + 0.25 * h3_change + 0.15 * |PE_prev| + 0.35 * relay
value = 0.5 * base + 0.5 * max(all signals)   # peak preservation

# Precision: (0.5 * energy + 0.5 * h3_change) * 10, clamped [0.5, 10]
```

Relay components: IACM.p3a_capture[P0] + IACM.attention_capture[M0].

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| IACM P0 | p3a_capture [6] | Primary P3a attention state |
| IACM M0 | attention_capture [3] | P3a-proportional capture level |
| IACM E0 | inharmonic_capture [0] | Raw inharmonic detection |
| IACM M1 | approx_entropy [4] | Spectral unpredictability |
| R3 [7] | amplitude | Energy component |
| R3 [10] | spectral_flux (onset_strength) | Onset component |

---

## Scientific Foundation

- **Basinski 2025**: P3a amplitude d=-1.37 for inharmonic vs harmonic (EEG, N=35)
- **Koelsch 1999**: P3a involuntary attention to spectral deviants in music
- **Friston 2005**: Precision-weighted prediction errors drive attention
- **Alain 2007**: ORN and P3a as dual indices of auditory scene analysis

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/attention_capture.py` (pending)
