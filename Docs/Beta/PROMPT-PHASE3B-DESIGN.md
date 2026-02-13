# Phase 3B — R³ v2 Mimari Tasarımı (Architecture Design)

Aşağıdaki dosyayı oku ve Phase 3 planını anla:
Docs/Beta/Beta_upgrade.md

Sen **Phase 3B Design Chat**'sin. Görevin: Phase 3A'nın araştırma çıktılarını kullanarak R³ v2'nin kesin mimari tasarımını oluşturmak.

## Proje Dizini
/Volumes/SRC-9/SRC Musical Intelligence

## Arka Plan
Phase 3A tamamlandı. 4 çıktı dosyası var:
- `Docs/R³/R3-DEMAND-MATRIX.md` — 96 modelin R³ talep analizi (bottom-up)
- `Docs/R³/R3-DSP-SURVEY-THEORY.md` — Literatür + psikoakustik DSP araştırması
- `Docs/R³/R3-DSP-SURVEY-TOOLS.md` — Web/toolkit DSP araştırması
- `Docs/R³/R3-CROSSREF.md` — 3 araştırmanın sentezi + kesin kararlar

**Crossref'in kesinleştirdiği kararlar:**
- **128D** toplam boyut (49 mevcut + 79 yeni)
- **6 yeni grup**: F:Pitch&Chroma(16D), G:Rhythm&Groove(10D), H:Harmony&Tonality(12D), I:Information&Surprise(7D), J:TimbreExtended(20D), K:Modulation&Psychoacoustic(14D)
- **Mevcut A-E [0:49] korunur** — indeksler değişmez, formül düzeltmeleri Phase 6'ya ertelenir
- **31 gap'ten 28'i çözüldü**, 3'ü multi-track (kapsam dışı)
- **Pipeline dependency**: parallel(A,B,C,D,E,K,J) → F → parallel(G,H) → I

## Giriş Dosyaları — TAMAMEN OKU
Şu dosyaları baştan sona oku:

1. `Docs/R³/R3-CROSSREF.md` — **ANA GİRDİ** (tüm kararlar burada)
2. `Docs/R³/R3-DEMAND-MATRIX.md` — model talepleri (gerektiğinde referans)
3. `Docs/R³/R3-DSP-SURVEY-THEORY.md` — psikoakustik formüller (gerektiğinde referans)
4. `Docs/R³/R3-DSP-SURVEY-TOOLS.md` — toolkit implementasyonları (gerektiğinde referans)

Mevcut R³ kodunu da oku (READ-ONLY):
5. `mi_beta/ear/r3/` altındaki 5 grup `.py` dosyası
6. `mi_beta/ear/r3/extensions/_template.py` — yeni grup pattern'i
7. `mi_beta/core/constants.py` — R3_DIM=49, grup sınırları
8. `mi_beta/core/dimension_map.py` — _R3_FEATURE_NAMES, validasyon
9. `mi_beta/contracts/base_spectral_group.py` — BaseSpectralGroup ABC
10. `mi_beta/contracts/feature_spec.py` — R3FeatureSpec validasyonu
11. `mi_beta/ear/r3/_registry.py` — R3FeatureRegistry
12. `mi_beta/ear/r3/__init__.py` — R3Extractor

## Adımlar

### Adım 1: 7 Açık Mimari Karar (Crossref §7.1)

Crossref 7 açık mimari karar bıraktı. Her birini çöz:

**1.1 Chroma hesaplama yöntemi:**
- Seçenek A: mel→freq→pitch-class fold (doğrudan, hızlı, ~1ms)
- Seçenek B: mel→CQT yaklaşımı (daha doğru, ~3ms)
- Seçenek C: Hybrid (mel-based varsayılan, CQT opsiyonel)
- R3-DSP-SURVEY-TOOLS.md §8.3'teki mel-to-chroma algoritmasını incele
- **Karar ver ve gerekçelendir**: Hesaplama adımları, matris boyutları, PyTorch implementasyon detayı

**1.2 Beat tracking yöntemi:**
- Seçenek A: Onset autocorrelation (basit, hızlı)
- Seçenek B: PLP (Probabilistic Latency-Prior Model)
- Seçenek C: DBN (Dynamic Bayesian Network) — madmom tarzı
- **Karar ver**: G grubu tempo_estimate[65], beat_strength[66], pulse_clarity[67] hangi yöntemle?

**1.3 Entropy/surprise pencere boyutu:**
- I grubundaki melodic_entropy[87], harmonic_entropy[88], spectral_surprise[90] için running statistics
- Exponential decay sabiti τ = ? (saniye)
- Kısa τ (~1s): daha responsive, daha gürültülü
- Uzun τ (~4s): daha stabil, daha geç tepki
- **Karar ver**: τ değeri ve warm-up stratejisi

