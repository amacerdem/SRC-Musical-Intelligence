/* ── MelSpectrogram — Pre-computed MI Pipeline Mel Spectrogram ────────────
 *  Renders a pre-computed mel spectrogram from the MI analysis pipeline
 *  as a 2D heatmap with log2 frequency axis, piano roll reference,
 *  note-spectrum colors, and peak amplitude markers.
 *
 *  Data: 128 mel bins × T frames @ 172.27 Hz, uint8 [0-255]
 *  Computed via: MelSpectrogram(sr=44100, n_fft=2048, hop=256, n_mels=128)
 *               → log1p → max-normalize → quantize to uint8
 *
 *  Rendering: Full spectrogram pre-rendered to offscreen canvas on data load.
 *  Each frame uses a single drawImage blit + overlay draws for grid/playhead/peaks.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState, useCallback, useMemo } from "react";

/* ── Constants ───────────────────────────────────────────────────────── */

const PIANO_MIN_HZ = 27.5;    // A0
const PIANO_MAX_HZ = 4186.01; // C8
const LOG2_MIN = Math.log2(PIANO_MIN_HZ); // ~4.78
const LOG2_MAX = Math.log2(PIANO_MAX_HZ); // ~11.87
const LOG2_RANGE = LOG2_MAX - LOG2_MIN;

const PIANO_ROLL_W = 52;        // px width of piano key strip
const SPEC_ROWS = 256;          // vertical resolution of offscreen canvas
const MAX_OFFSCREEN_W = 16000;  // safe canvas width for all browsers
const WINDOW_DURATION = 12;     // seconds visible
const PLAYHEAD_ANCHOR = 0.7;    // playhead at 70% from left
const NUM_PEAKS = 4;

/* ── MelData type (exported for Lab.tsx) ──────────────────────────────── */

export interface MelData {
  nMels: number;          // 128
  nFrames: number;        // T
  frameRate: number;      // 172.265625
  centerFreqs: Float32Array;  // 128 mel bin center frequencies (Hz)
  data: Uint8Array;       // (nFrames × nMels) frame-contiguous
}

/* ── Note-spectrum color anchors (semitone → [H, S, L]) ──────────── */
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

function hslToRgb(h: number, s: number, l: number): [number, number, number] {
  h = ((h % 360) + 360) % 360;
  s /= 100; l /= 100;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = l - c / 2;
  let r = 0, g = 0, b = 0;
  if (h < 60) { r = c; g = x; }
  else if (h < 120) { r = x; g = c; }
  else if (h < 180) { g = c; b = x; }
  else if (h < 240) { g = x; b = c; }
  else if (h < 300) { r = x; b = c; }
  else { r = c; b = x; }
  return [
    Math.round((r + m) * 255),
    Math.round((g + m) * 255),
    Math.round((b + m) * 255),
  ];
}

/** Pre-compute color LUT: [row] → [R, G, B] at full brightness */
function buildColorLUT(rows: number): Uint8Array {
  const lut = new Uint8Array(rows * 3);
  for (let row = 0; row < rows; row++) {
    const frac = 1 - row / (rows - 1);
    const log2Freq = LOG2_MIN + frac * LOG2_RANGE;
    const freq = Math.pow(2, log2Freq);
    const semitone = 12 * Math.log2(freq / 16.3516);
    const [h, s, l] = noteToHSL(semitone);
    const [r, g, b] = hslToRgb(h, s, l);
    lut[row * 3] = r;
    lut[row * 3 + 1] = g;
    lut[row * 3 + 2] = b;
  }
  return lut;
}

/* ── Display-row → mel-bin interpolation mapping ─────────────────────── */

interface RowBinMap {
  binLo: number;
  binHi: number;
  frac: number;
}

