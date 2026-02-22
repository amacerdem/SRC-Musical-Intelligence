# ESME — Cognitive Present

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | pitch_deviance_detection | Current pitch deviance signal. Represents the absolute deviation of the current pitch from the running template: abs(current_pitch - template_pitch), passed through sigmoid. Captures the real-time pitch MMN signal before expertise modulation. Wagner et al. 2018: pre-attentive harmonic interval MMN = -0.34 uV at 173ms (p = 0.003). Koelsch et al. 1999: violinists detect deviants as small as 0.75%. |
| 6 | rhythm_deviance_detection | Current rhythm deviance signal. Represents the absolute deviation of the current onset timing from the expected onset: abs(current_onset - expected_onset), passed through sigmoid. Captures the real-time rhythm MMN signal. Vuust et al. 2012: jazz musicians show strongest MMN for complex rhythmic deviants. Liao et al. 2024: percussionists' NMR network (putamen, GP, IFG, IPL, SMA) supports distinct rhythm processing. |
| 7 | timbre_deviance_detection | Current timbre deviance signal. Represents the absolute deviation of the current spectral envelope from the template envelope: abs(current_envelope - template_envelope), passed through sigmoid. Captures the real-time timbre MMN signal. Tervaniemi 2022: the parameter most important in performance evokes the largest MMN — for instrumentalists, this is timbre. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 12 | 2 | M0 (value) | L2 (bidi) | Warmth instantaneous 17ms for timbre context |
| 1 | 14 | 5 | M1 (mean) | L0 (fwd) | Tonalness template 46ms for pitch clarity |

---

## Computation

The P-layer decomposes the unified expertise-MMN function into three domain-specific present-moment detection signals. These represent the raw deviance detection happening right now in the auditory system, before expertise modulation.

1. **pitch_deviance_detection**: Computes the absolute pitch change velocity from the E-layer's pitch_change_vel H³ feature and applies sigmoid activation. This captures the pre-attentive pitch deviance signal that generates the pitch MMN component. The signal occurs at approximately 150-250ms post-deviant (Fong et al. 2020).

2. **rhythm_deviance_detection**: Computes the absolute onset timing deviation from the E-layer's onset_val H³ feature and applies sigmoid activation. This captures the temporal deviance signal that generates the rhythm MMN component. Jazz musicians show the strongest response to complex rhythmic deviants (Vuust et al. 2012).

3. **timbre_deviance_detection**: Computes timbre envelope change from the E-layer's timbre_change_std and applies sigmoid activation. This captures the spectral deviance signal that generates the timbre MMN component. The warmth instantaneous feature (H2, 17ms) provides gamma-band timbre context.

These three P-layer dimensions provide the instantaneous deviance signals that the F-layer uses for forward predictions about feature enhancement and expertise transfer.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer pitch_change_vel (H³) | Pitch velocity at 100ms | Raw pitch deviance input |
| E-layer onset_val (H³) | Onset strength at 100ms | Raw rhythm deviance input |
| E-layer timbre_change_std (H³) | Timbre change at 300ms | Raw timbre deviance input |
| R³[12] warmth | Timbre baseline | Context for timbre deviance evaluation |
| R³[14] tonalness | Pitch clarity | Harmonic-to-noise reference for pitch deviance |
| H³ (2 tuples) | Multi-scale temporal morphology | Warmth at gamma and tonalness at alpha-theta |
