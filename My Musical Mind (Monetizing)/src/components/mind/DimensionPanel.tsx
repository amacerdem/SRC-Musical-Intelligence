/* ── DimensionPanel — Tier-gated multi-layer dimension display ────
 *  Shows dimension values at the user's accessible tier:
 *    Free     → 6D psychology bars
 *    Basic    → 6D + 12D cognition expandable
 *    Premium  → 6D + 12D + 24D neuroscience tree
 *    Ultimate → 6D + 12D + 24D + research badge
 *
 *  Each layer shows dimension names + bar visualizations.
 *  Locked layers show a blurred preview with upgrade CTA.
 *  ──────────────────────────────────────────────────────────────── */

import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";
import { useDimensions } from "@/hooks/useDimensions";
import { useM3Gate } from "@/hooks/useM3Gate";
import type { DimensionLayer } from "@/types/dimensions";
import {
  ALL_PSYCHOLOGY,
  ALL_COGNITION,
  COGNITION_DISPLAY_GROUPS,
  getLabDim,
} from "@/data/dimensions";

interface Props {
  /** Persona color for accent theming */
  accentColor?: string;
  /** Show compact single-layer view */
  compact?: boolean;
}

const LAYER_CONFIG: { key: DimensionLayer; label: string; labelTr: string; count: number }[] = [
  { key: "psychology",   label: "Psychology",   labelTr: "Psikoloji",     count: 6 },
  { key: "cognition",    label: "Cognition",    labelTr: "Müzik Bilişi",  count: 12 },
  { key: "neuroscience", label: "Neuroscience", labelTr: "Nörobilim",     count: 24 },
];

export function DimensionPanel({ accentColor = "#A855F7", compact = false }: Props) {
  const { t, i18n } = useTranslation();
  const isTr = i18n.language === "tr";
  const { state, canSeeLayer, names } = useDimensions(isTr ? "tr" : "en");
  const { canSeeDimensionLayer } = useM3Gate();
  const [expandedLayer, setExpandedLayer] = useState<DimensionLayer | null>(
    compact ? null : "psychology",
  );

  const toggleLayer = (layer: DimensionLayer) => {
    if (!canSeeDimensionLayer(layer)) return;
    setExpandedLayer((prev) => (prev === layer ? null : layer));
  };

  const getLayerValues = (layer: DimensionLayer): number[] => {
    switch (layer) {
      case "psychology":   return state.psychology;
      case "cognition":    return state.cognition;
      case "neuroscience": return state.neuroscience;
      default:             return [];
    }
  };

  const getLayerNames = (layer: DimensionLayer): string[] => {
    switch (layer) {
      case "psychology":   return names.psychology;
      case "cognition":    return names.cognition;
      case "neuroscience": return names.neuroscience;
      default:             return [];
    }
  };

  return (
    <div className="space-y-2">
      {LAYER_CONFIG.map(({ key, label, labelTr, count }) => {
        const isAccessible = canSeeDimensionLayer(key);
        const isExpanded = expandedLayer === key;
        const layerValues = getLayerValues(key);
        const layerNames = getLayerNames(key);

        return (
          <div key={key} className="rounded-xl overflow-hidden" style={{
            background: "rgba(14, 14, 22, 0.4)",
            border: `1px solid ${isAccessible ? "rgba(255,255,255,0.05)" : "rgba(255,255,255,0.02)"}`,
          }}>
            {/* Layer header */}
            <button
              onClick={() => toggleLayer(key)}
              className="w-full flex items-center justify-between px-4 py-3 transition-colors"
              style={{ opacity: isAccessible ? 1 : 0.4 }}
            >
              <div className="flex items-center gap-2">
                <span
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: isAccessible ? accentColor : "#475569" }}
                />
                <span className="text-sm font-medium text-slate-300">
                  {isTr ? labelTr : label}
                </span>
                <span className="text-[10px] text-slate-600 font-mono">{count}D</span>
              </div>
              <div className="flex items-center gap-2">
                {!isAccessible && (
                  <span className="text-[9px] text-slate-600 bg-white/5 px-2 py-0.5 rounded-full">
                    {key === "cognition" ? "Basic+" : key === "neuroscience" ? "Premium+" : ""}
                  </span>
                )}
                <span className="text-slate-600 text-xs">
                  {isExpanded ? "−" : "+"}
                </span>
              </div>
            </button>

            {/* Expanded content */}
            <AnimatePresence>
              {isExpanded && isAccessible && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.3, ease: "easeInOut" }}
                  className="overflow-hidden"
                >
                  <div className="px-4 pb-3 space-y-1.5">
                    {layerValues.map((val, i) => {
                      const dimName = layerNames[i] ?? `D${i}`;
                      const depth = key === "psychology" ? 6 : key === "cognition" ? 12 : 24;
                      const dim = getLabDim(depth as 6 | 12 | 24, i);
                      const barColor = dim?.color ?? accentColor;

                      return (
                        <div key={i} className="flex items-center gap-2">
                          <div className="w-24 text-[9px] text-slate-500 truncate" title={dimName}>
                            {dimName}
                          </div>
                          <div className="flex-1 h-[3px] rounded-full bg-white/[0.03] overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${Math.min(100, Math.abs(val) * 100)}%` }}
                              transition={{ duration: 0.6, delay: i * 0.03 }}
                              className="h-full rounded-full"
                              style={{ backgroundColor: barColor, opacity: 0.6 }}
                            />
                          </div>
                          <div className="w-8 text-right text-[9px] text-slate-600 font-mono">
                            {(val * 100).toFixed(0)}
                          </div>
                        </div>
                      );
                    })}

                    {/* 12D: show parent grouping markers */}
                    {key === "cognition" && (
                      <div className="mt-2 flex flex-wrap gap-1">
                        {ALL_PSYCHOLOGY.map((psych) => {
                          const children = COGNITION_DISPLAY_GROUPS[psych.key];
                          if (!children) return null;
                          return (
                            <span
                              key={psych.key}
                              className="text-[8px] text-slate-600 bg-white/[0.03] px-1.5 py-0.5 rounded"
                            >
                              {isTr ? psych.nameTr : psych.name}: {children.map((c) => isTr ? c.nameTr : c.name).join(" + ")}
                            </span>
                          );
                        })}
                      </div>
                    )}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Locked blur preview */}
            {isExpanded && !isAccessible && (
              <div className="px-4 pb-3 relative">
                <div className="space-y-1.5 blur-sm pointer-events-none">
                  {Array.from({ length: Math.min(count, 6) }).map((_, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <div className="w-24 h-2 bg-white/5 rounded" />
                      <div className="flex-1 h-[3px] rounded-full bg-white/[0.03]">
                        <div
                          className="h-full rounded-full bg-white/10"
                          style={{ width: `${30 + Math.random() * 40}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-[10px] text-slate-500 bg-black/60 px-3 py-1 rounded-full backdrop-blur-sm">
                    Upgrade to unlock
                  </span>
                </div>
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
