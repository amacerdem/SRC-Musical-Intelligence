import { motion } from "framer-motion";
import { MiniOrganism } from "@/components/mind/MiniOrganism";

interface Props {
  role: "user" | "assistant";
  content: string;
  accentColor: string;
}

/** Simple markdown-lite: headers, bold, italic, bullet & numbered lists */
function renderContent(text: string) {
  const lines = text.split("\n");
  return lines.map((line, i) => {
    const trimmed = line.trimStart();

    // Headers: ### → h3, ## → h2, # → h1
    const headerMatch = trimmed.match(/^(#{1,3})\s+(.+)/);
    if (headerMatch) {
      const level = headerMatch[1].length;
      const content = headerMatch[2];
      const sizes = ["text-[15px]", "text-[14px]", "text-[13px]"];
      return (
        <p key={i} className={`${sizes[level - 1]} font-semibold text-white/90 mt-1`}>
          {formatInline(content)}
        </p>
      );
    }

    // Bullet list
    if (trimmed.startsWith("- ") || trimmed.startsWith("• ")) {
      const item = trimmed.slice(2);
      return (
        <div key={i} className="flex gap-1.5 ml-1">
          <span className="text-slate-500 mt-0.5">•</span>
          <span>{formatInline(item)}</span>
        </div>
      );
    }

    // Numbered list: 1. text, 2. text, etc.
    const numMatch = trimmed.match(/^(\d+)[.)]\s+(.+)/);
    if (numMatch) {
      return (
        <div key={i} className="flex gap-1.5 ml-1">
          <span className="text-slate-500 font-mono text-[11px] mt-0.5 w-4 text-right shrink-0">{numMatch[1]}.</span>
          <span>{formatInline(numMatch[2])}</span>
        </div>
      );
    }

    // Horizontal rule
    if (/^[-–—]{3,}$/.test(trimmed)) {
      return <hr key={i} className="border-white/[0.06] my-1" />;
    }

    // Empty line → spacer
    if (!trimmed) return <div key={i} className="h-2" />;
    return <p key={i}>{formatInline(line)}</p>;
  });
}

function formatInline(text: string) {
  // Bold: **text**
  const parts = text.split(/(\*\*[^*]+\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return <strong key={i} className="font-semibold text-white/90">{part.slice(2, -2)}</strong>;
    }
    // Italic: *text*
    const italicParts = part.split(/(\*[^*]+\*)/g);
    return italicParts.map((ip, j) => {
      if (ip.startsWith("*") && ip.endsWith("*") && ip.length > 2) {
        return <em key={`${i}-${j}`} className="italic text-slate-300">{ip.slice(1, -1)}</em>;
      }
      return <span key={`${i}-${j}`}>{ip}</span>;
    });
  });
}

export function ChatMessage({ role, content, accentColor }: Props) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
      className={`flex gap-2 ${isUser ? "flex-row-reverse" : "flex-row"}`}
    >
      {/* Avatar — only for assistant */}
      {!isUser && (
        <div className="flex-shrink-0 mt-1">
          <MiniOrganism color={accentColor} size={24} />
        </div>
      )}

      {/* Bubble */}
      <div
        className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 text-[13px] leading-relaxed font-body ${
          isUser
            ? "rounded-br-md"
            : "rounded-bl-md"
        }`}
        style={{
          background: isUser ? `${accentColor}18` : "rgba(255,255,255,0.04)",
          border: `1px solid ${isUser ? accentColor + "20" : "rgba(255,255,255,0.06)"}`,
          color: isUser ? "#e2e8f0" : "#cbd5e1",
        }}
      >
        {renderContent(content)}
      </div>
    </motion.div>
  );
}

/** Typing indicator — shows live status text or 3 pulsing dots */
export function TypingIndicator({
  accentColor,
  statusText,
}: {
  accentColor: string;
  statusText?: string | null;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="flex gap-2"
    >
      <div className="flex-shrink-0 mt-1">
        <MiniOrganism color={accentColor} size={24} animated />
      </div>
      <div
        className="rounded-2xl rounded-bl-md px-4 py-3 flex items-center gap-1.5"
        style={{
          background: "rgba(255,255,255,0.04)",
          border: "1px solid rgba(255,255,255,0.06)",
        }}
      >
        {statusText ? (
          <motion.span
            key={statusText}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.2 }}
            className="text-[12px] font-mono"
            style={{ color: `${accentColor}cc` }}
          >
            {statusText}
          </motion.span>
        ) : (
          [0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="w-1.5 h-1.5 rounded-full"
              style={{ background: accentColor }}
              animate={{ opacity: [0.3, 1, 0.3] }}
              transition={{
                duration: 1.2,
                repeat: Infinity,
                delay: i * 0.2,
              }}
            />
          ))
        )}
      </div>
    </motion.div>
  );
}
