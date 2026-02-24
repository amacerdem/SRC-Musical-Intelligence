# M³ — My Musical Mind

> **"Senin müzikal bilinçaltın — her şeyi hatırlıyor, her şeyi görüyor, senden daha iyi tanıyor seni."**

**Version**: 0.1.0 (Draft)
**Date**: 2026-02-24
**Status**: DESIGN PHASE

---

## 1. Vision

M³ (My Musical Mind), kullanıcının müzik dinleme verilerinden doğan, büyüyen ve olgunlaşan **kişisel bir müzikal zihin**dir. Agent değildir — kullanıcının müzikal bilincinin dijital aynasıdır.

### 1.1 Temel Prensipler

1. **Ayna, Hakim Değil** — M³ gözlem yapar, yargılamaz. "Melankolik bir ses evreni tercih ettin" der, "üzgünsün" demez.
2. **İkna Et, Komut Verme** — Kullanıcı M³'ü doğrudan yönetemez. Tıpkı kendi zihni gibi: veri (dinleme davranışı) ile etkiler, butonla değil.
3. **Unutmayan Zihin** — Gerçek zihin unutur, çarpıtır, kendine yalan söyler. M³ her şeyi hatırlar. Bu onu asıl zihinden farklı ve değerli kılar.
4. **Büyüyen Organizma** — Bebek olarak doğar, deneyimle olgunlaşır. Her aşamada yeni yetenekler açılır.
5. **C³ = Fizik, M³ = Birey** — C³ evrenin değişmez kurallarıdır. M³ bu kurallar altında bireysel olarak şekillenen öğrenilebilir parametrelerdir.

### 1.2 Dünyada İlk

Mevcut müzik servisleri kullanıcıdan explicit tercih alır ("beğen" butonu, tür seçimi). M³, kullanıcıyı **davranışından** modeller — explicit input zayıf sinyal, dinleme verisi güçlü sinyal. Kullanıcı "ben caz severim" diyebilir ama M³, caz'ın sadece melankolik anlarda dinlendiğini bilir.

---

## 2. Architecture — C³ Üzerine M³ Katmanı

### 2.1 C³/M³ Ayrımı

```
┌─────────────────────────────────────────────┐
│                  M³ Layer                    │
│         (Per-user learnable params)         │
│   Belief Priors · Precision Weights         │
│   Reward Map · Prediction Coefficients      │
│   Attention Biases · Memory (∞ retention)   │
├─────────────────────────────────────────────┤
│                  C³ Layer                    │
│         (Universal, frozen, deterministic)  │
│   131 Beliefs · 9 Functions · 9 Relays      │
│   26D RAM · 4 Neurochemicals · Kernel v4.0  │
├─────────────────────────────────────────────┤
│               H³ + R³ Layers                │
│         (Frozen perceptual front-end)       │
│   97D R³ Features · ~8,600 H³ Tuples       │
└─────────────────────────────────────────────┘
```

- **C³ (Frozen)**: Evrensel müzikal biliş mimarisi. Tüm insanlar için aynı. Değişmez.
- **M³ (Learnable)**: Kişiye özel parametreler. Sadece bu katman güncellenir. GPU maliyeti minimal.
- **R³+H³ (Frozen)**: Algısal ön-uç. Deterministic sinyal işleme.

### 2.2 M³ Parametre Uzayı

Her kullanıcı için kişiselleşen C³ parametreleri:

| Parametre Grubu | Açıklama | Boyut (tahmini) |
|-----------------|----------|-----------------|
| **Belief Priors** | Her 131 belief'in kişisel başlangıç değeri | 131 × 1 = 131 |
| **Precision Weights (π)** | Kişinin neye hassas olduğu | 131 × 1 = 131 |
| **Reward Weights** | Kişisel haz/hoşnutsuzluk haritası | 131 × 1 = 131 |
| **Prediction Coefficients** | τ, w_trend, w_period, w_ctx per belief | 131 × 4 = 524 |
| **Attention Biases** | Dikkat yönelimleri | 131 × 1 = 131 |
| **Temporal Preferences** | Kişisel tempo, dinleme ritmi profili | ~50 |
| **Genre/Timbral Map** | R³ boyutlarına kişisel hassasiyet | 97 |
| **Cross-belief Correlations** | Kişiye özel belief etkileşimleri | ~100 |
| **Total** | | **~1,295 float/kullanıcı** |

