/* ── SignalOverlay — Floating signal notifications ───────────────── */

import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";

const ease = [0.22, 1, 0.36, 1] as const;

const EMOTE_MAP: Record<string, string> = {
  wave: "👋",
  chills: "✨",
  vibe: "🌊",
  fire: "🔥",
  mind: "🧠",
  feel: "💜",
  sync: "🔗",
  peak: "⚡",
};

export function SignalOverlay() {
  const { t } = useTranslation();
  const signals = useResonanceStore(s => s.signals);
  const users = useResonanceStore(s => s.users);

  // Only show signals sent TO self, most recent 3
  const incomingSignals = signals
    .filter(s => s.to === "self")
    .slice(-3);

  return (
    <div className="fixed top-28 left-1/2 -translate-x-1/2 z-[46] flex flex-col items-center gap-2 pointer-events-none">
      <AnimatePresence>
        {incomingSignals.map(sig => {
          const sender = users.find(u => u.id === sig.from);
          const emoji = EMOTE_MAP[sig.type] ?? sig.content;
          const name = sender?.displayName ?? "Unknown";

          return (
            <motion.div
              key={sig.id}
              initial={{ opacity: 0, y: -20, scale: 0.8, filter: "blur(8px)" }}
              animate={{ opacity: 1, y: 0, scale: 1, filter: "blur(0px)" }}
              exit={{ opacity: 0, y: -15, scale: 0.9, filter: "blur(4px)" }}
              transition={{ duration: 0.5, ease }}
              className="glass px-4 py-2 rounded-full flex items-center gap-2"
            >
              <span className="text-sm">{emoji}</span>
              <span className="text-[9px] font-display text-white/50">
                {t("resonance.from")} <span className="text-white/70 font-medium">{name}</span>
              </span>
            </motion.div>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
