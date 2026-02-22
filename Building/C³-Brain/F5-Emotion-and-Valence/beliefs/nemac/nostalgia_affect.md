# nostalgia_affect — Core Belief (NEMAC)

**Category**: Core (full Bayesian PE)
**τ**: 0.65
**Owner**: NEMAC (F5)
**Multi-Scale**: single-scale in v1.0, T_char = 5s

---

## Definition

"I feel nostalgic." Tracks the FELT nostalgia experience — the bittersweet emotional response triggered by familiar music. Nostalgia is a complex, mixed-valence emotion combining warmth, longing, and autobiographical self-relevance. Higher τ than other F5 beliefs (0.65 vs 0.5) reflects nostalgia's slow build and persistence: once triggered, the nostalgic state lingers across musical phrases and does not rapidly fluctuate. The primary neural substrate is the mPFC-hippocampus-PCC circuit for self-referential autobiographical processing.

---

## Multi-Scale Horizons

```
Single-scale in v1.0: H20 (5s)
```

T_char = 5s reflects the characteristic timescale of nostalgic experience. Nostalgia builds over seconds as familiarity recognition cascades into autobiographical retrieval and self-referential processing. Future multi-scale expansion would add H16 (1s) for initial nostalgia recognition cues, H24 (36s) for sustained nostalgic episodes across sections, and H28 (414s) for session-level nostalgic engagement.

---

## Observation Formula

```
# Implicit (55%): H3 warmth + tonal stability
warmth = H3(12, 20, 1, 0)        # warmth mean H20 L0 — sustained warmth
tonal = H3(14, 20, 1, 0)         # tonalness mean H20 L0 — tonal stability
roughness_inv = 1 - H3(0, 20, 18, 0)  # inverse roughness trend — consonance trajectory

implicit = 0.45 * warmth + 0.30 * tonal + 0.25 * roughness_inv

# Explicit (45%): NEMAC P-layer + MEAMN relay
nostalgia_correl = NEMAC.nostalgia_correl[P0]   # index [7]
memory_reward = NEMAC.memory_reward_lnk[P1]      # index [8]
meamn_nostalgia = MEAMN.nostalgia_link[P2]        # cross-relay

explicit = 0.40 * nostalgia_correl + 0.30 * memory_reward + 0.30 * meamn_nostalgia

# Combined: (0.55 * implicit + 0.45 * explicit) * energy_gate
# Energy gate: sigma(10 * (energy - 0.1))

# Precision: 1/(std(warmth, tonal, roughness_inv) + 0.1) * gate
#            + NEMAC: 0.3 * nostalgia_correl + 0.2 * memory_reward
```

The implicit pathway captures the acoustic basis for nostalgia: timbral warmth, tonal stability, and consonance are the spectral features that make music sound "nostalgic." The explicit pathway reads the NEMAC relay's computed nostalgia correlate and memory-reward link, plus the cross-relay MEAMN nostalgia signal. The 55/45 split reflects that nostalgia requires both bottom-up acoustic cues and top-down memory/self-referential processing.

Relay components: NEMAC.nostalgia_correl[P0] + NEMAC.memory_reward_lnk[P1] + MEAMN.nostalgia_link[P2].

---

## Prediction Formula

```
predict = Linear(τ * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.65, the prediction is moderately dominated by the previous frame's value — nostalgia persists across frames but can shift with changing musical context. M18 (trend) captures warmth and tonal trajectory. M14 (periodicity) captures tonal periodicity stability. Context from beliefs_{t-1} includes autobiographical_retrieval (F4) and emotional_arousal, which modulate the nostalgia prediction.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NEMAC P0 | nostalgia_correl [7] | Acoustic nostalgia correlate (40%) |
| NEMAC P1 | memory_reward_lnk [8] | Memory-reward coupling strength (30%) |
| MEAMN P2 | nostalgia_link | Cross-relay nostalgia signal (30%) |
| NEMAC E1 | f11_nostalgia [1] | E-layer nostalgia extraction (upstream) |
| H3 | (12, 20, 1, 0) warmth mean H20 L0 | Implicit timbral warmth |
| H3 | (14, 20, 1, 0) tonalness mean H20 L0 | Implicit tonal stability |
| H3 | (0, 20, 18, 0) roughness trend H20 L0 | Implicit consonance trajectory |

---

## Scientific Foundation

- **Sakakibara et al. 2025**: Acoustic features predict nostalgia with r=0.985; nostalgic > non-nostalgic music response d=0.711; EEG decoder accuracy 64.0% younger, 71.5% older (EEG + behavioral + ML, N=33, eta_p^2=0.541)
- **Barrett et al. 2010**: Music-evoked nostalgia modulated by arousal, valence, and personality traits; nostalgia-wellbeing link established (behavioral, N=226)
- **Janata 2009**: Dorsal MPFC (BA 8/9) parametrically tracks tonal space movement during autobiographically salient songs; self-referential processing hub for nostalgia (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Wildschut et al. 2006**: Nostalgia is predominantly positive, self-relevant, and social; music is the most common nostalgia trigger (behavioral, N=172)

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/nostalgia_affect.py`
