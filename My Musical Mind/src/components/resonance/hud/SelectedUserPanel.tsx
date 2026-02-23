/* ── SelectedUserPanel — Bipolar comparison + resonance score ───── */

import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { DIMENSIONS, resonance, dimResonance } from "@/data/resonance-simulation";

const ease = [0.22, 1, 0.36, 1] as const;

/** Dimension color for a given psi value — same palette as SelfStatePanel & tendrils */
function dimColor(dim: typeof DIMENSIONS[number], psi: number): string {
  return psi >= 0 ? dim.posColor : dim.negColor;
}

export function SelectedUserPanel({ onOpenComm }: { onOpenComm?: () => void }) {
  const { t } = useTranslation();
  const selectedUserId = useResonanceStore(s => s.selectedUserId);
  const users = useResonanceStore(s => s.users);
  const selfPsi = useResonanceStore(s => s.selfPsi);
  const selectUser = useResonanceStore(s => s.selectUser);

  const user = selectedUserId ? users.find(u => u.id === selectedUserId) : null;
  const res = user ? resonance(selfPsi, user.psi) : 0;
  const resPct = Math.round(res * 100);

  const resColor = resPct >= 80 ? "#10B981" : resPct >= 50 ? "#A855F7" : "#64748B";

  return (
    <AnimatePresence>
      {user && (
        <motion.div
          key={user.id}
          initial={{ opacity: 0, x: 40, filter: "blur(8px)" }}
          animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
          exit={{ opacity: 0, x: 40, filter: "blur(8px)" }}
          transition={{ duration: 0.5, ease }}
          className="fixed top-24 right-6 z-[45] w-[380px]"
        >
          <div className="glass p-5 rounded-2xl flex flex-col gap-3">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-display font-bold"
                  style={{ background: `${resColor}20`, color: resColor, border: `1px solid ${resColor}30` }}
                >
                  {user.displayName.charAt(0)}
                </div>
                <div className="flex flex-col">
                  <span className="text-sm font-display font-medium text-white/80">{user.displayName}</span>
                  <span className="text-[10px] font-mono text-slate-500">{user.country}</span>
                </div>
              </div>
              <button onClick={() => selectUser(null)} className="text-slate-700 hover:text-slate-400 transition-colors">
                <X size={16} />
              </button>
            </div>

            {/* Bio */}
            <p className="text-[11px] font-body text-slate-500 leading-relaxed line-clamp-2">{user.bio}</p>

            {/* Resonance score */}
            <div className="flex items-center gap-3">
              <span className="text-2xl font-mono font-bold tabular-nums" style={{ color: resColor }}>
                {resPct}%
              </span>
              <div className="flex flex-col">
                <span className="text-[11px] font-display uppercase tracking-[0.15em]" style={{ color: resColor }}>
                  {t("resonance.resonanceLabel")}
                </span>
                <span className="text-[9px] font-mono text-slate-600">
                  {resPct >= 80 ? t("resonance.deepSync") : resPct >= 60 ? t("resonance.harmonic") : resPct >= 40 ? t("resonance.partial") : t("resonance.divergent")}
                </span>
              </div>
            </div>

            {/* Bipolar dimension comparison — consistent dimension colors */}
            <div className="flex flex-col gap-2.5 mt-1">
              {DIMENSIONS.map((dim, i) => {
                const selfVal = selfPsi[i];
                const userVal = user.psi[i];
                const dr = dimResonance(selfVal, userVal);
                const selfPct = 50 + (selfVal / 5) * 50;
                const userPct = 50 + (userVal / 5) * 50;
                const selfCol = dimColor(dim, selfVal);
                const userCol = dimColor(dim, userVal);

                return (
                  <div key={dim.id} className="flex items-center gap-2">
                    {/* Neg label — left */}
                    <span
                      className="text-[10px] font-mono w-[70px] text-right tracking-wider uppercase"
                      style={{ color: dim.negColor }}
                    >
                      {t(`resonance.dimensions.${dim.id}.neg`)}
                    </span>

                    {/* Bar */}
                    <div className="relative flex-1 h-3 rounded-full bg-white/[0.04]">
                      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/[0.06]" />
                      {/* Self marker */}
                      <div
                        className="absolute top-0 w-2 h-full rounded-full"
                        style={{
                          left: `calc(${selfPct}% - 4px)`,
                          background: selfCol,
                          opacity: 0.5,
                          boxShadow: `0 0 6px ${selfCol}50`,
                        }}
                      />
                      {/* User marker */}
                      <div
                        className="absolute top-0 w-2 h-full rounded-full"
                        style={{
                          left: `calc(${userPct}% - 4px)`,
                          background: userCol,
                          boxShadow: `0 0 8px ${userCol}60`,
                        }}
                      />
                      {/* Resonance bridge */}
                      {dr > 0.4 && (
                        <div
                          className="absolute top-[5px] h-0.5 rounded-full"
                          style={{
                            left: `${Math.min(selfPct, userPct)}%`,
                            width: `${Math.abs(selfPct - userPct)}%`,
                            background: `${userCol}40`,
                          }}
                        />
                      )}
                    </div>

                    {/* Pos label — right */}
                    <span
                      className="text-[10px] font-mono w-[70px] tracking-wider uppercase"
                      style={{ color: dim.posColor }}
                    >
                      {t(`resonance.dimensions.${dim.id}.pos`)}
                    </span>

                    {/* Resonance % */}
                    <span className="text-[9px] font-mono w-8 text-right tabular-nums font-medium" style={{ color: dr > 0.7 ? "#10B981" : "rgba(255,255,255,0.3)" }}>
                      {Math.round(dr * 100)}%
                    </span>
                  </div>
                );
              })}
              <div className="flex justify-between mt-1 px-1">
                <span className="text-[8px] font-mono text-white/25">○ {t("resonance.you").toUpperCase()}</span>
                <span className="text-[8px] font-mono" style={{ color: resColor }}>● {t("resonance.them").toUpperCase()}</span>
              </div>
            </div>

            {/* Current track with mini play bar */}
            {user.trackTitle && (
              <div className="flex flex-col gap-1.5 mt-2">
                <div className="flex items-center gap-2">
                  <div className="flex items-end gap-[2px] h-3 shrink-0">
                    {[0.5, 1, 0.6].map((_, i) => (
                      <div
                        key={i}
                        className="w-[2px] rounded-full origin-bottom"
                        style={{
                          background: resColor,
                          height: "100%",
                          animation: "eq 0.8s ease-in-out infinite",
                          animationDelay: `${i * 0.15}s`,
                        }}
                      />
                    ))}
                  </div>
                  <span className="text-[10px] font-mono text-slate-400 truncate flex-1">
                    {user.trackArtist} — {user.trackTitle}
                  </span>
                </div>
                <div className="h-[2px] rounded-full bg-white/5 overflow-hidden">
                  <div
                    className="h-full rounded-full transition-[width] duration-1000"
                    style={{
                      width: `${(user.trackProgress ?? 0) * 100}%`,
                      background: resColor,
                      opacity: 0.5,
                    }}
                  />
                </div>
              </div>
            )}

            {/* Send signal */}
            <button
              className="mt-1 w-full py-2.5 rounded-xl text-[11px] font-display uppercase tracking-[0.2em] transition-all duration-300 hover:scale-[1.02]"
              style={{ background: `${resColor}15`, border: `1px solid ${resColor}25`, color: resColor }}
              onClick={() => onOpenComm?.()}
            >
              {t("resonance.sendSignal")}
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
