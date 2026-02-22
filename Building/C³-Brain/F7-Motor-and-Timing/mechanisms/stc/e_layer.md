# STC — Extraction

**Model**: Singing Training Connectivity
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: E — Extraction
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f28_interoceptive_coupling | Insula-sensorimotor connectivity strength. Captures how strongly the interoceptive monitoring system (insula) is coupled with sensorimotor areas, estimated from interoceptive periodicity at 1s. f28 = sigma(0.40 * interoceptive_period_1s). Zamorano 2023: singing training predicts enhanced insula co-activation with sensorimotor areas (diaphragm, larynx), bilateral thalamus, left putamen. Kleber 2013: right AIC dissociates expertise x anesthesia (F = 22.08, MNI: 48, 0, -3). |
| 1 | f29_respiratory_integration | Respiratory motor control quality. Integrates respiratory periodicity with breath entropy to estimate the quality of breath-phrase coupling for vocal production. f29 = sigma(0.40 * respiratory_period_1s + 0.30 * breath_entropy). Zarate 2008: ACC + pSTS + anterior insula network for compensatory vocal control. Tsunada 2024: dual vocal suppression (phasic gating + tonic prediction) supports separate interoceptive and motor pathways. |
| 2 | f30_speech_sensorimotor | Speech motor area activation level. Estimates the engagement of speech sensorimotor areas from vocal warmth at 100ms, capturing the timbre quality that reflects laryngeal and articulatory motor output. f30 = sigma(0.35 * vocal_warmth_100ms). Kleber 2013: connectivity with M1, S1, auditory cortex; pitch deviation t(728) = -4.8, p < .001. Criscuolo 2022: ALE meta-analysis confirms coherent cortico-subcortical network in musicians. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 33 | 3 | M0 (value) | L2 (bidi) | Interoceptive signal 100ms |
| 1 | 33 | 3 | M2 (std) | L2 (bidi) | Interoceptive variability 100ms |
| 2 | 33 | 8 | M14 (periodicity) | L2 (bidi) | Interoceptive period 500ms |
| 3 | 33 | 16 | M14 (periodicity) | L2 (bidi) | Interoceptive period 1s |
| 4 | 25 | 3 | M0 (value) | L2 (bidi) | Respiratory coupling 100ms |
| 5 | 25 | 8 | M14 (periodicity) | L2 (bidi) | Respiratory period 500ms |
| 6 | 25 | 16 | M14 (periodicity) | L2 (bidi) | Respiratory period 1s |
| 7 | 8 | 3 | M0 (value) | L2 (bidi) | Breath amplitude 100ms |
| 8 | 8 | 3 | M20 (entropy) | L2 (bidi) | Breath entropy 100ms |
| 9 | 12 | 3 | M0 (value) | L2 (bidi) | Vocal warmth 100ms |
| 10 | 15 | 3 | M0 (value) | L2 (bidi) | Voice harmonic 100ms |

---

## Computation

The E-layer extracts three explicit features that characterize the interoceptive-motor integration underlying singing training connectivity. The key insight is that singing uniquely engages respiratory control, vocal production, and interoceptive monitoring in an integrated circuit, and training enhances the resting-state connectivity between these systems (Zamorano 2023).

All features use sigmoid activation with coefficient sums equal to 1.0 (saturation rule).

1. **f28** (interoceptive coupling): Estimates insula-sensorimotor connectivity from the periodicity of the interoceptive signal at 1s. The interoceptive signal (R3 x_l4l5) captures voice-body interactions, and its periodicity at the 1s scale reflects the regularity of interoceptive monitoring. Kleber 2013 provides causal evidence via vocal-fold anesthesia manipulation showing right AIC modulation (F = 22.08).

2. **f29** (respiratory integration): Combines respiratory periodicity at 1s (breath-phrase coupling regularity) with breath entropy at 100ms (uncertainty in breathing pattern). This dual integration captures both the long-term respiratory rhythm and the short-term breath state variability. Tsunada 2024's dual vocal suppression finding (phasic + tonic) supports the separation of fast entropy and slow periodicity pathways.

3. **f30** (speech sensorimotor): Estimates speech motor area engagement from vocal warmth at 100ms. Warmth (R3[12]) reflects the resonance quality of vocal production, providing a timbre-based proxy for laryngeal and articulatory motor output. Criscuolo 2022's meta-analysis (84 studies, 3,005 participants) confirms that musicians show increased volume in sensorimotor and interoceptive regions.

H3 tuples span H3 (100ms) through H16 (1s), exclusively using L2 (bidirectional) laws. The bidirectional processing reflects the inherently reciprocal nature of interoceptive-motor integration -- the insula both monitors and modulates motor output.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3[7] amplitude | Vocal intensity | Voice production amplitude |
| R3[8] loudness | Respiratory amplitude | Breath monitoring and entropy |
| R3[12] warmth | Vocal warmth | Singing resonance quality for speech sensorimotor |
| R3[15] tristimulus1 | Harmonic balance | Voice timbre fundamental energy |
| R3[16] tristimulus2 | Mid-harmonic energy | Vocal quality mid-frequency content |
| R3[17] tristimulus3 | High-harmonic energy | Vocal brightness |
| R3[21] spectral_change | Vocal dynamics | Phrase transition detection |
| R3[25:33] x_l0l5 | Respiratory timing | Breath-phrase coupling signal |
| R3[33:41] x_l4l5 | Interoceptive-motor | Voice-body connection signal |
| H3 (11 tuples) | Multi-scale temporal morphology | Interoceptive, respiratory, and vocal dynamics at 100ms-1s |
