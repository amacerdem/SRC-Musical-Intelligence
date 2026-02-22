# emotional_arousal — Core Belief (AAC)

**Category**: Core (full Bayesian PE)
**τ**: 0.5
**Owner**: AAC (F5)
**Multi-Scale**: single-scale in v1.0, T_char = 1s

---

## Definition

"I am emotionally activated." Tracks the overall level of physiological and psychological arousal evoked by music. This is the FELT arousal — the subjective experience of activation/deactivation — not perceived arousal in the music. Autonomic nervous system activation via the amygdala-hypothalamus pathway drives the somatic markers (SCR, HR, RespR) that underlie this belief. Moderate τ (0.5) reflects that arousal fluctuates on a ~1s timescale: fast enough to track dynamic passages but slow enough that arousal does not vanish between beats.

---

## Multi-Scale Horizons

```
Single-scale in v1.0: H16 (1s)
```

T_char = 1s reflects the characteristic timescale of felt emotional arousal. Arousal responds to individual musical events (crescendos, onset attacks) on a beat-level timescale. Future multi-scale expansion would add H9 (350ms) for onset-locked arousal spikes and H20 (5s) for sustained arousal during climactic passages.

---

## Observation Formula

```
# Implicit (60%): H3 energy + salience
energy_level = H3(7, 9, 4, 2)   # amplitude max H9 L2
velocity = H3(7, 9, 8, 2)        # amplitude velocity H9 L2
salience = salience_signal        # from salience module

implicit = 0.50 * energy_level + 0.30 * velocity + 0.20 * salience

# Explicit (40%): AAC E-layer + P-layer
explicit = 0.50 * f04_emotional_arousal + 0.30 * current_intensity + 0.20 * perceptual_arousal

# Combined: (0.60 * implicit + 0.40 * explicit) * energy_gate
# Energy gate: sigma(10 * (energy - 0.1))

# Precision: 1/(std(energy, velocity, salience) + 0.1) * gate
#            + AAC: 0.3 * f04_emotional_arousal + 0.2 * current_intensity
```

The implicit pathway captures the acoustic basis for arousal: peak energy level and energy velocity (crescendo/decrescendo) at the 350ms beat-level timescale, combined with the salience module's event significance signal. The explicit pathway reads the AAC extraction layer's emotional arousal computation and P-layer present-moment signals. The 60/40 split reflects that felt arousal is primarily driven by bottom-up acoustic energy, with the AAC mechanism providing context-sensitive modulation.

Relay components: AAC.f04_emotional_arousal[E0] + AAC.current_intensity[P0] + AAC.perceptual_arousal[P2].

---

## Prediction Formula

```
predict = Linear(τ * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.5, the prediction balances between persistence and responsiveness — arousal tracks moment-to-moment changes but maintains inertia through brief pauses. M18 (trend) captures crescendo/decrescendo trajectories. M14 (periodicity) captures rhythmic arousal modulation. Context from beliefs_{t-1} includes driving_signal and chills_intensity, which amplify arousal predictions.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| AAC E0 | f04_emotional_arousal [0] | Primary arousal extraction (50%) |
| AAC P0 | current_intensity [9] | Present-moment emotional intensity (30%) |
| AAC P2 | perceptual_arousal [11] | Event-density arousal (20%) |
| H3 | (7, 9, 4, 2) amplitude max H9 L2 | Implicit energy level |
| H3 | (7, 9, 8, 2) amplitude velocity H9 L2 | Implicit energy velocity |
| R3 [7] | amplitude | Baseline energy signal |

---

## Scientific Foundation

- **Koelsch 2014**: Brain correlates of music-evoked emotions — amygdala, hippocampus, ventral striatum, insula, and orbitofrontal cortex activated during emotional music listening (fMRI meta-review)
- **Salimpoor et al. 2011**: Chills correlate with dopamine release in ventral striatum; autonomic arousal markers (SCR, HR, RespR) track emotional peaks (PET, N=8, r=0.84)
- **Egermann 2013**: Unexpected events drive strongest ANS response; SCR d=2.5, HR d=6.0 (live concert + physiology, N=25-50)
- **Gomez & Danuser 2007**: Factor structure confirms arousal dominance in ANS response to music: RespR r=0.42 arousal, r=0.08 valence (multi-ANS, N=48)

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/emotional_arousal.py`
