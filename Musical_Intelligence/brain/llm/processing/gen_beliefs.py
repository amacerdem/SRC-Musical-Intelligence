"""Generate beliefs.jsonl from M3-LOGOS.md belief tables.

Usage:
    python -m Musical_Intelligence.brain.llm.processing.gen_beliefs

Reads the M3-LOGOS.md §6 tables and generates structured belief cards
with bilingual descriptions, parent dimension mappings, and tier info.
"""

import json
from pathlib import Path

OUTPUT = Path(__file__).parent.parent / "knowledge" / "beliefs.jsonl"

# ── Belief registry: 131 beliefs from M3-LOGOS §6 ──────────────────
# Format: (index, key, type, mechanism, cluster_24d, function)

BELIEFS = [
    # F1: Sensory Processing (0-16)
    (0, "consonance_salience_gradient", "Appraisal", "CSG", "sensory_encoding", "F1"),
    (1, "contour_continuation", "Anticipation", "MPG", "pitch_melody", "F1"),
    (2, "melodic_contour_tracking", "Appraisal", "MPG", "pitch_melody", "F1"),
    (3, "consonance_trajectory", "Anticipation", "BCH", "information_entropy", "F1"),
    (4, "harmonic_stability", "Core", "BCH", "harmonic_tension", "F1"),
    (5, "harmonic_template_match", "Appraisal", "BCH", "harmonic_tension", "F1"),
    (6, "interval_quality", "Appraisal", "BCH", "harmonic_tension", "F1"),
    (7, "pitch_continuation", "Anticipation", "PSCL", "information_entropy", "F1"),
    (8, "pitch_prominence", "Core", "PSCL", "pitch_melody", "F1"),
    (9, "octave_equivalence", "Appraisal", "PCCR", "pitch_melody", "F1"),
    (10, "pitch_identity", "Core", "PCCR", "pitch_melody", "F1"),
    (11, "aesthetic_quality", "Core", "STAI", "aesthetic_appraisal", "F1"),
    (12, "reward_response_pred", "Anticipation", "STAI", "aesthetic_appraisal", "F1"),
    (13, "spectral_temporal_synergy", "Appraisal", "STAI", "sensory_encoding", "F1"),
    (14, "imagery_recognition", "Anticipation", "MIAA", "aesthetic_appraisal", "F1"),
    (15, "timbral_character", "Core", "MIAA", "sensory_salience", "F1"),
    (16, "spectral_complexity", "Appraisal", "SDED", "sensory_encoding", "F1"),
    # F2: Pattern Recognition & Prediction (17-31)
    (17, "abstract_future", "Anticipation", "HTP", "information_entropy", "F2"),
    (18, "hierarchy_coherence", "Appraisal", "HTP", "sequence_learning", "F2"),
    (19, "midlevel_future", "Anticipation", "HTP", "information_entropy", "F2"),
    (20, "prediction_accuracy", "Core", "HTP", "predictive_processing", "F2"),
    (21, "prediction_hierarchy", "Core", "HTP", "predictive_processing", "F2"),
    (22, "arousal_change_pred", "Anticipation", "ICEM", "autonomic_arousal", "F2"),
    (23, "arousal_scaling", "Appraisal", "ICEM", "autonomic_arousal", "F2"),
    (24, "defense_cascade", "Appraisal", "ICEM", "sequence_learning", "F2"),
    (25, "information_content", "Core", "ICEM", "sequence_learning", "F2"),
    (26, "valence_inversion", "Appraisal", "ICEM", "autonomic_arousal", "F2"),
    (27, "valence_shift_pred", "Anticipation", "ICEM", "aesthetic_appraisal", "F2"),
    (28, "error_propagation", "Appraisal", "SPH", "predictive_processing", "F2"),
    (29, "oscillatory_signature", "Appraisal", "SPH", "sequence_learning", "F2"),
    (30, "sequence_completion", "Anticipation", "SPH", "information_entropy", "F2"),
    (31, "sequence_match", "Core", "SPH", "sequence_learning", "F2"),
    # F3: Attention & Salience (32-46)
    (32, "consonance_valence_mapping", "Appraisal", "CSG", "pitch_melody", "F3"),
    (33, "processing_load_pred", "Anticipation", "CSG", "sensory_encoding", "F3"),
    (34, "salience_network_activation", "Core", "CSG", "sensory_salience", "F3"),
    (35, "sensory_load", "Appraisal", "CSG", "sensory_encoding", "F3"),
    (36, "attention_capture", "Core", "IACM", "sensory_salience", "F3"),
    (37, "attention_shift_pred", "Anticipation", "IACM", "sensory_salience", "F3"),
    (38, "object_segregation", "Appraisal", "IACM", "sensory_salience", "F3"),
    (39, "precision_weighting", "Appraisal", "IACM", "sensory_encoding", "F3"),
    (40, "aesthetic_engagement", "Appraisal", "AACM", "aesthetic_appraisal", "F3"),
    (41, "savoring_effect", "Appraisal", "AACM", "aesthetic_appraisal", "F3"),
    (42, "beat_entrainment", "Core", "SNEM", "oscillation_coupling", "F3"),
    (43, "beat_onset_pred", "Anticipation", "SNEM", "oscillation_coupling", "F3"),
    (44, "meter_hierarchy", "Core", "SNEM", "oscillation_coupling", "F3"),
    (45, "meter_position_pred", "Anticipation", "SNEM", "oscillation_coupling", "F3"),
    (46, "selective_gain", "Appraisal", "SNEM", "oscillation_coupling", "F3"),
    # F4: Memory & Retrieval (47-59)
    (47, "melodic_recognition", "Appraisal", "MMP", "hippocampal_binding", "F4"),
    (48, "memory_preservation", "Appraisal", "MMP", "hippocampal_binding", "F4"),
    (49, "memory_scaffold_pred", "Anticipation", "MMP", "hippocampal_binding", "F4"),
    (50, "autobiographical_retrieval", "Core", "MEAMN", "autobiographical", "F4"),
    (51, "emotional_coloring", "Core", "MEAMN", "autobiographical", "F4"),
    (52, "memory_vividness", "Appraisal", "MEAMN", "autobiographical", "F4"),
    (53, "nostalgia_intensity", "Core", "MEAMN", "autobiographical", "F4"),
    (54, "retrieval_probability", "Appraisal", "MEAMN", "hippocampal_binding", "F4"),
    (55, "self_relevance", "Appraisal", "MEAMN", "autobiographical", "F4"),
    (56, "vividness_trajectory", "Anticipation", "MEAMN", "autobiographical", "F4"),
    (57, "consolidation_strength", "Appraisal", "HCMC", "hippocampal_binding", "F4"),
    (58, "episodic_boundary", "Appraisal", "HCMC", "hippocampal_binding", "F4"),
    (59, "episodic_encoding", "Core", "HCMC", "hippocampal_binding", "F4"),
    # F5: Emotion (60-73)
    (60, "ans_dominance", "Appraisal", "AAC", "autonomic_arousal", "F5"),
    (61, "chills_intensity", "Appraisal", "AAC", "sensory_salience", "F5"),
    (62, "driving_signal", "Appraisal", "AAC", "autonomic_arousal", "F5"),
    (63, "emotional_arousal", "Core", "AAC", "autonomic_arousal", "F5"),
    (64, "emotion_certainty", "Appraisal", "VMM", "valence_mode", "F5"),
    (65, "happy_pathway", "Appraisal", "VMM", "valence_mode", "F5"),
    (66, "mode_detection", "Appraisal", "VMM", "valence_mode", "F5"),
    (67, "perceived_happy", "Core", "VMM", "valence_mode", "F5"),
    (68, "perceived_sad", "Core", "VMM", "valence_mode", "F5"),
    (69, "sad_pathway", "Appraisal", "VMM", "nostalgia_circuitry", "F5"),
    (70, "nostalgia_affect", "Core", "NEMAC", "nostalgia_circuitry", "F5"),
    (71, "nostalgia_peak_pred", "Anticipation", "NEMAC", "nostalgia_circuitry", "F5"),
    (72, "self_referential_nostalgia", "Appraisal", "NEMAC", "nostalgia_circuitry", "F5"),
    (73, "wellbeing_enhancement", "Anticipation", "NEMAC", "nostalgia_circuitry", "F5"),
    # F6: Reward & Motivation (74-89)
    (74, "da_caudate", "Appraisal", "DAED", "dopaminergic_drive", "F6"),
    (75, "da_nacc", "Appraisal", "DAED", "dopaminergic_drive", "F6"),
    (76, "dissociation_index", "Appraisal", "DAED", "dopaminergic_drive", "F6"),
    (77, "temporal_phase", "Appraisal", "DAED", "dopaminergic_drive", "F6"),
    (78, "wanting_ramp", "Anticipation", "DAED", "dopaminergic_drive", "F6"),
    (79, "chills_proximity", "Anticipation", "SRP", "hedonic_valuation", "F6"),
    (80, "harmonic_tension", "Appraisal", "SRP", "harmonic_tension", "F6"),
    (81, "liking", "Core", "SRP", "hedonic_valuation", "F6"),
    (82, "peak_detection", "Appraisal", "SRP", "harmonic_tension", "F6"),
    (83, "pleasure", "Core", "SRP", "hedonic_valuation", "F6"),
    (84, "prediction_error", "Core", "SRP", "predictive_processing", "F6"),
    (85, "prediction_match", "Appraisal", "SRP", "predictive_processing", "F6"),
    (86, "resolution_expectation", "Anticipation", "SRP", "hedonic_valuation", "F6"),
    (87, "reward_forecast", "Anticipation", "SRP", "hedonic_valuation", "F6"),
    (88, "tension", "Core", "SRP", "harmonic_tension", "F6"),
    (89, "wanting", "Core", "SRP", "hedonic_valuation", "F6"),
    # F7: Motor & Timing (90-106)
    (90, "auditory_motor_coupling", "Appraisal", "HGSIC", "auditory_motor", "F7"),
    (91, "beat_prominence", "Appraisal", "HGSIC", "auditory_motor", "F7"),
    (92, "groove_quality", "Core", "HGSIC", "auditory_motor", "F7"),
    (93, "groove_trajectory", "Anticipation", "HGSIC", "auditory_motor", "F7"),
    (94, "meter_structure", "Appraisal", "HGSIC", "hierarchical_context", "F7"),
    (95, "motor_preparation", "Appraisal", "HGSIC", "auditory_motor", "F7"),
    (96, "kinematic_efficiency", "Core", "PEOM", "motor_period_locking", "F7"),
    (97, "next_beat_pred", "Anticipation", "PEOM", "motor_period_locking", "F7"),
    (98, "period_entrainment", "Core", "PEOM", "motor_period_locking", "F7"),
    (99, "period_lock_strength", "Appraisal", "PEOM", "motor_period_locking", "F7"),
    (100, "timing_precision", "Appraisal", "PEOM", "motor_period_locking", "F7"),
    (101, "context_depth", "Core", "HMCE", "hierarchical_context", "F7"),
    (102, "long_context", "Appraisal", "HMCE", "hierarchical_context", "F7"),
    (103, "medium_context", "Appraisal", "HMCE", "hierarchical_context", "F7"),
    (104, "phrase_boundary_pred", "Anticipation", "HMCE", "structural_prediction", "F7"),
    (105, "short_context", "Appraisal", "HMCE", "hierarchical_context", "F7"),
    (106, "structure_pred", "Anticipation", "HMCE", "structural_prediction", "F7"),
    # F8: Learning & Expertise (107-120)
    (107, "detection_accuracy", "Appraisal", "SLEE", "perceptual_learning", "F8"),
    (108, "multisensory_binding", "Appraisal", "SLEE", "perceptual_learning", "F8"),
    (109, "statistical_model", "Core", "SLEE", "perceptual_learning", "F8"),
    (110, "plasticity_magnitude", "Appraisal", "TSCP", "perceptual_learning", "F8"),
    (111, "trained_timbre_recognition", "Core", "TSCP", "perceptual_learning", "F8"),
    (112, "compartmentalization_cost", "Appraisal", "ECT", "perceptual_learning", "F8"),
    (113, "transfer_limitation", "Anticipation", "ECT", "perceptual_learning", "F8"),
    (114, "expertise_enhancement", "Core", "ESME", "structural_prediction", "F8"),
    (115, "expertise_trajectory", "Anticipation", "ESME", "structural_prediction", "F8"),
    (116, "pitch_mmn", "Appraisal", "ESME", "expertise_network", "F8"),
    (117, "rhythm_mmn", "Appraisal", "ESME", "expertise_network", "F8"),
    (118, "timbre_mmn", "Appraisal", "ESME", "expertise_network", "F8"),
    (119, "network_specialization", "Core", "EDNR", "expertise_network", "F8"),
    (120, "within_connectivity", "Appraisal", "EDNR", "expertise_network", "F8"),
    # F9: Social Cognition (121-130)
    (121, "collective_pleasure_pred", "Anticipation", "SSRI", "social_reward", "F9"),
    (122, "entrainment_quality", "Appraisal", "SSRI", "interpersonal_sync", "F9"),
    (123, "group_flow", "Appraisal", "SSRI", "interpersonal_sync", "F9"),
    (124, "social_bonding", "Appraisal", "SSRI", "interpersonal_sync", "F9"),
    (125, "social_prediction_error", "Appraisal", "SSRI", "social_reward", "F9"),
    (126, "synchrony_reward", "Appraisal", "SSRI", "social_reward", "F9"),
    (127, "catchiness_pred", "Anticipation", "NSCP", "social_reward", "F9"),
    (128, "neural_synchrony", "Core", "NSCP", "interpersonal_sync", "F9"),
    (129, "resource_allocation", "Appraisal", "DDSMI", "social_reward", "F9"),
    (130, "social_coordination", "Core", "DDSMI", "interpersonal_sync", "F9"),
]

