/**
 * app.js — Main orchestrator + render loop.
 * S³ Musical Intelligence Demo
 *
 * State machine: LANDING → LOADING → PLAYING → SUMMARY
 */

import { GLContext } from './gl.js';
import { MIData } from './data.js';
import { AudioPlayer } from './audio.js';
import { VERT, BACKGROUND, SPECTRAL_LANDSCAPE, REWARD_FLOW, NEURAL_PULSE, TRANSITION } from './shaders.js';
import { LEVELS, mapLevel1, mapLevel2, mapLevel3, mapBackground, getPanelData } from './levels.js';
import { QuestionEngine } from './questions.js';
import { generateNarrative } from './narrative.js';
import { UI } from './ui.js';
import { t, getLang } from './i18n.js';

// ═══════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════

const state = {
    phase: 'landing', // landing | loading | playing | summary
    currentLevel: 1,
    targetLevel: 1,
    transitionProgress: 1, // 0→1 (1 = no transition)
    piece: null,
    moments: [],
    peakPleasureTime: 0,
    peakPleasureVal: 0,
    frameCount: 0,
};

let gl, miData, audio, questions, ui;
let manifest = null;
let momentsData = null;

// ═══════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════

async function init() {
    const canvas = document.getElementById('canvas');
    gl = new GLContext(canvas);
    miData = new MIData();
    audio = new AudioPlayer();
    questions = new QuestionEngine();
    ui = new UI();

    // Compile all shader programs
    gl.createProgram(VERT, BACKGROUND, 'background');
    gl.createProgram(VERT, SPECTRAL_LANDSCAPE, 'spectral_landscape');
    gl.createProgram(VERT, REWARD_FLOW, 'reward_flow');
    gl.createProgram(VERT, NEURAL_PULSE, 'neural_pulse');
    gl.createProgram(VERT, TRANSITION, 'transition');

    // UI bindings
    ui.initLangToggle();
    ui.initTransport();

    ui.onPieceSelect(loadPiece);
    ui.onPlayPause(togglePlay);
    ui.onSeek((pct) => audio.seek(pct * audio.duration));
    ui.onLevelChange(setLevel);
    ui.onLangChange(() => {
        if (state.phase === 'landing') showLanding();
        ui.initLevels(LEVELS);
        ui.setActiveLevel(state.currentLevel);
    });

    // Keyboard
    document.addEventListener('keydown', (e) => {
        if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
        if (e.key === '1') setLevel(1);
        if (e.key === '2') setLevel(2);
        if (e.key === '3') setLevel(3);
    });

    // Question callbacks
    questions.onQuestion((q) => ui.showQuestion(q));
    questions.onDismiss(() => ui.hideQuestion());

    // Audio end
    audio.onEnd(() => {
        state.phase = 'summary';
        ui.showSummary({
            peakPleasureTime: state.peakPleasureTime,
            piece: state.piece,
        });
    });

    // Load manifest
    try {
        const res = await fetch('data/manifest.json');
        manifest = await res.json();
    } catch (e) {
        console.warn('No manifest.json found, using defaults');
        manifest = { pieces: [] };
    }

    // Load moments
    try {
        const res = await fetch('data/moments.json');
        momentsData = await res.json();
    } catch (e) {
        momentsData = { moments: [] };
    }

    showLanding();
    requestAnimationFrame(loop);
}

// ═══════════════════════════════════════════════════════════════════════
// PHASE HANDLERS
// ═══════════════════════════════════════════════════════════════════════

function showLanding() {
    state.phase = 'landing';
    const pieces = manifest?.pieces?.length > 0
        ? manifest.pieces
        : [{
            id: 'swan-lake',
            title: 'Swan Lake Suite, Op. 20a: I. Scene',
            composer: 'Pyotr Ilyich Tchaikovsky',
            genre: 'Classical Orchestral',
            genre_tr: 'Klasik Orkestra',
            description: "Where the brain's reward system comes alive",
            description_tr: 'Beynin ödül sisteminin canlandığı yer',
            data_file: 'swan-lake.mi.bin',
            audio_file: 'swan-lake.mp3',
        }];
    ui.showLanding(pieces);
}

async function loadPiece(piece) {
    state.piece = piece;
    state.phase = 'loading';
    state.peakPleasureTime = 0;
    state.peakPleasureVal = 0;
    state.currentLevel = 1;
    state.targetLevel = 1;
    state.transitionProgress = 1;

    ui.hideLanding();
    ui.showLoading();
    questions.reset();

    try {
        // Load data + audio in parallel
        const dataUrl = 'data/' + piece.data_file;
        const audioUrl = 'data/' + piece.audio_file;

        await Promise.all([
            miData.load(dataUrl, (p) => ui.setLoadProgress(p * 0.6)),
            audio.load(audioUrl, (p) => ui.setLoadProgress(0.6 + p * 0.4)),
        ]);

        ui.setLoadProgress(1);

        // Start
        state.phase = 'playing';
        state.moments = momentsData?.moments || [];
        ui.hideLoading();
        ui.showExperience();
        ui.initLevels(LEVELS);
        ui.setActiveLevel(1);
        ui.hideNarrative();

        audio.play(0);
    } catch (e) {
        console.error('Failed to load piece:', e);
        ui.hideLoading();
        showLanding();
    }
}

