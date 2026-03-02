/* ── peakExtractor — Extract spectral peaks from MI mel data ─────────
 *  Pre-computes peak positions, colors, sizes for GPU upload.
 *  All 16 peaks per frame extracted; peak count filtering (4/8/16)
 *  is handled by a shader uniform at render time.
 *  ──────────────────────────────────────────────────────────────────── */

/* ── MelData type (from MI pipeline binary) ────────────────────────── */

export interface MelData {
  nMels: number;            // 128
  nFrames: number;          // T
  frameRate: number;        // 172.265625
  centerFreqs: Float32Array; // 128 mel bin center frequencies (Hz)
  data: Uint8Array;         // (nFrames × nMels) frame-contiguous
}

/* ── PeakBuffers — typed arrays ready for GPU ──────────────────────── */

export interface PeakBuffers {
  positions: Float32Array;  // (nFrames * 16) * 3 — x=time(s), y=log2freq(0-1), z=0
  colors: Float32Array;     // (nFrames * 16) * 3 — note-spectrum RGB
  sizes: Float32Array;      // (nFrames * 16)      — amplitude-proportional
  ranks: Float32Array;      // (nFrames * 16)      — 0-15, for peak count filtering
  totalPoints: number;      // nFrames * 16
}

/* ── Constants ─────────────────────────────────────────────────────── */

const PIANO_MIN_HZ = 27.5;     // A0
const PIANO_MAX_HZ = 4186.01;  // C8
const LOG2_MIN = Math.log2(PIANO_MIN_HZ);
const LOG2_MAX = Math.log2(PIANO_MAX_HZ);
const LOG2_RANGE = LOG2_MAX - LOG2_MIN;

const MAX_PEAKS = 16;
const AMP_THRESHOLD = 10; // uint8, out of 255

/* ── Diatonic pitch-class color spectrum (S³-VI reference) ────────────
 *  7 diatonic anchors mapped to ROYGBIV, direct RGB interpolation.
 *  Ported from S³-VI/ColorSpectrum/freqToColor.js.
 *  Octave-repeating: same note class = same color regardless of octave.
 *
 *  Segments (semitone boundaries):
 *    C [0,2)  D [2,4)  E [4,5)  F [5,7)  G [7,9)  A [9,11)  B [11,12)
 *  ── */

const DIATONIC_COLORS: [number, number, number][] = [
  [1.000, 0.000, 0.000],  // C  — Red
  [1.000, 0.498, 0.000],  // D  — Orange
  [1.000, 1.000, 0.000],  // E  — Yellow
  [0.000, 1.000, 0.000],  // F  — Green
  [0.000, 1.000, 1.000],  // G  — Cyan
  [0.000, 0.000, 1.000],  // A  — Blue
  [0.545, 0.000, 1.000],  // B  — Purple
];

const DIATONIC_SEGMENTS: [number, number][] = [
  [0, 2],   // C → D
  [2, 4],   // D → E
  [4, 5],   // E → F
  [5, 7],   // F → G
  [7, 9],   // G → A
  [9, 11],  // A → B
  [11, 12], // B → C (wrap)
];

/** Frequency → diatonic-spectrum RGB in [0,1] range.
 *  Direct RGB interpolation between 7 ROYGBIV anchors.
 *  Octave-repeating: C=Red, D=Orange, E=Yellow, F=Green, G=Cyan, A=Blue, B=Purple. */
export function freqToColor(freq: number): [number, number, number] {
  const midi = 69 + 12 * Math.log2(freq / 440);
  const pc = ((midi % 12) + 12) % 12; // continuous pitch class 0-12

  // Find diatonic segment
  for (let i = 0; i < DIATONIC_SEGMENTS.length; i++) {
    const [start, end] = DIATONIC_SEGMENTS[i];
    const next = (i + 1) % 7;

    if (i < 6 ? (pc >= start && pc < end) : (pc >= start || pc < DIATONIC_SEGMENTS[0][0])) {
      // Compute interpolation factor within segment
      let t: number;
      if (i < 6) {
        t = (pc - start) / (end - start);
      } else {
        // B→C wrap: segment is [11, 12/0)
        t = pc >= start
          ? (pc - start) / (12 - start)
          : (pc + 12 - start) / (12 - start);
      }

      const c0 = DIATONIC_COLORS[i];
      const c1 = DIATONIC_COLORS[next];
      return [
        c0[0] + t * (c1[0] - c0[0]),
        c0[1] + t * (c1[1] - c0[1]),
        c0[2] + t * (c1[2] - c0[2]),
      ];
    }
  }

  return DIATONIC_COLORS[0]; // fallback: red
}

