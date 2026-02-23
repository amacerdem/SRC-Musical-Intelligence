/* ── SelectedUserPanel — Bipolar comparison + resonance score ───── */

import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { DIMENSIONS, resonance, dimResonance } from "@/data/resonance-simulation";

const ease = [0.22, 1, 0.36, 1] as const;

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
          className="fixed top-24 right-6 z-[45] w-72"
        >
          <div className="glass p-4 rounded-2xl flex flex-col gap-3">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-display font-bold"
                  style={{ background: `${resColor}20`, color: resColor, border: `1px solid ${resColor}30` }}
                >
                  {user.displayName.charAt(0)}
                </div>
                <div className="flex flex-col">
                  <span className="text-[11px] font-display font-medium text-white/80">{user.displayName}</span>
                  <span className="text-[8px] font-mono text-slate-600">{user.country}</span>
                </div>
              </div>
              <button onClick={() => selectUser(null)} className="text-slate-700 hover:text-slate-400 transition-colors">
                <X size={14} />
              </button>
            </div>

            {/* Bio */}
            <p className="text-[9px] font-body text-slate-500 leading-relaxed line-clamp-2">{user.bio}</p>

            {/* Resonance score */}
            <div className="flex items-center gap-3">
              <span className="text-[22px] font-mono font-bold tabular-nums" style={{ color: resColor }}>
                {resPct}%
              </span>
              <div className="flex flex-col">
                <span className="text-[9px] font-display uppercase tracking-[0.15em]" style={{ color: resColor }}>
                  {t("resonance.resonanceLabel")}
                </span>
                <span className="text-[7px] font-mono text-slate-700">
                  {resPct >= 80 ? t("resonance.deepSync") : resPct >= 60 ? t("resonance.harmonic") : resPct >= 40 ? t("resonance.partial") : t("resonance.divergent")}
                </span>
              </div>
            </div>

            {/* Bipolar dimension comparison */}
            <div className="flex flex-col gap-2 mt-1">
              {DIMENSIONS.map((dim, i) => {
                const selfVal = selfPsi[i];
                const userVal = user.psi[i];
                const dr = dimResonance(selfVal, userVal);
                const selfPct = 50 + (selfVal / 5) * 50;
                const userPct = 50 + (userVal / 5) * 50;
                const dimColor = dr > 0.7 ? "#10B981" : dr > 0.4 ? "#A855F7" : "#475569";

                return (
                  <div key={dim.id} className="flex flex-col gap-0.5">
                    <div className="flex items-center justify-between">
                      <span className="text-[7px] font-mono text-slate-600 uppercase tracking-wider">
                        {t(`resonance.dimensions.${dim.id}.neg`)} ← → {t(`resonance.dimensions.${dim.id}.pos`)}
                      </span>
                      <span className="text-[7px] font-mono tabular-nums" style={{ color: dimColor }}>
                        {Math.round(dr * 100)}%
                      </span>
                    </div>
                    <div className="relative h-2 rounded-full bg-white/[0.04]">
                      <div className="absolute left-1/2 top-0 bottom-0 w-px bg-white/[0.06]" />
                      {/* Self marker */}
                      <div
                        className="absolute top-0 w-1.5 h-full rounded-full"
                        style={{
                          left: `calc(${selfPct}% - 3px)`,
                          background: "rgba(255,255,255,0.5)",
                          boxShadow: "0 0 4px rgba(255,255,255,0.3)",
                        }}
                      />
                      {/* User marker */}
                      <div
                        className="absolute top-0 w-1.5 h-full rounded-full"
                        style={{
                          left: `calc(${userPct}% - 3px)`,
                          background: dimColor,
                          boxShadow: `0 0 6px ${dimColor}60`,
                        }}
                      />
                      {/* Resonance bridge */}
                      {dr > 0.4 && (
                        <div
                          className="absolute top-[3px] h-0.5 rounded-full"
                          style={{
                            left: `${Math.min(selfPct, userPct)}%`,
                            width: `${Math.abs(selfPct - userPct)}%`,
                            background: `${dimColor}40`,
                          }}
                        />
                      )}
                    </div>
                  </div>
                );
              })}
              <div className="flex justify-between mt-0.5 px-1">
                <span className="text-[6px] font-mono text-white/20">○ {t("resonance.you").toUpperCase()}</span>
                <span className="text-[6px] font-mono" style={{ color: resColor }}>● {t("resonance.them").toUpperCase()}</span>
              </div>
            </div>

            {/* Current track */}
            {user.currentTrack && (
              <div className="flex items-center gap-1.5 mt-1">
                <span className="text-[7px] font-mono text-slate-700">{t("resonance.now").toUpperCase()}</span>
                <span className="text-[8px] font-mono text-slate-500 truncate max-w-[180px]">{user.currentTrack}</span>
              </div>
            )}

            {/* Send signal */}
            <button
              className="mt-1 w-full py-2 rounded-xl text-[9px] font-display uppercase tracking-[0.2em] transition-all duration-300 hover:scale-[1.02]"
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
