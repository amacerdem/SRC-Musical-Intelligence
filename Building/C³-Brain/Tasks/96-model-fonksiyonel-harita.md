# C³ — 96 Model Fonksiyonel Beyin Haritası

**Perspektif**: Ünite bazlı değil, **beyin fonksiyonu** bazlı sınıflandırma
**Tarih**: 2026-02-21

> Bir model birden fazla kategoride görünebilir — çünkü beyin böyle çalışır.
> **Birincil** = modelin asıl hesapladığı şey, **İkincil** = dokunduğu diğer sistem.
> Her modelin yanında orijinal ünitesi `[SPU]` şeklinde gösterilir.

---

## Fonksiyonel Kategoriler (12)

| # | Kategori | Açıklama | Model Sayısı |
|---|----------|----------|:------------:|
| F1 | Duyusal İşleme | Temel akustik özellik çıkarımı: perde, timbre, konsonans, frekans | 14 |
| F2 | Örüntü Tanıma & Tahmin | Beklenti, tahmin hatası, bilgi içeriği, istatistiksel düzenlilik | 18 |
| F3 | Dikkat & Önemlilik | Kaynak tahsisi, filtreleme, seçici odaklanma, belirginlik | 14 |
| F4 | Bellek Sistemleri | Kodlama, konsolidasyon, geri çağırma, prosedürel/otobiyografik | 12 |
| F5 | Duygu & Valans | Duygu üretimi, duygusal renklendirme, mod algısı, nostalji | 11 |
| F6 | Ödül & Motivasyon | Dopamin, opioid, haz, istek, tüketim, ürperme | 16 |
| F7 | Motor & Zamanlama | Entrainment, motor planlama, senkronizasyon, groove | 21 |
| F8 | Öğrenme & Plastisite | Deneyime bağlı nöral değişim, ağ reorganizasyonu, verimlilik | 14 |
| F9 | Sosyal Biliş | Grup koordinasyonu, sosyal ödül, empati | 4 |
| F10 | Klinik & Terapötik | Rehabilitasyon, terapi, patoloji, ağrı, nörodejenerasyon | 10 |
| F11 | Gelişim & Evrim | Kritik dönemler, erken çocukluk, ontogeni, filogeni | 6 |
| F12 | Çapraz-Modal Entegrasyon | Modaliteler arası transfer, ortak kodlar, multimodal birleşme | 5 |

> **Not**: Toplam > 96 çünkü birçok model birden fazla kategoride yer alır.

---

## F1 — Duyusal İşleme (14 model)

> Ses → sinir sinyali dönüşümü, temel akustik özellik çıkarımı

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| SPU-α1-BCH | [SPU] | Konsonans hiyerarşisi, harmonik şablon eşleştirmesi | — |
| SPU-α2-PSCL | [SPU] | Perde belirginliği (pitch salience) kortikal temsili | — |
| SPU-α3-PCCR | [SPU] | Oktav-eşdeğer kroma kodlama | — |
| SPU-γ1-SDNPS | [SPU] | FFR-konsonans ilişkisinin sınırları (sentetik vs doğal) | — |
| SPU-γ3-SDED | [SPU] | Disonansın evrensel erken algılanması (152-258ms) | — |
| IMU-α2-PNH | [IMU] | Pisagor oranlarıyla aralık karmaşıklık hiyerarşisi | — |
| IMU-β8-TPRD | [IMU] | Tonotonik frekans haritası vs algısal perde temsili ayrımı | — |
| NDU-α1-MPG | [NDU] | Melodik dizilerin arka-ön korteks gradyanı (onset → kontur) | F2 |
| ASU-α3-CSG | [ASU] | Konsonans-disonans seviyesinin önemlilik ağına etkisi | F3 |
| SPU-β3-MIAA | [SPU] | Sessizlikte müzik imgelemesi → işitsel korteks aktivasyonu | F4 |
| STU-α3-MDNS | [STU] | EEG'den melodi kodu çözme (algı + imgeleme) | F4 |
| STU-β2-TPIO | [STU] | Timbre algısı ve imajinasyonunun aynı substratı paylaşması | F4, F7 |
| IMU-β6-MSPBA | [IMU] | Müzik sentaks ihlali tespiti (Broca alanı, ERAN) | F2 |
| RPU-γ1-LDAC | [RPU] | Beğeninin duyusal korteks kazancını kapılaması (gating) | F6 |

---

## F2 — Örüntü Tanıma & Tahmin (18 model)

