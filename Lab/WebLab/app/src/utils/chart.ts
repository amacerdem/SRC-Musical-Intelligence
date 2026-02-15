/** 12 distinct high-contrast colors for line charts on dark backgrounds. */
export const LINE_PALETTE = [
  "#ef4444", // red
  "#3b82f6", // blue
  "#22c55e", // green
  "#f59e0b", // amber
  "#8b5cf6", // violet
  "#06b6d4", // cyan
  "#ec4899", // pink
  "#14b8a6", // teal
  "#f97316", // orange
  "#a855f7", // purple
  "#84cc16", // lime
  "#e11d48", // rose
];

/** Pick a distinct color from the palette by index. */
export function lineColor(index: number): string {
  return LINE_PALETTE[index % LINE_PALETTE.length]!;
}

/**
 * Build a smoothed SVG path by binning data points.
 * Reduces ~2000 frames down to ~targetPoints for pixel-appropriate detail.
 *
 * @param data       2D array [T][D] — time × dimensions
 * @param dimIndex   Which dimension column to extract
 * @param plotW      SVG coordinate width of the plot area
 * @param plotH      SVG coordinate height of the plot area
 * @param targetPoints  Max points in the path (default: plotW / 2)
 * @returns SVG path `d` string in plot-relative coordinates (0,0 = top-left)
 */
export function buildSmoothPath(
  data: number[][],
  dimIndex: number,
  plotW: number,
  plotH: number,
  targetPoints?: number,
): string {
  const T = data.length;
  if (T === 0) return "";

  const nPts = Math.max(2, targetPoints ?? Math.min(T, Math.round(plotW / 2)));

  if (T <= nPts) {
    // No downsampling needed — plot every point
    const xStep = T > 1 ? plotW / (T - 1) : 0;
    const parts: string[] = [];
    for (let t = 0; t < T; t++) {
      const v = Math.max(0, Math.min(1, data[t]?.[dimIndex] ?? 0));
      const x = t * xStep;
      const y = plotH - v * plotH;
      parts.push(`${t === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`);
    }
    return parts.join(" ");
  }

  // Bin averaging: merge adjacent frames into bins, take the mean
  const binSize = T / nPts;
  const parts: string[] = [];
  const xStep = plotW / (nPts - 1);

  for (let i = 0; i < nPts; i++) {
    const binStart = Math.floor(i * binSize);
    const binEnd = Math.min(T, Math.floor((i + 1) * binSize));
    let sum = 0;
    let count = 0;
    for (let j = binStart; j < binEnd; j++) {
      sum += data[j]?.[dimIndex] ?? 0;
      count++;
    }
    const avg = count > 0 ? sum / count : 0;
    const v = Math.max(0, Math.min(1, avg));
    const x = i * xStep;
    const y = plotH - v * plotH;
    parts.push(`${i === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`);
  }

  return parts.join(" ");
}
