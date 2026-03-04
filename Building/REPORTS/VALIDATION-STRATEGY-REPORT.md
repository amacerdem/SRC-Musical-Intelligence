# MI Validation Strategy Report

**Date:** 2026-03-04
**Scope:** V1–V7 Validation Modules — Literature Comparison Strategy
**Prerequisite:** F-Test Analysis Report (ALL PASS, 99.3%)
**Status:** PRE-VALIDATION PLANNING

---

## 1. Validation Philosophy

### Temel İlke: MI Sistemi Farklı Sonuç Üretebilir — Bu Hata Anlamına Gelmez

Validasyon testleri, MI sisteminin çıktılarını yayınlanmış nörobilim araştırmalarıyla karşılaştırır. Ancak kritik bir fark var:

1. **MI, insan deneylerinden farklı bir yaklaşım kullanır** — Beyin görüntüleme (fMRI/EEG) yaklaşık 1-2Hz'de örnekler, MI 172.27 Hz'de hesaplar
2. **MI deterministiktir** — İnsan deneyleri stokastiktir (bireysel farklılıklar, dikkat, yorgunluk)
3. **MI, tasarımsal olarak daha hassas olabilir** — 131 boyutlu belief space, insan öz-raporlarından çok daha zengin
4. **Bazı MI çıktıları literatürden DAHA İYİ olabilir** — Bu bir sorun değil, bir özellik

### Karşılaştırma Stratejisi: 3 Katmanlı Değerlendirme

```
Katman 1: YÖN DOĞRULUĞU (Direction Correctness)
  → MI efekt yönü, yayınlanan yönle aynı mı?
  → Örn: Levodopa reward ↑ → MI reward ↑ ✓
  → EN ÖNEMLİ: Yön doğruysa, büyüklük farkı tolere edilir

Katman 2: SIRA KORUMASI (Rank Preservation)
  → MI sıralaması, literatür sıralamasıyla uyumlu mu?
  → Örn: K-K tonal profil sıralaması korunuyor mu? (ρ > 0.6)
  → ÖNEMLİ: Tam eşleşme beklenmez, sıra korelasyonu yeterli

Katman 3: BÜYÜKLÜK KARŞILAŞTIRMASI (Magnitude Comparison)
  → MI efekt büyüklüğü, yayınlanan değerlere yakın mı?
  → DİKKATLİ: MI deterministik, insan verileri değil
  → MI daha büyük/küçük efekt gösterebilir — her iki yönde de geçerli
```

---

## 2. Validation Module Detaylı Stratejisi

### V1: Farmakoloji — Nörokimyasal Validasyon

**Referanslar:**
- Ferreri et al. 2019 (PNAS): Levodopa/Risperidone + DA + müzik ödülü (N=27)
- Mallik et al. 2017 (Neuropsychopharmacology): Naltrexone + OPI + müzik duygusu (N=15)
- Laeng et al. 2021 (Frontiers): Naltrexone + OPI + arousal/valence ayrışması (N=30)

**MI Simülasyon Yöntemi:**
- DA gain: Levodopa=1.5×, Risperidone=0.3×, Placebo=1.0×
- OPI gain: Naltrexone=0.1×, Placebo=1.0×

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Literatür Beklentisi | Yorum |
|------|--------|-----------|---------------------|-------|
| Levodopa → reward ↑ | Yön | direction == "increase" | d = +0.84 | Yön doğruluğu yeterli |
| Risperidone → reward ↓ | Yön | direction == "decrease" | d = -0.67 | Yön doğruluğu yeterli |
| Levo > Placebo > Risp | Sıra | Strict inequality | 3-way ordering | Sıra koruması |
| DA channel modulated | Yön | Levo DA↑, Risp DA↓ | Nörokimyasal etki | Yön doğruluğu |
| Cohen's d sign | Büyüklük | d yönü eşleşir | d > 0 levo, d < 0 risp | İŞARET, büyüklük DEĞİL |
| Naltrexone → emotion ↓ | Yön | direction == "decrease" | d = -0.53 | Yön doğruluğu |
| Naltrexone → arousal ↓ | Yön | direction == "decrease" | d = -0.45 | Yön doğruluğu |
| Naltrexone valence korunur | Büyüklük | \|Δ%\| < 15% | d = 0.05 (neredeyse sıfır) | MI %15 tolerans |
| Arousal-valence ayrışması | Sıra | \|Δarousal\| > \|Δvalence\| | OPI selektif arousal etkisi | Ayrışma yönü |

