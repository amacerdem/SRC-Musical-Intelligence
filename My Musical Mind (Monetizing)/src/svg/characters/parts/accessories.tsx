/* ── Accessories ─────────────────────────────────────────────────────── */
import React from "react";
import type { AccessoryType } from "../types";

interface AccessoryProps {
  type: AccessoryType;
  color: string;
}

/** Lightning bolt — #1 Dopamine Seeker */
const Lightning = ({ color }: { color: string }) => (
  <g transform="translate(140, 140)">
    <path d="M0 0 L-4 12 L2 10 L-2 24 L6 10 L0 12 Z" fill={color} opacity="0.7" />
  </g>
);

/** Tuning fork — #2 Harmonic Purist */
const TuningFork = ({ color }: { color: string }) => (
  <g transform="translate(56, 170)">
    <line x1="0" y1="0" x2="0" y2="20" stroke={color} strokeWidth="1.5" opacity="0.6" />
    <path d="M-3 0 Q-3 -8 0 -10 Q3 -8 3 0" stroke={color} strokeWidth="1.5" fill="none" opacity="0.6" />
  </g>
);

/** Compass — #3 Chaos Explorer */
const Compass = ({ color }: { color: string }) => (
  <g transform="translate(148, 150)">
    <circle cx="0" cy="0" r="7" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
    <circle cx="0" cy="0" r="1" fill={color} opacity="0.6" />
    <line x1="0" y1="-5" x2="0" y2="5" stroke={color} strokeWidth="0.8" opacity="0.5" />
    <line x1="-5" y1="0" x2="5" y2="0" stroke={color} strokeWidth="0.8" opacity="0.5" />
    {/* North indicator */}
    <path d="M0 -5 L-2 -2 L2 -2 Z" fill={color} opacity="0.6" />
  </g>
);

/** Metronome — #5 Resolution Junkie */
const Metronome = ({ color }: { color: string }) => (
  <g transform="translate(54, 164)">
    <path d="M-5 16 L0 -4 L5 16 Z" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
    {/* Pendulum arm */}
    <line x1="0" y1="14" x2="3" y2="0" stroke={color} strokeWidth="1.5" opacity="0.6" />
    <circle cx="3" cy="-1" r="1.5" fill={color} opacity="0.5" />
  </g>
);

/** Blueprint — #6 Tension Architect */
const Blueprint = ({ color }: { color: string }) => (
  <g transform="translate(142, 158)">
    <rect x="-6" y="-8" width="12" height="16" rx="1" fill={color} opacity="0.15" />
    {/* Grid lines */}
    <line x1="-4" y1="-4" x2="4" y2="-4" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <line x1="-4" y1="0" x2="4" y2="0" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <line x1="-4" y1="4" x2="4" y2="4" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <line x1="0" y1="-6" x2="0" y2="6" stroke={color} strokeWidth="0.5" opacity="0.3" />
  </g>
);

/** Yin-yang — #7 Contrast Addict */
const YinYang = ({ color }: { color: string }) => (
  <g transform="translate(142, 148)">
    <circle cx="0" cy="0" r="7" fill={color} opacity="0.2" />
    <path d="M0 -7 A7 7 0 0 1 0 7 A3.5 3.5 0 0 0 0 0 A3.5 3.5 0 0 1 0 -7 Z" fill={color} opacity="0.5" />
    <circle cx="0" cy="-3.5" r="1.2" fill={color} opacity="0.2" />
    <circle cx="0" cy="3.5" r="1.2" fill={color} opacity="0.6" />
  </g>
);

/** Rose — #8 Structural Romantic */
const Rose = ({ color }: { color: string }) => (
  <g transform="translate(54, 162)">
    {/* Petals */}
    <circle cx="0" cy="0" r="4" fill={color} opacity="0.3" />
    <circle cx="-2" cy="-2" r="3" fill={color} opacity="0.4" />
    <circle cx="2" cy="-1" r="3" fill={color} opacity="0.35" />
    <circle cx="0" cy="1" r="2.5" fill={color} opacity="0.5" />
    {/* Stem */}
    <line x1="0" y1="4" x2="-2" y2="16" stroke="#4a7c3f" strokeWidth="1" opacity="0.5" />
  </g>
);

/** Magnifier — #9 Pattern Hunter */
const Magnifier = ({ color }: { color: string }) => (
  <g transform="translate(148, 154)">
    <circle cx="0" cy="0" r="6" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    <circle cx="0" cy="0" r="4" fill={color} opacity="0.08" />
    <line x1="4" y1="4" x2="10" y2="10" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
  </g>
);

