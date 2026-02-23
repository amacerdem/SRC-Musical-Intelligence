/* ── CommunicationPanel — Emote grid + message input ────────────── */

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useResonanceStore } from "@/stores/useResonanceStore";
import type { ResonanceSignal } from "@/data/resonance-simulation";

const ease = [0.22, 1, 0.36, 1] as const;

const EMOTE_KEYS: { type: ResonanceSignal["type"]; emoji: string; key: string }[] = [
  { type: "wave", emoji: "👋", key: "resonance.emotes.wave" },
  { type: "chills", emoji: "✨", key: "resonance.emotes.chills" },
  { type: "vibe", emoji: "🌊", key: "resonance.emotes.vibe" },
  { type: "fire", emoji: "🔥", key: "resonance.emotes.fire" },
  { type: "mind", emoji: "🧠", key: "resonance.emotes.mind" },
  { type: "feel", emoji: "💜", key: "resonance.emotes.feel" },
  { type: "sync", emoji: "🔗", key: "resonance.emotes.sync" },
  { type: "peak", emoji: "⚡", key: "resonance.emotes.peak" },
];

interface Props {
  targetUserId: string;
  onClose: () => void;
}

export function CommunicationPanel({ targetUserId, onClose }: Props) {
  const { t } = useTranslation();
  const sendSignal = useResonanceStore(s => s.sendSignal);
  const users = useResonanceStore(s => s.users);
  const [message, setMessage] = useState("");
  const [sentEmote, setSentEmote] = useState<string | null>(null);

  const targetUser = users.find(u => u.id === targetUserId);
  if (!targetUser) return null;

  const handleEmote = (type: ResonanceSignal["type"], emoji: string) => {
    sendSignal(targetUserId, type, emoji);
    setSentEmote(emoji);
    setTimeout(() => setSentEmote(null), 1500);
  };

  const handleMessage = () => {
    if (!message.trim()) return;
    sendSignal(targetUserId, "wave", message.trim());
    setMessage("");
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, y: 20, scale: 0.95 }}
      transition={{ duration: 0.4, ease }}
      className="fixed bottom-24 right-6 z-[46] w-56"
    >
      <div className="glass p-3 rounded-2xl flex flex-col gap-2.5">
        {/* Header */}
        <div className="flex items-center justify-between">
          <span className="text-[8px] font-display uppercase tracking-[0.2em] text-white/30">
            {t("resonance.signalTo", { name: targetUser.displayName })}
          </span>
          <button
            onClick={onClose}
            className="text-[8px] text-slate-700 hover:text-slate-400 transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Emote grid */}
        <div className="grid grid-cols-4 gap-1.5">
          {EMOTE_KEYS.map(e => (
            <button
              key={e.type}
              onClick={() => handleEmote(e.type, e.emoji)}
              className="flex flex-col items-center gap-0.5 py-1.5 rounded-lg transition-all duration-200 hover:bg-white/[0.05] active:scale-90"
            >
              <span className="text-base">{e.emoji}</span>
              <span className="text-[6px] font-mono text-slate-700">{t(e.key)}</span>
            </button>
          ))}
        </div>

        {/* Message input */}
        <div className="flex gap-1.5">
          <input
            type="text"
            value={message}
            onChange={e => setMessage(e.target.value.slice(0, 50))}
            onKeyDown={e => e.key === "Enter" && handleMessage()}
            placeholder={t("resonance.messagePlaceholder")}
            className="flex-1 px-2.5 py-1.5 bg-white/[0.03] rounded-lg text-[9px] font-body text-slate-300 placeholder:text-slate-800 outline-none border border-white/[0.04] focus:border-white/[0.08] transition-colors"
          />
          <button
            onClick={handleMessage}
            className="px-2 py-1.5 rounded-lg bg-white/[0.05] text-[9px] font-display text-white/40 hover:text-white/70 hover:bg-white/[0.08] transition-all"
          >
            →
          </button>
        </div>

        {/* Sent feedback */}
        <AnimatePresence>
          {sentEmote && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, y: -10 }}
              className="text-center text-sm"
            >
              {sentEmote} <span className="text-[8px] text-slate-600">{t("resonance.sent")}</span>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
}
