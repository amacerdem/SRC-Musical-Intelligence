# Phase 3A-3 — Crossref: R1 + R2 + R3 Sentezi → R³ v2 Kesin Tasarım

Aşağıdaki dosyayı oku ve Phase 3 planını anla:
Docs/Beta/Beta_upgrade.md

Sen **Crossref Chat**'sin. Görevin: 3 paralel araştırma chat'inin çıktılarını birleştirip, R³ v2 kesin tasarımını oluşturmak.

## Proje Dizini
/Volumes/SRC-9/SRC Musical Intelligence

## Arka Plan
Phase 3A'da 3 paralel chat çalıştı:
- **R1 (Bottom-up)**: 96 C³ modelin R³ taleplerini analiz etti → `Docs/R³/R3-DEMAND-MATRIX.md`
- **R2 (Literatür)**: Yerel 121 dosya + psikoakustik DSP araştırması → `Docs/R³/R3-DSP-SURVEY-THEORY.md`
- **R3 (Web/Toolkit)**: 6 toolkit + 7 özel konu web araştırması → `Docs/R³/R3-DSP-SURVEY-TOOLS.md`

Mevcut R³: 49D (A:Consonance 7D, B:Energy 5D, C:Timbre 9D, D:Change 4D, E:Interactions 24D)
Hedef: 128-256D arası genişleme.

## Giriş Dosyaları — TAMAMEN OKU
Şu 3 dosyayı baştan sona oku:
1. `Docs/R³/R3-DEMAND-MATRIX.md` — R1 çıktısı (6 bölüm + ekler)
2. `Docs/R³/R3-DSP-SURVEY-THEORY.md` — R2 çıktısı (8 bölüm)
3. `Docs/R³/R3-DSP-SURVEY-TOOLS.md` — R3 çıktısı (8 bölüm)

Ayrıca mevcut R³ kodunu anlamak için oku:
4. `mi_beta/ear/r3/` altındaki 5 grup `.py` dosyası (READ-ONLY)
5. `mi_beta/ear/r3/extensions/_template.py` — yeni grup pattern'i

## Adımlar

### Adım 1: Üç Perspektifin Karşılaştırmalı Analizi

Her dosyanın temel önerilerini karşılaştır:

**a) Boyut hedefi uyuşması:**
- R1: Senaryo B → 68D (muhafazakar, +19D), Senaryo C → ~128D
- R2: ~128D önerisi (49 mevcut + ~79 yeni), mevcut 49D'de sadece ~15-20 efektif bağımsız boyut
- R3: 128D minimum, 192D orta, 256D maksimum
- → Kesin hedef ne olmalı? Gerekçesiyle karar ver.

**b) Yeni grup yapısı uyuşması:**
- R1: 4 yeni grup → F:Pitch(5D), G:Rhythm(5D), H:Harmony(5D), I:Information(4D)
- R2: 4 yeni grup → F:Pitch(16-18D), G:Rhythm(8-12D), H:Harmony(12-18D), I:Information(8-12D)
- R3: 5 yeni grup → F:PitchHarmony(18D), G:RhythmGroove(12D), H:SpectralDetail(20D), I:InfoDynamics(9D), J:Modulation(20D)
- → Grup sayısı, isimleri, boyutları ne olmalı? R1'in talebiyle R2/R3'ün kapasitesini dengeleyerek karar ver.

**c) Mevcut grup revizyonu:**
- R2 ciddi sorunlar tespit etti: ~15-20 efektif boyut, 3 çapraz duplikasyon, normalizasyon bug, Stevens' law çift sıkıştırma
- R2 §3: A→10-12D, B→7D, C→10D, D→8D, E→16-24D revizyon önerileri
- R3: Mevcut A-E'yi koruma eğiliminde
- → Mevcut gruplar revize edilmeli mi, yoksa olduğu gibi korunup yeni gruplar mı eklenmeli? Argümanları tartış.

**d) Feature isim çakışmaları:**
- R1 ve R2'nin önerdiği feature isimleri örtüşüyor mu?
- Aynı kavrama farklı isimler verilmiş mi? (ör: R1 "melodic_entropy" vs R2 "spectral_surprise" vs R3 "i_info")
- → Kanonik isim listesi oluştur.

### Adım 2: Gap ↔ Feature Eşleştirme

R1'in Bölüm 1'deki 31 ACOUSTIC gap'ini tek tek ele al. Her gap için:

