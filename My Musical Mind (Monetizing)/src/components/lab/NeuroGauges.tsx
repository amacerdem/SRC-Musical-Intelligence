/* ── NeuroGauges — 4 neurochemical bar indicators ────────────────────── */

import { motion } from "framer-motion";

interface NeuroData {
  DA: number;
  NE: number;
  OPI: number;
  "5HT": number;
}

const NEURO_CONFIG = [
  { key: "DA"  as const, label: "Dopamine",       color: "#FBBF24" },
  { key: "NE"  as const, label: "Norepinephrine",  color: "#EF4444" },
  { key: "OPI" as const, label: "Opioid",          color: "#A855F7" },
  { key: "5HT" as const, label: "Serotonin",       color: "#38BDF8" },
];

interface Props {
  data: NeuroData | null;
}

export function NeuroGauges({ data }: Props) {
  if (!data) return null;

  return (
    <div className="flex items-center gap-4">
      {NEURO_CONFIG.map(({ key, label, color }, i) => {
        const value = data[key];
        const pct = Math.round(value * 100);
        return (
          <div key={key} className="flex-1 flex items-center gap-2">
            <span className="text-[9px] font-mono font-bold tracking-wider" style={{ color: `${color}90` }}>
              {key}
            </span>
            <div className="flex-1 h-[4px] rounded-full bg-white/5 overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ background: color, opacity: 0.7 }}
                initial={{ width: 0 }}
                animate={{ width: `${pct}%` }}
                transition={{ duration: 1, delay: 0.1 * i, ease: [0.22, 1, 0.36, 1] }}
              />
            </div>
            <span className="text-[10px] font-mono w-8 text-right" style={{ color: `${color}80` }}>
              {pct}%
            </span>
          </div>
        );
      })}
    </div>
  );
}
