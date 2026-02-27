/* ── CongratsAnimation — Tier-specific celebration overlay ──── */

import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { Sparkles, Crown, Brain } from "lucide-react";

interface Props {
  tier: "basic" | "premium" | "ultimate" | null;
  accentColor: string;
  isVisible: boolean;
  onDismiss: () => void;
}

const TIER_CONFIG = {
  basic: { icon: Brain, particles: 6, burstScale: 1.2, label: "Basic" },
  premium: { icon: Sparkles, particles: 12, burstScale: 1.5, label: "Plus" },
  ultimate: { icon: Crown, particles: 20, burstScale: 2.0, label: "Pro" },
};

export function CongratsAnimation({ tier, accentColor, isVisible, onDismiss }: Props) {
  const { t } = useTranslation();
  if (!tier) return null;
  const config = TIER_CONFIG[tier];
  const Icon = config.icon;

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.4 }}
          className="fixed inset-0 z-[70] flex items-center justify-center"
          onClick={onDismiss}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />

          {/* Radial burst */}
          <motion.div
            className="absolute inset-0"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 0.25, 0] }}
            transition={{ duration: 2.5, ease: "easeOut" }}
            style={{
              background: `radial-gradient(circle at center, ${accentColor}30, transparent 60%)`,
            }}
          />

          {/* Floating particles */}
          {Array.from({ length: config.particles }).map((_, i) => {
            const angle = (i / config.particles) * Math.PI * 2;
            const dist = 80 + Math.random() * 60;
            return (
              <motion.div
                key={i}
                className="absolute w-1.5 h-1.5 rounded-full"
                style={{ backgroundColor: accentColor, left: "50%", top: "50%" }}
                initial={{ x: 0, y: 0, opacity: 0, scale: 0 }}
                animate={{
                  x: Math.cos(angle) * dist,
                  y: Math.sin(angle) * dist,
                  opacity: [0, 0.8, 0],
                  scale: [0, 1.5, 0],
                }}
                transition={{
                  duration: 2,
                  delay: 0.3 + i * 0.05,
                  ease: "easeOut",
                }}
              />
            );
          })}

          {/* Center content */}
          <motion.div
            className="relative text-center z-10"
            initial={{ opacity: 0, scale: 0.7 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: [0, 1.3, 1] }}
              transition={{ duration: 0.8, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
              className="mx-auto mb-4"
            >
              <Icon
                size={48}
                style={{
                  color: accentColor,
                  filter: `drop-shadow(0 0 20px ${accentColor})`,
                }}
              />
            </motion.div>

            <motion.h2
              className="text-2xl font-display font-bold mb-2"
              style={{
                color: accentColor,
                textShadow: `0 0 20px ${accentColor}60`,
              }}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4, duration: 0.6 }}
            >
              {t("m3.congrats.title")}
            </motion.h2>

            <motion.p
              className="text-sm text-slate-400 font-display font-light max-w-xs mx-auto"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.6 }}
            >
              {t("m3.congrats.message", { tier: config.label })}
            </motion.p>

            <motion.p
              className="text-[10px] text-slate-600 font-display mt-4"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 1.2, duration: 0.6 }}
            >
              {t("m3.congrats.tapToDismiss")}
            </motion.p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
