import React, { useRef, useCallback, useEffect, useMemo } from "react";
import { useStore } from "../store";
import { viridis, drawPlayhead } from "../canvas/colormap";
import { useCanvasResize } from "../hooks/useCanvasResize";

const BG = "#0d0d14";
const TEXT = "#c8c8d4";
const BORDER = "#252538";
const LABEL_WIDTH = 80;

const SCOPE_TINTS: Record<string, [number, number, number]> = {
  internal: [59, 130, 246],  // #3b82f6
  external: [34, 197, 94],   // #22c55e
  hybrid: [245, 158, 11],    // #f59e0b
};

function blendViridisWithScope(
  value: number,
  scope: string,
): [number, number, number] {
  const [vr, vg, vb] = viridis(Math.max(0, Math.min(1, value)));
  const tint = SCOPE_TINTS[scope];
  if (!tint) return [vr, vg, vb];
  const blend = 0.2;
  return [
    Math.round(vr * (1 - blend) + tint[0] * blend),
    Math.round(vg * (1 - blend) + tint[1] * blend),
    Math.round(vb * (1 - blend) + tint[2] * blend),
  ];
}

/**
 * NucleusOutputPanel - Canvas-based (T_lod x OUTPUT_DIM) heatmap for selected nucleus.
 * Rows are color-tinted by layer scope (internal/external/hybrid).
 */
export default function NucleusOutputPanel(): React.ReactElement {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const offscreenRef = useRef<HTMLCanvasElement | null>(null);
  const sizeRef = useRef({ w: 0, h: 0 });

  const selectedNucleus = useStore((s) => s.selectedNucleus);
  const nucleusData = useStore((s) => s.nucleusData);
  const lodFrameIndex = useStore((s) => s.lodFrameIndex);

  const nd = selectedNucleus ? nucleusData[selectedNucleus] ?? null : null;

  // Build scope map: dimIndex -> scope
  const scopeMap = useMemo(() => {
    if (!nd) return [];
    const map: string[] = new Array(nd.output_dim).fill("internal");
    for (const layer of nd.layers) {
      for (let i = layer.start; i < layer.end; i++) {
        map[i] = layer.scope;
      }
    }
    return map;
  }, [nd]);

  // Build offscreen heatmap
  const offscreenReady = useMemo(() => {
    if (!nd || !nd.output || nd.output.length === 0) return false;
    const T = nd.output.length;
    const D = nd.output_dim;
    const oc = document.createElement("canvas");
    oc.width = T;
    oc.height = D;
    const ctx = oc.getContext("2d");
    if (!ctx) return false;
    const imageData = ctx.createImageData(T, D);
    const d = imageData.data;

    for (let y = 0; y < D; y++) {
      const scope = scopeMap[y] ?? "internal";
      for (let x = 0; x < T; x++) {
        const val = nd.output[x]?.[y] ?? 0;
        const [r, g, b] = blendViridisWithScope(val, scope);
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
  }, [nd, scopeMap]);

  const headerText = nd
    ? `${nd.name} \u2014 ${nd.full_name} (${nd.output_dim}D)`
    : "Nucleus Output";

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    const { w, h } = sizeRef.current;
    if (w === 0 || h === 0) return;

    ctx.fillStyle = BG;
    ctx.fillRect(0, 0, w, h);

    if (!selectedNucleus || !nd) {
      ctx.fillStyle = TEXT;
      ctx.font = "13px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText("Select a nucleus", w / 2, h / 2);
      return;
    }

    if (!offscreenReady || !offscreenRef.current) {
      ctx.fillStyle = TEXT;
      ctx.font = "12px Inter, sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("Loading\u2026", w / 2, h / 2);
      return;
    }

    const T = nd.output.length;
    const D = nd.output_dim;
    const plotX = LABEL_WIDTH;
    const plotW = w - LABEL_WIDTH;
    const plotH = h;

    // Draw heatmap
    ctx.imageSmoothingEnabled = false;
    ctx.drawImage(offscreenRef.current, plotX, 0, plotW, plotH);

    // Draw dimension labels on left
    ctx.save();
    ctx.font = "9px 'JetBrains Mono', monospace";
    ctx.textAlign = "right";
    ctx.textBaseline = "middle";
    const rowH = plotH / D;
    for (let i = 0; i < D; i++) {
      const yMid = i * rowH + rowH / 2;
      const scope = scopeMap[i] ?? "internal";
      const tint = SCOPE_TINTS[scope];
      ctx.fillStyle = tint
        ? `rgb(${tint[0]},${tint[1]},${tint[2]})`
        : TEXT;
      const label = nd.dimension_names[i] ?? `d${i}`;
      // Truncate long labels
      const displayLabel = label.length > 10 ? label.slice(0, 9) + "\u2026" : label;
      ctx.fillText(displayLabel, LABEL_WIDTH - 4, yMid);
    }
    ctx.restore();

    // Draw playhead
    if (T > 1) {
      const px = plotX + (lodFrameIndex / (T - 1)) * plotW;
      drawPlayhead(ctx, px, plotH);
    }
  }, [selectedNucleus, nd, offscreenReady, scopeMap, lodFrameIndex]);

  const handleResize = useCallback(
    (w: number, h: number) => {
      sizeRef.current = { w, h };
      draw();
    },
    [draw],
  );

  useCanvasResize(canvasRef, handleResize);

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
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {headerText}
      </div>
      <canvas
        ref={canvasRef}
        style={{ flex: 1, width: "100%", display: "block" }}
      />
    </div>
  );
}
