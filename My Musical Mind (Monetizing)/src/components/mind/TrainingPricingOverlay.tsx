/* ── TrainingPricingOverlay — Glassmorphism pricing for M³ training ── */

import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { X, Brain, Shield, Sparkles, Crown, Check } from "lucide-react";
import type { M3Tier } from "@/types/m3";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSelect: (tier: M3Tier) => void;
  accentColor: string;
}

const TIERS = ["basic", "plus", "pro"] as const;
type Tier = (typeof TIERS)[number];

const TIER_META: Record<Tier, { icon: typeof Brain; gradient: string; featureCount: number; m3Tier: M3Tier }> = {
  basic:  { icon: Brain,    gradient: "from-slate-500 to-slate-600",   featureCount: 4, m3Tier: "basic" },
  plus:   { icon: Sparkles, gradient: "from-violet-500 to-indigo-500", featureCount: 5, m3Tier: "premium" },
  pro:    { icon: Crown,    gradient: "from-amber-500 to-orange-500",  featureCount: 7, m3Tier: "ultimate" },
};

export function TrainingPricingOverlay({ isOpen, onClose, onSelect, accentColor }: Props) {
  const { t } = useTranslation();

  const handleSelect = (tier: Tier) => {
    const m3Tier = TIER_META[tier].m3Tier;
    onSelect(m3Tier);
    onClose();
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/70 backdrop-blur-md" />

          {/* Content panel */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            onClick={(e) => e.stopPropagation()}
            className="relative w-full max-w-3xl rounded-2xl overflow-hidden"
            style={{
              background: "rgba(8, 8, 16, 0.85)",
              backdropFilter: "blur(24px)",
              WebkitBackdropFilter: "blur(24px)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              boxShadow: `0 0 80px ${accentColor}10, 0 25px 60px -12px rgba(0, 0, 0, 0.6)`,
            }}
          >
            {/* Close button */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 z-10 w-8 h-8 rounded-full flex items-center justify-center text-slate-500 hover:text-slate-300 transition-colors duration-300"
              style={{ background: "rgba(255,255,255,0.05)" }}
            >
              <X size={16} />
            </button>

            {/* Header */}
            <div className="text-center pt-8 pb-4 px-6">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Brain size={20} style={{ color: accentColor }} />
                <h2
                  className="text-xl font-display font-bold tracking-tight"
                  style={{ color: accentColor }}
                >
                  {t("m3.pricing.title")}
                </h2>
              </div>
              <p className="text-sm text-slate-500 font-display font-light">
                {t("m3.pricing.subtitle")}
              </p>
            </div>

            {/* Tier cards grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 px-6 pb-6">
              {TIERS.map((tier) => {
                const meta = TIER_META[tier];
                const Icon = meta.icon;
                const isPopular = tier === "plus";
                const price = t(`m3.pricing.${tier}.price`);
                const period = t(`m3.pricing.${tier}.period`);
                const name = t(`m3.pricing.${tier}.name`);
                const frequency = t(`m3.pricing.${tier}.frequency`);
                const features = t(`m3.pricing.${tier}.features`, { returnObjects: true }) as string[];

                return (
                  <motion.div
                    key={tier}
                    initial={{ opacity: 0, y: 15 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: TIERS.indexOf(tier) * 0.1 + 0.2, duration: 0.5 }}
                    className="relative flex flex-col rounded-xl overflow-hidden"
                    style={{
                      background: isPopular
                        ? `linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(99, 102, 241, 0.06))`
                        : "rgba(255, 255, 255, 0.02)",
                      border: isPopular
                        ? `1.5px solid ${accentColor}40`
                        : "1px solid rgba(255, 255, 255, 0.06)",
                      boxShadow: isPopular ? `0 0 30px ${accentColor}12` : "none",
                    }}
                  >
                    {/* Popular badge */}
                    {isPopular && (
                      <div
                        className="absolute top-0 right-0 px-3 py-1 rounded-bl-lg text-[10px] font-display font-semibold tracking-wide uppercase"
                        style={{
                          background: `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`,
                          color: "#000",
                        }}
                      >
                        {t("m3.pricing.plus.badge")}
                      </div>
                    )}

                    <div className="p-5 flex flex-col flex-1">
                      {/* Icon + name */}
                      <div className="flex items-center gap-2 mb-3">
                        <div
                          className="w-8 h-8 rounded-lg flex items-center justify-center"
                          style={{
                            background: isPopular ? `${accentColor}20` : "rgba(255,255,255,0.05)",
                          }}
                        >
                          <Icon size={16} style={{ color: isPopular ? accentColor : "#94A3B8" }} />
                        </div>
                        <span
                          className="text-sm font-display font-semibold tracking-wide uppercase"
                          style={{ color: isPopular ? accentColor : "#CBD5E1" }}
                        >
                          {name}
                        </span>
                      </div>

                      {/* Price */}
                      <div className="mb-1">
                        <span className="text-3xl font-display font-bold text-white">{price}</span>
                        <span className="text-sm text-slate-500 font-display font-light">{period}</span>
                      </div>

                      {/* Frequency */}
                      <p className="text-xs text-slate-400 font-display font-light mb-4">
                        {frequency}
                      </p>

                      {/* Divider */}
                      <div
                        className="h-px w-full mb-4"
                        style={{ background: isPopular ? `${accentColor}20` : "rgba(255,255,255,0.06)" }}
                      />

                      {/* Features */}
                      <div className="space-y-2.5 flex-1">
                        {Array.isArray(features) && features.map((feat, i) => (
                          <div key={i} className="flex items-start gap-2">
                            <Check
                              size={13}
                              className="mt-0.5 flex-shrink-0"
                              style={{ color: isPopular ? accentColor : "#64748B" }}
                            />
                            <span className="text-[12px] text-slate-400 font-display font-light leading-tight">
                              {feat}
                            </span>
                          </div>
                        ))}
                      </div>

                      {/* CTA button — now clickable */}
                      <button
                        onClick={() => handleSelect(tier)}
                        className="w-full mt-5 py-2.5 rounded-lg text-xs font-display font-semibold transition-all duration-500 hover:scale-[1.02]"
                        style={{
                          background: isPopular
                            ? `linear-gradient(135deg, ${accentColor}, ${accentColor}CC)`
                            : "rgba(255, 255, 255, 0.05)",
                          color: isPopular ? "#000" : "#94A3B8",
                          border: isPopular
                            ? `1px solid ${accentColor}60`
                            : "1px solid rgba(255,255,255,0.08)",
                          boxShadow: isPopular ? `0 0 20px ${accentColor}20` : "none",
                          cursor: "pointer",
                        }}
                      >
                        {t("m3.pricing.select")}
                      </button>
                    </div>
                  </motion.div>
                );
              })}
            </div>

            {/* Footer */}
            <div className="text-center pb-6 px-6">
              <div className="flex items-center justify-center gap-1.5 text-slate-600">
                <Shield size={12} />
                <span className="text-[11px] font-display font-light">
                  {t("m3.pricing.secure")}
                </span>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
