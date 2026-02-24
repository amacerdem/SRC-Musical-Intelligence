/* ── TypeChangeAnimation — Subtle boom when Mind Type shifts ──── */

import { motion, AnimatePresence } from "framer-motion";

interface Props {
  isVisible: boolean;
  typeName: string;
  typeColor: string;
  onDismiss: () => void;
}

export function TypeChangeAnimation({ isVisible, typeName, typeColor, onDismiss }: Props) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
          className="fixed inset-0 z-[60] flex items-center justify-center pointer-events-none"
          onAnimationComplete={(def) => {
            if (typeof def === "object" && "opacity" in def && def.opacity === 0) onDismiss();
          }}
        >
          {/* Color pulse ring */}
          <motion.div
            className="absolute inset-0"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.15, 0.08, 0] }}
            transition={{ duration: 2, ease: "easeOut" }}
            style={{ background: `radial-gradient(circle at center, ${typeColor}40, transparent 70%)` }}
            onAnimationComplete={onDismiss}
          />

          {/* Type name reveal */}
          <motion.div
            className="relative text-center"
            initial={{ opacity: 0, scale: 0.8, y: 10 }}
            animate={{ opacity: [0, 1, 1, 0], scale: [0.8, 1.05, 1, 0.95], y: [10, 0, 0, -5] }}
            transition={{ duration: 3, times: [0, 0.2, 0.7, 1], ease: "easeOut" }}
          >
            <p className="text-xs font-display font-light tracking-[0.2em] uppercase text-slate-400 mb-1">
              Mind Type
            </p>
            <h2
              className="text-3xl md:text-4xl font-display font-bold tracking-tight"
              style={{
                color: typeColor,
                textShadow: `0 0 30px ${typeColor}60, 0 0 60px ${typeColor}30`,
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
