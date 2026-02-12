/**
 * questions.js — Interactive question engine with moment triggers.
 * S³ Musical Intelligence Demo
 *
 * Detects key musical moments from MI data and presents
 * interactive questions to guide the user deeper.
 */

import { BRAIN, LAYOUT } from './data.js';
import { getLang } from './i18n.js';

const COOLDOWN_SEC = 15;
const MAX_QUESTIONS = 8;
const AUTO_DISMISS_SEC = 10;

// ═══════════════════════════════════════════════════════════════════════
// QUESTION BANK (per level × trigger type)
// ═══════════════════════════════════════════════════════════════════════

const QUESTIONS = {
    energy_buildup: {
        1: { en: 'Can you hear the instruments getting louder? This is called dynamic buildup.',
             tr: 'Enstrümanların sesinin yükseldiğini duyabiliyor musunuz? Buna dinamik yükseliş denir.' },
        2: { en: 'Do you feel a sense of anticipation building? Like something big is coming?',
             tr: 'İçinizde bir beklenti hissi oluşuyor mu? Büyük bir şey gelecekmiş gibi?' },
        3: { en: 'Your caudate nucleus would be releasing anticipatory dopamine right now.',
             tr: 'Şu anda kaudat çekirdeğiniz beklenti dopamini salgılıyor olurdu.' },
    },
    consonance_peak: {
        1: { en: 'Notice how harmonious this sounds. The spectral fusion is very high.',
             tr: 'Ne kadar uyumlu duyulduğuna dikkat edin. Spektral füzyon çok yüksek.' },
        2: { en: 'Does this moment feel pleasant to you? Your brain rates this as highly consonant.',
             tr: 'Bu an size hoş geliyor mu? Beyniniz bunu yüksek uyumluluk olarak değerlendiriyor.' },
        3: { en: 'The superior temporal gyrus (STG) is strongly activated — processing this rich harmonic content.',
             tr: 'Üst temporal girus (STG) güçlü şekilde aktive oldu — bu zengin harmonik içeriği işliyor.' },
    },
    pleasure_convergence: {
        1: { en: 'This is the peak musical moment. Everything converges here.',
             tr: 'Bu en doruk müzikal an. Her şey burada birleşiyor.' },
        2: { en: 'Wanting and liking have converged — this is peak pleasure. The dual reward signals align.',
             tr: 'İsteme ve beğenme birleşti — bu doruk haz. İkili ödül sinyalleri hizalandı.' },
        3: { en: 'Dual-peak convergence: NAcc (consummatory DA) + Caudate (anticipatory DA) fire together. (Salimpoor 2011)',
             tr: 'İkili doruk yakınsaması: NAcc (tüketim DA) + Kaudat (beklenti DA) birlikte ateşleniyor. (Salimpoor 2011)' },
    },
    tension_resolution: {
        1: { en: 'The tension is releasing now. Can you feel the musical resolution?',
             tr: 'Gerilim şimdi çözülüyor. Müzikal çözümü hissedebiliyor musunuz?' },
        2: { en: 'How did that feel? The emotional arc has completed its journey.',
             tr: 'Nasıl hissettirdi? Duygusal seyir yolculuğunu tamamladı.' },
        3: { en: 'The opioid system sustains this feeling of beauty and resolution.',
             tr: 'Opioid sistemi bu güzellik ve çözüm hissini sürdürüyor.' },
    },
    chills_event: {
        1: { en: 'Did you feel a physical response? A shiver or goosebumps?',
             tr: 'Fiziksel bir tepki hissettiniz mi? Titreme veya tüyleriniz diken diken olma?' },
        2: { en: 'This is a chill moment — your autonomic nervous system is responding strongly.',
             tr: 'Bu bir ürperti anı — otonom sinir sisteminiz güçlü şekilde yanıt veriyor.' },
        3: { en: 'Autonomic response detected: SCR spike + vagal brake release. (de Fleurian & Pearce 2021, d=0.85)',
             tr: 'Otonom yanıt tespit edildi: DCI artışı + vagal fren gevşemesi. (de Fleurian & Pearce 2021, d=0.85)' },
    },
    prediction_error: {
        1: { en: 'Something unexpected just happened in the music. Did you catch it?',
             tr: 'Müzikte beklenmedik bir şey oldu. Fark ettiniz mi?' },
        2: { en: 'Your brain detected a surprise. The prediction error signal just spiked.',
             tr: 'Beyniniz bir sürpriz tespit etti. Tahmin hatası sinyali az önce yükseldi.' },
        3: { en: 'The inferior frontal gyrus (IFG) processes this prediction error signal.',
             tr: 'Alt frontal girus (IFG) bu tahmin hatası sinyalini işliyor.' },
    },
};