```markdown
### GAP-{ID}: {açıklama}
- **Kaynak**: {Unit}-{Model}
- **R2 karşılığı**: {R2 §5'ten feature adı} veya "Karşılık yok"
- **R3 karşılığı**: {R3 §3'ten feature adı ve toolkit} veya "Karşılık yok"
- **Mel uyumluluğu**: EVET / KISMEN / HAYIR
- **Hesaplama maliyeti**: Trivial / Ucuz / Orta / Pahalı (R3 §4'ten)
- **Çözüm**: {Hangi yeni R³ grubuna, hangi feature olarak eklenmeli}
- **Durum**: ✅ Çözüldü / ⚠️ Kısmen / ❌ Çözülemez (neden)
```

3 kategori oluştur:
- **(a) Bilinen DSP ile çözülebilir** — R2 veya R3'te karşılığı var, mel-uyumlu, maliyet uygun
- **(b) Yeni yöntem gerekli** — Konsept var ama doğrudan toolkit implementasyonu yok
- **(c) R³ kapsamı dışı** — Raw audio gerektiriyor veya neural-level çözüm gerektiriyor

### Adım 3: R1 Talep Sıralaması × R3 Fizibilite Çaprazı

R1 §3'teki en çok talep edilen feature'ları R3'ün fizibilite değerlendirmesiyle çaprazla:

| Sıra | Feature (R1) | Talep (model sayısı) | R3 Mel Uyumu | R3 Maliyet | R2 Psikoakustik Temeli | Kesin Karar |
|------|-------------|---------------------|-------------|-----------|----------------------|------------|
| 1 | melodic_entropy | 18 | ? | ? | ? | DAHİL/HARİÇ |
| 2 | syncopation_index | 17 | ? | ? | ? | DAHİL/HARİÇ |
| 3 | metricality_index | 14 | ? | ? | ? | DAHİL/HARİÇ |
| 4 | harmonic_entropy | 13 | ? | ? | ? | DAHİL/HARİÇ |
| ... | ... | ... | ... | ... | ... | ... |

Her feature için:
- R3 toolkit'te karşılığı var mı? (§2 tabloları)
- R2 literatürde psikoakustik dayanağı var mı? (§5 kataloğu)
- Mel spectrogram'dan hesaplanabilir mi? (her üçünün uyumu)
- **Kesin karar**: DAHİL (R³ v2'ye alınacak) veya HARİÇ (neden)

### Adım 4: R³ v2 Kesin Feature Listesi

Tüm analizi birleştirerek **kesin** R³ v2 feature listesini oluştur:

```markdown
## R³ v2 Feature Inventory

### Group A: Consonance [0:?] — ?D
| Index | Feature Name | Karar | Kaynak | Hesaplama |
|-------|-------------|-------|--------|-----------|
| 0 | ... | MEVCUT/YENİ/REVİZE | R2 §X | mel → ... |

### Group B: Energy [?:?] — ?D
...

### Group F: Pitch [?:?] — ?D (YENİ)
...
```

Her feature için:
- **Index**: Kesin R³ v2 indeksi
- **Feature Name**: Kanonik snake_case isim
- **Karar**: MEVCUT (değişmedi), REVİZE (formül değişti), YENİ (ilk kez eklendi), SİLİNDİ (çıkarıldı)
- **Kaynak**: R1 talebi (§3 + model listesi) + R2 teori (§bölüm) + R3 toolkit (§bölüm)
- **Hesaplama**: Mel spectrogram → feature adımları (1-2 cümle)
- **Psikoakustik temel**: Hangi algısal fenomeni ölçer?
- **Maliyet tahmini**: ms/frame (R3 §4'ten)

### Adım 5: Mevcut Grup Revizyonu Kararları

R2'nin tespit ettiği sorunları tek tek ele al ve karar ver:

**a) Duplikasyon problemi:**
- R2: [3]==[12], [1]==1-[16], [2]==[17] gibi çapraz duplikasyonlar var
- → Kaldırılacak mı? Yeniden hesaplanacak mı? Backward compatibility?

**b) Normalizasyon bug (concentration[24]):**
- R2'nin bulgusu: ne yanlış, doğrusu ne olmalı?
- → Phase 6'da düzeltilecek mi?

**c) Stevens' law çift-sıkıştırma:**
- R2'nin bulgusu: nerede oluyor, etkileri?
- → Phase 6'da düzeltilecek mi?

