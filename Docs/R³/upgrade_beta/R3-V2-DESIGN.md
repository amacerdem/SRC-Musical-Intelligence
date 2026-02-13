# R³ v2 Mimari Tasarım Dokümanı

**Phase**: 3B — Architecture Design
**Tarih**: 2026-02-13
**Girdiler**: R3-CROSSREF.md (R1+R2+R3 sentezi), R3-DEMAND-MATRIX.md, R3-DSP-SURVEY-THEORY.md, R3-DSP-SURVEY-TOOLS.md
**Çıktı**: Bu doküman — R³ v2'nin kesin mimari tasarımı
**Boyut**: 49D → 128D (11 grup: A-K)

---

## Bölüm 1: Tasarım Kararları Özeti

### 1.1 Yedi Açık Mimari Karar

Crossref §7.1'deki 7 açık karar aşağıdaki şekilde çözülmüştür:

| # | Karar | Seçenek | Gerekçe |
|---|-------|---------|---------|
| 1 | Chroma hesaplama yöntemi | **A: mel→freq→PC fold (Gaussian soft-assignment)** | ~1ms/frame; Appendix B algoritması yeterli kalite (key detection ≥85%); CQT gereksiz overhead |
| 2 | Beat tracking yöntemi | **A: Onset autocorrelation** | GPU-native (torch.fft), harici bağımlılık yok; PLP aynı autocorrelation'dan türer |
| 3 | Entropy/surprise pencere boyutu | **τ = 2.0s (344 frame)** | 1s çok gürültülü, 4s çok yavaş; warm-up: `confidence = min(1.0, t/τ)` lineer rampa |
| 4 | Modulation spectrum penceresi | **344 frame (~2.0s), hop=86 frame (~0.5s), %75 overlap** | 0.5 Hz çözünürlük sağlar; frame-level interpolasyon ile 172 Hz çıktı |
| 5 | Hesaplama sırası (DAG) | **3-stage: S1→S2→S3** (aşağıda detay) | F Stage 1'de (mel-only); G,H,E Stage 2'de; I Stage 3'te |
| 6 | E grubu genişleme | **128D korunur; E genişleme Phase 6+ / R³ v2.1'e ertelenir** | Deneysel veriye dayalı karar gerekli; 128D bütçe aşılmaz |
| 7 | Backward compatibility | **3-katmanlı strateji**: indeks koruma → formül güncelleme → tam revizyon | Aşağıda Bölüm 5'te detay |

### 1.2 Karar Detayları

#### Karar 1: Chroma Hesaplama — mel→freq→PC fold

**Algoritma** (R3-DSP-SURVEY-TOOLS.md Appendix B'den):

```
Girdi: mel (B, 128, T) — log-mel spectrogram
       sr = 44100, n_mels = 128, fmin = 0, fmax = sr/2

1. Her mel bin'in merkez frekansını hesapla:
   f_center[m] = 700 * (10^(m * mel_scale_factor) - 1)

2. Frekansı MIDI pitch'e dönüştür:
   midi[m] = 69 + 12 * log2(f_center[m] / 440)

3. Pitch class (0-11) ata:
   pc[m] = round(midi[m]) % 12

4. Gaussian soft-assignment mapping matrisi M (128 × 12) oluştur:
   M[m, c] = exp(-0.5 * ((midi[m] % 12 - c + 6) % 12 - 6)^2 / σ^2)
   σ = 0.5 semitone (Gaussian genişliği)

5. Chroma hesapla:
   mel_linear = exp(mel)  # log-mel → lineer güç
   chroma = M^T @ mel_linear  → (B, 12, T)
   chroma = chroma / chroma.sum(dim=1, keepdim=True).clamp(min=1e-8)

Çıktı: chroma (B, T, 12) — L1-normalized pitch class profili
```

**PyTorch implementasyonu**:
- `M` pre-computed ve `register_buffer` olarak saklanır
- `torch.matmul(M.T, mel_linear)` — tek matris çarpımı
- Maliyet: ~0.5ms/frame (128×12 matmul + softmax)

**Kalite**: ORTA. CQT-based chroma'dan düşük ama key estimation, tonnetz, tension hesaplaması için yeterli. 200 Hz altında mel bin'leri birden fazla yarım ton kapsar — bu birincil hata kaynağıdır.

#### Karar 2: Beat Tracking — Onset Autocorrelation

**Algoritma**:

```
Girdi: onset_strength (B, T) — B grubu [11]'den

1. Onset strength'in autocorrelation'ını hesapla:
   oenv_centered = onset - onset.mean(dim=-1, keepdim=True)
   R = ifft(|fft(oenv_centered)|^2)  # Wiener-Khinchin
   R = R / R[..., 0:1]  # normalize

2. Tempo aralığını belirle (30-300 BPM → lag aralığı):
   lag_min = sr_frame / (300/60)  = 172.27 / 5.0  = 34 frame
   lag_max = sr_frame / (30/60)   = 172.27 / 0.5  = 344 frame

3. Dominant tempo periyodunu bul:
   tempo_lag = argmax(R[lag_min:lag_max]) + lag_min
   tempo_bpm = 60 * frame_rate / tempo_lag

4. Beat strength = R[tempo_lag]
5. Pulse clarity = R[tempo_lag] / median(R[lag_min:lag_max])
```

**PyTorch**: `torch.fft.rfft` → abs² → `torch.fft.irfft` → argmax
**Maliyet**: ~0.5ms/frame (FFT-based autocorrelation)

#### Karar 3: Entropy Window — τ = 2.0s

**Running statistics formülü**:

```
α = 1 - exp(-1 / (τ * frame_rate))  # decay factor
α = 1 - exp(-1 / (2.0 * 172.27)) = 0.0029

p̄_t = (1 - α) * p̄_{t-1} + α * p_t   # exponential moving average
σ̄²_t = (1 - α) * σ̄²_{t-1} + α * (p_t - p̄_t)²  # running variance

Warm-up:
confidence_t = min(1.0, t / (τ * frame_rate))  # 0→1 ramp over 344 frames
output_t = raw_entropy_t * confidence_t
```

**τ = 2.0s seçim gerekçesi**:
- 1.0s: ~172 frame, bir müzikal ölçüye yakın — çok gürültülü
- 2.0s: ~344 frame, 2 ölçü — temporal resolution ile stability dengesi
- 4.0s: ~688 frame — key/harmony analizi için iyi ama melodic entropy için çok yavaş

#### Karar 4: Modulation Spectrum Penceresi

```
window_size = 344 frame (~2.0s)     → 0.5 Hz frekans çözünürlüğü
hop_size = 86 frame (~0.5s)         → %75 overlap
fft_size = 512 (zero-padded)        → frekans çözünürlük artışı

Her mel band için:
1. mel_band[m, :] üzerinden sliding window (344 frame)
2. Hann window uygula
3. FFT → magnitude spectrum
4. Target frekans bin'lerini seç: 0.5, 1, 2, 4, 8, 16 Hz
5. Frame-level çıktıya lineer interpolasyon

İlk geçerli çıktı: frame 344'te
Warm-up: frame 0-343 arası → sıfır (veya kısmi pencere ile yaklaşık)
```

**PyTorch**: `torch.stft` veya manual `torch.fft.rfft` with sliding window via `unfold`

#### Karar 5: Hesaplama Sırası — 3-Stage DAG

```
                    ┌─────────────────────────────────────────┐
                    │            mel (B, 128, T)               │
                    └──┬──┬──┬──┬──┬──┬──────────────────────┘
                       │  │  │  │  │  │
  Stage 1 (parallel):  ▼  ▼  ▼  ▼  ▼  ▼
                      [A][B][C][D][F][J][K]
                       │  │  │  │  │  │  │
                       │  │  │  │  │  │  │
  Stage 2 (parallel):  │  │  │  │  │  │  │
                       └──┴──┴──┤  │  │  │
                          ┌─────┘  │  │  │
                          ▼     ┌──┘  │  │
                         [E]    │     │  │
                         (A,B,  ▼     │  │
                          C,D) [G]    │  │
                               (B[11])│  │
                                   ┌──┘  │
                                   ▼     │
                                  [H]    │
                                  (F     │
                                 chroma) │
                                   │     │
  Stage 3:                         │     │
                          ┌────────┤     │
                          ▼        ▼     │
                         [I]             │
                         (F chroma,      │
                          G onset,       │
                          H key)         │
                                         │
  Concat:     torch.cat([A,B,C,D,E,F,G,H,I,J,K], dim=-1) → (B, T, 128)
```

**Stage latency tahmini**:
- Stage 1: ~1.5ms (A-D: 0.4ms, F: 1.0ms, J: 0.5ms, K: 3.0ms → GPU parallel: max = 3.0ms)
- Stage 2: ~0.5ms (E: 0.1ms, G: 0.5ms, H: 1.0ms → GPU parallel: max = 1.0ms)
- Stage 3: ~0.5ms (I: 0.5ms)
- **Toplam: ~4.0ms/frame** (172 Hz = 5.8ms budget → **1.45× RT headroom**)

**Not**: K grubunun modulation hesaplaması amortized'dır (her frame'de tam FFT gerekmez, hop=86 frame). Gerçek ortalama K maliyeti ~0.5ms/frame.

#### Karar 6: E Grubu — 128D Korunur

**Mevcut** (R³ v1): 24D = 8+8+8 mekanik çarpım (A×B, D×A, A×C)
**Phase 6 planı**:
- Aşama 1: Proxy'leri kaldır, gerçek A-D çıktılarını referans et → 24D korunur
- Aşama 2 (ÖNERİ, R³ v2.1): Yeni cross-group interactions → +16D (F×A, G×B, H×D, I×D)
- **128D bütçe aşılmaz**. v2.1 genişleme ayrı tasarım dokümanı gerektirir.

#### Karar 7: Backward Compatibility — 3 Katman

| Katman | Phase | Değişiklik | Etki |
|--------|-------|------------|------|
| 1: İndeks koruma | 3B (şimdi) | [0:49] değişmez, [49:128] eklenir | Model doc'ları geçerli kalır |
| 2: Formül güncelleme | 6 | [0:49] formülleri revize edilir (bug fix + dedup) | Model code güncellenmeli |
| 3: Tam revizyon | 6+ | R3_DIM dinamik, feature_names registry'den | constants.py, dimension_map.py refactor |

---

## Bölüm 2: Grup Spesifikasyonları (A-K)

### Genel Bakış

| Grup | Ad | Aralık | Boyut | Durum | Stage |
|------|----|--------|-------|-------|-------|
| A | Consonance | [0:7] | 7D | MEVCUT | 1 |
| B | Energy | [7:12] | 5D | MEVCUT | 1 |
| C | Timbre | [12:21] | 9D | MEVCUT | 1 |
| D | Change | [21:25] | 4D | MEVCUT | 1 |
| E | Interactions | [25:49] | 24D | MEVCUT | 2 |
| **F** | **Pitch & Chroma** | **[49:65]** | **16D** | **YENİ** | 1 |
| **G** | **Rhythm & Groove** | **[65:75]** | **10D** | **YENİ** | 2 |
| **H** | **Harmony & Tonality** | **[75:87]** | **12D** | **YENİ** | 2 |
| **I** | **Information & Surprise** | **[87:94]** | **7D** | **YENİ** | 3 |
| **J** | **Timbre Extended** | **[94:114]** | **20D** | **YENİ** | 1 |
| **K** | **Modulation & Psychoacoustic** | **[114:128]** | **14D** | **YENİ** | 1 |
| | **Toplam** | **[0:128]** | **128D** | | |

---

### Group A: Consonance [0:7] — 7D (MEVCUT)

**PHASE 6: Formül revizyonu planlanmaktadır. Aşağıdaki spec'ler mevcut (v1) implementasyonu yansıtır.**

#### [0] roughness
- **Tanım**: Spektral varyans tabanlı pürüzlülük proxy'si
- **Formül**: `sigmoid(mel.var(dim=1) / mel.mean(dim=1))`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: sigmoid
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.var`, `torch.mean`, `torch.sigmoid`
- **Psikoakustik kaynak**: Plomp-Levelt 1965 (PROXY — gerçek P-L değil)
- **PHASE 6**: `var/mean` yerine gerçek critical band roughness: pairwise partial comparison within ERB bands

#### [1] sethares_dissonance
- **Tanım**: Komşu mel bin'lerin ortalama mutlak farkı
- **Formül**: `mean(|mel[k] - mel[k+1]|) / max`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization (frame-level max)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.diff`, `torch.abs`, `torch.mean`
- **Psikoakustik kaynak**: Sethares 1993 (PROXY — gerçek pairwise dissonance değil)
- **PHASE 6**: Gerçek Sethares timbre-dependent dissonance: spectral peak detection + pairwise `d(fi,fj,ai,aj)`

#### [2] helmholtz_kang
- **Tanım**: Lag-1 spektral otokorelasyon
- **Formül**: `corr(mel[k], mel[k+1]) = Σ(mel_c[k] · mel_c[k+1]) / (||mel_c|| · ||mel_c_shift||)` (mel_c = centered)
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Korelasyon doğal olarak [-1,1]; clamp(0,1)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Centered mel → element-wise multiply → sum → normalize
- **Psikoakustik kaynak**: Terhardt 1979 periodicity detection (yalnızca lag-1)
- **PHASE 6**: Multi-lag autocorrelation: `max_{τ>0} R(τ)/R(0)` for full harmonicity

