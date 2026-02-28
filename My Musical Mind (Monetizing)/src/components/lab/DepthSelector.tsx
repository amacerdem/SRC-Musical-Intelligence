/* ── DepthSelector — 6D | 12D | 24D segmented toggle ────────────────── */

import { motion } from "framer-motion";
import type { DepthLevel } from "@/stores/useLabStore";

const DEPTHS: { value: DepthLevel; label: string; sub: string }[] = [
  { value: 6,  label: "6D",  sub: "Experiential" },
  { value: 12, label: "12D", sub: "Cognitive" },
  { value: 24, label: "24D", sub: "Neuroscience" },
];

interface Props {
  depth: DepthLevel;
  onChange: (d: DepthLevel) => void;
  accentColor: string;
}

export function DepthSelector({ depth, onChange, accentColor }: Props) {
  return (
    <div className="flex items-center gap-1 p-1 rounded-xl" style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}>
      {DEPTHS.map(({ value, label, sub }) => {
        const active = depth === value;
        return (
          <button
            key={value}
            onClick={() => onChange(value)}
            className="relative px-4 py-2 rounded-lg transition-all duration-300 flex flex-col items-center gap-0.5"
          >
            {active && (
              <motion.div
                layoutId="depth-bg"
                className="absolute inset-0 rounded-lg"
                style={{
                  background: `${accentColor}15`,
                  border: `1px solid ${accentColor}25`,
                  boxShadow: `0 0 16px ${accentColor}10`,
                }}
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
            <span
              className={`relative z-10 text-sm font-mono font-bold transition-colors duration-300 ${active ? "" : "text-slate-600"}`}
              style={active ? { color: accentColor } : undefined}
            >
              {label}
            </span>
            <span
              className={`relative z-10 text-[9px] font-display tracking-wider uppercase transition-colors duration-300 ${active ? "" : "text-slate-700"}`}
              style={active ? { color: `${accentColor}90` } : undefined}
            >
              {sub}
            </span>
          </button>
        );
      })}
    </div>
  );
}