function buildRowBinMap(centerFreqs: Float32Array, nMels: number): RowBinMap[] {
  const map: RowBinMap[] = [];
  for (let row = 0; row < SPEC_ROWS; row++) {
    const yFrac = 1 - row / (SPEC_ROWS - 1); // row 0 = top = high freq
    const log2Freq = LOG2_MIN + yFrac * LOG2_RANGE;
    const freq = Math.pow(2, log2Freq);

    if (freq <= centerFreqs[0]) {
      map.push({ binLo: 0, binHi: 0, frac: 0 });
      continue;
    }
    if (freq >= centerFreqs[nMels - 1]) {
      map.push({ binLo: nMels - 1, binHi: nMels - 1, frac: 0 });
      continue;
    }

    let lo = 0, hi = 1;
    for (let i = 0; i < nMels - 1; i++) {
      if (centerFreqs[i] <= freq && centerFreqs[i + 1] >= freq) {
        lo = i; hi = i + 1; break;
      }
    }

    const t = (freq - centerFreqs[lo]) / (centerFreqs[hi] - centerFreqs[lo]);
    map.push({ binLo: lo, binHi: hi, frac: Math.max(0, Math.min(1, t)) });
  }
  return map;
}

/* ── Piano key data ──────────────────────────────────────────────────── */

interface PianoKey {
  midi: number;
  name: string;
  octave: number;
  isBlack: boolean;
  freq: number;
}

function buildPianoKeys(): PianoKey[] {
  const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const BLACK = new Set([1, 3, 6, 8, 10]);
  const keys: PianoKey[] = [];
  for (let midi = 21; midi <= 108; midi++) {
    const noteIdx = (midi - 12) % 12;
    const octave = Math.floor((midi - 12) / 12);
    const freq = 440 * Math.pow(2, (midi - 69) / 12);
    keys.push({ midi, name: NOTE_NAMES[noteIdx], octave, isBlack: BLACK.has(noteIdx), freq });
  }
  return keys;
}

const PIANO_KEYS = buildPianoKeys();

function freqToNoteName(freq: number): string {
  const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const midi = Math.round(69 + 12 * Math.log2(freq / 440));
  const noteIdx = ((midi - 12) % 12 + 12) % 12;
  const octave = Math.floor((midi - 12) / 12);
  return `${NOTE_NAMES[noteIdx]}${octave}`;
}

/* ── Component ───────────────────────────────────────────────────────── */

interface Props {
  melData: MelData | null;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  duration: number;
  accentColor: string;
  onSeek: (ratio: number) => void;
}