function togglePlay() {
    if (state.phase !== 'playing') return;
    if (audio.playing) audio.pause();
    else audio.play();
}

function setLevel(id) {
    if (state.currentLevel === id) return;
    state.targetLevel = id;
    state.transitionProgress = 0;

    ui.setActiveLevel(id);

    // Show/hide narrative for L2/L3
    if (id >= 2) ui.showNarrative();
    else ui.hideNarrative();
}

// ═══════════════════════════════════════════════════════════════════════
// RENDER LOOP
// ═══════════════════════════════════════════════════════════════════════

function loop() {
    requestAnimationFrame(loop);

    const [w, h] = gl.resize();
    const time = audio.currentTime || 0;
    const duration = audio.duration || 1;

    if (state.phase !== 'playing') {
        // Render background only during landing/loading
        renderShader('background', w, h, time, null);
        return;
    }

    // Get current frame
    const frame = miData.getFrame(time);
    if (!frame) return;

    // Track peak pleasure
    const pleasure = frame[186]; // BRAIN.pleasure absolute index
    if (pleasure > state.peakPleasureVal) {
        state.peakPleasureVal = pleasure;
        state.peakPleasureTime = time;
    }

    // Update transition
    if (state.transitionProgress < 1) {
        state.transitionProgress = Math.min(1, state.transitionProgress + 1/90); // ~1.5s at 60fps
        if (state.transitionProgress >= 1) {
            state.currentLevel = state.targetLevel;
        }
    }

    // Render
    const currentShader = levelToShader(state.currentLevel);
    const targetShader = levelToShader(state.targetLevel);

    if (state.transitionProgress < 1 && currentShader !== targetShader) {
        // Dual-FBO transition
        gl.renderToFBO(0);
        renderShader(currentShader, w, h, time, frame);
        gl.renderToFBO(1);
        renderShader(targetShader, w, h, time, frame);
        gl.renderToScreen();

        const transProg = gl.getProgram('transition');
        if (transProg) {
            const glCtx = gl.gl;
            glCtx.useProgram(transProg.program);

            glCtx.activeTexture(glCtx.TEXTURE0);
            glCtx.bindTexture(glCtx.TEXTURE_2D, gl.getFBOTexture(0));
            glCtx.uniform1i(transProg.uniforms['u_tex_old'], 0);

            glCtx.activeTexture(glCtx.TEXTURE1);
            glCtx.bindTexture(glCtx.TEXTURE_2D, gl.getFBOTexture(1));
            glCtx.uniform1i(transProg.uniforms['u_tex_new'], 1);

            gl.setFloat(transProg, 'u_mix', state.transitionProgress);
            gl.drawQuad(transProg);
        }
    } else {
        renderShader(targetShader, w, h, time, frame);
    }

    // Update UI (throttle to every 4 frames)
    state.frameCount++;
    if (state.frameCount % 4 === 0) {
        const activeLevel = state.transitionProgress < 1 ? state.targetLevel : state.currentLevel;
        ui.updateTransport(time, duration, audio.playing);

        const panelData = getPanelData(frame, activeLevel);
        const levelDef = LEVELS.find(l => l.id === activeLevel);
        ui.updatePanel(panelData, activeLevel);
        ui.setPanelTitle(levelDef?.subtitle?.[getLangShort()] || '');

        // Narrative (L2/L3 only)
        if (activeLevel >= 2) {
            ui.setNarrative(generateNarrative(frame));
        }

        // Questions
        questions.update(time, frame, activeLevel);

        // Check pre-annotated moments
        for (const m of state.moments) {
            if (time >= m.start && time < m.start + 2) {
                questions.checkMoment(m, time, activeLevel);
            }
        }
    }
}

function renderShader(name, w, h, time, frame) {
    const prog = gl.getProgram(name);
    if (!prog) return;

    const glCtx = gl.gl;
    glCtx.useProgram(prog.program);
    gl.setVec2(prog, 'u_res', w, h);
    gl.setFloat(prog, 'u_time', time);
    gl.setFloat(prog, 'u_progress', audio.duration > 0 ? time / audio.duration : 0);

    if (frame) {
        // Upload level-specific uniforms
        if (name === 'background') mapBackground(frame, gl, prog);
        else if (name === 'spectral_landscape') { mapBackground(frame, gl, prog); mapLevel1(frame, gl, prog); }
        else if (name === 'reward_flow') mapLevel2(frame, gl, prog);
        else if (name === 'neural_pulse') mapLevel3(frame, gl, prog);
    }

    gl.drawQuad(prog);
}

function levelToShader(level) {
    if (level === 1) return 'spectral_landscape';
    if (level === 2) return 'reward_flow';
    if (level === 3) return 'neural_pulse';
    return 'background';
}

function getLangShort() {
    return getLang();
}

// ═══════════════════════════════════════════════════════════════════════
// BOOT
// ═══════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', init);