**DİKKAT NOKTALARI:**
- MI gain parametreleri (1.5×, 0.3×, 0.1×) insan dozlarının DOĞRUSAL yaklaşımıdır
- Gerçekte nörokimyasal etkiler nonlineerdir
- MI'ın daha güçlü veya zayıf efekt göstermesi BEKLENEN bir sonuçtur
- KRİTİK: Efekt YÖNÜ doğru olmalı. Büyüklük farkları kabul edilebilir.

**Olası Senaryolar:**
1. ✅ Yön doğru, büyüklük benzer → Mükemmel validasyon
2. ✅ Yön doğru, MI daha güçlü efekt → MI hassasiyeti yüksek (beklenen)
3. ✅ Yön doğru, MI daha zayıf efekt → MI konservatif (kabul edilir)
4. ⚠️ Yön ters → Model sorunu — mekanizma incelenmeli
5. ⚠️ Sıfır efekt → Gain parametresi yetersiz veya mekanizma bağımsız

---

### V2: IDyOM — Müzik Tahmini Benchmark

**Referans:** IDyOM (Information Dynamics of Music) — Pearce 2005, 2018

**MI Karşılaştırması:** MI Prediction Error (PE) vs IDyOM Information Content (IC)

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Literatür Bağlamı | Yorum |
|------|--------|-----------|-------------------|-------|
| Mean Pearson r > 0.3 | Büyüklük | r > 0.3 | IDyOM: symbolic, MI: audio | Farklı modalite → düşük threshold |
| >50% melodi anlamlı | Büyüklük | proportion > 0.5 | Per-melody p < 0.05 | Çoğunluk anlamlı |
| Spearman ρ > 0.25 | Sıra | ρ > 0.25 | Rank agreement | Sıra koruması |

**DİKKAT NOKTALARI:**
- IDyOM sembolik (MIDI), MI ses tabanlı → doğrudan karşılaştırma sınırlı
- Sentez artefaktları (MIDI→audio) korelasyonu düşürebilir
- MI, IDyOM'dan FARKLI şeyleri tahmin edebilir (örn: timbral surprise vs pitch surprise)
- r > 0.3 düşük görünebilir ama FARKLI MODALİTELER arası karşılaştırma için makul

**MI AVANTAJI:** MI çok boyutlu (131D), IDyOM tek boyutlu (IC). MI, pitch + timbre + rhythm surprise'ı ayrı ayrı hesaplar.

**Olası Senaryolar:**
1. ✅ r > 0.3, çoğunluk anlamlı → Yakınsak geçerlilik kanıtlandı
2. ✅ r = 0.15-0.30 → Kısmen yakınsak (modalite farkı açıklar)
3. ⚠️ r < 0.10 → MI PE ve IDyOM IC farklı yapıları ölçüyor olabilir
4. ✅ r > 0.50 → MI, IDyOM'dan daha iyi performans gösterebilir

---

### V3: Krumhansl — Tonal Hiyerarşi

**Referans:** Krumhansl & Kessler 1982 — Probe-tone ratings (Psychological Review)

**MI Karşılaştırması:** MI tonal profil (12 PC) vs K-K yayınlanan profiller

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Literatür Değeri | Yorum |
|------|--------|-----------|-----------------|-------|
| Major profil r > 0.7 | Büyüklük | Pearson r > 0.7 | K-K major profil | Yüksek threshold — temel test |
| Minor profil r > 0.7 | Büyüklük | Pearson r > 0.7 | K-K minor profil | Yüksek threshold |
| Tonik en yüksek | Sıra | max_idx == 0 OR >90% max | C en yüksek | Tonal merkez |
| Diyatonik > kromatik | Yön | diatonic_mean > chromatic_mean | Scale > non-scale | Yön doğruluğu |
| Spearman ρ > 0.6 | Sıra | ρ > 0.6 | Rank order | Sıra koruması |

**DİKKAT NOKTALARI:**
- K-K profilleri BEHAVIORAL (davranışsal) verilerdir — insan dinleyicilerin "uygunluk" derecelendirmesi
- MI profili HESAPLAMASAL — neural-inspired pitch processing çıktısı
- MI, BCH consonance hierarchy + pitch chroma üzerinden hesaplar
- Davranışsal "uygunluk" ile hesaplamalı "tonal belirginlik" farklı şeylerdir

**MI AVANTAJI:** MI frame-by-frame hesaplar (172Hz), K-K tek bir ortalama puandır.