/** Map — #10 Sonic Nomad */
const Map = ({ color }: { color: string }) => (
  <g transform="translate(146, 158)">
    <rect x="-7" y="-5" width="14" height="10" rx="1" fill={color} opacity="0.15" />
    {/* Fold lines */}
    <line x1="-2" y1="-5" x2="-2" y2="5" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <line x1="3" y1="-5" x2="3" y2="5" stroke={color} strokeWidth="0.5" opacity="0.3" />
    {/* Path line */}
    <path d="M-5 0 Q-2 -3 1 0 Q3 2 6 -1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.4" />
    {/* Pin */}
    <circle cx="5" cy="-2" r="1" fill={color} opacity="0.5" />
  </g>
);

/** Heart — #11 Emotional Anchor */
const Heart = ({ color }: { color: string }) => (
  <g transform="translate(140, 144)">
    <path
      d="M0 4 Q-6 -2 -6 -5 Q-6 -8 -3 -8 Q0 -8 0 -5 Q0 -8 3 -8 Q6 -8 6 -5 Q6 -2 0 4 Z"
      fill={color} opacity="0.5"
    />
  </g>
);

/** Drumstick — #12 Rhythmic Pulse */
const Drumstick = ({ color }: { color: string }) => (
  <g transform="translate(148, 150)">
    <line x1="0" y1="0" x2="-10" y2="18" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
    <circle cx="0" cy="-1" r="2.5" fill={color} opacity="0.4" />
  </g>
);

/** Cloud — #13 Tonal Dreamer */
const Cloud = ({ color }: { color: string }) => (
  <g transform="translate(144, 140)">
    <circle cx="0" cy="0" r="5" fill={color} opacity="0.15" />
    <circle cx="-4" cy="2" r="4" fill={color} opacity="0.12" />
    <circle cx="4" cy="1" r="4.5" fill={color} opacity="0.12" />
    <circle cx="0" cy="3" r="3.5" fill={color} opacity="0.1" />
  </g>
);

/** Lightning pair — #14 Dynamic Storm */
const LightningPair = ({ color }: { color: string }) => (
  <g>
    <g transform="translate(46, 148)">
      <path d="M0 0 L-3 10 L2 8 L-1 20 L5 8 L0 10 Z" fill={color} opacity="0.6" />
    </g>
    <g transform="translate(150, 142)">
      <path d="M0 0 L-3 10 L2 8 L-1 20 L5 8 L0 10 Z" fill={color} opacity="0.6" />
    </g>
  </g>
);

/** Headphones — #15 Quiet Observer */
const Headphones = ({ color }: { color: string }) => (
  <g>
    {/* Band */}
    <path d="M72 56 Q72 30 100 26 Q128 30 128 56" stroke={color} strokeWidth="2.5" fill="none" opacity="0.5" />
    {/* Ear cups */}
    <ellipse cx="70" cy="62" rx="5" ry="7" fill={color} opacity="0.4" />
    <ellipse cx="130" cy="62" rx="5" ry="7" fill={color} opacity="0.4" />
    <ellipse cx="70" cy="62" rx="3" ry="5" fill={color} opacity="0.2" />
    <ellipse cx="130" cy="62" rx="3" ry="5" fill={color} opacity="0.2" />
  </g>
);

/** Wrench — #16 Groove Mechanic */
const Wrench = ({ color }: { color: string }) => (
  <g transform="translate(148, 156)">
    <line x1="0" y1="0" x2="-8" y2="16" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
    {/* Wrench head */}
    <path d="M-3 -2 Q0 -6 3 -2 L2 2 L-2 2 Z" fill={color} opacity="0.4" />
  </g>
);

/** Wind effect — #17 Ambient Flow */
const Wind = ({ color }: { color: string }) => (
  <g>
    <path d="M140 80 Q152 78 158 82" stroke={color} strokeWidth="1" fill="none" opacity="0.3" strokeLinecap="round" />
    <path d="M142 88 Q156 86 164 90" stroke={color} strokeWidth="1.5" fill="none" opacity="0.25" strokeLinecap="round" />
    <path d="M140 96 Q150 94 156 98" stroke={color} strokeWidth="1" fill="none" opacity="0.2" strokeLinecap="round" />
  </g>
);

/** Theater mask — #18 Dramatic Arc */
const Mask = ({ color }: { color: string }) => (
  <g transform="translate(146, 152)">
    {/* Comedy mask */}
    <path d="M-6 -4 Q-6 -8 0 -8 Q6 -8 6 -4 Q6 2 0 4 Q-6 2 -6 -4 Z" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <circle cx="-2" cy="-4" r="1" fill={color} opacity="0.4" />
    <circle cx="2" cy="-4" r="1" fill={color} opacity="0.4" />
    <path d="M-2 -1 Q0 2 2 -1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.4" />
  </g>
);

