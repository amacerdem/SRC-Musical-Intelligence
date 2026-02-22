import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';

interface Props {
  height?: number;
}

// Viridis-inspired colormap (simplified 8-stop)
const COLORMAP = [
  [68, 1, 84],
  [72, 36, 117],
  [65, 68, 135],
  [53, 95, 141],
  [42, 120, 142],
  [33, 145, 140],
  [94, 201, 98],
  [253, 231, 37],
];

function colormapLookup(t: number): [number, number, number] {
  const clamped = Math.max(0, Math.min(1, t));
  const idx = clamped * (COLORMAP.length - 1);
  const lo = Math.floor(idx);
  const hi = Math.min(lo + 1, COLORMAP.length - 1);
  const frac = idx - lo;
  return [
    Math.round(COLORMAP[lo][0] + (COLORMAP[hi][0] - COLORMAP[lo][0]) * frac),
    Math.round(COLORMAP[lo][1] + (COLORMAP[hi][1] - COLORMAP[lo][1]) * frac),
    Math.round(COLORMAP[lo][2] + (COLORMAP[hi][2] - COLORMAP[lo][2]) * frac),
  ];
}

/**
 * Canvas-rendered mel spectrogram with cursor overlay.
 */
export default function Spectrogram({ height = 120 }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const imageDataRef = useRef<ImageData | null>(null);

  // Pre-render spectrogram image when data changes
  const renderImage = useCallback(() => {
    const { spectrogramData, spectrogramMels, spectrogramFrames } = useAudioStore.getState();
    if (!spectrogramData || spectrogramFrames === 0) {
      imageDataRef.current = null;
      return;
    }

    const nMels = spectrogramMels;
    const nFrames = spectrogramFrames;
    const imgData = new ImageData(nFrames, nMels);

    // Find min/max for normalization
    let min = Infinity, max = -Infinity;
    for (let i = 0; i < spectrogramData.length; i++) {
      if (spectrogramData[i] < min) min = spectrogramData[i];
      if (spectrogramData[i] > max) max = spectrogramData[i];
    }
    const range = max - min || 1;

    // Fill pixels (mel 0 = bottom, so we flip y)
    for (let m = 0; m < nMels; m++) {
      for (let f = 0; f < nFrames; f++) {
        const val = (spectrogramData[m * nFrames + f] - min) / range;
        const [r, g, b] = colormapLookup(val);
        const y = nMels - 1 - m; // flip
        const idx = (y * nFrames + f) * 4;
        imgData.data[idx] = r;
        imgData.data[idx + 1] = g;
        imgData.data[idx + 2] = b;
        imgData.data[idx + 3] = 255;
      }
    }
    imageDataRef.current = imgData;
  }, []);

  // Watch for data changes
  useEffect(() => {
    const unsub = useAudioStore.subscribe(
      (state) => state.spectrogramData,
      () => renderImage(),
      // @ts-ignore zustand subscribe selector
    );
    renderImage();
    // Simple fallback if subscribe with selector not available
    return typeof unsub === 'function' ? unsub : undefined;
  }, [renderImage]);

  // Draw loop
  useEffect(() => {
    let raf: number;
    const draw = () => {
      const canvas = canvasRef.current;
      const container = containerRef.current;
      if (!canvas || !container) { raf = requestAnimationFrame(draw); return; }

      const dpr = window.devicePixelRatio || 1;
      const w = container.clientWidth;
      const h = height;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;

      const ctx = canvas.getContext('2d');
      if (!ctx) { raf = requestAnimationFrame(draw); return; }
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const imgData = imageDataRef.current;
      if (!imgData) {
        ctx.fillStyle = 'rgba(255,255,255,0.03)';
        ctx.fillRect(0, 0, w, h);
        ctx.fillStyle = 'rgba(255,255,255,0.15)';
        ctx.font = '11px Inter';
        ctx.textAlign = 'center';
        ctx.fillText('No spectrogram loaded', w / 2, h / 2 + 4);
        raf = requestAnimationFrame(draw);
        return;
      }

      // Draw spectrogram to offscreen canvas then scale
      const offscreen = new OffscreenCanvas(imgData.width, imgData.height);
      const offCtx = offscreen.getContext('2d');
      if (offCtx) {
        offCtx.putImageData(imgData, 0, 0);
        ctx.imageSmoothingEnabled = true;
        ctx.drawImage(offscreen, 0, 0, w, h);
      }

      // Cursor
      const { currentTime, duration } = useAudioStore.getState();
      if (duration > 0) {
        const cursorX = (currentTime / duration) * w;
        ctx.strokeStyle = 'rgba(255,255,255,0.8)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(cursorX, 0);
        ctx.lineTo(cursorX, h);
        ctx.stroke();
      }

      raf = requestAnimationFrame(draw);
    };
    raf = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(raf);
  }, [height]);

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