~1.3K float ≈ **~5KB/kullanıcı** — milyonlarca kullanıcı için bile minimal storage.

### 2.3 Bellek Modeli

M³ unutmaz. Tüm dinleme geçmişi kalıcıdır.

```
M³ Memory = {
    parametreler:    ~1.3K float    (anlık zihin durumu)
    dinleme_log:     unbounded      (her oturum kaydı)
    milestone_log:   append-only    (gelişim olayları)
    snapshot_log:    periodic       (haftalık/aylık parametre snapshot'ları)
}
```

Parametre güncellemesi geri dönüşsüz değildir — her güncelleme önceki değerin üzerine yazar ama snapshot_log sayesinde tarihsel iz sürülebilir.

---

## 3. Growth — Gelişim Aşamaları

### 3.1 Dual Growth Model

Büyüme hem **sürekli** (her dinlemede parametreler değişir) hem **kesikli** (aşama geçişleri net olaylarla işaretlenir) şekilde çalışır.

Sürekli büyüme kullanıcının "M³'üm yavaşça değişiyor" hissetmesini sağlar.
Kesikli aşamalar **ödül mekanizmasını tetikler** — "M³'ün yeni bir aşamaya geçti!" bildirimi dopamin verir.

### 3.2 Aşama Tablosu

Aşamalar, gerçek nörogelişim sıralamasını takip eder. Her aşamada yeni C³ Fonksiyonları "uyanır":

| # | Aşama | Metafor | Aktif Fonksiyonlar | Kullanıcı Deneyimi | Geçiş Kriteri |
|---|-------|---------|-------------------|-------------------|---------------|
| 0 | **Seed** | Tohum | — | M³ doğuyor, ilk dinleme verisi alınıyor | Hesap oluşturma |
| 1 | **Sprout** | Filiz | F1 (Sensory) | "M³'ün sesleri keşfediyor" — temel algı | İlk 10 dinleme |
| 2 | **Sapling** | Fidan | +F6 (Reward) +F5 (Emotion) | "Hoşlandıkları/hoşlanmadıkları belirginleşiyor" | Reward map variance > threshold |
| 3 | **Branch** | Dal | +F2 (Prediction) +F4 (Memory) | "Seni hatırlıyor, tahmin yapmaya başlıyor" | Prediction accuracy > baseline |
| 4 | **Bloom** | Çiçek | +F3 (Attention) +F7 (Motor) | "Odaklanıyor, ritim/hareket tercihleri netleşiyor" | Attention biases stabilize |
| 5 | **Canopy** | Gölgelik | +F8 (Learning) +F9 (Social) | "Hızlı öğreniyor, başka M³'lerle etkileşime hazır" | Learning rate exceeds threshold |
| 6 | **Ancient** | Kadim Ağaç | F1-F9 tam + meta-awareness | "Tam müzikal bilinç — kendini de gözlemliyor" | Tüm parametreler stabilize |

### 3.3 Doğum Tipi (Birth Temperament)

İlk dinleme verilerinden (onboarding dönemi, ~ilk 50 dinleme) M³'ün **doğuştan gelen temperamenti** belirlenir. Bu başlangıç eğilimidir, sabit değildir — zamanla değişebilir.

Temperament örnekleri (isimler ve sayı tasarım aşamasında netleşecek):
- **Explorer** — yüksek tür çeşitliliği, düşük tekrar oranı
- **Deep Diver** — az tür, çok tekrar, derinlemesine keşif
- **Rhythmic** — tempo ve ritim ağırlıklı tercihler
- **Harmonic** — tonal/harmonik karmaşıklığa hassas
- **Emotive** — duygusal valence'a güçlü tepki