/** Binoculars — #19 Curious Wanderer */
const Binoculars = ({ color }: { color: string }) => (
  <g transform="translate(148, 156)">
    <circle cx="-3" cy="0" r="4" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <circle cx="3" cy="0" r="4" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <rect x="-1.5" y="-2" width="3" height="4" fill={color} opacity="0.2" />
  </g>
);

/** Ruler — #20 Precision Mind */
const Ruler = ({ color }: { color: string }) => (
  <g transform="translate(148, 158)">
    <rect x="-3" y="-12" width="6" height="24" rx="1" fill={color} opacity="0.15" />
    {/* Tick marks */}
    {[-10, -6, -2, 2, 6, 10].map((y) => (
      <line key={y} x1="-3" y1={y} x2="-1" y2={y} stroke={color} strokeWidth="0.5" opacity="0.3" />
    ))}
  </g>
);

/** Fire — #21 Raw Energy */
const Fire = ({ color }: { color: string }) => (
  <g transform="translate(148, 148)">
    <path d="M0 8 Q-4 2 -3 -2 Q-2 2 0 -6 Q2 2 3 -2 Q4 2 0 8 Z" fill={color} opacity="0.5" />
    <path d="M0 6 Q-2 2 0 -2 Q2 2 0 6 Z" fill={color} opacity="0.3" />
  </g>
);

/** Cassette — #22 Nostalgic Soul */
const Cassette = ({ color }: { color: string }) => (
  <g transform="translate(146, 160)">
    <rect x="-8" y="-5" width="16" height="10" rx="1.5" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    {/* Reels */}
    <circle cx="-3" cy="0" r="2.5" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <circle cx="3" cy="0" r="2.5" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <circle cx="-3" cy="0" r="0.8" fill={color} opacity="0.3" />
    <circle cx="3" cy="0" r="0.8" fill={color} opacity="0.3" />
    {/* Tape window */}
    <rect x="-5" y="2.5" width="10" height="2" rx="0.5" fill={color} opacity="0.1" />
  </g>
);

/** Thorns — #23 Edge Runner */
const Thorns = ({ color }: { color: string }) => (
  <g>
    {/* Thorn bracelet on left wrist */}
    <path d="M56 178 L52 174 L58 176" fill={color} opacity="0.4" />
    <path d="M60 180 L56 176 L62 178" fill={color} opacity="0.4" />
    <path d="M58 184 L54 180 L60 182" fill={color} opacity="0.4" />
  </g>
);

/** Palette — #24 Renaissance Mind */
const Palette = ({ color }: { color: string }) => (
  <g transform="translate(150, 148)">
    {/* Palette shape */}
    <ellipse cx="0" cy="0" rx="8" ry="6" fill={color} opacity="0.15" />
    {/* Thumb hole */}
    <circle cx="-3" cy="2" r="2" fill="#1a1a2e" />
    {/* Paint blobs */}
    <circle cx="-2" cy="-3" r="1.5" fill="#E040FB" opacity="0.5" />
    <circle cx="2" cy="-2" r="1.5" fill="#38BDF8" opacity="0.5" />
    <circle cx="4" cy="1" r="1.5" fill="#84CC16" opacity="0.5" />
    <circle cx="1" cy="3" r="1.5" fill="#FBBF24" opacity="0.5" />
  </g>
);

/** No accessory */
const NoAccessory = () => null;

const ACCESSORY_MAP: Record<AccessoryType, React.FC<{ color: string }>> = {
  lightning: Lightning,
  "tuning-fork": TuningFork,
  compass: Compass,
  metronome: Metronome,
  blueprint: Blueprint,
  "yin-yang": YinYang,
  rose: Rose,
  magnifier: Magnifier,
  map: Map,
  heart: Heart,
  drumstick: Drumstick,
  cloud: Cloud,
  "lightning-pair": LightningPair,
  headphones: Headphones,
  wrench: Wrench,
  wind: Wind,
  mask: Mask,
  binoculars: Binoculars,
  ruler: Ruler,
  fire: Fire,
  cassette: Cassette,
  thorns: Thorns,
  palette: Palette,
  none: NoAccessory as React.FC<{ color: string }>,
};

export function AccessoryPart({ type, color }: AccessoryProps) {
  const Component = ACCESSORY_MAP[type];
  return <Component color={color} />;
}
