import { AnimatePresence } from "framer-motion";
import { useLocation } from "react-router-dom";
import { useChatStore } from "@/stores/useChatStore";
import { useActiveIdentity } from "@/hooks/useActiveIdentity";
import { useM3Store } from "@/stores/useM3Store";
import { personas } from "@/data/personas";
import { ChatBubble } from "./ChatBubble";
import { ChatPanel } from "./ChatPanel";

export function MindChat() {
  const location = useLocation();
  const isOpen = useChatStore((s) => s.isOpen);
  const { color } = useActiveIdentity();
  const activePersonaId = useM3Store((s) => s.mind?.activePersonaId);
  const persona = activePersonaId ? personas.find((p) => p.id === activePersonaId) : null;
  const personaName = persona?.name ?? "Musical Mind";

  // Hide on immersive pages and dashboard (chat is embedded there)
  const hidden = location.pathname === "/live" || location.pathname === "/dashboard";
  if (hidden) return null;

  return (
    <>
      <ChatBubble accentColor={color} />
      <AnimatePresence>
        {isOpen && (
          <ChatPanel
            personaName={personaName}
            accentColor={color}
          />
        )}
      </AnimatePresence>
    </>
  );
}
