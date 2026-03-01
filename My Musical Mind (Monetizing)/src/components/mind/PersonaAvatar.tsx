/* ── PersonaAvatar — Wrapper that prefers custom PNG over SVG CharacterAvatar ── */
import { CharacterAvatar } from "@/svg/characters";
import type { NeuralFamily } from "@/types/mind";

/** Custom transparent-PNG persona images (override SVG CharacterAvatar) */
const PERSONA_IMAGES: Record<number, string> = {
  24: "/avatars/persona-24-renaissance-mind.png",
};

interface PersonaAvatarProps {
  personaId: number;
  color: string;
  family: NeuralFamily;
  size?: number;
  level?: number;
  showAura?: boolean;
  className?: string;
}

export function PersonaAvatar({
  personaId,
  color,
  family,
  size = 52,
  level = 1,
  showAura = false,
  className,
}: PersonaAvatarProps) {
  const imageSrc = PERSONA_IMAGES[personaId];

  if (imageSrc) {
    return (
      <img
        src={imageSrc}
        alt={`Persona ${personaId}`}
        className={`object-contain ${className ?? ""}`}
        style={{ width: size, height: size * 1.4 }}
      />
    );
  }

  return (
    <CharacterAvatar
      personaId={personaId}
      color={color}
      family={family}
      size={size}
      level={level}
      showAura={showAura}
      className={className}
    />
  );
}
