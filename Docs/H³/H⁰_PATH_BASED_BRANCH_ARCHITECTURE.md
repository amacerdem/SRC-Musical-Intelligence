# H⁰ Path-Based Branch Architecture (Deterministic, Demand-Driven)

## Objective

Bu belge, H⁰ için yeni deterministic path/branch yaklaşımını code-truth talep verisi ile sabitler:

1. Neden `S0[256] -> mean(dim=-1) -> scalar` yaklaşımı yetersiz?
2. Path-based/branch-based H⁰ nasıl çalışır?
3. `EH/HMorph/HL` kartları path üstünde nasıl seçilir?
4. Toplam boyut (D) baseline vs model-selective durumda ne olur?
5. D0 teacher ve T1 student ayrımında bu mimarinin rolü nedir?

---

## Canonical Notation

- `s`: S⁰ dimension index (`0..255`)
- `EH`: Event Horizon (`0..31`)
- `HMorph`: Morph index (`0..23`)
- `HL`: H-Law (`L0=forward`, `L1=backward`, `L2=bidirectional`)
- `H0 tuple`: `(EH, HMorph, HL)`
- `H0 path leaf`: `(s, EH, HMorph, HL)`
- `M(s)`: model seti (S⁰ dim `s` kullanan modeller)
- `T(m)`: model `m` için H⁰ tuple seti
- `U(s)`: `s` için tuple birleşimi `U(s)=⋃_{m∈M(s)} T(m)`

---

## 1) Sorun: Scalar Collapse

Mevcut klasik H⁰ çizgisinde çok modelde görülen pattern:

```text
S0[256] --(window, law, morph)--> [256] --mean(dim=-1)--> [1]
```

Bu, aşağıdaki kayba yol açar:

- `L0-T` ile `L5-harmonicity` gibi farklı fiziksel kaynaklar tek scalar içinde karışır.
- Downstream hangi S⁰ kaynağının hangi H⁰ karta katkı verdiğini path seviyesinde izleyemez.
- TDH/provenance leaf seviyesi kaybolur.

---

## 2) Çözüm: Deterministic Path -> Branch

Yeni yaklaşımda her S⁰ dim bağımsız path olarak H⁰’a girer:

```text
S0[s] -> branch by demand -> {(EH,HMorph,HL) leaves}
```

Kritik nokta:

- Bu yapı dense `a x b` tensör üretimi değildir.
- H⁰ çıktısı, her `s` için gerçekten talep edilen tuple leaf’lerinin toplamıdır.
- Her leaf tam izlenebilir: `(s, EH, HMorph, HL)`.

---

## 3) Demand Contract (Code-Truth)

Kaynaklar:

- `Library/Auditory/C⁰/C⁰_Core_demand.md`
- `Library/Auditory/R⁰/R⁰_Core_demand.md`
- `Pipeline/A0/D0/h0/tensor/downstream_hc0.py`

Sabit tuple uzayı:

- C⁰ unique tuple: `90`
- R⁰ (declared H⁰ path) unique tuple: `41`
- C⁰ ∩ R⁰ tuple overlap: `0`

Yani H⁰ üst-sınır (path ama selectivity yok):

- `C0: 256 x 90 = 23,040D`
- `R0: 25 x 41 = 1,025D`
- `Toplam = 24,065D`

---

## 4) Model-Level S⁰ Selectivity ile Optimizasyon

Bu belgede kullanılan exact hesap (93 model + S⁰ mapping parse):

- `Total models = 93`
- `C0_H0 = Σ_{s=0..255} |U(s)| = 13,466D`
- `R0_H0 = 25 x 41 = 1,025D`
- `Grand total = 14,491D`

Karşılaştırma:

| Scenario | C0 H0 | R0 H0 | Toplam | Not |
|---|---:|---:|---:|---|
| Naive path baseline | 23,040 | 1,025 | 24,065 | Her C0 tuple her S0 dim için hesap |
| Model-selective path | 13,466 | 1,025 | 14,491 | `U(s)` demand birleşimi ile |
| Kazanç | 9,574 | 0 | 9,574 | `%39.78` toplam azalma |

Ek oranlar:

- `14,491 / 2,304 = 6.29x` (mevcut flat H⁰’e göre)
- Baseline path `24,065 / 2,304 = 10.44x`

---

## 5) Morph Semantics (Path Modunda)

Önceki ayrım:

- Per-feature morphlar: `M0..M16, M19` (18 adet)
- Cross-feature morphlar: `M17, M18, M20, M21, M22, M23` (6 adet)

Path modunda her leaf tek `s` path’iyle çalıştığı için pratikte tüm morphlar aynı contract’a oturur:

```text
input: S0[s] timeseries/window
output: scalar leaf for one (s,EH,HMorph,HL)
```

Yani cross-feature morphların küresel 256→1 indirgeme zorunluluğu ortadan kalkar; indirgeme artık path’in kendisiyle doğal olur.

---

## 6) Layer-Level Etki (C⁰ H⁰ Üzerinde)

Model-selective hesap sonucunda C⁰ katkısı:

| Layer | Range | Used dims | Layer contribution (D) |
|---|---|---:|---:|
| L0 | `[0:4)` | 4/4 | 273 |
| L1 | `[4:10)` | 0/6 | 0 |
| L2 | `[10:14)` | 0/4 | 0 |
| L3 | `[14:15)` | 1/1 | 87 |
| L4 | `[15:30)` | 12/15 | 979 |
| L5 | `[30:55)` | 25/25 | 1,710 |
| L6 | `[55:80)` | 25/25 | 1,721 |
| L7 | `[80:104)` | 24/24 | 1,863 |
| L9 | `[104:128)` | 24/24 | 1,665 |
| X | `[128:256)` | 80/128 | 5,168 |

Toplam: `13,466D`

---

## 7) Deterministic Routing Contract

Her `s` için runtime sözleşmesi:

1. `consumer_models = models_using_s[s]`
2. `tuple_set = union(model_tuple_map[m] for m in consumer_models)`
3. Sadece `tuple_set` için H⁰ leaf üret
4. Leaf provenance kaydı: `(s, EH, HMorph, HL, consumers)`

Bu yüzden yapı tamamen deterministic ve whitebox kalır.

---

## 8) Engineering Notes (Uygulama Sırası)

1. H⁰ extractor path API:
   - flat `(B,T,2304)` yanında optional sparse leaf API
   - `emit_leaf(s, eh, m, l, value)`
2. `downstream_hc0.py` ve model registry ile `model -> tuple set` cache
3. C⁰ model dokümanlarından `model -> S0 dims` registry
4. Runtime branch planner:
   - precompute `U(s)`
   - CUDA batch grouping by identical tuple patterns
5. TDH lineage:
   - leaf-level provenance schema `(s,eh,m,l)`

---

## 9) Quality Status (Coverage Sync)

Model dosyalarındaki `**Total S⁰ Input Coverage**` satırları index tablosu parse sonuçlarıyla senkronize edilmiştir. Güncel durumda mismatch yoktur (`0/93`).

Yine de hesaplama için güvenilir kaynak sırası değişmez:

1. Index tablosu parse (birincil)
2. Declared coverage satırı (ikincil kontrol)

---

## Conclusion

Path-based branch H⁰, whitebox traceability hedefini korurken gerçek model talebine göre boyutu `24,065D` baseline’dan `14,491D` seviyesine indirir. Bu, D0 teacher’da bilgi kaybını engelleyip hesaplamayı demand-driven tutan pratik optimumdur.
