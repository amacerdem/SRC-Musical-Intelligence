/**
 * audio.js — Web Audio API playback with precise timing sync.
 * S³ Musical Intelligence Demo
 */
export class AudioPlayer {
    constructor() {
        this.ctx = null;
        this.buffer = null;
        this.source = null;
        this.startOffset = 0;
        this.startTime = 0;
        this.playing = false;
        this.duration = 0;
        this._onEnd = null;
    }

    async load(url, onProgress) {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }

        const response = await fetch(url);
        if (!response.ok) throw new Error(`Failed to load audio: ${response.status}`);

        const total = parseInt(response.headers.get('Content-Length') || '0');
        const reader = response.body.getReader();
        const chunks = [];
        let received = 0;

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            chunks.push(value);
            received += value.length;
            if (onProgress && total > 0) onProgress(received / total);
        }

        const raw = new Uint8Array(received);
        let offset = 0;
        for (const c of chunks) { raw.set(c, offset); offset += c.length; }

        this.buffer = await this.ctx.decodeAudioData(raw.buffer);
        this.duration = this.buffer.duration;
        console.log(`Audio loaded: ${this.duration.toFixed(1)}s`);
    }

    play(fromTime) {
        if (!this.buffer) return;
        this.stop();

        if (this.ctx.state === 'suspended') this.ctx.resume();

        this.source = this.ctx.createBufferSource();
        this.source.buffer = this.buffer;
        this.source.connect(this.ctx.destination);
        this.source.onended = () => {
            this.playing = false;
            if (this._onEnd) this._onEnd();
        };

        const offset = fromTime || this.startOffset;
        this.startOffset = offset;
        this.startTime = this.ctx.currentTime;
        this.source.start(0, offset);
        this.playing = true;
    }

    pause() {
        if (!this.playing) return;
        this.startOffset = this.currentTime;
        this.stop();
    }

    stop() {
        if (this.source) {
            try { this.source.stop(); } catch(e) {}
            this.source.disconnect();
            this.source = null;
        }
        this.playing = false;
    }

    seek(timeSec) {
        const wasPlaying = this.playing;
        this.stop();
        this.startOffset = Math.max(0, Math.min(timeSec, this.duration));
        if (wasPlaying) this.play(this.startOffset);
    }

    get currentTime() {
        if (!this.playing) return this.startOffset;
        return this.startOffset + (this.ctx.currentTime - this.startTime);
    }

    get progress() {
        return this.duration > 0 ? this.currentTime / this.duration : 0;
    }

    onEnd(cb) { this._onEnd = cb; }
}
