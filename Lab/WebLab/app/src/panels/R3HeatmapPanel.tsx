import React, { useRef, useCallback, useEffect, useMemo } from "react";
import { useStore } from "../store";
import { viridis, drawPlayhead } from "../canvas/colormap";
import { useCanvasResize } from "../hooks/useCanvasResize";
import { R3_GROUP_COLOR_MAP } from "../theme/tokens";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const BORDER = "#252538";
const LABEL_WIDTH = 28;
const FEATURES = 128;

/**
 * R3HeatmapPanel - Canvas-based (T_lod x 128) heatmap of R3 spectral features.
 * Full heatmap is rendered to an offscreen canvas on data change.
 * Only the playhead overlay redraws on frame change.
 */
export default function R3HeatmapPanel(): React.ReactElement {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const offscreenRef = useRef<HTMLCanvasElement | null>(null);
  const sizeRef = useRef({ w: 0, h: 0 });

  const r3Data = useStore((s) => s.r3Data);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);
  const r3Groups = useStore((s) => s.r3Groups);

  // Build the offscreen heatmap ImageData whenever r3Data changes
  const offscreenReady = useMemo(() => {
    if (!r3Data || r3Data.length === 0) return false;
    const T = r3Data.length;
    const oc = document.createElement("canvas");
    oc.width = T;
    oc.height = FEATURES;
    const ctx = oc.getContext("2d");
    if (!ctx) return false;
    const imageData = ctx.createImageData(T, FEATURES);
    const d = imageData.data;

    for (let y = 0; y < FEATURES; y++) {
      for (let x = 0; x < T; x++) {
        const val = r3Data[x]?.[y] ?? 0;
        const clamped = Math.max(0, Math.min(1, val));
        const [r, g, b] = viridis(clamped);
        const idx = (y * T + x) * 4;
        d[idx] = r;
        d[idx + 1] = g;
        d[idx + 2] = b;
        d[idx + 3] = 255;
      }
    }
    ctx.putImageData(imageData, 0, 0);
    offscreenRef.current = oc;
    return true;
  }, [r3Data]);

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const { w, h } = sizeRef.current;
    if (w === 0 || h === 0) return;

    // Clear
    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, w, h);

    if (!offscreenReady || !offscreenRef.current || !r3Data) {
      ctx.fillStyle = TEXT;
      ctx.font = "12px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Waiting for R\u00b3 data\u2026", w / 2, h / 2);
      return;
    }

    const T = r3Data.length;
    const plotX = LABEL_WIDTH;
    const plotW = w - LABEL_WIDTH;
    const plotH = h;

    // Draw heatmap from offscreen
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(offscreenRef.current, plotX, 0, plotW, plotH);

    // Draw group dividers and labels
    if (r3Groups.length > 0) {
      ctx.save();
      ctx.font = "10px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      for (const grp of r3Groups) {
        const yStart = (grp.start / FEATURES) * plotH;
        const yEnd = (grp.end / FEATURES) * plotH;
        // Divider line
        ctx.strokeStyle = BORDER;
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(plotX, yStart);
        ctx.lineTo(w, yStart);
        ctx.stroke();
        // Label
        const yMid = (yStart + yEnd) / 2;
        ctx.fillStyle = R3_GROUP_COLOR_MAP[grp.letter] ?? TEXT;
        ctx.fillText(grp.letter, LABEL_WIDTH / 2, yMid);
      }
      ctx.restore();
    }

    // Draw playhead
    if (T > 0) {
      const px = plotX + (lodFrameIndex / (T - 1)) * plotW;
      drawPlayhead(ctx, px, plotH);
    }
  }, [offscreenReady, r3Data, r3Groups, lodFrameIndex]);

  const handleResize = useCallback(
    (w: number, h: number) => {
      sizeRef.current = { w, h };
      draw();
    },
    [draw],
  );

  useCanvasResize(canvasRef, handleResize);

  // Redraw on frame change or data change
  useEffect(() => {
    draw();
  }, [draw]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100%",
        background: BG,
        border: `1px solid ${BORDER}`,
        borderRadius: 6,
        overflow: "hidden",
      }}
    >
      <div
        style={{
          padding: "6px 12px",
          fontSize: 12,
          fontWeight: 600,
          color: TEXT,
          borderBottom: `1px solid ${BORDER}`,
          flexShrink: 0,
        }}
      >
        R\u00b3 Spectral Features (128D)
      </div>
      <canvas
        ref={canvasRef}
        style={{ flex: 1, width: "100%", display: "block" }}
      />
    </div>
  );
}
