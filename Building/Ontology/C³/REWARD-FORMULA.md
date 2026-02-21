# Reward Formula

## Core: Salience-Gated Inverted-U Reward

```
reward = Σ_beliefs [ salience × (
    1.5 × surprise
  + 0.8 × resolution
  + 0.5 × exploration
  − 0.6 × monotony
)] × familiarity_mod × emotional_mod × da_gain
```

## 4 Components

```
π_eff = tanh(π_raw / 12)    # precision compression, breaks monotony saturation

surprise   = |PE| × π_eff × (1 − familiarity)    # unexpected in unfamiliar context
resolution = (1 − |PE|) × π_eff × familiarity     # expected in familiar context
exploration = |PE| × (1 − π_eff)                   # high PE + low precision = epistemic
monotony   = π_eff²                                # too predictable = boring
```

**Precision compression (v2.3):**
- π_raw=10 → π_eff=0.68 (tanh), not 1.0 (linear)
- Monotony at π=10: 0.37 (was 0.90), −59% drop
- Operating range expands: [0.55, 0.68] vs [0.93, 1.0]

**Weight rebalancing (v2.5):**
- Old: w_s=1.0, w_r=1.2, w_e=0.3, w_m=0.8 → slope A=0.028 (flat)
- New: w_s=1.5, w_r=0.8, w_e=0.5, w_m=0.6 → slope A=0.398 (14× steeper)
- Climaxes now produce visibly higher reward than calm passages

## Familiarity Modulation (Inverted-U)

```
fam_mod = 4 × familiarity × (1 − familiarity)    # peak at 0.5
reward *= 0.5 + 0.5 × fam_mod
```
- Familiar=0 (unknown): mod=0.5 (halved)
- Familiar=0.5 (sweet spot): mod=1.0 (full)
- Familiar=1.0 (overlearned): mod=0.5 (halved)

## SRP Hedonic Pathway (v4.0)

```
srp_hedonic = 0.30×wanting + 0.30×liking + 0.25×pleasure + 0.15×tension
chills_mult = 1 + 0.5 × chills_proximity
resolution_amp = 0.8 + 0.4 × resolution_expect
reward_srp = salience × srp_hedonic × chills_mult × resolution_amp

srp_confidence = 0.5 + 0.5 × reward_forecast
w_srp = 0.25 × srp_confidence

reward = (1 − w_srp) × reward_pe + w_srp × reward_srp
```

## MEAMN Emotional Modulation (v4.0)

```
emo_mod = 0.85 + 0.15 × emo_response_pred    # range [0.85, 1.0]
reward *= emo_mod
```

## DA Modulation — DAED Mesolimbic Pathway (v3.0)

```
da_signal = 0.6 × wanting_index + 0.4 × liking_index
da_gain = 1 + 0.25 × da_signal                # range [1.0, 1.25]
reward *= da_gain
```
- wanting = anticipatory DA (caudate, pre-climax)
- liking = consummatory DA (NAcc, pleasure)

## Multi-Scale Reward (v2.1)

```
reward = Σ_h [ w_h × reward_h(PE_h, π_pred_h, salience, familiarity) ]
```
- Her horizon kendi PE ve precision'ına sahip
- Short horizons: hızlı adapt (yüksek π → surprise/resolution)
- Long horizons: yavaş adapt (düşük π → exploration)

## Horizon Activation Gating (v2.2)

```
activation(t, T_h) = σ(5 × (t / T_h − 1))
```
- t < T_h: horizon henüz dolmadı → weight ≈ 0
- t = T_h: half active
- t > 2×T_h: fully active

Ultra horizons (H24=36s, H28=414s) 30s excerpt'lerde
neredeyse aktif olmuyor — spurious negative reward önlenir.

## Application Order

```
1. Per-belief PE-based reward (surprise/resolution/exploration/monotony)
2. SRP hedonic blend (v4.0)
3. Familiarity modulation (inverted-U)
4. MEAMN emotional modulation (v4.0)
5. DAED DA gain (v3.0)
```
