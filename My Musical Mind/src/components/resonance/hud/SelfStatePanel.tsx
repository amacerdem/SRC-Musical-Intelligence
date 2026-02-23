/* ── SelfStatePanel — Large bipolar bars [-5, +5], 60fps ─────────── */

import { useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { DIMENSIONS, type Psi5 } from "@/data/resonance-simulation";

const ease = [0.22, 1, 0.36, 1] as const;

/* ── Single bipolar bar (center-anchored, colored by polarity) ──── */

function BipolarBar({ value, dim, index, t }: { value: number; dim: typeof DIMENSIONS[number]; index: number; t: (key: string) => string }) {
  // value is [-5, +5], we show a bar from center (0) outward
  const pct = (value / 5) * 50; // -50% to +50%
  const isPositive = value >= 0;
  const color = isPositive ? dim.posColor : dim.negColor;
  const absValue = Math.abs(value).toFixed(1);

  return (
    <motion.div
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease, delay: 0.8 + index * 0.08 }}
      className="flex items-center gap-2"
    >
      {/* Negative label */}
      <span
        className="text-[8px] font-mono w-14 text-right tracking-wider transition-opacity duration-300"
        style={{ color: !isPositive ? dim.negColor : "rgba(100,116,139,0.3)" }}
      >
        {t(`resonance.dimensions.${dim.id}.neg`).toUpperCase()}
      </span>

      {/* Bar track */}
      <div className="relative flex-1 h-2.5 rounded-full bg-white/[0.04] overflow-hidden">
        {/* Center line */}
        <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/[0.08] z-10" />

        {/* Fill bar — anchored at center, extends left or right */}
        <div
          className="absolute top-0 bottom-0 rounded-full transition-none"
          style={{
            background: `linear-gradient(${isPositive ? '90deg' : '270deg'}, ${color}30, ${color})`,
            left: isPositive ? "50%" : `${50 + pct}%`,
            width: `${Math.abs(pct)}%`,
            boxShadow: `0 0 12px ${color}40`,
          }}
        />
      </div>

      {/* Positive label */}
      <span
        className="text-[8px] font-mono w-14 tracking-wider transition-opacity duration-300"
        style={{ color: isPositive ? dim.posColor : "rgba(100,116,139,0.3)" }}
      >
        {t(`resonance.dimensions.${dim.id}.pos`).toUpperCase()}
      </span>

      {/* Numeric value */}
      <span
        className="text-[10px] font-mono w-8 text-right tabular-nums font-medium"
        style={{ color }}
      >
        {isPositive ? "+" : ""}{absValue}
      </span>
    </motion.div>
  );
}

/* ── Panel ──────────────────────────────────────────────────────── */

export function SelfStatePanel() {
  const { t } = useTranslation();
  const entranceComplete = useResonanceStore(s => s.entranceComplete);
  const selfPsi = useResonanceStore(s => s.selfPsi);

  // 60fps smooth interpolation via requestAnimationFrame
  const displayPsi = useRef<Psi5>([...selfPsi]);
  const frameRef = useRef<number>(0);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let running = true;
    const tick = () => {
      if (!running) return;
      for (let i = 0; i < 5; i++) {
        displayPsi.current[i] += (selfPsi[i] - displayPsi.current[i]) * 0.12;
      }
      // Direct DOM update for 60fps (avoid React re-render)
      if (containerRef.current) {
        const bars = containerRef.current.querySelectorAll<HTMLElement>("[data-bar]");
        bars.forEach((bar, i) => {
          const val = displayPsi.current[i];
          const pct = (val / 5) * 50;
          const isPos = val >= 0;
          const dim = DIMENSIONS[i];
          const color = isPos ? dim.posColor : dim.negColor;
          bar.style.left = isPos ? "50%" : `${50 + pct}%`;
          bar.style.width = `${Math.abs(pct)}%`;
          bar.style.background = `linear-gradient(${isPos ? '90deg' : '270deg'}, ${color}30, ${color})`;
          bar.style.boxShadow = `0 0 12px ${color}40`;
        });
        const nums = containerRef.current.querySelectorAll<HTMLElement>("[data-num]");
        nums.forEach((num, i) => {
          const val = displayPsi.current[i];
          const isPos = val >= 0;
          const dim = DIMENSIONS[i];
          num.textContent = `${isPos ? "+" : ""}${Math.abs(val).toFixed(1)}`;
          num.style.color = isPos ? dim.posColor : dim.negColor;
        });
      }
      frameRef.current = requestAnimationFrame(tick);
    };
    frameRef.current = requestAnimationFrame(tick);
    return () => { running = false; cancelAnimationFrame(frameRef.current); };
  }, [selfPsi]);

  if (!entranceComplete) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease, delay: 0.5 }}
      className="fixed bottom-16 left-1/2 -translate-x-1/2 z-[45] w-[420px] max-w-[calc(100vw-48px)]"
    >
      <div ref={containerRef} className="glass px-5 py-4 rounded-2xl flex flex-col gap-2">
        <span className="text-[8px] font-display uppercase tracking-[0.25em] text-white/20 mb-1">
          {t("resonance.yourState")}
        </span>
        {DIMENSIONS.map((dim, i) => (
          <div key={dim.id} className="flex items-center gap-2">
            <span
              className="text-[8px] font-mono w-14 text-right tracking-wider"
              style={{ color: selfPsi[i] < 0 ? dim.negColor : "rgba(100,116,139,0.3)" }}
            >
              {t(`resonance.dimensions.${dim.id}.neg`).toUpperCase()}
            </span>
            <div className="relative flex-1 h-2.5 rounded-full bg-white/[0.04] overflow-hidden">
              <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/[0.08] z-10" />
              <div
                data-bar
                className="absolute top-0 bottom-0 rounded-full"
                style={{
                  left: selfPsi[i] >= 0 ? "50%" : `${50 + (selfPsi[i] / 5) * 50}%`,
                  width: `${Math.abs((selfPsi[i] / 5) * 50)}%`,
                  background: `linear-gradient(90deg, ${selfPsi[i] >= 0 ? dim.posColor : dim.negColor}30, ${selfPsi[i] >= 0 ? dim.posColor : dim.negColor})`,
                  boxShadow: `0 0 12px ${selfPsi[i] >= 0 ? dim.posColor : dim.negColor}40`,
                }}
              />
            </div>
            <span
              className="text-[8px] font-mono w-14 tracking-wider"
              style={{ color: selfPsi[i] >= 0 ? dim.posColor : "rgba(100,116,139,0.3)" }}
            >
              {t(`resonance.dimensions.${dim.id}.pos`).toUpperCase()}
            </span>
            <span
              data-num
              className="text-[10px] font-mono w-8 text-right tabular-nums font-medium"
              style={{ color: selfPsi[i] >= 0 ? dim.posColor : dim.negColor }}
            >
              {selfPsi[i] >= 0 ? "+" : ""}{Math.abs(selfPsi[i]).toFixed(1)}
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
