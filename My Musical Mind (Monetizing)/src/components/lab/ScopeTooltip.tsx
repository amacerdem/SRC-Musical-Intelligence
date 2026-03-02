/* ── ScopeTooltip — Unified hover tooltip for LayeredScope ────────────
 *  Combines dimension curve data (from FlowOverlay) with spectral peak
 *  info (from PeakBuffers) into a single depth-layered tooltip.
 *
 *  Ported from FlowTimeline.tsx FlowTooltip + DimRow, extended with
 *  peak note information.
 *  ──────────────────────────────────────────────────────────────────── */

import { useMemo } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { DepthLevel } from "@/stores/useLabStore";
import type { LabMode } from "./FlowTimeline";

/* ── Types ───────────────────────────────────────────────────────────── */

export interface TooltipDim {
  name: string;
  value: number;
  color: string;
  parentName?: string;
}

export interface PeakInfo {
  freq: number;
  noteName: string;
  amplitude: number;
  rank: number;
}

export interface ScopeTooltipData {
  timeStr: string;
  dims: TooltipDim[];
  reward: number;
  neuro: number[];
  peak: PeakInfo | null;
  posX: number;       // canvas-space X
}

interface Props {
  data: ScopeTooltipData | null;
  depth: DepthLevel;
  accentColor: string;
  containerW: number;
  labMode: LabMode;
}

/* ── Constants ───────────────────────────────────────────────────────── */

const NEURO_LABELS = ["DA", "NE", "OPI", "5HT"] as const;
const NEURO_COLORS = ["#22C55E", "#EF4444", "#38BDF8", "#A855F7"] as const;

function baseHex(col: string): string {
  if (col.length === 9) return col.slice(0, 7);
  return col;
}

/* ── Component ──────────────────────────────────────────────────────── */

export function ScopeTooltip({ data, depth, accentColor, containerW, labMode }: Props) {
  return (
    <AnimatePresence>
      {data && (
        <ScopeTooltipInner
          data={data}
          depth={depth}
          accentColor={accentColor}
          containerW={containerW}
          labMode={labMode}
        />
      )}
    </AnimatePresence>
  );
}

