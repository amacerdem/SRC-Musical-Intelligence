/**
 * ui.js — DOM management: genre picker, HUD, panels, transport.
 * S³ Musical Intelligence Demo
 */

import { t, getLang, setLang } from './i18n.js';

export class UI {
    constructor() {
        this._onPieceSelect = null;
        this._onPlayPause = null;
        this._onSeek = null;
        this._onLevelChange = null;
        this._onLangChange = null;
    }

    // ─── Event Handlers ──────────────────────────
    onPieceSelect(cb) { this._onPieceSelect = cb; }
    onPlayPause(cb) { this._onPlayPause = cb; }
    onSeek(cb) { this._onSeek = cb; }
    onLevelChange(cb) { this._onLevelChange = cb; }
    onLangChange(cb) { this._onLangChange = cb; }

    // ─── Landing Page ────────────────────────────
    showLanding(pieces) {
        const landing = document.getElementById('landing');
        const title = document.getElementById('landing-title');
        const tagline = document.getElementById('landing-tagline');
        const grid = document.getElementById('piece-grid');

        title.textContent = t('title');
        tagline.textContent = t('tagline');
        grid.innerHTML = '';

        for (const piece of pieces) {
            const lang = getLang();
            const btn = document.createElement('button');
            btn.className = 'piece-btn';
            btn.innerHTML = `
                <span class="piece-title">${piece.title}</span>
                <span class="piece-composer">${piece.composer}</span>
                <span class="piece-desc">${lang === 'tr' ? piece.description_tr : piece.description}</span>
            `;
            btn.addEventListener('click', () => {
                if (this._onPieceSelect) this._onPieceSelect(piece);
            });
            grid.appendChild(btn);
        }

        landing.classList.remove('hidden');
        document.getElementById('experience').classList.add('hidden');
        document.getElementById('loading-screen').classList.add('hidden');
    }

    hideLanding() {
        document.getElementById('landing').classList.add('hidden');
    }

    // ─── Loading Screen ──────────────────────────
    showLoading() {
        const el = document.getElementById('loading-screen');
        el.classList.remove('hidden');
        document.getElementById('loading-text').textContent = t('loading');
        this.setLoadProgress(0);
    }

    hideLoading() {
        document.getElementById('loading-screen').classList.add('hidden');
    }

    setLoadProgress(p) {
        document.getElementById('load-bar-fill').style.width = (p * 100) + '%';
    }

    // ─── Experience (main view) ──────────────────
    showExperience() {
        document.getElementById('experience').classList.remove('hidden');
    }

    // ─── Transport ───────────────────────────────
    updateTransport(currentTime, duration, playing) {
        const timeEl = document.getElementById('time-display');
        const progressEl = document.getElementById('progress-bar-fill');
        const playBtn = document.getElementById('play-btn');

        const cur = formatTime(currentTime);
        const dur = formatTime(duration);
        timeEl.textContent = `${cur} / ${dur}`;

        const pct = duration > 0 ? (currentTime / duration * 100) : 0;
        progressEl.style.width = pct + '%';

        playBtn.textContent = playing ? '⏸' : '▶';
    }

    initTransport() {
        const playBtn = document.getElementById('play-btn');
        playBtn.addEventListener('click', () => {
            if (this._onPlayPause) this._onPlayPause();
        });

        const progressBar = document.getElementById('progress-bar');
        progressBar.addEventListener('click', (e) => {
            const rect = progressBar.getBoundingClientRect();
            const pct = (e.clientX - rect.left) / rect.width;
            if (this._onSeek) this._onSeek(pct);
        });
    }

    // ─── Level Selector ──────────────────────────
    initLevels(levels) {
        const container = document.getElementById('level-selector');
        container.innerHTML = '';
        const lang = getLang();

        for (const level of levels) {
            const btn = document.createElement('button');
            btn.className = 'level-btn';
            btn.dataset.level = level.id;
            btn.textContent = level.name[lang];
            btn.style.setProperty('--level-color', level.color);
            btn.addEventListener('click', () => {
                if (this._onLevelChange) this._onLevelChange(level.id);
            });
            container.appendChild(btn);
        }
    }

    setActiveLevel(levelId) {
        const btns = document.querySelectorAll('.level-btn');
        btns.forEach(btn => {
            btn.classList.toggle('active', parseInt(btn.dataset.level) === levelId);
        });
    }

    // ─── Panel ───────────────────────────────────
    updatePanel(data, level) {
        const panel = document.getElementById('panel-content');
        let html = '';
        for (const [key, value] of Object.entries(data)) {
            const label = t(key) || key;
            const pct = Math.min(100, Math.max(0, (typeof value === 'number' ? value : 0) * 100));
            html += `
                <div class="panel-row">
                    <span class="panel-label">${label}</span>
                    <div class="panel-bar"><div class="panel-bar-fill" style="width:${pct}%"></div></div>
                    <span class="panel-value">${pct.toFixed(0)}%</span>
                </div>
            `;
        }
        panel.innerHTML = html;
    }

    setPanelTitle(title) {
        document.getElementById('panel-title').textContent = title;
    }

    // ─── Question Card ───────────────────────────
    showQuestion(question) {
        const card = document.getElementById('question-card');
        const text = document.getElementById('question-text');
        text.textContent = question.text;
        card.classList.remove('hidden');
        card.classList.add('slide-in');
    }

    hideQuestion() {
        const card = document.getElementById('question-card');
        card.classList.add('hidden');
        card.classList.remove('slide-in');
    }

    // ─── Narrative Text ──────────────────────────
    setNarrative(text) {
        const el = document.getElementById('narrative');
        if (el.textContent !== text) {
            el.classList.add('fade-out');
            setTimeout(() => {
                el.textContent = text;
                el.classList.remove('fade-out');
            }, 300);
        }
    }

    showNarrative() { document.getElementById('narrative').classList.remove('hidden'); }
    hideNarrative() { document.getElementById('narrative').classList.add('hidden'); }

    // ─── Language Toggle ─────────────────────────
    initLangToggle() {
        const btn = document.getElementById('lang-toggle');
        btn.textContent = getLang() === 'en' ? 'TR' : 'EN';
        btn.addEventListener('click', () => {
            const newLang = getLang() === 'en' ? 'tr' : 'en';
            setLang(newLang);
            btn.textContent = newLang === 'en' ? 'TR' : 'EN';
            if (this._onLangChange) this._onLangChange(newLang);
        });
    }

    // ─── Summary ─────────────────────────────────
    showSummary(stats) {
        const el = document.getElementById('summary');
        const lang = getLang();
        el.innerHTML = `
            <h2>${t('summary_title')}</h2>
            <p>${t('peak_pleasure')}: ${formatTime(stats.peakPleasureTime)}</p>
            <button id="replay-btn" class="piece-btn">${t('replay')}</button>
        `;
        el.classList.remove('hidden');
        document.getElementById('replay-btn').addEventListener('click', () => {
            el.classList.add('hidden');
            if (this._onPieceSelect) this._onPieceSelect(stats.piece);
        });
    }
}

function formatTime(sec) {
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
}
