/* ── DimensionSunburst — Concentric Ring Dimension Visualization ────
 *  Shows 6D → 12D → 24D as 3 concentric rings in a single SVG.
 *  Binary tree alignment: each 6D (60°) → 2×12D (30°) → 2×24D (15°).
 *
 *  Unlocked rings show colored data fill arcs.
 *  Locked rings show muted structural outlines + upgrade indicator.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { Lock } from "lucide-react";
import { useDimensions } from "@/hooks/useDimensions";
import { useM3Gate } from "@/hooks/useM3Gate";
import type { DimensionKey6D } from "@/types/dimensions";
import {
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
  PSYCHOLOGY_COLORS,
  COGNITION_CHILDREN,
  NEUROSCIENCE_CHILDREN,
} from "@/data/dimensions";

/* ── Props ─────────────────────────────────────────────────────── */

interface DimensionSunburstProps {
  /** Primary accent color (persona color) */
  color?: string;
  /** Chart diameter in pixels */
  size?: number;
  /** Called when user clicks a locked ring */
  onUpgrade?: () => void;
}

/* ── Geometry constants ────────────────────────────────────────── */

const VB = 400;
const CX = VB / 2;
const CY = VB / 2;

// Ring radii (innerR, outerR) — 3 rings with gaps
const RING_6D  = { innerR: 58,  outerR: 98  };
const RING_12D = { innerR: 106, outerR: 146 };
const RING_24D = { innerR: 154, outerR: 194 };

// Gaps in degrees
const GAP_6D  = 2;
const GAP_12D = 1.5;
const GAP_24D = 1;

const DEG = Math.PI / 180;
const START_OFFSET = -90 * DEG; // 12 o'clock

/* ── SVG arc path helpers ──────────────────────────────────────── */

function arcPath(
  cx: number, cy: number,
  innerR: number, outerR: number,
  startRad: number, endRad: number,
): string {
  const x1o = cx + Math.cos(startRad) * outerR;
  const y1o = cy + Math.sin(startRad) * outerR;
  const x2o = cx + Math.cos(endRad) * outerR;
  const y2o = cy + Math.sin(endRad) * outerR;
  const x1i = cx + Math.cos(endRad) * innerR;
  const y1i = cy + Math.sin(endRad) * innerR;
  const x2i = cx + Math.cos(startRad) * innerR;
  const y2i = cy + Math.sin(startRad) * innerR;
  const sweep = endRad - startRad;
  const la = sweep > Math.PI ? 1 : 0;
  return [
    `M ${x1o} ${y1o}`,
    `A ${outerR} ${outerR} 0 ${la} 1 ${x2o} ${y2o}`,
    `L ${x1i} ${y1i}`,
    `A ${innerR} ${innerR} 0 ${la} 0 ${x2i} ${y2i}`,
    `Z`,
  ].join(" ");
}

/** Label position at radial center of a segment */
function labelPos(
  cx: number, cy: number,
  r: number,
  startRad: number, endRad: number,
): { x: number; y: number; angle: number } {
  const mid = (startRad + endRad) / 2;
  return {
    x: cx + Math.cos(mid) * r,
    y: cy + Math.sin(mid) * r,
    angle: (mid * 180) / Math.PI,
  };
}

/** Lighten a hex color by mixing with white */
function lighten(hex: string, amount: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  const nr = Math.round(r + (255 - r) * amount);
  const ng = Math.round(g + (255 - g) * amount);
  const nb = Math.round(b + (255 - b) * amount);
  return `#${nr.toString(16).padStart(2, "0")}${ng.toString(16).padStart(2, "0")}${nb.toString(16).padStart(2, "0")}`;
}

/* ── Segment data structure ────────────────────────────────────── */

interface Segment {
  key: string;
  name: string;
  nameTr: string;
  layer: "psychology" | "cognition" | "neuroscience";
  parentColor: string;   // inherited 6D color
  color: string;         // segment-specific color
  startRad: number;
  endRad: number;
  innerR: number;
  outerR: number;
  value: number;
  index: number;
}

/* ── Build ordered segment list ────────────────────────────────── */

