/* ── EntranceSequence — Cinematic reveal then unmount ────────────── */

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";

const ease = [0.22, 1, 0.36, 1] as const;

export function EntranceSequence() {
  const { t } = useTranslation();
  const completeEntrance = useResonanceStore(s => s.completeEntrance);
  const entranceComplete = useResonanceStore(s => s.entranceComplete);
  const [visible, setVisible] = useState(true);
  const [phase, setPhase] = useState<"title" | "fade">("title");

  useEffect(() => {
    const t1 = setTimeout(() => setPhase("fade"), 2800);
    const t2 = setTimeout(() => {
      setVisible(false);
      completeEntrance();
    }, 4000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [completeEntrance]);

  if (entranceComplete || !visible) return null;

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          initial={{ opacity: 1 }}
          animate={{ opacity: phase === "fade" ? 0 : 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1.2, ease }}
          className="fixed inset-0 z-[60] bg-black flex items-center justify-center pointer-events-none"
        >
          <div className="flex flex-col items-center gap-4">
            <motion.h1
              initial={{ opacity: 0, y: 50, filter: "blur(16px)" }}
              animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
              transition={{ duration: 1.2, ease, delay: 0.3 }}
              className="text-3xl md:text-5xl font-display font-light tracking-[0.3em] text-white/90"
            >
              {t("resonance.entranceTitle")}
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, ease, delay: 1.0 }}
              className="text-xs font-display tracking-[0.25em] text-slate-600 uppercase"
            >
              {t("resonance.entranceSub")}
            </motion.p>
            <motion.div
              initial={{ scaleX: 0 }}
              animate={{ scaleX: 1 }}
              transition={{ duration: 1.5, ease, delay: 0.6 }}
              className="w-32 h-px bg-gradient-to-r from-transparent via-purple-500/40 to-transparent"
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