export function MelSpectrogram({
  melData, audioRef, isPlaying, duration, accentColor, onSeek,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const pianoCanvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [size, setSize] = useState({ w: 800, h: 400 });

  /* ── Refs ─────────────────────────────────────────── */
  const rafRef = useRef(0);
  const offscreenRef = useRef<HTMLCanvasElement | null>(null);
  const preRenderInfoRef = useRef({ skipFactor: 1, offscreenWidth: 0 });
  const scrollRef = useRef(0);
  const targetScrollRef = useRef(0);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  /* ── Color LUT (static, depends only on SPEC_ROWS) ─── */
  const colorLut = useMemo(() => buildColorLUT(SPEC_ROWS), []);

  /* ── Row → mel bin mapping (recomputed when melData changes) ─── */
  const rowBinMap = useMemo(() => {
    if (!melData) return null;
    return buildRowBinMap(melData.centerFreqs, melData.nMels);
  }, [melData]);

  /* ── ResizeObserver ────────────────────────────────── */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect;
      setSize({ w: Math.round(width), h: Math.round(height) });
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ── Sync canvas pixel size ────────────────────────── */
  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    c.width = (size.w - PIANO_ROLL_W) * dpr;
    c.height = size.h * dpr;
  }, [size, dpr]);

  useEffect(() => {
    const c = pianoCanvasRef.current;
    if (!c) return;
    c.width = PIANO_ROLL_W * dpr;
    c.height = size.h * dpr;
  }, [size, dpr]);

  /* ── Pre-render full spectrogram to offscreen canvas ─── */
  useEffect(() => {
    if (!melData || !rowBinMap) {
      offscreenRef.current = null;
      return;
    }

    const { nFrames, nMels, data } = melData;
    const skipFactor = Math.max(1, Math.ceil(nFrames / MAX_OFFSCREEN_W));
    const offscreenWidth = Math.ceil(nFrames / skipFactor);

    const osc = document.createElement("canvas");
    osc.width = offscreenWidth;
    osc.height = SPEC_ROWS;
    const octx = osc.getContext("2d")!;

    const imgData = new ImageData(offscreenWidth, SPEC_ROWS);
    const px = imgData.data;

    for (let col = 0; col < offscreenWidth; col++) {
      const frame = Math.min(col * skipFactor, nFrames - 1);
      const frameOff = frame * nMels;

      for (let row = 0; row < SPEC_ROWS; row++) {
        const { binLo, binHi, frac } = rowBinMap[row];
        const ampLo = data[frameOff + binLo] / 255;
        const ampHi = data[frameOff + binHi] / 255;
        const amp = ampLo + frac * (ampHi - ampLo);

        const bright = Math.pow(amp, 0.65);
        const pixelIdx = (row * offscreenWidth + col) * 4;
        px[pixelIdx]     = Math.round(colorLut[row * 3]     * bright);
        px[pixelIdx + 1] = Math.round(colorLut[row * 3 + 1] * bright);
        px[pixelIdx + 2] = Math.round(colorLut[row * 3 + 2] * bright);
        px[pixelIdx + 3] = amp > 0.008 ? Math.round(40 + 215 * bright) : 0;
      }
    }

    octx.putImageData(imgData, 0, 0);
    offscreenRef.current = osc;
    preRenderInfoRef.current = { skipFactor, offscreenWidth };

    // Reset scroll to beginning
    scrollRef.current = 0;
    targetScrollRef.current = 0;
  }, [melData, rowBinMap, colorLut]);

  /* ── Draw piano roll (static, only on size change) ─── */
  const drawPiano = useCallback(() => {
    const canvas = pianoCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const W = PIANO_ROLL_W;
    const H = size.h;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    ctx.fillStyle = "rgba(6,6,14,0.95)";
    ctx.fillRect(0, 0, W, H);

    const freqToY = (hz: number) => {
      const frac = (Math.log2(hz) - LOG2_MIN) / LOG2_RANGE;
      return H * (1 - frac);
    };

    // White keys
    for (const key of PIANO_KEYS) {
      if (key.isBlack) continue;
      const nextSemitone = key.freq * Math.pow(2, 1 / 12);
      const prevSemitone = key.freq / Math.pow(2, 1 / 12);
      const y1 = freqToY(Math.min(nextSemitone, PIANO_MAX_HZ));
      const y2 = freqToY(Math.max(prevSemitone, PIANO_MIN_HZ));
      const kh = Math.max(1, y2 - y1);

      ctx.fillStyle = "rgba(200,200,210,0.85)";
      ctx.fillRect(0, y1, W - 1, kh);
      ctx.strokeStyle = "rgba(0,0,0,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, W - 1, kh);

      if (key.name === "C") {
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.font = "bold 8px 'JetBrains Mono', monospace";
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(`C${key.octave}`, 3, y1 + kh / 2);
      }
    }

    // Black keys
    for (const key of PIANO_KEYS) {
      if (!key.isBlack) continue;
      const halfSemitone = Math.pow(2, 0.5 / 12);
      const y1 = freqToY(key.freq * halfSemitone);
      const y2 = freqToY(key.freq / halfSemitone);
      const kh = Math.max(1, y2 - y1);
      const kw = W * 0.6;

      ctx.fillStyle = "rgba(20,20,30,0.95)";
      ctx.fillRect(0, y1, kw, kh);
      ctx.strokeStyle = "rgba(80,80,100,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, kw, kh);
    }

    // Right border
    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(W - 0.5, 0);
    ctx.lineTo(W - 0.5, H);
    ctx.stroke();
  }, [size, dpr]);

  useEffect(() => { drawPiano(); }, [drawPiano]);

  /* ── Main draw loop ────────────────────────────────── */
  useEffect(() => {
    if (!melData) return;

    let running = true;
    const melDuration = melData.nFrames / melData.frameRate;

    const loop = () => {
      if (!running) return;
      const audio = audioRef.current;
      const ct = audio?.currentTime ?? 0;

      /* ── Auto-scroll when playing ───────────────── */
      if (isPlaying && audio && !isNaN(audio.duration)) {
        const target = Math.max(0, ct - WINDOW_DURATION * PLAYHEAD_ANCHOR);
        const maxS = Math.max(0, melDuration - WINDOW_DURATION);
        targetScrollRef.current = Math.min(maxS, target);
      }
      scrollRef.current += (targetScrollRef.current - scrollRef.current) * 0.12;

      /* ── Render to visible canvas ───────────────── */
      const canvas = canvasRef.current;
      const osc = offscreenRef.current;
      if (!canvas || !osc) { rafRef.current = requestAnimationFrame(loop); return; }
      const ctx = canvas.getContext("2d");
      if (!ctx) { rafRef.current = requestAnimationFrame(loop); return; }

      const W = size.w - PIANO_ROLL_W;
      const H = size.h;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.clearRect(0, 0, W, H);

      const sT = scrollRef.current;
      const { skipFactor, offscreenWidth } = preRenderInfoRef.current;

      /* ── Blit pre-rendered offscreen → visible canvas ── */
      const startCol = Math.max(0, Math.floor(sT * melData.frameRate / skipFactor));
      const windowCols = Math.ceil(WINDOW_DURATION * melData.frameRate / skipFactor);
      const endCol = Math.min(offscreenWidth, startCol + windowCols);
      const actualCols = endCol - startCol;

      if (actualCols > 0) {
        ctx.imageSmoothingEnabled = true;
        ctx.drawImage(osc, startCol, 0, actualCols, SPEC_ROWS, 0, 0, W, H);
      }

      /* ── Grid overlays ─────────────────────────── */
      // Octave lines
      ctx.strokeStyle = "rgba(255,255,255,0.06)";
      ctx.lineWidth = 0.5;
      for (let oct = 1; oct <= 8; oct++) {
        const freq = 16.3516 * Math.pow(2, oct);
        if (freq < PIANO_MIN_HZ || freq > PIANO_MAX_HZ) continue;
        const frac = (Math.log2(freq) - LOG2_MIN) / LOG2_RANGE;
        const y = H * (1 - frac);
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(W, y);
        ctx.stroke();
      }

      // Time markers
      const tStep = WINDOW_DURATION <= 6 ? 1 : WINDOW_DURATION <= 12 ? 2 : 4;
      const tStart = Math.ceil(sT / tStep) * tStep;
      ctx.font = "8px monospace";
      ctx.textAlign = "center";
      for (let t = tStart; t <= sT + WINDOW_DURATION + 0.01; t += tStep) {
        const x = ((t - sT) / WINDOW_DURATION) * W;
        if (x < -5 || x > W + 5) continue;
        ctx.strokeStyle = "rgba(255,255,255,0.04)";
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, H);
        ctx.stroke();
        const m = Math.floor(t / 60), s = Math.floor(t % 60);
        ctx.fillStyle = "rgba(255,255,255,0.15)";
        ctx.fillText(`${m}:${s.toString().padStart(2, "0")}`, x, H - 4);
      }

      /* ── Playhead ──────────────────────────────── */
      const phX = ((ct - sT) / WINDOW_DURATION) * W;
      if (phX >= -10 && phX <= W + 10) {
        // Glow
        const gw = 16;
        const pg = ctx.createLinearGradient(phX - gw, 0, phX + gw, 0);
        pg.addColorStop(0, "transparent");
        pg.addColorStop(0.5, accentColor + "18");
        pg.addColorStop(1, "transparent");
        ctx.fillStyle = pg;
        ctx.fillRect(phX - gw, 0, gw * 2, H);

        // Line
        ctx.beginPath();
        ctx.moveTo(phX, 0);
        ctx.lineTo(phX, H);
        ctx.strokeStyle = accentColor;
        ctx.lineWidth = 1.5;
        ctx.globalAlpha = 0.9;
        ctx.stroke();
        ctx.globalAlpha = 1;

        // Top triangle
        ctx.beginPath();
        ctx.moveTo(phX - 4, 0);
        ctx.lineTo(phX + 4, 0);
        ctx.lineTo(phX, 6);
        ctx.closePath();
        ctx.fillStyle = accentColor;
        ctx.fill();

        /* ── Peak markers from mel data ────────── */
        const currentFrame = Math.max(0, Math.min(melData.nFrames - 1,
          Math.floor(ct * melData.frameRate)));
        const frameOff = currentFrame * melData.nMels;

        const peaks: { amp: number; freq: number }[] = [];
        for (let b = 0; b < melData.nMels; b++) {
          const amp = melData.data[frameOff + b];
          const freq = melData.centerFreqs[b];
          if (amp > 20 && freq >= PIANO_MIN_HZ && freq <= PIANO_MAX_HZ) {
            peaks.push({ amp, freq });
          }
        }
        peaks.sort((a, b) => b.amp - a.amp);

        const topPeaks = peaks.slice(0, NUM_PEAKS);
        for (let pi = 0; pi < topPeaks.length; pi++) {
          const peak = topPeaks[pi];
          const frac = (Math.log2(peak.freq) - LOG2_MIN) / LOG2_RANGE;
          const y = H * (1 - frac);

          // Glow
          const grad = ctx.createRadialGradient(phX, y, 0, phX, y, 8);
          grad.addColorStop(0, "rgba(255,255,255,0.9)");
          grad.addColorStop(0.4, "rgba(255,255,255,0.3)");
          grad.addColorStop(1, "transparent");
          ctx.fillStyle = grad;
          ctx.fillRect(phX - 8, y - 8, 16, 16);

          // Dot
          ctx.beginPath();
          ctx.arc(phX, y, 3, 0, Math.PI * 2);
          ctx.fillStyle = "white";
          ctx.fill();
          ctx.strokeStyle = "rgba(0,0,0,0.5)";
          ctx.lineWidth = 0.8;
          ctx.stroke();

          // Label
          const freqStr = peak.freq >= 1000
            ? `${(peak.freq / 1000).toFixed(1)}k`
            : `${Math.round(peak.freq)}`;
          const noteStr = freqToNoteName(peak.freq);
          ctx.font = "bold 9px 'JetBrains Mono', monospace";
          ctx.textAlign = "left";
          ctx.fillStyle = "rgba(255,255,255,0.85)";
          const labelX = phX + 8;
          const labelY = y + (pi % 2 === 0 ? -3 : 10);
          ctx.fillText(`${noteStr} ${freqStr}Hz`, labelX, labelY);
        }
      }

      rafRef.current = requestAnimationFrame(loop);
    };

    rafRef.current = requestAnimationFrame(loop);
    return () => { running = false; cancelAnimationFrame(rafRef.current); };
  }, [melData, audioRef, isPlaying, duration, size, dpr, accentColor]);

  /* ── Click to seek ──────────────────────────────────── */
  const handleClick = useCallback((e: React.MouseEvent<HTMLCanvasElement>) => {
    const c = canvasRef.current;
    if (!c) return;
    const rect = c.getBoundingClientRect();
    const W = size.w - PIANO_ROLL_W;
    const cx = ((e.clientX - rect.left) / rect.width) * W;
    const t = scrollRef.current + (cx / W) * WINDOW_DURATION;
    onSeek(Math.max(0, Math.min(1, t / duration)));
  }, [size, duration, onSeek]);

  /* ── Wheel scroll ───────────────────────────────────── */
  const handleWheel = useCallback((e: React.WheelEvent<HTMLCanvasElement>) => {
    e.stopPropagation();
    const maxS = Math.max(0, duration - WINDOW_DURATION);
    const delta = (e.deltaX || e.deltaY) * 0.04;
    targetScrollRef.current = Math.max(0, Math.min(maxS, targetScrollRef.current + delta));
  }, [duration]);

  return (
    <div ref={containerRef} className="relative w-full h-full flex">
      <canvas
        ref={pianoCanvasRef}
        style={{ width: PIANO_ROLL_W, height: "100%", flexShrink: 0 }}
      />
      <canvas
        ref={canvasRef}
        style={{ flex: 1, height: "100%", cursor: "pointer" }}
        onClick={handleClick}
        onWheel={handleWheel}
      />
      {!melData && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-600 animate-pulse">
            Loading MI spectrogram...
          </span>
        </div>
      )}
    </div>
  );
}
