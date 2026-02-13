# Phase 3A-2 — Chat R3: Web Araştırması + Hesaplamalı DSP Envanteri

Aşağıdaki dosyayı oku ve Phase 3 planını anla:
Docs/Beta/Beta_upgrade.md

Sen **Chat R3**'sin. Görevin: Web'den derin araştırma yaparak modern ses analizi toolkit'lerinin ve uluslararası standartların sunduğu tüm hesaplanabilir ses özelliklerinin kapsamlı envanterini oluşturmak.

## Proje Dizini
/Volumes/SRC-9/SRC Musical Intelligence

## Arka Plan
R³ şu anda 49D. Input: mel spectrogram (B, 128, T) @ 172.27 Hz frame rate (~5.8ms/frame).
Hedef: 128-256D'ye genişletmek.

Mevcut R³ kodu `mi_beta/ear/r3/` altında 5 grup. Önce bunları oku:
- `psychoacoustic/consonance.py` → 7D
- `dsp/energy.py` → 5D
- `dsp/timbre.py` → 9D
- `dsp/change.py` → 4D
- `cross_domain/interactions.py` → 24D

Bu mevcut uygulamayı anla: input format, output format, [0,1] clamp, `BaseSpectralGroup` contract.
Ayrıca `mi_beta/ear/r3/extensions/_template.py` dosyasını oku — yeni grup ekleme pattern'i.

## Kritik Kısıt
Her yeni feature şu kısıtlara uymalı:
- **Input**: mel spectrogram (B, 128, T) — log-mel normalized
- **Output**: (B, T, dim) tensor, değerler [0, 1] aralığında
- **Hız**: Frame-level, real-time uyumlu (~5.8ms/frame budget'ı paylaşılıyor)
- **Bağımsızlık**: Raw audio'ya erişim YOK — sadece mel spectrogram

## Adımlar

### Adım 1: Toolkit Feature Set Araştırması
Her toolkit için web'den araştır ve **tam feature listesini** çıkar:

#### 1a. librosa (Python, en yaygın)
Web'den araştır: librosa resmi dokümanları, `librosa.feature` modülü.
Tüm feature fonksiyonlarını listele:
- `librosa.feature.chroma_stft` — 12D chroma from STFT
- `librosa.feature.chroma_cqt` — 12D chroma from CQT
- `librosa.feature.chroma_cens` — 12D chroma energy normalized
- `librosa.feature.melspectrogram` — zaten input'umuz
- `librosa.feature.mfcc` — 13-40D cepstral coefficients
- `librosa.feature.spectral_centroid`
- `librosa.feature.spectral_bandwidth`
- `librosa.feature.spectral_contrast` — 7D octave-band contrast
- `librosa.feature.spectral_flatness`
- `librosa.feature.spectral_rolloff`
- `librosa.feature.tonnetz` — 6D tonal centroid features
- `librosa.feature.zero_crossing_rate`
- `librosa.feature.rms`
- `librosa.feature.tempogram` — tempo autocorrelation
- `librosa.onset.onset_strength`
- `librosa.beat.beat_track`
- `librosa.piptrack` — pitch tracking
- ... ve eksik olanlar

Her feature için: boyut, mel'den hesaplanabilir mi, mevcut R³'teki karşılığı.

#### 1b. essentia (C++/Python, en kapsamlı)
Web'den araştır: essentia.upf.edu dokümanları.
Odak alanları:
- **Tonal**: `HPCP` (harmonic pitch class profile), `Key`, `Chords`, `TuningFrequency`, `Inharmonicity`, `Dissonance`, `OddToEvenHarmonicEnergyRatio`
- **Rhythm**: `BeatTrackerDegara`, `BPMHistogram`, `OnsetRate`, `Danceability`, `BeatLoudness`
- **Spectral**: `SpectralComplexity`, `SpectralContrast`, `StrongPeak`, `SpectralPeaks`, `ERBBands`, `BarkBands`
- **SFX**: `PitchSalience`, `MaxToTotal`, `TCToTotal`, `LogAttackTime`
- **Dynamic**: `DynamicComplexity`, `Loudness` (EBU R128), `LoudnessVickers`

Her feature için: boyut, input gereksinimi, mel uyumluluğu.

#### 1c. openSMILE / eGeMAPS (paralinguistic/emotion)
Web'den araştır: openSMILE dokümanları, eGeMAPS paper (Eyben 2015).
88 eGeMAPS feature set:
- F0 statistics (mean, std, percentiles, rising/falling slopes)
- Jitter (local, DDP)
- Shimmer (local, apq3, apq5)
- HNR (harmonics-to-noise ratio)
- Formant frequencies (F1, F2, F3) + bandwidths
- Spectral slopes (0-500Hz, 500-1500Hz)
- Alpha ratio, Hammarberg index
- MFCC 1-4, spectral flux

Hangileri mel'den hesaplanabilir, hangileri raw audio gerektiriyor?

#### 1d. Madmom (beat/onset specialist)
Web'den araştır: madmom dokümanları.
- `RNNBeatProcessor` — neural beat tracking
- `DBNBeatTrackingProcessor` — DBN-based
- `SpectralOnsetProcessor` — spectral flux variants
- `RNNOnsetProcessor` — neural onset
- `TempoEstimationProcessor`
- `CNNKeyRecognitionProcessor`
- `CNNChordRecognitionProcessor`

Hangileri mel spectrogram üzerinden çalışabilir?

#### 1e. CREPE / pYIN / SPICE (pitch estimation)
Web'den araştır:
- **CREPE**: Kim et al. 2018 — CNN monophonic pitch, mel uyumlu mu?
- **pYIN**: Mauch & Dixon 2014 — probabilistic YIN, frame-level
- **SPICE**: CREPE successor, self-supervised, polyphonic

Mel spectrogram'dan pitch estimation feasibility.

#### 1f. ISO / AES Standartları
Web'den araştır:
- **ISO 532-1 (Zwicker loudness)**: Specific loudness per Bark/ERB band → mel band'lardan yaklaşık hesaplanabilir mi?
- **ISO 226 (Equal-loudness contours)**: Loudness weighting → mel üzerine uygulanabilir
- **ITU-R BS.1770 (LUFS)**: Broadcast loudness → K-weighting + gating
- **AES17**: Audio measurement

### Adım 2: Özel Konu Derin Araştırmaları
Her biri için web'den 3-5 kaynak bul:

**a) Mel'den Chroma Hesaplama:**
- Mel spectrogram → chroma mümkün mü? (mel vs CQT vs STFT tabanlı)
- librosa `chroma_stft` mel input alıyor mu?
- Approximation kalitesi: mel-based chroma vs CQT-based chroma

