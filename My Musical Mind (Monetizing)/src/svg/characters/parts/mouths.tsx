/* ── Mouth Styles ────────────────────────────────────────────────────── */
import React from "react";
import type { MouthStyle } from "../types";

const MOUTH_COLOR = "#C4846A";

/** Smirk — Alchemists: confident half-smile */
const SmirkMouth = () => (
  <g>
    <path d="M92 94 Q100 96 108 92" stroke={MOUTH_COLOR} strokeWidth="1.8" fill="none" strokeLinecap="round" />
    <path d="M104 92 Q108 96 110 94" stroke={MOUTH_COLOR} strokeWidth="1" fill="none" opacity="0.5" />
  </g>
);

/** Neutral-precise — Architects: straight, controlled */
const NeutralPreciseMouth = () => (
  <g>
    <line x1="90" y1="94" x2="110" y2="94" stroke={MOUTH_COLOR} strokeWidth="1.6" strokeLinecap="round" />
  </g>
);

/** Open-smile — Explorers: energetic, open */
const OpenSmileMouth = () => (
  <g>
    <path d="M90 92 Q100 102 110 92" stroke={MOUTH_COLOR} strokeWidth="1.8" fill="none" strokeLinecap="round" />
    {/* Slight teeth hint */}
    <path d="M94 94 Q100 98 106 94" fill="white" opacity="0.7" />
  </g>
);

/** Gentle-smile — Anchors: warm, soft */
const GentleSmileMouth = () => (
  <g>
    <path d="M90 92 Q100 100 110 92" stroke={MOUTH_COLOR} strokeWidth="1.5" fill="none" strokeLinecap="round" />
  </g>
);

/** Grin — Kineticists: wide, energetic */
const GrinMouth = () => (
  <g>
    <path d="M86 90 Q100 104 114 90" stroke={MOUTH_COLOR} strokeWidth="2" fill="none" strokeLinecap="round" />
    <path d="M90 92 Q100 100 110 92" fill="white" opacity="0.6" />
  </g>
);

/** Focused — concentrated, slightly open */
const FocusedMouth = () => (
  <g>
    <ellipse cx="100" cy="94" rx="5" ry="3" fill={MOUTH_COLOR} opacity="0.7" />
    <ellipse cx="100" cy="93.5" rx="3.5" ry="1.5" fill="#1a1a2e" opacity="0.4" />
  </g>
);

const MOUTH_MAP: Record<MouthStyle, React.FC> = {
  smirk: SmirkMouth,
  "neutral-precise": NeutralPreciseMouth,
  "open-smile": OpenSmileMouth,
  "gentle-smile": GentleSmileMouth,
  grin: GrinMouth,
  focused: FocusedMouth,
};

export function MouthPart({ style }: { style: MouthStyle }) {
  const Component = MOUTH_MAP[style];
  return <Component />;
}
