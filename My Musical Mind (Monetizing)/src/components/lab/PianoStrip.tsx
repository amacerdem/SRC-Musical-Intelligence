/* ── PianoStrip — Left-side piano roll + spectrum color bar ───────────
 *  Extracted from SpectralPeaks.tsx. Static Canvas 2D rendering of
 *  piano keys (44px) + note-spectrum gradient bar (10px) = 54px total.
 *  Only redraws when container height changes.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState } from "react";
import { freqToColor } from "./peakExtractor";
import { LEFT_STRIP_W } from "./useViewport";

/* ── Constants ───────────────────────────────────────────────────────── */

const PIANO_MIN_HZ = 27.5;     // A0
const PIANO_MAX_HZ = 4186.01;  // C8
const LOG2_MIN = Math.log2(PIANO_MIN_HZ);
const LOG2_MAX = Math.log2(PIANO_MAX_HZ);
const LOG2_RANGE = LOG2_MAX - LOG2_MIN;

const PIANO_KEYS_W = 44;
const SPECTRUM_BAR_W = 10;

/* ── Piano key data ─────────────────────────────────────────────────── */

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

/* ── Component ──────────────────────────────────────────────────────── */

export function PianoStrip() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [height, setHeight] = useState(400);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  /* ── ResizeObserver ─────────────────────────────── */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      setHeight(Math.round(entries[0].contentRect.height));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ── Draw ────────────────────────────────────────── */
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const H = height;
    canvas.width = LEFT_STRIP_W * dpr;
    canvas.height = H * dpr;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, LEFT_STRIP_W, H);

    ctx.fillStyle = "rgba(6,6,14,0.95)";
    ctx.fillRect(0, 0, LEFT_STRIP_W, H);

    const freqToY = (hz: number) => {
      const frac = (Math.log2(hz) - LOG2_MIN) / LOG2_RANGE;
      return H * (1 - frac);
    };

    // ── White keys ──────────────────────────
    for (const key of PIANO_KEYS) {
      if (key.isBlack) continue;
      const nextSemitone = key.freq * Math.pow(2, 1 / 12);
      const prevSemitone = key.freq / Math.pow(2, 1 / 12);
      const y1 = freqToY(Math.min(nextSemitone, PIANO_MAX_HZ));
      const y2 = freqToY(Math.max(prevSemitone, PIANO_MIN_HZ));
      const kh = Math.max(1, y2 - y1);

      ctx.fillStyle = "rgba(200,200,210,0.85)";
      ctx.fillRect(0, y1, PIANO_KEYS_W - 1, kh);
      ctx.strokeStyle = "rgba(0,0,0,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, PIANO_KEYS_W - 1, kh);

      if (key.name === "C") {
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.font = "bold 7px 'JetBrains Mono', monospace";
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(`C${key.octave}`, 2, y1 + kh / 2);
      }
    }

    // ── Black keys ──────────────────────────
    for (const key of PIANO_KEYS) {
      if (!key.isBlack) continue;
      const halfSemitone = Math.pow(2, 0.5 / 12);
      const y1 = freqToY(key.freq * halfSemitone);
      const y2 = freqToY(key.freq / halfSemitone);
      const kh = Math.max(1, y2 - y1);
      const kw = PIANO_KEYS_W * 0.6;

      ctx.fillStyle = "rgba(20,20,30,0.95)";
      ctx.fillRect(0, y1, kw, kh);
      ctx.strokeStyle = "rgba(80,80,100,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, kw, kh);
    }

    // ── Note-spectrum color bar ─────────────
    const barX = PIANO_KEYS_W;
    for (let py = 0; py < H; py++) {
      const frac = 1 - py / (H - 1);
      const log2Freq = LOG2_MIN + frac * LOG2_RANGE;
      const freq = Math.pow(2, log2Freq);
      const [r, g, b] = freqToColor(freq);
      ctx.fillStyle = `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`;
      ctx.fillRect(barX, py, SPECTRUM_BAR_W, 1);
    }

    // ── Separators ──────────────────────────
    ctx.strokeStyle = "rgba(0,0,0,0.4)";
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.moveTo(barX, 0);
    ctx.lineTo(barX, H);
    ctx.stroke();

    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(LEFT_STRIP_W - 0.5, 0);
    ctx.lineTo(LEFT_STRIP_W - 0.5, H);
    ctx.stroke();
  }, [height, dpr]);

  return (
    <div ref={containerRef} className="h-full flex-shrink-0" style={{ width: LEFT_STRIP_W }}>
      <canvas
        ref={canvasRef}
        style={{ width: LEFT_STRIP_W, height: "100%" }}
      />
    </div>
  );
}
