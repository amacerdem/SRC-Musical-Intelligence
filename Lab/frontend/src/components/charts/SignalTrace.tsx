import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';
import { FRAME_RATE } from '../../design/tokens';

interface Signal {
  name: string;
  color: string;
  /** Index into the flat Float32Array (column in T × N matrix) */
  featureIndex: number;
}

interface Props {
  /** Flat Float32Array of shape (T × N_features) */
  data: Float32Array | null;
  /** Total number of features (columns) */
  nFeatures: number;
  /** Total number of frames (rows) */
  nFrames: number;
  /** Which signals to draw */
  signals: Signal[];
  /** Canvas height */
  height?: number;
  /** Y range [min, max]. Default [0, 1] */
  yRange?: [number, number];
  /** Show Y grid lines */
  showGrid?: boolean;
  /** Label on hover */
  showLabel?: boolean;
}

/**
 * High-performance Canvas-based multi-signal time series renderer.
 * Optimized for 26K+ frames at 97 features.
 *
 * Data layout: Row-major (T × N), so feature j at frame t = data[t * nFeatures + j]
 */
export default function SignalTrace({
  data,
  nFeatures,
  nFrames,
  signals,
  height = 100,
  yRange = [0, 1],
  showGrid = true,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const dpr = window.devicePixelRatio || 1;
    const w = container.clientWidth;
    const h = height;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.scale(dpr, dpr);
    ctx.clearRect(0, 0, w, h);

    if (!data || nFrames === 0 || signals.length === 0) {
      ctx.fillStyle = 'rgba(255,255,255,0.03)';
      ctx.fillRect(0, 0, w, h);
      return;
    }

    const [yMin, yMax] = yRange;
    const ySpan = yMax - yMin || 1;
    const pad = { top: 4, bottom: 4 };
    const plotH = h - pad.top - pad.bottom;

    // Grid lines
    if (showGrid) {
      ctx.strokeStyle = 'rgba(255,255,255,0.04)';
      ctx.lineWidth = 0.5;
      for (let v = 0; v <= 1; v += 0.25) {
        const y = pad.top + (1 - (v - yMin) / ySpan) * plotH;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(w, y);
        ctx.stroke();
      }
    }

    // Draw each signal
    const framesPerPixel = nFrames / w;

    for (const signal of signals) {
      ctx.strokeStyle = signal.color;
      ctx.lineWidth = signals.length > 4 ? 0.8 : 1.2;
      ctx.globalAlpha = signals.length > 8 ? 0.6 : 0.85;
      ctx.beginPath();

      let first = true;
      for (let px = 0; px < w; px++) {
        const frameStart = Math.floor(px * framesPerPixel);
        const frameEnd = Math.min(Math.floor((px + 1) * framesPerPixel), nFrames);

        // For downsampling: take mean or peak within pixel range
        let sum = 0;
        let count = 0;
        for (let f = frameStart; f < frameEnd; f++) {
          sum += data[f * nFeatures + signal.featureIndex];
          count++;
        }
        const val = count > 0 ? sum / count : 0;
        const y = pad.top + (1 - (val - yMin) / ySpan) * plotH;

        if (first) {
          ctx.moveTo(px, y);
          first = false;
        } else {
          ctx.lineTo(px, y);
        }
      }
      ctx.stroke();
    }
    ctx.globalAlpha = 1;

    // Cursor line
    const { currentTime, duration } = useAudioStore.getState();
    if (duration > 0) {
      const cursorX = (currentTime / duration) * w;
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.7)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cursorX, 0);
      ctx.lineTo(cursorX, h);
      ctx.stroke();

      // Draw value dots at cursor
      const cursorFrame = Math.floor(currentTime * FRAME_RATE);
      if (cursorFrame >= 0 && cursorFrame < nFrames) {
        for (const signal of signals) {
          const val = data[cursorFrame * nFeatures + signal.featureIndex];
          const y = pad.top + (1 - (val - yMin) / ySpan) * plotH;
          ctx.fillStyle = signal.color;
          ctx.beginPath();
          ctx.arc(cursorX, y, 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }
  }, [data, nFeatures, nFrames, signals, height, yRange, showGrid]);

  // Animation loop
  useEffect(() => {
    let raf: number;
    const loop = () => {
      draw();
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [draw]);

  // Resize
  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;
    const observer = new ResizeObserver(() => draw());
    observer.observe(container);
    return () => observer.disconnect();
  }, [draw]);

  // Click to seek
  const handleClick = (e: React.MouseEvent) => {
    const { duration } = useAudioStore.getState();
    if (duration <= 0) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const fraction = (e.clientX - rect.left) / rect.width;
    useAudioStore.getState().setCurrentTime(fraction * duration);
  };

  return (
    <div ref={containerRef} className="w-full cursor-crosshair" style={{ height }} onClick={handleClick}>
      <canvas ref={canvasRef} />
    </div>
  );
}
