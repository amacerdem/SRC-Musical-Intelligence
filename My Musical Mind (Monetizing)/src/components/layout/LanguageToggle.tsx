/* ── LanguageToggle — EN/TR switch ──────────────────────────────── */

import { useTranslation } from "react-i18next";

export function LanguageToggle() {
  const { i18n } = useTranslation();
  const isEn = i18n.language?.startsWith("en") ?? true;

  const toggle = () => {
    i18n.changeLanguage(isEn ? "tr" : "en");
  };

  return (
    <button
      onClick={toggle}
      className="flex items-center gap-1 px-2 py-1 rounded-full text-[10px] font-mono text-slate-600 hover:text-slate-300 transition-colors duration-300"
      style={{
        background: "rgba(255,255,255,0.03)",
        border: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      <span className={isEn ? "text-slate-300 font-medium" : "text-slate-700"}>EN</span>
      <span className="text-slate-700">/</span>
      <span className={!isEn ? "text-slate-300 font-medium" : "text-slate-700"}>TR</span>
    </button>
  );
}
