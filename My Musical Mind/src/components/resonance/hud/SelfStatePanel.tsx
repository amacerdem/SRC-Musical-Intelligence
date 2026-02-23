/* ── SelfStatePanel — Your 5 beliefs mini-bars (bottom center) ──── */

import { motion } from "framer-motion";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { useUserStore } from "@/stores/useUserStore";
import { beliefColors } from "@/design/tokens";

const ease = [0.22, 1, 0.36, 1] as const;

const BELIEFS = [
  { key: "consonance" as const, label: "CON" },
  { key: "tempo" as const, label: "TMP" },
  { key: "salience" as const, label: "SAL" },
  { key: "familiarity" as const, label: "FAM" },
  { key: "reward" as const, label: "RWD" },
];

function getSelfBeliefs() {
  const mind = useUserStore.getState().mind;
  if (!mind) return [0.5, 0.5, 0.5, 0.5, 0.5];
  const a = mind.axes;
  return [
    1 - a.entropyTolerance,
    a.tensionAppetite,
    a.salienceSensitivity,
    a.monotonyTolerance,
    a.resolutionCraving,
  ];
}

export function SelfStatePanel() {
  const entranceComplete = useResonanceStore(s => s.entranceComplete);
  const beliefs = getSelfBeliefs();

  if (!entranceComplete) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease, delay: 0.6 }}
      className="fixed bottom-20 left-1/2 -translate-x-1/2 z-[45]"
    >
      <div className="glass px-5 py-3 rounded-2xl flex items-center gap-4">
        <span className="text-[8px] font-display uppercase tracking-[0.2em] text-white/25 mr-1">
          Your State
        </span>
        {BELIEFS.map((b, i) => (
          <div key={b.key} className="flex flex-col items-center gap-1">
            <div className="w-12 h-1 rounded-full bg-white/[0.04] overflow-hidden">
              <motion.div
                className="h-full rounded-full"
                style={{ background: beliefColors[b.key].primary }}
                initial={{ width: 0 }}
                animate={{ width: `${beliefs[i] * 100}%` }}
                transition={{ duration: 1.2, ease, delay: 0.8 + i * 0.1 }}
              />
            </div>
            <span
              className="text-[7px] font-mono tracking-wider"
              style={{ color: `${beliefColors[b.key].primary}60` }}
            >
              {b.label}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
