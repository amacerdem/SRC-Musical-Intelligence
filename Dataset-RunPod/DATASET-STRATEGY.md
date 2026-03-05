# My Musical Mind — MVP Dataset Strategy v1.0

## Hedef: 5,000 Track (Deezer 30s Preview)

### Neden 5,000?
- **Kullanıcı deneyimi**: Her oturumda yeni şarkı keşfi → min 2K gerekli
- **MI analiz kalitesi**: 5 Neural Family × signal space coverage → min 3K gerekli
- **İstatistiksel güç**: C³ 131 belief × yeterli varyans → 5K optimal
- **Dosya boyutu**: 5,000 × ~480KB = **~2.3 GB** (30s MP3 preview)
- **Deezer API**: 5,000 track × 1 API call = ~25 dakika (rate limit dahil)

---

## Genre Dağılımı (MI Signal Space Optimizasyonu)

App geleneksel genre kullanmıyor — 5 Neural Family (Anchor/Alchemist/Kineticist/Architect/Explorer)
ve 5 Mind Gene (entropy/resolution/tension/resonance/plasticity) kullanıyor.

AMA genre çeşitliliği = signal space çeşitliliği = Neural Family coverage.

| # | Genre Kümesi | Track | % | Neden | Primary Signal Coverage |
|---|-------------|-------|---|-------|------------------------|
| 1 | **Pop / Mainstream** | 750 | 15% | Tanınırlık, geniş valence aralığı | Mid-energy, high-valence → Anchors |
| 2 | **Rock / Alternative** | 600 | 12% | Energy çeşitliliği, dinamik yapı | High-energy, varied-valence → Alchemists |
| 3 | **Hip-Hop / Rap** | 500 | 10% | Ritmik complexity, groove | Rhythmic density → Architects |
| 4 | **Electronic / Dance / EDM** | 500 | 10% | Tempo çeşitliliği, sentetik timbres | High-tempo, high-energy → Kineticists |
| 5 | **R&B / Soul / Funk** | 400 | 8% | Groove, warmth, vokal expression | Warm timbres → Anchors/Kineticists |
| 6 | **Jazz / Fusion** | 350 | 7% | Harmonik complexity, improv | High-complexity → Explorers/Architects |
| 7 | **Klasik / Orkestral / Film** | 350 | 7% | Dinamik range, timbral diversity | Full-range dynamics → All families |
| 8 | **Metal / Punk / Hard Rock** | 250 | 5% | Extreme energy, aggression | Max-energy, low-valence → Alchemists |
| 9 | **Latin / Reggaeton** | 250 | 5% | Ritmik diversity, dans | Rhythmic, high-valence → Kineticists |
| 10 | **Türkçe / Anadolu** | 250 | 5% | Kullanıcı tabanı, kültürel bağ | Varied → All families |
| 11 | **Folk / Acoustic / Singer-SW** | 250 | 5% | Acousticness, intimacy | High-acoustic → Anchors |
| 12 | **Ambient / Downtempo / Chill** | 200 | 4% | Low-energy exploration | Low-energy → Anchors/Explorers |
| 13 | **World / Regional** | 150 | 3% | Kültürel diversity (Arabic, Asian, African) | Novel timbres → Explorers |
| 14 | **Blues / Country** | 100 | 2% | Expression, dinamik | Varied → Architects |
| 15 | **Experimental / IDM** | 100 | 2% | Max entropy, novelty | High-entropy → Explorers |
| | **TOPLAM** | **5,000** | **100%** | | |

---

## Neural Family Coverage Hedefi

Her genre kümesi farklı Neural Family'lere katkı sağlar:

| Neural Family | Hedef | Besleyen Genres |
|--------------|-------|-----------------|
| **Anchors** (~20%) | 1,000 | Pop, R&B/Soul, Folk, Ambient, Türkçe ballad |
| **Alchemists** (~20%) | 1,000 | Rock, Metal, Klasik (dramatic), Alt |
| **Kineticists** (~20%) | 1,000 | Electronic, Latin, Funk, Dance |
| **Architects** (~20%) | 1,000 | Hip-Hop, Jazz, Blues, Pop (structured) |
| **Explorers** (~20%) | 1,000 | Jazz improv, Experimental, World, Ambient |