function buildSegments(
  psych: number[],
  cog: number[],
  neuro: number[],
): Segment[] {
  const segments: Segment[] = [];

  ALL_PSYCHOLOGY.forEach((p, pi) => {
    const pColor = PSYCHOLOGY_COLORS[p.key as DimensionKey6D] ?? "#888";
    const pStart = START_OFFSET + pi * 60 * DEG + (GAP_6D / 2) * DEG;
    const pEnd = START_OFFSET + (pi + 1) * 60 * DEG - (GAP_6D / 2) * DEG;

    // 6D segment
    segments.push({
      key: p.key, name: p.name, nameTr: p.nameTr,
      layer: "psychology", parentColor: pColor, color: pColor,
      startRad: pStart, endRad: pEnd,
      innerR: RING_6D.innerR, outerR: RING_6D.outerR,
      value: psych[pi] ?? 0, index: pi,
    });

    // 12D children (2 per 6D)
    const cogChildren = COGNITION_CHILDREN[p.key];
    if (!cogChildren) return;
    cogChildren.forEach((c, ci) => {
      const halfAngle = (pEnd - pStart) / 2;
      const cStart = pStart + ci * halfAngle + (GAP_12D / 2) * DEG;
      const cEnd = pStart + (ci + 1) * halfAngle - (GAP_12D / 2) * DEG;
      const cColor = lighten(pColor, 0.15);

      segments.push({
        key: c.key, name: c.name, nameTr: c.nameTr,
        layer: "cognition", parentColor: pColor, color: cColor,
        startRad: cStart, endRad: cEnd,
        innerR: RING_12D.innerR, outerR: RING_12D.outerR,
        value: cog[c.index] ?? 0, index: c.index,
      });

      // 24D children (2 per 12D)
      const neuroChildren = NEUROSCIENCE_CHILDREN[c.key];
      if (!neuroChildren) return;
      neuroChildren.forEach((n, ni) => {
        const qAngle = (cEnd - cStart) / 2;
        const nStart = cStart + ni * qAngle + (GAP_24D / 2) * DEG;
        const nEnd = cStart + (ni + 1) * qAngle - (GAP_24D / 2) * DEG;
        const nColor = lighten(pColor, 0.3);

        segments.push({
          key: n.key, name: n.name, nameTr: n.nameTr,
          layer: "neuroscience", parentColor: pColor, color: nColor,
          startRad: nStart, endRad: nEnd,
          innerR: RING_24D.innerR, outerR: RING_24D.outerR,
          value: neuro[n.index] ?? 0, index: n.index,
        });
      });
    });
  });

  return segments;
}

/* ── Component ─────────────────────────────────────────────────── */

