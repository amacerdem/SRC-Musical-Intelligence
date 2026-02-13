# L³ Validation — Index

Validation strategy for L³ semantic interpretation.

## Documents

| Document | Purpose |
|----------|---------|
| [AcceptanceCriteria.md](AcceptanceCriteria.md) | Automated per-group output checks |
| [BenchmarkPlan.md](BenchmarkPlan.md) | Empirical validation against human data |

## Approach

L³ validation uses two complementary strategies:

1. **Acceptance Criteria** (automated): Shape, range, and invariant checks that can run as unit tests after every code change
2. **Benchmark Plan** (empirical): Correlation with physiological measurements, emotion ratings, and psychometric instruments

## Priority

| Priority | Validation Target | Groups |
|----------|-------------------|--------|
| P0 | Shape and range correctness | All |
| P1 | Physiological correlation | δ |
| P2 | Emotion rating correlation | γ, ζ |
| P3 | Vocabulary agreement | η |
| P4 | Chills prediction | γ (chill dims) |
| P5 | Learning dynamics | ε |

---

**Parent**: [../00-INDEX.md](../00-INDEX.md)
