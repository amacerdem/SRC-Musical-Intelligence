/**
 * narrative.js — θ/η → bilingual text generation.
 * S³ Musical Intelligence Demo
 *
 * Generates human-readable narrative sentences from L³ θ (narrative structure)
 * and η (vocabulary gradations) dimensions.
 */

import { LAYOUT } from './data.js';
import { getLang } from './i18n.js';

// θ dimension layout within L³ (relative to theta start)
// Subject [0:4], Predicate [4:8], Modifier [8:12], Connector [12:16]

const SUBJECTS = {
    en: ['Musical pleasure', 'Tension', 'The energy', 'Beauty'],
    tr: ['Müzikal haz', 'Gerilim', 'Enerji', 'Güzellik'],
};

const PREDICATES = {
    en: ['is rising', 'reaches its peak', 'is fading', 'holds steady'],
    tr: ['yükseliyor', 'doruğa ulaşıyor', 'azalıyor', 'sabit kalıyor'],
};

const MODIFIERS = {
    en: ['with intense force', 'with clear certainty', 'with surprising novelty', 'swiftly'],
    tr: ['yoğun bir güçle', 'belirgin bir kesinlikle', 'şaşırtıcı bir yenilikle', 'hızla'],
};

const CONNECTORS = {
    en: ['as the music flows onward', 'while a new element emerges', 'finding resolution', 'marking a new chapter'],
    tr: ['müzik akarken', 'yeni bir unsur belirirken', 'çözüme kavuşarak', 'yeni bir sayfa açarak'],
};

// η vocabulary terms (simplified — 8 bands per axis)
const VOCAB_TERMS = {
    valence: {
        en: ['devastating', 'melancholic', 'wistful', 'subdued', 'content', 'happy', 'joyful', 'euphoric'],
        tr: ['yıkıcı', 'melankolik', 'hüzünlü', 'sönük', 'huzurlu', 'mutlu', 'neşeli', 'coşkulu'],
    },
    arousal: {
        en: ['comatose', 'lethargic', 'drowsy', 'calm', 'alert', 'energized', 'excited', 'explosive'],
        tr: ['uyuşuk', 'halsiz', 'uykulu', 'sakin', 'uyanık', 'enerjik', 'heyecanlı', 'patlayıcı'],
    },
    tension: {
        en: ['dissolved', 'slack', 'easy', 'mild', 'moderate', 'taut', 'strained', 'crushing'],
        tr: ['çözülmüş', 'gevşek', 'rahat', 'hafif', 'orta', 'gergin', 'gerilmiş', 'ezici'],
    },
    beauty: {
        en: ['harsh', 'grating', 'rough', 'plain', 'pleasing', 'beautiful', 'sublime', 'transcendent'],
        tr: ['kaba', 'rahatsız', 'sert', 'yalın', 'hoş', 'güzel', 'yüce', 'aşkın'],
    },
};

function argmax(arr, start, count) {
    let maxIdx = 0, maxVal = arr[start];
    for (let i = 1; i < count; i++) {
        if (arr[start + i] > maxVal) {
            maxVal = arr[start + i];
            maxIdx = i;
        }
    }
    return maxIdx;
}

function valueToBand(v) {
    return Math.min(7, Math.max(0, Math.floor(v * 8)));
}

/**
 * Generate a narrative sentence from the current 307D frame.
 */
export function generateNarrative(frame) {
    const lang = getLang();
    const T = LAYOUT.theta.start; // 291

    // θ: subject [0:4], predicate [4:8], modifier [8:12], connector [12:16]
    const subjectIdx = argmax(frame, T, 4);
    const predicateIdx = argmax(frame, T + 4, 4);
    const modifierIdx = argmax(frame, T + 8, 4);
    const connectorIdx = argmax(frame, T + 12, 4);

    const subject = SUBJECTS[lang][subjectIdx];
    const predicate = PREDICATES[lang][predicateIdx];
    const modifier = MODIFIERS[lang][modifierIdx];
    const connector = CONNECTORS[lang][connectorIdx];

    if (lang === 'tr') {
        return `${subject} ${modifier} ${predicate}, ${connector}.`;
    }
    return `${subject} ${predicate} ${modifier}, ${connector}.`;
}

/**
 * Get the η vocabulary term for a polarity axis.
 */
export function getVocabTerm(frame, axis) {
    const Z = LAYOUT.zeta.start; // 267
    const axisMap = { valence: 0, arousal: 1, tension: 2, beauty: 9 };
    const idx = axisMap[axis];
    if (idx == null) return '';

    const value = (frame[Z + idx] + 1) / 2; // [-1,1] → [0,1]
    const band = valueToBand(value);
    const lang = getLang();
    return VOCAB_TERMS[axis]?.[lang]?.[band] || '';
}

/**
 * Get all active vocabulary terms (most extreme axes).
 */
export function getActiveTerms(frame) {
    const Z = LAYOUT.zeta.start;
    const lang = getLang();
    const axes = Object.keys(VOCAB_TERMS);
    const terms = [];

    for (const axis of axes) {
        const axisMap = { valence: 0, arousal: 1, tension: 2, beauty: 9 };
        const idx = axisMap[axis];
        if (idx == null) continue;
        const raw = frame[Z + idx]; // [-1,1]
        const value = (raw + 1) / 2;
        const band = valueToBand(value);
        const extremity = Math.abs(raw);
        terms.push({ axis, term: VOCAB_TERMS[axis][lang][band], extremity, value: raw });
    }

    // Sort by extremity (most extreme first)
    terms.sort((a, b) => b.extremity - a.extremity);
    return terms;
}
