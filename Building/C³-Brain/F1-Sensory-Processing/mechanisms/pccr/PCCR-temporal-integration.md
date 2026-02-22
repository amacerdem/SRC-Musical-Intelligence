# PCCR M-Layer — Temporal Integration (1D)

**Layer**: M (Memory/Temporal)
**Dimensions**: 1D (index 4 of PCCR 11D output)
**Input**: H³ tuples (L2 present + L0 memory)
**Character**: Temporal chroma stability — how persistent is the dominant pitch class?

---

## Overview

Unlike BCH (4D M-layer) and PSCL (4D M-layer), PCCR has only **1D** for temporal integration. This reflects PCCR's focused role: it doesn't need to track multiple temporal streams. It needs one answer: "Is the chroma stable over time?"

Chroma stability is high when:
- The same pitch class persists across multiple analysis windows
- Pitch salience remains present over extended time
- Tonal quality is sustained (not transitioning to noise)
- Periodicity in tonal quality suggests repeating tonal patterns

---

## Output

### M0: Chroma Stability — [0, 1]

```
M0 = (
    0.30 × (1 − H³[38, H12, M1, L0])    # low PCE mean 525ms → stable chroma
  + 0.25 × H³[14, H6, M0, L2]            # tonalness value at 200ms
  + 0.25 × H³[39, H12, M1, L0]           # pitch_salience mean 525ms → persistent pitch
  + 0.20 × H³[14, H12, M14, L0]          # tonalness periodicity 525ms → cycling tonal
)
```

### Component Breakdown

| Signal | Weight | H³ Tuple | What It Captures |
|--------|--------|----------|------------------|
| (1 − PCE mean 525ms) | 30% | (38, 12, 1, 0) | Chroma distribution has been concentrated over the past 525ms — same pitch class dominates |
| Tonalness at 200ms | 25% | (14, 6, 0, 2) | Sound is currently tonal (not noise) — prerequisite for chroma |
| Pitch salience mean 525ms | 25% | (39, 12, 1, 0) | Pitch has been consistently present over half a second |
| Tonalness periodicity 525ms | 20% | (14, 12, 14, 0) | Tonal quality cycles predictably (suggests repeating tonal events) |

### Interpretation

- **M0 ≈ 0.85**: The same pitch class has been dominant, tonalness is high, pitch is persistent — strong chroma identity over time (e.g., sustained note, pedal tone).
- **M0 ≈ 0.50**: Moderate chroma stability — pitch class may be shifting (melody) but still identifiable.
- **M0 ≈ 0.15**: Low stability — rapid chroma changes (chromatic passage), noise, or silence.

---

## H³ Tuples Consumed

| # | R³ Idx | Feature | H | Morph | Law | Purpose |
|---|--------|---------|---|-------|-----|---------|
| 1 | 38 | pitch_class_entropy | 12 | M1 (mean) | L0 | PCE memory 525ms |
| 2 | 14 | tonalness | 6 | M0 (value) | L2 | Tonalness now at 200ms |
| 3 | 39 | pitch_salience | 12 | M1 (mean) | L0 | Pitch salience memory 525ms |
| 4 | 14 | tonalness | 12 | M14 (periodicity) | L0 | Tonalness cycling pattern |

**Shared tuples**: (39, 12, 1, 0) shared with BCH; (14, 6, 0, 2) unique to PCCR.

---

## Downstream Routing

| Output | → Layer | How It's Used |
|--------|---------|---------------|
| M0 | → P0 | 15% weight in chroma_identity_signal |
| M0 | → F0 | 20% weight in chroma_continuation_signal |
