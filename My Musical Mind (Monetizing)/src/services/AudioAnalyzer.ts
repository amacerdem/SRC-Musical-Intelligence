/* ── AudioAnalyzer — FFT → 15 Mind Visualization Parameters ─────────
 *  Reads real-time audio from an AnalyserNode and extracts:
 *    - 10 R³ musical parameters (from frequency/time-domain data)
 *    - 5 C³ cognitive parameters (blended from track profile + real-time)
 *  All values are EMA-smoothed to prevent jitter.
 *
 *  Usage:
 *    const analyzer = new AudioAnalyzer(analyserNode);
 *    analyzer.setTrackProfile(track.r3Profile, track.c3Profile);
 *    const params = analyzer.getParameters();  // call every frame
 *  ──────────────────────────────────────────────────────────────── */

import type { R3Profile, C3Profile } from "@/data/track-library";

export interface MindVisualizerParams {
  // R³ Musical (10)
  roughness: number;
  spectralFlux: number;
  loudness: number;
  keyClarity: number;
  onsetStrength: number;
  melodicClarity: number;
  brightness: number;
  tempoStability: number;
  tonalness: number;
  grooveStrength: number;
  // C³ Cognitive (5)
  harmonicConsonance: number;
  rhythmicSync: number;
  patternPredictability: number;
  memoryRecognition: number;
  wanting: number;
}

const EMA_ALPHA = 0.12;
const C3_STATIC_WEIGHT = 0.30;
const C3_REALTIME_WEIGHT = 0.70;
const C3_EMA_ALPHA = 0.05;

export class AudioAnalyzer {
  private analyser: AnalyserNode;
  private freqData: Uint8Array;
  private timeData: Uint8Array;
  private prevFreqData: Float32Array;
  private prevRMS = 0;
  private smoothed: MindVisualizerParams;
  private c3Smoothed: C3Profile;
  private trackR3: R3Profile | null = null;
  private trackC3: C3Profile | null = null;
  private frameCount = 0;

  constructor(analyser: AnalyserNode) {
    this.analyser = analyser;
    const bins = analyser.frequencyBinCount;
    this.freqData = new Uint8Array(bins);
    this.timeData = new Uint8Array(bins);
    this.prevFreqData = new Float32Array(bins);

    this.smoothed = {
      roughness: 0, spectralFlux: 0, loudness: 0, keyClarity: 0,
      onsetStrength: 0, melodicClarity: 0, brightness: 0,
      tempoStability: 0, tonalness: 0, grooveStrength: 0,
      harmonicConsonance: 0, rhythmicSync: 0, patternPredictability: 0,
      memoryRecognition: 0, wanting: 0,
    };
    this.c3Smoothed = {
      harmonicConsonance: 0, rhythmicSync: 0, patternPredictability: 0,
      memoryRecognition: 0, wanting: 0,
    };
  }

  /** Set the static track profile for C³ blending */
  setTrackProfile(r3: R3Profile, c3: C3Profile) {
    this.trackR3 = r3;
    this.trackC3 = c3;
  }

