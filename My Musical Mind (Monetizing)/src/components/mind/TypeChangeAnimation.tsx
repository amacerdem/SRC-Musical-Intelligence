/* ── TypeChangeAnimation — Centered boom when Mind Type shifts ──── */

import { useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";

interface Props {
  isVisible: boolean;
  typeName: string;
  typeColor: string;
  onDismiss: () => void;
}

export function TypeChangeAnimation({ isVisible, typeName, typeColor, onDismiss }: Props) {
  const { t } = useTranslation();

  // Auto-dismiss after full animation (3.5s)
  useEffect(() => {
    if (!isVisible) return;
    const timer = setTimeout(onDismiss, 3500);
    return () => clearTimeout(timer);
  }, [isVisible, onDismiss]);

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.4 }}
          className="fixed inset-0 z-[60] flex items-center justify-center"
          style={{ pointerEvents: "none" }}
        >
          {/* Color pulse ring — full screen */}
          <motion.div
            className="absolute inset-0"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.2, 0.1, 0] }}
            transition={{ duration: 3, ease: "easeOut" }}
            style={{ background: `radial-gradient(circle at 50% 50%, ${typeColor}50, transparent 65%)` }}
          />

          {/* Type name reveal — absolutely centered */}
          <motion.div
            className="text-center z-10"
            initial={{ opacity: 0, scale: 0.7, y: 15 }}
            animate={{ opacity: [0, 1, 1, 0], scale: [0.7, 1.08, 1, 0.95], y: [15, 0, 0, -8] }}
            transition={{ duration: 3.2, times: [0, 0.15, 0.7, 1], ease: "easeOut" }}
          >
            <p className="text-sm font-display font-light tracking-[0.25em] uppercase text-slate-400 mb-2">
              {t("m3.hub.mindType")}
            </p>
            <h2
              className="text-4xl md:text-5xl font-display font-bold tracking-tight"
              style={{
                color: typeColor,
                textShadow: `0 0 40px ${typeColor}70, 0 0 80px ${typeColor}35, 0 0 120px ${typeColor}15`,
              }}
            >
              {typeName}
            </h2>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