export function DimensionSunburst({
  color: _accentColor,
  size = 300,
  onUpgrade,
}: DimensionSunburstProps) {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { state } = useDimensions(isTr ? "tr" : "en");
  const { canSeeDimensionLayer } = useM3Gate();

  const [hovered, setHovered] = useState<string | null>(null);
  const [tooltip, setTooltip] = useState<{
    x: number; y: number; text: string; locked: boolean;
  } | null>(null);

  const canSeeCog = canSeeDimensionLayer("cognition");
  const canSeeNeuro = canSeeDimensionLayer("neuroscience");

  const segments = useMemo(
    () => buildSegments(state.psychology, state.cognition, state.neuroscience),
    [state.psychology, state.cognition, state.neuroscience],
  );

  const isLayerLocked = (layer: string) => {
    if (layer === "psychology") return false;
    if (layer === "cognition") return !canSeeCog;
    if (layer === "neuroscience") return !canSeeNeuro;
    return true;
  };

  const handleHover = (seg: Segment, e: React.MouseEvent<SVGPathElement>) => {
    setHovered(seg.key);
    const locked = isLayerLocked(seg.layer);
    const name = isTr ? seg.nameTr : seg.name;
    const valStr = locked ? "" : ` ${Math.round(seg.value * 100)}%`;
    const rect = e.currentTarget.closest("svg")!.getBoundingClientRect();
    const svgX = ((e.clientX - rect.left) / rect.width) * VB;
    const svgY = ((e.clientY - rect.top) / rect.height) * VB;
    setTooltip({
      x: svgX,
      y: svgY - 12,
      text: locked ? `${name}` : `${name}${valStr}`,
      locked,
    });
  };

  const handleLeave = () => {
    setHovered(null);
    setTooltip(null);
  };

  const handleLockedClick = (layer: string) => {
    if (isLayerLocked(layer) && onUpgrade) onUpgrade();
  };

  // 12D lock icon positions (6 pairs → center of each 6D's cognition span)
  const lockPositions12D = !canSeeCog
    ? ALL_PSYCHOLOGY.map((_, pi) => {
        const midAngle = START_OFFSET + (pi + 0.5) * 60 * DEG;
        const midR = (RING_12D.innerR + RING_12D.outerR) / 2;
        return { x: CX + Math.cos(midAngle) * midR, y: CY + Math.sin(midAngle) * midR };
      })
    : [];

  // 24D lock icon: one per 6D sector if locked
  const lockPositions24D = !canSeeNeuro
    ? ALL_PSYCHOLOGY.map((_, pi) => {
        const midAngle = START_OFFSET + (pi + 0.5) * 60 * DEG;
        const midR = (RING_24D.innerR + RING_24D.outerR) / 2;
        return { x: CX + Math.cos(midAngle) * midR, y: CY + Math.sin(midAngle) * midR };
      })
    : [];

  return (
    <div className="relative flex flex-col items-center">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${VB} ${VB}`}
        className="overflow-visible"
      >
        {/* ── Ring backgrounds (subtle circular guides) ────── */}
        <circle cx={CX} cy={CY} r={RING_6D.outerR} fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth={0.5} />
        <circle cx={CX} cy={CY} r={RING_12D.outerR} fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth={0.5} />
        <circle cx={CX} cy={CY} r={RING_24D.outerR} fill="none" stroke="rgba(255,255,255,0.02)" strokeWidth={0.5} />

        {/* ── Segment tracks + fills ──────────────────────── */}
        {segments.map((seg) => {
          const locked = isLayerLocked(seg.layer);
          const isHov = hovered === seg.key;
          const trackPath = arcPath(CX, CY, seg.innerR, seg.outerR, seg.startRad, seg.endRad);

          // Fill: proportional radius
          const clampedVal = Math.max(0, Math.min(1, seg.value));
          const fillOuterR = seg.innerR + (seg.outerR - seg.innerR) * clampedVal;
          const fillPath = clampedVal > 0.01
            ? arcPath(CX, CY, seg.innerR, fillOuterR, seg.startRad, seg.endRad)
            : null;

          // Stagger index for animation delay
          const layerOffset = seg.layer === "psychology" ? 0 : seg.layer === "cognition" ? 6 : 18;
          const animDelay = (layerOffset + seg.index) * 20;

          // Fill opacity by layer
          const fillOpacity = seg.layer === "psychology" ? 0.7
            : seg.layer === "cognition" ? 0.5 : 0.4;

          return (
            <g key={`${seg.layer}-${seg.key}`}>
              {/* Track (background arc) */}
              <path
                d={trackPath}
                fill={locked ? "rgba(255,255,255,0.015)" : "rgba(255,255,255,0.04)"}
                stroke={locked ? "rgba(255,255,255,0.06)" : "rgba(255,255,255,0.06)"}
                strokeWidth={0.5}
                strokeDasharray={locked ? "3 3" : undefined}
                opacity={isHov ? 1.2 : 1}
                onMouseEnter={(e) => handleHover(seg, e)}
                onMouseLeave={handleLeave}
                onClick={() => handleLockedClick(seg.layer)}
                style={{ cursor: locked ? "pointer" : "default" }}
              />

              {/* Data fill arc (only for unlocked layers) */}
              {!locked && fillPath && (
                <path
                  d={fillPath}
                  fill={seg.color}
                  opacity={fillOpacity}
                  stroke={seg.parentColor}
                  strokeWidth={0.5}
                  strokeOpacity={0.3}
                  style={{
                    transition: `opacity 0.6s ease ${animDelay}ms`,
                  }}
                  onMouseEnter={(e) => handleHover(seg, e)}
                  onMouseLeave={handleLeave}
                >
                  {/* Animate the fill arc growing from inner to target */}
                  <animate
                    attributeName="d"
                    from={arcPath(CX, CY, seg.innerR, seg.innerR + 1, seg.startRad, seg.endRad)}
                    to={fillPath}
                    dur="0.6s"
                    begin={`${animDelay}ms`}
                    fill="freeze"
                    calcMode="spline"
                    keySplines="0.22 1 0.36 1"
                    keyTimes="0;1"
                  />
                </path>
              )}
            </g>
          );
        })}

        {/* ── 6D Labels (always visible) ─────────────────── */}
        {ALL_PSYCHOLOGY.map((p, pi) => {
          const pStart = START_OFFSET + pi * 60 * DEG + (GAP_6D / 2) * DEG;
          const pEnd = START_OFFSET + (pi + 1) * 60 * DEG - (GAP_6D / 2) * DEG;
          const midR = (RING_6D.innerR + RING_6D.outerR) / 2;
          const pos = labelPos(CX, CY, midR, pStart, pEnd);
          const pColor = PSYCHOLOGY_COLORS[p.key as DimensionKey6D] ?? "#888";

          // Rotate text to follow the arc, flip if on bottom half
          let textAngle = pos.angle + 90;
          if (textAngle > 90 && textAngle < 270) textAngle += 180;
          // For 6D with only 6 segments and wide arcs, just center horizontally
          return (
            <text
              key={p.key}
              x={pos.x}
              y={pos.y}
              textAnchor="middle"
              dominantBaseline="middle"
              fill={pColor}
              fontSize={11}
              fontFamily="var(--font-display)"
              fontWeight="600"
              style={{ pointerEvents: "none" }}
            >
              {isTr ? p.nameTr : p.name}
            </text>
          );
        })}

        {/* ── 12D Labels (smaller, visible) ──────────────── */}
        {ALL_PSYCHOLOGY.map((p, pi) => {
          const cogChildren = COGNITION_CHILDREN[p.key];
          if (!cogChildren) return null;
          const pStart = START_OFFSET + pi * 60 * DEG + (GAP_6D / 2) * DEG;
          const pEnd = START_OFFSET + (pi + 1) * 60 * DEG - (GAP_6D / 2) * DEG;
          const halfAngle = (pEnd - pStart) / 2;
          const locked = !canSeeCog;

          return cogChildren.map((c, ci) => {
            const cStart = pStart + ci * halfAngle + (GAP_12D / 2) * DEG;
            const cEnd = pStart + (ci + 1) * halfAngle - (GAP_12D / 2) * DEG;
            const midR = (RING_12D.innerR + RING_12D.outerR) / 2;
            const pos = labelPos(CX, CY, midR, cStart, cEnd);

            // Abbreviated name: first word only for tight fit
            const shortName = (isTr ? c.nameTr : c.name).split(" ")[0];

            return (
              <text
                key={c.key}
                x={pos.x}
                y={pos.y}
                textAnchor="middle"
                dominantBaseline="middle"
                fill={locked ? "rgba(255,255,255,0.12)" : "rgba(255,255,255,0.45)"}
                fontSize={7.5}
                fontFamily="var(--font-mono)"
                style={{ pointerEvents: "none" }}
              >
                {shortName}
              </text>
            );
          });
        })}

        {/* ── Lock icons for locked rings ─────────────────── */}
        {lockPositions12D.map((pos, i) => (
          <g key={`lock12-${i}`} transform={`translate(${pos.x - 5}, ${pos.y - 5})`} opacity={0.25}>
            <rect x={0} y={0} width={10} height={10} rx={2} fill="rgba(0,0,0,0.6)" />
            <foreignObject x={1} y={1} width={8} height={8}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 8, height: 8 }}>
                <Lock size={6} color="rgba(255,255,255,0.5)" />
              </div>
            </foreignObject>
          </g>
        ))}

        {lockPositions24D.map((pos, i) => (
          <g key={`lock24-${i}`} transform={`translate(${pos.x - 5}, ${pos.y - 5})`} opacity={0.25}>
            <rect x={0} y={0} width={10} height={10} rx={2} fill="rgba(0,0,0,0.6)" />
            <foreignObject x={1} y={1} width={8} height={8}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 8, height: 8 }}>
                <Lock size={6} color="rgba(255,255,255,0.5)" />
              </div>
            </foreignObject>
          </g>
        ))}

        {/* ── Tooltip ────────────────────────────────────── */}
        {tooltip && (
          <g style={{ pointerEvents: "none" }}>
            <rect
              x={tooltip.x - 60}
              y={tooltip.y - 14}
              width={120}
              height={20}
              rx={6}
              fill="rgba(0,0,0,0.85)"
              stroke="rgba(255,255,255,0.08)"
              strokeWidth={0.5}
            />
            {tooltip.locked && (
              <foreignObject x={tooltip.x - 56} y={tooltip.y - 11} width={12} height={14}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 12, height: 14 }}>
                  <Lock size={8} color="rgba(255,255,255,0.4)" />
                </div>
              </foreignObject>
            )}
            <text
              x={tooltip.locked ? tooltip.x + 2 : tooltip.x}
              y={tooltip.y}
              textAnchor="middle"
              dominantBaseline="middle"
              fill={tooltip.locked ? "rgba(255,255,255,0.4)" : "rgba(255,255,255,0.8)"}
              fontSize={8}
              fontFamily="var(--font-mono)"
            >
              {tooltip.text}
            </text>
          </g>
        )}

        {/* ── Center label ───────────────────────────────── */}
        <text
          x={CX}
          y={CY - 6}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="rgba(255,255,255,0.25)"
          fontSize={9}
          fontFamily="var(--font-display)"
          fontWeight="500"
        >
          {t("dimensions.title", "Dimensions")}
        </text>
        <text
          x={CX}
          y={CY + 8}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="rgba(255,255,255,0.12)"
          fontSize={7}
          fontFamily="var(--font-mono)"
        >
          6 · 12 · 24
        </text>
      </svg>

      {/* ── Upgrade CTA below chart (if any ring is locked) ── */}
      {(!canSeeCog || !canSeeNeuro) && (
        <button
          onClick={onUpgrade}
          className="mt-2 text-[9px] font-mono px-3 py-1 rounded-full transition-colors"
          style={{
            color: "rgba(255,255,255,0.35)",
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(255,255,255,0.06)",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.color = "rgba(255,255,255,0.6)";
            e.currentTarget.style.background = "rgba(255,255,255,0.06)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.color = "rgba(255,255,255,0.35)";
            e.currentTarget.style.background = "rgba(255,255,255,0.03)";
          }}
        >
          {t("dimensions.upgrade", "Upgrade to unlock")}
        </button>
      )}
    </div>
  );
}
