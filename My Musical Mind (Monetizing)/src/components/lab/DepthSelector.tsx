/* ── DepthSelector — 6D | 12D | 24D compact segmented toggle ──────── */

import { motion } from "framer-motion";
import type { DepthLevel } from "@/stores/useLabStore";

const DEPTHS: { value: DepthLevel; label: string }[] = [
  { value: 6,  label: "6D" },
  { value: 12, label: "12D" },
  { value: 24, label: "24D" },
];

interface Props {
  depth: DepthLevel;
  onChange: (d: DepthLevel) => void;
  accentColor: string;
}

export function DepthSelector({ depth, onChange, accentColor }: Props) {
  return (
    <div className="flex items-center gap-0.5 p-0.5 rounded-lg" style={{ background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.06)" }}>
      {DEPTHS.map(({ value, label }) => {
        const active = depth === value;
        return (
          <button
            key={value}
            onClick={() => onChange(value)}
            className="relative px-3 py-1 rounded-md transition-all duration-300"
          >
            {active && (
              <motion.div
                layoutId="depth-bg"
                className="absolute inset-0 rounded-md"
                style={{
                  background: `${accentColor}15`,
                  border: `1px solid ${accentColor}25`,
                }}
                transition={{ type: "spring", stiffness: 400, damping: 30 }}
              />
            )}
            <span
              className={`relative z-10 text-[11px] font-mono font-semibold transition-colors duration-300 ${active ? "" : "text-slate-600"}`}
              style={active ? { color: accentColor } : undefined}
            >
              {label}
            </span>
          </button>
        );
      })}
    </div>
  );
}
