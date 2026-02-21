# Belief: interval_quality

**Category**: Appraisal
**Owner**: BCH (SPU-α1)
**Function**: F1 Sensory Processing
**τ**: — (Appraisal beliefs have no inertia)

---

## 1. What This Belief Says

> "The current interval sits at position X in the P1/P5/P4/M3/m6/TT consonance hierarchy."

This is a **categorical sensory assessment** — not "how consonant" (that's `harmonic_stability`) but "WHICH consonance level." It places the perceived interval on a discrete ordinal scale derived from the universal neural consonance hierarchy.

### Example Values

| interval_quality | Interpretation |
|-----------------|----------------|
| 0.80 | Near-unison or perfect fifth — top of hierarchy |
| 0.60 | Fourth or major third — middle |
| 0.40 | Minor sixth range — lower-middle |
| 0.15 | Near tritone — bottom of hierarchy |

---

## 2. Observe Formula

```python
interval_quality = E2_hierarchy
#                = 0.80 * R3[2] * R3[3]
#                         helmholtz × stumpf
```

### Source

| Source | Layer | Mechanism |
|--------|-------|-----------|
| E2:hierarchy (f03) | E-layer | Product of helmholtz_kang × stumpf_fusion |

This is a direct mechanism output — no weighted combination, no temporal integration. The value is computed frame-by-frame from R³ features.

### R³ Features (Post-Freeze)

| R³ Index | Feature | Role |
|----------|---------|------|
| **[2]** | helmholtz_kang | Integer ratio detection (mathematical consonance) |
| **[3]** | stumpf_fusion | Tonal fusion perception (auditory consonance) |

---

## 3. No Predict/Update Cycle

As an Appraisal belief:
- **No prediction**: No τ, no baseline, no trend integration
- **No PE**: No prediction error generated
- **No update**: Value is set directly each frame from mechanism output
- **No reward contribution**: Does not feed the reward formula via PE

The value is simply stored in BeliefStore for consumption by downstream Functions and models.

---

## 4. Scientific Grounding

### The Universal Neural Consonance Hierarchy

```
P1 (1:1) > P5 (3:2) > P4 (4:3) > M3 (5:4) > m6 (8:5) > TT (45:32)
```

| Property | Status |
|----------|--------|
| Neural basis | FFR amplitude ordering matches hierarchy (Bidelman 2009) |
| Cross-cultural | Neural hierarchy **universal** — confirmed in infants, animals |
| Behavioral | Ratings **vary** by culture — BCH models neural level, not preference |
| Peripheral sufficiency | AN population model predicts full hierarchy (Bidelman & Heinz 2011) |

### Qualification

The hierarchy is most clear with synthetic tones. With natural sounds (Cousineau 2015), the ranking becomes less distinct due to timbre complexity.

---

## 5. Distinction from Related Beliefs

| Belief | What It Says | Difference |
|--------|-------------|------------|
| `harmonic_stability` (Core) | "How resolved/stable is the harmony?" | Continuous quality assessment |
| **`interval_quality`** (Appraisal) | "Which consonance level?" | Discrete hierarchical position |
| `harmonic_template_match` (Appraisal) | "Do partials fit a template?" | Structural alignment, not ranking |

interval_quality provides the **categorical label** ("this is a fifth-like interval"), while harmonic_stability provides the **experienced quality** ("this sounds stable"). You can have high harmonic_stability with low interval_quality (e.g., a well-tuned tritone in context) or vice versa (a poorly-voiced fifth).

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses This |
|----------|----------|-----------------|
| `harmonic_stability` observe | F1 (BCH) | 20% weight in observe formula (E2:hierarchy) |
| HTP interval prediction | F2 | Hierarchical context for harmonic expectation |
| Salience modulation | F3 | Consonance level influences attention allocation |
