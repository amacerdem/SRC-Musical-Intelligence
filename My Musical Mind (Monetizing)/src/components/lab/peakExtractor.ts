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

/* ── Note-spectrum color anchors (semitone → [H, S, L]) ────────── */

const NOTE_ANCHORS: [number, [number, number, number]][] = [
  [0,  [0,   100, 50]],  // C  = red
  [2,  [30,  100, 50]],  // D  = orange
  [4,  [54,  100, 50]],  // E  = yellow
  [5,  [140, 100, 42]],  // F  = green
  [7,  [180, 100, 42]],  // G  = cyan
  [9,  [225, 100, 55]],  // A  = blue
  [11, [270, 100, 50]],  // B  = purple
];

function noteToHSL(semitone: number): [number, number, number] {
  const s = ((semitone % 12) + 12) % 12;
  let lo = NOTE_ANCHORS[NOTE_ANCHORS.length - 1];
  let hi = NOTE_ANCHORS[0];
  for (let i = 0; i < NOTE_ANCHORS.length - 1; i++) {
    if (s >= NOTE_ANCHORS[i][0] && s < NOTE_ANCHORS[i + 1][0]) {
      lo = NOTE_ANCHORS[i];
      hi = NOTE_ANCHORS[i + 1];
      break;
    }
  }
  if (s >= NOTE_ANCHORS[NOTE_ANCHORS.length - 1][0]) {
    lo = NOTE_ANCHORS[NOTE_ANCHORS.length - 1];
    hi = NOTE_ANCHORS[0];
    const range = 12 - lo[0] + hi[0];
    const t = (s - lo[0]) / range;
    return [
      lo[1][0] + t * (hi[1][0] + 360 - lo[1][0]),
      lo[1][1] + t * (hi[1][1] - lo[1][1]),
      lo[1][2] + t * (hi[1][2] - lo[1][2]),
    ];
  }
  const range = hi[0] - lo[0];
  const t = range > 0 ? (s - lo[0]) / range : 0;
  return [
    lo[1][0] + t * (hi[1][0] - lo[1][0]),
    lo[1][1] + t * (hi[1][1] - lo[1][1]),
    lo[1][2] + t * (hi[1][2] - lo[1][2]),
  ];
}

function hslToRgb01(h: number, s: number, l: number): [number, number, number] {
  h = ((h % 360) + 360) % 360;
  s /= 100; l /= 100;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;
  let r = 0, g = 0, b = 0;
  if (h < 60)       { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else              { r = c; b = x; }
  return [r + m, g + m, b + m]; // 0-1 range for GPU
}

/** Frequency → note-spectrum RGB in [0,1] range, full saturation.
 *  Amplitude/brightness is handled by the shader (alpha + point size),
 *  so colors stay vivid and distinguishable at all amplitudes. */
export function freqToColor(freq: number): [number, number, number] {
  const semitone = 12 * Math.log2(freq / 16.3516);
  const [h, s, l] = noteToHSL(semitone);
  return hslToRgb01(h, s, l);
}

/** Frequency → normalized log2 position (0 = A0 bottom, 1 = C8 top) */
function freqToLog2Norm(freq: number): number {
  return (Math.log2(freq) - LOG2_MIN) / LOG2_RANGE;
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

    // Collect peaks above threshold within piano range
    framePeaks.length = 0;
    for (let b = 0; b < nMels; b++) {
      const amp = data[frameOff + b];
      const freq = centerFreqs[b];
      if (amp > AMP_THRESHOLD && freq >= PIANO_MIN_HZ && freq <= PIANO_MAX_HZ) {
        framePeaks.push({ amp, freq, bin: b });
      }
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