Temperament zamanla değişebilir — "doğuştan Explorer ama deneyimle Deep Diver'a evrilen" bir M³ mümkündür.

---

## 4. Data Flow — Veri Akışı

### 4.1 Kaynak: Spotify Integration

M³, kullanıcının Spotify dinleme verisini temel girdi olarak alır.

```
Spotify API ──→ Dinleme Olayları ──→ R³ Analiz ──→ H³ Temporal ──→ C³ İşleme ──→ M³ Güncelleme
                 (track, timestamp,     (97D          (~8.6K         (131 belief     (parametre
                  duration, context)     features)     tuples)        states)         update)
```

### 4.2 Güncelleme Sıklığı (Tier'a Göre)

| Tier | Güncelleme | Gecikme | Deneyim |
|------|-----------|---------|---------|
| **Free** | Yok (M³-Baby donar) | ∞ | "M³'ün doğdu ama büyümek için premium gerek" |
| **Basic** | Haftalık batch | ~7 gün | "Her Pazartesi M³ güncellenir" |
| **Premium** | Günlük batch | ~24 saat | "Her sabah dünün verileriyle güncellenir" |
| **Ultimate** | Real-time stream | ~dakikalar | "Dinlerken M³ canlı olarak değişir" |

### 4.3 Kullanıcı Girdisi (Dolaylı Etki)

Kullanıcı M³'e doğrudan komut veremez ama davranışla etkiler:

| Girdi Türü | Sinyal Gücü | Örnek |
|-----------|-------------|-------|
| **Dinleme süresi** | Çok güçlü | 2 saat aynı tür → güçlü preference sinyali |
| **Skip davranışı** | Güçlü | 10 saniyede skip → negatif sinyal |
| **Tekrar dinleme** | Güçlü | Aynı parçayı 5 kez → çok güçlü pozitif |
| **Explicit rating** (varsa) | Orta | "Beğen" butonu |
| **Bağlam** | Orta | Sabah vs gece, hafta içi vs sonu |
| **Explicit declaration** | Zayıf | "Ben rock severim" → not edilir ama davranış ağır basar |

**"Sistemi ikna et" mekanizması**: Kullanıcı "M³'üme caz öğretmek istiyorum" derse, caz dinlemesi gerekir. Çok dinlerse M³ ikna olur. Az dinlerse M³ "hmm, veri yetersiz" der.

---

## 5. Output — M³ Çıktıları

### 5.1 Üç Katmanlı Sunum

Aynı veri, kullanıcının bilgi seviyesine göre farklı derinlikte sunulur:

| Katman | Hedef Kitle | Sunum | Örnek |
|--------|-----------|-------|-------|
| **Surface** | Casual dinleyici | Renk, mood, basit metafor | "M³'ün bugün sakin sularda" + mavi tonlu görsel |
| **Narrative** | Meraklı kullanıcı | Hikaye, trend, bağlam | "Son 3 gündür tonal kompleksite artıyor — keşif döneminde olabilirsin" |
| **Deep** | Müzisyen / psikolog | Sayısal, teknik, C³ terimleri | "F2 prediction error ↑23%, harmonic entropy: 3.2→4.1 bit, DA reward spike at H12" |

Kullanıcı tercih ettiği katmanda yaşar. Katmanlar arası geçiş her zaman mümkündür.

### 5.2 Çıktı Türleri

