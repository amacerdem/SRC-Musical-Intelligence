import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';
import { colors } from '../../design/tokens';

interface Props {
  height?: number;
}

/**
 * Canvas-rendered waveform with real-time cursor overlay.
 * Reads the downsampled envelope from audioStore.
 */
export default function Waveform({ height = 80 }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const { waveformEnvelope, currentTime, duration, isPlaying } = useAudioStore.getState();
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

    // Background
    ctx.clearRect(0, 0, w, h);

    if (!waveformEnvelope || waveformEnvelope.length === 0) {
      ctx.fillStyle = 'rgba(255,255,255,0.05)';
      ctx.fillRect(0, 0, w, h);
      ctx.fillStyle = 'rgba(255,255,255,0.2)';
      ctx.font = '11px Inter';
      ctx.textAlign = 'center';
      ctx.fillText('No waveform loaded', w / 2, h / 2 + 4);
      return;
    }

    const data = waveformEnvelope;
    const mid = h / 2;
    const samplesPerPixel = data.length / w;

    // Draw waveform
    ctx.fillStyle = colors.r3 + '40'; // 25% opacity
    ctx.strokeStyle = colors.r3 + '80';
    ctx.lineWidth = 0.5;

    ctx.beginPath();
    ctx.moveTo(0, mid);
    for (let x = 0; x < w; x++) {
      const i = Math.floor(x * samplesPerPixel);
      if (i < data.length) {
        const v = data[i] * mid * 0.9;
        ctx.lineTo(x, mid - v);
      }
    }
    for (let x = w - 1; x >= 0; x--) {
      const i = Math.min(Math.floor(x * samplesPerPixel) + 1, data.length - 1);
      if (i < data.length) {
        const v = data[i] * mid * 0.9;
        ctx.lineTo(x, mid - v);
      }
    }
    ctx.closePath();
    ctx.fill();
    ctx.stroke();

    // Center line
    ctx.strokeStyle = 'rgba(255,255,255,0.06)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(0, mid);
    ctx.lineTo(w, mid);
    ctx.stroke();

    // Cursor
    if (duration > 0) {
      const cursorX = (currentTime / duration) * w;
      ctx.strokeStyle = '#ffffff';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(cursorX, 0);
      ctx.lineTo(cursorX, h);
      ctx.stroke();

      // Played region tint
      ctx.fillStyle = 'rgba(59, 130, 246, 0.08)';
      ctx.fillRect(0, 0, cursorX, h);
    }
  }, [height]);

  // Redraw on animation frame when playing
  useEffect(() => {
    let raf: number;
    const loop = () => {
      draw();
      raf = requestAnimationFrame(loop);
    };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [draw]);

  // Resize observer
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