> Beklenti oluşturma, tahmin hatası, bilgi içeriği, istatistiksel düzenlilik

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| PCU-α1-HTP | [PCU] | Hiyerarşik zamansal tahmin (soyut 500ms, somut 110ms) | — |
| PCU-α2-SPH | [PCU] | İleri-geri döngülerle uzamsal-zamansal tahmin hiyerarşisi | F4 |
| PCU-α3-ICEM | [PCU] | Bilgi içeriği (IC) pikleri → fizyolojik duygusal tepki | F5 |
| PCU-β1-PWUP | [PCU] | Bağlamsal belirsizliğe göre PE hassasiyet ağırlıklandırma | — |
| PCU-γ3-PSH | [PCU] | Doğru tahminlerin üst düzey temsilleri sessizleştirmesi | — |
| RPU-α3-RPEM | [RPU] | Ödül tahmin hatası (şaşırtıcı+beğenilen vs beğenilmeyen) | F6 |
| RPU-β1-IUCP | [RPU] | Ters-U karmaşıklık tercihi (IC × entropi) | F6 |
| RPU-γ3-SSPS | [RPU] | Eyer şekilli tercih yüzeyi (IC × entropi 2 optimal bölge) | F6 |
| ARU-β1-PUPF | [ARU] | Belirsizlik-sürpriz etkileşiminden haz (Goldilocks) | F6 |
| PCU-β3-UDP | [PCU] | Yüksek belirsizlikte doğru tahmin → daha büyük ödül | F6 |
| IMU-β2-PMIM | [IMU] | ERAN + MMN paralel tahmin → hipokampus öğrenme | F4, F8 |
| ASU-γ1-PWSM | [ASU] | Hassasiyet ağırlıklı belirginlik (kararlı bağlam → MMN) | F3 |
| NDU-α2-SDD | [NDU] | Supramodal sapma algılama (IFG hub) | F3 |
| NDU-β2-CDMR | [NDU] | Bağlama bağlı uyumsuzluk yanıtı (karmaşık melodi) | F8 |
| STU-α1-HMCE | [STU] | Hiyerarşik bağlam kodlama (kısa→uzun pencereler) | F4 |
| PCU-β4-CHPI | [PCU] | Çapraz-modal harmonik tahmin entegrasyonu | F12 |
| IMU-β6-MSPBA | [IMU] | Müzik sentaks ihlal tespiti (Broca = tahmin hatası) | F1 |
| NDU-β3-SLEE | [NDU] | İstatistiksel öğrenme ile düzenlilik çıkarımı | F8 |

---

## F3 — Dikkat & Önemlilik (14 model)

> Kaynak tahsisi, filtreleme, seçici odaklanma, belirginlik tespiti

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| ASU-α1-SNEM | [ASU] | Seçici sinirsel entrainment — beat frekansında titreşim artışı | F7 |
| ASU-α2-IACM | [ASU] | Armonik olmayan seslerin dikkat çekmesi (P3a tepkisi) | — |
| ASU-α3-CSG | [ASU] | Konsonans seviyesinin önemlilik ağını modüle etmesi | F1 |
| ASU-β1-BARM | [ASU] | Bireysel vuruş algılama yeteneğinin entrainment eğilimini modüle etmesi | F7 |
| ASU-β2-STANM | [ASU] | Dikkat hedefine göre beyin ağ topolojisinin yeniden yapılanması | — |
| ASU-β3-AACM | [ASU] | Estetik beğeni → dikkat çekme + motor inhibisyon (savoring) | F6 |
| ASU-γ1-PWSM | [ASU] | Bağlam kararlılığına göre PE ağırlıklandırma (MMN kapılama) | F2 |
| ASU-γ2-DGTP | [ASU] | Müzik-konuşma arası alan-genel zamansal işleme | — |
| ASU-γ3-SDL | [ASU] | Yarımküre lateralizasyonunun dikkat talebine göre dinamik değişimi | — |
| STU-β1-AMSS | [STU] | Polifonik müzikte dikkat modülasyonlu akış ayrımı | F1 |
| STU-β4-ETAM | [STU] | Entrainment + tempo + dikkat çok ölçekli modülasyonu | F7 |
| NDU-α2-SDD | [NDU] | Supramodal sapma algılama mekanizması | F2 |
| PCU-γ1-IGFE | [PCU] | Bireysel gama frekansında uyaran → hafıza + yönetici kontrol | F4 |
| STU-γ2-NEWMD | [STU] | Entrainment vs çalışma belleği bağımsızlığı (paradoks) | F2, F7 |

---

## F4 — Bellek Sistemleri (12 model)

