/* ── LayerToggles — Floating layer visibility controls ──────────────
 *  Positioned top-right of the LayeredScope. Glass-pill style with
 *  colored dots per layer. Expand/collapse secondary toggles.
 *  ──────────────────────────────────────────────────────────────────── */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, ChevronUp } from "lucide-react";

/* ── Types ───────────────────────────────────────────────────────────── */

export interface LayerState {
  peaks: boolean;
  bloom: boolean;
  curves: boolean;
  reward: boolean;
  neuro: boolean;
  grid: boolean;
}

export const DEFAULT_LAYERS: LayerState = {
  peaks: true,
  bloom: true,
  curves: true,
  reward: false,
  neuro: false,
  grid: true,
};

interface Props {
  layers: LayerState;
  onToggle: (key: keyof LayerState) => void;
}

/* ── Layer definitions ──────────────────────────────────────────────── */

interface LayerDef {
  key: keyof LayerState;
  label: string;
  color: string;
  primary: boolean;
}

const LAYER_DEFS: LayerDef[] = [
  { key: "peaks",  label: "Peaks",  color: "#60a5fa", primary: true },
  { key: "curves", label: "Curves", color: "#34d399", primary: true },
  { key: "bloom",  label: "Bloom",  color: "#fbbf24", primary: true },
  { key: "grid",   label: "Grid",   color: "#64748b", primary: false },
  { key: "reward", label: "Reward", color: "#ffc864", primary: false },
  { key: "neuro",  label: "Neuro",  color: "#a78bfa", primary: false },
];

/* ── Component ──────────────────────────────────────────────────────── */

export function LayerToggles({ layers, onToggle }: Props) {
  const [expanded, setExpanded] = useState(false);

  const primary = LAYER_DEFS.filter((d) => d.primary);
  const secondary = LAYER_DEFS.filter((d) => !d.primary);

  return (
    <div
      className="absolute top-2 right-2 z-30 select-none"
      style={{
        background: "rgba(6,6,14,0.85)",
        backdropFilter: "blur(20px)",
        border: "1px solid rgba(255,255,255,0.07)",
        borderRadius: 12,
        padding: "6px 8px",
        boxShadow: "0 4px 20px rgba(0,0,0,0.4)",
      }}
    >
      {/* Primary toggles */}
      <div className="flex items-center gap-1">
        {primary.map((def) => (
          <TogglePill
            key={def.key}
            def={def}
            active={layers[def.key]}
            onToggle={() => onToggle(def.key)}
          />
        ))}
        <button
          onClick={() => setExpanded(!expanded)}
          className="ml-0.5 p-1 rounded-md hover:bg-white/5 transition-colors"
          style={{ color: "rgba(255,255,255,0.3)" }}
        >
          {expanded ? <ChevronUp size={10} /> : <ChevronDown size={10} />}
        </button>
      </div>

      {/* Secondary toggles (collapsible) */}
      <AnimatePresence>
        {expanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.15 }}
            className="overflow-hidden"
          >
            <div className="flex items-center gap-1 mt-1 pt-1 border-t border-white/[0.05]">
              {secondary.map((def) => (
                <TogglePill
                  key={def.key}
                  def={def}
                  active={layers[def.key]}
                  onToggle={() => onToggle(def.key)}
                />
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

/* ── TogglePill ─────────────────────────────────────────────────────── */

function TogglePill({
  def, active, onToggle,
}: { def: LayerDef; active: boolean; onToggle: () => void }) {
  return (
    <button
      onClick={onToggle}
      className="flex items-center gap-1.5 px-2 py-1 rounded-lg text-[9px] font-mono transition-all"
      style={{
        background: active ? `${def.color}15` : "transparent",
        color: active ? def.color : "rgba(255,255,255,0.25)",
        fontWeight: active ? 600 : 400,
      }}
    >
      <span
        className="w-1.5 h-1.5 rounded-full transition-opacity"
        style={{
          backgroundColor: def.color,
          opacity: active ? 1 : 0.25,
        }}
      />
      {def.label}
    </button>
  );
}
