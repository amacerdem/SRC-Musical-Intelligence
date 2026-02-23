/* ── SelectedUserPanel — Glass panel on user selection ────────────── */

import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { beliefColors } from "@/design/tokens";
import { beliefSimilarity } from "@/data/resonance-simulation";
import { getCompatibilityLabel } from "@/design/tokens";
import { useUserStore } from "@/stores/useUserStore";

const ease = [0.22, 1, 0.36, 1] as const;

const BELIEF_LABELS = ["Consonance", "Tempo", "Salience", "Familiarity", "Reward"];
const BELIEF_KEYS = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

function getSelfBeliefs(): [number, number, number, number, number] {
  const mind = useUserStore.getState().mind;
  if (!mind) return [0.5, 0.5, 0.5, 0.5, 0.5];
  const a = mind.axes;
  return [
    1 - a.entropyTolerance,
    a.tensionAppetite,
    a.salienceSensitivity,
    a.monotonyTolerance,
    a.resolutionCraving,
  ];
}

export function SelectedUserPanel({ onOpenComm }: { onOpenComm?: () => void }) {
  const selectedUserId = useResonanceStore(s => s.selectedUserId);
  const users = useResonanceStore(s => s.users);
  const selectUser = useResonanceStore(s => s.selectUser);

  const user = selectedUserId ? users.find(u => u.id === selectedUserId) : null;
  const selfBeliefs = getSelfBeliefs();
  const similarity = user ? beliefSimilarity(selfBeliefs, user.beliefs) : 0;
  const compatScore = Math.round(similarity * 100);
  const compat = getCompatibilityLabel(compatScore);

  return (
    <AnimatePresence>
      {user && (
        <motion.div
          key={user.id}
          initial={{ opacity: 0, x: 40, filter: "blur(8px)" }}
          animate={{ opacity: 1, x: 0, filter: "blur(0px)" }}
          exit={{ opacity: 0, x: 40, filter: "blur(8px)" }}
          transition={{ duration: 0.5, ease }}
          className="fixed top-24 right-6 z-[45] w-64"
        >
          <div className="glass p-4 rounded-2xl flex flex-col gap-3">
            {/* Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-[10px] font-display font-bold"
                  style={{
                    background: `${beliefColors[BELIEF_KEYS[user.dominantBelief]].primary}20`,
                    color: beliefColors[BELIEF_KEYS[user.dominantBelief]].primary,
                    border: `1px solid ${beliefColors[BELIEF_KEYS[user.dominantBelief]].primary}30`,
                  }}
                >
                  {user.displayName.charAt(0)}
                </div>
                <div className="flex flex-col">
                  <span className="text-[11px] font-display font-medium text-white/80">
                    {user.displayName}
                  </span>
                  <span className="text-[8px] font-mono text-slate-600">
                    {user.country}
                  </span>
                </div>
              </div>
              <button
                onClick={() => selectUser(null)}
                className="text-slate-700 hover:text-slate-400 transition-colors"
              >
                <X size={14} />
              </button>
            </div>

            {/* Bio */}
            <p className="text-[9px] font-body text-slate-500 leading-relaxed line-clamp-2">
              {user.bio}
            </p>

            {/* Compatibility */}
            <div className="flex items-center gap-2">
              <span
                className="text-[18px] font-mono font-bold"
                style={{ color: compat.color }}
              >
                {compatScore}%
              </span>
              <span
                className="text-[8px] font-display uppercase tracking-[0.15em]"
                style={{ color: compat.color }}
              >
                {compat.label}
              </span>
            </div>

            {/* Belief comparison bars */}
            <div className="flex flex-col gap-1.5">
              {BELIEF_KEYS.map((key, i) => (
                <div key={key} className="flex items-center gap-2">
                  <span
                    className="text-[7px] font-mono w-6 text-right"
                    style={{ color: `${beliefColors[key].primary}50` }}
                  >
                    {BELIEF_LABELS[i].slice(0, 3).toUpperCase()}
                  </span>
                  <div className="flex-1 flex gap-0.5">
                    {/* Self bar */}
                    <div className="flex-1 h-1 rounded-full bg-white/[0.04] overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-700"
                        style={{
                          width: `${selfBeliefs[i] * 100}%`,
                          background: `${beliefColors[key].primary}40`,
                        }}
                      />
                    </div>
                    {/* User bar */}
                    <div className="flex-1 h-1 rounded-full bg-white/[0.04] overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-700"
                        style={{
                          width: `${user.beliefs[i] * 100}%`,
                          background: beliefColors[key].primary,
                        }}
                      />
                    </div>
                  </div>
                </div>
              ))}
              <div className="flex justify-end gap-6 mt-0.5">
                <span className="text-[6px] font-mono text-white/20">YOU</span>
                <span className="text-[6px] font-mono text-white/40">THEM</span>
              </div>
            </div>

            {/* Current track */}
            {user.currentTrack && (
              <div className="flex items-center gap-1.5 mt-1">
                <span className="text-[7px] font-mono text-slate-700">NOW PLAYING</span>
                <span className="text-[8px] font-mono text-slate-500 truncate max-w-[160px]">
                  {user.currentTrack}
                </span>
              </div>
            )}

            {/* Send signal button */}
            <button
              className="mt-1 w-full py-2 rounded-xl text-[9px] font-display uppercase tracking-[0.2em] transition-all duration-300 hover:scale-[1.02]"
              style={{
                background: `${beliefColors[BELIEF_KEYS[user.dominantBelief]].primary}15`,
                border: `1px solid ${beliefColors[BELIEF_KEYS[user.dominantBelief]].primary}20`,
                color: beliefColors[BELIEF_KEYS[user.dominantBelief]].primary,
              }}
              onClick={() => onOpenComm?.()}
            >
              Send Signal
            </button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
