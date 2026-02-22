# Belief: octave_equivalence

**Category**: Appraisal
**Owner**: PCCR (SPU-α3)
**Function**: F1 Sensory Processing
**τ**: — (Appraisal beliefs have no inertia)

---

## 1. What This Belief Says

> "Tones separated by octaves are perceived as belonging to the same chroma class."

When octave_equivalence = 0.85, the auditory system assesses: "The current sound has strong octave-invariant structure — harmonics fold cleanly to the same pitch class, the sound is harmonic, and chroma encoding is unambiguous across octaves."

When octave_equivalence = 0.20, the assessment is: "Octave equivalence is weak — the sound is inharmonic (bell-like, metallic), or the chroma distribution is too scattered for reliable octave folding."

This is about the **quality of octave-invariant encoding**, not about pitch class identity or consonance.

---

## 2. Observe Formula

```
octave_equivalence = P1:octave_equivalence_index
```

### Source

| Source | Layer | Mechanism |
|--------|-------|-----------|
| P1:octave_equivalence_index | P-layer | E2 coherence + BCH harmonicity + E1 clarity + PCE gate |

### P1 Internals (from mechanism/PCCR-cognitive-present.md)

```
P1 = (
    0.40 × E2:octave_coherence           # harmonics agree on chroma (primary)
  + 0.25 × BCH.E1:harmonicity            # harmonic sounds have stronger OE
  + 0.20 × E1:chroma_clarity             # clear chroma → reliable octave folding
  + 0.15 × (1 − H³[38, H6, M0, L2])     # low PCE at 200ms = concentrated chroma
)
```

This integrates:
- **Octave coherence** (40%): Direct spectral assessment of cross-octave alignment
- **Harmonicity** (25%): BCH's harmonicity index — harmonic sounds have natural octave structure
- **Chroma clarity** (20%): Clear chroma distribution supports octave equivalence
- **PCE gate** (15%): Low pitch-class entropy confirms chroma is concentrated

---

## 3. No Predict/Update Cycle

As an Appraisal belief:
- **No prediction**: No τ, no baseline, no trend integration
- **No PE**: No prediction error generated
- **No update**: Value is set directly each frame from P1 mechanism output
- **No reward contribution**: Does not feed the reward formula via PE

The value is simply stored in BeliefStore for consumption by downstream Functions and models.

---

## 4. Scientific Grounding

### Octave Equivalence in Auditory Neuroscience

Octave equivalence is one of the most robust phenomena in pitch perception:

| Evidence | Finding | Relevance |
|----------|---------|-----------|
| Shepard 1964 | Circular pitch representation (pitch helix) | Foundational — pitch = height × chroma |
| Deutsch 1973 | Octave generalization in memory | Behavioral confirmation |
| Warren et al. 2003 | Octave-invariant pitch in auditory cortex (fMRI) | Neural substrate |
| Patterson 2002 | Pitch center in anterolateral HG | Cortical encoding |
| Briley et al. 2013 | IRN pitch sources lateral/anterior to pure-tone | Distinct processing streams |

### When Octave Equivalence Breaks Down

| Condition | OE Strength | Mechanism |
|-----------|-------------|-----------|
| Pure tones | Strong | Perfect harmonics |
| Complex harmonic tones | Strong | Harmonics fold to same chroma |
| Inharmonic tones (bells) | Weak | Partials don't fold to single chroma |
| Noise | Absent | No pitch, no chroma |
| Very high frequencies (>5kHz) | Weak | Phase-locking degrades |
| Atonal/chromatic passages | Moderate | Multiple chromas compete |

### The Pitch Helix

Shepard's (1964) pitch helix separates pitch into two orthogonal dimensions:
- **Pitch height**: Monotonically increasing with frequency (log scale)
- **Pitch chroma**: Circular, repeating every octave (12 classes)

PCCR.P1 measures the **strength of the chroma dimension** — how well the sound supports octave-invariant encoding. High P1 = the helix's circular dimension is well-defined; low P1 = only pitch height is available.

---

## 5. Distinction from Related Beliefs

| Belief | What It Says | Relationship to OE |
|--------|-------------|-------------------|
| **`octave_equivalence`** | "Octave folding is reliable" | THIS belief — encoding quality |
| `pitch_identity` (Core) | "This is chroma class X" | Downstream — uses OE to identify class |
| `harmonic_stability` (Core) | "Harmony is resolved" | Prerequisite — stability supports OE |
| `harmonic_template_match` (Appraisal) | "Partials fit a template" | Related — template match supports OE |
| `interval_quality` (Appraisal) | "This is a fifth" | Independent — interval rank, not octave folding |

octave_equivalence provides the **encoding quality assessment**: "Can we reliably fold this sound into chroma space?" When OE is high, pitch_identity's chroma assignment is trustworthy. When OE is low, pitch_identity should be less precise.

---

## 6. Downstream Consumers

| Consumer | Function | How It Uses This |
|----------|----------|-----------------|
| `pitch_identity` observe | F1 (PCCR) | OE quality feeds chroma identification confidence (indirect via P0) |
| HTP harmonic prediction | F2 | Strong OE → reliable chroma-based prediction |
| IMU memory encoding | F4 | Octave-invariant encoding → robust pitch memory |
| Precision engine | F1 | OE modulates observation precision for pitch_identity |

---

## 7. What This Belief Is NOT

- **Not** pitch identity ("This is C4") → that's `pitch_identity` (PCCR Core)
- **Not** harmonic quality ("This sounds consonant") → that's `harmonic_stability` (BCH)
- **Not** interval naming ("This is a perfect fifth") → that's `interval_quality` (BCH)
- **Not** pitch presence ("There is a pitch") → that's `pitch_prominence` (PSCL)

octave_equivalence is specifically: **"How reliably does this sound fold into octave-invariant chroma space?"**
