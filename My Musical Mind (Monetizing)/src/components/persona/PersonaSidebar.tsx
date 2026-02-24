/* ── PersonaSidebar — Sticky section navigation ──────────────── */

import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import { NARRATIVE_SECTIONS } from "@/data/persona-narratives";

interface Props {
  color: string;
}

export function PersonaSidebar({ color }: Props) {
  const { t } = useTranslation();
  const [activeSection, setActiveSection] = useState(NARRATIVE_SECTIONS[0].key);

  // Track which section is in view
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            const key = entry.target.id.replace("section-", "");
            setActiveSection(key);
          }
        }
      },
      { threshold: 0.3, rootMargin: "-80px 0px -60% 0px" }
    );

    for (const section of NARRATIVE_SECTIONS) {
      const el = document.getElementById(`section-${section.key}`);
      if (el) observer.observe(el);
    }

    return () => observer.disconnect();
  }, []);

  const scrollTo = (key: string) => {
    const el = document.getElementById(`section-${key}`);
    if (el) el.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <nav className="space-y-1">
      {NARRATIVE_SECTIONS.map((section) => {
        const isActive = activeSection === section.key;
        return (
          <button
            key={section.key}
            onClick={() => scrollTo(section.key)}
            className="w-full text-left px-3 py-2 rounded-lg text-xs font-display transition-all duration-300 flex items-center gap-2"
            style={{
              background: isActive ? `${color}12` : "transparent",
              color: isActive ? color : undefined,
              borderLeft: isActive ? `2px solid ${color}` : "2px solid transparent",
            }}
          >
            <span className="opacity-60">{section.iconEmoji}</span>
            <span className={isActive ? "text-slate-200" : "text-slate-600 hover:text-slate-400"}>
              {t(section.labelKey)}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
