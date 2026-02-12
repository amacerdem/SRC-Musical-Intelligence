/**
 * data.js — MI01 binary data loader + frame accessor.
 * S³ Musical Intelligence Demo
 *
 * Binary format:
 *   HEADER       32 bytes
 *   DIM_INDEX    307 × 32 bytes
 *   FRAME_DATA   T × 307 × Float16
 */

const HEADER_SIZE = 32;
const DIM_NAME_SIZE = 32;
const TOTAL_DIM = 307;
const FRAME_RATE = 172.265625;

// MI-space layout offsets (absolute in 307D)
export const LAYOUT = {
    cochlea:   { start: 0,   end: 128, dim: 128 },
    r3:        { start: 128, end: 177, dim: 49 },
    brain:     { start: 177, end: 203, dim: 26 },
    l3:        { start: 203, end: 307, dim: 104 },

    // Brain sub-pathways (absolute offsets)
    shared:    { start: 177, end: 181 },
    reward:    { start: 181, end: 190 },
    affect:    { start: 190, end: 196 },
    autonomic: { start: 196, end: 201 },
    integration: { start: 201, end: 203 },

    // L³ sub-groups (absolute offsets)
    alpha:   { start: 203, end: 209 },
    beta:    { start: 209, end: 223 },
    gamma:   { start: 223, end: 236 },
    delta:   { start: 236, end: 248 },
    epsilon: { start: 248, end: 267 },
    zeta:    { start: 267, end: 279 },
    eta:     { start: 279, end: 291 },
    theta:   { start: 291, end: 307 },
};

// Named brain dimension indices (absolute in 307D)
export const BRAIN = {
    arousal:            177,
    prediction_error:   178,
    harmonic_context:   179,
    emotional_momentum: 180,
    da_caudate:         181,
    da_nacc:            182,
    opioid_proxy:       183,
    wanting:            184,
    liking:             185,
    pleasure:           186,
    tension:            187,
    prediction_match:   188,
    reward_forecast:    189,
    f03_valence:        190,
    mode_signal:        191,
    consonance_valence: 192,
    happy_pathway:      193,
    sad_pathway:        194,
    emotion_certainty:  195,
    scr:                196,
    hr:                 197,
    respr:              198,
    chills_intensity:   199,
    ans_composite:      200,
    beauty:             201,
    emotional_arc:      202,
};

export class MIData {
    constructor() {
        this.loaded = false;
        this.frames = null;   // Float32Array — (T × 307) flat
        this.dimNames = [];
        this.nFrames = 0;
        this.nDims = TOTAL_DIM;
        this.durationMs = 0;
        this.frameRate = FRAME_RATE;
    }

    async load(url, onProgress) {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to load ${url}: ${response.status}`);

        const total = parseInt(response.headers.get('Content-Length') || '0');
        const reader = response.body.getReader();
        const chunks = [];
        let received = 0;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            received += value.length;
            if (onProgress && total > 0) {
                onProgress(received / total);
            }
        }

        // Combine chunks
        const buffer = new Uint8Array(received);
        let offset = 0;
        for (const chunk of chunks) {
            buffer.set(chunk, offset);
            offset += chunk.length;
        }

        this._parse(buffer.buffer);
    }

    _parse(buffer) {
        const view = new DataView(buffer);

        // ─── Header ──────────────────────────────────
        const magic = String.fromCharCode(
            view.getUint8(0), view.getUint8(1), view.getUint8(2), view.getUint8(3)
        );
        if (magic !== 'MI01') throw new Error(`Invalid magic: ${magic}`);

        const version = view.getUint32(4, true);
        this.nFrames = view.getUint32(8, true);
        this.nDims = view.getUint32(12, true);
        const sampleRate = view.getUint32(16, true);
        const hopLength = view.getUint32(20, true);
        this.durationMs = view.getUint32(24, true);
        this.frameRate = sampleRate / hopLength;

        console.log(`MI01 v${version}: ${this.nFrames} frames × ${this.nDims}D, ${(this.durationMs/1000).toFixed(1)}s`);

        // ─── Dimension Names ─────────────────────────
        const nameOffset = HEADER_SIZE;
        const decoder = new TextDecoder('ascii');
        this.dimNames = [];
        for (let i = 0; i < this.nDims; i++) {
            const start = nameOffset + i * DIM_NAME_SIZE;
            const bytes = new Uint8Array(buffer, start, DIM_NAME_SIZE);
            const nullIdx = bytes.indexOf(0);
            const name = decoder.decode(bytes.subarray(0, nullIdx >= 0 ? nullIdx : DIM_NAME_SIZE));
            this.dimNames.push(name);
        }

        // ─── Frame Data (Float16 → Float32) ─────────
        const dataOffset = HEADER_SIZE + this.nDims * DIM_NAME_SIZE;
        const f16 = new Uint16Array(buffer, dataOffset, this.nFrames * this.nDims);
        this.frames = new Float32Array(this.nFrames * this.nDims);

        for (let i = 0; i < f16.length; i++) {
            this.frames[i] = float16ToFloat32(f16[i]);
        }

        this.loaded = true;
        console.log(`Loaded: ${(buffer.byteLength / 1024 / 1024).toFixed(1)} MB`);
    }

    /**
     * Get frame data at a given time in seconds.
     * Returns a Float32Array view of 307 dimensions.
     */
    getFrame(timeSec) {
        if (!this.loaded) return null;
        const idx = Math.min(
            Math.max(0, Math.floor(timeSec * this.frameRate)),
            this.nFrames - 1
        );
        const offset = idx * this.nDims;
        return this.frames.subarray(offset, offset + this.nDims);
    }

    /**
     * Get a single dimension value at time.
     */
    getDim(timeSec, dimIndex) {
        const frame = this.getFrame(timeSec);
        return frame ? frame[dimIndex] : 0;
    }

    /**
     * Get a range of dimensions at time.
     */
    getRange(timeSec, start, end) {
        const frame = this.getFrame(timeSec);
        return frame ? frame.subarray(start, end) : new Float32Array(end - start);
    }
}

// ─── Float16 Decoder ─────────────────────────────────
function float16ToFloat32(h) {
    const sign = (h >> 15) & 1;
    const exp = (h >> 10) & 0x1f;
    const frac = h & 0x3ff;

    if (exp === 0) {
        if (frac === 0) return sign ? -0 : 0;
        // Denormalized
        const f = frac / 1024;
        return (sign ? -1 : 1) * f * Math.pow(2, -14);
    }
    if (exp === 0x1f) {
        return frac ? NaN : (sign ? -Infinity : Infinity);
    }
    return (sign ? -1 : 1) * Math.pow(2, exp - 15) * (1 + frac / 1024);
}

export { FRAME_RATE, TOTAL_DIM };
