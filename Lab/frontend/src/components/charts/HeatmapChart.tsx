import { useRef, useEffect, useCallback } from 'react';
import { useAudioStore } from '../../stores/audioStore';

interface Props {
  /** Flat Float32Array of shape (nRows × nCols), row-major */
  data: Float32Array | null;
  nRows: number;
  nCols: number;
  height?: number;
  /** Row labels (Y axis) */
  rowLabels?: string[];
  /** Colormap: 'viridis' | 'magma' | 'inferno' */
  colormap?: 'viridis' | 'magma';
  /** Value range [min, max]. Auto-detect if null. */
  valueRange?: [number, number] | null;
}

// Viridis colormap
const VIRIDIS = [
  [68,1,84],[72,36,117],[65,68,135],[53,95,141],
  [42,120,142],[33,145,140],[53,183,121],[94,201,98],
  [170,220,50],[253,231,37],
];

// Magma colormap
const MAGMA = [
  [0,0,4],[28,16,68],[79,18,123],[129,37,129],
  [181,54,122],[229,89,100],[251,135,97],[254,186,117],
  [254,227,145],[252,253,191],
];

function lookupColor(t: number, cmap: number[][]): [number, number, number] {
  const c = Math.max(0, Math.min(1, t));
  const idx = c * (cmap.length - 1);
  const lo = Math.floor(idx);
  const hi = Math.min(lo + 1, cmap.length - 1);
  const f = idx - lo;
  return [
    Math.round(cmap[lo][0] + (cmap[hi][0] - cmap[lo][0]) * f),
    Math.round(cmap[lo][1] + (cmap[hi][1] - cmap[lo][1]) * f),
    Math.round(cmap[lo][2] + (cmap[hi][2] - cmap[lo][2]) * f),
  ];
}

export default function HeatmapChart({
  data,
  nRows,
  nCols,
  height = 200,
  rowLabels,
  colormap = 'viridis',
  valueRange = null,
}: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const imageRef = useRef<ImageData | null>(null);

  const cmap = colormap === 'magma' ? MAGMA : VIRIDIS;

  // Pre-render heatmap image
  const renderImage = useCallback(() => {
    if (!data || nRows === 0 || nCols === 0) {
      imageRef.current = null;
      return;
    }

    let min: number, max: number;
    if (valueRange) {
      [min, max] = valueRange;
    } else {
      min = Infinity; max = -Infinity;
      for (let i = 0; i < data.length; i++) {
        if (data[i] < min) min = data[i];
        if (data[i] > max) max = data[i];
      }
    }
    const range = max - min || 1;

    const imgData = new ImageData(nCols, nRows);
    for (let r = 0; r < nRows; r++) {
      for (let c = 0; c < nCols; c++) {
        const val = (data[r * nCols + c] - min) / range;
        const [red, green, blue] = lookupColor(val, cmap);
        const y = nRows - 1 - r; // flip so row 0 is bottom
        const idx = (y * nCols + c) * 4;
        imgData.data[idx] = red;
        imgData.data[idx + 1] = green;
        imgData.data[idx + 2] = blue;
        imgData.data[idx + 3] = 255;
      }
    }
    imageRef.current = imgData;
  }, [data, nRows, nCols, cmap, valueRange]);

  useEffect(() => { renderImage(); }, [renderImage]);

  // Draw loop
  useEffect(() => {
    let raf: number;
    const draw = () => {
      const canvas = canvasRef.current;
      const container = containerRef.current;
      if (!canvas || !container) { raf = requestAnimationFrame(draw); return; }

      const dpr = window.devicePixelRatio || 1;
      const labelW = rowLabels ? 50 : 0;
      const w = container.clientWidth;
      const plotW = w - labelW;
      const h = height;
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      canvas.style.width = `${w}px`;
      canvas.style.height = `${h}px`;

      const ctx = canvas.getContext('2d');
      if (!ctx) { raf = requestAnimationFrame(draw); return; }
      ctx.scale(dpr, dpr);
      ctx.clearRect(0, 0, w, h);

      const imgData = imageRef.current;
      if (!imgData) {
        ctx.fillStyle = 'rgba(255,255,255,0.03)';
        ctx.fillRect(labelW, 0, plotW, h);
        ctx.fillStyle = 'rgba(255,255,255,0.15)';
        ctx.font = '11px Inter';
        ctx.textAlign = 'center';
        ctx.fillText('No H³ data', w / 2, h / 2);
        raf = requestAnimationFrame(draw);
        return;
      }

      // Draw heatmap
      const offscreen = new OffscreenCanvas(imgData.width, imgData.height);
      const offCtx = offscreen.getContext('2d');
      if (offCtx) {
        offCtx.putImageData(imgData, 0, 0);
        ctx.imageSmoothingEnabled = false;
        ctx.drawImage(offscreen, labelW, 0, plotW, h);
      }

      // Row labels
      if (rowLabels) {
        ctx.font = '9px JetBrains Mono, monospace';
        ctx.textAlign = 'right';
        ctx.fillStyle = 'rgba(255,255,255,0.4)';
        const rowH = h / nRows;
        for (let r = 0; r < nRows; r++) {
          const y = h - (r + 0.5) * rowH;
          ctx.fillText(rowLabels[r] || `${r}`, labelW - 4, y + 3);
        }
      }

      // Cursor
      const { currentTime, duration } = useAudioStore.getState();
      if (duration > 0) {
        const cursorX = labelW + (currentTime / duration) * plotW;
        ctx.strokeStyle = 'rgba(255,255,255,0.7)';
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
  }, [height, nRows, rowLabels]);

  const handleClick = (e: React.MouseEvent) => {
    const { duration } = useAudioStore.getState();
    if (duration <= 0) return;
    const rect = e.currentTarget.getBoundingClientRect();
    const labelW = rowLabels ? 50 : 0;
    const plotW = rect.width - labelW;
    const x = e.clientX - rect.left - labelW;
    if (x < 0) return;
    useAudioStore.getState().setCurrentTime((x / plotW) * duration);
  };

  return (
    <div ref={containerRef} className="w-full cursor-crosshair" style={{ height }} onClick={handleClick}>
      <canvas ref={canvasRef} />
    </div>
  );
}
