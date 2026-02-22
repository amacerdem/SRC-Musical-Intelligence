# nostalgia_intensity — Core Belief (MEAMN)

**Category**: Core (full Bayesian PE)
**τ**: 0.8
**Owner**: MEAMN (IMU-α1)
**Multi-Scale**: 6 horizons, T_char = 5s

---

## Definition

"This feels like home." Warmth-familiarity response to consonance-timbre interaction. Tracks the intensity of nostalgia evoked by music — the characteristic "warm glow" experience when familiar timbral qualities and harmonic structures activate deeply encoded personal associations. τ=0.8 reflects that nostalgia builds slowly and lingers; it does not spike and vanish.

---

## Multi-Scale Horizons

```
H13(600ms)  H16(1s)  H18(2s)  H20(5s)
H21(8s)     H24(36s)
```

T_char = 5s reflects the characteristic timescale of nostalgia emergence. H13–H16 capture the initial warmth flash at consonance-timbre recognition; H18–H20 track the full nostalgia buildup; H21 captures sustained nostalgic engagement; H24 tracks section-level persistence of the nostalgic state across musical phrases.

---

## Observation Formula

```
# Provisional (not yet implemented):
value = 0.40 × nostalgia_link + 0.30 × f02_nostalgia + 0.30 × memory_state

# nostalgia_link = familiarity × x_l5l7.mean (consonance-timbre warmth)
# f02_nostalgia  = sigma(0.70 × x_l5l7.mean × familiarity)
# memory_state   = retrieval_dynamics aggregation

# Precision: nostalgia_link × familiarity / (H³_std + ε)
```

The nostalgia_link (P2) provides the primary signal: the consonance-timbre interaction weighted by familiarity. The E-layer nostalgia response (E1) provides the raw acoustic trigger signal. memory_state (P0) modulates: nostalgia requires active memory retrieval to emerge.

Relay components: MEAMN.nostalgia_link[P2] + MEAMN.memory_state[P0] + MEAMN.f02_nostalgia[E1].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.8, nostalgia predictions are dominated by the previous frame. Context from beliefs_{t-1} includes autobiographical_retrieval (nostalgia requires active memory) and emotional_coloring (nostalgia is affectively charged).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN P2 | nostalgia_link [7] | Primary warmth-familiarity binding (40%) |
| MEAMN E1 | f02_nostalgia [1] | Acoustic nostalgia trigger (30%) |
| MEAMN P0 | memory_state [5] | Retrieval activation gating (30%) |
| R³ [12] | warmth | Timbral warmth input |
| R³ [41:49] | x_l5l7 | Consonance-timbre interaction |
| H³ | (12, 20, 1, 0) warmth mean H20 L0 | Sustained warmth = nostalgia |

---

## Scientific Foundation

- **Sakakibara et al. 2025**: Acoustic similarity alone triggers nostalgia; timbral warmth is sufficient without lyrics or explicit recognition (EEG, N=33, eta_p^2=0.636, Cohen's r=0.878 older adults)
- **Barrett et al. 2010**: Music-evoked nostalgia modulated by arousal, valence, and personality (behavioral)
- **Janata 2009**: mPFC tracks autobiographically salient tonal space movement (fMRI 3T, N=13)

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/nostalgia_intensity.py`
