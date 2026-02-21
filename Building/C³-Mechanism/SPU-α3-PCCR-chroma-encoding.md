# Chroma Encoding

**Source**: SPU-α3-PCCR (Pitch Chroma Cortical Representation)
**Unit**: SPU (Spectral Processing Unit)
**Tier**: α (Core)
**Score**: 9/10 — Fully implementable

---

## Scientific Basis

- Octave equivalence literature (Shepard 1964, Deutsch 1973)
- Pitch class representation in auditory cortex

## Mechanism

Pitch is represented as a circular 12-class system (chroma), collapsing octave information.
This enables octave-invariant pitch comparison.

### Formula

```
Chroma(F0) = F0 mod 12

Similarity(F1, F2) = cos(2π · |Chroma(F1) - Chroma(F2)| / 12)
```

### Implementation

```python
chroma = f0_semitones % 12  # 12-class pitch representation
similarity = torch.cos(2 * pi * torch.abs(chroma1 - chroma2) / 12.0)
```

## Inputs

| Input | Source | Description |
|-------|--------|-------------|
| F0 | R³ v2 F:Pitch [49:65] chroma_vector | Fundamental frequency in semitones |

## Outputs

| Name | Range | Description |
|------|-------|-------------|
| chroma | [0, 12) | Pitch class (C=0, C#=1, ..., B=11) |
| similarity | [-1, 1] | Cosine similarity between two chromas |

## Why 9/10

- Modulo arithmetic — simplest possible implementation
- Cosine distance on circular space — mathematically exact
- Foundational for any pitch-based cognition (harmony, melody, key)
- Requires F0 tracking (R³ v2 provides this)
