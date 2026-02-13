# R³ v2 Crossref — Three-Perspective Synthesis

> **Phase**: 3A-3 (Crossref Chat)
> **Inputs**: R3-DEMAND-MATRIX.md (R1), R3-DSP-SURVEY-THEORY.md (R2), R3-DSP-SURVEY-TOOLS.md (R3)
> **Output**: Definitive R³ v2 feature design (128D)
> **Created**: 2026-02-13
> **Status**: COMPLETE

---

## Bölüm 1: Üç Perspektif Karşılaştırması

### 1.1 Boyut Hedefi Karşılaştırması

| Perspektif | Kaynak | Minimum | Önerilen | Maksimum | Mevcut Revizyon |
|-----------|--------|---------|----------|----------|-----------------|
| **R1** (Bottom-up) | 96 model gap analizi | 57D (+8) | **68D** (+19) | ~128D (+79) | Hayır — mevcut 49D korunur |
| **R2** (Literatür) | 121 dosya + psikoakustik | — | **~128D** (+79) | ~141D (+92) | **Evet** — ciddi sorunlar tespit edildi |
| **R3** (Toolkit) | 6 toolkit + standartlar | **128D** (+79) | 192D (+143) | 256D (+207) | Hayır — mevcut A-E korunur |

**Konsensüs noktaları:**
- Her üç perspektif 128D'nin altında bir hedefin yetersiz olduğunda hemfikir
- R2 ve R3 birbirinden bağımsız olarak 128D'yi "önerilen minimum" olarak belirliyor
- R1'in 68D önerisi yalnızca mevcut model taleplerini karşılar; gelecek ihtiyaçları kapsamaz

**Ayrışma noktaları:**
- R2 mevcut 49D'de ciddi sorunlar tespit etti (~15-20 efektif bağımsız boyut); R3 mevcut durumu kabul ediyor
- R2 192D+ desteklerken, R1 68D yeterli buluyor — 3× fark
- R3'ün 256D önerisi büyük ölçüde MFCC delta-delta, ERB, NMF gibi toolkit-driven genişlemeye dayanıyor

**KARAR: 128D (49 mevcut + 79 yeni)**

Gerekçe:
1. **R1+R2 kesişimi**: R1'in talep ettiği ~19D yeni özellik, R2'nin önerdiği ~79 yeni boyutun alt kümesi. 128D R1'in tüm Tier 1-3 taleplerini karşılar.
2. **Real-time fizibilite**: R3 §4 — 128D ~1.2 ms/frame, 4.8× RT headroom (GPU batch). 256D bile (4.2 ms) RT uyumlu ama marjinal.
3. **Power-of-2 avantajı**: 128 = 2⁷. GPU tensor hizalaması, PyTorch DCT, ve gelecek genişleme (128→256) açısından optimal.
4. **Backward compatibility**: Mevcut [0:49] indeksleri değişmez. 96 model docu Section 4 sadece yeni boyut eklentileri alır.
5. **Psikoakustik kapsam**: R2'nin 67 aday feature'ından 46'sı 128D'ye sığar. Kalan 21 yüksek maliyetli veya ham ses gerektiren özellikler.

### 1.2 Grup Yapısı Karşılaştırması

| Kriter | R1 (Bottom-up) | R2 (Literatür) | R3 (Toolkit) |
|--------|----------------|----------------|--------------|
| Yeni grup sayısı | 4 | 4 | 5 |
| Grup yapısı | F:Pitch(5D), G:Rhythm(5D), H:Harmony(5D), I:Info(4D) | F:Pitch(16-18D), G:Rhythm(8-12D), H:Harmony(12-18D), I:Info(8-12D) | F:PitchHarmony(18D), G:RhythmGroove(12D), H:SpectralDetail(20D), I:InfoDynamics(9D), J:ModPerception(20D) |
| Toplam yeni D | 19D | 44-60D | 79D |
| Mevcut revizyon | Hayır | A→10-12D, B→7D, C→10D, D→8D, E→16-24D | Hayır |

**Konsensüs:**
- Her üçü Pitch, Rhythm, Harmony, Information olmak üzere 4 temel yeni grup öneriyor
- İsimlendirme ve kapsam büyük ölçüde örtüşüyor

**Ayrışma:**
- R1 her grubu 4-5D ile kısıtlıyor (sadece talep edilen özellikler); R2/R3 çok daha geniş
- R3 beşinci grup olarak "Spectral Detail" (MFCC+contrast) ve altıncı olarak "Modulation" ekliyor — R1 ve R2 bunları önermiyor
- R2 mevcut grupları revize ediyor; R1 ve R3 olduğu gibi bırakıyor

**KARAR: 6 yeni grup (F-K), mevcut A-E korunur**

| Grup | Ad | Boyut | Aralık | Kaynak | Gerekçe |
|------|-----|------|--------|--------|---------|
| F | Pitch & Chroma | 16D | [49:65] | R1 §3 (16 model), R2 §4.1, R3 §5.1 | 4 temel grubun en çok talep edilen ikincisi |
| G | Rhythm & Groove | 10D | [65:75] | R1 §3 (17+14 model), R2 §4.2, R3 §5.2 | STU+MPU birimleri için kritik |
| H | Harmony & Tonality | 12D | [75:87] | R1 §3 (5-13 model), R2 §4.3, R3 §5.1(kısmi) | NDU+PCU+IMU birimleri için gerekli |
| I | Information & Surprise | 7D | [87:94] | R1 §3 (18+13 model), R2 §4.4, R3 §5.4 | En yüksek talep; RPU+PCU kritik bağımlılık |
| J | Timbre Extended | 20D | [94:114] | R2 §3.3 (timbre revizyonu), R3 §5.3 | MFCC+spectral_contrast: MIR'ın en kanıtlı özellikleri |
| K | Modulation & Psychoacoustic | 14D | [114:128] | R2 §3.4 (modülasyon), R3 §5.5 | Temporal algı + psikoakustik köprü |

Toplam: 49 (mevcut) + 16 + 10 + 12 + 7 + 20 + 14 = **128D** ✓

### 1.3 Mevcut Grup Revizyonu Kararı

**R2 pozisyonu** (REVIZE):
- ~15-20 efektif bağımsız boyut (49D nominal)
- 3 çapraz duplikasyon: [3]≡[12], 1-[16]≡[1], [2]≡[17]
- Normalizasyon bug'ı: concentration [24]
- Stevens' law çift-sıkıştırma: loudness [10]
- A→10-12D, B→7D, C→10D, D→8D, E→16-24D

**R3 pozisyonu** (KORU):
- Mevcut özellikleri koru, yenileri ekle
- "Complement, not duplicate" prensibi

**R1 pozisyonu** (KORU):
- Gap analizi mevcut grup sorunlarını kapsamıyor
- Mevcut 49D'yi "yeterli" buluyor (sorunları tespit etmemiş)

**KARAR: KORU + FLAGLE**

Mevcut [0:49] indeksleri **değiştirilmez**. Gerekçe:
1. **96 model docu** Section 4'te [0:48] indekslerine referans var — değişiklik tüm docu'ları bozar
2. **mi_beta/ kodu** sabit indeks aralıkları kullanıyor — Phase 6 öncesi değişiklik mümkün değil
3. **R2'nin sorunları gerçek** ama çözümleri Phase 6 kod güncellemesini gerektiriyor

Phase 6'da düzeltilecek sorunlar (FLAG):
- DUPLIKASYON: [3]≡[12], [1]↔[16], [2]≡[17] → formül değişikliği
- BUG: [24] concentration normalizasyonu → formül düzeltme
- DOMAIN: [10] loudness çift-sıkıştırma → lineer spektrogram erişimi gerekli
- PROXY: E grubu [25:49] bağımsız proxy'leri → gerçek A-D çıktılarını kullanma

### 1.4 Feature İsim Kanonik Listesi

R1, R2, R3'te aynı kavrama verilen farklı isimler:

| Kavram | R1 İsmi | R2 İsmi | R3 İsmi | KANONİK İSİM |
|--------|---------|---------|---------|---------------|
| Pitch sınıfı dağılımı | pitch_chroma | chroma_vector | approximate_chromagram | **chroma_vector** |
| Melodik belirsizlik | melodic_entropy | melodic_information_content | — | **melodic_entropy** |
| Harmonik belirsizlik | harmonic_entropy | harmonic_surprisal | — | **harmonic_entropy** |
| Senkopasyon ölçüsü | syncopation_index | syncopation_index | syncopation | **syncopation_index** |
| Metrik düzenlilik | metricality_index | metrical_level | — | **metricality_index** |
| Tonal kararlılık | tonal_stability | tonal_stability / key_clarity | — | **tonal_stability** (ayrı: **key_clarity**) |
| Sürpriz sinyali | — | spectral_surprise | spectral_surprise | **spectral_surprise** |
| Ritim bilgi-içeriği | rhythmic_information_content | — | information_content | **rhythmic_information_content** |
| Groove kalitesi | groove_index | groove_factor | groove_features | **groove_index** |
| Tonal uzay pozisyonu | tonal_space_trajectory | tonnetz_coordinates | tonnetz | **tonnetz** (6D) |
| Spectral kontrast | — | spectral_contrast | spectral_contrast | **spectral_contrast** |
| MFCC | — | — | MFCC | **mfcc** |
| Modülasyon spektrumu | — | modulation_spectrum | modulation_spectrum | **modulation_spectrum** |

---

## Bölüm 2: Gap ↔ Feature Eşleştirme Tablosu

R1 Bölüm 1'deki 31 ACOUSTIC gap, R2/R3 çözümleriyle eşleştirildi.

### Kategori (a): Bilinen DSP ile Çözülebilir — 14 Gap

#### GAP-4: metricality_index (metrik düzenlilik ölçüsü)
- **Kaynak**: IMU-RASN (Grahn & Brett 2007 N=27 fMRI)
- **R2 karşılığı**: §4.2 G.3 metrical_level — multi-scale autocorrelation
- **R3 karşılığı**: §3 #23 syncopation_index / §5.2 g_groove — onset→beat pipeline
- **Mel uyumluluğu**: EVET — onset strength autocorrelation'dan türetilir
- **Hesaplama maliyeti**: Orta (Tier 2, ~0.5 ms/frame)
- **Çözüm**: G:Rhythm grubuna `metricality_index` olarak eklendi [69]
- **Durum**: ✅ Çözüldü