**d) Interaction grubu (E) yeniden tasarımı:**
- Mevcut: 24D mekanik çarpım terimleri
- R2: 16-24D principled redesign önerisi
- R3: Yeni gruplarla etkileşim genişlemesi
- → E grubu nasıl yeniden tasarlanmalı?

### Adım 6: Boyut Hedefi ve Senaryolar

Kesin boyut hedefini belirle:

| Senaryo | Toplam D | Mevcut A-E | Yeni Gruplar | Gerekçe |
|---------|---------|-----------|-------------|---------|
| Minimum | ?D | ?D | ?D | ... |
| Önerilen | ?D | ?D | ?D | ... |
| Maksimum | ?D | ?D | ?D | ... |

Seçilen senaryo için:
- GPU real-time fizibilitesi (R3 §4 maliyet analizine dayanarak)
- Model etkisi (R1 talep matrisine dayanarak kaç modele fayda)
- Psikoakustik kapsam (R2 literature coverage'a dayanarak)

### Adım 7: Açık Sorunlar ve Phase 3B Girdileri

Crossref'te kesinleştirilemeyen konuları listele:
- Hangi kararlar Phase 3B'de mimari tasarım gerektiriyor?
- Hangi feature'lar deneysel test/benchmark gerektiriyor?
- Backward compatibility stratejisi ne olmalı? (mevcut 49 indeks korunmalı mı?)

## Çıktı Dosyasını Yaz
`Docs/R³/R3-CROSSREF.md` dosyasını oluştur. Yapısı:

### Bölüm 1: Üç Perspektif Karşılaştırması
- R1/R2/R3 boyut hedeflerinin karşılaştırma tablosu
- Grup yapısı uyuşma/uyuşmazlık analizi
- Konsensüs noktaları ve ayrışma noktaları

### Bölüm 2: Gap ↔ Feature Eşleştirme Tablosu
- 31 ACOUSTIC gap × {R2 karşılığı, R3 karşılığı, mel uyumu, çözüm durumu}
- 3 kategori: (a) çözülebilir, (b) yeni yöntem gerekli, (c) kapsam dışı

### Bölüm 3: Talep × Fizibilite Çapraz Matrisi
- Top-20 talep edilen feature × mel uyumu × maliyet × karar tablosu

### Bölüm 4: R³ v2 Kesin Feature Listesi
- Tam indeksli, isimlendirilmiş, hesaplama yöntemi belirtilmiş feature inventory
- Mevcut (revize veya korunan) + yeni feature'ların tam listesi
- Her feature için: kaynak (R1 talep + R2 teori + R3 toolkit)

### Bölüm 5: Mevcut Grup Revizyon Kararları
- Duplikasyonlar, bug'lar, yeniden tasarım kararları
- E grubu (interactions) yeni tasarım planı

### Bölüm 6: Kesin Boyut Hedefi
- Seçilen senaryo ve gerekçesi
- Grup bazlı boyut dağılımı
- Real-time fizibilite onayı

### Bölüm 7: Phase 3B Girdileri ve Açık Sorular
- Mimari tasarım gerektiren kararlar listesi
- Backward compatibility stratejisi önerisi
- Deneysel doğrulama gerektiren feature'lar

### Bölüm 8: Kaynak Referansları
- R1, R2, R3'ten bölüm bazlı çapraz referanslar
- Her karar için hangi dosyanın hangi bölümüne dayandığı

## Kurallar
- **3 giriş dosyasını TAMAMEN oku** — seçici okuma yapma, her bölümü oku
- Mevcut dosyaları DEĞİŞTİRME (R1, R2, R3 çıktıları READ-ONLY)
- **Tek çıktı dosyası**: `Docs/R³/R3-CROSSREF.md`
- `mi_beta/` READ-ONLY (sadece mevcut kodu anlamak için)
- **Veri odaklı karar**: Her karar en az 2/3 chat'in verisine dayanmalı
- **Çelişki çözümü**: R1/R2/R3 farklı öneriyorsa, her birinin argümanını sun ve gerekçeli karar ver
- **Net kararlar**: "Olabilir" veya "belki" yerine DAHİL/HARİÇ/ERTELEME gibi net kararlar ver
- Feature isimleri **snake_case** olmalı
- Spekülatif önerileri "ÖNERİ:" etiketi ile işaretle
- Kesinleştirilemeyen konuları "AÇIK SORU:" etiketi ile işaretle