# ── 24D → 12D → 6D parent mappings ─────────────────────────────────

PARENT_12D = {
    "predictive_processing": "expectancy", "information_entropy": "expectancy",
    "sequence_learning": "information_rate", "sensory_encoding": "information_rate",
    "harmonic_tension": "tension_arc", "autonomic_arousal": "tension_arc",
    "sensory_salience": "sonic_impact", "aesthetic_appraisal": "sonic_impact",
    "oscillation_coupling": "entrainment", "motor_period_locking": "entrainment",
    "auditory_motor": "groove", "hierarchical_context": "groove",
    "valence_mode": "contagion", "nostalgia_circuitry": "contagion",
    "dopaminergic_drive": "reward", "hedonic_valuation": "reward",
    "hippocampal_binding": "episodic_resonance", "autobiographical": "episodic_resonance",
    "pitch_melody": "recognition", "perceptual_learning": "recognition",
    "structural_prediction": "synchrony", "expertise_network": "synchrony",
    "interpersonal_sync": "bonding", "social_reward": "bonding",
}

PARENT_6D = {
    "expectancy": "discovery", "information_rate": "discovery",
    "tension_arc": "intensity", "sonic_impact": "intensity",
    "entrainment": "flow", "groove": "flow",
    "contagion": "depth", "reward": "depth",
    "episodic_resonance": "trace", "recognition": "trace",
    "synchrony": "sharing", "bonding": "sharing",
}

