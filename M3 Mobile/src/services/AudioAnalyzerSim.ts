/* ── AudioAnalyzerSim — Simulated Audio Analysis for React Native ─────
 *  Since React Native doesn't have Web Audio API AnalyserNode (FFT),
 *  we simulate smooth, time-varying visualization parameters from the
 *  track's pre-computed R³ and C³ profiles.
 *
 *  Uses Perlin-like noise (simple sinusoidal composition) to modulate
 *  profile values over time, creating organic, music-responsive visuals.
 *  ──────────────────────────────────────────────────────────────── */

import type { VizParams } from "../stores/useM3AudioStore";
import type { R3Profile, C3Profile } from "../data/track-library";

/** Simple pseudo-noise function using layered sines */
function noise(t: number, seed: number): number {
  return (
    Math.sin(t * 1.3 + seed * 7.1) * 0.4 +
    Math.sin(t * 2.7 + seed * 3.3) * 0.3 +
    Math.sin(t * 4.1 + seed * 11.7) * 0.2 +
    Math.sin(t * 7.9 + seed * 5.9) * 0.1
  );
}

/** Clamp a value to [0, 1] */
function clamp01(v: number): number {
  return Math.max(0, Math.min(1, v));
}

export class AudioAnalyzerSim {
  private r3: R3Profile | null = null;
  private c3: C3Profile | null = null;
  private startTime = 0;

  /** Set the current track's profiles for simulation */
  setTrackProfile(r3: R3Profile, c3: C3Profile) {
    this.r3 = r3;
    this.c3 = c3;
    this.startTime = Date.now();
  }

  /** Clear profiles (when stopping) */
  clear() {
    this.r3 = null;
    this.c3 = null;
  }

  /**
   * Generate simulated VizParams.
   * Called at ~30fps from the audio bridge.
   * Modulates the track's static profiles with time-varying noise
   * to create organic, breathing visualizations.
   */
  getParams(): VizParams {
    if (!this.r3 || !this.c3) {
      return { energy: 0, loudness: 0, brightness: 0, tempo: 0, bass: 0, mid: 0, treble: 0 };
    }

    const elapsed = (Date.now() - this.startTime) / 1000;
    const t = elapsed * 0.5; // slow time scale for organic motion

    // Modulation amplitude scales with the track's energy
    const modAmp = 0.08 + this.r3.loudness * 0.12;

    // Derive VizParams from R³ profile + time-varying modulation
    const energy = clamp01(
      this.r3.loudness * 0.4 + this.r3.onsetStrength * 0.3 +
      this.r3.grooveStrength * 0.3 + noise(t, 1) * modAmp
    );

    const loudness = clamp01(
      this.r3.loudness + noise(t, 2) * modAmp
    );

    const brightness = clamp01(
      this.r3.brightness * 0.6 + this.r3.tonalness * 0.2 +
      this.r3.melodicClarity * 0.2 + noise(t, 3) * modAmp
    );

    // Tempo normalized to 0-1 (200 BPM = 1.0)
    const tempoBase = this.r3.tempoStability * 0.5 + this.r3.grooveStrength * 0.5;
    const tempo = clamp01(tempoBase + noise(t, 4) * modAmp * 0.5);

    // Bass from loudness + groove
    const bass = clamp01(
      this.r3.loudness * 0.5 + this.r3.grooveStrength * 0.4 +
      this.r3.onsetStrength * 0.1 + noise(t, 5) * modAmp
    );

    // Mid from melodic clarity + key clarity
    const mid = clamp01(
      this.r3.melodicClarity * 0.4 + this.r3.keyClarity * 0.3 +
      this.r3.tonalness * 0.3 + noise(t, 6) * modAmp
    );

    // Treble from brightness + spectral flux
    const treble = clamp01(
      this.r3.brightness * 0.5 + this.r3.spectralFlux * 0.3 +
      this.r3.roughness * 0.2 + noise(t, 7) * modAmp
    );

    return { energy, loudness, brightness, tempo, bass, mid, treble };
  }
}

/** Singleton */
export const audioAnalyzerSim = new AudioAnalyzerSim();
