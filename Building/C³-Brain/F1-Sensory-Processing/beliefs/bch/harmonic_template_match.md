# Belief: harmonic_template_match

**Category**: Appraisal
**Owner**: BCH (SPU-α1)
**Function**: F1 Sensory Processing
**τ**: — (Appraisal beliefs have no inertia)

---

## 1. What This Belief Says

> "The partials of this sound fit a harmonic series template."

When harmonic_template_match = 0.90, the listener's auditory system assesses: "The overtones align closely with integer multiples of a fundamental — this is a harmonic sound."

When harmonic_template_match = 0.20, the assessment is: "The overtones are scattered — this sound is inharmonic (bell-like, noise-like, or dissonant)."

This is about **structural alignment** of partials, not about experienced pleasantness or hierarchical position.

---

## 2. Observe Formula

```python
harmonic_template_match = P1_template_match
```

### Source

| Source | Layer | Mechanism |
|--------|-------|-----------|
| P1:template_match | P-layer | Multi-scale helmholtz/stumpf + deviation + tonal context |

### P1 Internals (from mechanism/BCH-cognitive-present.md)

```python
P1_template_match = (
    0.15 * H3[2, H0, M0, L2]    # helmholtz now
  + 0.15 * H3[2, H3, M1, L2]   # helmholtz mean 23ms
  + 0.15 * H3[3, H0, M0, L2]   # stumpf now
  + 0.10 * H3[3, H6, M1, L0]   # stumpf mean 200ms
  + 0.15 * (1 - H3[6, H0, M0, L2])   # low harmonic_deviation
  + 0.10 * (1 - R3[6])               # low harmonic_deviation (direct)
  + 0.10 * H3[51, H3, M0, L2]  # key clarity at 23ms
  + 0.10 * R3[60]               # tonal_stability
)
```

This integrates:
- **Helmholtz consonance** (30%): Integer ratio detection at two timescales
- **Stumpf fusion** (25%): Tonal fusion at two timescales
- **Harmonic deviation** (25%): Low deviation = partials close to ideal positions
- **Tonal context** (20%): Key clarity and tonal stability ground the template in musical key

---

## 3. No Predict/Update Cycle

As an Appraisal belief:
- No prediction, no PE, no τ, no Bayesian update
- Value set directly from P1:template_match each frame
- Stored in BeliefStore for downstream consumption

---

## 4. Scientific Grounding

### Harmonic Template Matching

The auditory system compares incoming spectra against an internalized harmonic series template. This is a brainstem/early cortical process, not a learned preference.

| Evidence | Finding | Relevance |
|----------|---------|-----------|
| Terhardt 1974 | Virtual pitch computation from peripheral harmonics | Foundation for template concept |
| McDermott et al. 2010 | Harmonicity preference = consonance preference | Behavioral confirmation |
| Bidelman & Heinz 2011 | AN population predicts hierarchy from template matching | Neural mechanism |
| Bidelman 2013 | Harmonicity > roughness as consonance predictor | Template > roughness |

### What "Template Match" Captures

The harmonic series template is: f₀, 2f₀, 3f₀, 4f₀, ...

Template match is high when:
- Spectral peaks fall near integer multiples of a common fundamental
- Energy distribution across harmonics is regular (low harmonic_deviation)
- The sound fits within a tonal key context (key_clarity, tonal_stability)

Template match is low when:
- Partials are inharmonic (bells, gongs, metallic percussion)
- Spectral noise dominates (no clear harmonic structure)
- Multiple conflicting fundamentals create spectral complexity

---

## 5. Distinction from Related Beliefs

| Belief | Focus | Input Dominance |
|--------|-------|----------------|
| **`harmonic_template_match`** | STRUCTURE: "Do partials fit harmonics?" | helmholtz, stumpf, deviation |
| `harmonic_stability` | EXPERIENCE: "Is this harmonically stable?" | roughness, pleasantness, template |
| `interval_quality` | CATEGORY: "Which consonance level?" | helmholtz × stumpf product |

harmonic_template_match is the most **structural** of the three — it asks about the sound's physical organization, not about how it feels or where it ranks.

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses This |
|----------|----------|-----------------|
| `harmonic_stability` observe | F1 (BCH) | 30% weight via P1:template_match |
| PCCR chroma encoding | F1 (SPU-α3) | Template quality informs chroma confidence |
| HTP abstract prediction | F2 | Template structure supports harmonic expectation |