> Kodlama, konsolidasyon, geri çağırma, prosedürel/otobiyografik bellek

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| IMU-α1-MEAMN | [IMU] | Müzik tarafından tetiklenen otobiyografik anı ağı | F5 |
| IMU-α3-MMP | [IMU] | Alzheimer'da müzik belleğinin korunma mekanizması | F10 |
| IMU-β4-HCMC | [IMU] | Hipokampus-korteks bellek konsolidasyon devresi | — |
| IMU-γ1-DMMS | [IMU] | Erken çocukluk müzik bellek iskeleleri (0-5 yaş) | F11 |
| IMU-γ3-CDEM | [IMU] | Bağlama bağlı duygusal bellek (ruh hali uyumu) | F5 |
| IMU-β2-PMIM | [IMU] | Tahmin hatası → hipokampus yeni desen öğrenme | F2 |
| STU-α1-HMCE | [STU] | Hiyerarşik bağlam kodlama (kısa→uzun pencereler) | F2 |
| STU-γ1-TMRM | [STU] | Tempo hafızası yeniden üretim doğruluğu (120 BPM referans) | F7 |
| RPU-β3-MEAMR | [RPU] | Tanıdık müzik → dMPFC otobiyografik hafıza + ödül | F6 |
| ARU-β4-NEMAC | [ARU] | "Benim müziğim" nostalji devresi (kişisel seçim > başkası) | F5 |
| PCU-α2-SPH | [PCU] | Uzamsal-zamansal tahmin → bellek tanıma döngüleri | F2 |
| SPU-β3-MIAA | [SPU] | Müzik imgelemesi → bellek temelli işitsel aktivasyon | F1 |

---

## F5 — Duygu & Valans (11 model)

> Duygu üretimi, duygusal renklendirme, mod algısı, nostalji, otonom yanıtlar

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| ARU-α3-VMM | [ARU] | Majör/minör → ayrı nöral devreler → mutlu/üzgün algısı | — |
| ARU-α2-AAC | [ARU] | Cilt iletkenliği, kalp hızı, solunum → dopamin bağlantısı | F6 |
| PCU-α3-ICEM | [PCU] | Bilgi içeriği pikleri → heyecan, cilt iletkenliği, nabız | F2 |
| IMU-α1-MEAMN | [IMU] | Müzik → otobiyografik anı → nostalji, melankolya, özlem | F4 |
| IMU-γ3-CDEM | [IMU] | Dinleme bağlamı + ruh hali uyumu → duygusal bellek kodlama | F4 |
| ARU-β4-NEMAC | [ARU] | Kişisel müzik → nostalji + iyi olma hali devresi | F4 |
| ARU-β2-CLAM | [ARU] | EEG'den duygu okuma → gerçek zamanlı müzik → duygu düzenleme | F10 |
| ARU-γ2-CMAT | [ARU] | Çapraz-modal duygusal transfer (ses→renk, tempo→uyarılma) | F12 |
| PCU-γ2-MAA | [PCU] | Atonal takdir = kişilik + estetik çerçeve + maruziyet | F8 |
| SPU-β1-STAI | [SPU] | Spektral+zamansal bütünleşme → estetik algı → ödül | F6 |
| ARU-γ3-TAR | [ARU] | Akustik parametreler → kaygı/depresyon/stres tedavisi | F10 |

---

## F6 — Ödül & Motivasyon (16 model)

> Dopamin, opioid, haz, istek, tüketim, ürperme, tercih

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| ARU-α1-SRP | [ARU] | İsteklilik / hoşlanma / haz üçlü dopamin yolağı | — |
| RPU-α1-DAED | [RPU] | Kaudat (beklenti) vs NAcc (tüketim) dopamin ayrışması | — |
| RPU-α2-MORMR | [RPU] | Endojen opioid μ-reseptör bağlanması = haz mekanizması | — |
| RPU-α3-RPEM | [RPU] | Ödül tahmin hatası (şaşırtıcı×beğenilen/beğenilmeyen) | F2 |
| RPU-β1-IUCP | [RPU] | Ters-U karmaşıklık tercihi (orta karmaşıklık = en çok haz) | F2 |
| RPU-β2-MCCN | [RPU] | Ürperme korteks ağı: OFC + insula + SMA + STG (theta) | F7 |
| RPU-β3-MEAMR | [RPU] | Tanıdık müzik → dMPFC nostalji + ödül entegrasyonu | F4 |
| RPU-β4-SSRI | [RPU] | Grup müzik → sosyal senkronizasyon → ödül amplifikasyonu | F9 |
| RPU-γ1-LDAC | [RPU] | Beğeni → duyusal korteks gating (haz geri bildirimi) | F1 |
| RPU-γ2-IOTMS | [RPU] | Bireysel μ-opioid reseptör tonu → müzik ödülü duyarlılığı | — |
| RPU-γ3-SSPS | [RPU] | IC × entropi eyer yüzeyi (2 optimal haz bölgesi) | F2 |
| ARU-β1-PUPF | [ARU] | Belirsizlik × sürpriz → Goldilocks haz fonksiyonu | F2 |
| PCU-β3-UDP | [PCU] | Yüksek belirsizlikte doğru tahmin → büyük ödül | F2 |
| SPU-β1-STAI | [SPU] | Spektral-zamansal estetik bütünleşme → ödül bölgeleri | F5 |
| ASU-β3-AACM | [ASU] | Estetik beğeni → dikkat + inhibisyon (savoring hazzı) | F3 |
| ARU-β3-MAD | [ARU] | Ödül yolağı kopukluğu → müzik anhedonisi | F10 |

