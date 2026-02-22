# PCCR P-Layer — Cognitive Present (3D)

**Layer**: P (Present/Cognitive)
**Dimensions**: 3D (indices 5–7 of PCCR 11D output)
**Input**: R³ direct + H³ tuples + E-layer + M-layer + upstream (BCH, PSCL)
**Scope**: hybrid (feeds both downstream models AND beliefs)

---

## Overview

The P-layer is where pitch-class encoding becomes a cognitive representation. It integrates raw chroma extraction (E-layer), temporal stability (M-layer), and upstream pitch/consonance information (BCH, PSCL) into three signals:

1. **P0**: Chroma identity — the primary belief-feeding output
2. **P1**: Octave equivalence — octave-invariant pitch class strength
3. **P2**: Chroma salience — perceptual saliency of the identified chroma

All three read from upstream models (BCH relay, PSCL encoder) via the Associator's `upstream_outputs` dict.

---

## Outputs

### P0: Chroma Identity Signal — [0, 1]

Primary output for the `pitch_identity` Core belief (55% weight in observe).

```
PSCL_P0 = upstream["PSCL"][:, :, 8]    # pitch_prominence_sig
PSCL_P2 = upstream["PSCL"][:, :, 10]   # periodicity_clarity

P0 = (
    0.25 × E0                           # chroma energy (strongest chroma bin)
  + 0.20 × E1                           # chroma clarity (one class dominates)
  + 0.15 × E3                           # pitch class confidence
  + 0.15 × M0                           # chroma stability over time
  + 0.15 × PSCL_P0                      # pitch prominence gates chroma ID
  + 0.10 × PSCL_P2                      # periodicity clarity for tuning
)
```

**Design rationale**: Six complementary signals ensuring robust chroma identification:
- **E0 + E1** (45%): Raw chroma quality — is there a dominant pitch class?
- **E3** (15%): Multi-indicator confidence check
- **M0** (15%): Temporal confirmation — has this chroma persisted?
- **PSCL** (25%): Upstream pitch quality — is there a pitch to identify?

**Key constraint**: PSCL.P0 (pitch_prominence) gates chroma identification. No pitch prominence → no chroma identity, regardless of chroma bin values. This implements the neuroscientific principle that pitch class encoding requires prior pitch detection.

### P1: Octave Equivalence Index — [0, 1]

Source for the `octave_equivalence` Appraisal belief (direct 1.0 weight).

```
BCH_E1 = upstream["BCH"][:, :, 1]      # E1:harmonicity

P1 = (
    0.40 × E2                           # octave_coherence (harmonics agree on chroma)
  + 0.25 × BCH_E1                       # harmonicity (harmonic sounds have stronger OE)
  + 0.20 × E1                           # chroma_clarity (clear chroma → clear OE)
  + 0.15 × (1 − H³[38, H6, M0, L2])    # low PCE at 200ms = concentrated chroma
)
```

**Scientific basis**: Octave equivalence (Shepard 1964) is strongest for harmonic sounds where partials naturally fold to the same chroma class. Inharmonic sounds (bells, metallic percussion) show weak or absent octave equivalence.

**Component interpretation**:
- **E2** (40%): Direct octave coherence from spectral analysis
- **BCH harmonicity** (25%): Harmonic sounds exhibit stronger octave equivalence
- **E1** (20%): Clear chroma → reliable octave folding
- **PCE gate** (15%): Low entropy confirms concentrated chroma

### P2: Chroma Salience — [0, 1]

How perceptually salient is the identified chroma class?

```
BCH_E2 = upstream["BCH"][:, :, 2]      # E2:hierarchy

P2 = (
    0.30 × P0                           # chroma identity quality
  + 0.25 × PSCL_P0                      # pitch prominence
  + 0.25 × E0                           # chroma energy
  + 0.20 × BCH_E2                       # consonance hierarchy context
)
```

**Interpretation**: Chroma is salient when:
1. Chroma identity is strong (P0 is high)
2. The underlying pitch is prominent (PSCL says "there's a clear pitch")
3. Chroma energy is concentrated (E0 is high)
4. The harmonic context supports it (BCH consonance hierarchy)

---

## Upstream Dependencies

| Model | Output Index | Dimension Name | Used In | Weight |
|-------|-------------|----------------|---------|--------|
| PSCL | 8 | P0:pitch_prominence_sig | P0, P2 | 0.15, 0.25 |
| PSCL | 10 | P2:periodicity_clarity | P0 | 0.10 |
| BCH | 1 | E1:harmonicity | P1 | 0.25 |
| BCH | 2 | E2:hierarchy | P2 | 0.20 |

---

## H³ Tuples Consumed (P-Layer Only)

| # | R³ Idx | Feature | H | Morph | Law | Used In |
|---|--------|---------|---|-------|-----|---------|
| 1 | 38 | pitch_class_entropy | 6 | M0 (value) | L2 | P1 |

---

## Belief Mapping

| Output | → Belief | Category | Weight |
|--------|----------|----------|--------|
| P0 | `pitch_identity` | Core | 55% observe |
| P1 | `octave_equivalence` | Appraisal | 100% observe |
| P2 | `pitch_identity` | Core | 25% observe |

---

## Downstream Routing (External)

| Output | → Model | Purpose |
|--------|---------|---------|
| P0 | → IMU (chroma→memory) | Chroma identity feeds melodic memory encoding |
| P0 | → STU (chroma→melody) | Chroma identity feeds temporal structure |
| P2 | → F3 (Attention) | Chroma salience contributes to attentional allocation |