# ── Human-readable descriptions per belief ──────────────────────────
# Format: {key: (what_en, what_tr, high_en, high_tr, analogy_en, analogy_tr)}

DESCRIPTIONS = {
    # F1 Sensory
    "consonance_salience_gradient": ("How consonance gradient drives attentional salience — smooth vs rough harmonic texture.", "Konsonans gradyanının dikkat belirginliğini nasıl yönlendirdiği — pürüzsüz vs pürüzlü harmonik doku.", "Strong consonance gradient — the harmonic texture has clear peaks and valleys of roughness.", "Güçlü konsonans gradyanı — harmonik dokunun belirgin pürüzlülük tepeleri ve vadileri var.", "Like running your hand over fabric — smooth silk vs rough burlap.", "Elini kumaş üzerinde gezdirmek gibi — pürüzsüz ipek vs kaba çuval bezi."),
    "contour_continuation": ("Prediction of where the melody will go next based on its contour pattern.", "Kontur kalıbına dayalı olarak melodinin nereye gideceğinin tahmini.", "Strong contour prediction — the brain has a clear model of melodic direction.", "Güçlü kontur tahmini — beyin melodik yön konusunda net bir modele sahip.", "Like following a hiking trail — you can see where the path curves ahead.", "Bir yürüyüş yolunu takip etmek gibi — yolun ileride nereye kıvrıldığını görebilirsin."),
    "melodic_contour_tracking": ("How accurately the brain tracks the up-down shape of the melody.", "Beynin melodinin yukarı-aşağı şeklini ne kadar doğru takip ettiği.", "Precise contour tracking — every rise and fall of the melody is being registered.", "Hassas kontur takibi — melodinin her yükselişi ve düşüşü kaydediliyor.", "Like watching a bird's flight path — tracking every swoop and climb.", "Bir kuşun uçuş yolunu izlemek gibi — her dalışı ve tırmanışı takip etme."),
    "consonance_trajectory": ("Anticipation of how consonance will change in the near future.", "Konsonansın yakın gelecekte nasıl değişeceğinin öngörüsü.", "Active consonance forecasting — the brain expects the harmonic texture to shift.", "Aktif konsonans tahmini — beyin harmonik dokunun kaymasını bekliyor.", "Like sensing weather change — you feel the atmospheric shift before it arrives.", "Hava değişimini hissetmek gibi — atmosferik kaymayı gelmeden hissedersin."),
    "harmonic_stability": ("How close the music stays to its tonal center — the gravitational pull of home key.", "Müziğin tonal merkeze ne kadar yakın durduğu — ana tonalitenin yerçekimi çekimi.", "Strong tonal ground. Chords orbit a familiar center. The brain predicts comfortably.", "Güçlü tonal zemin. Akorlar tanıdık bir merkez etrafında dönüyor. Beyin rahat tahmin ediyor.", "A compass pointing north — harmonic stability shows how clearly music points to its tonal north.", "Kuzeyi gösteren bir pusula — harmonik kararlılık müziğin tonal kuzeyini ne kadar net gösterdiğini ölçer."),
    "harmonic_template_match": ("How well current chords match stored harmonic templates from experience.", "Mevcut akorların deneyimden depolanmış harmonik şablonlarla ne kadar eşleştiği.", "High template match — these chord progressions are familiar, stored templates are firing.", "Yüksek şablon eşleşmesi — bu akor ilerlemeleri tanıdık, depolanmış şablonlar ateşleniyor.", "Like recognizing a friend's face in a crowd — instant, automatic, confident.", "Kalabalıkta bir arkadaşın yüzünü tanımak gibi — anlık, otomatik, emin."),
    "interval_quality": ("Assessment of the quality and character of musical intervals — consonant vs dissonant.", "Müzikal aralıkların kalite ve karakterinin değerlendirmesi — konsonant vs disonant.", "Clear interval quality assessment — the brain is classifying each interval along the consonance spectrum.", "Net aralık kalitesi değerlendirmesi — beyin her aralığı konsonans spektrumunda sınıflandırıyor.", "Like tasting flavors — some sweet (consonant), some bitter (dissonant), some complex (mixed).", "Tatları tatmak gibi — bazıları tatlı (konsonant), bazıları acı (disonant), bazıları karmaşık (karışık)."),
    "pitch_continuation": ("Prediction of the next pitch in a melodic sequence.", "Melodik dizide bir sonraki perdenin tahmini.", "Strong pitch prediction — the brain has a confident model of what note comes next.", "Güçlü perde tahmini — beyin bir sonraki notanın ne olacağı konusunda emin bir modele sahip.", "Like finishing someone's sentence — you know the word before they say it.", "Birinin cümlesini tamamlamak gibi — söylemeden önce kelimeyi bilirsin."),
    "pitch_prominence": ("How prominently pitch stands out in the current auditory scene.", "Perdenin mevcut işitsel sahnede ne kadar belirgin öne çıktığı.", "High pitch prominence — clear, distinct pitch dominating the auditory field.", "Yüksek perde belirginliği — net, belirgin perde işitsel alanı domine ediyor.", "Like a bright star in the sky — impossible to miss, drawing your gaze.", "Gökyüzünde parlak bir yıldız gibi — kaçırması imkansız, bakışını çekiyor."),
    "octave_equivalence": ("Recognition that pitches separated by octaves are perceptually equivalent.", "Oktavlarla ayrılmış perdelerin algısal olarak eşdeğer olduğunun tanınması.", "Octave equivalence active — the brain recognizes the same note at different heights.", "Oktav eşdeğerliği aktif — beyin aynı notayı farklı yüksekliklerde tanıyor.", "Like recognizing the same color in different shades — midnight blue and sky blue are both blue.", "Farklı tonlardaki aynı rengi tanımak gibi — gece mavisi ve gök mavisi ikisi de mavi."),
    "pitch_identity": ("Categorical identification of pitch — what note is this?", "Perdenin kategorik tanımlanması — bu hangi nota?", "Strong pitch identity — the brain is clearly categorizing pitches into discrete note identities.", "Güçlü perde kimliği — beyin perdeleri net olarak ayrık nota kimliklerine sınıflandırıyor.", "Like recognizing letters in a word — each pitch has a clear identity.", "Bir kelimedeki harfleri tanımak gibi — her perdenin net bir kimliği var."),
    "aesthetic_quality": ("The overall aesthetic evaluation of the sound — is it beautiful?", "Sesin genel estetik değerlendirmesi — güzel mi?", "High aesthetic quality — the vmPFC beauty circuit is responding positively.", "Yüksek estetik kalite — vmPFC güzellik devresi olumlu yanıt veriyor.", "Like seeing a sunset — the beauty is immediate, pre-reflective, undeniable.", "Bir gün batımı görmek gibi — güzellik anlık, düşünce-öncesi, yadsınamaz."),
    "reward_response_pred": ("Prediction of how rewarding the next moment will be aesthetically.", "Bir sonraki anın estetik olarak ne kadar ödüllendirici olacağının tahmini.", "Active reward prediction — the brain forecasts an aesthetically rewarding moment ahead.", "Aktif ödül tahmini — beyin ileride estetik olarak ödüllendirici bir an öngörüyor.", "Like smelling dinner cooking — you anticipate the pleasure before tasting.", "Akşam yemeğinin kokusunu almak gibi — tatmadan önce hazzı öngörürsün."),
    "spectral_temporal_synergy": ("How well spectral and temporal features work together to create a coherent percept.", "Spektral ve zamansal özelliklerin tutarlı bir algı yaratmak için ne kadar iyi birlikte çalıştığı.", "High synergy — spectral richness and temporal structure are reinforcing each other.", "Yüksek sinerji — spektral zenginlik ve zamansal yapı birbirini güçlendiriyor.", "Like choreography and music in dance — when they sync, the effect multiplies.", "Danstaki koreografi ve müzik gibi — senkronize olduğunda etki katlanır."),
    "imagery_recognition": ("Mental imagery evoked by the music — visual and spatial associations.", "Müziğin uyandırdığı zihinsel imgelem — görsel ve mekansal çağrışımlar.", "Active imagery — the music is generating visual/spatial representations in the mind.", "Aktif imgelem — müzik zihinde görsel/mekansal temsiller üretiyor.", "Like reading a novel — the words create pictures in your mind.", "Roman okumak gibi — kelimeler zihinde resimler yaratıyor."),
    "timbral_character": ("The distinctive quality of the sound source — brightness, warmth, texture.", "Ses kaynağının ayırt edici kalitesi — parlaklık, sıcaklık, doku.", "Clear timbral character — the sound has a distinctive, recognizable quality.", "Net tınısal karakter — sesin ayırt edici, tanınabilir bir kalitesi var.", "Like recognizing a voice — even without seeing, you know who speaks.", "Bir sesi tanımak gibi — görmeden bile kimin konuştuğunu bilirsin."),
    "spectral_complexity": ("How complex the frequency spectrum is — simple sine wave vs rich orchestral texture.", "Frekans spektrumunun ne kadar karmaşık olduğu — basit sinüs dalgası vs zengin orkestral doku.", "High spectral complexity — many frequency components creating a rich, dense sound.", "Yüksek spektral karmaşıklık — birçok frekans bileşeni zengin, yoğun bir ses yaratıyor.", "Like a crowd vs a solo speaker — many voices vs one clear voice.", "Bir kalabalık vs tek bir konuşmacı gibi — birçok ses vs bir net ses."),
    # F2 Prediction
    "abstract_future": ("High-level prediction of musical form and structure far ahead.", "Müzikal form ve yapının çok ilerisine yönelik üst düzey tahmin.", "Active abstract forecasting — the brain is modeling long-range musical structure.", "Aktif soyut tahmin — beyin uzun menzilli müzikal yapıyı modelliyor."),
    "hierarchy_coherence": ("How coherently the different levels of temporal hierarchy fit together.", "Zamansal hiyerarşinin farklı düzeylerinin ne kadar tutarlı bir şekilde birbirine uyduğu.", "High coherence — beat, meter, phrase, and form all align into a consistent hierarchy.", "Yüksek tutarlılık — vuruş, ölçü, cümle ve form hepsi tutarlı bir hiyerarşi oluşturuyor."),
    "midlevel_future": ("Prediction of musical events at the phrase level — what happens in the next few seconds.", "Cümle düzeyinde müzikal olayların tahmini — önümüzdeki birkaç saniyede ne olacak.", "Active mid-level prediction — the brain is modeling the next phrase or musical gesture.", "Aktif orta düzey tahmin — beyin sonraki cümleyi veya müzikal hareketi modelliyor."),
    "prediction_accuracy": ("How accurate the brain's predictions about upcoming events turn out to be.", "Beynin yaklaşan olaylar hakkındaki tahminlerinin ne kadar doğru çıktığı.", "High prediction accuracy — the brain is good at forecasting this music. Low surprise.", "Yüksek tahmin doğruluğu — beyin bu müziği tahmin etmekte iyi. Düşük sürpriz."),
    "prediction_hierarchy": ("The depth of the prediction hierarchy — from local pitch to global form.", "Tahmin hiyerarşisinin derinliği — yerel perdeden global forma kadar.", "Deep prediction hierarchy — multiple levels of prediction are active simultaneously.", "Derin tahmin hiyerarşisi — birden fazla tahmin düzeyi eşzamanlı olarak aktif."),
    "arousal_change_pred": ("Prediction of how arousal levels will change in the near future.", "Uyarılma düzeylerinin yakın gelecekte nasıl değişeceğinin tahmini.", "Active arousal forecasting — the brain anticipates a change in emotional intensity.", "Aktif uyarılma tahmini — beyin duygusal yoğunlukta bir değişim öngörüyor."),
    "arousal_scaling": ("How the brain scales its arousal response relative to the musical context.", "Beynin uyarılma tepkisini müzikal bağlama göre nasıl ölçeklendirdiği.", "Adjusted arousal scaling — the brain is calibrating its response to the current intensity level.", "Ayarlanmış uyarılma ölçeklemesi — beyin tepkisini mevcut yoğunluk düzeyine kalibre ediyor."),
    "defense_cascade": ("Activation of the defense cascade in response to musically startling events.", "Müzikal olarak ürpertici olaylara yanıt olarak savunma kaskadının aktivasyonu.", "Defense cascade triggered — a sudden musical event activated the startle response.", "Savunma kaskadı tetiklendi — ani bir müzikal olay ürperme tepkisini aktive etti."),
    "information_content": ("Shannon information content of the current musical event — how surprising it is given context.", "Mevcut müzikal olayın Shannon bilgi içeriği — bağlam göz önüne alındığında ne kadar şaşırtıcı.", "High information content — this event is statistically unlikely given the context. Highly informative.", "Yüksek bilgi içeriği — bu olay bağlam göz önüne alındığında istatistiksel olarak olası değil. Son derece bilgilendirici."),
    "valence_inversion": ("Detection of emotional valence shifts — from positive to negative or vice versa.", "Duygusal valans kaymalarının tespiti — pozitiften negatife veya tam tersi.", "Valence inversion detected — the emotional direction has flipped.", "Valans inversiyonu tespit edildi — duygusal yön tersine döndü."),
    "valence_shift_pred": ("Prediction of upcoming emotional valence changes.", "Yaklaşan duygusal valans değişikliklerinin tahmini.", "Active valence prediction — the brain expects an emotional shift is coming.", "Aktif valans tahmini — beyin bir duygusal kaymanın geleceğini bekliyor."),
    "error_propagation": ("How prediction errors propagate through the processing hierarchy.", "Tahmin hatalarının işleme hiyerarşisi boyunca nasıl yayıldığı.", "Active error propagation — prediction errors are rippling through multiple processing levels.", "Aktif hata yayılımı — tahmin hataları birden fazla işleme düzeyine yayılıyor."),
    "oscillatory_signature": ("The characteristic oscillatory pattern associated with the current sequence.", "Mevcut diziyle ilişkilendirilen karakteristik osilasyon kalıbı.", "Clear oscillatory signature — the brain has identified a distinctive rhythmic/spectral pattern.", "Net osilasyon imzası — beyin ayırt edici bir ritmik/spektral kalıp belirledi."),
    "sequence_completion": ("Anticipation of how an ongoing sequence will complete.", "Devam eden bir dizinin nasıl tamamlanacağının öngörüsü.", "Active completion prediction — the brain has a model for how this sequence resolves.", "Aktif tamamlanma tahmini — beyin bu dizinin nasıl çözüleceğine dair bir modele sahip."),
    "sequence_match": ("How well the current sequence matches previously learned patterns.", "Mevcut dizinin daha önce öğrenilmiş kalıplarla ne kadar eşleştiği.", "High sequence match — current patterns strongly match stored sequential knowledge.", "Yüksek dizi eşleşmesi — mevcut kalıplar depolanmış ardışık bilgiyle güçlü eşleşiyor."),
}

