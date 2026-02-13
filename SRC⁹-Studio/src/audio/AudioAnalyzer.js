/**
 * AudioAnalyzer — Plays WAV audio and feeds precomputed FFT data into
 * PavelFluidSimulation as splats.
 *
 * Color mapping: S³-VI 7-anchor diatonic pitch-class system
 *   C=#FF0000 D=#FF7F00 E=#FFFF00 F=#00FF00 G=#00FFFF A=#0000FF B=#8B00FF
 *
 * Frequency range: 20 Hz – 4000 Hz, log2 Y-axis mapping.
 */

// ─── S³-VI Diatonic Note Color System ───
// 7-anchor colors: MIDI pitch-class → RGB
const PITCH_CLASS_COLORS = [
  // C=0   D=2   E=4   F=5   G=7   A=9   B=11
  { pc: 0,  rgb: [255,   0,   0] },  // C  - Red
  { pc: 2,  rgb: [255, 127,   0] },  // D  - Orange
  { pc: 4,  rgb: [255, 255,   0] },  // E  - Yellow
  { pc: 5,  rgb: [  0, 255,   0] },  // F  - Green
  { pc: 7,  rgb: [  0, 255, 255] },  // G  - Cyan
  { pc: 9,  rgb: [  0,   0, 255] },  // A  - Blue
  { pc: 11, rgb: [139,   0, 255] },  // B  - Purple
];

/**
 * Frequency → diatonic interpolated RGB color.
 * Works for ANY frequency (not limited to a single octave).
 * Returns { r, g, b } in 0-1 range (for fluid sim splat).
 */
function freqToNoteColor(freq, brightness = 0.15) {
  // Freq → continuous MIDI → pitch class (0-12)
  const midi = 69 + 12 * Math.log2(freq / 440);
  const pc = ((midi % 12) + 12) % 12;

  // Find which diatonic segment this pitch class falls in
  const anchors = PITCH_CLASS_COLORS;
  let segIdx = anchors.length - 1; // default: B→C wrap
  for (let i = 0; i < anchors.length - 1; i++) {
    if (pc >= anchors[i].pc && pc < anchors[i + 1].pc) {
      segIdx = i;
      break;
    }
  }

  const cur = anchors[segIdx];
  const nxt = anchors[(segIdx + 1) % anchors.length];

  // Interpolation factor within segment
  let span = nxt.pc - cur.pc;
  if (span <= 0) span += 12; // B→C wraparound
  let t = (pc - cur.pc);
  if (t < 0) t += 12;
  t /= span;

  // Linear RGB interpolation, scaled to 0-1 with brightness
  const r = (cur.rgb[0] + t * (nxt.rgb[0] - cur.rgb[0])) / 255 * brightness;
  const g = (cur.rgb[1] + t * (nxt.rgb[1] - cur.rgb[1])) / 255 * brightness;
  const b = (cur.rgb[2] + t * (nxt.rgb[2] - cur.rgb[2])) / 255 * brightness;

  return { r, g, b };
}

/**
 * Frequency → Y position on canvas (log2 scale, 20Hz–4kHz).
 * Low freq = bottom (Y=1), high freq = top (Y=0).
 */
function freqToY(freq, minFreq = 20, maxFreq = 4000) {
  const t = Math.log2(freq / minFreq) / Math.log2(maxFreq / minFreq);
  return 1 - Math.min(1, Math.max(0, t));
}


export default class AudioAnalyzer {
  constructor(fluidSim, options = {}) {
    this.fluidSim = fluidSim;
    this.ctx = null;
    this.source = null;
    this.gainNode = null;
    this.playing = false;
    this.rafId = null;

    // Precomputed FFT data
    this.fftData = null;     // { meta, frames }
    this.fftLoaded = false;

    // Audio buffer (for playback only)
    this.audioBuffer = null;

    // Timing
    this.startTime = 0;      // AudioContext.currentTime at play()
    this.pauseOffset = 0;    // seconds elapsed before last pause

    // Config
    this.gain = options.gain || 1.0;
    this.splatsPerFrame = options.splatsPerFrame || 32;
    this.brightness = options.brightness || 0.15;
  }