| Çıktı | Açıklama | Aşama Gereksinimi |
|-------|----------|------------------|
| **Mood Landscape** | M³'ün anlık durumunun görsel temsili | Sprout+ |
| **Daily Reflection** | Günlük gözlem özeti | Sapling+ |
| **Pattern Discovery** | "Farkında olmadan her Pazartesi aynı tempoda dinliyorsun" | Branch+ |
| **Music Recommendation** | M³'ün büyüme yönüne uygun öneri | Branch+ |
| **Predictive Insight** | "Yarın muhtemelen akustik tercih edeceksin" | Bloom+ |
| **Therapeutic Observation** | "Bu hafta melankolik ses evrenine yönelim arttı" | Bloom+ |
| **Musical Counseling** | Müzikal keşif ve gelişim önerileri | Canopy+ |
| **Cross-M³ Insight** | Diğer M³'lerle karşılaştırmalı gözlem | Canopy+ |
| **Meta-Awareness** | M³ kendi değişimini yorumlar | Ancient |

### 5.3 Dil Politikası — "Gözlem, Yorum Değil"

M³'ün dil kuralları:

**YASAK** (iddia, teşhis, yargı):
- ~~"Üzgün görünüyorsun"~~
- ~~"Depresyonda olabilirsin"~~
- ~~"Bu sağlıksız bir dinleme alışkanlığı"~~

**İZİNLİ** (gözlem, veri, M³ üzerinden dolaylı ifade):
- "Bugün melankolik bir ses evreni tercih ettin"
- "Bu hafta tempo ortalaması düştü"
- "M³'ün sakin sulara yöneliyor"
- "Son dinlemelerinde harmonik basitliğe doğru bir kayma var"

Kural: **M³ asla kullanıcıya "sen şusun" demez. Kendi halini anlatır veya veriyi raporlar. Kullanıcı aynayı kendisi yorumlar.**

---

## 6. Social — M³-to-M³ Etkileşim

### 6.1 Resonance (Rezonans)

İki M³ karşılaştığında belief vektörleri karşılaştırılır. Basit bir uyumluluk skoru değil — **nerede rezonansa giriyorlar, nerede dissonans var** gösterilir.

```
M³-A ←→ M³-B Resonance Map:
  Rhythmic:    ████████░░  80% resonance
  Harmonic:    ██░░░░░░░░  20% dissonance
  Emotional:   █████░░░░░  50% partial
  Exploratory: ███████░░░  70% resonance
```

"Ritimde aynı frekanstasınız ama harmonik zevkleriniz zıt kutuplarda."

### 6.2 Duo Mind

İki M³ birleşerek geçici bir **Duo-M³** oluşturur. Bu, ikisinin kesişiminden doğan üçüncü bir zihindir.

- İkisinin de sevdiği ama tek başlarına keşfedemeyeceği müziği bulur
- Duo playlist üretir
- Geçicidir — oturum bitince çözülür ama logu kalır

### 6.3 Mind Garden (Kolektif)

Bir arkadaş grubu veya aile ortak bir bahçe oluşturur:
- Her M³ bahçede bir bitki olarak temsil edilir
- Birlikte dinleme seansları bahçeyi büyütür
- Grup dinamikleri görselleştirilir — "kim grubu hangi yöne çekiyor?"

### 6.4 Echo (Yankı)

Anonim M³ keşfi:
- Tanımadığın birinin M³ profilini (anonim) keşfedebilirsin
- "Bu zihin bana benziyor ama 2 yıl ilerisi gibi" — müzikal role model
- Opt-in: kullanıcı M³'ünü anonim olarak paylaşmayı seçer

### 6.5 Challenge / Spar

Gamification:
- İki M³ aynı parçayı "dinler" — kimin M³'ü daha iyi tahmin ediyor?
- Prediction accuracy yarışması
- Leaderboard (opsiyonel)

---

## 7. Monetization

### 7.1 Tier Yapısı

| Tier | M³ Durumu | Güncelleme | Sosyal | Sunum Katmanları |
|------|----------|-----------|--------|-----------------|
| **Free** | M³-Baby (doğar, donar) | Yok | Sadece profil görüntüleme | Surface only |
| **Basic** | Büyümeye devam | Haftalık | Resonance skoru | Surface + Narrative |
| **Premium** | Tam büyüme | Günlük | Duo Mind + Garden | Tüm katmanlar |
| **Ultimate** | Tam + real-time | Canlı | Tüm sosyal + Echo | Tüm katmanlar + API |