**1.4 Modulation spectrum penceresi:**
- K grubundaki modulation_0_5Hz[114]...modulation_16Hz[119] için temporal FFT
- 0.5 Hz çözünürlük → ~2s pencere gerekli
- Frame-level çıktı gerekliliği (172 Hz) ile 2s pencere çelişkisi
- **Karar ver**: Pencere boyutu, overlap, hop-size, warm-up handling

**1.5 Hesaplama sırası ve bağımlılık grafiği:**
- F→H bağımlılığı (H tonnetz ve key_clarity F chroma'ya bağlı)
- F→I bağımlılığı (I melodic/harmonic entropy F chroma'ya bağlı)
- G→I bağımlılığı (I rhythmic_IC G onset'lerine bağlı)
- B[11]→G bağımlılığı (G onset_strength mevcut energy grubundan)
- **Detaylı dependency DAG çiz**: Her grubun hangi feature'ları hangi sırayla hesaplanmalı?
- GPU parallelization stratejisi

**1.6 E grubu Phase 6 genişleme planı:**
- Mevcut: 24D mekanik çarpımlar (A×B, D×A, A×C)
- Phase 6'da: Yeni F-K gruplarıyla cross-group interactions?
- 128D budget'ı aşılır mı? (128→144D veya daha fazla?)
- **Karar ver**: E grubu revizyon kapsamı ve boyut hedefi

**1.7 Backward compatibility sınırı:**
- [0:49] indeksleri korunuyor ama formüller Phase 6'da değişecek
- Yeni [49:128] feature'lar eklenirken mevcut model code'u etkilenmeli mi?
- **Detaylı migration stratejisi**: constants.py, dimension_map.py, feature_spec.py için

### Adım 2: Per-Group Detaylı Teknik Spec (3B-1)

Her grup için (A-K) detaylı teknik spec yaz. Crossref §4'teki feature listesini temel al ama **implementasyon detayını** ekle:

**Her feature için:**
```markdown
#### [{index}] {feature_name}
- **Tanım**: 1 cümle
- **Formül**: LaTeX veya pseudo-code
- **Input**: mel[B, 128, T] veya başka grubun çıktısı
- **Output**: [B, T, 1] tensor, [0,1] aralığında
- **Normalizasyon**: sigmoid / min-max / clamp / custom → [0,1] dönüşüm yöntemi
- **Parametreler**: Sabitler, pencere boyutları, eşik değerleri
- **Bağımlılıklar**: Hangi feature'ların önce hesaplanması gerekir?
- **Tahmini maliyet**: ms/frame
- **PyTorch notu**: Hangi torch fonksiyonları kullanılacak? (torch.fft, F.conv1d, etc.)
- **Psikoakustik kaynak**: Birincil referans
```

**Özellikle kritik feature'lar için detay ver:**
- chroma_C..chroma_B [49:61]: mel→freq dönüşüm matrisi nasıl oluşturulur? (128 mel bin → 12 pitch class)
- tonnetz [76:82]: Harte 2006 formülleri, 6D projeksiyon detayı
- syncopation_index [68]: LHL metrik ağırlık formülü, onset→metrical grid eşleme
- melodic_entropy [87]: Running statistics formülü, decay, minimum sample
- mfcc [94:107]: DCT matrisi boyutu (128×13), pre-computed mi?
- modulation [114:120]: Per-band temporal FFT parametreleri

### Adım 3: Interaction Redesign (3B-2)

Mevcut E grubu [25:49] analizi ve Phase 6 revizyon planı:

**3.1 Mevcut E grubunun eleştirisi:**
- 24D = 8+8+8 (A×B, D×A, A×C) çarpım terimleri
- Sadece 3 grup çifti kapsanıyor, F-K hiç yok
- Proxy-based: A grubundaki proxy'lerle çarpım yapmak anlamsız

**3.2 Phase 6 E grubu yeniden tasarım seçenekleri:**
- Seçenek A: Exhaustive pairwise (11 grup × 10/2 = 55 çift → çok büyük)
- Seçenek B: Learned interactions (eğitimle öğrenilen ağırlıklar)
- Seçenek C: Curated domain-expert products (el-seçimi anlamlı çaprazlar)
- Seçenek D: Attention-based dynamic interactions

**3.3 Önerilen interaction tasarımı:**
- Hangi grup çiftleri anlamlı? (ör: Pitch×Rhythm, Harmony×Energy, etc.)
- Her çift için hangi operasyon? (element-wise product, dot product, cosine similarity?)
- Boyut kısıtı: 128D budget dahilinde mi yoksa R³ v2.1'de genişleme mi?

### Adım 4: Kod Kilidi Açma Tasarımı (3B-3)

Mevcut kodda 6 hardcoded "49" kısıtı var. Her birinin Phase 6 çözümünü detaylı tasarla:

**4.1 `mi_beta/core/constants.py`:**
```python
# MEVCUT:
R3_DIM: int = 49
R3_GROUP_BOUNDARIES = ((0, 7), (7, 12), (12, 21), (21, 25), (25, 49))

# HEDEF:
R3_DIM: int = ???  # Nasıl hesaplanmalı?
R3_GROUP_BOUNDARIES = ???  # Nasıl genişletilmeli?
```
- Seçenek A: R3_DIM = 128 (yeni sabit)
- Seçenek B: R3_DIM = R3FeatureRegistry.total_dim (dinamik)
- **Karar ver ve gerekçelendir**

**4.2 `mi_beta/core/dimension_map.py`:**
```python
# MEVCUT: 49-element hardcoded tuple
_R3_FEATURE_NAMES = ("roughness", "sethares_dissonance", ...)

# HEDEF: 128-element, nasıl?
```
- Seçenek A: 128-element yeni tuple (yine hardcoded)
- Seçenek B: R3FeatureRegistry.freeze().feature_names (dinamik)
- **Karar ver**

**4.3 `mi_beta/contracts/feature_spec.py`:**
```python
# MEVCUT:
assert 0 <= self.index < 49

# HEDEF:
assert 0 <= self.index < ???
```
- Registry'den mi? Constants'tan mı?

**4.4 `mi_beta/contracts/base_spectral_group.py`:**
- Docstring'lerdeki "49-D" referansları
- INDEX_RANGE validasyonu

**4.5 `mi_beta/ear/r3/__init__.py` (R3Extractor):**
- Auto-discovery zaten dinamik — extensions/ klasöründen otomatik buluyor
- Yeni grup `.py` dosyaları `extensions/` altına mı yoksa yeni alt klasörlere mi?

**4.6 `mi_beta/ear/r3/_registry.py`:**
- R3FeatureRegistry.freeze() zaten dinamik
- Yeni gruplar register edildiğinde total_dim otomatik güncellenecek mi?

**Her kısıt için:**
- Mevcut kod (kopyala)
- Hedef kod (yaz)
- Migration adımları
- Test stratejisi
- Backward compatibility notu

### Adım 5: BaseSpectralGroup Alt Sınıf Şablonları

Yeni gruplar için `BaseSpectralGroup` implementasyon şablonları yaz. `_template.py`'yi temel al ama somut örnekler ver:

**5.1 F grubu (Pitch & Chroma) örnek implementasyonu:**
```python
class PitchChromaGroup(BaseSpectralGroup):
    GROUP_NAME = "pitch_chroma"
    OUTPUT_DIM = 16
    INDEX_RANGE = (49, 65)  # auto-assigned in v2

    def __init__(self):
        super().__init__()
        self._mel_to_chroma = self._build_chroma_matrix()  # 128×12
        self._dct_matrix = ...  # (varsa)

    @property
    def feature_names(self) -> tuple[str, ...]:
        return ("chroma_C", "chroma_Db", ..., "inharmonicity_index")

    def compute(self, mel: Tensor) -> Tensor:
        # mel: (B, 128, T) → output: (B, T, 16)
        ...
```

**5.2 Diğer 5 grup için de benzer şablonlar** (G, H, I, J, K)

**5.3 Grup arası bağımlılık çözümü:**
- H ve I grupları F'nin chroma çıktısına bağlı
- R3Extractor'ın compute sıralamasını nasıl yönetmeli?
- Mevcut: `torch.cat(parts, dim=-1)` — sıra bağımsız
- Yeni: Sıra bağımlı → compute_ordered() veya dependency injection?

### Adım 6: Deneysel Doğrulama Planı

Crossref §7.2'deki 6 deneysel doğrulama ihtiyacı için test planı yaz:

| Feature | Benchmark Yöntemi | Veri Seti | Başarı Kriteri |
|---------|-------------------|-----------|----------------|
| mel-chroma [49:60] | vs librosa.chroma_cqt key detection | GTZAN, Hainsworth | ≥85% acc |
| melodic_entropy [87] | vs IDyOM IC korelasyonu | Essen folksong | r ≥ 0.7 |
| harmonic_entropy [88] | vs uzman harmoni analizi | Billboard chords | r ≥ 0.6 |
| syncopation_index [68] | vs Witek 2014 ratings | Witek corpus | r ≥ 0.7 |
| groove_index [71] | vs behavioral groove ratings | Madison/Janata | r ≥ 0.5 |
| inharmonicity_index [64] | vs essentia Inharmonicity | NSynth | r ≥ 0.8 |

Her test için:
- Input data formatı
- Karşılaştırma baseline
- Metrik (correlation, accuracy, etc.)
- Fail durumunda fallback planı

### Adım 7: R³ v2 Geçiş Yol Haritası

Phase 3→Phase 6 arası geçiş planı:

```
Phase 3B (ŞİMDİ): Mimari tasarım → R3-V2-DESIGN.md
Phase 3C (SIRADA): Dokümantasyon → 20+ dosya
Phase 3E (SIRADA): 96 model Section 4 güncelleme → v2.2.0
Phase 6 (İLERİDE): Kod implementasyonu:
  6.1: constants.py + dimension_map.py + feature_spec.py güncelle
  6.2: 6 yeni BaseSpectralGroup alt sınıfı yaz (F-K)
  6.3: R3Extractor dependency-aware compute ekle
  6.4: Mevcut A-E formül düzeltmeleri (bug'lar + duplikasyonlar)
  6.5: E grubu interaction redesign
  6.6: Integration test + benchmark
  6.7: 96 model code güncelleme (r3[idx] referansları)
```

## Çıktı Dosyasını Yaz
`Docs/R³/R3-V2-DESIGN.md` dosyasını oluştur. Yapısı:

### Bölüm 1: Tasarım Kararları Özeti
- 7 açık mimari karar ve çözümleri (1 tablo)
- Kesin boyut: 128D (11 grup: A-K)
- Pipeline dependency grafiği (ASCII art)

### Bölüm 2: Grup Spesifikasyonları (A-K)
- Her grup için: ad, boyut, index range, feature listesi
- Her feature için: detaylı teknik spec (formül, normalizasyon, parametreler, PyTorch notu)
- Mevcut gruplar (A-E): Phase 6 revizyon notları ile
- Yeni gruplar (F-K): Tam implementasyon detayı

### Bölüm 3: Hesaplama Pipeline'ı
- Dependency DAG (grup seviyesi ve feature seviyesi)
- GPU parallelization stratejisi
- Frame-level latency analizi (ms/feature, ms/group, ms/total)
- Warm-up davranışı (modulation penceresi, entropy decay)

### Bölüm 4: Interaction Redesign (E Grubu)
- Mevcut 24D analizi
- Phase 6 yeniden tasarım planı
- Yeni interaction tasarımı (grup çiftleri, operasyonlar, boyut)

### Bölüm 5: Kod Değişiklik Planı (Phase 6)
- 6 hardcoded kısıtın çözümü (dosya bazlı)
- Her dosya için: mevcut → hedef kod
- Migration adımları
- Test stratejisi

### Bölüm 6: BaseSpectralGroup Şablonları
- 6 yeni grup için implementasyon şablonları
- Dependency-aware compute mekanizması
- R3Extractor güncelleme tasarımı

### Bölüm 7: Deneysel Doğrulama Planı
- 6 feature × benchmark detayı
- Veri setleri, metrikler, başarı kriterleri
- Fallback planları

### Bölüm 8: Geçiş Yol Haritası
- Phase 3B → 3C → 3E → Phase 6 zaman çizelgesi
- Her aşamada hangi dosyalar üretilecek/güncellenecek
- Bağımlılıklar ve parallelization

## Kurallar
- **Tüm giriş dosyalarını TAMAMEN oku** — özellikle R3-CROSSREF.md her bölümünü
- Mevcut dosyaları DEĞİŞTİRME (R3-CROSSREF.md, DEMAND-MATRIX, SURVEY dosyaları READ-ONLY)
- **Tek çıktı dosyası**: `Docs/R³/R3-V2-DESIGN.md`
- `mi_beta/` READ-ONLY (sadece mevcut kodu anlamak için)
- **Crossref kararlarıyla tutarlı ol** — crossref'in kesinleştirdiği kararları DEĞİŞTİRME, sadece detaylandır
- **Somut ol**: "yaklaşık" veya "belki" yerine kesin sayılar, kesin formüller, kesin parametreler ver
- **PyTorch-native tasarla**: Her hesaplama torch tensor operasyonlarıyla ifade edilebilir olmalı
- Feature isimleri **snake_case** olmalı
- Tüm formüller mel spectrogram (B, 128, T) input'undan başlamalı
- Her feature [0,1] aralığına normalize edilmeli — normalizasyon yöntemi açıkça belirtilmeli
- Spekülatif önerileri "ÖNERİ:" etiketi ile işaretle
- Phase 6'ya ertelenen konuları "PHASE 6:" etiketi ile işaretle
