/* ── AnalysisSummary — dominant dimension, gene profile, F1-F9 ──────── */

import { motion } from "framer-motion";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { DepthLevel } from "@/stores/useLabStore";
import {
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  ALL_NEUROSCIENCE,
  PSYCHOLOGY_COLORS,
} from "@/data/dimensions";
import type { DimensionKey6D } from "@/types/dimensions";

interface Props {
  detail: MITrackDetail;
  depth: DepthLevel;
  accentColor: string;
}

export function AnalysisSummary({ detail, depth, accentColor }: Props) {
  const dims =
    depth === 6
      ? detail.dimensions.psychology_6d
      : depth === 12
        ? detail.dimensions.cognition_12d
        : detail.dimensions.neuroscience_24d;

  const nodes =
    depth === 6
      ? ALL_PSYCHOLOGY
      : depth === 12
        ? ALL_COGNITION
        : ALL_NEUROSCIENCE;

  // Find dominant & weakest
  let maxIdx = 0, minIdx = 0;
  for (let i = 1; i < dims.length; i++) {
    if (dims[i] > dims[maxIdx]) maxIdx = i;
    if (dims[i] < dims[minIdx]) minIdx = i;
  }
  const dominant = nodes[maxIdx];
  const weakest = nodes[minIdx];

  const dominantColor =
    depth === 6
      ? PSYCHOLOGY_COLORS[dominant.key as DimensionKey6D] ?? accentColor
      : accentColor;

  return (
    <div className="flex items-center gap-4 flex-wrap">
      {/* Dominant dimension */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
        style={{ background: `${dominantColor}12`, border: `1px solid ${dominantColor}20` }}
      >
        <div className="w-2 h-2 rounded-full" style={{ background: dominantColor }} />
        <span className="text-[10px] font-display text-slate-500 uppercase tracking-wider">Dominant</span>
        <span className="text-xs font-display font-medium" style={{ color: dominantColor }}>
          {dominant.name}
        </span>
        <span className="text-xs font-mono" style={{ color: `${dominantColor}90` }}>
          {Math.round(dims[maxIdx] * 100)}%
        </span>
      </motion.div>

      {/* Weakest dimension */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        className="flex items-center gap-2 px-3 py-1.5 rounded-lg"
        style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}
      >
        <span className="text-[10px] font-display text-slate-600 uppercase tracking-wider">Weakest</span>
        <span className="text-xs font-display text-slate-500">{weakest.name}</span>
        <span className="text-xs font-mono text-slate-600">{Math.round(dims[minIdx] * 100)}%</span>
      </motion.div>

      {/* Gene family badge */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg"
        style={{ background: `${accentColor}08`, border: `1px solid ${accentColor}12` }}
      >
        <span className="text-[10px] font-display text-slate-600 uppercase tracking-wider">Family</span>
        <span className="text-xs font-display font-medium" style={{ color: `${accentColor}90` }}>
          {detail.dominant_family}
        </span>
      </motion.div>

      {/* F1-F9 mini overview */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="flex items-center gap-1"
      >
        {Object.entries(detail.functions).map(([fn, val]) => (
          <div
            key={fn}
            className="flex flex-col items-center gap-0.5"
            title={`${fn}: ${Math.round((val as number) * 100)}%`}
          >
            <div
              className="w-3 rounded-sm"
              style={{
                height: Math.max(4, (val as number) * 20),
                background: accentColor,
                opacity: 0.3 + (val as number) * 0.5,
              }}
            />
            <span className="text-[7px] font-mono text-slate-700">{fn}</span>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
