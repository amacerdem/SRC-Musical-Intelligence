/* ── Persona Narrative Sections ─────────────────────────────────────
 *  8 sections per persona, 16personalities-style.
 *  All content is via i18n keys: `persona.{id}.section.{sectionKey}`
 *  ──────────────────────────────────────────────────────────────── */

export interface NarrativeSection {
  key: string;
  labelKey: string;     // i18n key for sidebar label
  iconEmoji: string;    // sidebar icon
}

/** 8 narrative sections in display order */
export const NARRATIVE_SECTIONS: NarrativeSection[] = [
  { key: "intro",       labelKey: "persona.sections.intro",       iconEmoji: "◈" },
  { key: "listening",   labelKey: "persona.sections.listening",   iconEmoji: "♫" },
  { key: "emotion",     labelKey: "persona.sections.emotion",     iconEmoji: "◉" },
  { key: "social",      labelKey: "persona.sections.social",      iconEmoji: "⊕" },
  { key: "growth",      labelKey: "persona.sections.growth",      iconEmoji: "↗" },
  { key: "famous",      labelKey: "persona.sections.famous",      iconEmoji: "★" },
  { key: "compatible",  labelKey: "persona.sections.compatible",  iconEmoji: "⇌" },
  { key: "shadow",      labelKey: "persona.sections.shadow",      iconEmoji: "◐" },
];

/** Build the i18n key for a persona section body text */
export function sectionI18nKey(personaId: number, sectionKey: string): string {
  return `persona.${personaId}.section.${sectionKey}`;
}