# ── Fallback descriptions for beliefs without explicit entries ───────

def make_description(key: str, belief_type: str, mechanism: str, cluster: str, fn: str) -> dict:
    """Generate a description dict for a belief."""
    nice_key = key.replace("_", " ").title()
    cluster_nice = cluster.replace("_", " ").title()

    if key in DESCRIPTIONS:
        desc = DESCRIPTIONS[key]
        result = {
            "what_en": desc[0],
            "what_tr": desc[1],
            "high_en": desc[2],
            "high_tr": desc[3],
        }
        if len(desc) > 4:
            result["analogy_en"] = desc[4]
            result["analogy_tr"] = desc[5]
        return result

    # Generate reasonable fallback
    type_desc = {
        "Core": ("Full Bayesian predict-observe-update cycle.", "Tam Bayesçi tahmin-gözlem-güncelleme döngüsü."),
        "Appraisal": ("Observe-only — monitors this aspect without prediction.", "Yalnızca gözlem — tahmin olmadan bu yönü izler."),
        "Anticipation": ("Forward prediction — forecasts future state.", "İleriye dönük tahmin — gelecek durumu öngörür."),
    }

    what_en = f"{nice_key} — measures {cluster_nice.lower()} aspect within {mechanism} ({fn})."
    what_tr = f"{nice_key} — {mechanism} ({fn}) içindeki {cluster_nice.lower()} yönünü ölçer."
    high_en = f"High {nice_key.lower()}. {type_desc[belief_type][0]}"
    high_tr = f"Yüksek {nice_key.lower()}. {type_desc[belief_type][1]}"

    return {"what_en": what_en, "what_tr": what_tr, "high_en": high_en, "high_tr": high_tr}


def generate():
    """Generate beliefs.jsonl."""
    records = []
    for idx, key, btype, mechanism, cluster_24d, fn in BELIEFS:
        parent_12d = PARENT_12D[cluster_24d]
        parent_6d = PARENT_6D[parent_12d]

        desc = make_description(key, btype, mechanism, cluster_24d, fn)

        record = {
            "index": idx,
            "key": key,
            "function": fn,
            "type": btype,
            "mechanism": mechanism,
            "parent_24d": cluster_24d,
            "parent_12d": parent_12d,
            "parent_6d": parent_6d,
            **desc,
        }
        records.append(record)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated {len(records)} belief cards → {OUTPUT}")
    assert len(records) == 131, f"Expected 131 beliefs, got {len(records)}"


if __name__ == "__main__":
    generate()
