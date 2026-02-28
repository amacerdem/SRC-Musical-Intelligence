/* ── AnalysisSummary — dominant dimension, gene profile, F1-F9 ──────── */

import { motion } from "framer-motion";
import type { MITrackDetail } from "@/types/mi-dataset";
import type { DepthLevel } from "@/stores/useLabStore";
import type { TemporalDimensions } from "@/stores/useLabStore";
import { getLabDim } from "@/data/dimensions";

interface Props {
  detail: MITrackDetail;
  depth: DepthLevel;
  accentColor: string;
  temporal: TemporalDimensions;
}

export function AnalysisSummary({ detail, depth, accentColor, temporal }: Props) {
  const dims =
    depth === 6
      ? temporal.overall.psychology
      : depth === 12
        ? temporal.overall.cognition
        : temporal.overall.neuroscience;

  // Find dominant & weakest
  let maxIdx = 0, minIdx = 0;
  for (let i = 1; i < dims.length; i++) {
    if (dims[i] > dims[maxIdx]) maxIdx = i;
    if (dims[i] < dims[minIdx]) minIdx = i;
  }
  const dominant = getLabDim(depth, maxIdx);
  const weakest = getLabDim(depth, minIdx);
  const dominantColor = dominant?.color ?? accentColor;

  return (
    <div className="flex flex-col gap-1.5">
      {/* Dominant dimension */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2, duration: 0.6 }}
        className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg"
        style={{ background: `${dominantColor}12`, border: `1px solid ${dominantColor}20` }}
      >
        <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ background: dominantColor }} />
        <span className="text-[9px] font-display text-slate-500 uppercase tracking-wider">Dom</span>
        <span className="text-[11px] font-display font-medium truncate" style={{ color: dominantColor }}>
          {dominant?.name ?? ""}
        </span>
        <span className="text-[10px] font-mono ml-auto flex-shrink-0" style={{ color: `${dominantColor}90` }}>
          {Math.round(dims[maxIdx] * 100)}%
        </span>
      </motion.div>

      {/* Weakest dimension */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: 0.6 }}
        className="flex items-center gap-2 px-2.5 py-1.5 rounded-lg"
        style={{ background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.06)" }}
      >
        <span className="text-[9px] font-display text-slate-600 uppercase tracking-wider">Low</span>
        <span className="text-[11px] font-display text-slate-500 truncate">{weakest?.name ?? ""}</span>
        <span className="text-[10px] font-mono text-slate-600 ml-auto flex-shrink-0">{Math.round(dims[minIdx] * 100)}%</span>
      </motion.div>

      {/* Gene family badge */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg"
        style={{ background: `${accentColor}08`, border: `1px solid ${accentColor}12` }}
      >
        <span className="text-[9px] font-display text-slate-600 uppercase tracking-wider">Family</span>
        <span className="text-[11px] font-display font-medium truncate" style={{ color: `${accentColor}90` }}>
          {detail.dominant_family}
        </span>
      </motion.div>

      {/* F1-F9 mini overview — horizontal strip */}
      <motion.div
        initial={{ opacity: 0, y: 6 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.6 }}
        className="flex items-end gap-0.5 px-1 pt-1"
      >
        {Object.entries(detail.functions).map(([fn, val]) => (
          <div
            key={fn}
            className="flex flex-col items-center gap-0.5 flex-1"
            title={`${fn}: ${Math.round((val as number) * 100)}%`}
          >
            <div
              className="w-full max-w-[14px] rounded-sm"
              style={{
                height: Math.max(4, (val as number) * 20),
                background: accentColor,
                opacity: 0.3 + (val as number) * 0.5,
              }}
            />
            <span className="text-[6px] font-mono text-slate-700">{fn}</span>
          </div>
        ))}
      </motion.div>
    </div>
  );
}
