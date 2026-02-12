/**
 * i18n.js — Bilingual string tables (EN/TR).
 * S³ Musical Intelligence Demo
 */

let _lang = 'en';

export function setLang(lang) { _lang = lang; }
export function getLang() { return _lang; }
export function t(key) { return STRINGS[key]?.[_lang] || STRINGS[key]?.en || key; }

const STRINGS = {
    // Landing
    title: { en: 'Musical Intelligence', tr: 'Müzikal Zeka' },
    tagline: { en: 'What does your brain hear when you listen to music?', tr: 'Müzik dinlerken beyniniz ne duyuyor?' },
    choose_piece: { en: 'Choose a piece to begin', tr: 'Başlamak için bir eser seçin' },

    // Loading
    loading: { en: 'Preparing your journey...', tr: 'Yolculuğunuz hazırlanıyor...' },
    loading_data: { en: 'Loading analysis data', tr: 'Analiz verisi yükleniyor' },
    loading_audio: { en: 'Loading audio', tr: 'Ses yükleniyor' },

    // Levels
    level_1: { en: 'Musical', tr: 'Müzikal' },
    level_2: { en: 'Psychological', tr: 'Psikolojik' },
    level_3: { en: 'Neuroscience', tr: 'Nörobilim' },
    level_1_sub: { en: 'What you\'re hearing', tr: 'Ne duyuyorsunuz' },
    level_2_sub: { en: 'What you\'re feeling', tr: 'Ne hissediyorsunuz' },
    level_3_sub: { en: 'What your brain is doing', tr: 'Beyniniz ne yapıyor' },

    // Panel labels — Level 1
    consonance: { en: 'Consonance', tr: 'Uyum' },
    energy: { en: 'Energy', tr: 'Enerji' },
    loudness: { en: 'Loudness', tr: 'Ses Şiddeti' },
    warmth: { en: 'Warmth', tr: 'Sıcaklık' },
    tonalness: { en: 'Tonalness', tr: 'Tonalite' },
    clarity: { en: 'Clarity', tr: 'Berraklık' },
    flux: { en: 'Spectral Change', tr: 'Spektral Değişim' },

    // Panel labels — Level 2
    wanting: { en: 'Wanting', tr: 'İsteme' },
    liking: { en: 'Liking', tr: 'Beğenme' },
    pleasure: { en: 'Pleasure', tr: 'Haz' },
    tension: { en: 'Tension', tr: 'Gerilim' },
    valence: { en: 'Valence', tr: 'Duygu Yönü' },
    arousal: { en: 'Arousal', tr: 'Uyarılma' },
    beauty: { en: 'Beauty', tr: 'Güzellik' },
    emotional_arc: { en: 'Emotional Arc', tr: 'Duygusal Seyir' },

    // Panel labels — Level 3
    nacc: { en: 'NAcc (Reward)', tr: 'NAcc (Ödül)' },
    caudate: { en: 'Caudate (Anticipation)', tr: 'Kaudat (Beklenti)' },
    vta: { en: 'VTA (Dopamine)', tr: 'VTA (Dopamin)' },
    stg: { en: 'STG (Auditory)', tr: 'STG (İşitsel)' },
    ifg: { en: 'IFG (Prediction)', tr: 'IFG (Tahmin)' },
    amygdala: { en: 'Amygdala (Emotion)', tr: 'Amigdala (Duygu)' },
    hippocampus: { en: 'Hippocampus (Memory)', tr: 'Hipokampüs (Bellek)' },
    dopamine: { en: 'Dopamine', tr: 'Dopamin' },
    opioid: { en: 'Opioid', tr: 'Opioid' },
    scr: { en: 'Skin Conductance', tr: 'Deri İletkenliği' },
    hr: { en: 'Heart Rate', tr: 'Kalp Atışı' },
    chills: { en: 'Chills', tr: 'Tüyler Diken' },

    // Transport
    play: { en: 'Play', tr: 'Oynat' },
    pause: { en: 'Pause', tr: 'Duraklat' },

    // Summary
    summary_title: { en: 'Journey Complete', tr: 'Yolculuk Tamamlandı' },
    peak_pleasure: { en: 'Peak Pleasure', tr: 'Doruk Haz' },
    replay: { en: 'Replay', tr: 'Tekrar Oynat' },

    // Questions
    yes: { en: 'Yes', tr: 'Evet' },
    no: { en: 'No', tr: 'Hayır' },
    somewhat: { en: 'Somewhat', tr: 'Biraz' },
    strongly: { en: 'Strongly', tr: 'Kesinlikle' },
    go_deeper: { en: 'Go deeper', tr: 'Daha derine in' },
};
