/* ── WaveformNavigator — Full-piece minimap with viewport indicator ────
 *  Canvas 2D, 48px height. Shows the entire piece waveform with a
 *  draggable/clickable viewport rectangle indicating the currently
 *  visible region in the LayeredScope above.
 *
 *  Features:
 *  - Min/max per-pixel waveform rendering
 *  - Viewport rectangle (scroll..scroll+window)
 *  - Click-to-jump, drag-to-pan
 *  - Playhead indicator
 *  - 60fps cursor sync via rAF
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState, useCallback } from "react";
import type { ViewportState } from "./useViewport";

/* ── Constants ───────────────────────────────────────────────────────── */

const NAV_HEIGHT = 48;
const FRAME_RATE = 172.27;

/* ── Types ───────────────────────────────────────────────────────────── */

interface Props {
  audioRef: React.RefObject<HTMLAudioElement | null>;
  duration: number;
  viewport: ViewportState;
  accentColor: string;
  samples?: Float32Array | null;
}

/* ── Component ──────────────────────────────────────────────────────── */

export function WaveformNavigator({
  audioRef, duration, viewport, accentColor, samples,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [width, setWidth] = useState(800);
  const drawRef = useRef<() => void>(() => {});
  const rafRef = useRef(0);
  const draggingRef = useRef(false);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  /* ── ResizeObserver ─────────────────────────────── */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      setWidth(Math.round(entries[0].contentRect.width));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ── Sync canvas pixel size ────────────────────── */
  useEffect(() => {
    const c = canvasRef.current;
    if (!c) return;
    c.width = width * dpr;
    c.height = NAV_HEIGHT * dpr;
  }, [width, dpr]);

  /* ── Draw function ─────────────────────────────── */
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas || duration <= 0) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = width;
    const H = NAV_HEIGHT;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);

    // Background
    ctx.fillStyle = "rgba(6,6,14,0.90)";
    ctx.fillRect(0, 0, W, H);

    // ── Waveform ────────────────────────────────
    if (samples && samples.length > 0) {
      const samplesPerPixel = Math.max(1, Math.floor(samples.length / W));
      ctx.fillStyle = "rgba(255,255,255,0.20)";

      for (let px = 0; px < W; px++) {
        const start = Math.floor((px / W) * samples.length);
        const end = Math.min(samples.length, start + samplesPerPixel);
        let min = 0, max = 0;
        for (let i = start; i < end; i++) {
          const s = samples[i];
          if (s < min) min = s;
          if (s > max) max = s;
        }
        const mid = H / 2;
        const top = mid + min * (H / 2 - 2);
        const bot = mid + max * (H / 2 - 2);
        ctx.fillRect(px, top, 1, Math.max(1, bot - top));
      }
    } else {
      // No samples: draw placeholder
      ctx.fillStyle = "rgba(255,255,255,0.05)";
      ctx.fillRect(0, H / 2 - 1, W, 2);
    }

    // ── Viewport rectangle ──────────────────────
    const scroll = viewport.scrollRef.current;
    const window_ = viewport.windowRef.current;
    const vpX = (scroll / duration) * W;
    const vpW = Math.max(4, (window_ / duration) * W);

    // Dimmed regions outside viewport
    ctx.fillStyle = "rgba(0,0,0,0.4)";
    ctx.fillRect(0, 0, vpX, H);
    ctx.fillRect(vpX + vpW, 0, W - vpX - vpW, H);

    // Viewport border
    ctx.strokeStyle = accentColor + "80";
    ctx.lineWidth = 1.5;
    ctx.strokeRect(vpX + 0.5, 0.5, vpW - 1, H - 1);

    // Viewport fill
    ctx.fillStyle = accentColor + "08";
    ctx.fillRect(vpX, 0, vpW, H);

    // ── Playhead ────────────────────────────────
    const ct = audioRef.current?.currentTime ?? 0;
    if (ct >= 0 && ct <= duration) {
      const px = (ct / duration) * W;
      ctx.beginPath();
      ctx.moveTo(px, 0);
      ctx.lineTo(px, H);
      ctx.strokeStyle = accentColor;
      ctx.lineWidth = 1.5;
      ctx.globalAlpha = 0.9;
      ctx.stroke();
      ctx.globalAlpha = 1;

      // Playhead dot
      ctx.beginPath();
      ctx.arc(px, 3, 2.5, 0, Math.PI * 2);
      ctx.fillStyle = accentColor;
      ctx.fill();
    }

    // ── Top border ──────────────────────────────
    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, 0.5);
    ctx.lineTo(W, 0.5);
    ctx.stroke();
  }, [width, dpr, duration, samples, accentColor, viewport, audioRef]);

  drawRef.current = draw;

  /* ── rAF loop for cursor sync ──────────────────── */
  useEffect(() => {
    let running = true;
    const loop = () => {
      if (!running) return;
      drawRef.current();
      rafRef.current = requestAnimationFrame(loop);
    };
    rafRef.current = requestAnimationFrame(loop);
    return () => { running = false; cancelAnimationFrame(rafRef.current); };
  }, []);

  /* ── Mouse handlers ────────────────────────────── */
  const getTimeFrac = useCallback((e: React.MouseEvent) => {
    const rect = containerRef.current?.getBoundingClientRect();
    if (!rect) return 0;
    return Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  }, []);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    draggingRef.current = true;
    const frac = getTimeFrac(e);
    viewport.handleNavigatorSeek(frac);
  }, [getTimeFrac, viewport]);

  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    if (!draggingRef.current) return;
    const frac = getTimeFrac(e);
    viewport.handleNavigatorDrag(frac - (viewport.windowRef.current / duration) / 2);
  }, [getTimeFrac, viewport, duration]);

  const handleMouseUp = useCallback(() => {
    draggingRef.current = false;
  }, []);

  const handleMouseLeave = useCallback(() => {
    draggingRef.current = false;
  }, []);

  return (
    <div
      ref={containerRef}
      className="w-full cursor-pointer select-none"
      style={{ height: NAV_HEIGHT }}
      onMouseDown={handleMouseDown}
      onMouseMove={handleMouseMove}
      onMouseUp={handleMouseUp}
      onMouseLeave={handleMouseLeave}
    >
      <canvas
        ref={canvasRef}
        className="block w-full"
        style={{ height: NAV_HEIGHT }}
      />
    </div>
  );
}