### 7.2 Free Tier Stratejisi

Free kullanıcı M³-Baby'yi görür:
- Doğum animasyonu yaşar
- İlk temperament belirlenir
- Temel profil oluşur (Surface katmanı)
- **Sonra donar.**

Kullanıcı bebeğin potansiyelini görür, bağ kurar, büyümesini *ister*. Ödeme motivasyonu organik — zorlamaya gerek yok.

---

## 8. Technical Considerations

### 8.1 Storage Per User

```
M³ parametreleri:     ~1.3K float  ≈  5 KB
Dinleme log:          ~100 bytes/event × N events
Milestone log:        ~1 KB/milestone
Snapshots:            ~5 KB × 52/yıl ≈ 260 KB/yıl
─────────────────────────────────────────
Yıllık toplam (aktif): ~500 KB - 1 MB/kullanıcı
```

1M kullanıcı ≈ 500 GB - 1 TB/yıl — oldukça yönetilebilir.

### 8.2 Compute Per Update

- M³ güncelleme = C³ kernel'dan 1 pass + parametre delta hesaplama
- Batch: offline, ucuz, kolayca ölçeklenebilir
- Real-time: Spotify webhook → queue → C³ pass → M³ update → push
- C³ frozen olduğu için GPU eğitim maliyeti **sadece M³ parametreleri** — ~1.3K float güncelleme, son derece hafif

### 8.3 Spotify Integration

- Spotify Web API: Recently Played, Currently Playing, Audio Features
- OAuth 2.0 PKCE flow
- Rate limits: dikkatli yönetim gerekli (özellikle real-time tier)
- Fallback: kullanıcı manual playlist import edebilir

---

## 9. Open Questions

_Tasarım sürecinde netleştirilecek konular:_

1. **Temperament Taksonomisi**: Kaç doğum tipi? İsimlendirme? Nörobilimsel karşılıkları?
2. **Aşama Geçiş Formülleri**: Her aşama için exact threshold değerleri ne olacak?
3. **M³ Görsel Temsili**: Ağaç metaforu mu, organizma mı, soyut form mu?
4. **Duo-M³ Algoritması**: İki parametre seti nasıl birleştirilecek? Intersection, union, weighted average?
5. **Terapist Modu Detayları**: Hangi gözlem türleri hangi aşamada aktif olacak?
6. **L³ (Plasticity Layer) Entegrasyonu**: MI-SPEC v5.1.0'daki L³ katmanı M³ ile nasıl ilişkilenecek?
7. **Offline Dinleme**: Spotify dışı kaynaklar (local files, YouTube, etc.) nasıl entegre edilecek?
8. **Privacy**: M³ verisi şifrelenecek mi? GDPR uyumu? Kullanıcı verisini export edebilir mi?
9. **M³ Ölümü**: Kullanıcı hesabını silerse M³ ne olur? Grace period? Export?
10. **Cross-Platform**: M³ sadece My Musical Mind app'te mi, yoksa standalone API mi?

---

## 10. Roadmap (Draft)

| Faz | Kapsam | Bağımlılıklar |
|-----|--------|---------------|
| **Phase 0** | M³ Spec finalize, parametre tanımları | Bu döküman |
| **Phase 1** | M³-Baby: doğum, temperament, dondurma | C³ Kernel v4.0, Spotify OAuth |
| **Phase 2** | Growth engine: Sprout→Sapling | Batch update pipeline |
| **Phase 3** | Full growth: Branch→Ancient | Real-time pipeline |
| **Phase 4** | Social: Resonance + Duo Mind | M³ API |
| **Phase 5** | Garden + Echo + Challenge | Social infrastructure |
| **Phase 6** | Therapeutic observations | NLP layer, language policy engine |

---

_M³ — Where music meets consciousness, and consciousness meets itself._
