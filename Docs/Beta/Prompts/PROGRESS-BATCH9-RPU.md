# BATCH 9: RPU (Reward Processing) — Progress Tracker

**Chat Assignment:** Chat 7
**Unit:** RPU (Reward Processing)
**Total Models:** 10 (#87-#96)
**Status:** COMPLETE (10/10)
**Last Updated:** 2026-02-13

---

## Models

- [x] #87 RPU-α1-DAED — Dopamine Anticipation-Experience Dissociation ✅ v2.1.0 (6 papers, corrected N/effect sizes, +5 new citations)
- [x] #88 RPU-α2-MORMR — mu-Opioid Receptor Music Reward ✅ v2.1.0 (3 papers, corrected reference/journal, +2 citations)
- [x] #89 RPU-α3-RPEM — Reward Prediction Error in Music ✅ v2.1.0 (4 papers, disambiguated Gold 2023a/b, +3 new citations)
- [x] #90 RPU-β1-IUCP — Inverted-U Complexity Preference ✅ v2.1.0 (3 papers, corrected method/p-values, +2 new citations with fMRI evidence)
- [x] #91 RPU-β2-MCCN — Musical Chills Cortical Network ✅ v2.1.0 (3 papers, corrected method HD-EEG not fMRI, added N=18, +2 PET citations)
- [x] #92 RPU-β3-MEAMR — Music-Evoked Autobiographical Memory Reward ✅ v2.1.0 (2 papers, corrected N=13, added brain regions from Table 2, +1 PET citation)
- [x] #93 RPU-β4-SSRI — Social Synchrony Reward Integration ✅ v2.1.0 (NEW model created + literature-reviewed; 17 papers, 11D output, 18 H³ tuples; 13/17 verified in catalog; added Spiech 2022, Mori & Zatorre 2024, Nguyen 2023, Salimpoor 2011, Cheung 2019, Gold 2019)
- [x] #94 RPU-γ1-LDAC — Liking-Dependent Auditory Cortex ✅ v2.1.0 (6 papers, corrected effect sizes from d=0.18/1.22 to t-stats, added N=24, journal=Front.Neurosci., +5 new citations: Cheung 2019, Martinez-Molina 2016, Gold 2019b, Mori & Zatorre 2024, Kim 2019; expanded brain regions 1->5 with MNI; 8 doc-code mismatches logged; 2 R³ gaps filed)
- [x] #95 RPU-γ2-IOTMS — Individual Opioid Tone Music Sensitivity ✅ v2.1.0 (5 papers, corrected author list/journal/N from Putkinen 2025, +4 new citations: Salimpoor 2011 PET-DA, Mas-Herrero 2014 behavioral, Martinez-Molina 2016 fMRI, Loui 2017 DTI; expanded brain regions 2->8 with MNI from primary sources; falsification 1/5->5/7 confirmed; 10 doc-code mismatches logged; no R³ gaps)
- [x] #96 RPU-γ3-SSPS — Saddle-Shaped Preference Surface ✅ v2.1.0 (8 papers, corrected citations from fictitious Gold 2023 to Cheung 2019 primary + Gold 2019b/2023 replications, expanded 7 brain regions with MNI, +7 new citations, 7/7 falsification criteria confirmed)

## Notes

- RPU-β4-SSRI created and literature-reviewed (2026-02-13). New model with 11D output (5E + 2M + 2P + 2F). Models social synchrony reward integration — how interpersonal neural synchronization during group music-making generates hedonic reward through prefrontal-limbic pathways. Key innovation: Social Prediction Error (SPE) extending RPEM to interpersonal coordination. 17 papers across fNIRS hyperscanning, EEG, MEG, fMRI, PET, pupillometry, behavioral methods. 4 canonical papers (Dunbar 2012, Tarr 2014, Kokal 2011, Novembre 2012) not in catalog but cited per Beta_upgrade.md spec as supporting evidence for the social synchrony → reward pathway.

- RPU-γ1-LDAC revised (2026-02-13). **Key corrections**: v2.0.0 reported effect sizes as "d=0.18" and "d=1.22" which were actually t-statistics: t(23)=2.56, p=0.018 (STG-liking coupling) and t(23)=2.92, p=0.008 (IC x liking interaction). Missing N=24 and journal (Frontiers in Neuroscience 17:1209398) now corrected. The paper is Gold et al. 2023a (not the RPE study Gold 2019a). Evidence expanded 1->6 papers from 4 independent labs: (1) Gold/Zatorre group: 2023a fMRI N=24, 2019b behavioral N=70; (2) Cheung/Koelsch group: 2019 fMRI N=40 bilateral AC uncertainty x surprise; (3) Martinez-Molina/Marco-Pallares group: 2016 fMRI N=45 STG-NAcc PPI in anhedonia; (4) Mori/Zatorre: 2024 fMRI N=49 auditory-reward connectivity. Brain regions expanded from R STG only to 5 regions (R STG, bilateral AC, NAcc/VS, amygdala/hippocampus) with literature MNI coordinates. Falsification criteria 2/5 -> 3/5 confirmed (added reward-connectivity gating from Martinez-Molina anhedonia PPI). 8 doc-code mismatches logged in Section 12.1 (code is 10D stub vs doc 6D, wrong FULL_NAME, empty h3_demand, single mechanism). 2 R³ gaps filed: GAP-RPU-004 (melodic entropy dimension, medium-high priority) and GAP-RPU-005 (bilateral AC lateralization, low priority).

- RPU-γ3-SSPS revised (2026-02-13). **Critical correction**: v2.0.0 cited fictitious "Gold 2023" with fabricated d=0.48 as sole reference. Actual primary source: Cheung et al. (2019) *Current Biology* (N=79, saddle-shaped IC x entropy interaction, beta=-0.124, p=0.000246). Gold et al. 2023 exists in *Frontiers in Neuroscience* (N=24) as fMRI replication. Evidence expanded 1->8 papers from 3 independent labs (Koelsch/Cheung, Zatorre/Gold, Kim/Fritz). Brain regions expanded 2->7 with literature-verified MNI. Falsification 2/5->7/7 confirmed. 8 doc-code mismatches logged (code is stub with wrong name/dim/mechanisms). No R³ gaps found.

- RPU-γ2-IOTMS revised (2026-02-13). **Key corrections**: v2.0.0 had incomplete Putkinen 2025 citation (missing authors, journal, N). Corrected to: Putkinen, Seppala, Harju, Hirvonen, Karlsson, & Nummenmaa (2025), *Eur J Nucl Med Mol Imaging* 52:3540-3549. N=15 (PET, all female) + 30 (fMRI). Primary effect: NAcc BPND negatively correlated with chills (r=-0.52, p<0.05); baseline MOR predicted pleasure-BOLD in insula, ACC, SMA, STG, NAcc, thalamus. Evidence expanded 1->5 papers with cross-method convergence: (1) Putkinen 2025 PET-MOR N=15/30; (2) Salimpoor 2011 PET-DA N=8/7, NAcc BP vs chills r=0.84; (3) Mas-Herrero 2014 behavioral N=30, BMRQ→SCR slope R²=0.32; (4) Martinez-Molina 2016 fMRI N=45, reduced NAcc for music in anhedonics, BMRQ→pleasure R²=0.40; (5) Loui 2017 DTI N=47, STG-NAcc tract volumes predict BMRQ R²=0.38. Brain regions expanded 2->8 with MNI from primary sources. Falsification 1/5->5/7 confirmed (MOR-pleasure slope, striatal release, individual differences, musical specificity, structural connectivity). 10 doc-code mismatches logged (code has wrong FULL_NAME "Individual Optimal Tempo Matching System", OUTPUT_DIM=10 vs doc 5, MECHANISM_NAMES=("BEP",) vs doc ("AED","CPD","C0P"), empty h3_demand, wrong NAcc MNI). No R³ gaps found.