**Olası Senaryolar:**
1. ✅ r > 0.7, tonik en yüksek → Mükemmel (tonal hiyerarşi validated)
2. ✅ r = 0.5-0.7, sıralama korunur → İyi (farklı ölçüm metodolojisi)
3. ⚠️ r < 0.5 ama diyatonik > kromatik → Kısmen geçerli (daha kaba ayrışma)
4. ❌ r < 0.3, tonik en yüksek değil → Tonal işleme sorunu

---

### V4: DEAM — Sürekli Duygu Validasyonu

**Referans:** DEAM dataset — 1,802 şarkı, 2Hz sürekli valence/arousal (Aljanaki et al.)

**MI Karşılaştırması:** MI Ψ³ affect (valence/arousal) vs insan derecelendirmeleri

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Literatür Bağlamı | Yorum |
|------|--------|-----------|-------------------|-------|
| Arousal r > 0.3 | Büyüklük | Mean per-song r > 0.3 | İnsan agreement ~0.4-0.6 | MI < insan arası korelasyon |
| Valence r > 0.2 | Büyüklük | Mean per-song r > 0.2 | Valence daha subjektif | Düşük threshold |
| >30% arousal anlamlı | Büyüklük | proportion > 0.3 | Per-song p < 0.05 | Çoğunluk anlamlı |

**DİKKAT NOKTALARI:**
- İnsan arası korelasyon (inter-rater) arousal için ~0.4-0.6 — MI bu TAVANın altında olacak
- Valence çok subjektif — aynı müziğe farklı insanlar farklı valence atayabilir
- DEAM 2Hz, MI 172Hz → 86× downsampling gerekli (alignment.py)
- MI "perceived emotion" değil, "computed affect" ölçer

**MI AVANTAJI:**
- MI hem düşük seviye (arousal: loudness, onset density) hem yüksek seviye (valence: consonance, mode) kullanır
- MI deterministic: aynı şarkı her zaman aynı sonuç
- MI 131D → valence/arousal sadece 2D özet

**Olası Senaryolar:**
1. ✅ Arousal r > 0.3, valence r > 0.2 → Sistem duygu modellemeyi başarıyor
2. ✅ Arousal r > 0.4, valence r < 0.2 → Arousal güçlü, valence zayıf (beklenen)
3. ⚠️ Arousal r < 0.2 → Arousal çıkarımı sorunlu
4. ✅ Her ikisi > 0.4 → İnsan-arası korelasyona yakın (mükemmel)

---

### V5: EEG Encoding — Nöral Kodlama Modelleri

**Referans:** NMED-T dataset — 20 denek, 128-kanal EEG, doğal müzik (Losorelli et al.)

**MI Karşılaştırması:** MI özellikleri EEG yanıtını ne kadar iyi tahmin ediyor?

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Benchmark | Yorum |
|------|--------|-----------|-----------|-------|
| MI full > envelope | Sıra | full_R² > envelope_R² | Acoustic envelope baseline | MI > basit zarf |
| C³ ek varyans | Sıra | full_R² > r3_R² | R³ only baseline | Bilişsel boyut katıyor |
| R² > 0 | Yön | Pozitif R² | Şanstan iyi | Herhangi bir açıklanan varyans |

**DİKKAT NOKTALARI:**
- EEG encoding modelleri genellikle düşük R² verir (R² = 0.01-0.10 normal)
- MI 172Hz → EEG 125Hz alignment gerekli
- TRF (Temporal Response Function) ~500ms pencere kullanır
- Tek denek test edilir → genellenebilirlik sınırlı

**MI AVANTAJI:**
- 97D R³ + 131D C³ = 228D özellik → çok zengin temsil
- Hem bottom-up (R³) hem top-down (C³) özellikler
- Bilinen nöral korelatlara doğrudan haritalanır (26 ROI → EEG topography)

**Olası Senaryolar:**
1. ✅ full > envelope > chance → Hiyerarşik avantaj kanıtlandı
2. ✅ full ≈ r3 > envelope → C³ katmıyor ama R³ güçlü
3. ⚠️ envelope > full → Overfitting riski (çok boyutlu MI)
4. ❌ full < chance → Alignment/preprocessing hatası

---

### V6: fMRI Encoding — Beyin Bölgesi Tahmini

**Referans:** OpenNeuro ds002725/ds003720 — müzik dinleme fMRI

**MI Karşılaştırması:** MI özellikleri 26 beyin bölgesinin BOLD yanıtını tahmin edebiliyor mu?

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Benchmark | Yorum |
|------|--------|-----------|-----------|-------|
| İşitsel bölgeler R² > 0 | Yön | A1 veya STG pozitif | Temel işitsel kodlama | Minimum beklenti |
| ≥10/26 bölge anlamlı | Büyüklük | significant ≥ 10 | %38 bölge | Yaygın temsil |
| C³ > R³ | Sıra | full_R² > r3_R² | Bilişsel katman faydalı | Hiyerarşik avantaj |

