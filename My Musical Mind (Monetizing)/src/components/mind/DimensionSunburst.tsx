/* ── DimensionSunburst — 3 Nested Radar Charts ────────────────────
 *  Three concentric radar rings: 6D (inner) → 12D → 24D (outer).
 *  Each layer occupies its own radial band with gaps for labels.
 *  Binary-tree aligned axes: each 6D splits into 2×12D, 2×24D.
 *  Locked layers show muted grid structure, no data polygon.
 *  ──────────────────────────────────────────────────────────────── */

import { useState, useMemo, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Lock } from "lucide-react";
import { useDimensions } from "@/hooks/useDimensions";
import { useM3Gate } from "@/hooks/useM3Gate";
import {
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
} from "@/data/dimensions";

/* ── Props ───────────────────────────────────────────────────────── */

interface DimensionSunburstProps {
  color?: string;
  size?: number;
  onUpgrade?: () => void;
}

/* ── Geometry constants ──────────────────────────────────────────── */

const VB = 400;
const CX = VB / 2;
const CY = VB / 2;
const DEG = Math.PI / 180;

const R6_MAX = 62;
const R12_BASE = 82;
const R12_MAX = 126;
const R24_BASE = 146;
const R24_MAX = 192;

const R6_LABEL = (R6_MAX + R12_BASE) / 2;
const R12_LABEL = (R12_MAX + R24_BASE) / 2;

const ANGLES_6D = Array.from({ length: 6 }, (_, i) => -90 + i * 60);

const ANGLES_12D: number[] = [];
for (let i = 0; i < 6; i++) {
  ANGLES_12D.push(ANGLES_6D[i] - 15, ANGLES_6D[i] + 15);
}

const ANGLES_24D: number[] = [];
for (const a of ANGLES_12D) {
  ANGLES_24D.push(a - 7.5, a + 7.5);
}

const GRID_RADII = [
  R6_MAX * 0.5, R6_MAX,
  R12_BASE, (R12_BASE + R12_MAX) / 2, R12_MAX,
  R24_BASE, (R24_BASE + R24_MAX) / 2, R24_MAX,
];

/* ── Helpers ─────────────────────────────────────────────────────── */

function polar(deg: number, r: number) {
  const rad = deg * DEG;
  return { x: CX + Math.cos(rad) * r, y: CY + Math.sin(rad) * r };
}

function clamp01(v: number) {
  return Math.max(0, Math.min(1, v));
}

function colorOf6D(i: number): string {
  return ALL_PSYCHOLOGY[i]?.color ?? "#888";
}

/** 12D index → 6D parent index via parentKey chain */
const PARENT_6D_OF_12D: number[] = ALL_COGNITION.map((cog) => {
  const idx = ALL_PSYCHOLOGY.findIndex((p) => p.key === cog.parentKey);
  return idx >= 0 ? idx : 0;
});

/** 24D index → 6D grandparent index via parentKey chain */
const PARENT_6D_OF_24D: number[] = ALL_NEUROSCIENCE.map((neuro) => {
  const cogParent = ALL_COGNITION.find((c) => c.key === neuro.parentKey);
  if (!cogParent) return 0;
  const idx = ALL_PSYCHOLOGY.findIndex((p) => p.key === cogParent.parentKey);
  return idx >= 0 ? idx : 0;
});

function lighten(hex: string, amt: number): string {
  // Handle hex with alpha suffix (e.g. "#38BDF8B0")
  const cleanHex = hex.length > 7 ? hex.slice(0, 7) : hex;
  const r = parseInt(cleanHex.slice(1, 3), 16);
  const g = parseInt(cleanHex.slice(3, 5), 16);
  const b = parseInt(cleanHex.slice(5, 7), 16);
  return `#${[r, g, b]
    .map((c) =>
      Math.round(c + (255 - c) * amt)
        .toString(16)
        .padStart(2, "0"),
    )
    .join("")}`;
}

function mkCenterSectors(
  angles: number[],
  values: number[],
  maxR: number,
  colorFn: (i: number) => string,
) {
  const N = angles.length;
  return values.map((v, i) => {
    const next = (i + 1) % N;
    const p1 = polar(angles[i], maxR * clamp01(v));
    const p2 = polar(angles[next], maxR * clamp01(values[next] ?? 0));
    return {
      path: `M ${CX},${CY} L ${p1.x},${p1.y} L ${p2.x},${p2.y} Z`,
      color: colorFn(i),
    };
  });
}

