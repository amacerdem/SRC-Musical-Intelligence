# AMSC — Cognitive Present

**Model**: Auditory-Motor Stream Coupling
**Unit**: STU
**Function**: F7 Motor & Timing
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | auditory_activation | pSTG current activation state. Measures real-time auditory cortex intensity tracking. Driven by amplitude × loudness at beat level. High values = strong auditory encoding driving motor pathway. Maps to pSTG high-gamma. Bellier 2023: right STG dominance for music (F=7.48). |
| 7 | motor_preparation | Premotor preparation state. Measures readiness of the motor system to synchronize with auditory input. Combines motor coupling from E-layer with f02 motor gamma. The dorsal stream automatically engages motor cortex during passive listening. Maps to dorsal precentral gyrus. |
| 8 | onset_trigger | Motor trigger from onset detection. Measures precision of beat-level event detection from spectral flux × onset strength at H6. Sharp onsets produce high values, enabling precise motor-auditory synchronization. Maps to the onset detection circuit in the dorsal auditory pathway. |

---

## H³ Demands

No additional unique H³ demands beyond E/M layers. The P-layer reuses:
- spectral_flux value from (10, 6, M0, L0)
- onset_strength value from (11, 6, M0, L0)

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E/M layer tuples |

---

## Computation

The P-layer computes the real-time state of the auditory-motor coupling system:

1. **Auditory activation** (idx 6): Current pSTG activation from intensity tracking. Combines amplitude and loudness at beat level. Reflects bottom-up auditory encoding that automatically engages motor cortex (Grahn & Brett 2007).

2. **Motor preparation** (idx 7): Premotor readiness combining motor coupling context with f02 motor gamma signal. Higher when both auditory input is strong and motor pathway is engaged. Reflects the 110ms-delayed automatic motor response.

3. **Onset trigger** (idx 8): Beat-event motor trigger from spectral flux × onset strength. Sharp, well-defined onsets produce the motor synchronization anchors that enable precise auditory-motor coupling. Formula: σ(flux_val × onset_val).

All outputs are sigmoid-bounded to [0, 1].

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_auditory_gamma, f02_motor_gamma | Gamma signals for activation/preparation |
| R³ [10] | spectral_flux | Onset detection for motor trigger |
| R³ [11] | onset_strength | Event boundary for motor synchronization |
| H³ (shared) | Reuses E-layer tuples | Current-state features at H6 |
