# Phase 3A-2 — Chat R2: Yerel Literatür + Psikoakustik DSP Araştırması

Aşağıdaki dosyayı oku ve Phase 3 planını anla:
Docs/Beta/Beta_upgrade.md

Sen **Chat R2**'sin. Görevin: Literature/r3/ klasöründeki 121 dosyayı ve mevcut R³ kodunu inceleyerek, psikoakustik temelli ses ölçüm yöntemlerinin kapsamlı envanterini oluşturmak.

## Proje Dizini
/Volumes/SRC-9/SRC Musical Intelligence

## Arka Plan
R³ şu anda 49D. Mevcut kod `mi_beta/ear/r3/` altında 5 grup:
- A: Consonance (7D) — basit proxy hesaplamalar (spectral variance, autocorrelation, bin ratio)
- B: Energy (5D) — RMS, türevler, onset detection
- C: Timbre (9D) — bin ratio'lar, tristimulus
- D: Change (4D) — spectral flux, entropy, flatness
- E: Interactions (24D) — mekanik çarpım terimleri

Literature/r3/ klasöründe 58 PDF'den oluşturulmuş 121 markdown dosyası var. Bunlar psikoakustik, DSP, spectral müzik ve hesaplamalı müzik teorisi konularını kapsıyor.

## Adımlar

### Adım 1: Mevcut R³ Kodunu Derinlemesine Anla
`mi_beta/ear/r3/` altındaki 5 grubun `.py` dosyalarını oku:
- `psychoacoustic/consonance.py` — compute() metodunu oku, hangi formüller kullanılıyor?
- `dsp/energy.py` — compute() metodunu oku
- `dsp/timbre.py` — compute() metodunu oku
- `dsp/change.py` — compute() metodunu oku
- `cross_domain/interactions.py` — compute() metodunu oku

Her grup için not et:
- Kullanılan DSP yöntemi
- Psikoakustik modele ne kadar sadık? (ör: "roughness" gerçek Plomp-Levelt mı yoksa basit proxy mi?)
- Zayıf yanları (nerede bilinen daha iyi yöntemler var?)

### Adım 2: Literature/r3/ Taraması
5 alt klasördeki dosyaların İÇERİĞİNİ oku (sadece isimlerini değil):

