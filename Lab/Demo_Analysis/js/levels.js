/**
 * levels.js — Level configuration + 307D → shader uniform mapping.
 * S³ Musical Intelligence Demo
 *
 * Maps MI-space dimensions to shader uniforms for each depth level.
 */

import { LAYOUT, BRAIN } from './data.js';

// ═══════════════════════════════════════════════════════════════════════
// LEVEL DEFINITIONS
// ═══════════════════════════════════════════════════════════════════════

export const LEVELS = [
    {
        id: 1,
        name: { en: 'Musical', tr: 'Müzikal' },
        subtitle: { en: 'What you\'re hearing', tr: 'Ne duyuyorsunuz' },
        shader: 'spectral_landscape',
        color: '#06b6d4', // cyan
    },
    {
        id: 2,
        name: { en: 'Psychological', tr: 'Psikolojik' },
        subtitle: { en: 'What you\'re feeling', tr: 'Ne hissediyorsunuz' },
        shader: 'reward_flow',
        color: '#8b5cf6', // purple
    },
    {
        id: 3,
        name: { en: 'Neuroscience', tr: 'Nörobilim' },
        subtitle: { en: 'What your brain is doing', tr: 'Beyniniz ne yapıyor' },
        shader: 'neural_pulse',
        color: '#f97316', // orange
    },
];

// ═══════════════════════════════════════════════════════════════════════
// UNIFORM MAPPERS — frame(307D) → shader uniforms
// ═══════════════════════════════════════════════════════════════════════

/**
 * Compute 8 mel band averages from 128 cochlea dims.
 * Each band = average of 16 mel bins.
 */
function melBands(frame) {
    const out = new Float32Array(8);
    for (let b = 0; b < 8; b++) {
        let sum = 0;
        const start = b * 16;
        for (let i = 0; i < 16; i++) sum += frame[start + i];
        out[b] = sum / 16;
    }
    return out;
}

/**
 * Map 307D frame to Level 1 (Musical) uniforms.
 */
export function mapLevel1(frame, gl, prog) {
    // u_mel[8]: mel band averages
    gl.setFloatArray(prog, 'u_mel', melBands(frame));

    // u_r3[16]: selected R³ features
    const r3 = new Float32Array(16);
    const R3 = LAYOUT.r3.start; // 128

    // Consonance: roughness, stumpf_fusion, sensory_pleasantness
    r3[0] = frame[R3 + 0];   // roughness
    r3[1] = frame[R3 + 3];   // stumpf_fusion
    r3[2] = frame[R3 + 4];   // sensory_pleasantness

    // Energy: amplitude, loudness, onset_strength
    r3[3] = frame[R3 + 7];   // amplitude
    r3[4] = frame[R3 + 10];  // loudness
    r3[5] = frame[R3 + 11];  // onset_strength

    // Timbre: warmth, sharpness, tonalness, clarity
    r3[6] = frame[R3 + 12];  // warmth
    r3[7] = frame[R3 + 13];  // sharpness
    r3[8] = frame[R3 + 14];  // tonalness
    r3[9] = frame[R3 + 15];  // clarity

    // Change: spectral_flux, distribution_entropy, distribution_flatness
    r3[10] = frame[R3 + 21]; // spectral_flux
    r3[11] = frame[R3 + 22]; // distribution_entropy
    r3[12] = frame[R3 + 23]; // distribution_flatness

    // Interactions (first 3)
    r3[13] = frame[R3 + 25]; // x_amp_roughness
    r3[14] = frame[R3 + 29]; // x_vel_roughness
    r3[15] = frame[R3 + 33]; // x_flux_roughness

    gl.setFloatArray(prog, 'u_r3', r3);
}

/**
 * Map 307D frame to Level 2 (Psychological) uniforms.
 */