---

## F7 — Motor & Zamanlama (21 model)

> Entrainment, motor planlama, senkronizasyon, groove, tempo, ritim

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| MPU-α1-PEOM | [MPU] | Periyot entrainment → kinematik optimizasyon | — |
| MPU-α2-MSR | [MPU] | Müzisyen auditorik-motor fonksiyonel reorganizasyon | F8 |
| MPU-α3-GSSM | [MPU] | Yürüyüş fazı senkronlu SMA+M1 uyarım → denge kontrolü | F10 |
| MPU-β1-ASAP | [MPU] | Motor beat simülasyonu → auditorik "ne zaman" tahmini | F2 |
| MPU-β2-DDSMI | [MPU] | Çift dansı: müzik + kendi + partner + sosyal koordinasyon | F9 |
| MPU-β3-VRMSME | [MPU] | VR müzik → sensorimotor ağ bağlantısı (rehabilitasyon) | F10 |
| MPU-β4-SPMC | [MPU] | SMA→PMC→M1 hiyerarşik motor planlama devresi | — |
| MPU-γ2-CTBB | [MPU] | Serebellar theta-burst → zamansal hassasiyet iyileştirme | — |
| MPU-γ3-STC | [MPU] | Şarkı eğitimi → insula-sensorimotor bağlantı artışı | F8 |
| STU-α2-AMSC | [STU] | İşitsel gama → 110ms gecikmeli motor korteks yayılımı | F1 |
| STU-β3-EDTA | [STU] | Alan-spesifik tempo hassasiyeti (DJ 120-139, perk 100-139) | F8 |
| STU-β4-ETAM | [STU] | Beat entrainment delta-theta + dikkat modülasyonu | F3 |
| STU-β5-HGSIC | [STU] | Groove: pSTG gama → motor korteks hiyerarşik entegrasyon | F6 |
| STU-β6-OMS | [STU] | Orkestral senkronizasyon 4 osilatör ağı | F9 |
| STU-γ1-TMRM | [STU] | Tempo hafızası üretim doğruluğu (120 BPM referans) | F4 |
| STU-γ2-NEWMD | [STU] | Otomatik entrainment vs çalışma belleği paradoksu | F2, F3 |
| STU-γ5-MPFS | [STU] | Motor otomatiklik × yapısal hakimiyet → akış durumu | F8 |
| ASU-α1-SNEM | [ASU] | Beat/metrik frekansta seçici sinirsel titreşim artışı | F3 |
| ASU-β1-BARM | [ASU] | Vuruş algılama yeteneği → entrainment eğilimi modülasyonu | F3 |
| RPU-β2-MCCN | [RPU] | Ürperme ağında SMA motor bileşeni | F6 |
| PCU-β2-WMED | [PCU] | Ritim üretiminde entrainment ↔ çalışma belleği ayrışması | F2 |

---

## F8 — Öğrenme & Plastisite (14 model)

> Deneyime bağlı nöral değişim, ağ reorganizasyonu, sinirsel verimlilik

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| SPU-β2-TSCP | [SPU] | Enstrüman timbresi → kortikal plastisite (eğitim süresiyle orantılı) | F1 |
| SPU-γ2-ESME | [SPU] | Eğitim alanına göre seçici MMN artışı | F1 |
| NDU-α3-EDNR | [NDU] | Uzmanlık → ağ-içi bağlantı ↑, ağlar-arası ↓ → uzmanlaşma | — |
| NDU-β2-CDMR | [NDU] | Karmaşık bağlamda seçici uyumsuzluk yanıtı gelişimi | F2 |
| NDU-β3-SLEE | [NDU] | İstatistiksel öğrenme → çoklu-duyu düzenlilik çıkarımı | F2 |
| NDU-γ3-ECT | [NDU] | Uzmanlaşma ↔ esneklik dengesi (compartmentalization trade-off) | — |
| STU-β3-EDTA | [STU] | Alan-spesifik sensorimotor uzmanlaşma | F7 |
| STU-γ3-MTNE | [STU] | Müzik eğitimi → sinirsel verimlilik (daha iyi davranış + stabil nöral) | — |
| STU-γ4-PTGMP | [STU] | Piyano eğitimi → DLPFC + serebellum gri madde artışı | — |
| STU-γ5-MPFS | [STU] | Akış durumu propensitesi prodijilik belirleyicisi | F7 |
| MPU-α2-MSR | [MPU] | Müzisyen auditorik-motor devre reorganizasyonu | F7 |
| MPU-γ3-STC | [MPU] | Şarkı eğitimi → insula-sensorimotor kalıcı bağlantı | F7 |
| IMU-β3-OII | [IMU] | Beyin osilasyonları (theta+gama) ↔ akışkan zeka bağlantısı | — |
| PCU-γ2-MAA | [PCU] | Atonal takdir = kişilik + maruziyet + estetik çerçeve | F5 |