/** Frequency → normalized log2 position (0 = A0 bottom, 1 = C8 top) */
function freqToLog2Norm(freq: number): number {
  return (Math.log2(freq) - LOG2_MIN) / LOG2_RANGE;
}

/* ── Parabolic interpolation for sub-bin frequency estimation ────────
 *  Given amplitudes at bins (b-1, b, b+1), estimates the true peak
 *  offset δ ∈ [-0.5, +0.5] from bin center using:
 *    δ = 0.5 × (α − γ) / (α − 2β + γ)
 *  where α = amp[b-1], β = amp[b], γ = amp[b+1].
 *  Frequency is interpolated in log2 space (mel bins are ~log-spaced).
 *  ──────────────────────────────────────────────────────────────────── */

function interpolateFreq(
  centerFreqs: Float32Array,
  data: Uint8Array,
  frameOff: number,
  b: number,
  nMels: number,
): number {
  if (b <= 0 || b >= nMels - 1) return centerFreqs[b];

  const alpha = data[frameOff + b - 1]; // left neighbor
  const beta  = data[frameOff + b];     // peak bin
  const gamma = data[frameOff + b + 1]; // right neighbor

  const denom = alpha - 2 * beta + gamma;
  if (denom >= 0) return centerFreqs[b]; // concave check — no valid peak shape

  const delta = 0.5 * (alpha - gamma) / denom; // offset in bins, [-0.5, +0.5]

  // Interpolate in log2 space for mel-scale accuracy
  const log2f0 = Math.log2(centerFreqs[b]);
  const log2Left  = Math.log2(centerFreqs[b - 1]);
  const log2Right = Math.log2(centerFreqs[b + 1]);

  const log2Step = delta < 0
    ? log2f0 - log2Left    // step toward left neighbor
    : log2Right - log2f0;  // step toward right neighbor

  return Math.pow(2, log2f0 + delta * log2Step);
}

/* ── Main extraction function ─────────────────────────────────────── */

export function extractPeaks(mel: MelData): PeakBuffers {
  const { nFrames, nMels, frameRate, centerFreqs, data } = mel;
  const totalPoints = nFrames * MAX_PEAKS;

  const positions = new Float32Array(totalPoints * 3);
  const colors = new Float32Array(totalPoints * 3);
  const sizes = new Float32Array(totalPoints);
  const ranks = new Float32Array(totalPoints);

  // Temp array for sorting peaks per frame
  const framePeaks: { amp: number; freq: number; bin: number }[] = [];

  for (let t = 0; t < nFrames; t++) {
    const frameOff = t * nMels;
    const timeS = t / frameRate;

    // Collect LOCAL MAXIMA above threshold within piano range
    // A local maximum is a bin with amplitude > both neighbors
    framePeaks.length = 0;
    for (let b = 1; b < nMels - 1; b++) {
      const amp = data[frameOff + b];
      if (amp <= AMP_THRESHOLD) continue;

      const freq = centerFreqs[b];
      if (freq < PIANO_MIN_HZ || freq > PIANO_MAX_HZ) continue;

      // Local maximum check
      const left  = data[frameOff + b - 1];
      const right = data[frameOff + b + 1];
      if (amp < left || amp < right) continue;

      // Parabolic sub-bin frequency interpolation
      const interpFreq = interpolateFreq(centerFreqs, data, frameOff, b, nMels);
      framePeaks.push({ amp, freq: interpFreq, bin: b });
    }

    // Sort by amplitude descending
    framePeaks.sort((a, b) => b.amp - a.amp);

    // Write top 16 peaks (or fewer, padding with zero-size)
    const baseIdx = t * MAX_PEAKS;
    for (let p = 0; p < MAX_PEAKS; p++) {
      const idx = baseIdx + p;

      if (p < framePeaks.length) {
        const peak = framePeaks[p];
        const ampNorm = peak.amp / 255;
        const y = freqToLog2Norm(peak.freq);
        const [r, g, b] = freqToColor(peak.freq);

        positions[idx * 3] = timeS;
        positions[idx * 3 + 1] = y;
        positions[idx * 3 + 2] = 0;

        colors[idx * 3] = r;
        colors[idx * 3 + 1] = g;
        colors[idx * 3 + 2] = b;

        sizes[idx] = ampNorm;
        ranks[idx] = p;
      } else {
        // No peak — place off-screen with zero size
        positions[idx * 3] = timeS;
        positions[idx * 3 + 1] = -1;
        positions[idx * 3 + 2] = 0;

        colors[idx * 3] = 0;
        colors[idx * 3 + 1] = 0;
        colors[idx * 3 + 2] = 0;

        sizes[idx] = 0;
        ranks[idx] = p;
      }
    }
  }

  return { positions, colors, sizes, ranks, totalPoints };
}

