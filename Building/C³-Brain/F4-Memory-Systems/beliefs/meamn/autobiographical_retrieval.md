# autobiographical_retrieval — Core Belief (MEAMN)

**Category**: Core (full Bayesian PE)
**τ**: 0.85
**Owner**: MEAMN (IMU-α1)
**Multi-Scale**: 8 horizons, T_char = 8s

---

## Definition

"I remember this." Music uniquely activates autobiographical memory through hippocampal-mPFC-PCC hub engagement. This is the primary F4 belief — the degree to which the listener is experiencing music-evoked autobiographical memory (MEAM). The highest τ in the system (0.85) reflects that retrieved memories do not vanish between frames; once a memory is activated, it persists and deepens over seconds.

---

## Multi-Scale Horizons

```
H10(400ms)  H13(600ms)  H16(1s)  H18(2s)
H21(8s)     H24(36s)    H28(414s)  H30(800s)
```

T_char = 8s reflects the characteristic timescale of autobiographical memory retrieval. Short horizons (H10, H13) capture the initial recognition flash; H16–H18 track the retrieval buildup; H21 is the primary retrieval scale where MEAMs fully emerge; H24–H28 capture sustained reminiscence across musical sections; H30 tracks session-level autobiographical engagement.

---

## Observation Formula

```
# Implicit (65%): H³ periodicity + stability
period_signal = mean(M14(tonalness, key_clarity, tonal_stability))
stability = mean(1 / (1 + 5×M2(features)))
implicit = 0.50×periodicity + 0.35×stability + 0.15×R³_tonal

# Explicit (35%): MEAMN memory
explicit = 0.60×memory_state + 0.25×emotional_color + 0.15×self_ref

# Combined: (0.65×implicit + 0.35×explicit) × energy_gate
# Energy gate: σ(10 × (energy − 0.1))

# Precision: 1/(std(3 periodicity features) + 0.1) × gate
#            + MEAMN: 0.3×(memory×nostalgia) + 0.2×self_ref + 0.1×vividness
```

The implicit pathway captures the acoustic basis for memory activation: tonal periodicity and spectral stability are the features that make music "recognizable." The explicit pathway reads the MEAMN relay's computed memory state. The 65/35 split reflects that memory activation is primarily driven by bottom-up acoustic features, with top-down memory state confirming and amplifying.

Relay components: MEAMN.memory_state[P0] + MEAMN.emotional_color[P1] + MEAMN.nostalgia_link[P2] + MEAMN.self_ref_fc[F2].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.85, the prediction is dominated by the previous frame's value — memory retrieval is highly autocorrelated. M18 (trend) and M14 (periodicity) provide slow corrections. Context from beliefs_{t-1} includes nostalgia_intensity and emotional_coloring, which modulate the memory prediction.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN P0 | memory_state [5] | Primary memory retrieval activation (40%) |
| MEAMN P1 | emotional_color [6] | Affective tag strength (30%) |
| MEAMN E0 | f01_retrieval [0] | Hippocampal retrieval signal (30%) |
| H³ M14 | periodicity (tonalness, key_clarity, tonal_stability) | Implicit tonal familiarity |
| H³ M2 | std (features) | Implicit spectral stability |
| R³ tonal | tonal features | Baseline tonal quality |

---

## Scientific Foundation

- **Janata 2009**: Dorsal MPFC (BA 8/9) parametrically tracks tonal space movement during autobiographically salient songs; left-lateralized FAV (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Sakakibara et al. 2025**: Acoustic similarity alone triggers nostalgia — timbral warmth and consonance are sufficient (EEG, N=33, eta_p^2=0.636)
- **Belfi et al. 2016**: Music-evoked autobiographical memories are more vivid and emotional than word-cued memories (behavioral, N=31)
- **Janata et al. 2007**: 30-80% MEAM trigger rate; reminiscence bump ages 10-30 (behavioral, N~300)

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/autobiographical_retrieval.py`
