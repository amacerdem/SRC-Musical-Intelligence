/* ── CharacterAvatar — Parametric SVG Character (React Native) ────────── */
import React from "react";
import Svg, { G, Path } from "react-native-svg";
import type { CharacterAvatarProps } from "./types";
import { FAMILY_HEAD } from "./types";
import { CHARACTER_CONFIGS } from "./character-configs";
import { HeadPart } from "./parts/heads";
import { BodyPart } from "./parts/bodies";
import { EyesPart } from "./parts/eyes";
import { MouthPart } from "./parts/mouths";
import { HairPart } from "./parts/hair";
import { ClothingPart } from "./parts/clothing";
import { AccessoryPart } from "./parts/accessories";
import { AuraPart, CrownPart, WingsPart } from "./parts/auras";

export function CharacterAvatar({
  personaId,
  color,
  family,
  size = 200,
  level = 1,
  showAura = false,
}: CharacterAvatarProps) {
  const config = CHARACTER_CONFIGS[personaId];
  if (!config) return null;

  const headShape = FAMILY_HEAD[family];
  const uid = `p${personaId}`;
  const height = size * 1.4;

  return (
    <Svg viewBox="0 0 200 280" width={size} height={height}>
      {/* Layer 0: Background aura */}
      {showAura && <AuraPart color={color} level={level} id={uid} />}

      {/* Layer 1: Wings (level 12) */}
      {level >= 12 && <WingsPart color={color} id={uid} />}

      {/* Layer 2: Clothing */}
      <ClothingPart style={config.clothing} color={color} />

      {/* Layer 3: Body */}
      <BodyPart shape={headShape} color={color} />

      {/* Layer 4: Head */}
      <HeadPart shape={headShape} />

      {/* Layer 5: Hair */}
      <HairPart style={config.hair} color={color} />

      {/* Layer 6: Eyes */}
      <EyesPart style={config.eyes} color={color} />

      {/* Layer 7: Mouth */}
      <MouthPart style={config.mouth} />

      {/* Layer 8: Accessories */}
      <AccessoryPart type={config.accessory} color={color} />

      {/* Layer 9: Crown (level 11+) */}
      {level >= 11 && <CrownPart color={color} id={uid} />}

      {/* Layer 10: Nose */}
      <NosePart />
    </Svg>
  );
}

function NosePart() {
  return (
    <Path
      d="M98 84 Q100 88 102 84"
      stroke="#D4B08C"
      strokeWidth="1.2"
      fill="none"
      opacity="0.4"
    />
  );
}
