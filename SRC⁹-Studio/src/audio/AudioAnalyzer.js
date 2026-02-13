/**
 * AudioAnalyzer — Loads a WAV/MP3, plays it, and provides real-time FFT data.
 * Feeds spectral data into PavelFluidSimulation as splats.
 */
export default class AudioAnalyzer {
  constructor(fluidSim, options = {}) {
    this.fluidSim = fluidSim;
    this.ctx = null;
    this.analyser = null;
    this.source = null;
    this.freqData = null;
    this.rafId = null;
    this.playing = false;

    // Config
    this.fftSize = options.fftSize || 2048;
    this.minFreq = options.minFreq || 20;
    this.maxFreq = options.maxFreq || 4000;
    this.splatsPerFrame = options.splatsPerFrame || 32;  // How many frequency bands to splat
    this.gain = options.gain || 1.0;
  }

  async load(url) {
    this.ctx = new AudioContext();
    const response = await fetch(url);
    const arrayBuffer = await response.arrayBuffer();
    this.audioBuffer = await this.ctx.decodeAudioData(arrayBuffer);

    // Analyzer
    this.analyser = this.ctx.createAnalyser();
    this.analyser.fftSize = this.fftSize;
    this.analyser.smoothingTimeConstant = 0.8;
    this.freqData = new Uint8Array(this.analyser.frequencyBinCount);

    // Gain node
    this.gainNode = this.ctx.createGain();
    this.gainNode.gain.value = this.gain;
    this.gainNode.connect(this.ctx.destination);
  }

  play() {
    if (!this.audioBuffer || this.playing) return;

    // Create new source each play
    this.source = this.ctx.createBufferSource();
    this.source.buffer = this.audioBuffer;
    this.source.connect(this.analyser);
    this.analyser.connect(this.gainNode);
    this.source.start(0);
    this.playing = true;

    this.source.onended = () => { this.playing = false; };

    // Start analysis loop
    this._tick();
  }

  pause() {
    if (this.source && this.playing) {
      this.source.stop();
      this.playing = false;
    }
    if (this.rafId) cancelAnimationFrame(this.rafId);
  }

  /**
   * Returns current FFT as array of { freq, amplitude01 } objects
   * Filtered to minFreq-maxFreq range
   */
  getSpectralData() {
    if (!this.analyser || !this.freqData) return [];

    this.analyser.getByteFrequencyData(this.freqData);
    const binCount = this.analyser.frequencyBinCount;
    const sampleRate = this.ctx.sampleRate;
    const binWidth = sampleRate / this.fftSize;

    const minBin = Math.max(1, Math.floor(this.minFreq / binWidth));
    const maxBin = Math.min(binCount - 1, Math.ceil(this.maxFreq / binWidth));

    const result = [];
    for (let i = minBin; i <= maxBin; i++) {
      const freq = i * binWidth;
      const amplitude01 = this.freqData[i] / 255;
      if (amplitude01 > 0.02) {  // Noise gate
        result.push({ freq, amplitude01, bin: i });
      }
    }
    return result;
  }

  /**
   * Convert frequency to hue (log scale, 20Hz-4kHz → 0-1)
   */
  freqToHue(freq) {
    return Math.log2(freq / this.minFreq) / Math.log2(this.maxFreq / this.minFreq);
  }

  /**
   * Convert frequency to Y position on canvas (log scale)
   * Low freq = bottom, high freq = top
   */
  freqToY(freq) {
    const t = Math.log2(freq / this.minFreq) / Math.log2(this.maxFreq / this.minFreq);
    return 1 - Math.min(1, Math.max(0, t));  // Invert: low freq at bottom
  }

  /**
   * HSV to RGB
   */
  _hsvToRgb(h, s, v) {
    let r, g, b, i = Math.floor(h * 6), f = h * 6 - i;
    const p = v * (1 - s), q = v * (1 - f * s), t = v * (1 - (1 - f) * s);
    switch (i % 6) {
      case 0: r = v; g = t; b = p; break;
      case 1: r = q; g = v; b = p; break;
      case 2: r = p; g = v; b = t; break;
      case 3: r = p; g = q; b = v; break;
      case 4: r = t; g = p; b = v; break;
      case 5: r = v; g = p; b = q; break;
    }
    return { r, g, b };
  }

  /**
   * Main analysis tick — sends splats to fluid simulation
   */
  _tick() {
    if (!this.playing) return;

    const spectral = this.getSpectralData();

    if (spectral.length > 0 && this.fluidSim) {
      // Select top N bands by amplitude
      const sorted = spectral.sort((a, b) => b.amplitude01 - a.amplitude01);
      const topBands = sorted.slice(0, this.splatsPerFrame);

      for (const band of topBands) {
        const y = this.freqToY(band.freq);
        const x = 0.3 + Math.random() * 0.4;  // Center-ish horizontal spread

        // Color from frequency
        const hue = this.freqToHue(band.freq);
        const color = this._hsvToRgb(hue, 0.85, band.amplitude01 * 0.2);

        // Velocity — slight upward drift for high freq, downward for low
        const drift = (y - 0.5) * 200;
        const dx = (Math.random() - 0.5) * 300 * band.amplitude01;
        const dy = drift + (Math.random() - 0.5) * 200 * band.amplitude01;

        // Radius scales with amplitude
        const savedRadius = this.fluidSim.config.SPLAT_RADIUS;
        this.fluidSim.config.SPLAT_RADIUS = 0.1 + band.amplitude01 * 0.4;

        this.fluidSim.splat(x, y, dx, dy, color);

        this.fluidSim.config.SPLAT_RADIUS = savedRadius;
      }
    }

    this.rafId = requestAnimationFrame(() => this._tick());
  }

  /**
   * Get summary data for HUD panels
   */
  getSummary() {
    const spectral = this.getSpectralData();
    if (spectral.length === 0) return null;

    let totalEnergy = 0;
    let weightedFreq = 0;
    let maxAmp = 0;
    let lowEnergy = 0, midEnergy = 0, highEnergy = 0;

    for (const band of spectral) {
      totalEnergy += band.amplitude01;
      weightedFreq += band.freq * band.amplitude01;
      if (band.amplitude01 > maxAmp) maxAmp = band.amplitude01;

      if (band.freq < 250) lowEnergy += band.amplitude01;
      else if (band.freq < 2000) midEnergy += band.amplitude01;
      else highEnergy += band.amplitude01;
    }

    const centroid = totalEnergy > 0 ? weightedFreq / totalEnergy : 0;
    const rms = totalEnergy / Math.max(1, spectral.length);

    return {
      centroid,
      rms,
      peakAmplitude: maxAmp,
      bandCount: spectral.length,
      lowEnergy: lowEnergy / Math.max(1, spectral.length),
      midEnergy: midEnergy / Math.max(1, spectral.length),
      highEnergy: highEnergy / Math.max(1, spectral.length),
      brightness: centroid / this.maxFreq,
    };
  }

  destroy() {
    this.pause();
    if (this.ctx) {
      this.ctx.close();
      this.ctx = null;
    }
  }
}