**b) Syncopation Index:**
- Witek et al. 2014 "Effect of syncopation on groove" — formül nedir?
- Longuet-Higgins & Lee 1984 syncopation measure
- Onset pattern → syncopation score hesaplama

**c) Groove Features:**
- Madison 2006 groove operational definition
- Janata et al. 2012 groove and BOLD fMRI
- Senn et al. 2020 groove modeling
- Onset strength + tempo stability → groove proxy

**d) Harmonic Tension Computation:**
- Herremans & Chew 2017 tonal tension computational model
- Lerdahl 2001 Tonal Pitch Space distance
- Chroma → key → tension distance hesaplama pipeline

**e) Information Content (IC) from Audio:**
- IDyOM (Pearce 2005, 2018) — symbolic model, ama audio'dan yaklaşık IC?
- Spectral entropy → information proxy (zaten R³'te var)
- Temporal predictability features
- Hansen & Pearce 2014: IC from audio features

**f) Modulation Spectrum:**
- Spectro-temporal modulation features (Chi et al. 2005)
- AM modulation rates 2-20 Hz → speech/music distinction
- Mel spectrogram → temporal envelope → modulation spectrum

**g) Spectral Contrast:**
- Jiang et al. 2002 spectral contrast features
- Octave-band peak vs valley: 7D
- librosa `spectral_contrast` implementasyonu

