import { useEffect, type RefObject } from "react";

/**
 * Keeps a canvas element sized to its CSS layout dimensions (devicePixelRatio-aware).
 * Calls `onResize` whenever the size changes.
 */
export function useCanvasResize(
  canvasRef: RefObject<HTMLCanvasElement | null>,
  onResize?: (w: number, h: number) => void,
): void {
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        const dpr = window.devicePixelRatio || 1;
        canvas.width = Math.round(width * dpr);
        canvas.height = Math.round(height * dpr);
        const ctx = canvas.getContext("2d");
        if (ctx) ctx.scale(dpr, dpr);
        onResize?.(width, height);
      }
    });

    ro.observe(canvas);
    return () => ro.disconnect();
  }, [canvasRef, onResize]);
}