function ScopeTooltipInner({ data, depth, accentColor, containerW, labMode }: {
  data: ScopeTooltipData;
  depth: DepthLevel;
  accentColor: string;
  containerW: number;
  labMode: LabMode;
}) {
  const isAcoustic = labMode === "acoustic";
  const tw = depth <= 6 ? 220 : depth <= 12 ? 260 : 340;

  // Edge-aware positioning
  let leftPct = (data.posX / containerW) * 100;
  const leftPx = (leftPct / 100) * containerW;
  if (leftPx < tw / 2 + 12) leftPct = ((tw / 2 + 12) / containerW) * 100;
  else if (leftPx > containerW - tw / 2 - 12) leftPct = ((containerW - tw / 2 - 12) / containerW) * 100;

  // Group dimensions by parent for 12D/24D
  const grouped = useMemo(() => {
    if (depth === 6) return null;
    const groups: { parentName: string; items: TooltipDim[] }[] = [];
    let cur = "";
    for (const d of data.dims) {
      const pn = d.parentName ?? "Other";
      if (pn !== cur) { cur = pn; groups.push({ parentName: pn, items: [] }); }
      groups[groups.length - 1].items.push(d);
    }
    return groups;
  }, [data.dims, depth]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 8 }}
      transition={{ duration: 0.1 }}
      className="absolute bottom-3 z-40 pointer-events-none"
      style={{ left: `${leftPct}%`, transform: "translateX(-50%)", width: tw }}
    >
      <div
        className="rounded-xl px-3 py-2.5"
        style={{
          background: isAcoustic ? "rgba(14,8,6,0.93)" : "rgba(6,6,14,0.93)",
          backdropFilter: "blur(20px)",
          border: "1px solid rgba(255,255,255,0.07)",
          boxShadow: `0 8px 32px rgba(0,0,0,0.55), 0 0 24px ${accentColor}06`,
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-mono text-slate-400">{data.timeStr}</span>
          {!isAcoustic && (
            <div className="flex items-center gap-1.5">
              <span className="text-[9px] font-mono text-slate-600 uppercase tracking-wider">Reward</span>
              <div className="w-14 h-[4px] rounded-full bg-white/5 overflow-hidden">
                <div className="h-full rounded-full" style={{ width: `${data.reward * 100}%`, background: accentColor, opacity: 0.65 }} />
              </div>
              <span className="text-[11px] font-mono" style={{ color: `${accentColor}90` }}>
                {data.reward.toFixed(2)}
              </span>
            </div>
          )}
        </div>

        {/* Peak info */}
        {data.peak && (
          <div className="mb-2 pb-2 border-b border-white/[0.05]">
            <div className="flex items-center gap-2">
              <span className="text-[10px] text-slate-500">&#9834;</span>
              <span className="text-[11px] font-mono text-slate-300 font-semibold">
                {data.peak.noteName}
              </span>
              <span className="text-[9px] font-mono text-slate-600">
                {data.peak.freq.toFixed(0)} Hz
              </span>
              <span className="flex-1" />
              <span className="text-[9px] font-mono text-slate-500">
                amp {data.peak.amplitude.toFixed(2)}
              </span>
            </div>
          </div>
        )}

        {/* Flat list (6D or Acoustic mode) */}
        {(depth === 6 || isAcoustic) && (
          <div className={`space-y-0.5 ${isAcoustic && depth === 24 ? "grid grid-cols-2 gap-x-2 gap-y-0 space-y-0" : ""}`}>
            {data.dims.map((d, i) => (
              <DimRow key={i} name={d.name} value={d.value} color={d.color} compact={isAcoustic && depth >= 12} />
            ))}
          </div>
        )}

        {/* 12D grouped (NeuroAcoustic) */}
        {!isAcoustic && depth === 12 && grouped && (
          <div className="space-y-1.5">
            {grouped.map((g, gi) => (
              <div key={gi}>
                <div className="text-[9px] font-display text-slate-600 uppercase tracking-wider mb-0.5">
                  {g.parentName}
                </div>
                {g.items.map((d, di) => (
                  <DimRow key={di} name={d.name} value={d.value} color={d.color} />
                ))}
              </div>
            ))}
          </div>
        )}

        {/* 24D compact 2-column grouped (NeuroAcoustic) */}
        {!isAcoustic && depth === 24 && grouped && (
          <div className="space-y-1">
            {grouped.map((g, gi) => (
              <div key={gi}>
                <div className="text-[9px] font-display text-slate-600 uppercase tracking-wider mb-0.5">
                  {g.parentName}
                </div>
                <div className="grid grid-cols-2 gap-x-2 gap-y-0">
                  {g.items.map((d, di) => (
                    <DimRow key={di} name={d.name} value={d.value} color={d.color} compact />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Neurochemicals (12D+ neuro mode) */}
        {!isAcoustic && depth >= 12 && (
          <div className="flex items-center gap-3 mt-2.5 pt-2 border-t border-white/[0.05]">
            {NEURO_LABELS.map((label, i) => (
              <div key={label} className="flex items-center gap-1">
                <div className="w-1.5 h-1.5 rounded-full" style={{ background: NEURO_COLORS[i] }} />
                <span className="text-[9px] font-mono text-slate-600">{label}</span>
                <span className="text-[10px] font-mono" style={{ color: NEURO_COLORS[i] + "90" }}>
                  {data.neuro[i]?.toFixed(2) ?? "0"}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}

/* ── DimRow — single dimension bar ──────────────────────────────────── */

function DimRow({ name, value, color, compact = false }: {
  name: string;
  value: number;
  color: string;
  compact?: boolean;
}) {
  return (
    <div className="flex items-center gap-1.5 py-[1px]">
      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: color }} />
      <span className={`${compact ? "text-[9px]" : "text-[11px]"} font-display text-slate-400 flex-1 truncate`}>
        {name}
      </span>
      <div className={`${compact ? "w-10" : "w-16"} h-[3px] rounded-full bg-white/5 flex-shrink-0 overflow-hidden`}>
        <div
          className="h-full rounded-full"
          style={{ width: `${value * 100}%`, background: color, opacity: 0.65 }}
        />
      </div>
      <span
        className={`${compact ? "text-[8px]" : "text-[10px]"} font-mono flex-shrink-0`}
        style={{ color: baseHex(color) + "90" }}
      >
        {value.toFixed(2)}
      </span>
    </div>
  );
}