// ═══════════════════════════════════════════════════════════════════════
// TRIGGER CONDITIONS
// ═══════════════════════════════════════════════════════════════════════

const TRIGGERS = {
    energy_buildup: (frame, prev) =>
        frame[BRAIN.emotional_momentum] > 0.7 && (!prev || prev[BRAIN.emotional_momentum] < 0.5),
    consonance_peak: (frame) =>
        frame[LAYOUT.r3.start + 3] > 0.8, // stumpf_fusion
    pleasure_convergence: (frame, prev) =>
        frame[BRAIN.pleasure] > 0.6 && (!prev || prev[BRAIN.pleasure] < 0.5),
    chills_event: (frame) =>
        frame[BRAIN.chills_intensity] > 0.7,
    prediction_error: (frame) =>
        Math.abs(frame[BRAIN.prediction_error]) > 0.6,
    tension_resolution: (frame, prev) =>
        frame[BRAIN.tension] < 0.3 && prev && prev[BRAIN.tension] > 0.5,
};

// ═══════════════════════════════════════════════════════════════════════
// QUESTION ENGINE
// ═══════════════════════════════════════════════════════════════════════

export class QuestionEngine {
    constructor() {
        this.lastQuestionTime = -COOLDOWN_SEC;
        this.questionCount = 0;
        this.currentQuestion = null;
        this.showTime = 0;
        this._prevFrame = null;
        this._onQuestion = null;
        this._onDismiss = null;
    }

    onQuestion(cb) { this._onQuestion = cb; }
    onDismiss(cb) { this._onDismiss = cb; }

    reset() {
        this.lastQuestionTime = -COOLDOWN_SEC;
        this.questionCount = 0;
        this.currentQuestion = null;
        this._prevFrame = null;
    }

    /**
     * Check triggers and potentially show a question.
     * Call once per frame with current time and 307D data.
     */
    update(timeSec, frame, currentLevel) {
        // Auto-dismiss
        if (this.currentQuestion && (timeSec - this.showTime > AUTO_DISMISS_SEC)) {
            this.dismiss();
        }

        // Don't check if question active or in cooldown or max reached
        if (this.currentQuestion) { this._prevFrame = frame; return; }
        if (timeSec - this.lastQuestionTime < COOLDOWN_SEC) { this._prevFrame = frame; return; }
        if (this.questionCount >= MAX_QUESTIONS) { this._prevFrame = frame; return; }

        // Check each trigger
        for (const [type, check] of Object.entries(TRIGGERS)) {
            if (check(frame, this._prevFrame)) {
                this._showQuestion(type, currentLevel, timeSec);
                break;
            }
        }

        this._prevFrame = frame ? new Float32Array(frame) : null;
    }

    _showQuestion(type, level, timeSec) {
        const lang = getLang();
        const q = QUESTIONS[type]?.[level];
        if (!q) return;

        this.currentQuestion = {
            type,
            text: q[lang] || q.en,
            level,
        };
        this.showTime = timeSec;
        this.lastQuestionTime = timeSec;
        this.questionCount++;

        if (this._onQuestion) this._onQuestion(this.currentQuestion);
    }

    dismiss() {
        this.currentQuestion = null;
        if (this._onDismiss) this._onDismiss();
    }

    /**
     * Check pre-annotated moments (from moments.json).
     */
    checkMoment(moment, timeSec, currentLevel) {
        if (this.currentQuestion) return;
        if (timeSec - this.lastQuestionTime < COOLDOWN_SEC) return;
        if (this.questionCount >= MAX_QUESTIONS) return;

        const type = moment.type;
        if (QUESTIONS[type]) {
            this._showQuestion(type, currentLevel, timeSec);
        }
    }
}