**DİKKAT NOKTALARI:**
- fMRI BOLD tepkisi ~5-6s gecikmelidir → HRF convolution gerekli
- TR = 2s → MI 172Hz'den büyük downsampling
- 26 ROI MNI152 koordinatlarına dayalı → atlas registrasyonu gerekli
- Tek denek → genellenebilirlik sınırlı

**MI AVANTAJI:**
- MI doğrudan 26 beyin bölgesine haritalanır (RAM: Region Activation Map)
- Her bölge için nöroanatomik olarak motive edilmiş özellikler
- Nörokimyasal sistem (DA, NE, OPI, 5HT) fMRI ile karşılaştırılabilir

**Olası Senaryolar:**
1. ✅ İşitsel bölgeler güçlü, ≥10 bölge pozitif → Nöroanatomik validasyon
2. ✅ İşitsel güçlü, prefrontal zayıf → R³ güçlü, C³ refinement gerekli
3. ⚠️ < 10 bölge pozitif → ROI tanımları veya alignment sorunu
4. ❌ İşitsel bölgeler bile negatif → Ciddi alignment hatası

---

### V7: RSA — Temsil Benzerlik Analizi

**Referans:** RSA framework (Kriegeskorte 2008)

**MI Karşılaştırması:** MI belief RDM, akustik baseline'lardan farklı yapı gösteriyor mu?

**Karşılaştırma Kriterleri:**

| Test | Katman | MI Kriteri | Benchmark | Yorum |
|------|--------|-----------|-----------|-------|
| RDM varyansı > 0.01 | Yön | σ > 0.01 | Düz olmayan matris | Farklılaştırma var |
| Belief ≠ MFCC | Büyüklük | ρ < 0.95 | Akustik baseline | Bilişsel katman farkı |
| Belief ≠ R³ | Büyüklük | ρ < 0.90 | R³ perceptual | C³ > R³ zenginlik |
| RDM simetri | — | rdm ≈ rdm.T | Matematiksel doğruluk | Hesaplama kontrolü |

**DİKKAT NOKTALARI:**
- RDM, stimuli çiftleri arasındaki mesafeyi ölçer → yüksek boyutlu karşılaştırma
- ρ < 0.95 "farklı" demek → ρ = 0.90 bile yeterli ayrışma
- Nöral RDM baseline henüz yok → gelecek çalışma

**MI AVANTAJI:**
- 131D belief space → çok zengin RDM
- Farklı seviyelerde (R³, C³, Ψ³) RDM hesaplanabilir
- Bilişsel yapı, akustikten DAHA ZENGİN olmalı

---

## 3. Genel Validasyon Çerçevesi

### 3.1 Evidence Tier Haritalaması

| Validasyon | MI Bileşeni | Tier | Dayanağı |
|------------|-------------|------|----------|
| V1 Ferreri | DA nörokimya | α (mechanistic) | Causal manipulation (drug) |
| V1 Mallik | OPI nörokimya | α | Causal manipulation |
| V1 Laeng | OPI arousal/valence | α | Causal + dissociation |
| V2 IDyOM | F2 Prediction | α-β | Convergent computation |
| V3 Krumhansl | F1 tonal processing | α | Benchmark replication |
| V4 DEAM | F5 emotion/affect | β | Correlational |
| V5 EEG | Full pipeline | β | Encoding model |
| V6 fMRI | RAM (26 bölge) | β | Encoding model |
| V7 RSA | C³ beliefs | β | Representational structure |

### 3.2 Geçiş/Kalış Kriterleri

```
GEÇER (PASS):
  ✅ Katman 1 (Yön): Tüm efekt yönleri doğru
  ✅ Katman 2 (Sıra): Sıralamalar %80+ korunur
  ✅ Katman 3 (Büyüklük): Thresholdlar karşılanır VEYA
     MI yaklaşımının neden farklı olduğu açıklanabilir

KOŞULLU GEÇER (CONDITIONAL PASS):
  ⚠️ Katman 1 doğru ama Katman 2-3 zayıf
  ⚠️ Fark, bilinen bir model limitasyonundan kaynaklanıyor
  ⚠️ MI deterministik olduğu için stokastik veriyle tam eşleşme beklenmez

KALMAZ (FAIL):
  ❌ Katman 1 yanlış (efekt yönü ters)
  ❌ Birden fazla modülde sistematik sapma
  ❌ Açıklanamayan büyük farklar
```