---

## F9 — Sosyal Biliş (4 model)

> Grup koordinasyonu, sosyal ödül, kişiler arası senkronizasyon

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| RPU-β4-SSRI | [RPU] | Grup müzik → endorfin/oksitosin → ödül 1.3-1.8× amplifikasyon | F6 |
| MPU-β2-DDSMI | [MPU] | Çift dansı: 4 paralel sosyal-motor süreç koordinasyonu | F7 |
| STU-β6-OMS | [STU] | Orkestral senkronizasyon: 4 osilatör ağ (prefrontal, temporo-parietal, limbik, beyin sapı) | F7 |
| MPU-γ1-NSCP | [MPU] | Dinleyiciler arası sinirsel senkronizasyon → ticari başarı tahmini | — |

---

## F10 — Klinik & Terapötik (10 model)

> Rehabilitasyon, terapi, patoloji, ağrı, nörodejenerasyon, anhedonia

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| IMU-α3-MMP | [IMU] | Alzheimer'da müzik belleği korunma mekanizması (SMA/ACC direnci) | F4 |
| IMU-β1-RASN | [IMU] | RAS ritmik uyaran → SMA/serebellum senkronizasyon → motor iyileşme | F7, F8 |
| IMU-β5-RIRI | [IMU] | RAS + VR + robotik → hızlandırılmış motor rehabilitasyon | F7 |
| IMU-β7-VRIAP | [IMU] | Müzik + aktif motor etkileşim → ağrı kesme (S1 bağlantı azalması) | F7 |
| MPU-α3-GSSM | [MPU] | Yürüyüş senkronlu uyarım → denge + yürüme iyileştirme | F7 |
| MPU-β3-VRMSME | [MPU] | VR müzik stimülasyonu → sensorimotor ağ güçlendirme | F7 |
| ARU-β2-CLAM | [ARU] | EEG kapalı döngü → duygu düzenleme (kaygı/depresyon) | F5 |
| ARU-β3-MAD | [ARU] | İşitsel korteks ↔ NAcc kopukluğu = müzik anhedonisi | F6 |
| ARU-γ3-TAR | [ARU] | Akustik parametre manipülasyonu → terapötik müzik reçetesi | F5 |
| NDU-β1-DSP | [NDU] | Ebeveyn şarkısı → erken doğan bebek işitsel plastisite | F11 |

---

## F11 — Gelişim & Evrim (6 model)

> Kritik dönemler, erken çocukluk, ontogeni, filogeni

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| ARU-γ1-DAP | [ARU] | 0-5 yaş müzik maruziyeti → işitsel-limbik bağlantı şekillenmesi | F6 |
| IMU-γ1-DMMS | [IMU] | Erken çocukluk ninni/müzik → kalıcı bellek iskelesi oluşumu | F4 |
| IMU-γ2-CSSL | [IMU] | Türler arası şarkı öğrenme (zebra ispinoz ↔ insan ortak mekanizma) | F4 |
| NDU-β1-DSP | [NDU] | Erken doğan bebekler: ebeveyn şarkısı → işitsel plastisite | F10 |
| NDU-γ1-SDDP | [NDU] | Cinsiyet-bağımlı müzik müdahale yanıtları (erken doğan) | F10 |
| NDU-γ2-ONI | [NDU] | Müzik müdahalesi → beklenen düzeltmenin ötesinde iyileşme | F10 |

---

## F12 — Çapraz-Modal Entegrasyon (5 model)

> Modaliteler arası transfer, ortak kodlar, multimodal birleşme