function mkRingSectors(
  angles: number[],
  values: number[],
  baseR: number,
  maxR: number,
  colorFn: (i: number) => string,
  lightenAmt: number,
) {
  const N = angles.length;
  const span = maxR - baseR;
  return values.map((v, i) => {
    const next = (i + 1) % N;
    const r1 = baseR + span * clamp01(v);
    const r2 = baseR + span * clamp01(values[next] ?? 0);
    const d1 = polar(angles[i], r1);
    const d2 = polar(angles[next], r2);
    const b1 = polar(angles[i], baseR);
    const b2 = polar(angles[next], baseR);
    return {
      path: `M ${b1.x},${b1.y} L ${d1.x},${d1.y} L ${d2.x},${d2.y} L ${b2.x},${b2.y} Z`,
      color: lightenAmt > 0 ? lighten(colorFn(i), lightenAmt) : colorFn(i),
    };
  });
}

function centerOutline(angles: number[], values: number[], maxR: number): string {
  const pts = angles.map((a, i) => {
    const p = polar(a, maxR * clamp01(values[i] ?? 0));
    return `${p.x},${p.y}`;
  });
  return `M ${pts.join(" L ")} Z`;
}

function ringOutline(angles: number[], values: number[], baseR: number, maxR: number): string {
  const span = maxR - baseR;
  const pts = angles.map((a, i) => {
    const r = baseR + span * clamp01(values[i] ?? 0);
    const p = polar(a, r);
    return `${p.x},${p.y}`;
  });
  return `M ${pts.join(" L ")} Z`;
}

/* ── Component ───────────────────────────────────────────────────── */

