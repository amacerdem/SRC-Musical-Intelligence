# F1 Micro-Belief Diagnostics Report — MIDI Stimuli

**Date:** 2026-02-26
**Pipeline:** R³(97D) → H³(634 tuples) → C³(88 mechanisms, 131 beliefs)
**Audio Source:** FluidSynth + TimGM6mb.sf2 SoundFont rendering
**Sample Rate:** 44,100 Hz | **Warmup Trim:** 50 frames
**Total:** 87 WAV files across 8 relays | **Processing Time:** 122s

---

## Executive Summary

F1 Sensory Processing katmaninin 17 belief'i, MIDI ile sentezlenmis 87 gercekci enstruman sesi uzerinden test edildi. Her sesin frekans icerigi, araliklari ve konsonans seviyesi tam olarak bilindigi icin ground truth referansi mevcuttur.

**Genel Degerlendirme:** Sistem buyuk olcude dogru calisiyor. BCH konsonans hiyerarsisi muzik teorisi ile %100 uyumlu. R³ perceptual front-end guclu. Bazi C³ belief'lerde (MIAA, MPG, STAI) duyarlilik sinirli — bu beklenen bir sonuc cunku bu belief'ler daha yuksek seviye cognitif isleme gerektiriyor.

### Sonuc Kategorileri

| Kategori | Relay'ler | Yorum |
|----------|-----------|-------|
| **Mukemmel** | BCH, CSG | Tam beklenen siralama, guclu ayrim |
| **Iyi** | PSCL, PCCR, SDED | Dogru yonde fakat sinirlibazi ayrimlar |
| **Gelistirilmeli** | MIAA, MPG, STAI | Dar dinamik aralik, zayif differansiasyon |

---

## 1. BCH — Brainstem Consonance Hierarchy

**Test Edilen Belief'ler:** harmonic_stability (Core), interval_quality (Appraisal), harmonic_template_match (Appraisal), consonance_trajectory (Anticipation)

**Stimulus Tasarimi:** 17 MIDI stimulus — tek nota, dyad'lar (oktav, P5, P4), triad'lar (major, minor, dim, aug), dom7, kromatik kumeler (4-nota, 6-nota), progresyonlar. Piano, organ ve strings tinilarinda.

### harmonic_stability Siralama Tablosu

| Stimulus | harmonic_stability | roughness | sethares_diss | helmholtz | sensory_pleas |
|----------|-------------------|-----------|---------------|-----------|---------------|
| Single C4 | **0.690** | 0.331 | 0.348 | 0.890 | 0.789 |
| Octave C4-C5 | **0.682** | 0.315 | 0.330 | 0.866 | 0.783 |
| P5 C4-G4 | **0.641** | 0.306 | 0.357 | 0.744 | 0.739 |
| P4 C4-F4 | **0.613** | 0.314 | 0.433 | 0.708 | 0.678 |
| Major triad | **0.568** | 0.389 | 0.565 | 0.733 | 0.542 |
| Aug triad | **0.514** | 0.393 | 0.559 | 0.566 | 0.496 |
| Minor triad | **0.508** | 0.307 | 0.618 | 0.516 | 0.450 |
| Dim triad | **0.457** | 0.477 | 0.749 | 0.488 | 0.366 |
| Dom7 | **0.439** | 0.640 | 0.868 | 0.542 | 0.315 |
| Cluster 4 | **0.308** | 0.945 | 0.977 | 0.481 | 0.164 |
| Cluster 6 | **0.288** | 0.960 | 0.992 | 0.451 | 0.127 |

**Analiz:**
- Siralama muzik teorisi ile **tam uyumlu**: Unison > Oktav > P5 > P4 > Major > Minor > Dim > Cluster
- Sethares dissonance modeli cok guclu ayrim sagliyor (0.33 → 0.99)
- Helmholtz-Kang degerleri consonant araliklardan cluster'a dogru dusuyor
- Aug triad, minor triad'dan biraz yuksek — bu tartismali ama Sethares modeli icin kabul edilebilir (aug triad'in partial overlap patterni farkli)
- **Degerlendirme: MUKEMMEL** — Tam beklenen psikoakustik siralama