### Adım 3: Çıktı Dosyasını Yaz
`Docs/R³/R3-DSP-SURVEY-TOOLS.md` dosyasını oluştur. Yapısı:

#### Bölüm 1: Executive Summary
- Araştırılan toolkit sayısı, toplam bulunan feature sayısı
- Mel-uyumlu feature sayısı (doğrudan ve dolaylı)
- R³'ye en uygun feature kategorileri

#### Bölüm 2: Toolkit Bazlı Feature Tabloları
Her toolkit için ayrı tablo:

| Feature Adı | Boyut | Input | Mel Uyumu | Maliyet | Mevcut R³ Karşılığı | Önerilen R³ Grubu |
|-------------|-------|-------|-----------|---------|---------------------|-------------------|

#### Bölüm 3: Mel-Uyumlu Feature Kataloğu
Sadece mel spectrogram'dan (doğrudan veya dolaylı) hesaplanabilen feature'lar:

| # | Feature | Boyut | Kaynak Toolkit | Hesaplama Yöntemi | R³ Grubu | Öncelik |
|---|---------|-------|----------------|-------------------|----------|---------|

Öncelik: **HIGH** (çok model talep ediyor + kolay hesaplanır), **MEDIUM**, **LOW**

#### Bölüm 4: Hesaplama Maliyeti Analizi
- Frame-level real-time feasibility (172 Hz = 5.8ms budget)
- CPU vs GPU gereksinimi
- Batch processing uygunluğu
- Maliyet sıralaması: en ucuzdan en pahalıya

#### Bölüm 5: Önerilen Yeni R³ Grupları (Toolkit Perspektifi)
Her yeni grup için önerilen feature'lar:

**F: Pitch** — önerilen feature'lar ve toolkit referansları
**G: Rhythm** — önerilen feature'lar ve toolkit referansları
**H: Harmony** — önerilen feature'lar ve toolkit referansları
**I: Information** — önerilen feature'lar ve toolkit referansları
**J: Modulation** — önerilen feature'lar ve toolkit referansları (varsa)

Her feature için:
```
{feature_name}:
  Toolkit: {kaynak}
  Boyut: {nD}
  Mel Hesaplama: {adımlar}
  Referans Kod: {fonksiyon adı veya URL}
  Tahmini Maliyet: {ms/frame}
```

#### Bölüm 6: Karşılaştırma Matrisi
| Kategori | librosa | essentia | openSMILE | Madmom | CREPE | ISO |
|----------|---------|----------|-----------|--------|-------|-----|
| Pitch    |         |          |           |        |       |     |
| Rhythm   |         |          |           |        |       |     |
| Harmony  |         |          |           |        |       |     |
| Timbre   |         |          |           |        |       |     |
| ...      |         |          |           |        |       |     |

(Sütunlarda feature sayısı veya kapsam notu)

#### Bölüm 7: Boyut Hedefi Önerisi
Mevcut 49D + önerilen yeni feature'lar → toplam kaç D?
Minimum genişleme: sadece HIGH priority → ?D
Orta genişleme: HIGH + MEDIUM → ?D
Maksimum genişleme: tümü → ?D

#### Bölüm 8: Implementation Referansları
Her önerilen feature için:
- Kaynak kodu URL (GitHub repo veya toolkit docs)
- API fonksiyon adı
- Örnek kullanım snippet'i
- `BaseSpectralGroup.compute(mel)` formatına dönüştürme notları

## Kurallar
- **Web araştırması için WebSearch ve WebFetch kullan** — agresif araştır
- Mevcut dosyaları DEĞİŞTİRME
- **Tek çıktı dosyası**: `Docs/R³/R3-DSP-SURVEY-TOOLS.md`
- `mi_beta/` READ-ONLY (sadece mevcut R³ kodunu anlamak için oku)
- Tüm web kaynaklarını URL ile referans ver
- "Mel spectrogram'dan hesaplanabilir mi?" sorusuna her feature için **EVET/HAYIR/KISMEN** net cevap ver
- Gerçek zamanlı çalışabilirliği (172 Hz) her feature için değerlendir
- Spekülatif önerileri "ÖNERİ:" etiketi ile işaretle
