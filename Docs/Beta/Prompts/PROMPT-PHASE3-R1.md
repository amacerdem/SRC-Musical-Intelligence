# Phase 3A-1 — Chat R1: R³ Model Talep Analizi (Bottom-up)

Aşağıdaki dosyayı oku ve Phase 3 planını anla:
Docs/Beta/Beta_upgrade.md

Sen **Chat R1**'sin. Görevin: 96 C³ modelin R³ ihtiyaçlarını analiz et ve talep matrisi oluştur.

## Proje Dizini
/Volumes/SRC-9/SRC Musical Intelligence

## Arka Plan
R³ şu anda 49D (5 grup: A:Consonance 7D, B:Energy 5D, C:Timbre 9D, D:Change 4D, E:Interactions 24D). Phase 3'te 128-256D'ye genişletilecek. Senin görevin **modellerin ne istediğini** haritalamak.

## Adımlar

### Adım 1: Mevcut R³ Feature Listesini Al
`mi_beta/ear/r3/` altındaki 5 grubun `feature_names` listesini oku:
- `psychoacoustic/consonance.py`
- `dsp/energy.py`
- `dsp/timbre.py`
- `dsp/change.py`
- `cross_domain/interactions.py`

49 feature'ın tam isim-index listesini çıkar. Bu senin referans çerçeven.

### Adım 2: 7 R³ Gap Log'u Oku ve Konsolide Et
Şu dosyaları oku:
- `Docs/R³/R3-GAP-LOG-IMU.md`
- `Docs/R³/R3-GAP-LOG-ASU.md`
- `Docs/R³/R3-GAP-LOG-PCU.md`
- `Docs/R³/R3-GAP-LOG-RPU.md`
- `Docs/R³/R3-GAP-LOG-MPU.md`
- `Docs/R³/R3-GAP-LOG-NDU.md`
- `Docs/R³/R3-GAP-LOG-ARU.md`

Her gap'i 3 kategoriye ayır:
- **ACOUSTIC**: Gerçek akustik özellik eksikliği → R³'e yeni feature olarak eklenebilir
- **NAMING**: İsimlendirme uyumsuzluğu → mevcut feature var ama doc'ta farklı isimle referans ediliyor
- **NEURAL**: Neural-seviye metrik → R³ olamaz, model/mekanizma seviyesinde çözülmeli

### Adım 3: 96 Model Doc Section 4 Tara
`Docs/C³/Models/` altındaki 96 model klasörünü tara. Her modelin doc dosyasında "Section 4" veya "R³" veya "Input" bölümünü bul ve oku.

Her model için kaydet:
- Model ID (ör: SPU-α1-BCH)
- Okuduğu R³ indeksleri (0-48)
- R³ bağımlılığının gücü: **critical** (model bu feature olmadan çalışamaz) / **important** (ana girdi) / **minor** (destek)
- Mevcut R³'te olmayan ama ihtiyaç duyduğu feature kategorisi: Pitch? Rhythm? Harmony? Information? Modulation? Diğer?

### Adım 4: Mevcut Kullanım Haritasını Oku
`Docs/C³/Matrices/R3-Usage.md` dosyasını oku — Phase 2'de oluşturulan mevcut kullanım matrisi.

### Adım 5: Talep Matrisi Dosyasını Yaz
`Docs/R³/R3-DEMAND-MATRIX.md` dosyasını oluştur. İçeriği:

#### Bölüm 1: Konsolide Gap Tablosu
Tüm gap'ler tek tabloda:

| Gap ID | Unit | Model | Eksik Feature | Kategori (ACOUSTIC/NAMING/NEURAL) | Önerilen Yeni R³ Grubu | Öncelik |
|--------|------|-------|---------------|-----------------------------------|----------------------|---------|

#### Bölüm 2: Birim Bazlı Talep Özeti
Her unit için:
- Toplam model sayısı
- Mevcut R³ kullanım profili (hangi grupları yoğun kullanıyor)
- İhtiyaç duyduğu yeni R³ grupları
- En kritik eksik feature'lar

#### Bölüm 3: Feature Talep Sıralaması
En çok talep edilen eksik feature'lar, kaç model istiyor:

| Sıra | Eksik Feature | Talep Eden Model Sayısı | Önerilen R³ Grubu | İlgili Modeller |
|------|--------------|------------------------|-------------------|-----------------|

#### Bölüm 4: 96 Model × 5 Mevcut Grup Kullanım Matrisi
Hangi model hangi grubu (A-E) okuyor — yoğunluk tablosu.

#### Bölüm 5: Yeni Grup Talep Matrisi
96 model × önerilen yeni gruplar (F:Pitch, G:Rhythm, H:Harmony, I:Information, ...):

| Model | F:Pitch | G:Rhythm | H:Harmony | I:Information | Diğer |
|-------|---------|----------|-----------|---------------|-------|

#### Bölüm 6: Sonuç ve Öneriler
- Hangi yeni grup en çok modele fayda sağlar?
- Minimum genişleme senaryosu (en kritik 10-20 feature)
- Maksimum genişleme senaryosu (tüm faydalı feature'lar)

## Kurallar
- **Sadece OKUMA ve YAZMA** — mevcut model doc'larını DEĞİŞTİRME
- **Tek çıktı dosyası**: `Docs/R³/R3-DEMAND-MATRIX.md`
- `Literature/` ve `mi_beta/` READ-ONLY
- Veriye dayalı analiz yap, her iddia bir dosya referansına dayanmalı
- Spekülatif önerileri "ÖNERİ:" etiketi ile işaretle