/* ── Note naming ─────────────────────────────────────────────────────── */

const NOTE_NAMES_FULL = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

/** Frequency → note name like "A4", "C#5" */
export function freqToNoteName(freq: number): string {
  const semitone = 12 * Math.log2(freq / 440);
  const midi = Math.round(semitone + 69);
  const name = NOTE_NAMES_FULL[((midi - 12) % 12 + 12) % 12];
  const octave = Math.floor((midi - 12) / 12);
  return `${name}${octave}`;
}

/* ── Nearest peak lookup for tooltip ─────────────────────────────────── */

export interface NearestPeakInfo {
  freq: number;
  noteName: string;
  amplitude: number;
  rank: number;
}

/* ── All peaks at a given time (for spectral tooltip) ─────────────── */

export interface PeakAtTime {
  freq: number;
  noteName: string;
  amplitude: number;
  rank: number;
  yNorm: number;        // 0-1 log2 normalized vertical position
  color: [number, number, number]; // RGB 0-1
}

/** Return all visible peaks at a given time, sorted high→low frequency */
export function findAllPeaksAtTime(
  peaks: PeakBuffers,
  time: number,
  frameRate: number,
  peakCount: 4 | 8 | 16,
): PeakAtTime[] {
  const nFrames = Math.floor(peaks.totalPoints / MAX_PEAKS);
  const frame = Math.max(0, Math.min(nFrames - 1, Math.round(time * frameRate)));

  const result: PeakAtTime[] = [];
  for (let p = 0; p < peakCount; p++) {
    const idx = frame * MAX_PEAKS + p;
    if (peaks.sizes[idx] < 0.01) continue;

    const yNorm = peaks.positions[idx * 3 + 1];
    const freq = Math.pow(2, LOG2_MIN + yNorm * LOG2_RANGE);

    result.push({
      freq,
      noteName: freqToNoteName(freq),
      amplitude: peaks.sizes[idx],
      rank: peaks.ranks[idx],
      yNorm,
      color: freqToColor(freq),
    });
  }

  result.sort((a, b) => b.freq - a.freq); // high → low
  return result;
}

/** Find the peak closest to (time, yFrac) within threshold distance */
export function findNearestPeak(
  peaks: PeakBuffers,
  time: number,
  yFrac: number,
  frameRate: number,
  peakCount: 4 | 8 | 16,
  threshold: number = 0.03,
): NearestPeakInfo | null {
  // Determine frame range to search (±2 frames around target time)
  const frame = Math.round(time * frameRate);
  const f0 = Math.max(0, frame - 2);
  const f1 = Math.min(Math.floor(peaks.totalPoints / MAX_PEAKS) - 1, frame + 2);

  let bestDist = Infinity;
  let bestIdx = -1;

  for (let f = f0; f <= f1; f++) {
    for (let p = 0; p < peakCount; p++) {
      const idx = f * MAX_PEAKS + p;
      if (peaks.sizes[idx] < 0.01) continue;

      const px = peaks.positions[idx * 3];      // time in seconds
      const py = peaks.positions[idx * 3 + 1];  // log2 normalized y (0-1)

      const dt = (px - time) / 0.1;  // normalize time diff (0.1s = 1 unit)
      const dy = (py - yFrac) / 0.05; // normalize freq diff
      const dist = dt * dt + dy * dy;

      if (dist < bestDist) {
        bestDist = dist;
        bestIdx = idx;
      }
    }
  }

  if (bestIdx < 0 || bestDist > (threshold / 0.05) * (threshold / 0.05) * 4) return null;

  const freq = Math.pow(2, LOG2_MIN + peaks.positions[bestIdx * 3 + 1] * LOG2_RANGE);
  return {
    freq,
    noteName: freqToNoteName(freq),
    amplitude: peaks.sizes[bestIdx],
    rank: peaks.ranks[bestIdx],
  };
}
