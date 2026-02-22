# object_segregation — Appraisal Belief (IACM)

**Category**: Appraisal (observe-only)
**Owner**: IACM (ASU-alpha2)

---

## Definition

"Multiple sound sources segregating." Observes the degree to which the auditory system is parsing the acoustic scene into separate concurrent objects. High object segregation means the listener perceives distinct sound streams rather than a fused auditory image. Indexed by the Object-Related Negativity (ORN) ERP component.

---

## Observation Formula

```
# Direct read from IACM M-layer:
object_segregation = IACM.object_perception_or[M2]  # index [5]

# Calibrated against Basinski 2025 odds ratios:
# OR_inharmonic = 16.44
# OR_changing = 62.80
```

No prediction — observe-only appraisal. The value is directly consumed as a scene complexity indicator for downstream functions.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| IACM M2 | object_perception_or [5] | Calibrated odds ratio for object perception |
| IACM E1 | object_segregation [1] | E-layer scene complexity |
| IACM M1 | approx_entropy [4] | Spectral unpredictability feeding OR |

---

## Kernel Usage

The object_segregation appraisal provides scene complexity context:

```python
# Downstream consumers:
# F4 Memory: scene segmentation context for episodic boundaries
# F1 Sensory: auditory scene complexity indicator
```

High object segregation indicates the auditory scene is complex, with multiple concurrent sound sources being actively parsed. This informs memory encoding (scene transitions become episode boundaries) and sensory processing (resource allocation across streams).

---

## Scientific Foundation

- **Basinski 2025**: OR=16.44 inharmonic ORN, OR=62.80 changing spectrum (EEG, N=35)
- **Alain 2007**: ORN as index of concurrent auditory object segregation
- **Foo 2016**: ECoG STG high-gamma reflects spectral object encoding
- **Koelsch 1999**: Auditory scene analysis in musical contexts

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/iacm_relay.py` (pending)
