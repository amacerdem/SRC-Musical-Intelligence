# self_referential_nostalgia — Appraisal Belief (NEMAC)

**Category**: Appraisal (observe-only)
**Owner**: NEMAC (F5)

---

## Definition

"Music holds personal meaning for me." Self-referential processing assessment — how much the music connects to personal identity and history. This appraisal captures the mPFC-mediated sense of "this is MY music" that distinguishes personal nostalgia from generic familiarity. The self-referential dimension is the primary driver of nostalgia intensity (Sakakibara 2025: 0.6 weighting in nostalgia extraction), and its activation parametrically tracks autobiographical salience (Janata 2009).

---

## Observation Formula

```
# Direct read from NEMAC E-layer:
self_referential_nostalgia = NEMAC.f11_nostalgia[E1]  # index [1]

# f11_nostalgia = clamp(0.6 * mpfc + 0.4 * hippocampus, 0, 1)
# The 0.6 mPFC weighting captures self-referential primacy
# The 0.4 hippocampus weighting captures memory retrieval contribution

# Self-referential component isolated:
# mpfc_component = NEMAC internal mPFC self-referential signal
# Driven by familiarity * tonal_quality * warmth interaction
```

No prediction — observe-only appraisal. The value is directly read from the NEMAC extraction layer's nostalgia computation, which weights self-referential processing (mPFC) at 0.6 and memory retrieval (hippocampus) at 0.4. It represents the degree to which the current music is personally meaningful.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NEMAC E1 | f11_nostalgia [1] | Composite nostalgia with self-referential primacy |
| NEMAC P0 | nostalgia_correl [7] | Acoustic nostalgia correlate (upstream validation) |
| NEMAC P1 | memory_reward_lnk [8] | Memory-reward link (self-relevant memories = stronger reward) |
| R3 [14] | tonalness | Tonal quality for familiarity estimation |
| R3 [4] | sensory_pleasantness | Hedonic quality for warmth computation |

---

## Kernel Usage

The self_referential_nostalgia appraisal serves as a personal-meaning diagnostic:

```python
# Available in BeliefStore for downstream consumers:
# - F4 Memory: gates autobiographical retrieval depth — high self-reference
#   triggers deeper episodic memory search
# - F6 Reward: self-referential nostalgia modulates hedonic reward magnitude
# - Precision engine: high self-reference → higher pi_obs for nostalgia beliefs
# - F5 Emotion: self-referential intensity modulates nostalgia_affect core belief
```

Unlike the nostalgia_affect Core belief (which integrates acoustic and memory signals into the full nostalgic experience), self_referential_nostalgia isolates the identity-connection dimension — it reports how personally meaningful the music is without the acoustic warmth or memory vividness components.

---

## Scientific Foundation

- **Janata 2009**: Dorsal MPFC (BA 8/9) parametrically tracks autobiographical salience; self-referential processing is the neural hub for music-evoked nostalgia (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Sakakibara et al. 2025**: Self-referential processing weighted 0.6 in nostalgia model; acoustic similarity alone triggers nostalgia but self-reference amplifies it (EEG + behavioral, N=33, eta_p^2=0.636)
- **Scarratt et al. 2025**: Familiar music activates auditory, motor, emotion, and memory areas; 4 distinct response clusters including self-referential mPFC cluster (fMRI, N=57)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/nemac_relay.py`