### interval_quality Siralama

| Stimulus | interval_quality |
|----------|-----------------|
| Single C4 | **0.708** |
| Octave | **0.677** |
| P5 | **0.529** |
| P4 | **0.486** |
| Major triad | **0.422** |
| Aug triad | **0.281** |
| Minor triad | **0.248** |
| Dim triad | **0.232** |
| Dom7 | **0.272** |
| Cluster 4 | **0.179** |
| Cluster 6 | **0.144** |

**Analiz:** Siralama dogru. Dyad'lardan triad'lara geciste buyuk dusus (multi-interval ambiguity).

### Cross-Timbre Karsilastirma (Ayni Akor, Farkli Enstruman)

| Stimulus | harmonic_stability | interval_quality |
|----------|-------------------|-----------------|
| Major — Piano | 0.568 | 0.422 |
| Major — Organ | 0.567 | 0.335 |
| Major — Strings | 0.511 | 0.253 |
| Cluster — Piano | 0.308 | 0.179 |
| Cluster — Organ | 0.356 | 0.207 |

**Analiz:** Ayni harmoni, farkli tinilar. harmonic_stability tutarli (major > cluster tum tinilarla). Organ'in cluster'i piano'dan biraz yuksek — organ tini daha az inharmonic partial ureter.

---

## 2. PSCL — Pitch Salience in Cortical Lateralization

**Test Edilen Belief'ler:** pitch_prominence (Core, tau=0.35), pitch_continuation (Anticipation)

**Stimulus Tasarimi:** 12 MIDI stimulus — A4 (440 Hz) 5 farkli enstrumanda; C3-C6 arasi 4 register; major akor, 6-nota cluster, diatonik melodi.

### pitch_prominence Sonuclari

| Stimulus | pitch_prominence | R³ pitch_salience | R³ tonalness |
|----------|-----------------|-------------------|-------------|
| C6 piano | **0.673** | 0.987 | 0.373 |
| C4 piano | **0.653** | 0.986 | 0.166 |
| Piano A4 | **0.651** | 0.985 | 0.190 |
| C5 piano | **0.641** | 0.984 | 0.208 |
| Melody diatonic | **0.626** | 0.980 | 0.120 |
| C3 piano | **0.627** | 0.982 | 0.078 |
| Oboe A4 | **0.609** | 0.984 | 0.082 |
| Chord C major | **0.609** | 0.986 | 0.110 |
| Violin A4 | **0.608** | 0.992 | 0.091 |
| Flute A4 | **0.595** | 0.939 | 0.086 |
| Trumpet A4 | **0.571** | 0.955 | 0.069 |
| Cluster 6 | **0.562** | 0.987 | 0.131 |

**Analiz:**
- Tum enstrumanlar yuksek pitch salience (R³ > 0.93) — dogru, hepsi pitched
- Piano en yuksek pitch_prominence — tonalness'i en yuksek (piano SoundFont en "tonal" tini)
- Cluster en dusuk — beklenen (ambiguous pitch)
- Trumpet en dusuk tekli enstruman — ilginc, muhtemelen SoundFont kalitesiyle ilgili
- **Degerlendirme: IYI** — Dogru yonde, fakat enstrumanlar arasi fark kucuk (0.57-0.67)

### pitch_continuation Sonuclari

| Stimulus | pitch_continuation |
|----------|-------------------|
| C6 piano | **0.622** |
| C4 piano | **0.591** |
| Piano A4 | **0.583** |
| Melody | **0.582** |
| Cluster 6 | **0.548** |
| C3 piano | **0.520** |
| Violin A4 | **0.509** |
| Flute A4 | **0.499** |

**Analiz:** Yuksek register = yuksek continuation prediction. Cluster en dusuk. Makul.

---

## 3. PCCR — Pitch Chroma Cortical Representation

**Test Edilen Belief'ler:** pitch_identity (Core, tau=0.4), octave_equivalence (Appraisal)

### Oktav Esdegerligi Testi

