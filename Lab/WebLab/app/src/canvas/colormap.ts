/**
 * Viridis-inspired colormap: value [0,1] → [r, g, b] each in [0,255].
 * Pre-computed 256-entry LUT for fast Canvas rendering.
 */
const VIRIDIS_LUT: [number, number, number][] = [];

// Generate viridis approximation (dark purple → teal → yellow)
for (let i = 0; i < 256; i++) {
  const t = i / 255;
  const r = Math.round(
    255 *
      Math.min(
        1,
        Math.max(0, -0.0195 + 4.0348 * t - 14.9533 * t * t + 26.7721 * t * t * t - 16.2141 * t * t * t * t),
      ),
  );
  const g = Math.round(
    255 *
      Math.min(
        1,
        Math.max(0, 0.0146 + 0.4235 * t + 3.3697 * t * t - 8.5706 * t * t * t + 5.8137 * t * t * t * t),
      ),
  );
  const b = Math.round(
    255 *
      Math.min(
        1,
        Math.max(0, 0.3289 + 1.7672 * t - 6.9457 * t * t + 10.7639 * t * t * t - 5.9004 * t * t * t * t),
      ),
  );
  VIRIDIS_LUT.push([r, g, b]);
}

/** Map a [0,1] value to an RGB triple. */
export function viridis(v: number): [number, number, number] {
  const idx = Math.max(0, Math.min(255, Math.round(v * 255)));
  return VIRIDIS_LUT[idx]!;
}

/** Map a [0,1] value to a CSS color string. */
export function viridisCSS(v: number): string {
  const [r, g, b] = viridis(v);
  return `rgb(${r},${g},${b})`;
}

/** Draw a playhead line on a canvas 2D context. */
export function drawPlayhead(
  ctx: CanvasRenderingContext2D,
  x: number,
  height: number,
  color = "#ef4444",
): void {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  ctx.moveTo(x, 0);
  ctx.lineTo(x, height);
  ctx.stroke();
  ctx.restore();
}