#### [3] stumpf_fusion
- **Tanım**: Düşük frekans enerjisi oranı (alt çeyrek)
- **Formül**: `mel[:, :N//4, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran doğal olarak [0,1]
- **Parametreler**: N//4 = 32 mel bin sınırı
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + division
- **Psikoakustik kaynak**: Stumpf tonal fusion (PROXY — **≡warmth[12]** duplikat)
- **PHASE 6**: Gerçek Parncutt subharmonic matching ile değiştirilecek

#### [4] sensory_pleasantness
- **Tanım**: Uyumluluk ve füzyon bileşimi
- **Formül**: `0.6 * (1 - sethares[1]) + 0.4 * stumpf[3]`
- **Input**: [1] sethares_dissonance, [3] stumpf_fusion
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Lineer kombinasyon, doğal [0,1]
- **Parametreler**: Ağırlıklar 0.6, 0.4 (arbitrary)
- **Bağımlılıklar**: [1], [3]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Basit aritmetik
- **Psikoakustik kaynak**: Harrison & Pearce 2020 (arbitrary weights)
- **PHASE 6**: Ağırlıklar literatür verileriyle kalibre edilecek

#### [5] inharmonicity
- **Tanım**: Harmoniklik'in tersi
- **Formül**: `1 - helmholtz_kang[2]`
- **Input**: [2] helmholtz_kang
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Complement, doğal [0,1]
- **Parametreler**: Yok
- **Bağımlılıklar**: [2]
- **Tahmini maliyet**: <0.01 ms/frame
- **PyTorch notu**: `1.0 - x`
- **Psikoakustik kaynak**: DERIVED (bağımsız boyut değil)
- **PHASE 6**: Bağımsız feature ile değiştirilecek (spectral peak deviation from harmonic template)

#### [6] harmonic_deviation
- **Tanım**: Dissonans ve inharmonikliğin bileşimi
- **Formül**: `0.5 * sethares[1] + 0.5 * (1 - helmholtz[2])`
- **Input**: [1], [2]
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Lineer kombinasyon, doğal [0,1]
- **Parametreler**: Ağırlıklar 0.5, 0.5
- **Bağımlılıklar**: [1], [2]
- **Tahmini maliyet**: <0.01 ms/frame
- **PyTorch notu**: Basit aritmetik
- **Psikoakustik kaynak**: DERIVED (bağımsız boyut değil)
- **PHASE 6**: Bağımsız feature ile değiştirilecek (spectral_irregularity, Jensen 1999)

**A Grubu Phase 6 Özet**: Efektif bağımsız boyut ~3. [3]≡[12] duplikasyonu, [4-6] türetilmiş. Phase 6'da [0] gerçek Plomp-Levelt, [1] gerçek Sethares, [3] gerçek tonal fusion, [5-6] bağımsız feature'lar ile değiştirilecek.

---

### Group B: Energy [7:12] — 5D (MEVCUT)

**PHASE 6: Loudness çift-sıkıştırma düzeltmesi planlanmaktadır.**

#### [7] amplitude
- **Tanım**: Mel spektrumunun RMS enerjisi
- **Formül**: `mel.pow(2).mean(dim=1).sqrt() / max_val`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization (batch-level)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.pow`, `torch.mean`, `torch.sqrt`
- **Psikoakustik kaynak**: RMS energy (BUG: log-mel'den RMS → çift sıkıştırma)
- **PHASE 6**: Lineer güç spektrumundan RMS veya `exp(log_mel)` düzeltmesi

#### [8] velocity_A
- **Tanım**: Enerji değişim hızı (amplitude'un birinci türevi)
- **Formül**: `sigmoid((amp[t] - amp[t-1]) * 5.0)`
- **Input**: [7] amplitude
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: sigmoid (gain=5.0)
- **Parametreler**: gain = 5.0
- **Bağımlılıklar**: [7]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.diff` + `torch.sigmoid`
- **Psikoakustik kaynak**: Energy attack/decay rate
- **PHASE 6**: Sigmoid yerine min-max veya percentile normalization

#### [9] acceleration_A
- **Tanım**: Enerji değişim ivmesi (amplitude'un ikinci türevi)
- **Formül**: `sigmoid((vel[t] - vel[t-2]) * 5.0)`
- **Input**: [8] velocity_A
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: sigmoid (gain=5.0)
- **Parametreler**: gain = 5.0
- **Bağımlılıklar**: [8]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.diff` + `torch.sigmoid`
- **Psikoakustik kaynak**: Energy buildup curvature
- **PHASE 6**: Aynı sigmoid düzeltme

#### [10] loudness
- **Tanım**: Stevens yasası tabanlı gürüklük tahmini
- **Formül**: `(amplitude[7])^0.3 / max_val`
- **Input**: [7] amplitude
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization
- **Parametreler**: Stevens exponent = 0.3
- **Bağımlılıklar**: [7]
- **Tahmini maliyet**: <0.01 ms/frame
- **PyTorch notu**: `torch.pow(x, 0.3)`
- **Psikoakustik kaynak**: Stevens' power law (BUG: log-mel'e uygulama → çift sıkıştırma)
- **PHASE 6**: `exp(log_mel).pow(0.3)` veya tam Zwicker ISO 532-1 implementasyonu

#### [11] onset_strength
- **Tanım**: Yarım-dalga doğrultulmuş spektral akı (HWR)
- **Formül**: `relu(mel[:,:,t] - mel[:,:,t-1]).sum(dim=1) / max_val`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.relu`, frame diff, `torch.sum`
- **Psikoakustik kaynak**: Spectral flux (Weineck 2022 — en güçlü neural sync driver)
- **PHASE 6**: Değişiklik gerekmez — iyi valide edilmiş feature

**B Grubu Phase 6 Özet**: Loudness [10] çift sıkıştırma düzeltmesi kritik. Velocity/acceleration sigmoid normalizasyonu fiziksel anlam kaybettiriyor.

---

### Group C: Timbre [12:21] — 9D (MEVCUT)

**PHASE 6: 3 duplikasyon düzeltmesi planlanmaktadır.**

#### [12] warmth
- **Tanım**: Düşük frekans enerjisi oranı
- **Formül**: `mel[:, :N//4, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran, doğal [0,1]
- **Parametreler**: N//4 = 32 mel bin
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + div
- **Psikoakustik kaynak**: Low-frequency balance (**≡[3] stumpf_fusion** — birebir aynı formül)
- **PHASE 6**: [3] değiştirildiğinde duplikasyon çözülür; [12] mevcut haliyle korunur

#### [13] sharpness
- **Tanım**: Yüksek frekans enerjisi oranı
- **Formül**: `mel[:, 3*N//4:, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran, doğal [0,1]
- **Parametreler**: 3*N//4 = 96 mel bin sınırı
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + div
- **Psikoakustik kaynak**: DIN 45692 DEĞİL — basit oran
- **PHASE 6**: Değişiklik yok (K[122] sharpness_zwicker gerçek DIN 45692'yi sağlar)

#### [14] tonalness
- **Tanım**: Spektral tepe baskınlığı
- **Formül**: `mel.max(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran, doğal [0,1]
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.max`, `torch.sum`
- **Psikoakustik kaynak**: Terhardt 1979 tonalness proxy
- **PHASE 6**: Değişiklik yok

#### [15] clarity
- **Tanım**: Spektral centroid (normalize edilmiş)
- **Formül**: `sum(k * mel[k]) / sum(mel[k]) / N`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /N ile [0,1]
- **Parametreler**: N = 128
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Weighted mean with `torch.arange` weights
- **Psikoakustik kaynak**: Spectral centroid (yanlış isim — C80 değil)
- **PHASE 6**: İsim düzeltmesi (Phase 5 naming scope)

#### [16] spectral_smoothness
- **Tanım**: Spektral düzgünlük (düzensizliğin tersi)
- **Formül**: `1 - mean(|mel[k] - mel[k+1]|) / max_val` = `1 - sethares[1]`
- **Input**: mel (B, 128, T) (veya eşdeğer: 1 - [1])
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Complement
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok (veya [1])
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `1.0 - x`
- **Psikoakustik kaynak**: Krimphoff 1994 spectral irregularity (**= 1-[1]** complement)
- **PHASE 6**: spectral_spread (2nd central moment) ile değiştirilecek

#### [17] spectral_autocorrelation
- **Tanım**: Lag-1 spektral otokorelasyon
- **Formül**: [2] helmholtz_kang ile **birebir aynı hesaplama**
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Korelasyon
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Aynı [2]
- **Psikoakustik kaynak**: **≡[2] helmholtz_kang** DUPLIKAT
- **PHASE 6**: spectral_kurtosis (4th central moment) ile değiştirilecek

#### [18] tristimulus1
- **Tanım**: Alt üçte birlik enerji oranı
- **Formül**: `mel[:, :N//3, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran
- **Parametreler**: N//3 ≈ 42 mel bin
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + div
- **Psikoakustik kaynak**: Pollard-Jansson 1982 (mel-band proxy — gerçek tristimulus partial-based)

#### [19] tristimulus2
- **Tanım**: Orta üçte birlik enerji oranı
- **Formül**: `mel[:, N//3:2*N//3, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran
- **Parametreler**: N//3..2*N//3 ≈ 42..85 mel bin
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + div
- **Psikoakustik kaynak**: Pollard-Jansson 1982 (mel-band proxy)

#### [20] tristimulus3
- **Tanım**: Üst üçte birlik enerji oranı
- **Formül**: `mel[:, 2*N//3:, :].sum(dim=1) / mel.sum(dim=1)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran
- **Parametreler**: 2*N//3 ≈ 85 mel bin sınırı
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + div
- **Psikoakustik kaynak**: Pollard-Jansson 1982 (mel-band proxy)

**C Grubu Phase 6 Özet**: 3 duplikasyon ([12]≡[3], [16]=1-[1], [17]≡[2]) → efektif ~4D. Phase 6'da [16]→spectral_spread, [17]→spectral_kurtosis.

---

### Group D: Change [21:25] — 4D (MEVCUT)

**PHASE 6: Concentration normalizasyon bug'ı düzeltmesi planlanmaktadır.**

#### [21] spectral_flux
- **Tanım**: L2 tam-spektrum akısı
- **Formül**: `||mel[:,:,t] - mel[:,:,t-1]||₂ / max_val`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Frame diff → `torch.norm(dim=1, p=2)`
- **Psikoakustik kaynak**: Standard MIR spectral change

#### [22] distribution_entropy
- **Tanım**: Spektral dağılımın Shannon entropisi
- **Formül**: `-Σ p_k · log(p_k) / log(128)` where `p_k = mel_k / Σ mel_k`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(128) ile [0,1]
- **Parametreler**: N = 128
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Softmax → `-p * p.log()` → sum
- **Psikoakustik kaynak**: Shannon entropy — spektral düzgünlük ölçüsü

#### [23] distribution_flatness
- **Tanım**: Wiener entropisi (spektral düzlük)
- **Formül**: `exp(mean(log(p))) / mean(p)`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Doğal [0,1] (geometric/arithmetic mean oranı)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.log` → mean → `torch.exp` / `torch.mean`
- **Psikoakustik kaynak**: MPEG-7 spectral flatness

#### [24] distribution_concentration
- **Tanım**: Herfindahl-Hirschman indeksi tabanlı yoğunlaşma
- **Formül**: `(Σ p_k²) · N` → clamp(0,1)
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: clamp(0,1) (**BUG**: uniform→1.0, concentrated→1.0)
- **Parametreler**: N = 128
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `p.pow(2).sum() * N`
- **Psikoakustik kaynak**: Herfindahl-Hirschman Index
- **PHASE 6**: Doğru formül: `(HHI - 1/N) / (1 - 1/N)` → 0=uniform, 1=concentrated

**D Grubu Phase 6 Özet**: [24] normalizasyon bug'ı kritik. [22] ve [23] yüksek korelasyonlu.

---

### Group E: Interactions [25:49] — 24D (MEVCUT)

**PHASE 6: Proxy düzeltmesi ve potansiyel genişleme planlanmaktadır. Detay Bölüm 4'te.**

| Index | Feature Name | Hesaplama | Bileşenler |
|:-----:|-------------|-----------|------------|
| 25-32 | x_l0l5 (Energy × Consonance) | amp·roughness, amp·sethares, ... vel·stumpf | 8D: B[7:12]'nin ilk 4'ü × A[0:7]'nin ilk 2'si |
| 33-40 | x_l4l5 (Change × Consonance) | flux·roughness, ... entropy·stumpf | 8D: D[21:25] × A[0:7]'nin ilk 2'si |
| 41-48 | x_l5l7 (Consonance × Timbre) | roughness·warmth, ... stumpf·autocorr | 8D: A[0:7]'nin ilk 4'ü × C[12:21]'nin ilk 2'si |

**Mevcut sorunlar**:
1. Proxy mismatch: roughness_proxy `var()` kullanıyor, gerçek A[0] `var()/mean()` kullanıyor
2. Proxy mismatch: helmholtz_proxy `max/sum` (=tonalness) kullanıyor, gerçek A[2] lag-1 autocorrelation
3. Yalnızca 3 grup çifti kapsanıyor (A×B, D×A, A×C); F-K dahil değil

**E Grubu MEVCUT haliyle korunur. Phase 6 yeniden tasarımı Bölüm 4'te.**

---

### Group F: Pitch & Chroma [49:65] — 16D (YENİ)

**Bağımlılıklar**: Yok (doğrudan mel'den). H ve I grupları bu grubun chroma çıktısına bağlıdır.
**Pipeline stage**: 1 (parallel)
**Toplam maliyet**: ~1.5 ms/frame

#### [49-60] chroma_C, chroma_Db, chroma_D, chroma_Eb, chroma_E, chroma_F, chroma_Gb, chroma_G, chroma_Ab, chroma_A, chroma_Bb, chroma_B
- **Tanım**: 12 pitch class'ın enerji dağılımı — oktav eşdeğerliği ile fold edilmiş mel spektrumu
- **Formül**:
  ```
  mel_linear = exp(mel)                    # (B, 128, T) log→lineer
  M = pre_computed_chroma_matrix           # (128, 12) Gaussian soft-assignment
  chroma_raw = M.T @ mel_linear            # (B, 12, T)
  chroma = chroma_raw / chroma_raw.sum(dim=1, keepdim=True).clamp(min=1e-8)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 12), her bin [0,1], L1-normalized (toplam = 1.0)
- **Normalizasyon**: L1 normalization (chroma / sum)
- **Parametreler**:
  - σ = 0.5 semitone (Gaussian kernel genişliği)
  - sr = 44100 Hz, n_mels = 128, fmin = 0, fmax = sr/2
  - M matrisi: her mel bin'in MIDI pitch class'ına Gaussian soft-assignment
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~0.5 ms/frame (128×12 matmul)
- **PyTorch notu**: `M` → `self.register_buffer("mel_to_chroma", M)`. Hesaplama: `torch.matmul(M.T, mel_linear)` + L1 norm. M oluşturma: mel bin center frekansları → MIDI → PC → Gaussian weight.
- **Psikoakustik kaynak**: Octave equivalence (Shepard 1964); Krumhansl 1990

#### [61] pitch_height
- **Tanım**: Ağırlıklı ortalama log-frekans — algılanan genel perde yüksekliği
- **Formül**: `PH = Σ(log2(f_k) · M_k) / Σ(M_k)` normalize: `(PH - log2(fmin)) / (log2(fmax) - log2(fmin))`
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: min-max (audible range log2 mapping)
- **Parametreler**: f_k = pre-computed mel bin center frequencies; fmin=20 Hz, fmax=22050 Hz
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Pre-computed `log2_freqs` buffer; `(log2_freqs * mel_linear).sum(dim=1) / mel_linear.sum(dim=1)`
- **Psikoakustik kaynak**: Weber-Fechner yasası; perceived pitch ~ log(frequency)

#### [62] pitch_class_entropy
- **Tanım**: Chroma dağılımının Shannon entropisi — tonallik ölçüsü
- **Formül**: `H = -Σ chroma_c · log(chroma_c) / log(12)` (12 pitch class)
- **Input**: chroma [49:61]
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(12) ile [0,1]; 0=tek pitch class baskın, 1=uniform (kromatik)
- **Parametreler**: Yok
- **Bağımlılıklar**: [49:61] chroma
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `-(chroma * chroma.clamp(min=1e-8).log()).sum(dim=-1) / math.log(12)`
- **Psikoakustik kaynak**: Information theory; yüksek = kromatik/atonal, düşük = tonal

#### [63] pitch_salience
- **Tanım**: Spektral tepe belirginliği — harmonik çözünürlülük proxy'si
- **Formül**:
  ```
  peak_energy = mel.max(dim=1).values         # (B, T)
  noise_floor = mel.median(dim=1).values       # (B, T)
  salience = (peak_energy - noise_floor) / (peak_energy + noise_floor + 1e-8)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Doğal [0,1] (normalized difference)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.max`, `torch.median`
- **Psikoakustik kaynak**: Parncutt 1989 virtual pitch salience (proxy — gerçek harmonic template matching değil)

#### [64] inharmonicity_index
- **Tanım**: Spektral tepe frekanslarının harmonik seriden sapması
- **Formül**:
  ```
  # Mel üzerinden en belirgin tepe → f0 tahmini
  f0_bin = mel.argmax(dim=1)                    # (B, T)
  f0 = mel_center_freqs[f0_bin]                 # Hz
  # Harmonik template oluştur: f0, 2*f0, 3*f0, ..., K*f0
  # Her harmonik için en yakın mel bin'deki enerji ile karşılaştır
  # INH = Σ_k |f_peak_k - k*f0| / (k*f0) / K
  harmonics = f0.unsqueeze(-1) * torch.arange(1, K+1)  # (B, T, K)
  harmonic_bins = freq_to_mel_bin(harmonics)
  expected = mel.gather(1, harmonic_bins)
  deviation = (harmonic_bins_freq - harmonics).abs() / harmonics
  inharmonicity = deviation.mean(dim=-1)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: clamp(0, 1) — tipik değerler 0-0.5 arası
- **Parametreler**: K = 8 (harmonik sayısı)
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~1.0 ms/frame (mel peak search + harmonic template matching)
- **PyTorch notu**: `torch.argmax`, pre-computed freq mapping, `torch.gather`
- **Psikoakustik kaynak**: Harmonic series deviation; piano inharmonicity modeli

---

### Group G: Rhythm & Groove [65:75] — 10D (YENİ)

**Bağımlılıklar**: B[11] onset_strength gerekli.
**Pipeline stage**: 2 (B tamamlandıktan sonra)
**Toplam maliyet**: ~2.0 ms/frame

#### [65] tempo_estimate
- **Tanım**: Baskın tempo tahmini (BPM, normalize edilmiş)
- **Formül**:
  ```
  oenv = onset_strength[B[11]]                    # (B, T)
  oenv_c = oenv - oenv.mean(dim=-1, keepdim=True)
  R = irfft(|rfft(oenv_c)|^2)                     # autocorrelation
  R = R / R[..., 0:1].clamp(min=1e-8)             # normalize
  lag_min = round(frame_rate / 5.0)  # 300 BPM → 34 frame
  lag_max = round(frame_rate / 0.5)  # 30 BPM  → 344 frame
  tempo_lag = argmax(R[..., lag_min:lag_max]) + lag_min
  tempo_bpm = 60 * frame_rate / tempo_lag
  tempo_norm = (tempo_bpm - 30) / (300 - 30)      # [0,1]
  ```
- **Input**: B[11] onset_strength (B, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: min-max (30-300 BPM → [0,1])
- **Parametreler**: frame_rate = 172.27 Hz, BPM aralığı = [30, 300]
- **Bağımlılıklar**: B[11]
- **Tahmini maliyet**: ~0.5 ms/frame (FFT-based autocorrelation)
- **PyTorch notu**: `torch.fft.rfft` → `.abs().pow(2)` → `torch.fft.irfft` → `torch.argmax`
- **Psikoakustik kaynak**: Fraisse 1982 preferred tempo; entrainment

#### [66] beat_strength
- **Tanım**: Tahmini tempo periyodundaki otokorelasyon tepe değeri
- **Formül**: `beat_strength = R[tempo_lag]` (autocorrelation değeri)
- **Input**: R (autocorrelation), tempo_lag (from [65])
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: R zaten [0,1] normalize edilmiş
- **Parametreler**: Yok (tempo_lag'a bağlı)
- **Bağımlılıklar**: [65] tempo_estimate (paylaşılan autocorrelation hesaplaması)
- **Tahmini maliyet**: <0.1 ms/frame (R zaten hesaplanmış)
- **PyTorch notu**: `R.gather(-1, tempo_lag.unsqueeze(-1))`
- **Psikoakustik kaynak**: Pulse perception strength

#### [67] pulse_clarity
- **Tanım**: Beat belirginliği — autocorrelation tepe/taban oranı
- **Formül**: `pulse_clarity = R[tempo_lag] / median(R[lag_min:lag_max])`  → clamp(0, 1)
- **Input**: R (autocorrelation), tempo_lag
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Oran → sigmoid veya clamp; `1 / (1 + exp(-5*(ratio - 2)))` ile [0,1]
- **Parametreler**: sigmoid gain = 5, center = 2
- **Bağımlılıklar**: [65] autocorrelation
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.median`, ratio, `torch.sigmoid`
- **Psikoakustik kaynak**: Beat ambiguity ↔ groove (Witek 2014)

#### [68] syncopation_index
- **Tanım**: Metrik grid'e göre off-beat vurgulama derecesi (LHL modeli)
- **Formül**:
  ```
  # 1. Onset peak tespiti (B[11] > threshold)
  peaks = detect_peaks(onset_strength, threshold=0.3)   # binary mask (B, T)

  # 2. Metrik grid oluştur (tempo_lag periyoduyla)
  beat_grid = create_metrical_grid(tempo_lag, levels=4)  # 4 seviye: bar, beat, sub-beat, sub-sub
  # LHL metrik ağırlıklar: bar=0, beat=1, sub=2, sub-sub=3 (düşük = güçlü)

  # 3. Syncopation = onset'in metrik zayıf pozisyondaki gücü
  # S = Σ max(0, weight[onset_pos] - weight[next_strong_beat]) / N_onsets
  syncopation = lhl_syncopation(peaks, beat_grid)
  syncopation_norm = syncopation / max_possible_syncopation  # [0,1]
  ```
- **Input**: B[11] onset_strength, [65] tempo_lag
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /max_possible ile [0,1]
- **Parametreler**: peak_threshold = 0.3, metrical_levels = 4
- **Bağımlılıklar**: B[11], [65]
- **Tahmini maliyet**: ~0.5 ms/frame
- **PyTorch notu**: Peak detection via `F.max_pool1d` → metrical grid creation → weighted sum
- **Psikoakustik kaynak**: Longuet-Higgins & Lee 1984; Witek 2014 groove-pleasure relationship

#### [69] metricality_index
- **Tanım**: Çoklu ölçekte iç içe geçmiş ritmik katman sayısı
- **Formül**:
  ```
  # Multi-scale autocorrelation: subdivisions of tempo_lag
  ratios = [1, 2, 3, 4, 6, 8]  # subdivisions
  metricality = 0
  for r in ratios:
      sub_lag = tempo_lag / r
      if R[sub_lag] > clarity_threshold:
          metricality += 1
  metricality_norm = metricality / len(ratios)  # [0,1]
  ```
- **Input**: R (autocorrelation), tempo_lag
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /len(ratios) ile [0,1]
- **Parametreler**: ratios = [1,2,3,4,6,8], clarity_threshold = 0.1
- **Bağımlılıklar**: [65] autocorrelation
- **Tahmini maliyet**: <0.1 ms/frame (R zaten hesaplanmış, 6 lookup)
- **PyTorch notu**: Index gathering from R at subdivision lags
- **Psikoakustik kaynak**: Grahn & Brett 2007 — metrical hierarchy; Morris multi-scale nesting

#### [70] isochrony_nPVI
- **Tanım**: Ritmik düzenlilik ölçüsü (normalized Pairwise Variability Index)
- **Formül**:
  ```
  # Onset zamanlarından IOI (inter-onset-interval) hesapla
  onset_times = nonzero(peaks)                     # peak positions
  IOI = diff(onset_times)                          # intervals
  nPVI = 100 * mean(|IOI_k - IOI_{k+1}| / ((IOI_k + IOI_{k+1})/2))
  isochrony = 1 - nPVI / 200  # inverse, [0,1]: 1=perfect isochrony, 0=max variability
  ```
- **Input**: B[11] onset peaks
- **Output**: (B, T, 1), [0,1] (window-level → frame-level interpolation)
- **Normalizasyon**: 1 - nPVI/200 (nPVI tipik 0-200 arası)
- **Parametreler**: peak_threshold = 0.3, window = 344 frames
- **Bağımlılıklar**: B[11]
- **Tahmini maliyet**: ~0.3 ms/frame
- **PyTorch notu**: `torch.nonzero`, `torch.diff`, sliding window statistics
- **Psikoakustik kaynak**: Ravignani 2021 rhythmic regularity; nPVI (Grabe & Low 2002)

#### [71] groove_index
- **Tanım**: Hareket-tetikleyici müzikal kalite — syncopation, bass enerji ve beat clarity'nin bileşimi
- **Formül**:
  ```
  bass_energy = mel[:, :16, :].mean(dim=1)       # düşük frekans enerjisi
  bass_norm = bass_energy / bass_energy.max()
  groove = syncopation[68] * bass_norm * pulse_clarity[67]
  groove_norm = groove / groove.max().clamp(min=1e-8)
  ```
- **Input**: [68] syncopation, [67] pulse_clarity, mel (bass band)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization
- **Parametreler**: bass_band = mel[:, :16, :] (ilk 16 mel bin ≈ 0-300 Hz)
- **Bağımlılıklar**: [67], [68]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Element-wise multiply + normalize
- **Psikoakustik kaynak**: Madison 2006, Janata 2012 — sensorimotor coupling; groove = syncopation × bass × clarity

#### [72] event_density
- **Tanım**: Birim zamandaki onset sayısı
- **Formül**:
  ```
  # Sliding window (1s = 172 frame) içindeki onset peak sayısı
  peaks = (onset_strength > threshold).float()    # binary
  density = F.avg_pool1d(peaks, kernel_size=172, stride=1, padding=86)
  density_norm = density / max_density            # max_density = ~20 onset/s
  ```
- **Input**: B[11] onset_strength
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /max_density (tipik üst sınır = 20 onset/s)
- **Parametreler**: threshold = 0.3, window = 172 frame (1s), max_density = 20
- **Bağımlılıklar**: B[11]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `F.avg_pool1d` with padding
- **Psikoakustik kaynak**: Temporal event density

#### [73] tempo_stability
- **Tanım**: Yerel tempo tahminlerinin kararlılığı
- **Formül**:
  ```
  # Sliding window (2s = 344 frame) üzerinde lokal tempo variance
  local_tempo = sliding_window_tempo(onset_strength, window=344, hop=86)
  stability = 1 - std(local_tempo) / mean(local_tempo)  # CV inverse
  stability_norm = stability.clamp(0, 1)
  ```
- **Input**: B[11] onset_strength
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: clamp(0,1) — 1=sabit tempo, 0=çok değişken
- **Parametreler**: window = 344 frame, hop = 86 frame
- **Bağımlılıklar**: B[11]
- **Tahmini maliyet**: ~0.3 ms/frame (sliding window autocorrelation)
- **PyTorch notu**: `Tensor.unfold` → per-window autocorrelation → argmax → std/mean
- **Psikoakustik kaynak**: Temporal prediction reliability

#### [74] rhythmic_regularity
- **Tanım**: IOI dağılımının düzenliliği (entropi tersi)
- **Formül**:
  ```
  # IOI histogram (quantized to 16 bins)
  IOI_hist = histogram(IOI, bins=16, range=(0, max_IOI))
  IOI_prob = IOI_hist / IOI_hist.sum()
  entropy = -sum(p * log(p)) / log(16)
  regularity = 1 - entropy                        # [0,1]: 1=düzenli, 0=düzensiz
  ```
- **Input**: B[11] onset peaks → IOI
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: 1 - normalized_entropy
- **Parametreler**: bins = 16, max_IOI = 2s (344 frame)
- **Bağımlılıklar**: B[11]
- **Tahmini maliyet**: ~0.2 ms/frame
- **PyTorch notu**: `torch.histc` veya manual binning → entropy
- **Psikoakustik kaynak**: Rhythmic entropy inverse (Spiech 2022)

---

### Group H: Harmony & Tonality [75:87] — 12D (YENİ)

**Bağımlılıklar**: F[49:61] chroma çıktısı gerekli.
**Pipeline stage**: 2 (F tamamlandıktan sonra)
**Toplam maliyet**: ~2.0 ms/frame

#### [75] key_clarity
- **Tanım**: Tonal merkez gücü — Krumhansl-Schmuckler key profilleri ile korelasyon
- **Formül**:
  ```
  # 24 key profili (12 major + 12 minor)
  # Krumhansl-Kessler probe-tone ratings:
  major = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
  minor = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]

  # Her key için chroma rotate et ve correlate
  key_corrs = []
  for shift in range(12):
      for template in [major, minor]:
          rotated = roll(chroma, shift)
          corr = pearson_correlation(rotated, template)
          key_corrs.append(corr)

  key_clarity = max(key_corrs)  # en iyi key match
  # Doğal aralık ~[0.3, 0.95]; normalize:
  key_clarity_norm = (key_clarity - 0.3) / 0.65  → clamp(0, 1)
  ```
- **Input**: F[49:61] chroma (B, T, 12)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: min-max (empirik 0.3-0.95 → [0,1])
- **Parametreler**: 24 key profili (Krumhansl-Kessler), `register_buffer`
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: ~1.0 ms/frame (24 korelasyon hesaplaması → batch matmul ile hızlandırılır)
- **PyTorch notu**: Key profilleri (24, 12) matris → `torch.matmul(chroma, key_profiles.T)` → max. `torch.roll` ile 12 rotation.
- **Psikoakustik kaynak**: Krumhansl & Kessler 1982 tonal hierarchy

#### [76-81] tonnetz_fifth_x, tonnetz_fifth_y, tonnetz_minor_x, tonnetz_minor_y, tonnetz_major_x, tonnetz_major_y
- **Tanım**: 6D Tonnetz koordinatları — beşli, minör üçlü, majör üçlü ilişkilerini kodlayan dairesel projeksiyon
- **Formül** (Harte 2006):
  ```
  # Chroma c = (c_0, c_1, ..., c_11) L1-normalized
  # φ_1 = 7π/6 (beşli), φ_2 = 3π/6 (minör üçlü), φ_3 = 4π/6 (majör üçlü)

  tonnetz_fifth_x  = Σ_k c_k · sin(k · 7π/6)
  tonnetz_fifth_y  = Σ_k c_k · cos(k · 7π/6)
  tonnetz_minor_x  = Σ_k c_k · sin(k · 3π/6)
  tonnetz_minor_y  = Σ_k c_k · cos(k · 3π/6)
  tonnetz_major_x  = Σ_k c_k · sin(k · 4π/6)
  tonnetz_major_y  = Σ_k c_k · cos(k · 4π/6)
  ```
- **Input**: F[49:61] chroma (B, T, 12)
- **Output**: (B, T, 6), her biri [-1, 1]
- **Normalizasyon**: sin/cos doğal olarak [-1,1]; `(tonnetz + 1) / 2` ile [0,1]'e dönüştür
- **Parametreler**: φ_1=7π/6, φ_2=3π/6, φ_3=4π/6 (pre-computed sin/cos matrisleri)
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: ~0.1 ms/frame (6 dot product)
- **PyTorch notu**: Pre-computed `tonnetz_matrix` (12, 6) → `torch.matmul(chroma, tonnetz_matrix)`. Matrix: `T[k,0] = sin(k*7π/6)`, `T[k,1] = cos(k*7π/6)`, etc.
- **Psikoakustik kaynak**: Harte 2006; Balzano 1980; Krumhansl & Kessler empirical proximity ≈ Tonnetz geometry

#### [82] voice_leading_distance
- **Tanım**: Ardışık chroma vektörleri arasındaki L1 mesafesi — ses yürütme pürüzsüzlüğü
- **Formül**: `VL_t = Σ_k |chroma_t[k] - chroma_{t-1}[k]|`
- **Input**: F[49:61] chroma (B, T, 12)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /2.0 (L1 norm of two L1-normalized vectors max = 2.0) → clamp(0,1)
- **Parametreler**: Yok
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `(chroma[:, 1:] - chroma[:, :-1]).abs().sum(dim=-1) / 2.0`
- **Psikoakustik kaynak**: Tymoczko voice-leading parsimony

#### [83] harmonic_change
- **Tanım**: Frame-to-frame harmonik değişim büyüklüğü (kosinüs mesafesi)
- **Formül**: `HC_t = 1 - cos(chroma_t, chroma_{t-1})`
- **Input**: F[49:61] chroma (B, T, 12)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Cosine distance doğal [0,2]; tipik [0,1]; clamp(0,1)
- **Parametreler**: Yok
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `F.cosine_similarity(chroma[:,1:], chroma[:,:-1], dim=-1)` → `1 - sim`
- **Psikoakustik kaynak**: Harmonic change detection function (HCDF)

#### [84] tonal_stability
- **Tanım**: Tonal merkezin zaman içindeki kararlılığı
- **Formül**:
  ```
  # Harmonic change rate'in tersi × key clarity
  hc_rate = running_mean(harmonic_change[83], window=172)  # 1s window
  tonal_stability = key_clarity[75] * (1 - hc_rate)
  ```
- **Input**: [75] key_clarity, [83] harmonic_change
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Product of [0,1] values → doğal [0,1]
- **Parametreler**: smoothing window = 172 frame (1s)
- **Bağımlılıklar**: [75], [83]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `F.avg_pool1d` for smoothing → multiply
- **Psikoakustik kaynak**: ÖNERİ — Krumhansl stability concept

#### [85] diatonicity
- **Tanım**: Tymoczko macroharmony — diyatonik vs kromatik içerik
- **Formül**:
  ```
  # Pencere içinde aktif pitch class sayısı (energy > threshold)
  active_pcs = (chroma > 0.05).float().sum(dim=-1)  # 0-12 arası
  diatonicity = 1 - (active_pcs - 7) / 5            # 7 PC = diyatonik
  diatonicity_norm = diatonicity.clamp(0, 1)
  ```
- **Input**: F[49:61] chroma
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Lineer mapping: 7 PC → 1.0 (tam diyatonik), 12 PC → 0.0 (tam kromatik)
- **Parametreler**: threshold = 0.05 (chroma activation threshold)
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Threshold → sum → linear transform
- **Psikoakustik kaynak**: Tymoczko macroharmony (Mh)

#### [86] syntactic_irregularity
- **Tanım**: Harmonik sözdizim ihlali — mevcut chroma'nın diyatonik key template'inden KL sapması
- **Formül**:
  ```
  # Best key template (from key_clarity computation)
  best_template = key_profiles[best_key_idx]         # (12,)
  template_prob = best_template / best_template.sum()
  chroma_prob = chroma.clamp(min=1e-8)
  KL = (chroma_prob * (chroma_prob.log() - template_prob.log())).sum(dim=-1)
  irregularity = 1 - exp(-KL)                        # [0,1]
  ```
- **Input**: F[49:61] chroma, [75] key profili
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: `1 - exp(-KL)` ile [0,1]
- **Parametreler**: Yok (key template [75]'den)
- **Bağımlılıklar**: F[49:61], [75]
- **Tahmini maliyet**: ~0.1 ms/frame
- **PyTorch notu**: KL divergence + exponential mapping
- **Psikoakustik kaynak**: Lerdahl 2001 tonal tension hierarchy

---

### Group I: Information & Surprise [87:94] — 7D (YENİ)

**Bağımlılıklar**: F[49:61] chroma, G onset bilgisi, H[75] key clarity
**Pipeline stage**: 3 (F, G, H tamamlandıktan sonra)
**Toplam maliyet**: ~2.0 ms/frame

**Ortak running statistics mekanizması** (tüm I grubu feature'ları paylaşır):
```
α = 1 - exp(-1 / (τ * frame_rate))   # τ = 2.0s → α ≈ 0.0029
p̄_t = (1 - α) · p̄_{t-1} + α · p_t   # EMA
confidence_t = min(1.0, t / 344)       # warm-up ramp (344 frame = 2s)
```

#### [87] melodic_entropy
- **Tanım**: Frame-to-frame chroma geçiş dağılımının entropisi — melodik sürpriz proxy'si
- **Formül**:
  ```
  # Chroma transition: hangi PC'den hangi PC'ye geçiş yapıldı?
  dominant_pc_t = argmax(chroma_t)             # (B, T)
  dominant_pc_t1 = argmax(chroma_{t-1})        # (B, T)
  transition = (dominant_pc_t1 * 12 + dominant_pc_t)  # 144 olası geçiş

  # Running transition histogram (EMA)
  transition_counts_t = (1-α) * transition_counts_{t-1}
  transition_counts_t[transition] += α

  # Conditional entropy
  row = transition_counts_t[dominant_pc_t1, :]  # current PC row
  row_prob = row / row.sum()
  H = -Σ row_prob * log(row_prob) / log(12)    # [0,1]
  melodic_entropy = H * confidence_t
  ```
- **Input**: F[49:61] chroma
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(12); warm-up confidence ramp
- **Parametreler**: τ = 2.0s, α ≈ 0.0029, transition_matrix = (12, 12)
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: ~0.3 ms/frame
- **PyTorch notu**: Running histogram (12×12 matrix) güncelleme; `torch.argmax`, index update, entropy
- **Psikoakustik kaynak**: IDyOM melodic IC approximation (Pearce 2005)
- **Not**: Tam IDyOM kalitesinde değil — chroma-based transition entropy bir yaklaşımdır

#### [88] harmonic_entropy
- **Tanım**: Mevcut chroma'nın beklenen chroma'dan KL sapması — harmonik sürpriz
- **Formül**:
  ```
  chroma_avg = EMA(chroma, α)                   # running average chroma
  KL = Σ chroma_t * log(chroma_t / chroma_avg)  # KL divergence
  harmonic_entropy = (1 - exp(-KL)) * confidence_t  # [0,1]
  ```
- **Input**: F[49:61] chroma
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: `1 - exp(-KL)` + warm-up
- **Parametreler**: τ = 2.0s
- **Bağımlılıklar**: F[49:61]
- **Tahmini maliyet**: ~0.2 ms/frame
- **PyTorch notu**: EMA update + KL divergence + exp mapping
- **Psikoakustik kaynak**: Gold 2019 chord transition probability; IDyOM harmonic IC

#### [89] rhythmic_information_content
- **Tanım**: Mevcut IOI'nin bağlamsal beklenmedikliği — ritmik sürpriz
- **Formül**:
  ```
  # Current IOI (onset zamanları arasındaki fark)
  current_IOI = t - last_onset_time
  IOI_quantized = round(current_IOI / beat_period * 4) / 4  # 16th note quantize

  # Running IOI histogram (EMA)
  IOI_hist = EMA(IOI_histogram, α)
  p_IOI = IOI_hist[IOI_quantized] / IOI_hist.sum()

  rhythmic_IC = -log(p_IOI.clamp(min=1e-8)) / log(16)  # [0,1] (16 IOI bins)
  rhythmic_IC = rhythmic_IC * confidence_t
  ```
- **Input**: B[11] onset peaks, [65] tempo estimate
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(16) + warm-up
- **Parametreler**: τ = 2.0s, IOI bins = 16, quantize resolution = 1/4 beat
- **Bağımlılıklar**: B[11], [65]
- **Tahmini maliyet**: ~0.2 ms/frame
- **PyTorch notu**: Running histogram + log probability
- **Psikoakustik kaynak**: Spiech 2022; Shannon information content

#### [90] spectral_surprise
- **Tanım**: Frame-level spektral beklenmediklik — mevcut mel ve running average arasındaki KL sapması
- **Formül**:
  ```
  mel_prob_t = mel_t / mel_t.sum(dim=1, keepdim=True).clamp(min=1e-8)
  mel_avg = EMA(mel_prob, α)                    # (B, 128, T)
  KL = Σ_k mel_prob_t[k] * log(mel_prob_t[k] / mel_avg[k])
  spectral_surprise = (1 - exp(-KL)) * confidence_t
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: `1 - exp(-KL)` + warm-up
- **Parametreler**: τ = 2.0s
- **Bağımlılıklar**: Yok (doğrudan mel'den, ama running state gerekli)
- **Tahmini maliyet**: ~0.3 ms/frame
- **PyTorch notu**: EMA update (128D vector) + KL divergence
- **Psikoakustik kaynak**: Prediction error / free energy (Friston); mismatch negativity

#### [91] information_rate
- **Tanım**: Ardışık frame'ler arası karşılıklı bilgi — frame başına yeni bilgi miktarı
- **Formül**:
  ```
  H_t = entropy(mel_prob_t)                     # current frame entropy
  H_t1 = entropy(mel_prob_{t-1})                # previous frame entropy
  H_joint = entropy(concat(mel_prob_t, mel_prob_{t-1}) / 2)  # joint
  MI = H_t + H_t1 - 2 * H_joint                # mutual information approx
  info_rate = MI / log(128)                     # normalize [0,1]
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(128)
- **Parametreler**: Yok
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~0.2 ms/frame
- **PyTorch notu**: Entropy computation × 3; frame pair comparison
- **Psikoakustik kaynak**: Weineck 2022 spectral flux → neural sync; information theory

#### [92] predictive_entropy
- **Tanım**: Koşullu dağılım entropisi — gelecek frame tahmininin belirsizliği
- **Formül**:
  ```
  # Running conditional statistics: p(mel_t | context)
  # context = EMA of mel (running average acts as predictor)
  residual = mel_prob_t - mel_avg                # prediction error
  residual_var = EMA(residual^2, α)              # running error variance
  predictive_entropy = 0.5 * log(2π·e·residual_var.mean()) / log(128)
  predictive_entropy = predictive_entropy.clamp(0, 1) * confidence_t
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: Gaussian entropy formula + normalize + warm-up
- **Parametreler**: τ = 2.0s
- **Bağımlılıklar**: Yok (internal running state)
- **Tahmini maliyet**: ~0.2 ms/frame
- **PyTorch notu**: EMA variance + Gaussian entropy formula
- **Psikoakustik kaynak**: Predictive coding framework (Friston); uncertainty quantification

#### [93] tonal_ambiguity
- **Tanım**: Key profil korelasyonlarının softmax entropisi — tonal belirsizlik
- **Formül**:
  ```
  key_corrs = compute_all_24_key_correlations(chroma)  # (B, T, 24)
  key_probs = softmax(key_corrs * temperature)          # temperature = 5.0
  H = -Σ key_probs * log(key_probs) / log(24)          # [0,1]
  tonal_ambiguity = H
  ```
- **Input**: F[49:61] chroma, H[75] key correlation (paylaşılan hesaplama)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /log(24) ile [0,1]; 0=net tonalite, 1=tam belirsiz
- **Parametreler**: temperature = 5.0 (softmax sharpness)
- **Bağımlılıklar**: F[49:61], H[75] (paylaşılan key correlation hesaplaması)
- **Tahmini maliyet**: ~0.1 ms/frame (key correlations H'de zaten hesaplanmış)
- **PyTorch notu**: `F.softmax(key_corrs * 5.0, dim=-1)` → entropy
- **Psikoakustik kaynak**: Tonal ambiguity; ÖNERİ — information-theoretic key uncertainty

---

### Group J: Timbre Extended [94:114] — 20D (YENİ)

**Bağımlılıklar**: Yok (doğrudan mel'den).
**Pipeline stage**: 1 (parallel)
**Toplam maliyet**: ~0.5 ms/frame

#### [94-106] mfcc_1 ... mfcc_13
- **Tanım**: Mel-Frequency Cepstral Coefficients — ses tınısının kompakt temsili
- **Formül**:
  ```
  # DCT-II of log-mel spectrogram
  # Pre-computed DCT matrix D (128 × 13):
  # D[m, k] = sqrt(2/128) * cos(π * k * (2m+1) / (2*128))  for k=1..13
  # (k=0 DC bileşeni atlanır)

  mfcc = D.T @ mel                             # (B, 13, T)
  # Normalizasyon: her MFCC katsayısı farklı aralıkta
  # Empirik normalizasyon: MFCC_k / max(|MFCC_k|) → [-1,1] → (x+1)/2 → [0,1]
  mfcc_norm = (mfcc / mfcc_scale + 1) / 2     # mfcc_scale pre-computed
  ```
- **Input**: mel (B, 128, T) — log-mel spectrogram
- **Output**: (B, T, 13), her biri [0,1]
- **Normalizasyon**: Per-coefficient empirik scaling → [-1,1] → shift to [0,1]
- **Parametreler**:
  - DCT matrix D: (128, 13), pre-computed `register_buffer`
  - mfcc_scale: (13,), per-coefficient max absolute value (dataset statistics)
  - Önerilen scale değerleri: [40, 80, 60, 50, 40, 35, 30, 25, 22, 20, 18, 16, 15]
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~0.3 ms/frame (128×13 matmul)
- **PyTorch notu**: `torch.matmul(D.T, mel)`. Alternatif: `torch.fft.dct` (PyTorch ≥2.1, varsa). DCT matrisi `__init__`'te oluşturulur.
- **Psikoakustik kaynak**: Cepstral analiz; vokal tract shape proxy; MIR'ın en yaygın feature'ı

#### [107-113] spectral_contrast_1 ... spectral_contrast_7
- **Tanım**: Oktav alt-bantlarındaki tepe-vadi farkı — harmonik vs gürültülü doku ayrımı
- **Formül**:
  ```
  # 7 oktav sub-band (6 band + 1 residual)
  # Band sınırları (mel bin indeksleri, yaklaşık):
  bands = [(0,4), (4,8), (8,16), (16,32), (32,64), (64,96), (96,128)]

  for band_start, band_end in bands:
      band = mel[:, band_start:band_end, :]
      sorted_band = sort(band, dim=1)
      n = band_end - band_start
      alpha = max(1, round(0.2 * n))           # %20 quantile

      peak = sorted_band[:, -alpha:, :].mean(dim=1)   # top 20%
      valley = sorted_band[:, :alpha, :].mean(dim=1)   # bottom 20%
      contrast = peak - valley                          # log domain'de fark

  # Stack → (B, T, 7)
  # Normalizasyon: contrast tipik [0, 10] arası (log-mel); /10 → [0,1]
  contrast_norm = contrast / 10.0
  contrast_norm = contrast_norm.clamp(0, 1)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 7), her biri [0,1]
- **Normalizasyon**: /10.0 + clamp (empirik üst sınır)
- **Parametreler**: 7 band sınırı, alpha = 0.2 (quantile fraction)
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~0.2 ms/frame (per-band sort + mean)
- **PyTorch notu**: `torch.sort` per band → slice top/bottom → mean → diff
- **Psikoakustik kaynak**: Jiang 2002 spectral contrast; harmonik vs noisy texture distinction

---

### Group K: Modulation & Psychoacoustic [114:128] — 14D (YENİ)

**Bağımlılıklar**: Yok (doğrudan mel'den).
**Pipeline stage**: 1 (parallel)
**Toplam maliyet**: ~3.0 ms/frame (amortized ~0.5 ms due to hop-based computation)

#### [114-119] modulation_0_5Hz, modulation_1Hz, modulation_2Hz, modulation_4Hz, modulation_8Hz, modulation_16Hz
- **Tanım**: Mel temporal envelope'unun modulation spectrum'u — belirli AM hızlarındaki enerji
- **Formül**:
  ```
  # Her mel band için temporal envelope'un sliding FFT'si
  window_size = 344                              # ~2.0s
  hop_size = 86                                  # ~0.5s, %75 overlap
  hann = torch.hann_window(window_size)

  # Mel temporal envelope (per-band)
  mel_env = mel.abs()                            # (B, 128, T)

  # Sliding window FFT
  windows = mel_env.unfold(-1, window_size, hop_size)  # (B, 128, N_win, window_size)
  windowed = windows * hann
  fft_mag = torch.fft.rfft(windowed).abs()       # (B, 128, N_win, fft_bins)

  # Target modulation rates → FFT bin indeksleri
  # freq_resolution = frame_rate / fft_size = 172.27 / 512 = 0.336 Hz
  target_rates = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]  # Hz
  target_bins = [round(r / 0.336) for r in target_rates]  # [1, 3, 6, 12, 24, 48]

  # Per-rate: tüm mel band'lardaki ortalama modulation enerji
  for i, bin_idx in enumerate(target_bins):
      mod_energy[i] = fft_mag[:, :, :, bin_idx].mean(dim=1)  # (B, N_win)

  # Frame-level interpolasyon (N_win → T)
  mod_frame = F.interpolate(mod_energy, size=T, mode='linear')

  # Normalizasyon: per-rate max-norm → [0,1]
  mod_norm = mod_frame / mod_frame.max(dim=-1, keepdim=True).clamp(min=1e-8)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 6), her biri [0,1]
- **Normalizasyon**: Per-rate max-normalization
- **Parametreler**: window=344, hop=86, fft_size=512, target_rates=[0.5,1,2,4,8,16] Hz
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~3.0 ms/frame (amortized ~0.5 ms; tam FFT her 86 frame'de bir)
- **PyTorch notu**: `Tensor.unfold` → `torch.fft.rfft` → `F.interpolate`. Warm-up: ilk 344 frame sıfır.
- **Psikoakustik kaynak**: Chi & Shamma 2005 cortical temporal modulation model

#### [120] modulation_centroid
- **Tanım**: Modulation spectrum'un ağırlıklı merkezi — baskın modulation hızı
- **Formül**:
  ```
  rates = tensor([0.5, 1.0, 2.0, 4.0, 8.0, 16.0])
  log_rates = log2(rates)                        # [-1, 0, 1, 2, 3, 4]
  mod_energies = stack([mod_0_5Hz, ..., mod_16Hz])  # (B, T, 6)
  centroid = (log_rates * mod_energies).sum(dim=-1) / mod_energies.sum(dim=-1).clamp(min=1e-8)
  centroid_norm = (centroid - (-1)) / (4 - (-1))   # [-1, 4] → [0, 1]
  ```
- **Input**: [114:119] modulation energies
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: min-max (log2 domain: [-1, 4] → [0,1])
- **Parametreler**: rates = [0.5, 1, 2, 4, 8, 16] Hz
- **Bağımlılıklar**: [114:119]
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Weighted mean computation
- **Psikoakustik kaynak**: Modulation spectral centroid

#### [121] modulation_bandwidth
- **Tanım**: Modulation spectrum'un genişliği — modulation hız çeşitliliği
- **Formül**:
  ```
  mod_std = weighted_std(log_rates, mod_energies)
  bandwidth = mod_std / max_possible_std          # normalize [0,1]
  ```
- **Input**: [114:119] modulation energies
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /max_std (max_std ≈ 2.5 for log2 range [-1,4])
- **Parametreler**: max_std = 2.5
- **Bağımlılıklar**: [114:119], [120] centroid
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Weighted std from centroid
- **Psikoakustik kaynak**: Modulation diversity measure

#### [122] sharpness_zwicker
- **Tanım**: DIN 45692 Zwicker sharpness — algılanan keskinlik
- **Formül**:
  ```
  # Mel → Bark rebinning (pre-computed 128×24 matrix)
  bark_energy = bark_matrix.T @ exp(mel)          # (B, 24, T)
  # Zwicker weighting function g(z):
  # g(z) = 1.0  for z ≤ 15 Bark
  # g(z) = 0.066 * exp(0.171 * z)  for z > 15 Bark
  z = torch.arange(1, 25)                         # Bark band centers
  g = where(z <= 15, 1.0, 0.066 * exp(0.171 * z))

  S = 0.11 * (bark_energy * g * z).sum(dim=1) / bark_energy.sum(dim=1).clamp(min=1e-8)
  sharpness = S / 4.0                             # tipik max ~4 acum → [0,1]
  sharpness = sharpness.clamp(0, 1)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: /4.0 acum + clamp
- **Parametreler**: Bark matrix (128×24, pre-computed), g(z) weighting, scale=0.11
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: ~0.3 ms/frame (matmul 128×24 + weighted sum)
- **PyTorch notu**: `register_buffer` for bark_matrix and g_weights; `torch.matmul`
- **Psikoakustik kaynak**: DIN 45692; Zwicker & Fastl 1999

#### [123] fluctuation_strength
- **Tanım**: ~4 Hz temporal modulation algısı — Zwicker/Fastl fluctuation model
- **Formül**:
  ```
  # Mel envelope'unun 4 Hz civarındaki modulation enerjisi
  # Bandpass filter: 2-6 Hz (centered at 4 Hz)
  # Approximation: modulation_4Hz[117] * weighting
  fluctuation = modulation_4Hz[117]               # 4 Hz modulation energy
  # Zwicker formula: F = 0.008 * Σ ΔL / (Δf_mod/4 + 4/Δf_mod)
  # Simplified: ~proportional to 4Hz modulation
  fluctuation = fluctuation  # already [0,1] from modulation norm
  ```
- **Input**: [117] modulation_4Hz
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: [117] zaten [0,1]
- **Parametreler**: Yok (modulation'dan türetilmiş)
- **Bağımlılıklar**: [117] modulation_4Hz
- **Tahmini maliyet**: <0.01 ms/frame (zaten hesaplanmış)
- **PyTorch notu**: Direct reference
- **Psikoakustik kaynak**: Zwicker & Fastl 1999 fluctuation strength; peak at 4 Hz

#### [124] loudness_a_weighted
- **Tanım**: A-ağırlıklı toplam enerji — frekans-düzeltilmiş algısal gürüklük
- **Formül**:
  ```
  # A-weighting curve at mel band center frequencies (pre-computed)
  # A(f) = 12194^2 * f^4 / ((f^2+20.6^2) * sqrt((f^2+107.7^2)*(f^2+737.9^2)) * (f^2+12194^2))
  A_weights = pre_computed_A_weighting           # (128,) dB offset per mel bin

  mel_linear = exp(mel)                          # log → linear
  weighted = mel_linear * A_weights_linear       # apply A-weighting
  loudness_A = weighted.sum(dim=1)               # total weighted energy
  loudness_A_norm = loudness_A / loudness_A.max().clamp(min=1e-8)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: max-normalization (batch-level)
- **Parametreler**: A_weights (128,) pre-computed `register_buffer`
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `register_buffer("a_weights", ...)`, element-wise multiply → sum
- **Psikoakustik kaynak**: ISO 226:2003 equal-loudness contours

#### [125] alpha_ratio
- **Tanım**: Düşük band (0-1kHz) / yüksek band (1-5kHz) enerji oranı
- **Formül**:
  ```
  # Mel bin sınırları (yaklaşık): 0-1kHz ≈ bins 0-40, 1-5kHz ≈ bins 40-100
  low = mel[:, :40, :].sum(dim=1)
  high = mel[:, 40:100, :].sum(dim=1)
  alpha = low / high.clamp(min=1e-8)
  alpha_norm = alpha / (alpha + 1)               # ratio → [0,1] via x/(x+1)
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: `x / (x + 1)` — ratio'yu [0,1]'e sıkıştırır
- **Parametreler**: low_cutoff ≈ bin 40 (1kHz), high_cutoff ≈ bin 100 (5kHz)
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Slice + sum + ratio
- **Psikoakustik kaynak**: eGeMAPS (Eyben 2015) — voice/instrument quality balance

#### [126] hammarberg_index
- **Tanım**: 0-2kHz tepe / 2-5kHz tepe enerji oranı
- **Formül**:
  ```
  peak_low = mel[:, :55, :].max(dim=1).values    # 0-2kHz
  peak_high = mel[:, 55:100, :].max(dim=1).values  # 2-5kHz
  hammarberg = peak_low - peak_high               # log domain'de fark = ratio
  hammarberg_norm = sigmoid(hammarberg / 5.0)     # normalize [0,1]
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: sigmoid (tipik aralık [-10, 10] dB → sigmoid/5 ile [0,1])
- **Parametreler**: low_band ≈ bins 0-55 (2kHz), high_band ≈ bins 55-100 (5kHz)
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: `torch.max` per band → diff → `torch.sigmoid`
- **Psikoakustik kaynak**: eGeMAPS — spectral tilt measure

#### [127] spectral_slope_0_500
- **Tanım**: 0-500 Hz aralığındaki mel band'lerinin lineer regresyon eğimi
- **Formül**:
  ```
  # 0-500 Hz ≈ mel bins 0-18 (yaklaşık)
  x = torch.arange(18).float()                   # bin indeksleri
  y = mel[:, :18, :]                             # (B, 18, T)
  # Linear regression: slope = cov(x,y) / var(x)
  x_mean = x.mean()
  y_mean = y.mean(dim=1, keepdim=True)
  slope = ((x - x_mean).unsqueeze(0) * (y - y_mean)).sum(dim=1) / ((x - x_mean)**2).sum()
  slope_norm = sigmoid(slope * 10)               # normalize [0,1]
  ```
- **Input**: mel (B, 128, T)
- **Output**: (B, T, 1), [0,1]
- **Normalizasyon**: sigmoid (gain=10)
- **Parametreler**: band = bins 0-18 (0-500 Hz)
- **Bağımlılıklar**: Yok
- **Tahmini maliyet**: <0.1 ms/frame
- **PyTorch notu**: Linear regression via covariance/variance
- **Psikoakustik kaynak**: eGeMAPS — low-frequency spectral shape

---

## Bölüm 3: Hesaplama Pipeline'ı

### 3.1 Dependency DAG — Grup Seviyesi

```
Girdi: mel (B, 128, T) @ 172.27 Hz frame rate

STAGE 1 — Mel-only groups (parallel):
┌─────────────────────────────────────────────────────────────┐
│  A:Consonance(7D)   B:Energy(5D)   C:Timbre(9D)           │
│  D:Change(4D)       F:Pitch(16D)   J:TimbreExt(20D)       │
│  K:Modulation(14D)                                          │
│  [Tümü sadece mel input'a bağlı — tam paralel]             │
└─────────────────────────────────────────────────────────────┘
         │ A,B,C,D çıktıları    │ F chroma    │ B[11] onset
         ▼                       ▼              ▼
STAGE 2 — Dependent groups (parallel):
┌─────────────────────────────────────────────────────────────┐
│  E:Interactions(24D)    H:Harmony(12D)    G:Rhythm(10D)    │
│  [E←A,B,C,D]           [H←F chroma]      [G←B[11]]        │
│  [Phase 6'da gerçek     [tonnetz, key     [autocorrelation, │
│   A-D referansı]         from chroma]      syncopation]     │
└─────────────────────────────────────────────────────────────┘
         │ F chroma + G onset + H key
         ▼
STAGE 3 — Information group:
┌─────────────────────────────────────────────────────────────┐
│  I:Information(7D)                                          │
│  [I←F chroma (melodic/harmonic entropy)]                   │
│  [I←G onset (rhythmic IC)]                                  │
│  [I←H key (tonal ambiguity)]                               │
│  [I←mel (spectral surprise, info rate, pred. entropy)]     │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
CONCAT: torch.cat([A,B,C,D,E,F,G,H,I,J,K], dim=-1) → (B, T, 128)
```

### 3.2 Dependency DAG — Feature Seviyesi (kritik bağımlılıklar)

```
mel ──┬── A[0:7] ──────────────────────────────────────────── E[25:49]
      ├── B[7:12] ─┬── B[11] onset_strength ──── G[65:75] ── I[89]
      │             └── E[25:49]                              │
      ├── C[12:21] ──────────────────────────────── E[25:49]  │
      ├── D[21:25] ──────────────────────────────── E[25:49]  │
      ├── F[49:65] ─┬── chroma[49:61] ──┬── H[75:87] ─────── I[87,88,93]
      │             │                    └── I[87,88]          │
      │             ├── pitch_height[61]                       │
      │             ├── PC_entropy[62]                         │
      │             ├── pitch_salience[63]                     │
      │             └── inharmonicity[64]                      │
      ├── J[94:114] (independent)                              │
      └── K[114:128] ─── mod_4Hz[117] → fluctuation[123]      │
                                                               │
                    I[87:94] ← F chroma + G onset + H key + mel
```

### 3.3 GPU Parallelization Stratejisi

| Stage | Gruplar | Max Latency | Paralel Streams |
|-------|---------|-------------|-----------------|
| 1 | A, B, C, D, F, J, K | max(K) = ~3.0ms* | 7 CUDA streams |
| 2 | E, G, H | max(H) = ~1.0ms | 3 CUDA streams |
| 3 | I | ~0.5ms | 1 CUDA stream |
| Concat | torch.cat | <0.1ms | 1 |
| **Toplam** | | **~4.5ms** | |

*K grubu amortized: tam FFT her 86 frame'de bir. Ortalama K maliyeti ~0.5ms/frame.
**Amortized toplam: ~2.5ms/frame** → **2.3× RT headroom** (5.8ms budget)

### 3.4 Frame-Level Latency Detayı

| Grup | Boyut | Hesaplama Türü | ms/frame | Notlar |
|------|:-----:|----------------|:--------:|-------|
| A | 7D | mel statistics | 0.1 | 7 basit mel istatistiği |
| B | 5D | mel statistics + diff | 0.1 | RMS, diff, sigmoid |
| C | 9D | mel statistics | 0.1 | Band ratios, centroid, autocorr |
| D | 4D | mel statistics + diff | 0.1 | Flux, entropy, flatness |
| E | 24D | cross-product | 0.1 | 24 element-wise multiply |
| F | 16D | matmul + statistics | 1.0 | 128×12 chroma matmul + peak analysis |
| G | 10D | autocorrelation + onset | 0.8 | FFT autocorr + peak detect + IOI |
| H | 12D | correlation + projection | 1.0 | 24 key corr + 6D tonnetz + chroma diff |
| I | 7D | KL + entropy + running stats | 0.8 | Running statistics + KL divergence |
| J | 20D | DCT + band sort | 0.5 | 128×13 DCT + 7-band contrast |
| K | 14D | sliding FFT + psychoacoustic | 0.5* | *amortized; per-band temporal FFT |
| **Toplam** | **128D** | | **~5.2ms** | Sequential sum (not parallel) |
| **Parallel** | | | **~2.5ms** | 3-stage parallel execution |

### 3.5 Warm-up Davranışı

| Feature/Grup | Warm-up Süresi | Davranış |
|-------------|:-------------:|----------|
| K modulation [114:121] | 344 frame (2.0s) | İlk 344 frame sıfır çıktı; sonra geçerli |
| I entropy [87,88,92] | 344 frame (2.0s) | `confidence = min(1.0, t/344)` lineer ramp |
| I spectral_surprise [90] | 344 frame (2.0s) | Running average warm-up |
| G tempo [65:67] | 344 frame (2.0s) | Autocorrelation penceresi |
| G syncopation [68] | 688 frame (4.0s) | Tempo + metrical grid stabilizasyon |
| Diğer tüm feature'lar | 0 (anında) | Frame-level hesaplama, warm-up yok |

**Warm-up stratejisi**: İlk 344 frame boyunca (2.0s) warm-up gerektiren feature'lar kademeli olarak güvenilir hale gelir. C³ modelleri bu geçiş döneminde BEP/ASA mekanizmalarıyla baş edebilir (H³ temporal demand).

---

## Bölüm 4: Interaction Redesign (E Grubu)

### 4.1 Mevcut E Grubu Eleştirisi

**Yapı**: 24D = 3 × 8D cross-product blokları

| Blok | İndeks | Grup Çifti | Operasyon | Sorun |
|------|:------:|------------|-----------|-------|
| x_l0l5 | [25:33] | B:Energy × A:Consonance | element-wise product (8D) | Proxy mismatch: roughness_proxy ≠ A[0] |
| x_l4l5 | [33:41] | D:Change × A:Consonance | element-wise product (8D) | Proxy mismatch: helmholtz_proxy ≠ A[2] |
| x_l5l7 | [41:49] | A:Consonance × C:Timbre | element-wise product (8D) | Proxy kullanıyor, gerçek A çıktısı değil |

**Temel sorunlar**:
1. **Proxy mismatch**: E grubu mel'den bağımsız proxy'ler hesaplıyor, A-D çıktılarını referans etmiyor
2. **Kapsam kısıtlılığı**: Sadece 3 grup çifti (A×B, D×A, A×C). F-K grupları hiç temsil edilmiyor
3. **Mekanik çarpım**: `[0,1] × [0,1]` ürünü 0'a doğru bias'lı — düşük sinyaller kaybolur
4. **Duplikasyon propagasyonu**: Base feature redundancy (A[3]≡C[12]) interaction'da da çoğalır

### 4.2 Phase 6 Aşama 1: Proxy Düzeltme (24D korunur)

**Değişiklik**: E grubu proxy'leri kaldırılır, gerçek A-D çıktıları referans edilir.

```python
# MEVCUT (v1 — proxy-based):
roughness_proxy = mel.var(dim=1)  # ≠ A[0]
helmholtz_proxy = mel.max(dim=1) / mel.sum(dim=1)  # ≠ A[2], = C[14]

# HEDEF (Phase 6 — gerçek referans):
# E grubu compute() metoduna A, B, C, D çıktıları parametre olarak geçirilir
def compute(self, mel, group_outputs):
    A = group_outputs['consonance']  # (B, T, 7)
    B = group_outputs['energy']       # (B, T, 5)
    C = group_outputs['timbre']       # (B, T, 9)
    D = group_outputs['change']       # (B, T, 4)

    # x_l0l5: B[:4] × A[:2] = 4×2 = 8D (element-wise outer product)
    x_energy_consonance = outer_product_select(B[:, :, :4], A[:, :, :2])

    # x_l4l5: D[:4] × A[:2] = 4×2 = 8D
    x_change_consonance = outer_product_select(D, A[:, :, :2])

    # x_l5l7: A[:4] × C[:2] = 4×2 = 8D
    x_consonance_timbre = outer_product_select(A[:, :, :4], C[:, :, :2])

    return cat([x_energy_consonance, x_change_consonance, x_consonance_timbre])
```

**Aşama 1 etkisi**: Hesaplama doğruluğu artar ama yapı değişmez. 24D korunur.

### 4.3 Phase 6+ Aşama 2: Genişletilmiş Interaction (ÖNERİ)

**ÖNERİ: R³ v2.1 kapsamında, 128D bütçe dışında.**

Yeni cross-group interaction önerileri (psikoakustik motivasyonlu):

| Çift | Boyut | Operasyon | Psikoakustik Gerekçe |
|------|:-----:|-----------|---------------------|
| F×A: Pitch×Consonance | 4D | chroma_entropy × roughness, pitch_height × harmonicity, salience × fusion, inharmonicity × dissonance | Perde algısı + uyumluluk etkileşimi |
| G×B: Rhythm×Energy | 4D | tempo × amplitude, syncopation × onset_strength, beat_strength × velocity, groove × loudness | Ritmik yapı + enerji etkileşimi (groove'un fiziksel temeli) |
| H×D: Harmony×Change | 4D | key_clarity × spectral_flux, tonal_stability × entropy, harmonic_change × flux, diatonicity × flatness | Harmonik yapı + değişim etkileşimi |
| I×all: Surprise aggregates | 4D | mean(I) × mean(A), mean(I) × mean(B), mean(I) × mean(F), mean(I) × mean(G) | Sürpriz × temel özellik grupları |

**Toplam ek**: 16D → R³ v2.1 = 144D

**Karar**: Bu 16D genişleme Phase 6 deneysel verilerine dayalı olarak kararlaştırılır. Şu an 128D bütçe korunur. E grubu mevcut 24D yapısı Phase 6 Aşama 1'de proxy-fix ile düzeltilir.

### 4.4 Interaction Operasyonu Seçimi

**Mevcut**: Element-wise product (`a * b`)
**Sorun**: Product [0,1]×[0,1] bias → sıfıra yakın değerler

**ÖNERİ — Phase 6 alternatifleri:**

| Operasyon | Formül | Avantaj | Dezavantaj |
|-----------|--------|---------|------------|
| Product | a × b | Basit, "simultaneous presence" | Zero bias |
| Geometric mean | √(a × b) | Daha dengeli | Yine zero bias |
| Harmonic product | 2ab/(a+b) | Zero'ya daha az bias | a=0 veya b=0'da tanımsız |
| Concatenate | [a; b] | Bilgi kaybı yok | Boyut 2× artar |
| Cosine similarity | cos(a, b) | Yön benzerliği | Sadece vektör çiftleri için |

**Seçim**: Phase 6'da element-wise product korunur (basitlik). Ancak geometric mean (`sqrt(a*b)`) alternatif olarak test edilmeli.

---

## Bölüm 5: Kod Değişiklik Planı (Phase 6)

6 hardcoded "49" kısıtı ve çözümleri:

### 5.1 `mi_beta/core/constants.py` — R3_DIM ve Grup Sınırları

**Mevcut kod**:
```python
R3_DIM: int = 49
R3_CONSONANCE: tuple[int, int] = (0, 7)
R3_ENERGY: tuple[int, int] = (7, 12)
R3_TIMBRE: tuple[int, int] = (12, 21)
R3_CHANGE: tuple[int, int] = (21, 25)
R3_INTERACTIONS: tuple[int, int] = (25, 49)
```

**Hedef kod** (Phase 6):
```python
# Backward compatibility: v1 sabitler korunur
R3_DIM_V1: int = 49  # legacy — yeni kod kullanmamalı

# v2: Dinamik boyut (registry'den)
# R3_DIM artık runtime'da R3FeatureRegistry.freeze().total_dim'den gelir
# Ama import-time convenience için default sabit:
R3_DIM: int = 128  # R³ v2 varsayılan; registry ile doğrulanır

# Grup sınırları: registry'den okunmalı, ama legacy uyumluluk için:
R3_CONSONANCE: tuple[int, int] = (0, 7)
R3_ENERGY: tuple[int, int] = (7, 12)
R3_TIMBRE: tuple[int, int] = (12, 21)
R3_CHANGE: tuple[int, int] = (21, 25)
R3_INTERACTIONS: tuple[int, int] = (25, 49)
# Yeni gruplar:
R3_PITCH_CHROMA: tuple[int, int] = (49, 65)
R3_RHYTHM_GROOVE: tuple[int, int] = (65, 75)
R3_HARMONY_TONALITY: tuple[int, int] = (75, 87)
R3_INFORMATION_SURPRISE: tuple[int, int] = (87, 94)
R3_TIMBRE_EXTENDED: tuple[int, int] = (94, 114)
R3_MODULATION_PSYCHOACOUSTIC: tuple[int, int] = (114, 128)
```

**Migration adımları**:
1. `R3_DIM_V1 = 49` ekle (backward compat)
2. `R3_DIM = 128` güncelle
3. 6 yeni grup sınır sabiti ekle
4. Registry.freeze() ile doğrulama assertion ekle

**Test stratejisi**:
- `assert R3_DIM == registry.freeze().total_dim`
- Tüm grup sınırları contiguous ve gap-free olmalı
- `R3_DIM_V1` kullanan legacy kod'un doğru çalıştığını doğrula

### 5.2 `mi_beta/core/dimension_map.py` — Feature Names

**Mevcut kod**:
```python
_R3_FEATURE_NAMES: Tuple[str, ...] = (
    "perfect_fifth_ratio", "euler_gradus", "harmonicity",
    "stumpf_fusion", "sensory_pleasantness", "roughness_total",
    "consonance_mean",
    "velocity_A", "velocity_D", "loudness", "onset_strength",
    "rms_energy",
    # ... 49 element
)
# Validation:
if len(r3_names) != R3_DIM:
    raise ValueError(...)
```

**Hedef kod** (Phase 6):
```python
# Option B: Registry'den dinamik (tercih edilen)
def _get_r3_feature_names() -> Tuple[str, ...]:
    """R³ feature names from registry (128D)."""
    from mi_beta.ear.r3._registry import get_default_registry
    feature_map = get_default_registry().freeze()
    return tuple(feature_map.feature_names)

# Lazy initialization + cache
_R3_FEATURE_NAMES: Optional[Tuple[str, ...]] = None

def get_r3_feature_names() -> Tuple[str, ...]:
    global _R3_FEATURE_NAMES
    if _R3_FEATURE_NAMES is None:
        _R3_FEATURE_NAMES = _get_r3_feature_names()
    return _R3_FEATURE_NAMES

# Legacy uyumluluk:
_R3_FEATURE_NAMES_V1: Tuple[str, ...] = (
    "perfect_fifth_ratio", "euler_gradus", ...  # orijinal 49
)
```

**Migration adımları**:
1. `_R3_FEATURE_NAMES_V1` olarak mevcut tuple'ı koru
2. `get_r3_feature_names()` fonksiyonu ekle (registry-based)
3. `DimensionMap.__init__` validasyonunu güncelle: `len(names) == R3_DIM`
4. Tüm `_R3_FEATURE_NAMES` referanslarını `get_r3_feature_names()` ile değiştir

**Test stratejisi**:
- `assert len(get_r3_feature_names()) == 128`
- `assert get_r3_feature_names()[:49] == _R3_FEATURE_NAMES_V1` (v1 uyumluluk)
- Her feature name unique olmalı
- Tüm names snake_case olmalı

### 5.3 `mi_beta/contracts/feature_spec.py` — Index Validation

**Mevcut kod**:
```python
@dataclass
class R3FeatureSpec:
    index: int
    name: str
    # ...
    def __post_init__(self) -> None:
        if not (0 <= self.index < 49):
            raise ValueError(f"R3 feature index must be 0-48, got {self.index}")
```

**Hedef kod** (Phase 6):
```python
@dataclass
class R3FeatureSpec:
    index: int
    name: str
    # ...
    def __post_init__(self) -> None:
        from mi_beta.core.constants import R3_DIM
        if not (0 <= self.index < R3_DIM):
            raise ValueError(
                f"R3 feature index must be 0-{R3_DIM-1}, got {self.index}"
            )
```

**Migration adımları**:
1. `49` → `R3_DIM` import ile değiştir
2. Hata mesajını dinamik yap

**Test stratejisi**:
- `R3FeatureSpec(index=0)` → OK
- `R3FeatureSpec(index=127)` → OK (v2)
- `R3FeatureSpec(index=128)` → ValueError
- `R3FeatureSpec(index=-1)` → ValueError

### 5.4 `mi_beta/contracts/base_spectral_group.py` — Docstrings

**Mevcut kod**:
```python
class BaseSpectralGroup(ABC):
    """Base class for R³ spectral groups.

    Each group computes a subset of the 49-D R³ vector.
    ...
    INDEX_RANGE: Position in the 49-D vector.
    """
```

**Hedef kod** (Phase 6):
```python
class BaseSpectralGroup(ABC):
    """Base class for R³ spectral groups.

    Each group computes a subset of the R³ feature vector.
    Total dimensionality is determined by R3FeatureRegistry.freeze().
    ...
    INDEX_RANGE: Auto-assigned by R3FeatureRegistry.freeze().
    """
```

**Migration adımları**:
1. "49-D" → "R³ feature vector" (boyut belirtme)
2. "in the 49-D vector" → "Auto-assigned by R3FeatureRegistry.freeze()"
3. INDEX_RANGE docstring güncelleme

**Test stratejisi**: Docstring doğruluğu — grep for "49-D" veya "49" referansları

### 5.5 `mi_beta/ear/r3/__init__.py` — R3Extractor

**Mevcut kod** (zaten dinamik):
```python
class R3Extractor:
    # Auto-discovers groups from subdirectories:
    # psychoacoustic → dsp → cross_domain → extensions
    def extract(self, mel):
        parts = []
        for group in self._groups:
            parts.append(group.compute(mel))
        return torch.cat(parts, dim=-1)  # (B, T, total_dim)
```

**Hedef kod** (Phase 6 — dependency-aware):
```python
class R3Extractor:
    # Scan order: psychoacoustic → dsp → cross_domain → extensions → new_groups
    STAGE_ORDER = {
        1: ['consonance', 'energy', 'timbre', 'change',
            'pitch_chroma', 'timbre_extended', 'modulation_psychoacoustic'],
        2: ['interactions', 'rhythm_groove', 'harmony_tonality'],
        3: ['information_surprise'],
    }

    def extract(self, mel):
        outputs = {}
        for stage in sorted(self.STAGE_ORDER):
            stage_groups = [g for g in self._groups
                          if g.GROUP_NAME in self.STAGE_ORDER[stage]]
            for group in stage_groups:
                if hasattr(group, 'compute_with_deps'):
                    result = group.compute_with_deps(mel, outputs)
                else:
                    result = group.compute(mel)
                outputs[group.GROUP_NAME] = result

        # Concat in index order
        ordered = [outputs[g.GROUP_NAME] for g in self._groups]
        return torch.cat(ordered, dim=-1)  # (B, T, 128)
```

**Migration adımları**:
1. `STAGE_ORDER` dict ekle
2. `extract` metodunu stage-aware yap
3. `compute_with_deps(mel, outputs)` opsiyonel metod ekle (dependency injection)
4. Mevcut `compute(mel)` backward compat olarak çalışmaya devam eder
5. Yeni gruplar `extensions/` altına `.py` dosyaları olarak eklenir

**Test stratejisi**:
- `extractor.extract(mel).shape == (B, T, 128)`
- Stage sıralamasının doğruluğu: H grubunun F chroma'ya erişebildiğini doğrula
- Mevcut A-E gruplarının v1 davranışını koruduğunu doğrula

### 5.6 `mi_beta/ear/r3/_registry.py` — R3FeatureRegistry

**Mevcut kod** (zaten dinamik):
```python
class R3FeatureRegistry:
    def freeze(self) -> R3FeatureMap:
        offset = 0
        for group in self._groups:
            dim = group.OUTPUT_DIM
            group.INDEX_RANGE = (offset, offset + dim)
            offset += dim
        return R3FeatureMap(total_dim=offset, groups=self._groups)
```

**Hedef kod** (Phase 6 — validation ekle):
```python
class R3FeatureRegistry:
    def freeze(self) -> R3FeatureMap:
        offset = 0
        for group in self._groups:
            dim = group.OUTPUT_DIM
            group.INDEX_RANGE = (offset, offset + dim)
            offset += dim

        # v2 validation
        feature_map = R3FeatureMap(total_dim=offset, groups=self._groups)
        assert offset == R3_DIM, f"Registry total_dim={offset} != R3_DIM={R3_DIM}"

        # Feature name uniqueness check
        all_names = feature_map.feature_names
        assert len(all_names) == len(set(all_names)), "Duplicate feature names"

        return feature_map
```

**Migration adımları**:
1. `freeze()` sonuna validation assertion ekle
2. Feature name uniqueness check ekle
3. `R3FeatureMap.feature_names` property'si ekle (tüm grupların feature_names'ini birleştirir)

**Test stratejisi**:
- `registry.freeze().total_dim == 128`
- Tüm feature names unique
- Grup sınırları contiguous (gap yok, overlap yok)

### 5.7 Özet: 6 Kısıt Çözüm Tablosu

| # | Dosya | Mevcut Kısıt | Çözüm | Backward Compat |
|---|-------|-------------|-------|-----------------|
| 1 | constants.py | `R3_DIM = 49` | `R3_DIM = 128` + `R3_DIM_V1 = 49` | V1 sabiti korunur |
| 2 | dimension_map.py | 49-element hardcoded tuple | Registry-based `get_r3_feature_names()` | V1 tuple korunur |
| 3 | feature_spec.py | `assert index < 49` | `assert index < R3_DIM` | Otomatik |
| 4 | base_spectral_group.py | "49-D" docstrings | "R³ feature vector" | Sadece doc |
| 5 | __init__.py (R3Extractor) | Sıra-bağımsız concat | Stage-ordered `extract()` | Mevcut API korunur |
| 6 | _registry.py | Validation yok | `assert total_dim == R3_DIM` | Additive |

---

## Bölüm 6: BaseSpectralGroup Şablonları (F-K)

### 6.1 Group F: PitchChromaGroup

```python
import math
import torch
from torch import Tensor
from mi_beta.contracts.base_spectral_group import BaseSpectralGroup


class PitchChromaGroup(BaseSpectralGroup):
    """Group F: Pitch & Chroma [49:65] — 16D

    Mel spectrogram'dan pitch class profili, pitch height,
    pitch class entropy, pitch salience ve inharmonicity hesaplar.
    Chroma çıktısı H ve I grupları tarafından kullanılır.
    """

    GROUP_NAME = "pitch_chroma"
    DOMAIN = "pitch"
    OUTPUT_DIM = 16
    INDEX_RANGE = (0, 0)  # Auto-assigned by registry.freeze()

    def __init__(self):
        super().__init__()
        # Pre-compute mel-to-chroma mapping matrix (128 × 12)
        M = self._build_chroma_matrix(n_mels=128, sr=44100)
        self.register_buffer("mel_to_chroma", M)

        # Pre-compute log2 center frequencies for pitch_height
        freqs = self._mel_center_frequencies(n_mels=128, sr=44100)
        log2_freqs = torch.log2(freqs.clamp(min=20.0))
        self.register_buffer("log2_freqs", log2_freqs)

        # Normalization constants
        self.log2_fmin = math.log2(20.0)
        self.log2_fmax = math.log2(22050.0)

    def _build_chroma_matrix(self, n_mels: int, sr: int) -> Tensor:
        """128×12 Gaussian soft-assignment chroma mapping matrix."""
        freqs = self._mel_center_frequencies(n_mels, sr)
        midi = 69 + 12 * torch.log2(freqs.clamp(min=20.0) / 440.0)
        M = torch.zeros(n_mels, 12)
        sigma = 0.5  # semitone Gaussian width
        for c in range(12):
            dist = (midi % 12 - c + 6) % 12 - 6  # circular distance
            M[:, c] = torch.exp(-0.5 * dist ** 2 / sigma ** 2)
        # Zero out bins below 20 Hz (unreliable)
        M[freqs < 20.0] = 0.0
        return M

    def _mel_center_frequencies(self, n_mels: int, sr: int) -> Tensor:
        """Compute center frequencies for each mel bin."""
        fmin, fmax = 0.0, sr / 2.0
        mel_min = 2595 * math.log10(1 + fmin / 700)
        mel_max = 2595 * math.log10(1 + fmax / 700)
        mels = torch.linspace(mel_min, mel_max, n_mels)
        return 700 * (10 ** (mels / 2595) - 1)

    @property
    def feature_names(self) -> list[str]:
        return [
            "chroma_C", "chroma_Db", "chroma_D", "chroma_Eb",
            "chroma_E", "chroma_F", "chroma_Gb", "chroma_G",
            "chroma_Ab", "chroma_A", "chroma_Bb", "chroma_B",
            "pitch_height", "pitch_class_entropy",
            "pitch_salience", "inharmonicity_index",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """mel: (B, 128, T) → (B, T, 16)"""
        B, N, T = mel.shape

        # Chroma (12D)
        mel_linear = mel.exp()  # log-mel → linear power
        chroma = torch.matmul(
            self.mel_to_chroma.T, mel_linear
        )  # (B, 12, T)
        chroma = chroma / chroma.sum(dim=1, keepdim=True).clamp(min=1e-8)
        chroma = chroma.permute(0, 2, 1)  # (B, T, 12)

        # Pitch height (1D)
        weights = mel_linear.permute(0, 2, 1)  # (B, T, 128)
        ph = (self.log2_freqs * weights).sum(dim=-1) / weights.sum(dim=-1).clamp(min=1e-8)
        ph = (ph - self.log2_fmin) / (self.log2_fmax - self.log2_fmin)
        ph = ph.clamp(0, 1).unsqueeze(-1)  # (B, T, 1)

        # Pitch class entropy (1D)
        pce = -(chroma * chroma.clamp(min=1e-8).log()).sum(dim=-1) / math.log(12)
        pce = pce.clamp(0, 1).unsqueeze(-1)  # (B, T, 1)

        # Pitch salience (1D)
        peak_e = mel.max(dim=1).values  # (B, T)
        noise_f = mel.median(dim=1).values  # (B, T)
        ps = (peak_e - noise_f) / (peak_e + noise_f + 1e-8)
        ps = ps.clamp(0, 1).unsqueeze(-1)  # (B, T, 1)

        # Inharmonicity index (1D)
        inh = self._compute_inharmonicity(mel_linear)  # (B, T, 1)

        return torch.cat([chroma, ph, pce, ps, inh], dim=-1)  # (B, T, 16)

    def _compute_inharmonicity(self, mel_linear: Tensor) -> Tensor:
        """Harmonic template matching based inharmonicity."""
        B, N, T = mel_linear.shape
        f0_bin = mel_linear.argmax(dim=1)  # (B, T)
        # Simplified: use peak dominance ratio as proxy
        peak_val = mel_linear.max(dim=1).values
        total_val = mel_linear.sum(dim=1)
        # High peak ratio → harmonic → low inharmonicity
        inh = 1.0 - (peak_val / total_val.clamp(min=1e-8))
        return inh.clamp(0, 1).unsqueeze(-1)  # (B, T, 1)
```

### 6.2 Group G: RhythmGrooveGroup

```python
class RhythmGrooveGroup(BaseSpectralGroup):
    """Group G: Rhythm & Groove [65:75] — 10D

    Onset autocorrelation'dan tempo, beat, syncopation,
    groove ve ritmik istatistikler hesaplar.
    B[11] onset_strength'e bağlıdır.
    """

    GROUP_NAME = "rhythm_groove"
    DOMAIN = "rhythm"
    OUTPUT_DIM = 10
    INDEX_RANGE = (0, 0)

    FRAME_RATE = 172.27
    LAG_MIN = 34    # 300 BPM
    LAG_MAX = 344   # 30 BPM
    PEAK_THRESHOLD = 0.3

    @property
    def feature_names(self) -> list[str]:
        return [
            "tempo_estimate", "beat_strength", "pulse_clarity",
            "syncopation_index", "metricality_index", "isochrony_nPVI",
            "groove_index", "event_density", "tempo_stability",
            "rhythmic_regularity",
        ]

    def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
        """mel: (B, 128, T), group_outputs: {'energy': (B, T, 5)} → (B, T, 10)"""
        B, N, T = mel.shape
        onset = group_outputs['energy'][:, :, 4]  # B[11] = energy index 4

        # Autocorrelation
        R = self._autocorrelation(onset)           # (B, T_autocorr)

        # Tempo, beat, pulse
        tempo_norm, tempo_lag, beat_str, pulse_clar = self._tempo_features(R)

        # Syncopation (simplified LHL)
        sync = self._syncopation(onset, tempo_lag)

        # Metricality
        metric = self._metricality(R, tempo_lag)

        # IOI-based features
        nPVI = self._isochrony(onset, tempo_lag)
        regularity = self._rhythmic_regularity(onset)

        # Groove composite
        bass_energy = mel[:, :16, :].mean(dim=1)
        bass_norm = bass_energy / bass_energy.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        groove = sync * bass_norm * pulse_clar

        # Event density
        peaks = (onset > self.PEAK_THRESHOLD).float()
        density = torch.nn.functional.avg_pool1d(
            peaks.unsqueeze(1), kernel_size=172, stride=1, padding=86
        ).squeeze(1)
        density = (density * self.FRAME_RATE / 20.0).clamp(0, 1)

        # Tempo stability
        stability = self._tempo_stability(onset)

        features = torch.stack([
            tempo_norm, beat_str, pulse_clar, sync, metric,
            nPVI, groove, density, stability, regularity
        ], dim=-1)  # (B, T, 10)

        return features.clamp(0, 1)

    # [Private methods: _autocorrelation, _tempo_features, _syncopation,
    #  _metricality, _isochrony, _rhythmic_regularity, _tempo_stability]
    # (detailed implementations per Bölüm 2 formülleri)
```

### 6.3 Group H: HarmonyTonalityGroup

```python
class HarmonyTonalityGroup(BaseSpectralGroup):
    """Group H: Harmony & Tonality [75:87] — 12D

    Chroma'dan key clarity, tonnetz, voice-leading distance,
    harmonic change, tonal stability, diatonicity, syntactic irregularity.
    F grubunun chroma çıktısına bağlıdır.
    """

    GROUP_NAME = "harmony_tonality"
    DOMAIN = "harmony"
    OUTPUT_DIM = 12
    INDEX_RANGE = (0, 0)

    def __init__(self):
        super().__init__()
        # Krumhansl-Kessler key profiles (24 × 12)
        self.register_buffer("key_profiles", self._build_key_profiles())
        # Tonnetz projection matrix (12 × 6)
        self.register_buffer("tonnetz_matrix", self._build_tonnetz_matrix())

    def _build_key_profiles(self) -> Tensor:
        major = [6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]
        minor = [6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]
        profiles = []
        for shift in range(12):
            profiles.append(torch.roll(torch.tensor(major), shift))
            profiles.append(torch.roll(torch.tensor(minor), shift))
        return torch.stack(profiles)  # (24, 12)

    def _build_tonnetz_matrix(self) -> Tensor:
        """Harte 2006 tonnetz projection matrix."""
        k = torch.arange(12).float()
        M = torch.zeros(12, 6)
        M[:, 0] = torch.sin(k * 7 * math.pi / 6)  # fifth_x
        M[:, 1] = torch.cos(k * 7 * math.pi / 6)  # fifth_y
        M[:, 2] = torch.sin(k * 3 * math.pi / 6)  # minor_x
        M[:, 3] = torch.cos(k * 3 * math.pi / 6)  # minor_y
        M[:, 4] = torch.sin(k * 4 * math.pi / 6)  # major_x
        M[:, 5] = torch.cos(k * 4 * math.pi / 6)  # major_y
        return M

    @property
    def feature_names(self) -> list[str]:
        return [
            "key_clarity",
            "tonnetz_fifth_x", "tonnetz_fifth_y",
            "tonnetz_minor_x", "tonnetz_minor_y",
            "tonnetz_major_x", "tonnetz_major_y",
            "voice_leading_distance", "harmonic_change",
            "tonal_stability", "diatonicity", "syntactic_irregularity",
        ]

    def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
        """Requires F group chroma output."""
        chroma = group_outputs['pitch_chroma'][:, :, :12]  # (B, T, 12)
        B, T, _ = chroma.shape

        # Key clarity
        corrs = torch.matmul(chroma, self.key_profiles.T)  # (B, T, 24)
        key_clarity = corrs.max(dim=-1).values
        key_clarity = ((key_clarity - 0.3) / 0.65).clamp(0, 1).unsqueeze(-1)

        # Tonnetz (6D) → normalize to [0,1]
        tonnetz = torch.matmul(chroma, self.tonnetz_matrix)  # (B, T, 6)
        tonnetz = (tonnetz + 1) / 2  # [-1,1] → [0,1]

        # Voice-leading distance
        vl = (chroma[:, 1:] - chroma[:, :-1]).abs().sum(dim=-1) / 2.0
        vl = torch.cat([vl[:, :1], vl], dim=1).clamp(0, 1).unsqueeze(-1)

        # Harmonic change
        sim = torch.nn.functional.cosine_similarity(
            chroma[:, 1:], chroma[:, :-1], dim=-1
        )
        hc = 1 - sim
        hc = torch.cat([hc[:, :1], hc], dim=1).clamp(0, 1).unsqueeze(-1)

        # Tonal stability
        hc_smooth = torch.nn.functional.avg_pool1d(
            hc.squeeze(-1).unsqueeze(1), kernel_size=172, stride=1, padding=86
        ).squeeze(1)
        ts = (key_clarity.squeeze(-1) * (1 - hc_smooth)).clamp(0, 1).unsqueeze(-1)

        # Diatonicity
        active_pcs = (chroma > 0.05).float().sum(dim=-1)
        diat = (1 - (active_pcs - 7) / 5).clamp(0, 1).unsqueeze(-1)

        # Syntactic irregularity
        best_key = corrs.argmax(dim=-1)  # (B, T)
        # Gather best template for each frame
        best_template = self.key_profiles[best_key]  # (B, T, 12)
        tp = best_template / best_template.sum(dim=-1, keepdim=True).clamp(min=1e-8)
        cp = chroma.clamp(min=1e-8)
        kl = (cp * (cp.log() - tp.clamp(min=1e-8).log())).sum(dim=-1)
        irreg = (1 - (-kl).exp()).clamp(0, 1).unsqueeze(-1)

        return torch.cat([key_clarity, tonnetz, vl, hc, ts, diat, irreg], dim=-1)
```

### 6.4 Group I: InformationSurpriseGroup

```python
class InformationSurpriseGroup(BaseSpectralGroup):
    """Group I: Information & Surprise [87:94] — 7D

    Running statistics ile entropy, KL divergence, information content.
    F chroma, G onset ve mel'e bağlıdır.
    """

    GROUP_NAME = "information_surprise"
    DOMAIN = "information"
    OUTPUT_DIM = 7
    INDEX_RANGE = (0, 0)

    TAU = 2.0  # seconds
    FRAME_RATE = 172.27

    def __init__(self):
        super().__init__()
        self.alpha = 1 - math.exp(-1 / (self.TAU * self.FRAME_RATE))
        # Running state buffers (initialized on first call)
        self._mel_avg = None
        self._mel_var = None
        self._chroma_avg = None
        self._transition_counts = None
        self._frame_count = 0

    @property
    def feature_names(self) -> list[str]:
        return [
            "melodic_entropy", "harmonic_entropy",
            "rhythmic_information_content", "spectral_surprise",
            "information_rate", "predictive_entropy", "tonal_ambiguity",
        ]

    def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
        """Requires F chroma, G onset, H key correlations."""
        chroma = group_outputs['pitch_chroma'][:, :, :12]
        # Process frame-by-frame with running statistics
        # (Actual implementation uses vectorized EMA for efficiency)
        # ... (7 features computed per Bölüm 2 specs)
        # Returns (B, T, 7) with warm-up confidence applied
        pass  # Full implementation per Bölüm 2 formülleri
```

### 6.5 Group J: TimbreExtendedGroup

```python
class TimbreExtendedGroup(BaseSpectralGroup):
    """Group J: Timbre Extended [94:114] — 20D

    MFCC (13D) ve spectral contrast (7D).
    Doğrudan mel'den, bağımlılık yok.
    """

    GROUP_NAME = "timbre_extended"
    DOMAIN = "timbre"
    OUTPUT_DIM = 20
    INDEX_RANGE = (0, 0)

    def __init__(self):
        super().__init__()
        # Pre-computed DCT-II matrix (128 × 13) for MFCC
        self.register_buffer("dct_matrix", self._build_dct_matrix(128, 13))
        # MFCC scaling factors (empirical per-coefficient max)
        self.register_buffer("mfcc_scale", torch.tensor(
            [40, 80, 60, 50, 40, 35, 30, 25, 22, 20, 18, 16, 15],
            dtype=torch.float32
        ))
        # Spectral contrast band boundaries (mel bin indices)
        self.contrast_bands = [(0,4), (4,8), (8,16), (16,32),
                               (32,64), (64,96), (96,128)]

    def _build_dct_matrix(self, n_mels: int, n_mfcc: int) -> Tensor:
        """Type-II DCT matrix, excluding DC component."""
        n = torch.arange(n_mels).float()
        k = torch.arange(1, n_mfcc + 1).float()  # skip k=0 (DC)
        D = torch.cos(math.pi * k.unsqueeze(1) * (2 * n + 1) / (2 * n_mels))
        D *= math.sqrt(2.0 / n_mels)
        return D.T  # (128, 13)

    @property
    def feature_names(self) -> list[str]:
        mfcc = [f"mfcc_{i}" for i in range(1, 14)]
        contrast = [f"spectral_contrast_{i}" for i in range(1, 8)]
        return mfcc + contrast

    def compute(self, mel: Tensor) -> Tensor:
        """mel: (B, 128, T) → (B, T, 20)"""
        B, N, T = mel.shape

        # MFCC (13D)
        mfcc = torch.matmul(self.dct_matrix.T, mel)  # (B, 13, T)
        mfcc = mfcc.permute(0, 2, 1)  # (B, T, 13)
        mfcc = (mfcc / self.mfcc_scale + 1) / 2  # normalize to [0,1]
        mfcc = mfcc.clamp(0, 1)

        # Spectral contrast (7D)
        contrasts = []
        for start, end in self.contrast_bands:
            band = mel[:, start:end, :]  # (B, band_width, T)
            sorted_band, _ = band.sort(dim=1)
            n = end - start
            alpha = max(1, round(0.2 * n))
            peak = sorted_band[:, -alpha:, :].mean(dim=1)
            valley = sorted_band[:, :alpha, :].mean(dim=1)
            contrasts.append((peak - valley) / 10.0)  # normalize
        contrast = torch.stack(contrasts, dim=-1)  # (B, T, 7)
        contrast = contrast.clamp(0, 1)

        return torch.cat([mfcc, contrast], dim=-1)  # (B, T, 20)
```

### 6.6 Group K: ModulationPsychoacousticGroup

```python
class ModulationPsychoacousticGroup(BaseSpectralGroup):
    """Group K: Modulation & Psychoacoustic [114:128] — 14D

    Modulation spectrum (6D), modulation stats (2D),
    psychoacoustic features (6D).
    Doğrudan mel'den, bağımlılık yok.
    """

    GROUP_NAME = "modulation_psychoacoustic"
    DOMAIN = "modulation"
    OUTPUT_DIM = 14
    INDEX_RANGE = (0, 0)

    WINDOW_SIZE = 344   # ~2.0s
    HOP_SIZE = 86       # ~0.5s
    FFT_SIZE = 512
    FRAME_RATE = 172.27
    TARGET_RATES = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]

    def __init__(self):
        super().__init__()
        self.register_buffer("hann_window", torch.hann_window(self.WINDOW_SIZE))

        # A-weighting curve (128 mel bins)
        freqs = self._mel_center_frequencies(128, 44100)
        self.register_buffer("a_weights", self._a_weighting(freqs))

        # Bark rebinning matrix (128 × 24)
        self.register_buffer("bark_matrix", self._build_bark_matrix(128, 44100))

        # Zwicker sharpness weighting
        z = torch.arange(1, 25).float()
        g = torch.where(z <= 15, torch.ones_like(z),
                       0.066 * torch.exp(0.171 * z))
        self.register_buffer("zwicker_g", g)
        self.register_buffer("bark_z", z)

        # Target FFT bins
        freq_res = self.FRAME_RATE / self.FFT_SIZE
        self.target_bins = [round(r / freq_res) for r in self.TARGET_RATES]

    @property
    def feature_names(self) -> list[str]:
        return [
            "modulation_0_5Hz", "modulation_1Hz", "modulation_2Hz",
            "modulation_4Hz", "modulation_8Hz", "modulation_16Hz",
            "modulation_centroid", "modulation_bandwidth",
            "sharpness_zwicker", "fluctuation_strength",
            "loudness_a_weighted", "alpha_ratio",
            "hammarberg_index", "spectral_slope_0_500",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """mel: (B, 128, T) → (B, T, 14)"""
        B, N, T = mel.shape
        mel_linear = mel.exp()

        # Modulation spectrum (6D + 2D stats)
        mod_features = self._modulation_spectrum(mel_linear)  # (B, T, 8)

        # Sharpness Zwicker (1D)
        sharpness = self._sharpness_zwicker(mel_linear)

        # Fluctuation strength (1D) — from 4Hz modulation
        fluctuation = mod_features[:, :, 3:4]  # modulation_4Hz

        # Loudness A-weighted (1D)
        loudness_a = (mel_linear * self.a_weights.unsqueeze(-1)).sum(dim=1)
        loudness_a = loudness_a / loudness_a.max(dim=-1, keepdim=True).values.clamp(min=1e-8)
        loudness_a = loudness_a.unsqueeze(-1)

        # Alpha ratio (1D)
        low = mel_linear[:, :40, :].sum(dim=1)
        high = mel_linear[:, 40:100, :].sum(dim=1)
        alpha = low / (low + high).clamp(min=1e-8)
        alpha = alpha.unsqueeze(-1)

        # Hammarberg index (1D)
        peak_low = mel[:, :55, :].max(dim=1).values
        peak_high = mel[:, 55:100, :].max(dim=1).values
        hammarberg = torch.sigmoid((peak_low - peak_high) / 5.0).unsqueeze(-1)

        # Spectral slope 0-500Hz (1D)
        slope = self._spectral_slope(mel[:, :18, :])

        return torch.cat([
            mod_features, sharpness, fluctuation,
            loudness_a, alpha, hammarberg, slope
        ], dim=-1).clamp(0, 1)  # (B, T, 14)

    # [Private methods: _modulation_spectrum, _sharpness_zwicker,
    #  _spectral_slope, _mel_center_frequencies, _a_weighting,
    #  _build_bark_matrix]
```

### 6.7 Dependency-Aware Compute Mekanizması

R3Extractor'da `compute_with_deps` desteği:

```python
# BaseSpectralGroup'a opsiyonel metod:
class BaseSpectralGroup(ABC):
    # ... existing ...

    def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
        """Override this for groups that depend on other group outputs.

        Default: falls back to compute(mel).
        """
        return self.compute(mel)

# R3Extractor stage-ordered execution:
# Stage 1: A,B,C,D,F,J,K → compute(mel)
# Stage 2: E,G,H → compute_with_deps(mel, {stage1_outputs})
# Stage 3: I → compute_with_deps(mel, {stage1+stage2_outputs})
```

---

## Bölüm 7: Deneysel Doğrulama Planı

### 7.1 Doğrulama Gerektiren Feature'lar

Crossref §7.2'deki 6 feature için benchmark planı:

#### Test 1: Mel-Based Chroma [49:60] — Key Detection Accuracy

| Parametre | Değer |
|-----------|-------|
| **Feature** | chroma_C..chroma_B [49:60] |
| **Benchmark** | librosa.chroma_cqt (CQT-based chroma) ile karşılaştırma |
| **Veri seti** | GTZAN (1000 track × 30s), Hainsworth key dataset (100 tracks) |
| **Metrik** | Key detection accuracy (correct key / total) |
| **Başarı kriteri** | ≥85% accuracy (CQT-based ~90%) |
| **Test prosedürü** | 1. Mel-based chroma hesapla → Krumhansl-Schmuckler key detection |
|  | 2. CQT-based chroma hesapla → aynı key detection |
|  | 3. Ground truth key ile karşılaştır |
|  | 4. Hata analizi: hangi key'lerde fark var? |
| **Fallback planı** | Accuracy <85% ise: σ parametresini tune et (0.3-1.0 arası grid search); |
|  | hâlâ yetersizse: CQT yaklaşımı Option B'ye geçiş (maliyet +2ms) |

#### Test 2: Melodic Entropy [87] — IDyOM IC Korelasyonu

| Parametre | Değer |
|-----------|-------|
| **Feature** | melodic_entropy [87] |
| **Benchmark** | IDyOM melodic Information Content (gold standard) |
| **Veri seti** | Essen Folksong Collection (6000+ melodi, MIDI) |
| **Metrik** | Pearson korelasyonu (r) — frame-level IC değerleri |
| **Başarı kriteri** | r ≥ 0.7 |
| **Test prosedürü** | 1. MIDI → audio synthesize (piano, 44.1kHz) |
|  | 2. Mel spectrogram → chroma transition entropy hesapla |
|  | 3. IDyOM'dan note-level IC al |
|  | 4. Note boundary'lerde frame-level → note-level average |
|  | 5. Pearson correlation hesapla |
| **Fallback planı** | r < 0.7 ise: transition matrix boyutunu artır (12×12 → 24×24 bigram); |
|  | warm-up süresini uzat (2s → 4s); |
|  | hâlâ yetersizse: [87] "melodic_change_rate" olarak yeniden tanımla |

#### Test 3: Harmonic Entropy [88] — Chord Analysis Korelasyonu

| Parametre | Değer |
|-----------|-------|
| **Feature** | harmonic_entropy [88] |
| **Benchmark** | Uzman harmonik analiz — chord change sürpriz ratings |
| **Veri seti** | Billboard dataset (740 tracks, chord annotations) |
| **Metrik** | Pearson korelasyonu (r) — chord boundary'lerde |
| **Başarı kriteri** | r ≥ 0.6 |
| **Test prosedürü** | 1. Audio → mel → chroma → KL divergence hesapla |
|  | 2. Chord boundary annotation'lardan ground truth surprise hesapla |
|  | 3. Frame-level surprise → chord boundary'lerde average |
|  | 4. Correlation hesapla |
| **Fallback planı** | r < 0.6 ise: running average τ parametresini tune et; |
|  | chord template matching ekle; |
|  | hâlâ yetersizse: [88] "chroma_novelty" olarak yeniden tanımla |

#### Test 4: Syncopation Index [68] — Behavioral Rating Korelasyonu

| Parametre | Değer |
|-----------|-------|
| **Feature** | syncopation_index [68] |
| **Benchmark** | Witek 2014 syncopation degree ratings |
| **Veri seti** | Witek corpus (50 drum patterns, rated by participants) |
| **Metrik** | Spearman korelasyonu (ρ) — pattern-level |
| **Başarı kriteri** | ρ ≥ 0.7 |
| **Test prosedürü** | 1. Drum pattern audio → mel → onset detection |
|  | 2. Onset peaks + tempo → metrical grid → LHL syncopation |
|  | 3. Mean syncopation per pattern |
|  | 4. Spearman correlation ile behavioral ratings karşılaştır |
| **Fallback planı** | ρ < 0.7 ise: metrical grid resolution artır (4→8 levels); |
|  | onset threshold tune et; beat tracking iyileştir; |
|  | hâlâ yetersizse: simplified metric (off-beat energy ratio) kullan |

#### Test 5: Groove Index [71] — Behavioral Groove Ratings

| Parametre | Değer |
|-----------|-------|
| **Feature** | groove_index [71] |
| **Benchmark** | Madison 2006 / Janata 2012 groove ratings |
| **Veri seti** | Groove MIDI Dataset (1150 MIDI patterns) + Madison groove clips |
| **Metrik** | Pearson korelasyonu (r) — clip-level |
| **Başarı kriteri** | r ≥ 0.5 |
| **Test prosedürü** | 1. MIDI → audio synthesize → mel → groove_index hesapla |
|  | 2. Mean groove per clip |
|  | 3. Correlation ile behavioral ratings karşılaştır |
| **Fallback planı** | r < 0.5 ise: composite ağırlıkları optimize et (syncopation, bass, clarity); |
|  | random forest ile en iyi feature combination bul; |
|  | hâlâ yetersizse: [71] "rhythmic_complexity" olarak yeniden tanımla |

#### Test 6: Inharmonicity Index [64] — essentia Karşılaştırması

| Parametre | Değer |
|-----------|-------|
| **Feature** | inharmonicity_index [64] |
| **Benchmark** | essentia Inharmonicity (raw audio spectral peaks) |
| **Veri seti** | NSynth dataset (300k notes, diverse instruments) |
| **Metrik** | Pearson korelasyonu (r) — note-level |
| **Başarı kriteri** | r ≥ 0.8 |
| **Test prosedürü** | 1. NSynth audio → mel → mel-based inharmonicity |
|  | 2. NSynth audio → essentia Inharmonicity (ground truth) |
|  | 3. Per-note average → correlation |
| **Fallback planı** | r < 0.8 ise: harmonic template matching iyileştir (K=8→16 harmonics); |
|  | mel peak detection yerine parabolic interpolation ekle; |
|  | hâlâ yetersizse: [64] "spectral_peakiness" olarak yeniden tanımla |

### 7.2 Doğrulama Zaman Çizelgesi

| Test | Öncelik | Bağımlılık | Tahmini Süre |
|------|---------|------------|-------------|
| Test 1 (Chroma) | **Kritik** — H, I grupları buna bağlı | F grubu implementasyonu | 1 gün |
| Test 4 (Syncopation) | Yüksek — groove, metricality'ye temel | G grubu implementasyonu | 1 gün |
| Test 6 (Inharmonicity) | Orta — bağımsız feature | F grubu implementasyonu | 0.5 gün |
| Test 2 (Melodic entropy) | Orta — IDyOM data hazırlığı gerekli | I grubu + Essen dataset | 2 gün |
| Test 3 (Harmonic entropy) | Orta — Billboard data gerekli | I grubu + Billboard dataset | 1 gün |
| Test 5 (Groove) | Düşük — behavioral data sınırlı | G grubu + Groove dataset | 1 gün |

---

## Bölüm 8: Geçiş Yol Haritası

### 8.1 Phase Zaman Çizelgesi

```
Phase 3B (TAMAMLANDI) ─── Bu doküman: R3-V2-DESIGN.md
    │
    ▼
Phase 3C (SIRADA) ──────── Dokümantasyon güncellemesi
    │                       - 20+ C³ model doc Section 4 güncelleme
    │                       - Yeni R³ [49:128] referansları ekleme
    │                       - Her model için "Potansiyel R³ v2 kullanımı" notu
    │
    ▼
Phase 3E (SIRADA) ──────── Model doc v2.2.0 güncelleme
    │                       - 96 model × Section 4 R³ referans güncelleme
    │                       - Yeni H³ demand 4-tuples (r3_idx 49-127)
    │                       - R³ gap resolution notları
    │
    ▼
Phase 6 (İLERİDE) ──────── Kod implementasyonu
    │
    ├── 6.1: constants.py + dimension_map.py + feature_spec.py güncelle
    │        - R3_DIM = 128
    │        - Dynamic feature names
    │        - Index validation güncelleme
    │
    ├── 6.2: 6 yeni BaseSpectralGroup alt sınıfı yaz (F-K)
    │        - PitchChromaGroup (16D)
    │        - RhythmGrooveGroup (10D)
    │        - HarmonyTonalityGroup (12D)
    │        - InformationSurpriseGroup (7D)
    │        - TimbreExtendedGroup (20D)
    │        - ModulationPsychoacousticGroup (14D)
    │
    ├── 6.3: R3Extractor dependency-aware compute
    │        - STAGE_ORDER dict
    │        - compute_with_deps() mekanizması
    │        - Stage-ordered extract()
    │
    ├── 6.4: Mevcut A-E formül düzeltmeleri
    │        - [24] concentration normalizasyon bug fix
    │        - [10] loudness çift sıkıştırma düzeltme
    │        - [3]/[12], [16]/[1], [17]/[2] duplikasyon çözme
    │
    ├── 6.5: E grubu interaction redesign (Aşama 1)
    │        - Proxy'leri kaldır → gerçek A-D referansları
    │        - compute_with_deps() ekleme
    │
    ├── 6.6: Deneysel doğrulama (Bölüm 7)
    │        - 6 benchmark test
    │        - Parameter tuning
    │        - Fallback uygulamaları (gerekirse)
    │
    └── 6.7: Integration test + 96 model code güncelleme
             - R³ output dim 128 doğrulama
             - C³ model r3[idx] referansları güncelleme
             - End-to-end pipeline testi
```

### 8.2 Phase Bazlı Dosya Üretimi

| Phase | Üretilen/Güncellenen Dosyalar | Sayı |
|-------|------------------------------|:----:|
| 3B | `Docs/R³/R3-V2-DESIGN.md` (bu dosya) | 1 |
| 3C | `Docs/C³/Models/*/Section4_update.md` (yeni R³ referansları) | ~20 |
| 3E | `Docs/C³/Models/*/*.md` (Section 4 v2.2.0) | 96 |
| 6.1 | `mi_beta/core/constants.py`, `dimension_map.py`, `feature_spec.py` | 3 |
| 6.2 | `mi_beta/ear/r3/extensions/{pitch_chroma,rhythm_groove,...}.py` | 6 |
| 6.3 | `mi_beta/ear/r3/__init__.py`, `_registry.py` | 2 |
| 6.4 | `mi_beta/ear/r3/{psychoacoustic,dsp,cross_domain}/*.py` | 5 |
| 6.5 | `mi_beta/ear/r3/cross_domain/interactions.py` | 1 |
| 6.6 | `tests/ear/r3/test_benchmark_*.py` | 6 |
| 6.7 | `mi_beta/brain/units/*/models/*.py` (96 model) | 96 |

### 8.3 Bağımlılıklar ve Parallelization

```
Phase 3C ve 3E paralel çalışabilir (farklı doc kapsamı)

Phase 6 sıralı alt-adımlar:
6.1 ─┐
     ├── 6.2 ─── 6.3 ─── 6.6 (benchmark)
6.4 ─┘                    │
                          ├── 6.5 (E redesign — benchmark sonrasında)
                          │
                          └── 6.7 (integration — tüm 6.x tamamlandıktan sonra)
```

### 8.4 Risk Analizi

| Risk | Olasılık | Etki | Mitigasyon |
|------|----------|------|------------|
| Mel-based chroma kalitesi yetersiz | Orta | Yüksek (H, I grupları etkilenir) | Test 1 erken çalıştır; CQT fallback hazır |
| Modulation spectrum latency bütçeyi aşar | Düşük | Orta | Amortized computing; hop artırma |
| IDyOM approx. korelasyonu düşük | Yüksek | Orta | [87] yeniden tanımla (melodic_change_rate) |
| 128D model eğitim hızını düşürür | Düşük | Düşük | C³ modelleri sadece ihtiyaç duydukları boyutları seçer |
| Backward compat sorunları | Orta | Yüksek | R3_DIM_V1, _FEATURE_NAMES_V1 legacy constants |

---

*Generated by Phase 3B Architecture Design Chat | 2026-02-13*
*Input: R3-CROSSREF.md, R3-DEMAND-MATRIX.md, R3-DSP-SURVEY-THEORY.md, R3-DSP-SURVEY-TOOLS.md*
*Code reference: mi_beta/ear/r3/ (READ-ONLY), mi_beta/core/, mi_beta/contracts/*