  /** Extract 15 parameters from current audio frame. Call every rAF. */
  getParameters(): MindVisualizerParams {
    this.analyser.getByteFrequencyData(this.freqData);
    this.analyser.getByteTimeDomainData(this.timeData);
    this.frameCount++;

    const bins = this.freqData.length;
    const sampleRate = this.analyser.context.sampleRate;
    const nyquist = sampleRate / 2;
    const binHz = nyquist / bins;

    // ── RMS (loudness) ──────────────────────────
    let sumSq = 0;
    for (let i = 0; i < this.timeData.length; i++) {
      const v = (this.timeData[i] - 128) / 128;
      sumSq += v * v;
    }
    const rms = Math.sqrt(sumSq / this.timeData.length);
    const loudness = Math.min(1, rms * 3.5);

    // ── Spectral Flux (change between frames) ───
    let fluxSum = 0;
    for (let i = 0; i < bins; i++) {
      const diff = this.freqData[i] / 255 - this.prevFreqData[i];
      if (diff > 0) fluxSum += diff;
    }
    const spectralFlux = Math.min(1, fluxSum / (bins * 0.15));

    // ── Onset Strength (RMS derivative) ─────────
    const rmsDerivative = Math.abs(rms - this.prevRMS);
    const onsetStrength = Math.min(1, rmsDerivative * 12);

    // ── Brightness (spectral centroid) ──────────
    let weightedSum = 0, totalEnergy = 0;
    for (let i = 0; i < bins; i++) {
      const e = this.freqData[i] / 255;
      weightedSum += i * e;
      totalEnergy += e;
    }
    const centroid = totalEnergy > 0 ? weightedSum / totalEnergy : 0;
    const brightness = Math.min(1, centroid / (bins * 0.5));

    // ── Roughness (2-8kHz energy ratio) ─────────
    const lowBin = Math.floor(2000 / binHz);
    const highBin = Math.min(bins - 1, Math.floor(8000 / binHz));
    let roughEnergy = 0, totalE = 0;
    for (let i = 0; i < bins; i++) {
      const e = this.freqData[i] / 255;
      totalE += e;
      if (i >= lowBin && i <= highBin) roughEnergy += e;
    }
    const roughness = totalE > 0 ? Math.min(1, (roughEnergy / totalE) * 2.5) : 0;

    // ── Key Clarity (peak-to-mean ratio) ────────
    let maxBin = 0, sumBin = 0;
    for (let i = 1; i < bins; i++) {
      const e = this.freqData[i];
      if (e > maxBin) maxBin = e;
      sumBin += e;
    }
    const meanBin = sumBin / bins;
    const keyClarity = meanBin > 0 ? Math.min(1, (maxBin / 255) / (meanBin / 255 + 0.1) * 0.3) : 0;

    // ── Melodic Clarity (harmonic peak detection) ──
    let peaks = 0;
    for (let i = 2; i < bins - 2; i++) {
      if (
        this.freqData[i] > this.freqData[i - 1] &&
        this.freqData[i] > this.freqData[i + 1] &&
        this.freqData[i] > 60
      ) {
        peaks++;
      }
    }
    const melodicClarity = Math.min(1, peaks / 30);

    // ── Tonalness (harmonic-to-noise ratio) ─────
    // Simple approximation: energy in pitched bins vs total
    let tonalEnergy = 0;
    for (let i = 0; i < bins; i++) {
      if (this.freqData[i] > meanBin * 1.2) {
        tonalEnergy += this.freqData[i] / 255;
      }
    }
    const tonalness = totalE > 0 ? Math.min(1, tonalEnergy / totalE * 1.8) : 0;

    // ── Tempo Stability (envelope autocorrelation approximation) ──
    // Use variance of RMS over time as proxy (lower variance = more stable)
    const tempoStability = loudness > 0.01
      ? Math.min(1, 1 - Math.min(1, onsetStrength * 2))
      : 0;

    // ── Groove Strength (sub-bass + onset regularity) ──
    const subBassBin = Math.min(bins - 1, Math.floor(120 / binHz));
    let subBassEnergy = 0;
    for (let i = 0; i <= subBassBin; i++) {
      subBassEnergy += this.freqData[i] / 255;
    }
    const subBassRatio = totalE > 0 ? subBassEnergy / totalE : 0;
    const grooveStrength = Math.min(1, subBassRatio * 4 + onsetStrength * 0.3);

    // ── Raw R³ values ───────────────────────────
    const rawR3 = {
      roughness, spectralFlux, loudness, keyClarity, onsetStrength,
      melodicClarity, brightness, tempoStability, tonalness, grooveStrength,
    };

    // ── EMA smooth R³ ───────────────────────────
    const r3Keys = Object.keys(rawR3) as (keyof typeof rawR3)[];
    for (const key of r3Keys) {
      this.smoothed[key] = this.smoothed[key] * (1 - EMA_ALPHA) + rawR3[key] * EMA_ALPHA;
    }

    // ── C³ Cognitive: blend static profile + real-time modulation ──
    if (this.trackC3) {
      // Derive C³ from R³ in real-time
      const rtC3 = {
        harmonicConsonance: tonalness * 0.5 + keyClarity * 0.3 + (1 - roughness) * 0.2,
        rhythmicSync: grooveStrength * 0.4 + tempoStability * 0.3 + onsetStrength * 0.3,
        patternPredictability: tempoStability * 0.4 + (1 - spectralFlux) * 0.3 + keyClarity * 0.3,
        memoryRecognition: tonalness * 0.3 + melodicClarity * 0.4 + (1 - roughness) * 0.3,
        wanting: loudness * 0.25 + grooveStrength * 0.25 + brightness * 0.2 + onsetStrength * 0.3,
      };

      // Blend static (30%) + real-time (70%)
      const c3Keys = Object.keys(this.trackC3) as (keyof C3Profile)[];
      for (const key of c3Keys) {
        const blended = this.trackC3[key] * C3_STATIC_WEIGHT + rtC3[key] * C3_REALTIME_WEIGHT;
        // Slow EMA for cognitive parameters
        this.c3Smoothed[key] = this.c3Smoothed[key] * (1 - C3_EMA_ALPHA) + blended * C3_EMA_ALPHA;
        this.smoothed[key] = this.c3Smoothed[key];
      }
    }

    // Store current frame for next diff
    for (let i = 0; i < bins; i++) {
      this.prevFreqData[i] = this.freqData[i] / 255;
    }
    this.prevRMS = rms;

    return { ...this.smoothed };
  }

  /** Reset all smoothed values */
  reset() {
    const keys = Object.keys(this.smoothed) as (keyof MindVisualizerParams)[];
    for (const k of keys) this.smoothed[k] = 0;
    const c3Keys = Object.keys(this.c3Smoothed) as (keyof C3Profile)[];
    for (const k of c3Keys) this.c3Smoothed[k] = 0;
    this.prevRMS = 0;
    this.frameCount = 0;
    this.prevFreqData.fill(0);
  }
}