| Model | Orijinal | Ne Hesaplar | İkincil Bağlantı |
|-------|----------|-------------|-------------------|
| ARU-γ2-CMAT | [ARU] | Görsel-dokunsal-işitsel duygusal transfer (mPFC/OFC/insula) | F5 |
| IMU-β9-CMAPCC | [IMU] | Premotor kortekste modaliteden bağımsız dizi temsili (ortak kod) | F7 |
| PCU-β4-CHPI | [PCU] | Görsel+motor+işitsel → harmonik tahmin doğruluğu artışı | F2 |
| ASU-γ2-DGTP | [ASU] | Müzik-konuşma ortak zamansal işleme mekanizması | F3 |
| NDU-α2-SDD | [NDU] | Supramodal sapma algılama (duyular arası ortak mekanizma) | F2, F3 |

---

## Çapraz Kesişim Matrisi

> Bir modelin kaç fonksiyonel kategoriye dokunduğu

### Tek-Fonksiyonlu Modeller (Saf — sadece 1 kategori)

| Model | Kategori | Ne Yapar |
|-------|----------|----------|
| SPU-α1-BCH | F1 | Konsonans hiyerarşisi |
| SPU-α2-PSCL | F1 | Perde belirginliği |
| SPU-α3-PCCR | F1 | Kroma kodlama |
| SPU-γ1-SDNPS | F1 | FFR sınırları |
| SPU-γ3-SDED | F1 | Erken disonans tespiti |
| IMU-α2-PNH | F1 | Pisagor aralık hiyerarşisi |
| IMU-β8-TPRD | F1 | Tonotopi/perde ayrımı |
| IMU-β4-HCMC | F4 | Bellek konsolidasyon devresi |
| ARU-α3-VMM | F5 | Valans-mod haritalama |
| ARU-α1-SRP | F6 | Dopamin ödül yolağı |
| RPU-α1-DAED | F6 | Beklenti/tüketim dopamin ayrışması |
| RPU-α2-MORMR | F6 | Opioid haz mekanizması |
| RPU-γ2-IOTMS | F6 | Bireysel opioid duyarlılığı |
| MPU-α1-PEOM | F7 | Periyot entrainment |
| MPU-β4-SPMC | F7 | SMA→PMC→M1 motor devredsi |
| MPU-γ2-CTBB | F7 | Serebellar zamanlama |
| PCU-α1-HTP | F2 | Hiyerarşik zamansal tahmin |
| PCU-β1-PWUP | F2 | PE hassasiyet ağırlıklandırma |
| PCU-γ3-PSH | F2 | Tahmin sessizleştirme |
| ASU-α2-IACM | F3 | Armonik olmayan dikkat çekme |
| ASU-β2-STANM | F3 | Ağ topoloji yeniden yapılanması |
| ASU-γ3-SDL | F3 | Dinamik lateralizasyon |
| NDU-α3-EDNR | F8 | Uzmanlık ağ reorganizasyonu |
| NDU-γ3-ECT | F8 | Uzmanlaşma-esneklik dengesi |
| STU-γ3-MTNE | F8 | Sinirsel verimlilik |
| STU-γ4-PTGMP | F8 | Gri madde plastisitesi |
| IMU-β3-OII | F8 | Osilasyon-zeka bağlantısı |
| MPU-γ1-NSCP | F9 | Popülasyon senkronizasyonu → ticari tahmin |

> 28 model tek fonksiyon (saf modeller)

### Çift-Fonksiyonlu Modeller (2 kategoriye dokunan)

