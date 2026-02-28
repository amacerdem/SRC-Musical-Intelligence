import { motion } from "framer-motion";
import { useChatStore } from "@/stores/useChatStore";
import { useMobile } from "@/hooks/useMediaQuery";
import { MiniOrganism } from "@/components/mind/MiniOrganism";
import { NucleusDot } from "@/components/mind/NucleusDot";

interface Props {
  accentColor: string;
}

export function ChatBubble({ accentColor }: Props) {
  const toggle = useChatStore((s) => s.toggle);
  const hasUnread = useChatStore((s) => s.hasUnread);
  const isOpen = useChatStore((s) => s.isOpen);
  const isMobile = useMobile();

  return (
    <motion.button
      initial={{ scale: 0, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1], delay: 0.8 }}
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggle}
      className="fixed z-[55] flex items-center justify-center"
      style={{
        width: 52,
        height: 52,
        left: "50%",
        transform: "translateX(-50%)",
        bottom: isMobile
          ? "calc(56px + env(safe-area-inset-bottom, 0px) + 12px)"
          : 24,
        borderRadius: "50%",
        background: `radial-gradient(circle at 40% 40%, ${accentColor}30, ${accentColor}08)`,
        border: `1.5px solid ${accentColor}25`,
        boxShadow: isOpen
          ? `0 0 24px ${accentColor}20`
          : `0 0 16px ${accentColor}10, 0 4px 12px rgba(0,0,0,0.3)`,
      }}
    >
      <MiniOrganism color={accentColor} size={36} animated={isOpen} />

      {/* Unread indicator */}
      {hasUnread && !isOpen && (
        <div className="absolute -top-0.5 -right-0.5">
          <NucleusDot color={accentColor} size={6} active pulsing />
        </div>
      )}
    </motion.button>
  );
}
