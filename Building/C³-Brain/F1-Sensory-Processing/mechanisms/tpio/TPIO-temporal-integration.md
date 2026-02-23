# TPIO M-Layer — Temporal Integration (1D)

**Layer**: M (Memory/Temporal)
**Dimensions**: 1D (index 4 of TPIO 10D output)
**Input**: E-layer features
**Character**: Normalized overlap strength — temporal integration of perception-imagery convergence

---

## Overview

The M-layer produces a single temporally integrated output: the overlap index. This normalizes the three E-layer components (perception substrate, imagery substrate, and their overlap) into a single measure of perception-imagery convergence. No additional H³ tuples are consumed — the M-layer operates entirely on E-layer outputs.

---

## M0: Overlap Index (overlap_index)

**Range**: [0, 1]
**Question answered**: "What is the overall strength of perception-imagery convergence right now?"

### Formula

```python
overlap_index = (f01_perception_substrate + f02_imagery_substrate + f03_perc_imag_overlap) / 3
```

### Dependencies

| Source | Feature | Role |
|--------|---------|------|
| E0 | f01_perception_substrate | Perception pathway activation |
| E1 | f02_imagery_substrate | Imagery pathway activation |
| E2 | f03_perc_imag_overlap | Shared substrate strength |

### Logic

Simple average of the three components of the perception-imagery circuit:
1. **Perception** (how well pSTG encodes timbre from acoustic input)
2. **Imagery** (how well pSTG maintains timbre from memory)
3. **Overlap** (how strongly they share the same code)

When all three are high → strong perception-imagery integration. When perception is high but imagery is low → passive listening. When imagery is high but perception is low → internal rehearsal. The overlap index captures the degree to which both pathways co-activate.

This output feeds the P-layer (as context for pSTG/SMA activation) and downstream models (ARU for imagery-driven affective response).

---

## Layer Summary

| Idx | Name | Range | Key Inputs | Purpose |
|-----|------|-------|------------|---------|
| M0 | overlap_index | [0, 1] | E0+E1+E2 averaged | Temporal convergence metric |

**Total M-layer H³ tuples**: 0 (uses E-layer outputs only)
