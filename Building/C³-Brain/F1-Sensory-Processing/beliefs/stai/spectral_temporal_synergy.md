# Belief: spectral_temporal_synergy

**Category**: Appraisal
**Owner**: STAI (SPU-β1)
**Function**: F1 Sensory Processing

---

## 1. What This Belief Says

> "Spectral and temporal features reinforce each other."

When spectral_temporal_synergy = 0.85: "The spectral content (harmonic structure, timbre, consonance) and temporal content (rhythm, forward motion, predictability) are mutually reinforcing — they co-vary in a way that strengthens the overall aesthetic percept."

When spectral_temporal_synergy = 0.15: "Spectral and temporal features are decoupled or contradictory — e.g., consonant harmonies with temporally disrupted rhythm, or rich temporal flow with dissonant spectral content."

This is an **observe-only** judgment. No predict/update cycle, no PE, no τ. It provides evaluative context for `aesthetic_quality` (Core).

---

## 2. Observe Formula

```python
observed = (
    0.50 * STAI_E_spectral_temporal_interaction   # spectral x temporal co-variance
  + 0.30 * STAI_M_coherence_index                 # mathematical coherence metric
  + 0.20 * STAI_P_binding_strength                # real-time binding assessment
)
```

### Source Breakdown

| Source | Weight | What It Captures |
|--------|--------|------------------|
| E:spectral_temporal_interaction | 50% | Direct co-variance: do spectral and temporal features move together? |
| M:coherence_index | 30% | Temporal integration of spectral-temporal co-variance |
| P:binding_strength | 20% | Present-state: how strongly are features bound? |

---

## 3. Downstream Consumers

| Consumer | How It Uses This |
|----------|------------------|
| `aesthetic_quality` (Core, F1) | Synergy modulates aesthetic prediction context |
| Salience (F3) | High synergy → stronger salience signal |
| Reward formula (F6) | Synergy contributes to resolution component |

---

## 4. What This Belief Is NOT

- **Not** aesthetic quality → that's `aesthetic_quality` (STAI Core)
- **Not** harmonic template match → that's `harmonic_template_match` (BCH)
- **Not** spectral complexity → that's `spectral_complexity` (SDED)

---

## 5. Evidence Foundation

| Study | Key Finding | Relevance |
|-------|-------------|-----------|
| Kim et al. 2019 | Spectral × Temporal factorial interaction (d=0.709-0.735) | Core: the interaction effect IS the synergy |
| Alluri et al. 2012 | Independent parallel streams converge in association cortex | Integration produces synergy |
| Singer et al. 2023 | Temporal predictability positively predicts valence | Temporal integrity contributes |