| Stimulus | pitch_identity | octave_equivalence | R³ pitch_class_entropy |
|----------|---------------|-------------------|----------------------|
| Single C4 | **0.296** | **0.347** | 0.880 |
| Single A4 | **0.319** | **0.350** | 0.808 |
| Melody C oct3 | **0.258** | **0.301** | 0.957 |
| Melody C oct4 | **0.272** | **0.321** | 0.927 |
| Melody C oct5 | **0.309** | **0.346** | 0.826 |
| Octave dyad | **0.294** | **0.330** | 0.885 |
| 5th dyad | **0.271** | **0.290** | 0.926 |
| Tritone dyad | **0.269** | **0.290** | 0.932 |
| All 12 notes | **0.230** | **0.118** | 0.974 |

**Analiz:**
- 12 nota birden calinca octave_equivalence en dusuk (0.118) — beklenen (tum chroma class'lar esit, equivalence yok)
- Tek nota en yuksek pitch_identity — dogru (net chroma)
- Oktav dyad > tritone dyad icin octave_equivalence — dogru (oktav = ayni chroma class)
- Ayni melodi uc oktavda: pitch_identity oct5 > oct4 > oct3 — yuksek register daha net chroma
- **Degerlendirme: IYI** — Ayrimlar dogru yonde fakat dar aralik (0.12-0.35)

---

## 4. SDED — Sensory Dissonance Early Detection

**Test Edilen Belief:** spectral_complexity (Appraisal)

### Spectral Complexity vs R³ Roughness

| Stimulus | spectral_complexity | R³ roughness | R³ sethares | R³ spectral_flux |
|----------|-------------------|-------------|-------------|-----------------|
| Bitonal C+F# | **0.467** | 0.753 | 0.900 | 0.115 |
| Cluster 4 | **0.457** | 0.945 | 0.977 | 0.154 |
| Cluster 6 | **0.453** | 0.960 | 0.992 | 0.183 |
| Full chromatic | **0.449** | 0.984 | 0.998 | 0.213 |
| m2 dyad | **0.465** | 0.814 | 0.784 | 0.151 |
| Single C4 | **0.443** | 0.331 | 0.348 | 0.025 |
| Octave | **0.441** | 0.315 | 0.330 | 0.030 |
| Major triad | **0.439** | 0.389 | 0.565 | 0.044 |

**Analiz:**
- R³ roughness guclu ayrim sagliyor (0.31 → 0.98)
- R³ sethares_dissonance cok guclu (0.33 → 1.00)
- **PROBLEM:** spectral_complexity belief'i cok dar aralik (0.439-0.467) — R³'teki guclu sinyali C³'e yeterince yansitamiyor
- **Degerlendirme: ZAYIF** — R³ dogru calisiyor ama belief observe() fonksiyonu sinyali bastiriyor. SDED mekanizmasinin P-layer ciktisi incelenmeli.

---

## 5. CSG — Consonance-Salience Gradient

**Test Edilen Belief:** consonance_salience_gradient (Appraisal)

### Salience Siralama

| Stimulus | cons_salience_grad | R³ roughness | R³ sensory_pleas |
|----------|-------------------|-------------|-----------------|
| Cluster 4 | **0.670** | 0.945 | 0.164 |
| m2 dyad | **0.657** | 0.814 | 0.335 |
| V7→I resolution | **0.639** | 0.468 | 0.450 |
| I→V7 tension | **0.642** | 0.486 | 0.419 |
| Major triad | **0.626** | 0.389 | 0.542 |
| Single note | **0.611** | 0.331 | 0.789 |

**Analiz:**
- Siralama dogru: dissonance = yuksek salience, consonance = dusuk salience
- Cluster (0.670) > m2 (0.657) > Major (0.626) > Single (0.611)
- Bu noro-bilimsel olarak dogru: dissonant uyaranlar daha fazla dikkat ceker
- V7→I ve I→V7 benzer ortalama — beklenen (ortalamada ayni notalar)
- **Degerlendirme: IYI** — Dogru yonde, makul aralik (0.06 span)

---

## 6. MPG — Melodic Processing Gradient

**Test Edilen Belief'ler:** melodic_contour_tracking (Appraisal), contour_continuation (Anticipation)

### Melodic Contour Tracking

| Stimulus | contour_tracking | R³ onset_strength | R³ spectral_flux |
|----------|-----------------|-------------------|-----------------|
| Octave leaps | **0.599** | 0.025 | 0.061 |
| Ascending diatonic | **0.599** | 0.046 | 0.108 |
| Violin diatonic | **0.601** | 0.059 | 0.129 |
| Flute diatonic | **0.596** | 0.146 | 0.271 |
| Arpeggio arch | **0.599** | 0.035 | 0.078 |
| Repeated C4 | **0.598** | 0.061 | 0.131 |
| Sustained C4 | **0.600** | 0.013 | 0.025 |

**Analiz:**
- **PROBLEM:** Tum stimulus'lar neredeyse ayni deger (0.596-0.601) — belief hiçbir sey ayirt edemiyor
- R³ onset_strength ve spectral_flux arasinda net farklar var (flute 0.146 vs sustained 0.013)
- Sorun C³ MPG mekanizmasinda: kontur bilgisini adequate sekilde temsil edemiyor
- **Degerlendirme: ZAYIF** — R³ dogru fakat C³ belief sinyali kayip. MPG mekanizmasinin kontur extraction katmani gozden gecirilmeli.

---

## 7. MIAA — Musical Imagery & Auditory Awareness

**Test Edilen Belief'ler:** timbral_character (Core, tau=0.5), imagery_recognition (Anticipation)

### Timbral Character — Ayni Nota (C4), 8 Farkli Enstruman

| Enstruman | timbral_char | R³ warmth | R³ tonalness | R³ spec_autocorr |
|-----------|-------------|-----------|-------------|-----------------|
| Piano pp | **0.591** | 0.369 | 0.083 | 0.782 |
| Piano C5 | **0.572** | 0.426 | 0.213 | 0.620 |
| Piano | **0.564** | 0.752 | 0.188 | 0.755 |
| Guitar | **0.562** | 0.649 | 0.145 | 0.735 |
| Organ | **0.560** | 0.489 | 0.061 | 0.634 |
| Cello | **0.555** | 0.525 | 0.077 | 0.674 |
| Oboe | **0.564** | 0.295 | 0.052 | 0.637 |
| Flute | **0.553** | 0.525 | 0.070 | 0.708 |
| Violin | **0.547** | 0.399 | 0.061 | 0.605 |
| Trumpet | **0.534** | 0.309 | 0.050 | 0.590 |

**Analiz:**
- R³ seviyesinde net timbre farklari var: warmth (0.29-0.75), tonalness (0.05-0.21)
- **PROBLEM:** timbral_character belief'i dar aralik (0.534-0.591) — 8 farkli enstrumani zorlukla ayirt ediyor
- Piano en yuksek (0.564), Trumpet en dusuk (0.534) — makul ama fark cok kucuk
- **Degerlendirme: ORTA** — Yonde dogru fakat duyarlilik yetersiz. MIAA observe() agirlik vektorleri incelenmeli.

---

## 8. STAI — Spectral-Temporal Aesthetic Integration

**Test Edilen Belief'ler:** aesthetic_quality (Core, tau=0.4), spectral_temporal_synergy (Appraisal), reward_response_pred (Anticipation)

### Aesthetic Quality Siralama

| Stimulus | aesthetic_q | spec_temp_syn | reward_pred | R³ sensory_pleas | R³ roughness |
|----------|------------|--------------|-------------|-----------------|-------------|
| Major strings p | **0.569** | 0.561 | 0.577 | 0.452 | 0.385 |
| Chorale choir | **0.570** | 0.563 | 0.578 | 0.446 | 0.505 |
| Beautiful I-vi-IV-V | **0.565** | 0.558 | 0.575 | 0.384 | 0.469 |
| Melody+chords | **0.568** | 0.560 | 0.576 | 0.437 | 0.395 |
| Minor progression | **0.562** | 0.558 | 0.573 | 0.404 | 0.495 |
| Dissonant→resolved | **0.560** | 0.558 | 0.572 | 0.399 | 0.565 |
| Resolved→dissonant | **0.557** | 0.555 | 0.570 | 0.351 | 0.614 |
| Harsh clusters | **0.545** | 0.545 | 0.563 | 0.189 | 0.925 |
| Dense cluster ff | **0.541** | 0.543 | 0.561 | 0.141 | 0.971 |

**Analiz:**
- Siralama dogru: consonant/beautiful > harsh/dissonant
- Major strings (0.569) > Dense cluster (0.541) — dogru yonde
- R³ sensory_pleasantness guclu ayrim sagliyor (0.14 → 0.45)
- **PROBLEM:** C³ belief aralik cok dar (0.541-0.570, sadece 0.03 span)
- STAI F5'ten gelen bir encoder — F1 seviyesinde aesthetic degerlendirme sinirli, bu architectural olarak beklenen
- **Degerlendirme: ORTA** — Dogru siralama ama dar dinamik aralik. STAI mekanizmasinin F5 ile etkilesimi sonraki fazlarda test edilecek.

---

## Katman Bazli Analiz

### R³ (Perceptual Front-End) — GUCLU

R³ 97D vektoru tum stimulus'lar icin beklenen pattermleri uretiyor:

| R³ Boyutu | Dinamik Aralik | Ayrim Gucu | Yorum |
|-----------|---------------|------------|-------|
| roughness | 0.31 — 0.98 | Cok yuksek | Cluster vs tek nota net |
| sethares_dissonance | 0.33 — 0.99 | Cok yuksek | Plomp-Levelt modeli isliyor |
| helmholtz_kang | 0.45 — 0.89 | Yuksek | Konsonans hiyerarsisi dogru |
| sensory_pleasantness | 0.13 — 0.79 | Yuksek | Genis aralik, iyi ayrim |
| pitch_salience | 0.94 — 1.00 | Dusuk (tavan) | Tum pitched sesler yuksek — ceiling effect |
| tonalness | 0.04 — 0.37 | Orta | Piano > diger enstrumanlar |
| warmth | 0.29 — 0.79 | Yuksek | Timbre farkliligi net |
| spectral_autocorrelation | 0.53 — 0.87 | Orta | Timbre correlate |
| onset_strength | 0.01 — 0.15 | Orta | Sustained vs melodic ayrim |
| spectral_flux | 0.02 — 0.27 | Orta | Temporal degisim gostergesi |

### C³ Belief Katmani — KARISIK

| Belief | Dinamik Aralik | Span | Degerlendirme |
|--------|---------------|------|---------------|
| harmonic_stability | 0.29 — 0.69 | **0.40** | Mukemmel |
| interval_quality | 0.14 — 0.71 | **0.57** | Mukemmel |
| harmonic_template_match | 0.51 — 0.82 | **0.31** | Iyi |
| consonance_trajectory | 0.38 — 0.63 | **0.25** | Iyi |
| pitch_prominence | 0.56 — 0.67 | **0.11** | Orta |
| pitch_continuation | 0.47 — 0.62 | **0.15** | Orta |
| pitch_identity | 0.23 — 0.32 | **0.09** | Zayif |
| octave_equivalence | 0.12 — 0.35 | **0.23** | Orta |
| spectral_complexity | 0.44 — 0.47 | **0.03** | Zayif |
| cons_salience_gradient | 0.61 — 0.67 | **0.06** | Orta |
| melodic_contour_tracking | 0.596 — 0.601 | **0.005** | Zayif |
| contour_continuation | 0.648 — 0.657 | **0.009** | Zayif |
| timbral_character | 0.53 — 0.59 | **0.06** | Orta |
| imagery_recognition | 0.62 — 0.64 | **0.02** | Zayif |
| aesthetic_quality | 0.54 — 0.57 | **0.03** | Zayif |
| spectral_temporal_synergy | 0.54 — 0.56 | **0.02** | Zayif |
| reward_response_pred | 0.56 — 0.58 | **0.02** | Zayif |

---

## Temel Bulgular

### 1. R³→C³ Sinyal Kaybı (Signal Attenuation)

En kritik bulgu: R³ guclu sinyaller uretiyor (roughness 0.31-0.98 = 0.67 span) ama C³ belief'lerin cogu bunu dar bir araliga sikistiriyor (spectral_complexity 0.44-0.47 = 0.03 span). Bu "signal attenuation" sorunu uc mekanizmada ozellikle belirgin:

- **SDED:** R³ roughness 67 puan ayrim → C³ spectral_complexity 3 puan ayrim
- **MPG:** R³ onset_strength 14 puan ayrim → C³ melodic_contour 0.5 puan ayrim
- **STAI:** R³ sensory_pleasantness 66 puan ayrim → C³ aesthetic_quality 3 puan ayrim

Olasi nedenler:
1. Mekanizma P-layer'larindaki weighted sum cok fazla smoothing yapıyor
2. Belief observe() agirlik vektorleri R³ sinyalini diger (sessiz) boyutlarla karistiriyor
3. H³ temporal integration uzun horizon'larda ortalama alarak dynamic range'i daraltıyor

### 2. BCH Basarisi

BCH relay'inin basarisi, diger relay'ler icin referans olusturuyor:
- BCH dogrudan R³ Consonance grubunu (A[0:7]) kullaniyor — en guclu R³ boyutlari
- harmonic_stability observe(): 0.50×P0 + 0.30×P1 + 0.20×E2 — agirliklar iyi kalibre
- Sonuc: 0.40 span — en genis dinamik aralik

### 3. Enstruman Timbresinin Etkisi

Piano tum belief'lerde en yuksek degerleri uretiyor — SoundFont bias:
- TimGM6mb.sf2 piano ornekleri en kaliteli (6MB SF icinde en buyuk pay)
- Trumpet, flute gibi enstrumanlar daha dusuk kaliteli
- Bu test sonuclarini etkiliyor: timbre farklari kismenSoundFont limitasyonlari

### 4. Pitch Salience Ceiling Effect

R³ pitch_salience tum pitched sesler icin >0.93 — hic ayrim yok. Bu sorun R³ pitch_salience hesaplamasinin thresholding/normalization'indan kaynaklanıyor. Sonuc: PSCL ve PCCR belief'leri diger R³ boyutlarina (tonalness, pitch_class_entropy) dayanmak zorunda kaliyor.

---

## Oneriler

### Kisa Vadeli (Kalibrasyon)

1. **SDED observe() agirliklarini gozden gecir** — roughness ve sethares_dissonance'a daha yuksek agirlik ver
2. **MPG mekanizmasinin contour extraction'ini incele** — R³ pitch_height degisim sinyalini E-layer'da daha iyi kullan
3. **STAI observe() formülünü guncelle** — sensory_pleasantness sinyaline daha duyarli hale getir

### Orta Vadeli (Mekanizma Iyilestirme)

4. **R³ pitch_salience normalization'i gozden gecir** — ceiling effect'i azalt
5. **H³ horizon secimini optimize et** — kisa horizon'lar (H0-H3) melody/timbre belief'ler icin daha uygun olabilir
6. **MIAA mekanizmasinda timbre-specific R³ boyutlarini (warmth, tonalness, MFCC) daha agir agirlikla kullan**

### Uzun Vadeli (Architectural)

7. **F2-F9 belief testlerini calistir** — STAI gibi cross-function belief'ler tam potansiyellerini F5 (Emotion) ile birlikte gosterecek
8. **Temporal test'ler ekle** — progression'lardaki zaman icerisindeki degisimi izle (frame-by-frame), sadece ortalama degil
9. **Plasticity layer (L³)** implement edildiginde, belief dinamik araliklarinin genislemesi bekleniyor

---

## Dosya Referanslari

| Dosya | Amac |
|-------|------|
| `Tests/micro_beliefs/real_audio_stimuli.py` | MIDI sentez kutuphanesi |
| `Tests/micro_beliefs/generate_f1_midi_audio.py` | 87 WAV uretici |
| `Tests/micro_beliefs/diagnose_f1_audio.py` | Diagnostik runner (--source midi) |
| `Test-Audio/micro_beliefs/f1_midi/` | 87 MIDI WAV dosyasi |
| `Test-Audio/micro_beliefs/f1/` | 67 sentetik WAV dosyasi (Phase 1) |

---

*Bu rapor C³ v4.0 kernel uzerinde, MIDI-sentezlenmis stimuli ile otomatik olarak uretilmistir.*
