# AAC Extraction — Emotional Arousal + Autonomic Markers (7D)

**Layer**: Extraction (E+A)
**Indices**: [0:7]
**Scope**: internal
**Activation**: sigmoid / tanh (f06_ans_response only)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 0 | E0:f04_emotional_arousal | [0, 1] | Activation/deactivation dimension. f00 = sigma(0.50 * arousal_signal + 0.40 * salience_signal + 0.10 * energy_level_H9). Amygdala + insula arousal circuit. Egermann 2013: unexpected events drive strongest ANS response. |
| 1 | E1:f06_ans_response | [-1, 1] | Composite ANS marker. f01 = tanh(0.35 * scr_z + 0.40 * (1 - hr_z) + 0.25 * respr_z). Positive = sympathetic dominance, negative = parasympathetic dominance. Berntson 1991: 2D autonomic space model. |
| 2 | A0:scr | [0, 1] | Skin Conductance Response proxy. f02 = sigma(0.40 * arousal + 0.35 * velocity_signal_H9 + 0.25 * accel_signal_H9). Sympathetic-only (eccrine glands). 1-3.5s onset. Fancourt 2020: meta-pooled d=0.85. |
| 3 | A1:hr | [0, 1] | Heart Rate proxy (normalized). f03 = sigma(0.50 * (1 - arousal * 0.6) + 0.30 * tempo_signal_H16 + 0.20 * stability_H19). INVERTED at peaks (vagal brake). Rickard 2004: biphasic HR pattern. Peng 2022: PEP-down + RSA-up = cardiac co-activation. |
| 4 | A2:respr | [0, 1] | Respiration Rate proxy. f04 = sigma(0.40 * arousal + 0.30 * periodicity_H16 + 0.30 * energy_velocity_H16). Entrains to beat (Janata 2012). Etzel 2006: breath-holding at peak moments. Fancourt 2020: d=0.45. |
| 5 | A3:bvp | [0, 1] | Blood Volume Pulse proxy. f05 = sigma(0.50 * (1 - arousal * 0.5) + 0.30 * stability_H19 + 0.20 * baseline_H19). INVERTED: high arousal = vasoconstriction = low BVP. Alpha-adrenergic, 0.5-1s onset. |
| 6 | A4:temp | [0, 1] | Peripheral Temperature proxy. f06 = sigma(0.50 * baseline_H19 + 0.30 * (1 - arousal * 0.3) + 0.20 * stability_H19). SLOWEST response (10-30s). Weakest marker, d=0.15-0.25 meta-pooled. |

---

## Design Rationale

1. **Emotional Arousal (E0)**: The primary arousal dimension — measures activation level of the emotional system. Integrates shared arousal signal (from SRP affective dynamics), auditory salience (event significance), and direct energy level at 350ms (H9). This drives all downstream autonomic markers. Amygdala evaluation + anterior insula interoceptive awareness circuit.

2. **ANS Response (E1)**: Composite autonomic balance indicator. Uses z-scored versions of SCR, HR (inverted), and RespR to produce a bipolar signal: positive = sympathetic dominance (fight-or-flight), negative = parasympathetic dominance (rest-and-digest). The co-activation paradox at chills (SCR up + HR down simultaneously) places the response in Berntson's co-activation quadrant.

3. **SCR (A0)**: Purely sympathetic marker via eccrine sweat glands. Rises with arousal, energy velocity (crescendo), and energy acceleration (onset attacks). Onset 1-3.5s, fastest reliable ANS marker. Ferreri 2019: levodopa causally increases SCR (t=-2.26, p=0.033).

4. **HR (A1)**: Biphasic cardiac marker. Brief acceleration (+2-5 BPM, 0.5s) then sustained deceleration (-3 to -8 BPM, 2-5s) at peak emotional moments. INVERTED with arousal: high emotional intensity activates the vagal brake. Tempo modulates baseline: fast tempo raises HR independently of emotion.

5. **RespR (A2)**: Respiration rate rises with arousal and entrains to musical beat (Janata 2012). Brief apnea (breath-holding) at exact peak moments before RespR rises (Etzel 2006). Beat periodicity at H16 captures rhythmic entrainment component.

6. **BVP (A3)**: Blood volume pulse decreases with arousal due to peripheral vasoconstriction (alpha-adrenergic). Inverted relationship: high arousal = low BVP amplitude. Modulated by baseline stability (homeostatic reference at H19 3s window).

7. **Temp (A4)**: Peripheral temperature is the slowest ANS marker (10-30s onset) and weakest signal (d=0.15-0.25). Decreases with prolonged sympathetic activation. Dominated by baseline state with arousal as a minor modulator.

---

## H3 Dependencies (Extraction)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (7, 9, 4, 2) | amplitude max H9 L2 | energy_level — current peak energy at 350ms |
| (7, 9, 8, 2) | amplitude velocity H9 L2 | velocity_signal — rate of energy change at 350ms |
| (7, 9, 11, 2) | amplitude acceleration H9 L2 | accel_signal — onset acceleration at 350ms |
| (10, 9, 14, 2) | spectral_flux periodicity H9 L2 | periodicity_h9 — beat clarity at 350ms |
| (10, 16, 14, 2) | spectral_flux periodicity H16 L2 | tempo_signal — bar-level tempo at 1s |
| (7, 16, 8, 2) | amplitude velocity H16 L2 | energy_velocity — bar-level dynamics at 1s |
| (7, 19, 19, 2) | amplitude stability H19 L2 | stability — baseline ANS reference at 3s |
| (7, 19, 1, 2) | amplitude mean H19 L2 | baseline — homeostatic reference at 3s |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [7] | amplitude | E0: energy level, A0: SCR driver |
| [10] | spectral_flux | A2: beat periodicity, A4: onset rate |
| [11] | onset_strength | A0: SCR onset acceleration |

---

## Scientific Foundation

- **Egermann 2013**: Unexpected events -> SCR up, HR down. d=2.5 (SCR), d=6.0 (HR) context-specific (live concert + physiology, N=25-50)
- **Fancourt 2020**: Meta-pooled effect sizes: SCR d=0.85, HR d=0.8-1.5, RespR d=0.45 (meta-analysis, k=26)
- **Ferreri 2019**: Levodopa -> SCR up (t=-2.26, p=0.033). DA causally drives ANS (pharmacology, N=27)
- **Peng 2022**: PEP shortened (d=-0.45) + RSA increased (d=+0.38) simultaneously = cardiac co-activation (impedance cardiography)
- **Rickard 2004**: Biphasic HR pattern — brief accel then sustained decel (psychophysiology)
- **Etzel 2006**: Breath-holding at peak emotional moments (respiratory analysis)
- **Janata 2012**: Respiratory entrainment to musical beat (sensorimotor coupling)
- **Berntson 1991**: 2D autonomic space model — co-activation quadrant (Psychophysiology)
- **Gomez & Danuser 2007**: SCR, HR, RespR, Temp all respond; arousal dominance factor (N=48)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/aac/extraction.py`
