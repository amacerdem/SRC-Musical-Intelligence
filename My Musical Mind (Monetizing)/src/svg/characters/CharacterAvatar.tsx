/* ── CharacterAvatar — Detailed Parametric SVG Character ────────────── *
 *  High-fidelity character rendering with gradient shading, anatomical
 *  detail, neural-scientific motifs, and per-family visual identity.
 *
 *  ViewBox: 0 0 200 280 (200:280 aspect ratio)
 *  Coordinate anchors:
 *    Head center:  cx=100, top≈32, bottom≈112
 *    Neck:         y=108-124
 *    Body:         y=124-220
 *    Face:         eyes≈y74, nose≈y84, mouth≈y94
 *    Ears:         x≈70/130, y≈72-86
 * ──────────────────────────────────────────────────────────────────── */
import React from "react";
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
import type { NeuralFamily } from "../../types/mind";

/**
 * Shared SVG defs — skin gradients, shadow, glow filters, family motifs.
 * The `uid` prefix ensures unique IDs when multiple avatars render on screen.
 */
function SharedDefs({ uid, color, family }: { uid: string; color: string; family: NeuralFamily }) {
  const motif = FAMILY_MOTIFS[family];
  return (
    <defs>
      {/* Skin gradient — warm realistic tone */}
      <linearGradient id={`skin-${uid}`} x1="0" y1="0" x2="0.3" y2="1">
        <stop offset="0%" stopColor="#F5DCC4" />
        <stop offset="40%" stopColor="#F0D5B8" />
        <stop offset="100%" stopColor="#D9B896" />
      </linearGradient>

      {/* Skin shadow gradient — for under-chin, neck */}
      <linearGradient id={`skin-shadow-${uid}`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#D4B08C" />
        <stop offset="100%" stopColor="#C49A74" />
      </linearGradient>

      {/* Hair highlight gradient */}
      <linearGradient id={`hair-hi-${uid}`} x1="0.3" y1="0" x2="0.7" y2="1">
        <stop offset="0%" stopColor="white" stopOpacity="0.25" />
        <stop offset="100%" stopColor="white" stopOpacity="0" />
      </linearGradient>

      {/* Persona color glow for accents */}
      <radialGradient id={`accent-glow-${uid}`}>
        <stop offset="0%" stopColor={color} stopOpacity="0.4" />
        <stop offset="100%" stopColor={color} stopOpacity="0" />
      </radialGradient>

      {/* Subtle drop shadow filter */}
      <filter id={`shadow-${uid}`} x="-10%" y="-10%" width="120%" height="130%">
        <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#000" floodOpacity="0.15" />
      </filter>

      {/* Clothing fabric gradient */}
      <linearGradient id={`fabric-${uid}`} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stopColor="#22223a" />
        <stop offset="50%" stopColor="#1a1a2e" />
        <stop offset="100%" stopColor="#141424" />
      </linearGradient>

      {/* Eye iris gradient — persona color tinted */}
      <radialGradient id={`iris-${uid}`}>
        <stop offset="0%" stopColor={color} stopOpacity="0.6" />
        <stop offset="50%" stopColor="#2d2d44" stopOpacity="0.9" />
        <stop offset="100%" stopColor="#1a1a2e" />
      </radialGradient>

      {/* Family neural motif pattern */}
      <pattern id={`motif-${uid}`} x="0" y="0" width={motif.size} height={motif.size} patternUnits="userSpaceOnUse">
        {motif.elements.map((el, i) => (
          <React.Fragment key={i}>{el(color)}</React.Fragment>
        ))}
      </pattern>
    </defs>
  );
}

/** Family-specific neural decorative motifs — subtle patterns overlaid on clothing/body */
const FAMILY_MOTIFS: Record<NeuralFamily, { size: number; elements: ((c: string) => React.ReactNode)[] }> = {
  Alchemists: {
    size: 20,
    elements: [
      (c) => <path d="M2 10 L10 2 L18 10 L10 18 Z" stroke={c} strokeWidth="0.3" fill="none" opacity="0.08" />,
      (c) => <circle cx="10" cy="10" r="2" stroke={c} strokeWidth="0.2" fill="none" opacity="0.06" />,
    ],
  },
  Architects: {
    size: 16,
    elements: [
      (c) => <rect x="2" y="2" width="12" height="12" stroke={c} strokeWidth="0.3" fill="none" opacity="0.06" />,
      (c) => <line x1="8" y1="2" x2="8" y2="14" stroke={c} strokeWidth="0.2" opacity="0.05" />,
      (c) => <line x1="2" y1="8" x2="14" y2="8" stroke={c} strokeWidth="0.2" opacity="0.05" />,
    ],
  },
  Explorers: {
    size: 24,
    elements: [
      (c) => <path d="M4 12 Q12 4 20 12 Q12 20 4 12 Z" stroke={c} strokeWidth="0.3" fill="none" opacity="0.06" />,
      (c) => <circle cx="12" cy="12" r="1.5" fill={c} opacity="0.04" />,
    ],
  },
  Anchors: {
    size: 20,
    elements: [
      (c) => <circle cx="10" cy="10" r="6" stroke={c} strokeWidth="0.3" fill="none" opacity="0.05" />,
      (c) => <circle cx="10" cy="10" r="3" stroke={c} strokeWidth="0.2" fill="none" opacity="0.04" />,
    ],
  },
  Kineticists: {
    size: 18,
    elements: [
      (c) => <path d="M2 9 Q5 3 9 9 Q13 15 16 9" stroke={c} strokeWidth="0.3" fill="none" opacity="0.06" />,
      (c) => <line x1="9" y1="2" x2="9" y2="16" stroke={c} strokeWidth="0.15" opacity="0.04" />,
    ],
  },
};

/** Family neural decoration overlay — renders over clothing */
function FamilyDecor({ color, family, uid }: { color: string; family: NeuralFamily; uid: string }) {
  return (
    <g opacity="0.5" style={{ mixBlendMode: "screen" }}>
      {/* Subtle neural network nodes along shoulders/torso */}
      <circle cx="84" cy="132" r="1.2" fill={color} opacity="0.15" />
      <circle cx="116" cy="132" r="1.2" fill={color} opacity="0.15" />
      <circle cx="100" cy="155" r="1" fill={color} opacity="0.1" />
      {/* Connection lines */}
      <line x1="84" y1="132" x2="100" y2="155" stroke={color} strokeWidth="0.4" opacity="0.08" />
      <line x1="116" y1="132" x2="100" y2="155" stroke={color} strokeWidth="0.4" opacity="0.08" />
      {/* Pattern overlay on torso area */}
      <rect
        x="76" y="130" width="48" height="70" rx="4"
        fill={`url(#motif-${uid})`}
        opacity="0.6"
      />
    </g>
  );
}

/**
 * Renders a full-body 2D SVG character for a given persona.
 * Enhanced with gradient shading, anatomical detail, and neural motifs.
 */
export function CharacterAvatar({
  personaId,
  color,
  family,
  size = 200,
  level = 1,
  showAura = false,
  className,
}: CharacterAvatarProps) {
  const config = CHARACTER_CONFIGS[personaId];
  if (!config) return null;

  const headShape = FAMILY_HEAD[family];
  const uid = `p${personaId}`;
  const height = size * 1.4;

  return (
    <svg
      viewBox="0 0 200 280"
      width={size}
      height={height}
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label={`Persona ${personaId} character`}
    >
      {/* ── Shared gradients & filters ── */}
      <SharedDefs uid={uid} color={color} family={family} />

      {/* ── Layer 0: Background aura ── */}
      {showAura && <AuraPart color={color} level={level} id={uid} />}

      {/* ── Layer 1: Wings (level 12) ── */}
      {level >= 12 && <WingsPart color={color} id={uid} />}

      {/* ── Layer 2: Clothing overlays (cloaks etc behind body) ── */}
      <ClothingPart style={config.clothing} color={color} uid={uid} />

      {/* ── Layer 3: Body ── */}
      <BodyPart shape={headShape} color={color} uid={uid} />

      {/* ── Layer 3.5: Family neural decoration overlay ── */}
      <FamilyDecor color={color} family={family} uid={uid} />

      {/* ── Layer 4: Head ── */}
      <HeadPart shape={headShape} uid={uid} />

      {/* ── Layer 5: Hair ── */}
      <HairPart style={config.hair} color={color} uid={uid} />

      {/* ── Layer 6: Eyes ── */}
      <EyesPart style={config.eyes} color={color} uid={uid} />

      {/* ── Layer 7: Mouth ── */}
      <MouthPart style={config.mouth} color={color} />

      {/* ── Layer 8: Nose (refined) ── */}
      <NosePart uid={uid} />

      {/* ── Layer 9: Accessories ── */}
      <AccessoryPart type={config.accessory} color={color} />

      {/* ── Layer 10: Crown (level 11+) ── */}
      {level >= 11 && <CrownPart color={color} id={uid} />}
    </svg>
  );
}

/** Refined nose — bridge line + nostril hint */
function NosePart({ uid }: { uid: string }) {
  return (
    <g>
      {/* Nose bridge — very subtle */}
      <path d="M99 76 Q100 80 99.5 84" stroke="#D4B08C" strokeWidth="0.6" fill="none" opacity="0.25" />
      {/* Nose tip + nostrils */}
      <path d="M96 86 Q98 89 100 88 Q102 89 104 86" stroke="#D4B08C" strokeWidth="1" fill="none" opacity="0.35" />
      {/* Subtle nose shadow */}
      <ellipse cx="100" cy="87" rx="4" ry="2" fill="#D4B08C" opacity="0.08" />
    </g>
  );
}