export function mapLevel2(frame, gl, prog) {
    // u_brain[12]: key brain dimensions for reward/emotion
    const brain = new Float32Array(12);
    brain[0]  = frame[BRAIN.wanting];
    brain[1]  = frame[BRAIN.liking];
    brain[2]  = frame[BRAIN.pleasure];
    brain[3]  = frame[BRAIN.tension];
    brain[4]  = frame[BRAIN.f03_valence];
    brain[5]  = frame[BRAIN.arousal];
    brain[6]  = frame[BRAIN.beauty];
    brain[7]  = frame[BRAIN.emotional_arc];
    brain[8]  = frame[BRAIN.prediction_error];
    brain[9]  = frame[BRAIN.emotional_momentum];
    brain[10] = frame[BRAIN.harmonic_context];
    brain[11] = frame[BRAIN.emotion_certainty];
    gl.setFloatArray(prog, 'u_brain', brain);

    // u_zeta[4]: key polarity axes from L³ ζ
    const Z = LAYOUT.zeta.start; // 267
    const zeta = new Float32Array(4);
    zeta[0] = frame[Z + 0];  // valence polarity
    zeta[1] = frame[Z + 1];  // arousal polarity
    zeta[2] = frame[Z + 2];  // tension polarity
    zeta[3] = frame[Z + 11]; // engagement polarity
    gl.setFloatArray(prog, 'u_zeta', zeta);
}

/**
 * Map 307D frame to Level 3 (Neuroscience) uniforms.
 */
export function mapLevel3(frame, gl, prog) {
    // u_beta[14]: all β neuroscience dims
    const B = LAYOUT.beta.start; // 209
    const beta = new Float32Array(14);
    for (let i = 0; i < 14; i++) beta[i] = frame[B + i];
    gl.setFloatArray(prog, 'u_beta', beta);

    // u_autonomic[6]: autonomic pathway + extras
    const autonomic = new Float32Array(6);
    autonomic[0] = frame[BRAIN.scr];
    autonomic[1] = frame[BRAIN.hr];
    autonomic[2] = frame[BRAIN.respr];
    autonomic[3] = frame[BRAIN.chills_intensity];
    autonomic[4] = frame[BRAIN.ans_composite];
    autonomic[5] = frame[BRAIN.opioid_proxy]; // da_opioid
    gl.setFloatArray(prog, 'u_autonomic', autonomic);
}

/**
 * Map background uniforms (mel bands — used by all levels).
 */
export function mapBackground(frame, gl, prog) {
    gl.setFloatArray(prog, 'u_mel', melBands(frame));
}

// ═══════════════════════════════════════════════════════════════════════
// PANEL DATA — extract human-readable values for the side panel
// ═══════════════════════════════════════════════════════════════════════

export function getPanelData(frame, level) {
    if (level === 1) {
        const R3 = LAYOUT.r3.start;
        return {
            consonance: frame[R3 + 3],        // stumpf_fusion
            pleasantness: frame[R3 + 4],       // sensory_pleasantness
            energy: frame[R3 + 7],             // amplitude
            loudness: frame[R3 + 10],          // loudness
            onset: frame[R3 + 11],             // onset_strength
            warmth: frame[R3 + 12],            // warmth
            tonalness: frame[R3 + 14],         // tonalness
            clarity: frame[R3 + 15],           // clarity
            flux: frame[R3 + 21],              // spectral_flux
        };
    }
    if (level === 2) {
        return {
            wanting: frame[BRAIN.wanting],
            liking: frame[BRAIN.liking],
            pleasure: frame[BRAIN.pleasure],
            tension: frame[BRAIN.tension],
            valence: frame[BRAIN.f03_valence],
            arousal: frame[BRAIN.arousal],
            beauty: frame[BRAIN.beauty],
            emotional_arc: frame[BRAIN.emotional_arc],
        };
    }
    if (level === 3) {
        const B = LAYOUT.beta.start;
        return {
            nacc: frame[B + 0],
            caudate: frame[B + 1],
            vta: frame[B + 2],
            stg: frame[B + 4],
            ifg: frame[B + 5],
            amygdala: frame[B + 6],
            hippocampus: frame[B + 7],
            dopamine: frame[B + 8],
            opioid: frame[B + 9],
            scr: frame[BRAIN.scr],
            hr: frame[BRAIN.hr],
            chills: frame[BRAIN.chills_intensity],
        };
    }
    return {};
}
