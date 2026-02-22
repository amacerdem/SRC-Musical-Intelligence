# nostalgia_peak_pred — Anticipation Belief (NEMAC)

**Category**: Anticipation (prediction)
**Owner**: NEMAC (F5)

---

## Definition

"Nostalgic peak moment approaching." Predicts an upcoming peak nostalgic experience based on building familiarity and emotional intensity signals. Uses hippocampal activation trajectory plus buildup tracking from H3 to detect approaching "nostalgia breakthroughs" — moments of suddenly vivid autobiographical recall accompanied by strong bittersweet emotion. The prediction window is 2-5 seconds ahead, matching the characteristic buildup time for peak nostalgic experiences.

---

## Observation Formula

```
# From NEMAC F-layer:
nostalgia_peak_pred = NEMAC.vividness_pred[F1]  # index [10]

# Formula: sigma(hippocampus + 0.3 * buildup_tracking_mean)
# Based on:
#   NEMAC E1: f11_nostalgia — current nostalgia strength (rising = approaching peak)
#   NEMAC P0: nostalgia_correl — acoustic nostalgia match (strengthening = cue alignment)
#   H3 (3, 20, 1, 2): stumpf_fusion mean H20 L2 — binding trajectory for vividness
#   buildup_tracking: H3 trend features detecting rising nostalgia cues
```

Anticipation beliefs are forward-looking predictions that generate PE when the predicted nostalgia peak mismatches the observed nostalgic evolution. High nostalgia_peak_pred signals that the listener is about to enter a peak nostalgic state — a moment of intense autobiographical re-experiencing.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| NEMAC F1 | vividness_pred [10] | Memory vividness prediction (2-5s ahead) |
| NEMAC E1 | f11_nostalgia [1] | Current nostalgia state (upstream input) |
| NEMAC P0 | nostalgia_correl [7] | Acoustic nostalgia correlate (upstream input) |
| H3 | (3, 20, 1, 2) stumpf_fusion mean H20 L2 | Binding trajectory for vividness prediction |
| H3 | (22, 20, 19, 0) entropy stability H20 L0 | Pattern stability for familiarity trajectory |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F6 Reward | Anticipatory pleasure — predicted nostalgia peak feeds caudate anticipation signal (Salimpoor 2011: dopamine ramp 15-30s before peak) |
| F4 Memory | Retrieval preparation — predicted peak triggers deeper autobiographical search; hippocampal pre-activation for episodic recall |
| Precision engine | pi_pred estimation — high nostalgia_peak_pred increases prediction confidence for nostalgia_affect |
| F5 Emotion | Emotional preparation — if nostalgia peak is predicted, affective systems prepare for stronger bittersweet re-experiencing |

---

## Scientific Foundation

- **Sakakibara et al. 2025**: Nostalgia builds over seconds with predictable trajectory; acoustic similarity cues precede peak nostalgic experience (EEG + behavioral, N=33, eta_p^2=0.541)
- **Janata 2009**: Imagery vividness strong vs weak autobiographical memory — hippocampal activation trajectory predicts memory quality (fMRI 3T, N=13, t(9)=5.784, p<0.0003)
- **Salimpoor et al. 2011**: Caudate dopamine ramp 15-30s before peak emotional experience; anticipation is neurally distinct from consummation (PET, N=8)
- **Barrett et al. 2010**: Nostalgia intensity builds through familiarity-arousal-valence interaction over time (behavioral, N=226)

## Implementation

File: `Musical_Intelligence/brain/kernel/relays/nemac_relay.py`