export function DimensionSunburst({
  size = 300,
  onUpgrade,
}: DimensionSunburstProps) {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { state } = useDimensions(isTr ? "tr" : "en");
  const { canSeeDimensionLayer } = useM3Gate();

  const canSeeCog = canSeeDimensionLayer("cognition");
  const canSeeNeuro = canSeeDimensionLayer("neuroscience");

  const [tip, setTip] = useState<{
    x: number;
    y: number;
    name: string;
    value: number;
    locked: boolean;
  } | null>(null);

  const d6 = state.psychology;
  const d12 = state.cognition;
  const d24 = state.neuroscience;

  const sectors6D = useMemo(
    () => mkCenterSectors(ANGLES_6D, d6, R6_MAX, colorOf6D),
    [d6],
  );
  const sectors12D = useMemo(
    () => mkRingSectors(ANGLES_12D, d12, R12_BASE, R12_MAX, (i) => colorOf6D(PARENT_6D_OF_12D[i]), 0.15),
    [d12],
  );
  const sectors24D = useMemo(
    () => mkRingSectors(ANGLES_24D, d24, R24_BASE, R24_MAX, (i) => colorOf6D(PARENT_6D_OF_24D[i]), 0.25),
    [d24],
  );

  const path6D = useMemo(() => centerOutline(ANGLES_6D, d6, R6_MAX), [d6]);
  const path12D = useMemo(() => ringOutline(ANGLES_12D, d12, R12_BASE, R12_MAX), [d12]);
  const path24D = useMemo(() => ringOutline(ANGLES_24D, d24, R24_BASE, R24_MAX), [d24]);

  const onHover = useCallback(
    (e: React.MouseEvent<SVGElement>, name: string, value: number, locked: boolean) => {
      const svg = e.currentTarget.closest("svg")!;
      const rect = svg.getBoundingClientRect();
      setTip({
        x: ((e.clientX - rect.left) / rect.width) * VB,
        y: ((e.clientY - rect.top) / rect.height) * VB - 18,
        name,
        value,
        locked,
      });
    },
    [],
  );

  const offHover = useCallback(() => setTip(null), []);

  const isLockedGrid = (r: number) =>
    (r >= R12_BASE && r <= R12_MAX && !canSeeCog) ||
    (r >= R24_BASE && r <= R24_MAX && !canSeeNeuro);

  return (
    <div className="relative flex flex-col items-center">
      <svg
        width={size}
        height={size}
        viewBox={`0 0 ${VB} ${VB}`}
        className="overflow-visible"
      >
        <defs>
          <style>{`@keyframes dimFadeIn{from{opacity:0}to{opacity:1}}`}</style>
        </defs>

        {/* Grid circles */}
        {GRID_RADII.map((r) => (
          <circle
            key={r}
            cx={CX} cy={CY} r={r}
            fill="none"
            stroke={isLockedGrid(r) ? "rgba(255,255,255,0.03)" : "rgba(255,255,255,0.06)"}
            strokeWidth={
              r === R6_MAX || r === R12_BASE || r === R12_MAX || r === R24_BASE || r === R24_MAX
                ? 0.8 : 0.4
            }
            strokeDasharray={isLockedGrid(r) ? "4 3" : undefined}
          />
        ))}

        {/* 6D axis lines */}
        {ANGLES_6D.map((a, i) => {
          const end = polar(a, R6_MAX);
          return (
            <line key={`a6-${i}`} x1={CX} y1={CY} x2={end.x} y2={end.y}
              stroke="rgba(255,255,255,0.06)" strokeWidth={0.6}
            />
          );
        })}

        {/* 12D axis lines */}
        {ANGLES_12D.map((a, i) => {
          const s = polar(a, R12_BASE);
          const e = polar(a, R12_MAX);
          return (
            <line key={`a12-${i}`} x1={s.x} y1={s.y} x2={e.x} y2={e.y}
              stroke={canSeeCog ? "rgba(255,255,255,0.05)" : "rgba(255,255,255,0.02)"}
              strokeWidth={0.5}
              strokeDasharray={canSeeCog ? undefined : "3 3"}
            />
          );
        })}

        {/* 24D axis lines */}
        {ANGLES_24D.map((a, i) => {
          const s = polar(a, R24_BASE);
          const e = polar(a, R24_MAX);
          return (
            <line key={`a24-${i}`} x1={s.x} y1={s.y} x2={e.x} y2={e.y}
              stroke={canSeeNeuro ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.015)"}
              strokeWidth={0.4}
              strokeDasharray={canSeeNeuro ? undefined : "2 2"}
            />
          );
        })}

        {/* 24D data polygon */}
        {canSeeNeuro && (
          <g style={{ animation: "dimFadeIn 0.7s ease 0.4s both" }}>
            {sectors24D.map((s, i) => (
              <path key={i} d={s.path} fill={s.color} fillOpacity={0.2} />
            ))}
            <path d={path24D} fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth={0.8} />
          </g>
        )}

        {/* 12D data polygon */}
        {canSeeCog && (
          <g style={{ animation: "dimFadeIn 0.6s ease 0.2s both" }}>
            {sectors12D.map((s, i) => (
              <path key={i} d={s.path} fill={s.color} fillOpacity={0.25} />
            ))}
            <path d={path12D} fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth={1} />
          </g>
        )}

        {/* 6D data polygon */}
        <g style={{ animation: "dimFadeIn 0.5s ease both" }}>
          {sectors6D.map((s, i) => (
            <path key={i} d={s.path} fill={s.color} fillOpacity={0.35} />
          ))}
          <path d={path6D} fill="none" stroke="rgba(255,255,255,0.35)" strokeWidth={1.5} />
        </g>

        {/* Data dots — 6D */}
        {d6.map((v, i) => {
          const p = polar(ANGLES_6D[i], R6_MAX * clamp01(v));
          return (
            <circle
              key={`d6-${i}`} cx={p.x} cy={p.y} r={3.5}
              fill={colorOf6D(i)} stroke="#0a0a0f" strokeWidth={1}
              className="cursor-pointer"
              onMouseEnter={(e) =>
                onHover(e, isTr ? ALL_PSYCHOLOGY[i].nameTr : ALL_PSYCHOLOGY[i].name, v, false)
              }
              onMouseLeave={offHover}
            />
          );
        })}

        {/* Data dots — 12D */}
        {canSeeCog &&
          d12.map((v, i) => {
            const r = R12_BASE + (R12_MAX - R12_BASE) * clamp01(v);
            const p = polar(ANGLES_12D[i], r);
            return (
              <circle
                key={`d12-${i}`} cx={p.x} cy={p.y} r={2.5}
                fill={lighten(colorOf6D(PARENT_6D_OF_12D[i]), 0.15)}
                stroke="#0a0a0f" strokeWidth={0.8}
                className="cursor-pointer"
                onMouseEnter={(e) =>
                  onHover(e, isTr ? ALL_COGNITION[i].nameTr : ALL_COGNITION[i].name, v, false)
                }
                onMouseLeave={offHover}
              />
            );
          })}

        {/* Data dots — 24D */}
        {canSeeNeuro &&
          d24.map((v, i) => {
            const r = R24_BASE + (R24_MAX - R24_BASE) * clamp01(v);
            const p = polar(ANGLES_24D[i], r);
            return (
              <circle
                key={`d24-${i}`} cx={p.x} cy={p.y} r={2}
                fill={lighten(colorOf6D(PARENT_6D_OF_24D[i]), 0.25)}
                stroke="#0a0a0f" strokeWidth={0.6}
                className="cursor-pointer"
                onMouseEnter={(e) =>
                  onHover(e, isTr ? ALL_NEUROSCIENCE[i].nameTr : ALL_NEUROSCIENCE[i].name, v, false)
                }
                onMouseLeave={offHover}
              />
            );
          })}

        {/* Locked axis hover targets */}
        {!canSeeCog &&
          ANGLES_12D.map((a, i) => {
            const p = polar(a, (R12_BASE + R12_MAX) / 2);
            return (
              <circle
                key={`lk12-${i}`} cx={p.x} cy={p.y} r={8}
                fill="transparent" className="cursor-pointer"
                onMouseEnter={(e) =>
                  onHover(e, isTr ? ALL_COGNITION[i].nameTr : ALL_COGNITION[i].name, 0, true)
                }
                onMouseLeave={offHover}
                onClick={onUpgrade}
              />
            );
          })}
        {!canSeeNeuro &&
          ANGLES_24D.map((a, i) => {
            const p = polar(a, (R24_BASE + R24_MAX) / 2);
            return (
              <circle
                key={`lk24-${i}`} cx={p.x} cy={p.y} r={6}
                fill="transparent" className="cursor-pointer"
                onMouseEnter={(e) =>
                  onHover(e, isTr ? ALL_NEUROSCIENCE[i].nameTr : ALL_NEUROSCIENCE[i].name, 0, true)
                }
                onMouseLeave={offHover}
                onClick={onUpgrade}
              />
            );
          })}

        {/* 6D axis labels */}
        {ALL_PSYCHOLOGY.map((dim, i) => {
          const p = polar(ANGLES_6D[i], R6_LABEL);
          return (
            <text
              key={`lbl6-${i}`} x={p.x} y={p.y}
              textAnchor="middle" dominantBaseline="middle"
              fill={colorOf6D(i)} fontSize={9} fontWeight="600"
              fontFamily="var(--font-display)"
              style={{ pointerEvents: "none" }}
            >
              {isTr ? dim.nameTr : dim.name}
            </text>
          );
        })}

        {/* 12D axis labels */}
        {ALL_COGNITION.map((dim, i) => {
          const p = polar(ANGLES_12D[i], R12_LABEL);
          const name = (isTr ? dim.nameTr : dim.name).split(" ")[0];
          return (
            <text
              key={`lbl12-${i}`} x={p.x} y={p.y}
              textAnchor="middle" dominantBaseline="middle"
              fill={canSeeCog ? `${colorOf6D(PARENT_6D_OF_12D[i])}88` : "rgba(255,255,255,0.08)"}
              fontSize={6.5} fontFamily="var(--font-mono)"
              style={{ pointerEvents: "none" }}
            >
              {name}
            </text>
          );
        })}

        {/* Lock icons */}
        {!canSeeCog && (
          <foreignObject x={CX - 8} y={CY - (R12_BASE + R12_MAX) / 2 - 8} width={16} height={16}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 16, height: 16 }}>
              <Lock size={11} color="rgba(255,255,255,0.3)" />
            </div>
          </foreignObject>
        )}
        {!canSeeNeuro && (
          <foreignObject x={CX - 8} y={CY - (R24_BASE + R24_MAX) / 2 - 8} width={16} height={16}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center", width: 16, height: 16 }}>
              <Lock size={11} color="rgba(255,255,255,0.3)" />
            </div>
          </foreignObject>
        )}

        {/* Tooltip */}
        {tip && (
          <g style={{ pointerEvents: "none" }}>
            <rect x={tip.x - 58} y={tip.y - 12} width={116} height={20} rx={6}
              fill="rgba(0,0,0,0.88)" stroke="rgba(255,255,255,0.08)" strokeWidth={0.5}
            />
            <text x={tip.x} y={tip.y + 1} textAnchor="middle" dominantBaseline="middle"
              fill={tip.locked ? "rgba(255,255,255,0.4)" : "rgba(255,255,255,0.8)"}
              fontSize={8} fontFamily="var(--font-mono)"
            >
              {tip.locked
                ? `\uD83D\uDD12 ${tip.name}`
                : `${tip.name} ${Math.round(tip.value * 100)}%`}
            </text>
          </g>
        )}
      </svg>

      {/* Upgrade CTA */}
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
