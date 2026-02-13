# H3 Laws -- Master Index

**Version**: 2.0.0
**Count**: 3 laws (L0-L2)
**Shared kernel**: A(dt) = exp(-3|dt|/H), ATTENTION_DECAY = 3.0
**Code reference**: `mi_beta.core.constants.LAW_NAMES`
**Implementation**: `mi_beta.ear.h3.attention.AttentionKernel`
**Updated**: 2026-02-13

---

## Overview

The three temporal laws define how H3 views time when computing morphological descriptors over R3 features. Each law selects a different window of frames relative to the current time `t` and applies the same exponential attention kernel within that window. Together they model three distinct cognitive processes:

- **L0 Memory**: Looks backward from the present -- how has this feature behaved recently?
- **L1 Prediction**: Looks forward from the present -- where is this feature heading?
- **L2 Integration**: Looks in both directions symmetrically -- what is the overall character around now?

All three laws share the identical kernel shape `A(dt) = exp(-3|dt|/H)`. They differ **only** in which frames fall inside the attention window. The kernel always peaks at the current frame (weight = 1.0) and decays to ~5% at the window boundary (exp(-3) = 0.0498).

---

## Summary Table

| Law | Name | Direction | Window | Causality | Latency | Primary Users |
|:---:|------|-----------|--------|-----------|---------|---------------|
| L0 | Memory | Past --> Present | `[max(0, t-n+1), t+1)` | Fully causal | 0 frames | IMU, STU, MPU |
| L1 | Prediction | Present --> Future | `[t, min(T, t+n))` | Non-causal | n frames | NDU, MPU, PCU |
| L2 | Integration | Past <--> Future | `[max(0, t-half), min(T, t+n-half))` | Semi-causal | n/2 frames | SPU, ASU, ARU |

---

## Usage Across Units

| Unit | L0 | L1 | L2 | Count |
|------|:--:|:--:|:--:|:-----:|
| SPU | Yes | -- | Yes | 2 |
| STU | Yes | Yes | Yes | 3 |
| IMU | Yes | -- | Yes | 2 |
| ASU | -- | -- | Yes | 1 |
| NDU | Yes | Yes | Yes | 3 |
| MPU | Yes | Yes | -- | 2 |
| PCU | Yes | Yes | Yes | 3 |
| ARU | Yes | Yes | Yes | 3 |
| RPU | Yes | Yes | Yes | 3 |
| **Total** | **8/9** | **6/9** | **8/9** | |

L0 and L2 are the most widely used (8 of 9 units each). L1 is used by 6 units -- those with anticipatory or predictive processing needs.

---

## File Listing

| File | Law | Description |
|------|-----|-------------|
| [L0-Memory.md](L0-Memory.md) | L0 | Causal memory law: past-to-present exponential decay, echoic memory basis, real-time advantage |
| [L1-Prediction.md](L1-Prediction.md) | L1 | Anticipatory prediction law: present-to-future projection, predictive coding basis, latency implications |
| [L2-Integration.md](L2-Integration.md) | L2 | Bidirectional integration law: symmetric context window, perceptual present basis, L0+L1 relationship |

---

## Cross-References

| Document | Location |
|----------|----------|
| Law catalog (registry) | [../Registry/LawCatalog.md](../Registry/LawCatalog.md) |
| Attention kernel contract | [../Contracts/AttentionKernel.md](../Contracts/AttentionKernel.md) |
| H3 architecture | [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md) |
| H3 master index | [../00-INDEX.md](../00-INDEX.md) |
| Morph catalog | [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md) |
| Code: attention kernel | `mi_beta/ear/h3/attention.py` |
| Code: law constants | `mi_beta/core/constants.py` (`LAW_NAMES`, `ATTENTION_DECAY`) |