#### GAP-5: predictive_entropy (öngörü belirsizliği)
- **Kaynak**: IMU-PMIM, IMU-HCMC, IMU-MSPBA (Cheung 2019, Gold 2019/2023)
- **R2 karşılığı**: §4.4 I.3 predictive_entropy — conditional entropy
- **R3 karşılığı**: §3 #25 information_content — entropy + surprise + predictability
- **Mel uyumluluğu**: EVET — frame istatistiklerinden hesaplanır
- **Hesaplama maliyeti**: Orta (Tier 2, ~0.5 ms/frame)
- **Çözüm**: I:Information grubuna `predictive_entropy` olarak eklendi [92]
- **Durum**: ✅ Çözüldü

#### GAP-6: pitch_chroma (siklik oktav-eşdeğerliği)
- **Kaynak**: IMU-TPRD (Briley 2013 EEG)
- **R2 karşılığı**: §5.2 chroma_vector — 12-bin pitch class profile, mel→freq→PC folding
- **R3 karşılığı**: §3 #11 approximate_chromagram — mel→frequency→pitch class fold
- **Mel uyumluluğu**: EVET — mel-to-chroma folding (R3 Appendix B algoritması)
- **Hesaplama maliyeti**: Ucuz (Tier 1, ~1 ms/frame)
- **Çözüm**: F:Pitch grubuna `chroma_vector` (12D) olarak eklendi [49:61]
- **Durum**: ✅ Çözüldü

#### GAP-9: isochrony_nPVI (ritmik düzenlilik)
- **Kaynak**: IMU-CSSL (Burchardt 2025, Ravignani 2021)
- **R2 karşılığı**: §4.2 — rhythmic regularity measures
- **R3 karşılığı**: §3 #24 groove_features — beat clarity, regularity
- **Mel uyumluluğu**: EVET — onset detection → IOI dağılımı → nPVI hesaplama
- **Hesaplama maliyeti**: Orta (Tier 2, onset detection pipeline)
- **Çözüm**: G:Rhythm grubuna `isochrony_nPVI` olarak eklendi [70]
- **Durum**: ✅ Çözüldü

#### GAP-10: groove_index (hareket-tetikleyici kalite)
- **Kaynak**: IMU-RIRI (Li 2025 locomotion biomechanics)
- **R2 karşılığı**: §4.2 G.5 groove_factor — tempo stability × microtiming
- **R3 karşılığı**: §3 #24 groove_features (5D) — Janata/Madison
- **Mel uyumluluğu**: EVET — onset→beat→stats pipeline
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: G:Rhythm grubuna `groove_index` olarak eklendi [71]
- **Durum**: ✅ Çözüldü

#### GAP-12: inharmonicity_index (harmonik sapmadan bağımsız ölçü)
- **Kaynak**: ASU-IACM (Basinski 2025 ApEn)
- **R2 karşılığı**: §3.3 C.9 inharmonicity_score — peak deviation from harmonic series
- **R3 karşılığı**: §2.2 Dissonance (essentia, partial mel-compatible)
- **Mel uyumluluğu**: KISMEN — mel peak detection'dan yaklaşık hesaplanabilir
- **Hesaplama maliyeti**: Orta (Tier 2-3, ~3 ms/frame)
- **Çözüm**: F:Pitch grubuna `inharmonicity_index` olarak eklendi [64]
- **Durum**: ✅ Çözüldü

#### GAP-14: syntactic_irregularity (harmonik kural ihlali derecesi)
- **Kaynak**: NDU-SDD, NDU-CDMR (Kim 2021 MEG)
- **R2 karşılığı**: §4.3 H.7 harmonic_tension — Lerdahl model
- **R3 karşılığı**: §3 #19 harmonic_tension (3D) — tonal distance + entropy + flux
- **Mel uyumluluğu**: KISMEN — chroma→key→template deviation
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: H:Harmony grubuna `syntactic_irregularity` olarak eklendi [86]
- **Durum**: ✅ Çözüldü

#### GAP-15: perceptual_ambiguity (algısal belirsizlik düzeyi)
- **Kaynak**: NDU-SDD (Kim 2021 MEG F(2,36)=12.373)
- **R2 karşılığı**: §4.4 I.8 tonal_ambiguity — entropy of key correlations
- **R3 karşılığı**: İma edilmiş (chroma entropy)
- **Mel uyumluluğu**: KISMEN — chroma→key profile softmax→entropy
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: I:Information grubuna `tonal_ambiguity` olarak eklendi [93]
- **Durum**: ✅ Çözüldü

#### GAP-18: syncopation_index (beat offset from metrical grid)
- **Kaynak**: MPU-PEOM (Grahn & Brett 2007; Witek 2014)
- **R2 karşılığı**: §4.2 G.4 syncopation_index — LHL metrical conflict
- **R3 karşılığı**: §3 #23 syncopation — LHL via onset strength, Medium cost
- **Mel uyumluluğu**: KISMEN — onset→beat tracking→metrical grid→LHL
- **Hesaplama maliyeti**: Orta (Tier 2, ~0.5 ms/frame)
- **Çözüm**: G:Rhythm grubuna `syncopation_index` olarak eklendi [68]
- **Durum**: ✅ Çözüldü

#### GAP-23: 1/f_spectral_slope (spektral eğim)
- **Kaynak**: PCU-UDP (Borges 2019)
- **R2 karşılığı**: Doğrudan karşılık yok ama D.7 spectral_change_rate benzer
- **R3 karşılığı**: §3 #33 spectral_slopes — linear regression 0-500, 500-1500 Hz
- **Mel uyumluluğu**: EVET — mel band üzerinde lineer regresyon
- **Hesaplama maliyeti**: Ucuz (Tier 1)
- **Çözüm**: K:Modulation grubuna `spectral_slope_0_500` olarak eklendi [126]
- **Durum**: ✅ Çözüldü

#### GAP-24: key_clarity / tonal_stability
- **Kaynak**: PCU-UDP (Mencke 2019 d=3.0)
- **R2 karşılığı**: §5.3 key_clarity — Krumhansl-Schmuckler max correlation
- **R3 karşılığı**: §3 #19 harmonic_tension includes tonal distance
- **Mel uyumluluğu**: KISMEN — chroma→24 key profile correlation
- **Hesaplama maliyeti**: Orta (Tier 2, ~2 ms/frame)
- **Çözüm**: H:Harmony grubuna `key_clarity` [75] ve `tonal_stability` [84] olarak eklendi
- **Durum**: ✅ Çözüldü

#### GAP-28: rhythmic_information_content
- **Kaynak**: RPU-SSRI, RPU-IUCP (Spiech 2022, Gold 2019)
- **R2 karşılığı**: §4.4 — information-theoretic features
- **R3 karşılığı**: §3 #25 information_content (3D)
- **Mel uyumluluğu**: EVET — onset pattern entropy
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: I:Information grubuna `rhythmic_information_content` olarak eklendi [89]
- **Durum**: ✅ Çözüldü