### 3.3 MI vs Literatür Farklılık Analiz Çerçevesi

Bir farklılık bulunduğunda şu sırayla değerlendir:

```
1. METODOLOJI FARKI MI?
   → MI audio-tabanlı, literatür davranışsal/nöral
   → MI deterministik, literatür stokastik
   → MI 172Hz, literatür 1-2Hz
   → EVETSE: Farklılık beklenen, açıklanabilir

2. MI DAHA HASSAS MI?
   → MI 131D, insan raporu 1-7D
   → MI alt-frekans bilgisini de yakalar
   → EVETSE: MI efekti DAHA BÜYÜK olabilir (beklenen)

3. MI SIGMOID KOMPRESYONU MU?
   → Bilinen dar dinamik aralık sorunu (VMM, HGSIC)
   → EVETSE: MI efekti DAHA KÜÇÜK olabilir (bilinen limitasyon)

4. MODEL HATASI MI?
   → Efekt yönü ters
   → Mekanizma formülünde sorun
   → EVETSE: Mekanizma incelenmeli, belki düzeltilmeli
```

---

## 4. Validasyon Uygulama Planı

### Faz 1: Veri Gerektirmeyen Modüller (Öncelik)

| Sıra | Modül | Veri Kaynağı | Süre | Zorluk |
|------|-------|-------------|------|--------|
| 1 | V1 Pharmacology | Hardcoded (literature) | ~30min | Düşük |
| 2 | V3 Krumhansl | Hardcoded (K-K profiles) | ~20min | Düşük |

Bu ikisi hiçbir veri indirmesi gerektirmiyor — hemen çalıştırılabilir.

### Faz 2: Küçük Veri Gerektiren Modüller

| Sıra | Modül | Veri Kaynağı | Boyut | Süre |
|------|-------|-------------|-------|------|
| 3 | V2 IDyOM | Essen Folksong Collection | ~10MB | ~1-2h |
| 4 | V7 RSA | Test-Audio (mevcut) | 0 (mevcut) | ~30min |

### Faz 3: Büyük Veri Gerektiren Modüller

| Sıra | Modül | Veri Kaynağı | Boyut | Süre |
|------|-------|-------------|-------|------|
| 5 | V4 DEAM | DEAM dataset | ~15GB | ~4-8h |
| 6 | V5 EEG | NMED-T (Stanford) | ~39GB | ~8-16h |
| 7 | V6 fMRI | OpenNeuro | ~25-40GB | ~8-16h |

### Faz 4: Tümleştirme

| Sıra | İşlem |
|------|-------|
| 8 | compile_results.py → Tüm sonuçları birleştir |
| 9 | generate_all_figures.py → Nature-style figürler |
| 10 | validation_summary.py → Manuscript supplementary table |

---

## 5. Risk Değerlendirmesi

| Risk | Olasılık | Etki | Azaltma |
|------|----------|------|---------|
| V1 yön hatası | Düşük | Yüksek | Gain parametrelerini ayarla |
| V3 düşük korelasyon | Düşük | Yüksek | BCH consonance → tonal profile mapping |
| V4 valence < 0.2 | Orta | Orta | VMM narrow range bilinen issue |
| V5/V6 alignment hatası | Orta | Yüksek | alignment.py HRF/resampling test |
| V7 RDM flat | Düşük | Düşük | 131D → RDM varyansı beklenir |
| Veri indirme sorunları | Orta | Orta | Faz 1-2'den başla |

---

## 6. Sonuç

MI sistemi, F-testlerini %99.3 başarı oranıyla geçmiştir. Validasyon aşaması, bu dahili başarıyı **harici empirik verilerle** doğrulayacaktır. Karşılaştırma stratejimiz:

1. **Mutlak eşleşme beklenmez** — MI farklı bir hesaplama paradigmasıdır
2. **Yön doğruluğu önceliklidir** — Efekt yönü en kritik kriter
3. **Sıra koruması ikincildir** — Rank korelasyonları kabul edilebilir düzeyde olmalı
4. **Büyüklük farklılıkları açıklanmalıdır** — Her fark için metodolojik neden aranır
5. **MI daha iyi olabilir** — Bu bir hata değil, hesaplamalı avantajdır

**Önerilen başlangıç:** V1 (Pharmacology) + V3 (Krumhansl) — veri indirmesi gerektirmez, hemen çalıştırılabilir.

---

*Report generated 2026-03-04 | MI Validation Strategy | SRC Musical Intelligence*