  /**
   * Load precomputed FFT JSON.
   */
  async loadFFT(url) {
    const res = await fetch(url);
    this.fftData = await res.json();
    this.fftLoaded = true;
    console.log(`FFT loaded: ${this.fftData.meta.num_frames} frames @ ${this.fftData.meta.frame_rate}fps`);
  }

  /**
   * Load WAV for audio playback (no real-time analysis).
   */
  async loadAudio(url) {
    this.ctx = new AudioContext();
    const res = await fetch(url);
    const buf = await res.arrayBuffer();
    this.audioBuffer = await this.ctx.decodeAudioData(buf);

    this.gainNode = this.ctx.createGain();
    this.gainNode.gain.value = this.gain;
    this.gainNode.connect(this.ctx.destination);
  }

  get duration() {
    return this.audioBuffer ? this.audioBuffer.duration : 0;
  }

  get elapsed() {
    if (!this.playing) return this.pauseOffset;
    return this.pauseOffset + (this.ctx.currentTime - this.startTime);
  }

  play() {
    if (!this.audioBuffer || this.playing) return;

    this.source = this.ctx.createBufferSource();
    this.source.buffer = this.audioBuffer;
    this.source.connect(this.gainNode);
    this.source.start(0, this.pauseOffset);
    this.startTime = this.ctx.currentTime;
    this.playing = true;

    this.source.onended = () => {
      this.playing = false;
    };

    this._tick();
  }

  pause() {
    if (!this.playing) return;
    this.pauseOffset += this.ctx.currentTime - this.startTime;
    this.source.stop();
    this.playing = false;
    if (this.rafId) cancelAnimationFrame(this.rafId);
  }

  /**
   * Main tick — reads precomputed FFT frame, creates splats on fluid sim.
   */
  _tick() {
    if (!this.playing) return;

    if (this.fftLoaded && this.fluidSim) {
      const elapsed = this.elapsed;
      const frameIdx = Math.min(
        this.fftData.meta.num_frames - 1,
        Math.floor(elapsed * this.fftData.meta.frame_rate)
      );

      const peaks = this.fftData.frames[frameIdx];
      if (peaks && peaks.length > 0) {
        // -60 dB gate: only visualize peaks within 60 dB of the frame's loudest
        const peakAmp = peaks[0][1]; // peaks are sorted by amplitude desc
        const dbFloor = peakAmp * 0.1; // 10^(-20/20)
        const count = Math.min(peaks.length, this.splatsPerFrame);

        for (let i = 0; i < count; i++) {
          const [freq, amp] = peaks[i];
          if (amp < dbFloor) continue; // below -60 dB relative to frame peak

          // Y from log2 frequency
          const y = freqToY(freq, this.fftData.meta.min_freq, this.fftData.meta.max_freq);

          // X: spread across canvas center
          const x = 0.25 + Math.random() * 0.5;

          // Color from S³-VI diatonic note system
          const color = freqToNoteColor(freq, this.brightness * amp);

          // Velocity: gentle upward drift for high, downward for low
          const drift = (0.5 - y) * 150;
          const dx = (Math.random() - 0.5) * 250 * amp;
          const dy = drift + (Math.random() - 0.5) * 150 * amp;

          // Radius scales with amplitude
          const savedRadius = this.fluidSim.config.SPLAT_RADIUS;
          this.fluidSim.config.SPLAT_RADIUS = 0.08 + amp * 0.35;
          this.fluidSim.splat(x, y, dx, dy, color);
          this.fluidSim.config.SPLAT_RADIUS = savedRadius;
        }
      }
    }

    this.rafId = requestAnimationFrame(() => this._tick());
  }

  destroy() {
    this.pause();
    if (this.ctx) {
      this.ctx.close();
      this.ctx = null;
    }
  }
}