| Model | Birincil | İkincil | Köprü |
|-------|----------|---------|-------|
| SPU-β1-STAI | F5 Duygu | F6 Ödül | estetik → ödül |
| SPU-β3-MIAA | F1 Duyusal | F4 Bellek | imgeleme → bellek |
| STU-α3-MDNS | F1 Duyusal | F4 Bellek | algı = imgeleme |
| STU-α2-AMSC | F7 Motor | F1 Duyusal | auditorik → motor |
| STU-β1-AMSS | F3 Dikkat | F1 Duyusal | dikkat → akış ayrımı |
| STU-γ1-TMRM | F7 Motor | F4 Bellek | tempo hafızası |
| ARU-α2-AAC | F5 Duygu | F6 Ödül | otonom → dopamin |
| ARU-β2-CLAM | F5 Duygu | F10 Klinik | duygu düzenleme → terapi |
| ARU-β4-NEMAC | F5 Duygu | F4 Bellek | nostalji → bellek |
| ARU-γ1-DAP | F11 Gelişim | F6 Ödül | kritik dönem → ödül kapasitesi |
| ARU-γ2-CMAT | F12 Çapraz | F5 Duygu | çapraz modal → duygu |
| ARU-γ3-TAR | F10 Klinik | F5 Duygu | terapi → duygu düzenleme |
| ASU-α3-CSG | F3 Dikkat | F1 Duyusal | konsonans → belirginlik |
| ASU-β3-AACM | F3 Dikkat | F6 Ödül | estetik beğeni → dikkat |
| ASU-γ1-PWSM | F3 Dikkat | F2 Tahmin | hassasiyet → belirginlik |
| NDU-α1-MPG | F1 Duyusal | F2 Tahmin | onset → kontur gradyan |
| NDU-β2-CDMR | F2 Tahmin | F8 Öğrenme | bağlam → uyumsuzluk |
| NDU-β3-SLEE | F2 Tahmin | F8 Öğrenme | istatistiksel öğrenme |
| NDU-γ1-SDDP | F11 Gelişim | F10 Klinik | cinsiyet + erken doğan |
| NDU-γ2-ONI | F11 Gelişim | F10 Klinik | aşırı normalizasyon |
| PCU-α3-ICEM | F2 Tahmin | F5 Duygu | IC → duygu |
| PCU-β3-UDP | F2 Tahmin | F6 Ödül | belirsizlik → haz |
| PCU-γ2-MAA | F5 Duygu | F8 Öğrenme | maruziyet + kişilik |
| RPU-α3-RPEM | F6 Ödül | F2 Tahmin | ödül PE |
| RPU-β1-IUCP | F6 Ödül | F2 Tahmin | ters-U tercihi |
| RPU-γ1-LDAC | F6 Ödül | F1 Duyusal | beğeni → duyusal gating |
| RPU-γ3-SSPS | F6 Ödül | F2 Tahmin | eyer yüzeyi |
| ARU-β3-MAD | F6 Ödül | F10 Klinik | anhedonia |
| IMU-α1-MEAMN | F4 Bellek | F5 Duygu | otobiyografik → duygu |
| IMU-γ3-CDEM | F4 Bellek | F5 Duygu | bağlam → duygusal bellek |
| IMU-γ1-DMMS | F4 Bellek | F11 Gelişim | çocukluk bellek iskelesi |
| IMU-α3-MMP | F4 Bellek | F10 Klinik | Alzheimer direnci |
| IMU-β6-MSPBA | F1 Duyusal | F2 Tahmin | sentaks → tahmin |
| MPU-α2-MSR | F7 Motor | F8 Öğrenme | reorganizasyon |
| MPU-γ3-STC | F7 Motor | F8 Öğrenme | şarkı → bağlantı artışı |
| STU-β3-EDTA | F7 Motor | F8 Öğrenme | alan-spesifik uzmanlaşma |
| STU-γ5-MPFS | F7 Motor | F8 Öğrenme | akış durumu |
| PCU-α2-SPH | F2 Tahmin | F4 Bellek | tahmin → tanıma |
| RPU-β3-MEAMR | F6 Ödül | F4 Bellek | nostalji ödülü |
| RPU-β2-MCCN | F6 Ödül | F7 Motor | ürperme ağı motor bileşeni |
| NDU-α2-SDD | F2 Tahmin | F3 Dikkat | supramodal sapma |
| PCU-γ1-IGFE | F3 Dikkat | F4 Bellek | gama → hafıza |
| MPU-β1-ASAP | F7 Motor | F2 Tahmin | beat simülasyonu → tahmin |
| PCU-β2-WMED | F2 Tahmin | F7 Motor | entrainment ↔ bellek |
| ASU-α1-SNEM | F3 Dikkat | F7 Motor | seçici entrainment |
| ASU-β1-BARM | F3 Dikkat | F7 Motor | BAT → entrainment |
| STU-β2-TPIO | F1 Duyusal | F7 Motor | timbre algı → motor |
| ASU-γ2-DGTP | F3 Dikkat | F12 Çapraz | müzik-konuşma ortak |
| NDU-β1-DSP | F10 Klinik | F11 Gelişim | erken doğan + plastisite |
| IMU-γ2-CSSL | F4 Bellek | F11 Gelişim | evrimsel ortak mekanizma |
| IMU-β9-CMAPCC | F12 Çapraz | F7 Motor | ortak kod → motor |
| PCU-β4-CHPI | F2 Tahmin | F12 Çapraz | çapraz modal tahmin |

### Üç+ Fonksiyonlu Modeller (3 veya daha fazla kategoriye dokunan)

