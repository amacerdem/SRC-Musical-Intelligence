/* ── FieldHeader — "RESONANCE FIELD" + online count ─────────────── */

import { motion } from "framer-motion";
import { useResonanceStore } from "@/stores/useResonanceStore";

const ease = [0.22, 1, 0.36, 1] as const;

export function FieldHeader() {
  const users = useResonanceStore(s => s.users);
  const entranceComplete = useResonanceStore(s => s.entranceComplete);
  const onlineCount = users.length + 1; // +1 for self

  if (!entranceComplete) return null;

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8, ease, delay: 0.2 }}
      className="fixed top-20 left-6 z-[45] flex items-center gap-4"
    >
      <div className="flex flex-col gap-1">
        <span className="text-[10px] font-display font-medium uppercase tracking-[0.25em] text-white/40">
          Resonance Field
        </span>
        <div className="flex items-center gap-2">
          <span className="relative flex h-1.5 w-1.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-50" />
            <span className="relative inline-flex rounded-full h-1.5 w-1.5 bg-emerald-400" />
          </span>
          <span className="text-[9px] font-mono text-emerald-500/60 tracking-wider">
            {onlineCount} ONLINE
          </span>
        </div>
      </div>
    </motion.div>
  );
}