**psychoacoustics/** (11 dosya) — ÖNCELİKLİ, derinlemesine oku:
- `Consonance&Dissonance_Part1.md`, `Part2.md` — Plomp-Levelt modeli, critical band theory
- `Fundamental_Principles_of_Just_Intonatio_Part1-3.md` — JI interval ratios, harmonicity
- `Pressnitzer_2000_ContMusRev.md` — continuous perception, roughness temporal dynamics
- `elife-neural_Part1-2.md` — neural correlates of pitch, timbre, rhythm
- `ji_primer_ed3.md` — just intonation theory
- `JI-Terry.md` — practical JI
- `Intonation_of_Harmonic_Intervals_Adaptab.md` — interval tuning

Her dosyadan çıkar:
- Tanımlanan ölçülebilir akustik özellikler
- Hesaplama formülleri (varsa)
- R³'teki mevcut karşılığı (varsa) ve mevcut implementasyonun yeterliliği

**dsp-and-ml/** (4 dosya):
- `A_Short_Survey_and_Comparison_of_CNN-Based_Music_Genre_Classification_Using_Multiple_Spectral_Features.md`
- `Automatic_Music_Genre_Classification_Based_on_Modu.md`
- `Music_type_classification_by_spectral_contrast_fea.md`
- `Benetos Automatic transcription of Turkish microtonal 2015 published.md`

Her dosyadan: kullanılan feature set, mel'den hesaplanabilirlik.

**spectral-music/** (7 dosya):
- Anderson, Chung, Fineberg, Stanford spectral composition
- Microtonal pitch organization

Spectral müziğin hangi boyutları R³'e katkı sağlayabilir?

**computational-music-theory/** (65 dosya) — SEÇİCİ oku (en büyük klasör):
- `Geometry_of_Music_Part1-24.md` (Tymoczko) — özellikle Part 1-5 oku: voice leading distance, chord spaces
- `Neo-Riemannian_Part1-32.md` — özellikle Part 1-5 oku: transformational operations (P, L, R)
- `Balzano-GroupTheoreticDescription12Fold-1980.md` — 12-fold pitch class group structure
- `Tymoczko.md` — kısa versiyon
- `Julian Hook.md`, `Steven Rings.md`, `Lewin.md` — transformational theory

Her dosyadan: hesaplanabilir müzikal boyutlar. Mel spectrogram'dan türetilebilir mi?

### Adım 3: Aday Feature Envanteri
Her bulunan aday feature için şu formatı kullan:

```markdown
### {Feature Adı} (snake_case)
- **Kategori**: Consonance / Energy / Timbre / Change / Pitch / Rhythm / Harmony / Information / Modulation
- **Önerilen R³ Grubu**: A-I (mevcut veya yeni)
- **Tanım**: 1 cümle — ne ölçer?
- **Psikoakustik Temeli**: Hangi algısal fenomene karşılık gelir?
- **Hesaplama Yöntemi**: Mel spectrogram → feature (formül veya algoritma adımları)
- **Beklenen Aralık**: [min, max], birim
- **Kaynak**: Literature/r3/{dosya_adı} — bölüm/sayfa
- **Mevcut R³'te**: Var (index X) / Yok / Kısmen (proxy: {hangi feature})
- **Mel Uyumluluğu**: Doğrudan / Dolaylı (ara adım: ...) / Mümkün değil (neden: ...)
```

### Adım 4: Derinlik Analizi (4 kritik alan)

**A) Consonance Genişlemesi:**
- Mevcut roughness: basit spectral variance proxy. Gerçek Plomp-Levelt (1965) modeli mel'den uygulanabilir mi?
- Sethares (1993) timbre-dependent dissonance modeli — tam implementasyon nasıl olur?
- Vassilakis (2005) roughness modeli — 3 faktör (amplitude, frequency, phase)
- Helmholtz harmonicity — mevcut autocorrelation yeterli mi, daha iyi yöntem var mı?

**B) Pitch Boyutu (Yeni Grup F):**
- Pitch class profile (chroma): 12D histogram, mel'den CQT'ye dönüşüm gerekli mi yoksa mel tabanlı chroma hesaplanabilir mi?
- Pitch height: log-frequency estimate, mel band'larından türetilebilir
- Tonnetz koordinatları: chroma'dan 6D tonal space (Harte 2006)
- Pitch salience: spectral peak prominence
- Vibrato rate/extent: AM/FM modülasyon analizi

**C) Harmony Boyutu (Yeni Grup H):**
- Tymoczko voice-leading distance: chord → chord geçiş miktarı
- Neo-Riemannian operators: P, L, R transformasyonlar — mel'den hesaplanabilir mi?
- Key clarity: Krumhansl-Kessler probe tone profilleri → chroma korelasyonu
- Harmonic tension: Lerdahl (2001) tonal tension modeli
- Chord template matching: chroma → 24 major/minor template korelasyonu

**D) Information Boyutu (Yeni Grup I):**
- Shannon entropy zaten change grubunda var (index 22). Ama bu sadece spectral entropy.
- Melodic information content: IDyOM (Pearce 2005) — mel'den yaklaşık hesaplanabilir mi?
- Harmonic surprisal: beklenen chord → actual chord divergence
- Predictive uncertainty: entropi üzerinden tahmin güvenirliği

### Adım 5: Çıktı Dosyasını Yaz
`Docs/R³/R3-DSP-SURVEY-THEORY.md` dosyasını oluştur. Yapısı:

1. **Executive Summary** — Kaç dosya tarandı, kaç aday feature bulundu, kategorilere dağılım
2. **Mevcut R³ Eleştirisi** — Literature temelli: her mevcut grubun güçlü/zayıf yanları
3. **Mevcut Grupların Revizyon Önerileri** — A-E için: ne eklenmeli, ne değişmeli?
4. **Yeni Grup Önerileri** — F:Pitch, G:Rhythm, H:Harmony, I:Information için detaylı analiz
5. **Tam Aday Feature Kataloğu** — Yukarıdaki formatta tüm feature'lar (tablo)
6. **Hesaplanabilirlik Değerlendirmesi** — Mel → feature zorluk sıralaması
7. **Literature Referans Matrisi** — Dosya adı → bulunan feature'lar tablosu
8. **Açık Sorular** — Chat R3 (web araştırması) ile çözülmesi gereken belirsizlikler

## Kurallar
- **Sadece OKUMA ve YAZMA** — mevcut dosyaları DEĞİŞTİRME
- **Tek çıktı dosyası**: `Docs/R³/R3-DSP-SURVEY-THEORY.md`
- `Literature/` ve `mi_beta/` READ-ONLY
- Dosya İÇERİKLERİNİ oku, sadece isim listesi yapma
- Her iddia için kaynak belirt: `Literature/r3/{alt_klasör}/{dosya_adı}` + bölüm
- 65 dosyalık computational-music-theory klasöründe seçici ol: en az Geometry Part1-5, Neo-Riemannian Part1-5, Balzano, ve kısa makaleleri oku
- Spekülatif önerileri "ÖNERİ:" etiketi ile işaretle