| Model | Kategoriler | Açıklama |
|-------|-------------|----------|
| STU-β4-ETAM | F3+F7+F2 | Dikkat + motor + tahmin hepsi birlikte |
| STU-β5-HGSIC | F7+F6+F1 | Motor groove + ödül hazzı + duyusal gama |
| STU-β6-OMS | F7+F9+F3 | Motor senkronizasyon + sosyal + dikkat |
| STU-γ2-NEWMD | F7+F2+F3 | Motor + tahmin + dikkat paradoksu |
| IMU-β1-RASN | F10+F7+F8 | Klinik + motor + plastisite |
| IMU-β2-PMIM | F2+F4+F8 | Tahmin + bellek + öğrenme |
| IMU-β5-RIRI | F10+F7+F8 | Klinik + motor + plastisite (multimodal) |
| IMU-β7-VRIAP | F10+F7+F1 | Klinik + motor + duyusal (ağrı kesme) |
| MPU-α3-GSSM | F7+F10 | Motor + klinik (yürüyüş) |
| MPU-β2-DDSMI | F7+F9 | Motor + sosyal (çift dansı) |
| MPU-β3-VRMSME | F7+F10 | Motor + klinik (VR rehabilitasyon) |
| RPU-β4-SSRI | F6+F9 | Ödül + sosyal senkronizasyon |
| NDU-α2-SDD | F2+F3+F12 | Tahmin + dikkat + çapraz-modal |
| ARU-β1-PUPF | F6+F2 | Ödül + tahmin (Goldilocks) |

---

## Özet: Fonksiyonel Dağılım

```
F7  Motor & Zamanlama      ████████████████████░  21 model
F2  Tahmin & Örüntü        ██████████████████░░░  18 model
F6  Ödül & Motivasyon      ████████████████░░░░░  16 model
F1  Duyusal İşleme         ██████████████░░░░░░░  14 model
F3  Dikkat & Önemlilik     ██████████████░░░░░░░  14 model
F8  Öğrenme & Plastisite   ██████████████░░░░░░░  14 model
F4  Bellek Sistemleri      ████████████░░░░░░░░░  12 model
F5  Duygu & Valans         ███████████░░░░░░░░░░  11 model
F10 Klinik & Terapötik     ██████████░░░░░░░░░░░  10 model
F11 Gelişim & Evrim        ██████░░░░░░░░░░░░░░░   6 model
F12 Çapraz-Modal           █████░░░░░░░░░░░░░░░░   5 model
F9  Sosyal Biliş           ████░░░░░░░░░░░░░░░░░   4 model
```

### Ünite → Fonksiyon Dağılım Tablosu

> Her ünite hangi fonksiyonlara kaç modelle katkıda bulunuyor?

| Ünite | F1 | F2 | F3 | F4 | F5 | F6 | F7 | F8 | F9 | F10 | F11 | F12 |
|-------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:---:|:---:|:---:|
| SPU(9) | **7** | — | — | 1 | 1 | 1 | — | 2 | — | — | — | — |
| STU(14) | 3 | 2 | 3 | 2 | — | 1 | **10** | 4 | 1 | — | — | — |
| IMU(15) | 3 | 2 | — | **6** | 2 | — | 2 | 1 | — | 4 | 2 | 1 |
| ARU(10) | — | 1 | — | 1 | **6** | **4** | — | — | — | 2 | 1 | 1 |
| ASU(9) | 1 | 1 | **8** | — | — | 1 | 3 | — | — | — | — | 1 |
| NDU(9) | 1 | 3 | 1 | — | — | — | — | **4** | — | 1 | 2 | 1 |
| MPU(10) | — | 1 | — | — | — | — | **9** | 2 | 2 | 2 | — | — |
| PCU(10) | — | **7** | 1 | 2 | 2 | 2 | 1 | 1 | — | — | — | 1 |
| RPU(10) | 1 | 4 | — | 1 | — | **9** | 1 | — | 1 | 1 | — | — |

> **Koyu** = ünite-fonksiyon en güçlü eşleşme. Dikkat: çapraz katkılar önemli.

### Kritik Gözlemler

1. **Motor (F7)** en kalabalık kategori — 21 model. Müzik beyin modellemesinde motor sistem merkezi konumda.
2. **Tahmin (F2)** 18 modelle ikinci — tahmin hatası tüm üniteleri kesiyor (PCU, RPU, NDU, IMU, ASU, STU).
3. **Ödül (F6)** 16 model — ARU ve RPU dışında SPU, ASU, PCU bile ödüle dokunuyor.
4. **SPU → F1 uyumu güçlü** (7/9 model saf duyusal) ama STU, IMU, ARU çok dağınık.
5. **IMU en heterojen ünite**: 15 modeli 9 farklı kategoriye dağılmış — bellek (6) + klinik (4) + gelişim (2) + duyusal (3) + tahmin (2) + duygu (2) + motor (2) + öğrenme (1) + çapraz-modal (1).
6. **Klinik (F10)** modelleri 4 farklı üniteden geliyor: IMU(4), MPU(2), ARU(2), NDU(2) — hiçbir ünite bunu tek başına temsil etmiyor.
7. **Sosyal (F9)** en az temsil edilen (4 model) — gelecek genişleme alanı.
