# Branch-Consonance — Model Priority

Group A [0:7] dışında kaç farklı R³ index'e ihtiyaç duyuyor?
Az = consonance branch ile daha kolay test edilebilir.

| # | Model | Unit | Tier | Non-A R³ | Groups Needed |
|---|-------|------|------|----------|---------------|
| 1 | BCH | SPU | α | **10** | C, G, H, J, K |
| 2 | SDED | SPU | γ | **10** | C, G, J |
| 3 | DAP | ARU | γ | **12** | B, C, D, F, J |
| 4 | IOTMS | RPU | γ | **14** | B, C, F, J |
| 5 | MEAMR | RPU | β | **14** | B, C, D, G, K |
| 6 | NEMAC | ARU | β | **14** | B, C, D, F, K |
| 7 | CMAT | ARU | γ | **14** | B, C, D, F, J, K |
| 8 | TAR | ARU | γ | **14** | B, C, D, F |
| 9 | CLAM | ARU | β | **15** | B, C, D, F, J |
| 10 | MAD | ARU | β | **15** | B, C, D, F, K |
| 11 | SDNPS | SPU | γ | **15** | C, G, J |
| 12 | PWSM | ASU | γ | **15** | B, D, F, G, K |
| 13 | IACM | ASU | α | **16** | B, C, D, F, J |
| 14 | CSG | ASU | α | **16** | B, C, D, F, H, J |
| 15 | AACM | ASU | β | **16** | B, C, D, F, K |
| 16 | DAED | RPU | α | **16** | B, D, F, K |
| 17 | IUCP | RPU | β | **16** | B, D, F, J, K |
| 18 | MCCN | RPU | β | **16** | B, D, F, K |
| 19 | SSPS | RPU | γ | **16** | B, D, F, K |
| 20 | LDAC | RPU | γ | **16** | B, C, D, F, K |
| 21 | PWUP | PCU | β | **16** | B, C, D, G, J, K |
| 22 | UDP | PCU | β | **18** | B, C, D, G, J, K |
| 23 | NSCP | MPU | γ | **21** | B, D, F, J |
| 24 | TSCP | SPU | β | **21** | C, D, G, K |
| 25 | MAA | PCU | γ | **21** | C, D, G, J, K |
| 26 | SSRI | RPU | β | **22** | B, C, D, F, J, K |
| 27 | EDNR | NDU | α | **23** | B, C, F, J, K |
| 28 | MORMR | RPU | α | **24** | B, C, D, F, G, K |
| 29 | RPEM | RPU | α | **24** | B, D, F, K |
| 30 | PSH | PCU | γ | **24** | B, C, D, F, G, K |
| 31 | SDD | NDU | α | **25** | B, D, F, G, J, K |
| 32 | PCCR | SPU | α | **25** | C, D, G, H, J |
| 33 | STAI | SPU | β | **25** | B, C, D, F, J, K |
| 34 | MPG | NDU | α | **25** | B, C, D, F, K |
| 35 | PUPF | ARU | β | **26** | B, C, D, F, K |
| 36 | CDEM | IMU | γ | **27** | B, C, D, F, G, K |
| 37 | SPH | PCU | α | **27** | B, C, D, F, G, H, J |
| 38 | PNH | IMU | α | **28** | B, C, F, G, H, J |
| 39 | MDNS | STU | α | **28** | B, C, D, F, H, J |
| 40 | ICEM | PCU | α | **29** | B, C, D, F, G, J, K |
| 41 | CMAPCC | IMU | β | **31** | B, F, G, J |
| 42 | MSPBA | IMU | β | **33** | B, D, F, G, J, K |
| 43 | VRIAP | IMU | β | **33** | B, C, D, F, G |
| 44 | PMIM | IMU | β | **35** | B, C, D, F, G, K |
| 45 | HCMC | IMU | β | **35** | B, C, D, F, G, K |
| 46 | OII | IMU | β | **36** | B, C, D, F, G, J |
| 47 | RIRI | IMU | β | **36** | B, C, D, F, G, J |
| 48 | ESME | SPU | γ | **37** | B, C, D, F, G, H |
| 49 | DMMS | IMU | γ | **37** | B, C, D, F, G, H, K |
| 50 | RASN | IMU | β | **37** | B, D, F, G, J |
| 51 | TPRD | IMU | β | **38** | B, C, D, F, G, H, J |
| 52 | CSSL | IMU | β | **39** | B, C, D, F, G, H, J |
| 53 | PSCL | SPU | α | **39** | C, D, F, G, H, J |
| 54 | MIAA | SPU | β | **41** | B, C, D, F, G, H, K |
| 55 | MEAMN | IMU | α | **43** | B, C, D, F, G, J, K |
| 56 | SRP | ARU | α | **44** | B, C, D, F, G, K |
| 57 | MMP | IMU | α | **45** | B, C, D, F, G, H, J, K |
| 58 | CHPI | PCU | β | **47** | B, C, D, F, G, H, J, K |

## Segmentler

```
Non-A R³ ≤ 15:   12 model — consonance-ağırlıklı, az dış bağımlılık
Non-A R³ 16-20:   9 model — orta bağımlılık
Non-A R³ 21-30:  16 model — geniş bağımlılık
Non-A R³ 31+:    21 model — çok geniş, birden fazla branch gerektirir
```

## Top 12 — Consonance-Ağırlıklı Modeller

| Model | Unit | Non-A | Consonance R³ | Oran |
|-------|------|-------|---------------|------|
| BCH | SPU-α | 10 | 0,2,3,5,6 | 5:10 |
| SDED | SPU-γ | 10 | 0,1,2,5 | 4:10 |
| DAP | ARU-γ | 12 | 0,4 | 2:12 |
| IOTMS | RPU-γ | 14 | 0,4 | 2:14 |
| MEAMR | RPU-β | 14 | 4 | 1:14 |
| NEMAC | ARU-β | 14 | 0,4 | 2:14 |
| CMAT | ARU-γ | 14 | 0,4 | 2:14 |
| TAR | ARU-γ | 14 | 0,4 | 2:14 |
| CLAM | ARU-β | 15 | 0,4 | 2:15 |
| MAD | ARU-β | 15 | 0,4 | 2:15 |
| SDNPS | SPU-γ | 15 | 0,2,5 | 3:15 |
| PWSM | ASU-γ | 15 | 4 | 1:15 |

## Sonuc

Hicbir model sadece A[0:7] ile calismiyor — minimum 10 dış R³ index.
BCH ve SDED en az dış bağımlılığa sahip (10).
Tum modeller en az B (Energy) veya D (Change) grubuna ihtiyac duyuyor.