#### GAP-30: melodic_entropy (pitch geçiş belirsizliği)
- **Kaynak**: RPU-LDAC, RPU-IUCP + 16 diğer model (Tier 1 talep)
- **R2 karşılığı**: §4.4 I.6 melodic_information_content — IDyOM framework
- **R3 karşılığı**: §3 #25 information_content — entropy + surprise
- **Mel uyumluluğu**: KISMEN — chroma entropy değişimi olarak yaklaşık hesaplanabilir (tam IDyOM mel'den mümkün değil)
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: I:Information grubuna `melodic_entropy` olarak eklendi [87]
- **Not**: Tam IDyOM uygulaması yerine, chroma-tabanlı pitch transition entropy yaklaşımı kullanılacak
- **Durum**: ✅ Çözüldü (yaklaşık)

#### GAP-31: harmonic_entropy (akor geçiş belirsizliği)
- **Kaynak**: RPU-LDAC + 12 diğer model (Tier 1 talep)
- **R2 karşılığı**: §4.4 I.5 harmonic_surprisal — chord transition probability
- **R3 karşılığı**: §3 #25 — chroma KL divergence
- **Mel uyumluluğu**: KISMEN — chroma→chord detection→transition matrix→entropy
- **Hesaplama maliyeti**: Orta (Tier 2)
- **Çözüm**: I:Information grubuna `harmonic_entropy` olarak eklendi [88]
- **Durum**: ✅ Çözüldü (yaklaşık)

### Kategori (b): Yeni Yöntem Gerekli — 9 Gap

#### GAP-2: tonal_space_trajectory
- **Kaynak**: IMU-MEAMN (Janata 2009 MPFC toroidal tracking)
- **R2 karşılığı**: §5.3 tonnetz_coordinates (6D) — position sağlar ama trajectory yok
- **R3 karşılığı**: §3 #18 tonnetz (6D) — tonal centroid
- **Mel uyumluluğu**: KISMEN
- **Çözüm**: H:tonnetz frame-to-frame L2 distance "harmonic_change" [83] olarak eklendi; trajectory bilgisi H³ (temporal) katmanında sağlanabilir
- **Durum**: ⚠️ Kısmen — pozisyon var, trajectory H³'e bırakıldı

#### GAP-7: harmonic_resolvability
- **Kaynak**: IMU-TPRD (Norman-Haignere 2013)
- **R2 karşılığı**: §5.2 virtual_pitch_salience — harmonic template matching
- **R3 karşılığı**: Doğrudan karşılık yok
- **Mel uyumluluğu**: KISMEN — mel peak prominence proxy
- **Çözüm**: F:pitch_salience [63] harmonik resolve edilebilirliğin proxy'si; tam çözüm spectral peak detection gerektiriyor
- **Durum**: ⚠️ Kısmen — proxy

#### GAP-8: melodic_contour_direction
- **Kaynak**: IMU-DMMS (Sena Moore 2025 MCRF)
- **R2 karşılığı**: §5.2 pitch_height — weighted log-frequency
- **R3 karşılığı**: Doğrudan karşılık yok
- **Mel uyumluluğu**: KISMEN — pitch_height'ın temporal derivative'i
- **Çözüm**: F:pitch_height [61] frame-to-frame delta ile contour direction yaklaşık elde edilir; H³ morph="slope" olarak daha iyi çözülür
- **Durum**: ⚠️ Kısmen — delta ile yaklaşım

#### GAP-13: consonance_gradient
- **Kaynak**: ASU-CSG (Fishman, Bravo 2017 d=5.16)
- **R2 karşılığı**: A grubu consonance features zaten mevcut
- **R3 karşılığı**: Karşılık yok
- **Mel uyumluluğu**: EVET — A grubu frame-to-frame derivative'i
- **Çözüm**: A grubu çıktılarının temporal gradient'ı D:spectral_flux [21] ile birlikte kullanılabilir; ayrı feature gerekmez
- **Durum**: ⚠️ Kısmen — mevcut A+D kombinasyonu yeterli

#### GAP-17: perceived_musical_roundness
- **Kaynak**: NDU-CDMR, NDU-EDNR (Wöhrle 2024 η²p=0.592)
- **R2 karşılığı**: Doğrudan karşılık yok
- **R3 karşılığı**: Karşılık yok
- **Mel uyumluluğu**: KISMEN
- **Çözüm**: H:tonal_stability [84] + H:key_clarity [75] composite proxy. "Roundness" konseptinin akustik tanımı belirsiz — deneysel doğrulama gerekli
- **Durum**: ⚠️ Kısmen — AÇIK SORU: "roundness" nedir?

#### GAP-19: metrical_structure_complexity
- **Kaynak**: MPU-PEOM (Grahn & Brett 2007)
- **R2 karşılığı**: §4.2 G.3 metrical_level — multi-scale autocorrelation
- **R3 karşılığı**: §3 #21 tempogram_ratio — metrical subdivision strengths
- **Mel uyumluluğu**: KISMEN — multi-scale autocorrelation
- **Çözüm**: G:metricality_index [69] metrik düzenlilik ölçer; complexity ≈ 1 - metricality. K:modulation_spectrum metrik katman sayısını dolaylı yansıtır
- **Durum**: ⚠️ Kısmen — ters proxy

#### GAP-20: locomotion_periodicity (0.5-2 Hz)
- **Kaynak**: MPU-GSSM (Yamashita 2025 stride time CV)
- **R2 karşılığı**: Doğrudan karşılık yok
- **R3 karşılığı**: §5.5 j_mod — modulation energy at 0.5-2 Hz rates
- **Mel uyumluluğu**: EVET — energy envelope autocorrelation at 0.5-2 Hz
- **Çözüm**: K:modulation_0.5Hz [114] ve K:modulation_1Hz [115] ve K:modulation_2Hz [116] 0.5-2 Hz bandını karşılar; G:tempo_estimate [65] da bu aralıkta çalışır
- **Durum**: ⚠️ Kısmen — modulation spectrum'dan türetilir ama dedike feature değil

#### GAP-22: periodicity (R³[5] yerine)
- **Kaynak**: PCU-PWUP, PCU-UDP
- **R2 karşılığı**: §5.1 harmonicity — multi-lag autocorrelation
- **R3 karşılığı**: Karşılık yok
- **Mel uyumluluğu**: KISMEN
- **Çözüm**: F:pitch_salience [63] + A:harmonicity proxy [2] periodicity bilgisini birlikte sağlar; Phase 6'da A[5] "inharmonicity" → gerçek periodicity olarak revize edilecek
- **Durum**: ⚠️ Kısmen — Phase 6 formül düzeltmesi gerekli

#### GAP-29: rhythmic_entropy (ritmik belirsizlik)
- **Kaynak**: RPU-SSRI, RPU-IUCP (Spiech 2022)
- **R2 karşılığı**: §4.2 G.7 rhythmic_entropy — IOI distribution entropy
- **R3 karşılığı**: İma edilmiş (onset pattern analysis)
- **Mel uyumluluğu**: EVET — onset times → IOI → entropy
- **Çözüm**: I:predictive_entropy [92] ve I:rhythmic_information_content [89] birlikte ritmik belirsizliği karşılar. Ayrıca G:onset_regularity [74] ters proxy'dir (regularity = 1 - entropy)
- **Durum**: ⚠️ Kısmen — dolaylı kapsam (2 feature kombinasyonu)

### Kategori (c): R³ Kapsamı Dışı — 8 Gap

#### GAP-1: nostalgia_acoustic_signature
- **Kaynak**: IMU-MEAMN (Sakakibara 2025)
- **Neden**: Composite duygusal özellik — birden fazla R³ boyutunun ağırlıklı kombinasyonu. CNN embedding gerektirir. Tekil akustik boyut değil.
- **Durum**: ❌ Çözülemez — L³ (semantic) katmanında çözülmeli

#### GAP-3: arousal_potential
- **Kaynak**: IMU-MMP (Scarratt 2025)
- **Neden**: B:Energy grubunun composite'i (amplitude + onset_strength + tempo). Bağımsız akustik boyut değil.
- **Durum**: ❌ Çözülemez — L³ arousal dimension olarak türetilebilir

#### GAP-11: relaxation_index
- **Kaynak**: IMU-VRIAP (Arican & Soyman 2025)
- **Neden**: B+C composite (düşük enerji + sıcak timbre). Bağımsız boyut değil.
- **Durum**: ❌ Çözülemez — L³ katmanında

#### GAP-16: cortical_entrainment_index
- **Kaynak**: NDU-CDMR, NDU-EDNR (Bridwell 2017)
- **Neden**: Beyinsel EEG ITPC ölçümü. Akustik özellik değil — neural entrainment H³ temporal katmanında BEP mekanizması ile modellenir.
- **Durum**: ❌ Çözülemez — H³/BEP mekanizması kapsamında

#### GAP-21: R³[14] tonalness→brightness_kuttruff remap
- **Kaynak**: PCU-PWUP
- **Neden**: NAMING mismatch (doc-code farkı). Mevcut indeks doğru, ad yanlış. Phase 5 isimlendirme düzeltmesi.
- **Durum**: ❌ R³ genişleme değil — Phase 5 NAMING çözümü

#### GAP-25: onset_synchrony_quality
- **Kaynak**: RPU-SSRI (Bigand 2025, Kokal 2011)
- **Neden**: Multi-track gerektirir. Mevcut R³ single-stream pipeline'ı tek ses kaynağı varsayar.
- **Durum**: ❌ Çözülemez — multi-track pipeline gerekli (Phase 4+ konusu)

#### GAP-26: timbral_blend_index
- **Kaynak**: RPU-SSRI (Bigand 2025)
- **Neden**: Multi-track gerektirir.
- **Durum**: ❌ Çözülemez — multi-track

#### GAP-27: rhythmic_entrainment_index
- **Kaynak**: RPU-SSRI (Ni 2024, Kokal 2011)
- **Neden**: Multi-track gerektirir.
- **Durum**: ❌ Çözülemez — multi-track

### 2.1 Özet Tablo

| Kategori | Sayı | % | Açıklama |
|----------|------|---|----------|
| (a) DSP ile çözülebilir | 14 | 45% | R³ v2'de doğrudan eklendi |
| (b) Yeni yöntem gerekli | 9 | 29% | Proxy veya yaklaşık çözüm, Phase 3B deneysel doğrulama |
| (c) Kapsam dışı | 8 | 26% | 3 multi-track, 2 composite, 1 neural, 1 naming, 1 semantic |
| **Toplam** | **31** | **100%** | |

---

## Bölüm 3: Talep × Fizibilite Çapraz Matrisi

R1 §3'teki en çok talep edilen feature'lar × R3 fizibilite × R2 psikoakustik temel:

| Sıra | Feature (R1) | Talep | R3 Mel Uyumu | R3 Maliyet | R2 Psikoakustik Temeli | R³ v2 Grubu | Kesin Karar |
|------|-------------|:-----:|:-------------|:-----------|:-----------------------|:------------|:------------|
| 1 | melodic_entropy | 18 | KISMEN (chroma entropy Δ) | Orta (Tier 2) | §4.4 I.6: IDyOM, Pearce 2005 — prediction error framework | I [87] | **DAHİL** (yaklaşık) |
| 2 | syncopation_index | 17 | KISMEN (onset→beat grid→LHL) | Orta (Tier 2) | §4.2 G.4: Witek 2014, LHL 1984 — metrical conflict | G [68] | **DAHİL** |
| 3 | metricality_index | 14 | EVET (autocorrelation) | Orta (Tier 2) | §4.2 G.3: multi-scale temporal nesting (Morris) | G [69] | **DAHİL** |
| 4 | harmonic_entropy | 13 | KISMEN (chroma transition) | Orta (Tier 2) | §4.4 I.5: chord transition probability — Pearce/IDyOM | I [88] | **DAHİL** (yaklaşık) |
| 5 | rhythmic_IC | 8 | EVET (onset pattern entropy) | Orta (Tier 2) | §4.4: information theory — Shannon, Dubnov | I [89] | **DAHİL** |
| 6 | groove_index | 7 | EVET (onset→beat→stats) | Orta (Tier 2) | §4.2 G.5: Madison 2006, Janata 2012 — sensorimotor | G [71] | **DAHİL** |
| 7 | syntactic_irregularity | 5 | KISMEN (chroma template) | Orta (Tier 2) | §4.3 H.7: Lerdahl 2001 — tonal tension hierarchy | H [86] | **DAHİL** |
| 8 | pitch_chroma | 5 | EVET (mel→freq→PC fold) | Ucuz (Tier 1) | §5.2: Krumhansl 1990, Shepard 1964 — octave equivalence | F [49:61] | **DAHİL** (12D) |
| 9 | tonal_stability | 5 | KISMEN (key clarity + Δ) | Orta (Tier 2) | §5.3: Krumhansl-Kessler 1982 — tonal hierarchy | H [84] | **DAHİL** |
| 10 | isochrony_nPVI | 5 | EVET (onset→IOI→nPVI) | Orta (Tier 2) | §4.2: Ravignani 2021 — rhythmic regularity measure | G [70] | **DAHİL** |
| 11 | melodic_contour | 3 | KISMEN (pitch_height Δ) | Ucuz (Tier 1) | §5.2 pitch_height: Weber-Fechner | F [61] delta | **DAHİL** (proxy) |
| 12 | harmonic_resolution | 3 | KISMEN (template match) | Orta (Tier 2-3) | §5.3: Lerdahl hierarchical tension | H [84] proxy | **DAHİL** (proxy) |
| 13 | inharmonicity_index | 2 | KISMEN (mel peak deviation) | Orta (Tier 2-3) | §5.1: Standard; Stanford-Spectral | F [64] | **DAHİL** |
| 14 | harmonic_resolvability | 2 | KISMEN (peak prominence) | Orta (Tier 2-3) | §5.2: Parncutt 1989 virtual pitch | F [63] proxy | **DAHİL** (proxy) |
| 15 | rhythmic_entropy | 2 | EVET (IOI entropy) | Ucuz (Tier 1) | §4.2 G.7: standard information theory | I [89]+[92] | **DAHİL** (kapsanıyor) |
| 16 | perceptual_ambiguity | 1 | KISMEN (key entropy) | Orta (Tier 2) | §4.4 I.8: tonal ambiguity | I [93] | **DAHİL** |
| 17 | 1/f_spectral_slope | 1 | EVET (mel regression) | Ucuz (Tier 1) | — (DSP standard, psikoakustik temeli zayıf) | K [126] | **DAHİL** |
| 18 | locomotion_periodicity | 1 | EVET (0.5-2 Hz mod) | Orta (Tier 2) | — (motor; Yamashita 2025 lokomotif) | K [114:116] | **DAHİL** (modulation) |
| 19 | onset_synchrony | 1 | HAYIR (multi-track) | — | — | — | **HARİÇ** (multi-track) |
| 20 | timbral_blend | 1 | HAYIR (multi-track) | — | — | — | **HARİÇ** (multi-track) |

**Sonuç**: Top-20 talep edilen feature'dan **18'i DAHİL** (%90), 2'si HARİÇ (multi-track requirement).

---

## Bölüm 4: R³ v2 Kesin Feature Listesi

### Genel Bakış

| Grup | Ad | Aralık | Boyut | Durum |
|------|----|--------|-------|-------|
| A | Consonance | [0:7] | 7D | MEVCUT (Phase 6'da formül revizyonu) |
| B | Energy | [7:12] | 5D | MEVCUT (Phase 6'da loudness düzeltmesi) |
| C | Timbre | [12:21] | 9D | MEVCUT (Phase 6'da duplikasyon düzeltmesi) |
| D | Change | [21:25] | 4D | MEVCUT (Phase 6'da concentration bug düzeltmesi) |
| E | Interactions | [25:49] | 24D | MEVCUT (Phase 6'da proxy düzeltmesi) |
| **F** | **Pitch & Chroma** | **[49:65]** | **16D** | **YENİ** |
| **G** | **Rhythm & Groove** | **[65:75]** | **10D** | **YENİ** |
| **H** | **Harmony & Tonality** | **[75:87]** | **12D** | **YENİ** |
| **I** | **Information & Surprise** | **[87:94]** | **7D** | **YENİ** |
| **J** | **Timbre Extended** | **[94:114]** | **20D** | **YENİ** |
| **K** | **Modulation & Psychoacoustic** | **[114:128]** | **14D** | **YENİ** |
| | **Toplam** | **[0:128]** | **128D** | |

---

### Group A: Consonance [0:7] — 7D (MEVCUT, Phase 6 revizyon)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 0 | roughness | MEVCUT | Code: sigmoid(spectral_var/mean) | mel high-bins variance → sigmoid | Plomp-Levelt critical band beating (PROXY — gerçek P-L değil) | <0.1 ms |
| 1 | sethares_dissonance | MEVCUT | Code: mean abs adjacent diff | mel adjacent bin difference → max-norm | Sethares timbre-dependent dissonance (PROXY — gerçek Sethares değil) | <0.1 ms |
| 2 | helmholtz_kang | MEVCUT | Code: lag-1 spectral autocorrelation | centered mel → lag-1 autocorr | Periodicity detection / harmonicity (yalnızca lag-1) | <0.1 ms |
| 3 | stumpf_fusion | MEVCUT | Code: low-quarter energy ratio | mel bottom-quarter / total | Stumpf tonal fusion (PROXY — gerçek fusion değil, ≡warmth[12]) | <0.1 ms |
| 4 | sensory_pleasantness | MEVCUT | Code: 0.6*(1-[1]) + 0.4*[3] | Linear combination | Harrison & Pearce 2020 consonance model (arbitrary weights) | <0.1 ms |
| 5 | inharmonicity | MEVCUT | Code: 1 - helmholtz_kang | Complement of [2] | Deviation from harmonic series (DERIVED, not independent) | <0.1 ms |
| 6 | harmonic_deviation | MEVCUT | Code: 0.5*[1] + 0.5*(1-[2]) | Linear combination | Spectral irregularity (DERIVED, not independent) | <0.1 ms |

**Phase 6 revizyon notu**: R2 §2.1'e göre efektif bağımsız boyut ~3. [3]≡[12] duplikasyonu, [4-6] türetilmiş feature'lar. Phase 6'da [0] gerçek Plomp-Levelt roughness, [1] gerçek Sethares pairwise dissonance, [3] gerçek tonal fusion (Parncutt subharmonic) ile değiştirilecek.

---

### Group B: Energy [7:12] — 5D (MEVCUT, Phase 6 loudness düzeltme)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 7 | amplitude | MEVCUT | Code: RMS of mel bins | mel.pow(2).mean().sqrt() / max | RMS energy (double compression — log-mel'den RMS alınıyor) | <0.1 ms |
| 8 | velocity_A | MEVCUT | Code: d(amp)/dt | sigmoid((amp[t]-amp[t-1]) * 5) | Energy change rate | <0.1 ms |
| 9 | acceleration_A | MEVCUT | Code: d²(amp)/dt² | sigmoid((vel[t]-vel[t-2]) * 5) | Energy buildup curvature | <0.1 ms |
| 10 | loudness | MEVCUT | Code: amplitude^0.3 | RMS^0.3 / max | Stevens' law sone approximation (BUG: çift sıkıştırma) | <0.1 ms |
| 11 | onset_strength | MEVCUT | Code: HWR spectral flux | relu(mel[t]-mel[t-1]).sum() / max | Spectral flux — en güçlü neural sync driver (Weineck 2022) | <0.1 ms |

**Phase 6 revizyon notu**: R2 §2.2 — loudness [10] çift sıkıştırma sorunu. `amplitude^0.3` yerine lineer güç spektrumundan Zwicker/Stevens uygulanmalı. Velocity/acceleration sigmoid normalizasyonu fiziksel anlam kaybettiriyor.

---

### Group C: Timbre [12:21] — 9D (MEVCUT, Phase 6 duplikasyon düzeltme)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 12 | warmth | MEVCUT | Code: low-quarter energy ratio | mel[:N/4].sum() / total | Low-frequency balance — **≡[3] stumpf_fusion** | <0.1 ms |
| 13 | sharpness | MEVCUT | Code: high-quarter energy ratio | mel[3N/4:].sum() / total | High-frequency weighting (DIN 45692 DEĞİL) | <0.1 ms |
| 14 | tonalness | MEVCUT | Code: max(mel)/sum(mel) | Peak dominance | Harmonic-to-noise proxy (Terhardt DEĞİL) | <0.1 ms |
| 15 | clarity | MEVCUT | Code: spectral_centroid / N | Weighted mean bin / N | Spectral centroid (yanlış isim — C80 değil) | <0.1 ms |
| 16 | spectral_smoothness | MEVCUT | Code: 1 - spectral_irregularity | 1 - normalized mean-abs-diff | Spectral envelope regularity — **= 1-[1]** | <0.1 ms |
| 17 | spectral_autocorrelation | MEVCUT | Code: lag-1 autocorrelation | **≡[2] helmholtz_kang** identical computation | Spectral periodicity — DUPLIKAT | <0.1 ms |
| 18 | tristimulus1 | MEVCUT | Code: bottom-third ratio | mel[:N/3].sum() / total | Fundamental strength (mel-band proxy) | <0.1 ms |
| 19 | tristimulus2 | MEVCUT | Code: middle-third ratio | mel[N/3:2N/3].sum() / total | Mid-harmonic energy | <0.1 ms |
| 20 | tristimulus3 | MEVCUT | Code: top-third ratio | mel[2N/3:].sum() / total | High-harmonic energy | <0.1 ms |

**Phase 6 revizyon notu**: R2 §2.3 — 3 duplikasyon ([12]≡[3], [16]=1-[1], [17]≡[2]). Efektif bağımsız boyut ~4. Phase 6'da duplikatlar yeni bağımsız timbre feature'larıyla değiştirilecek: spectral_spread, spectral_skewness, spectral_kurtosis.

---

### Group D: Change [21:25] — 4D (MEVCUT, Phase 6 bug düzeltme)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 21 | spectral_flux | MEVCUT | Code: L2 full-spectrum flux | ||mel[t]-mel[t-1]||₂ / max | Frame-to-frame spectral change | <0.1 ms |
| 22 | distribution_entropy | MEVCUT | Code: Shannon entropy / log(N) | -Σ p·log(p) / log(128) | Spectral uniformity measure | <0.1 ms |
| 23 | distribution_flatness | MEVCUT | Code: Wiener entropy | exp(mean(log(p))) / mean(p) | MPEG-7 spectral flatness | <0.1 ms |
| 24 | distribution_concentration | MEVCUT | Code: HHI * N | Σp²·N → clamp(0,1) | **BUG**: Hem uniform hem concentrated → 1.0 | <0.1 ms |

**Phase 6 revizyon notu**: R2 §2.4 — concentration [24] normalizasyon hatası. `(HHI - 1/N) / (1 - 1/N)` formülü ile düzeltilecek. Ayrıca [22] ve [23] yüksek korelasyonlu (her ikisi spectral uniformity ölçer).

---

### Group E: Interactions [25:49] — 24D (MEVCUT, Phase 6 proxy düzeltme)

| Index | Feature Name | Karar | Hesaplama | Not |
|:-----:|-------------|-------|-----------|-----|
| 25-32 | x_l0l5 (Energy × Consonance) | MEVCUT | amp·roughness, amp·sethares, ... vel·stumpf | 8D |
| 33-40 | x_l4l5 (Change × Consonance) | MEVCUT | flux·roughness, ... entropy·stumpf | 8D |
| 41-48 | x_l5l7 (Consonance × Timbre) | MEVCUT | roughness·warmth, ... stumpf·autocorr | 8D |

**Phase 6 revizyon notu**: R2 §2.5 — Proxy mismatch'ler: roughness_proxy `var()` kullanırken gerçek A[0] `var()/mean()` kullanıyor; helmholtz_proxy `max/sum` (=tonalness) kullanırken gerçek A[2] lag-1 autocorrelation kullanıyor. Phase 6'da proxy'ler kaldırılacak, gerçek A-D çıktıları referans edilecek. Ayrıca yeni F-K gruplarıyla cross-group interaction'lar eklenecek.

---

### Group F: Pitch & Chroma [49:65] — 16D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 49 | chroma_C | YENİ | R2 §5.2 + R3 §3 #11 | mel→freq mapping→pitch class 0 fold→L1 norm | Octave equivalence (Shepard 1964) | ~1 ms (tüm chroma birlikte) |
| 50 | chroma_Db | YENİ | " | pitch class 1 | " | " |
| 51 | chroma_D | YENİ | " | pitch class 2 | " | " |
| 52 | chroma_Eb | YENİ | " | pitch class 3 | " | " |
| 53 | chroma_E | YENİ | " | pitch class 4 | " | " |
| 54 | chroma_F | YENİ | " | pitch class 5 | " | " |
| 55 | chroma_Gb | YENİ | " | pitch class 6 | " | " |
| 56 | chroma_G | YENİ | " | pitch class 7 | " | " |
| 57 | chroma_Ab | YENİ | " | pitch class 8 | " | " |
| 58 | chroma_A | YENİ | " | pitch class 9 | " | " |
| 59 | chroma_Bb | YENİ | " | pitch class 10 | " | " |
| 60 | chroma_B | YENİ | " | pitch class 11 | " | " |
| 61 | pitch_height | YENİ | R2 §5.2 + R3 implied | Σ(log(f_k) · M_k) / Σ(M_k), normalize to [0,1] | Weber-Fechner law; perceived pitch ~ log(frequency) | <0.1 ms |
| 62 | pitch_class_entropy | YENİ | R2 §4.1 F.4 | H = -Σ chroma_c · log(chroma_c) / log(12) | Pitch distribution uniformity — high = chromatic, low = tonal | <0.1 ms |
| 63 | pitch_salience | YENİ | R2 §5.2 + R1 (7 model) | max(mel) prominence / surrounding noise floor ratio | Parncutt (1989) virtual pitch salience; proxy for harmonic resolvability | <0.1 ms |
| 64 | inharmonicity_index | YENİ | R1 GAP-12 + R2 §3.3 C.9 | Spectral peak deviation from nearest harmonic series: Σ|f_k - k·f_0|/(k·f_0) | Deviation from ideal harmonic template | ~3 ms |

**Hesaplama pipeline**: `mel (B,128,T) → freq mapping (pre-computed 128×12 matrix) → chroma (B,T,12) → normalize → pitch_height, PC_entropy from mel statistics → pitch_salience from peak analysis → inharmonicity from harmonic template matching`

**Bağımlıklar**: H grubu tonnetz ve key features bu grubun chroma çıktısına bağlıdır. Compute order: F → H.

---

### Group G: Rhythm & Groove [65:75] — 10D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 65 | tempo_estimate | YENİ | R2 §4.2 G.0 + R3 §2.1 | Onset strength autocorrelation → dominant period → BPM, normalized to [0,1] (30-300 BPM) | Entrainment / preferred tempo (Fraisse 1982) | ~1 ms |
| 66 | beat_strength | YENİ | R2 §4.2 G.1 + R3 §2.1 | Autocorrelation peak value at estimated tempo period | Pulse perception strength | <0.5 ms |
| 67 | pulse_clarity | YENİ | R2 §4.2 G.2 + R3 §3 #22 | Autocorrelation peak / noise floor ratio | How clear is the beat? (ambiguity ↔ groove) | <0.5 ms |
| 68 | syncopation_index | YENİ | R1 Tier 1 (17 model) + R2 §4.2 G.4 + R3 §3 #23 | LHL: onset accent at off-beat positions relative to metrical grid | Witek 2014 — metrical conflict → groove/pleasure | ~0.5 ms |
| 69 | metricality_index | YENİ | R1 Tier 1 (14 model) + R2 §4.2 G.3 | Multi-scale autocorrelation: count of nested integer-ratio pulse levels detected | Grahn & Brett 2007 — metrical hierarchy strength | ~0.5 ms |
| 70 | isochrony_nPVI | YENİ | R1 Tier 2 (5 model) + R2 §4.2 | nPVI = 100 · mean(|IOI_k - IOI_{k+1}| / mean(IOI_k, IOI_{k+1})) from onset times | Rhythmic regularity measure (Ravignani 2021) | ~0.5 ms |
| 71 | groove_index | YENİ | R1 Tier 2 (7 model) + R2 §4.2 G.5 + R3 §3 #24 | Composite: syncopation × bass_energy × pulse_clarity → movement-inducing quality | Madison 2006, Janata 2012 — sensorimotor coupling | ~0.5 ms |
| 72 | event_density | YENİ | R2 §4.2 G.6 + R3 §3 #8 | Count of onsets per second, normalized | Temporal density of auditory events | <0.1 ms |
| 73 | tempo_stability | YENİ | R3 §3 #24 | Variance of local tempo estimates over sliding window, inverted → high = stable | Temporal prediction reliability | ~0.5 ms |
| 74 | rhythmic_regularity | YENİ | R3 §3 #24 + R2 §4.2 | 1 - entropy(IOI distribution) → high = regular, low = irregular | Inverse of rhythmic entropy | ~0.5 ms |

**Hesaplama pipeline**: `mel → onset_strength (from B[11]) → autocorrelation → tempo/beat → metrical grid → syncopation/metricality → IOI analysis → groove composite`

---

### Group H: Harmony & Tonality [75:87] — 12D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 75 | key_clarity | YENİ | R1 GAP-24 + R2 §5.3 + R3 §3 #19 | max(corr(chroma, 24_key_profiles)) — Krumhansl-Schmuckler | Tonal hierarchy perception (Krumhansl & Kessler 1982) | ~2 ms |
| 76 | tonnetz_fifth_x | YENİ | R2 §5.3 + R3 §3 #18 | Σ chroma_c · sin(c·7π/6) (Harte 2006) | Tonal space: circle-of-fifths position | ~1 ms (tüm tonnetz birlikte) |
| 77 | tonnetz_fifth_y | YENİ | " | Σ chroma_c · cos(c·7π/6) | " | " |
| 78 | tonnetz_minor_x | YENİ | " | Σ chroma_c · sin(c·3π/6) | Tonal space: minor-third relations | " |
| 79 | tonnetz_minor_y | YENİ | " | Σ chroma_c · cos(c·3π/6) | " | " |
| 80 | tonnetz_major_x | YENİ | " | Σ chroma_c · sin(c·4π/6) | Tonal space: major-third relations | " |
| 81 | tonnetz_major_y | YENİ | " | Σ chroma_c · cos(c·4π/6) | " | " |
| 82 | voice_leading_distance | YENİ | R2 §5.3 + R3 implied | L1 norm: Σ|chroma_t - chroma_{t-1}| | Tymoczko — voice-leading parsimony | <0.5 ms |
| 83 | harmonic_change | YENİ | R2 §4.3 H.5 | 1 - cosine(chroma_t, chroma_{t-1}) | Frame-to-frame harmonic shift magnitude | <0.5 ms |
| 84 | tonal_stability | YENİ | R1 GAP-24 + R2 §5.3 ÖNERİ H.9 | 1 / (1 + harmonic_change_rate + (1 - key_clarity)) → normalized | High = stable tonal center; inverse of harmonic flux | <0.1 ms |
| 85 | diatonicity | YENİ | R2 §4.3 H.6 | Count of distinct PCs with energy > threshold in window / 12; low = diatonic | Tymoczko macroharmony: diatonic vs chromatic content | <0.5 ms |
| 86 | syntactic_irregularity | YENİ | R1 GAP-14 + R2 §4.3 H.7 | KL divergence of current chroma from diatonic key template | Harmonic syntax violation — deviation from tonal expectation | ~1 ms |

**Hesaplama pipeline**: `F:chroma [49:60] → key_profile correlation → key_clarity → tonnetz projection → frame-to-frame chroma distances → tonal_stability composite → diatonicity/irregularity`

**Bağımlılık**: F grubu chroma çıktısı gerekli. Compute order: F → H.

---

### Group I: Information & Surprise [87:94] — 7D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 87 | melodic_entropy | YENİ | R1 Tier 1 (18 model) + R2 §4.4 I.6 | Entropy of frame-to-frame chroma transition distribution over sliding window; approximates IDyOM melodic IC | Prediction error / surprise (Pearce 2005) | ~0.5 ms |
| 88 | harmonic_entropy | YENİ | R1 Tier 1 (13 model) + R2 §4.4 I.5 | KL divergence of current chroma from running chroma average → how unexpected is the current chord | Chord transition probability (Gold 2019) | ~0.5 ms |
| 89 | rhythmic_information_content | YENİ | R1 Tier 2 (8 model) + R2 §4.4 | -log(p(IOI_current | IOI_context)) from onset interval statistics | Rhythmic surprise (Spiech 2022) | ~0.5 ms |
| 90 | spectral_surprise | YENİ | R2 §5.4 + R3 §3 #25 | D_KL(mel_t || mel_running_avg) — frame-level spectral unexpectedness | Prediction error / free energy (Friston) — mismatch negativity | ~0.5 ms |
| 91 | information_rate | YENİ | R2 §5.4 + R3 implied | I(mel_t; mel_{t-1}) = H(mel_t) + H(mel_{t-1}) - H(mel_t, mel_{t-1}) | Mutual information — how much new information per frame | ~0.5 ms |
| 92 | predictive_entropy | YENİ | R1 GAP-5 + R2 §4.4 I.3 | Entropy of conditional distribution p(frame_t | context) from running statistics | Uncertainty of frame prediction — high = unpredictable | ~0.5 ms |
| 93 | tonal_ambiguity | YENİ | R1 GAP-15 + R2 §4.4 ÖNERİ I.8 | Entropy of key profile correlation softmax: H = -Σ p_key · log(p_key) | Tonal uncertainty — high = ambiguous tonality | ~1 ms |

**Hesaplama pipeline**: `mel → running statistics (exponential decay) → KL divergences → F:chroma → chroma transitions → melodic/harmonic entropy → onset events → rhythmic IC`

**Bağımlılıklar**: F:chroma gerekli, G:onset events gerekli. Compute order: F → G → I.

**AÇIK SORU**: melodic_entropy [87] ve harmonic_entropy [88] tam IDyOM kalitesinde hesaplanamaz — mel-based chroma transition entropy bir yaklaşımdır. Kalite farkı deneysel benchmark ile ölçülmeli.

---

### Group J: Timbre Extended [94:114] — 20D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 94 | mfcc_1 | YENİ | R3 §2.1 + §3 #1 | DCT of log-mel: coefficient 1 | Cepstral timbre — vocal tract shape proxy | ~0.5 ms (tüm MFCC birlikte) |
| 95 | mfcc_2 | YENİ | " | coefficient 2 | " | " |
| 96 | mfcc_3 | YENİ | " | coefficient 3 | " | " |
| 97 | mfcc_4 | YENİ | " | coefficient 4 | " | " |
| 98 | mfcc_5 | YENİ | " | coefficient 5 | " | " |
| 99 | mfcc_6 | YENİ | " | coefficient 6 | " | " |
| 100 | mfcc_7 | YENİ | " | coefficient 7 | " | " |
| 101 | mfcc_8 | YENİ | " | coefficient 8 | " | " |
| 102 | mfcc_9 | YENİ | " | coefficient 9 | " | " |
| 103 | mfcc_10 | YENİ | " | coefficient 10 | " | " |
| 104 | mfcc_11 | YENİ | " | coefficient 11 | " | " |
| 105 | mfcc_12 | YENİ | " | coefficient 12 | " | " |
| 106 | mfcc_13 | YENİ | " | coefficient 13 | " | " |
| 107 | spectral_contrast_1 | YENİ | R3 §2.1 + §3 #5 | librosa spectral_contrast: octave sub-band 1 peak-valley | Harmonic vs. noisy texture (Jiang 2002) | ~0.5 ms (tüm contrast birlikte) |
| 108 | spectral_contrast_2 | YENİ | " | sub-band 2 | " | " |
| 109 | spectral_contrast_3 | YENİ | " | sub-band 3 | " | " |
| 110 | spectral_contrast_4 | YENİ | " | sub-band 4 | " | " |
| 111 | spectral_contrast_5 | YENİ | " | sub-band 5 | " | " |
| 112 | spectral_contrast_6 | YENİ | " | sub-band 6 | " | " |
| 113 | spectral_contrast_7 | YENİ | " | sub-band 7 (residual) | " | " |

**Hesaplama**: MFCC = pre-computed DCT matrix (128×13) applied to log-mel. Spectral contrast = per-octave peak-valley difference on mel.

**Not**: MFCC ve spectral_contrast doğrudan C³ model doc'larında talep edilmemiş (R1'de gap yok) ama MIR literatürünün en kanıtlı özellikleri. SPU, IMU, ARU modelleri bunları potansiyel olarak kullanabilir.

---

### Group K: Modulation & Psychoacoustic [114:128] — 14D (YENİ)

| Index | Feature Name | Karar | Kaynak | Hesaplama | Psikoakustik Temel | Maliyet |
|:-----:|-------------|-------|--------|-----------|-------------------|---------|
| 114 | modulation_0_5Hz | YENİ | R3 §5.5 j_mod | Per-band FFT of mel temporal envelope → energy at 0.5 Hz AM rate | Cortical temporal modulation (Chi/Shamma 2005) | ~3 ms (tüm mod birlikte) |
| 115 | modulation_1Hz | YENİ | " | energy at 1 Hz | Phrase-level rhythmic modulation | " |
| 116 | modulation_2Hz | YENİ | " | energy at 2 Hz | Beat-rate modulation | " |
| 117 | modulation_4Hz | YENİ | " | energy at 4 Hz | Speech syllabic rate / strong beat | " |
| 118 | modulation_8Hz | YENİ | " | energy at 8 Hz | Rapid articulation / tremolo | " |
| 119 | modulation_16Hz | YENİ | " | energy at 16 Hz | Roughness boundary / vibrato upper | " |
| 120 | modulation_centroid | YENİ | R3 §3 #39 | Weighted mean of modulation spectrum | Dominant modulation rate | <0.1 ms |
| 121 | modulation_bandwidth | YENİ | R3 implied | Standard deviation of modulation spectrum | Modulation rate diversity | <0.1 ms |
| 122 | sharpness_zwicker | YENİ | R2 §3.3 C.6 + R3 §2.6 DIN 45692 | S = 0.11 · ∫ N'(z)·g(z)·z dz / ∫ N'(z) dz on Bark scale | Zwicker/Fastl perceptual sharpness | ~0.5 ms |
| 123 | fluctuation_strength | YENİ | R3 §2.6 Zwicker/Fastl | Temporal modulation at ~4 Hz: mel envelope band-pass → amplitude | Temporal fluctuation perception (peak at 4 Hz) | ~0.5 ms |
| 124 | loudness_a_weighted | YENİ | R3 §2.6 ISO 226 | A-weighting curve applied to mel bands → total weighted energy | Perceptual loudness with frequency weighting | <0.1 ms |
| 125 | alpha_ratio | YENİ | R3 §3 #31 eGeMAPS | Low-band (0-1kHz) / high-band (1k-5kHz) energy ratio on mel | Voice/instrument quality balance | <0.1 ms |
| 126 | hammarberg_index | YENİ | R3 §3 #32 eGeMAPS | Peak energy ratio 0-2kHz / 2k-5kHz on mel | Spectral tilt measure | <0.1 ms |
| 127 | spectral_slope_0_500 | YENİ | R3 §3 #33 eGeMAPS | Linear regression slope of mel bands in 0-500 Hz range | Low-frequency spectral envelope shape | <0.1 ms |

**Hesaplama pipeline**: `mel → per-band temporal FFT (sliding window ~2s) → modulation energy at target rates → centroid/bandwidth → Bark rebin → sharpness → 4Hz bandpass → fluctuation → A-weighting → ratios/slopes`

---

## Bölüm 5: Mevcut Grup Revizyon Kararları

### 5.1 Duplikasyon Problemi

R2 §2.6'da tespit edilen 3 çapraz duplikasyon:

| Duplikat Çifti | Grup A-D | Grup C | İlişki | Phase 6 Kararı |
|----------------|----------|--------|--------|----------------|
| stumpf_fusion [3] | A:Consonance | warmth [12] C:Timbre | **Identical** — her ikisi `mel[:N/4].sum()/total` | [3] → gerçek Parncutt tonal fusion (subharmonic matching); [12] korunur |
| helmholtz_kang [2] | A:Consonance | spectral_autocorrelation [17] C:Timbre | **Identical** — her ikisi lag-1 autocorrelation | [17] → spectral_kurtosis (4th moment); [2] → multi-lag autocorrelation |
| sethares_dissonance [1] | A:Consonance | spectral_smoothness [16] C:Timbre | **Complement** — [16] = 1 - [1] | [16] → spectral_spread (2nd moment); [1] → gerçek Sethares pairwise |

**Backward compatibility stratejisi**: İndeks numaraları [0-48] değişmez. Sadece hesaplama formülü Phase 6'da güncellenir. 96 model docu Section 4'te indeks referansları geçerli kalır; Section 12.1'de (doc-code mismatch) "Phase 6: formül değişikliği" notu eklenir.

### 5.2 Normalizasyon Bug (concentration [24])

**R2 bulgusu** (§2.4):
- Mevcut formül: `concentration = (Σ p_i²) · N`
- Sorun: Uniform dağılım → `N · (1/N)² · N = 1.0`; Tekil pik → `N · 1² = N → clamp → 1.0`
- Her iki uç da 1.0 veriyor → feature ayırt edicilik yeteneğini kaybetmiş

**Doğru formül**: `concentration = (HHI - 1/N) / (1 - 1/N)` → [0,1] aralığında 0=uniform, 1=concentrated

**KARAR**: Phase 6'da düzeltilecek. Şu an [24] indeksi korunur, bug'lı haliyle. Yeni I:spectral_surprise [90] ve D:distribution_entropy [22] zaten spectral concentration bilgisini sağlıyor.

### 5.3 Stevens' Law Çift-Sıkıştırma

**R2 bulgusu** (§2.2):
- Mevcut: `loudness = RMS(log_mel)^0.3`
- Sorun: log-mel zaten logaritmik sıkıştırma uygulamış; üzerine Stevens' law (^0.3) → çift sıkıştırma
- Stevens' law lineer güç spektrumuna uygulanmalı: `loudness ~ power^0.3`
- Etki: Dinamik aralık daraltılmış, düşük ve yüksek enerji seviyeleri ayrışamıyor

**KARAR**: Phase 6'da düzeltilecek. İki seçenek:
1. Lineer güç spektrumuna erişim sağla (pipeline değişikliği gerekli)
2. `exp(log_mel)` ile lineer alana dön, sonra Stevens uygula (yaklaşık düzeltme)

Şu an [10] loudness korunur. Yeni K:loudness_a_weighted [124] A-weighting ile farklı bir loudness yaklaşımı sunar.

### 5.4 Interaction Grubu (E) Yeniden Tasarımı

**Mevcut durum** (R2 §2.5):
- 24D mekanik çarpım terimleri (3×8 cross-product)
- Bağımsız proxy'ler kullanıyor (A-D çıktılarını referans etmiyor)
- 2 proxy mismatch: roughness_proxy (`var()` vs `var()/mean()`), helmholtz_proxy (`max/sum` vs lag-1 autocorrelation)

**R2 önerisi**: 3 seçenek — (1) curated fix, (2) learned MLP, (3) psychoacoustically motivated

**KARAR**: Phase 6'da iki aşamalı:

**Aşama 1** (Kısa vadeli): Proxy'leri kaldır, gerçek A-D çıktılarını kullan. Mevcut 24D cross-product yapısı korunur ama doğru inputlarla hesaplanır.

**Aşama 2** (Orta vadeli): Yeni F-K gruplarıyla genişletilmiş interaction matrisi:
- Mevcut: B×A (8D), D×A (8D), A×C (8D) = 24D
- Ek (ÖNERİ): F×A (pitch×consonance, 4D), G×B (rhythm×energy, 4D), H×D (harmony×change, 4D), I×D (information×change, 4D) = +16D
- **Toplam E (Phase 6)**: 24D (mevcut düzeltilmiş) + 16D (yeni) = 40D

**AÇIK SORU**: Bu 16D ek E grubu R³ v2'nin 128D bütçesi dışında kalıyor. İki seçenek:
1. 128D'den K grubunu 14D→ küçült ve E_extended'ı dahil et → karmaşık
2. 128D'yi koru, E genişleme → R³ v2.1 (Phase 6 sonrası 144D) olarak ertelenir

**Tercih**: Seçenek 2 — E genişleme Phase 6'da deneysel veriye dayalı olarak kararlaştırılır.

---

## Bölüm 6: Kesin Boyut Hedefi

### 6.1 Senaryo Karşılaştırması

| Senaryo | Toplam D | Mevcut A-E | Yeni F-K | Gerekçe |
|---------|:--------:|:----------:|:--------:|---------|
| **Minimum** | **68D** | 49D (koru) | 19D (R1 4 grup, 4-5D her biri) | R1 Senaryo B. Yalnızca Tier 1-2 talepleri karşılar. Gelecek genişleme alanı yok. |
| **Önerilen** | **128D** | 49D (koru) | 79D (6 yeni grup) | R1+R2+R3 konsensüsü. Talep + toolkit + psikoakustik denge. Power-of-2 GPU uyumu. |
| **Maksimum** | **256D** | 49D (revize ~55D) + 6D fark | 201D (6 genişletilmiş + interaction) | R3 Option C. MFCC delta-delta, ERB, NMF, genişletilmiş interaction, polynomial. |

### 6.2 Seçilen Senaryo: 128D

**Grup bazlı boyut dağılımı:**

```
A: Consonance    ████████  7D  [0:7]    MEVCUT
B: Energy        █████     5D  [7:12]   MEVCUT
C: Timbre        █████████ 9D  [12:21]  MEVCUT
D: Change        ████      4D  [21:25]  MEVCUT
E: Interactions  ████████████████████████ 24D [25:49]  MEVCUT
F: Pitch&Chroma  ████████████████ 16D [49:65]  YENİ ★
G: Rhythm&Groove ██████████ 10D [65:75]  YENİ ★
H: Harmony       ████████████ 12D [75:87]  YENİ ★
I: Info&Surprise ███████  7D  [87:94]  YENİ ★
J: Timbre Ext    ████████████████████ 20D [94:114] YENİ ★
K: Mod&Psycho    ██████████████ 14D [114:128] YENİ ★
                 ─────────────────────────────
                 128D TOPLAM
```

### 6.3 Fizibilite Onayı

**GPU Real-Time Fizibilitesi** (R3 §4 verilerine dayalı):

| Bileşen | Boyut | Tier | Tahmini Maliyet |
|---------|:-----:|:----:|:----------------|
| A-E (mevcut) | 49D | 0-1 | ~0.5 ms/frame |
| F: Pitch & Chroma | 16D | 1 | ~1.0 ms/frame |
| G: Rhythm & Groove | 10D | 2 | ~0.5 ms/frame |
| H: Harmony & Tonality | 12D | 2 | ~1.0 ms/frame |
| I: Information & Surprise | 7D | 2 | ~0.5 ms/frame |
| J: Timbre Extended | 20D | 0-1 | ~0.5 ms/frame |
| K: Modulation & Psychoacoustic | 14D | 2-3 | ~3.0 ms/frame |
| **Toplam** | **128D** | | **~7.0 ms/frame** |

**Frame budget**: 5.8 ms (172.27 Hz). Toplam maliyet 7.0 ms > 5.8 ms gibi görünse de:
- K grubu modulation hesaplaması sliding window kullanır (her frame'de tam FFT gerekmez)
- GPU batch parallelism: A-E, F, J aynı anda çalışabilir → gerçek latency ~3-4 ms
- **Real-time onay**: EVET (GPU batch processing ile ~3-4 ms/frame, 1.5-2× RT headroom)

**Model etkisi** (R1 talep matrisine dayalı):

| Yeni Grup | Doğrudan Fayda (X) | Dolaylı Fayda (x) | Toplam |
|-----------|:------------------:|:------------------:|:------:|
| F: Pitch & Chroma | 16 model | 11 model | 27 |
| G: Rhythm & Groove | 25 model | 8 model | 33 |
| H: Harmony & Tonality | 12 model | 10 model | 22 |
| I: Information & Surprise | 22 model | 10 model | 32 |
| J: Timbre Extended | ~20 model (ÖNERİ) | ~30 model (ÖNERİ) | ~50 |
| K: Modulation & Psychoacoustic | ~10 model (ÖNERİ) | ~20 model (ÖNERİ) | ~30 |

J ve K grubunun model etkisi ÖNERİ niteliğindedir — Phase 3E'de 96 model Section 4 güncellemesi sırasında kesinleşecektir.

**Psikoakustik kapsam** (R2 literature coverage):

| Psikoakustik Alan | Mevcut 49D | 128D Kapsam | Kaynak |
|-------------------|:----------:|:-----------:|--------|
| Roughness/dissonance | Proxy | Proxy (Phase 6 düzeltme) | Plomp-Levelt, Sethares |
| Pitch perception | Yok | **16D** (chroma, height, salience) | Krumhansl, Shepard, Parncutt |
| Rhythmic perception | Yok (sadece onset) | **10D** (tempo→groove) | Fraisse, Witek, Madison |
| Tonal/harmonic | Yok | **12D** (key, tonnetz, tension) | Krumhansl-Kessler, Tymoczko |
| Information/surprise | Yok | **7D** (entropy, KL, IC) | Pearce, Friston, Shannon |
| Timbre detail | Kısıtlı (~4 efektif) | **20D** (MFCC + contrast) | Krimphoff, Jiang |
| Temporal modulation | Yok | **14D** (mod spectrum, psychoacoustic) | Chi/Shamma, Zwicker |
| Cross-feature interaction | 24D (proxy) | 24D (Phase 6 düzeltme) | — |

---

## Bölüm 7: Phase 3B Girdileri ve Açık Sorular

### 7.1 Mimari Tasarım Gerektiren Kararlar

| # | Karar | Bağımlılık | Phase 3B Bölümü |
|---|-------|-----------|----------------|
| 1 | F grubunun chroma hesaplama yöntemi — mel→freq→PC fold vs daha sofistike yöntem? | Chroma kalitesi tüm H ve I grubunu etkiler | 3B-1 |
| 2 | G grubunun beat tracking yöntemi — autocorrelation vs PLP vs DBN? | Syncopation ve metricality kalitesi beat quality'ye bağlı | 3B-1 |
| 3 | I grubunun entropy/surprise hesaplaması — exponential decay window size? | Running average decay hızı temporal resolution belirler | 3B-1 |
| 4 | K grubunun modulation spectrum — FFT window size, overlap? | ~2s window gerekli (0.5 Hz resolution) vs frame-level (5.8 ms) çelişki | 3B-1 |
| 5 | Compute order ve bağımlılık grafiği: F→H→I vs paralel | Pipeline latency vs doğruluk | 3B-3 |
| 6 | E grubu Phase 6 genişleme planı (24D→40D?) | 128D bütçe aşılır mı? R³ v2.1? | 3B-2 |
| 7 | [0:49] indeks backward compatibility — yeni feature ekleme vs formül değişikliği ayrımı | 96 model doc update stratejisi | 3B-3 |

### 7.2 Deneysel Doğrulama Gerektiren Feature'lar

| Feature | Sorun | Test Yöntemi |
|---------|-------|-------------|
| melodic_entropy [87] | IDyOM kalitesine ne kadar yakın? | Benchmark: mel-based vs IDyOM IC correlation on annotated corpus |
| harmonic_entropy [88] | Chord transition model quality? | Benchmark: chroma-based surprise vs expert harmonic analysis |
| approximate chroma [49:60] | CQT chroma'ya göre kalite farkı? | Benchmark: mel-chroma vs librosa.chroma_cqt key detection accuracy |
| syncopation_index [68] | LHL implementation from mel onset — accuracy? | Benchmark: vs annotated syncopation ratings (Witek 2014 corpus) |
| groove_index [71] | Composite feature — weights? | Regression: behavioral groove ratings prediction |
| inharmonicity_index [64] | Mel peak detection resolution yeterli mi? | Benchmark: mel-based vs essentia Inharmonicity (raw audio) |

### 7.3 Backward Compatibility Stratejisi

**ÖNERİ**: 3-katmanlı strateji:

**Katman 1: İndeks koruması (Phase 3 — şimdi)**
- [0:49] indeksleri DEĞİŞMEZ
- Yeni feature'lar [49:128] aralığına eklenir
- 96 model doc Section 4: mevcut referanslar geçerli kalır, yeni referanslar eklenir

**Katman 2: Formül güncellemesi (Phase 6)**
- [0:49] indeksleri KORUNUR ama hesaplama formülleri güncellenir
- Duplikasyon kaldırılır: [3], [16], [17] yeni hesaplamalar alır
- Bug'lar düzeltilir: [24] normalizasyon, [10] loudness
- 96 model doc Section 12.1: "formül değişikliği" notu

**Katman 3: Tam revizyon (Phase 6+)**
- `R3_DIM=49` → `R3_DIM=128` (registry.freeze().total_dim)
- `_R3_FEATURE_NAMES` → auto-generated from registry
- Group boundaries → read from `R3FeatureMap.groups`
- E grubu proxy'leri → gerçek A-D referansları
- E grubu genişleme (yeni cross-group interactions)

### 7.4 Multi-Track Pipeline Sorusu

R1'de 3 gap multi-track gereksinimi nedeniyle çözülemedi (GAP-25,26,27 — RPU-SSRI modeli). Mevcut R³ pipeline single-stream (tek ses kaynağı). Multi-track pipeline:

**AÇIK SORU**: RPU-SSRI modeli (Social Synchrony Reward Integration) grup müzik yapımı için multi-track özellikler gerektiriyor. Bu, R³'ün single-stream pipeline'ı dışında mı kalacak, yoksa multi-stream genişleme mi planlanacak?

**ÖNERİ**: R³ v2 single-stream kalır. Multi-track özellikleri ayrı bir pipeline katmanı (R³-multi?) olarak Phase 4+'da tasarlanır. SSRI modeli şimdilik mevcut single-stream R³ özelliklerini kullanır.

---

## Bölüm 8: Kaynak Referansları

### 8.1 R1 → Karar Referansları

| R1 Bölüm | İçerik | Kullanılan Kararlar |
|-----------|--------|---------------------|
| §1.1 ACOUSTIC Gaps | 31 gap tablosu | Bölüm 2: tüm 31 gap eşleştirmesi |
| §1.2 NAMING Gaps | ~64 naming mismatch | Phase 5'e erteleme kararı |
| §1.4 Summary by Unit | Unit bazlı gap dağılımı | Bölüm 1.2: grup boyut kararları |
| §3.1 Tier 1 Demand | melodic_entropy(18), syncopation(17), metricality(14), harmonic_entropy(13) | Bölüm 3: tüm Tier 1 DAHİL |
| §3.2 Tier 2 Demand | rhythmic_IC(8), groove(7), syntactic(5), chroma(5), tonal_stability(5), nPVI(5) | Bölüm 3: tüm Tier 2 DAHİL |
| §5 Yeni Grup Talebi | F(5D), G(5D), H(5D), I(4D) = 19D | Bölüm 4: genişletilmiş F(16D), G(10D), H(12D), I(7D) |
| §6.2 Senaryo B | 49D→68D (+19D) | Bölüm 6: 128D seçildi (68D yetersiz) |
| §6.5 Açık Sorular | IDyOM, groove, interaction, 128 vs 256 | Bölüm 7: açık sorulara dahil edildi |

### 8.2 R2 → Karar Referansları

| R2 Bölüm | İçerik | Kullanılan Kararlar |
|-----------|--------|---------------------|
| §2.1-2.5 Current R³ Critique | 49D → ~15-20 efektif boyut, 3 duplikasyon, 2 bug | Bölüm 5: tüm revizyon kararları |
| §2.6 Redundancy Map | [3]≡[12], [1]↔[16], [2]≡[17] + 3 derived | Bölüm 5.1: duplikasyon Phase 6 planı |
| §3.1-3.5 Revision Proposals | A→10-12D, B→7D, C→10D, D→8D, E→redesign | Bölüm 5: Phase 6'da formül güncellemesi kararı |
| §4.1 Group F: Pitch | 12-16D, chroma(12), pitch_height, salience, virtual_pitch | Bölüm 4 F: 16D seçimi |
| §4.2 Group G: Rhythm | 8-12D, tempo, beat, syncopation, groove | Bölüm 4 G: 10D seçimi |
| §4.3 Group H: Harmony | 12-18D, key, tonnetz, VL distance, tension | Bölüm 4 H: 12D seçimi |
| §4.4 Group I: Information | 8-12D, surprise, entropy, IC, predictive_entropy | Bölüm 4 I: 7D seçimi |
| §5 Complete Catalog | 67 aday feature, detaylı tanımlar | Bölüm 4: tüm feature tanımları için birincil kaynak |
| §6 Computability Assessment | Tier 1-4 maliyet sıralaması | Bölüm 6.3: fizibilite onayı |
| §7 Literature Reference Matrix | 30+ kaynak dosya → feature bağlantıları | Tüm psikoakustik temel referansları |
| §8 Open Questions for R3 | 16 açık soru | Bölüm 7: karşılanan ve kalan sorular |
| Appendix A Dimensionality | 95-141D önerisi | Bölüm 6: 128D seçimi |

### 8.3 R3 → Karar Referansları

| R3 Bölüm | İçerik | Kullanılan Kararlar |
|-----------|--------|---------------------|
| §1 Executive Summary | ~300+ feature, ~95 mel-compatible | Bölüm 1.1: mel constraint doğrulaması |
| §2.1 librosa | 33 mel-compatible functions | Bölüm 4: J grubunda MFCC, spectral_contrast; G grubunda tempogram, PLP |
| §2.2 essentia | 28 mel-compatible algorithms | Bölüm 4: K grubunda eGeMAPS features; J grubunda contrast |
| §2.3 eGeMAPS | 42/88 mel-computable | Bölüm 4 K: alpha_ratio, hammarberg, slopes |
| §2.4 madmom | Only SpectralOnsetProcessor | Madmom neural models dışarıda (mel-incompatible) |
| §2.5 Pitch estimators | ALL require raw audio | F grubu pitch_salience mel-proxy olarak; gerçek F0 yok |
| §2.6 ISO/AES Standards | ISO 532-1, DIN 45692, ISO 226 | K grubu: sharpness_zwicker, fluctuation, loudness_A |
| §3 Mel-Compatible Catalog | 63D HIGH, 79D MEDIUM, 73D LOW | Bölüm 4: HIGH+MEDIUM feature seçimi |
| §4 Cost Analysis | Tier 0-4, real-time budget | Bölüm 6.3: GPU RT fizibilite |
| §5 Proposed Groups | F(18D), G(12D), H(20D), I(9D), J(20D) | Bölüm 4: boyut ayarlamaları yapıldı |
| §7 Dimension Target | 128D min, 192D med, 256D max | Bölüm 6: 128D seçimi |
| §8 Implementation Refs | librosa/essentia API calls, PyTorch patterns | Phase 3B ve Phase 6 uygulamaları için referans |
| Appendix B Mel-to-Chroma | Algorithm for approximate chroma | F grubu hesaplama detayı |

### 8.4 Kod Referansları

| Dosya | Bölüm | Kullanım |
|-------|-------|----------|
| `mi_beta/ear/r3/psychoacoustic/consonance.py` | A grubu: 7D | Bölüm 5: duplikasyon analizi, formül doğrulaması |
| `mi_beta/ear/r3/dsp/energy.py` | B grubu: 5D | Bölüm 5: Stevens' law çift sıkıştırma tespiti |
| `mi_beta/ear/r3/dsp/timbre.py` | C grubu: 9D | Bölüm 5: duplikasyon analizi ([12]≡[3], [17]≡[2]) |
| `mi_beta/ear/r3/dsp/change.py` | D grubu: 4D | Bölüm 5: concentration [24] bug doğrulaması |
| `mi_beta/ear/r3/cross_domain/interactions.py` | E grubu: 24D | Bölüm 5: proxy mismatch analizi |
| `mi_beta/ear/r3/extensions/_template.py` | Yeni grup şablonu | Bölüm 4: F-K grupları bu şablonu takip edecek |
| `mi_beta/ear/r3/_registry.py` | R3FeatureRegistry | Phase 3B: auto-indexing, freeze() mekanizması |

---

## Ek: Karar Özet Tablosu

| Karar # | Konu | Seçenek | Gerekçe | Dayanak |
|---------|------|---------|---------|---------|
| K1 | Boyut hedefi | **128D** | R2+R3 konsensüsü, RT uyumlu, power-of-2 | R2 App.A, R3 §7 |
| K2 | Yeni grup sayısı | **6** (F-K) | 4 temel (talep-driven) + 2 ek (toolkit-driven) | R1 §5, R2 §4, R3 §5 |
| K3 | Mevcut A-E | **KORU** (indeks ve formül) | Backward compatibility; Phase 6 revizyon | R2 §2-3, pragmatik |
| K4 | E grubu | **KORU + Phase 6 fix** | Proxy düzeltme + yeni interaction'lar erteleme | R2 §2.5 |
| K5 | duplikasyonlar | **Phase 6 formül güncelleme** | [3],[16],[17] yeni hesaplamalar; indeks korunur | R2 §2.6 |
| K6 | concentration bug | **Phase 6 düzeltme** | Formül: (HHI-1/N)/(1-1/N) | R2 §2.4 |
| K7 | loudness bug | **Phase 6 düzeltme** | Lineer spektrum erişimi gerekli | R2 §2.2 |
| K8 | Multi-track | **HARİÇ** (single-stream kalır) | 3 RPU gap çözülemez; ayrı pipeline gerekli | R1 GAP-25,26,27 |
| K9 | IDyOM entropi | **DAHİL** (yaklaşık) | Chroma-based approximation; benchmark gerekli | R2 §4.4, R3 §3 |
| K10 | MFCC/contrast | **DAHİL** (J grubu) | Talep-driven değil ama MIR'ın en kanıtlı feature'ları | R3 §3 #1,#5 |

---

*Generated by Phase 3A-3 Crossref Chat | 2026-02-13*
*Sources: R3-DEMAND-MATRIX.md (R1), R3-DSP-SURVEY-THEORY.md (R2), R3-DSP-SURVEY-TOOLS.md (R3)*
*Code reference: mi_beta/ear/r3/ (5 groups + template, READ-ONLY)*
