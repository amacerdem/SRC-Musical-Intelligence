# sensory_load — Appraisal Belief (CSG)

**Category**: Appraisal (observe-only)
**Owner**: CSG (ASU-a3)

---

## Definition

"Processing resource demand high/low." Observes the sensory processing load imposed by the current stimulus. Ambiguous stimuli (neither clearly consonant nor dissonant) demand more processing resources, following an inverted-U function of consonance. Clear consonance or clear dissonance is easy to categorize; ambiguity is costly.

---

## Observation Formula

```
# Direct read from CSG P-layer:
sensory_load = CSG.sensory_load[P2]   # index [8], [0,1]

# Computation:
# ambiguity = 1 - |consonance - 0.5| * 2
# sensory_load = sigma(0.5 * ambiguity)
#
# Inverted-U: maximum load at consonance=0.5 (ambiguous),
# minimum load at consonance=0 (clear dissonance) or 1 (clear consonance)
```

No prediction — observe-only appraisal. The value reflects how much Heschl's gyrus processing resources are demanded by the current stimulus.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| CSG P2 | sensory_load [8] | Processing resource demand |
| CSG E0 | consonance level | Drives ambiguity computation |

---

## Kernel Usage

The sensory_load appraisal provides a resource-demand signal:

```python
# Phase 1 in scheduler:
sensory_load = observe(csg_relay['sensory_load'])
```

High sensory load means the auditory system is working harder to categorize the stimulus. This can modulate attention allocation — ambiguous stimuli recruit more processing but do not necessarily capture attention the way salient events do.

---

## Scientific Foundation

- **Bravo 2017**: Dissonance-consonance categorization difficulty modulates processing load
- **Sarasso 2019**: Processing demand varies with interval ambiguity (EEG)
- **Koelsch 2011**: Heschl's gyrus activation scales with auditory complexity

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/csg_relay.py`
