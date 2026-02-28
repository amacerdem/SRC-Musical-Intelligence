import { useState, useRef, useCallback } from "react";
import { Send } from "lucide-react";
import { useTranslation } from "react-i18next";

interface Props {
  onSend: (text: string) => void;
  disabled?: boolean;
  accentColor: string;
}

export function ChatInput({ onSend, disabled, accentColor }: Props) {
  const { t } = useTranslation();
  const [text, setText] = useState("");
  const inputRef = useRef<HTMLTextAreaElement>(null);

  const handleSend = useCallback(() => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText("");
    // Reset textarea height
    if (inputRef.current) {
      inputRef.current.style.height = "auto";
    }
  }, [text, disabled, onSend]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleInput = () => {
    const el = inputRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 120) + "px";
  };

  return (
    <div className="flex items-end gap-2 p-3 border-t border-white/[0.06]">
      <textarea
        ref={inputRef}
        value={text}
        onChange={(e) => { setText(e.target.value); handleInput(); }}
        onKeyDown={handleKeyDown}
        placeholder={t("chat.placeholder")}
        disabled={disabled}
        rows={1}
        className="flex-1 resize-none bg-white/[0.04] border border-white/[0.08] rounded-xl px-3.5 py-2.5 text-sm text-slate-200 placeholder:text-slate-600 outline-none focus:border-white/[0.15] transition-colors font-body"
        style={{ maxHeight: 120 }}
      />
      <button
        onClick={handleSend}
        disabled={disabled || !text.trim()}
        className="flex-shrink-0 w-9 h-9 rounded-xl flex items-center justify-center transition-all duration-200 disabled:opacity-30"
        style={{
          background: text.trim() && !disabled ? `${accentColor}25` : "transparent",
          border: `1px solid ${text.trim() && !disabled ? accentColor + "40" : "transparent"}`,
        }}
      >
        <Send
          size={16}
          style={{ color: text.trim() && !disabled ? accentColor : "#64748b" }}
        />
      </button>
    </div>
  );
}