*Not: Gerçek dağılım MI analizi sonrası belirlenir, bu sadece hedef.*

---

## Track Seçim Kriterleri

Her genre kümesi için:

### Popularity Mix (Tanınırlık Stratejisi)
- **%40 Viral/Hit**: Deezer rank > 800K — herkesin bildiği şarkılar
- **%35 Mid-tier**: Rank 400K-800K — genre sevenler bilir
- **%25 Deep-cut**: Rank < 400K — keşif heyecanı

### Temporal Coverage (Dönem Çeşitliliği)
- **%20** Klasik dönem (pre-2000)
- **%30** 2000-2015
- **%30** 2015-2023
- **%20** 2023-2026 (güncel)

### Artist Diversity
- **Max 5 track per artist** (mevcut katalogda 10-14 → çok fazla)
- **Min 1,500 unique artist** (5000/3.3 avg)
- Her genre kümesinde en az 30 farklı artist

### Signal Space Coverage (Teknik)
- Her genre kümesi içinde:
  - Energy: min 3 track < 0.3, min 3 track > 0.7
  - Tempo: 60-180 BPM aralığı kaplansın
  - Duration: 30s-600s mix

---

## Veri Toplama Stratejisi (Deezer API)

### Yöntem 1: Artist-Based (Primary — %70)
1. Her genre için 50-100 artist listesi hazırla
2. Her artist'ten top 3-5 track al
3. Avantaj: Kalite garantisi, genre doğruluğu yüksek

### Yöntem 2: Editorial Playlist-Based (%20)
1. Deezer editorial playlist'lerinden track çek
2. "Pop Essentials", "Viral Dance", "80s Hits" gibi
3. Avantaj: Zaten popüler ve çeşitli

### Yöntem 3: Chart-Based (%10)
1. Deezer global/ülke chart'larından
2. Avantaj: Güncel viral hit'ler

### Dedup & Validation
- deezer_id unique constraint
- Preview URL varlığı kontrolü
- MP3 header validation (indirme sonrası)
- Duration > 15s (çok kısa olanları ele)

---

## Dosya Yapısı

```
My Musical Mind (Test-01)/
└── data/
    └── dataset_5k/
        ├── catalog.json          — Track metadata + genre + signal features
        ├── manifest.json         — Download status, MD5, file sizes
        ├── artist_list.json      — Genre → artist mapping (seed data)
        ├── previews/             — 5,000 MP3 files ({deezer_id}.mp3)
        └── stats.json            — Genre distribution, signal coverage report
```

---

## Türkçe Müzik Kümesi (250 Track) — Özel Seçim

| Alt-genre | Track | Örnek Artistler |
|-----------|-------|-----------------|
| Pop | 60 | Tarkan, Sezen Aksu, Aleyna Tilki, Mabel Matiz |
| Rock/Alt | 50 | maNga, Duman, Mor ve Ötesi, Adamlar |
| Arabesk/Fantezi | 30 | Müslüm Gürses, İbrahim Tatlıses, Orhan Gencebay |
| Anadolu Rock | 30 | Barış Manço, Erkin Koray, Cem Karaca, Altın Gün |
| Rap | 30 | Ceza, Şanışer, Ezhel, Murda |
| Elektronik | 25 | Amon Tobin (TR?), Oceanvs Orientalis, Ahu |
| Türk Sanat/Halk | 25 | Zeki Müren, Neşet Ertaş, Aşık Veysel |

---

## Tahmini Süre & Kaynak

| Adım | Süre | Not |
|------|------|-----|
| Artist listesi hazırlama | Script ile ~5 dk | Curated seed list |
| Deezer API collection | ~30 dk | 5000 track × rate limit |
| Preview download | ~20 dk | 16 concurrent, ~480KB each |
| Validation & dedup | ~5 dk | Header check, duplicate removal |
| **TOPLAM** | **~1 saat** | |
