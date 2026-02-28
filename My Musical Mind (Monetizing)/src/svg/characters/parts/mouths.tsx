/* ── Mouth Styles ────────────────────────────────────────────────────── */
import React from "react";
import type { MouthStyle } from "../types";

/* ── Palette ─────────────────────────────────────────────────────────── */
const LIP_MAIN   = "#C4846A";   // warm base
const LIP_UPPER  = "#B07058";   // upper lip shadow (darker)
const LIP_LOWER  = "#D4917E";   // lower lip highlight (lighter)
const LIP_CORNER = "#8E5A48";   // corner shadow dots
const TEETH      = "white";
const TEETH_OPACITY = 0.7;
const PHILTRUM   = "#BF7D68";   // subtle cupid's-bow lines
const DIMPLE     = "#B5705A";   // smile-line / dimple color

/* ── Philtrum — two tiny vertical lines above upper lip ──────────────── */
const Philtrum = ({ cx = 100, top = 87, bottom = 90.5 }: { cx?: number; top?: number; bottom?: number }) => (
  <g opacity="0.22">
    <line x1={cx - 1.4} y1={top} x2={cx - 1.1} y2={bottom} stroke={PHILTRUM} strokeWidth="0.5" strokeLinecap="round" />
    <line x1={cx + 1.4} y1={top} x2={cx + 1.1} y2={bottom} stroke={PHILTRUM} strokeWidth="0.5" strokeLinecap="round" />
  </g>
);

/* ── Lip corner shadow dots ──────────────────────────────────────────── */
const LipCorners = ({ left, right }: { left: [number, number]; right: [number, number] }) => (
  <g>
    <circle cx={left[0]} cy={left[1]} r="0.7" fill={LIP_CORNER} opacity="0.35" />
    <circle cx={right[0]} cy={right[1]} r="0.7" fill={LIP_CORNER} opacity="0.35" />
  </g>
);

/* ── Dimples / smile lines ───────────────────────────────────────────── */
const Dimples = ({ left, right, size = "normal" }: {
  left: [number, number]; right: [number, number]; size?: "normal" | "subtle"
}) => {
  const opacity = size === "subtle" ? 0.15 : 0.22;
  const len = size === "subtle" ? 2 : 3;
  return (
    <g opacity={opacity}>
      <path
        d={`M${left[0]} ${left[1]} Q${left[0] - 1} ${left[1] + len * 0.5} ${left[0] - 0.5} ${left[1] + len}`}
        stroke={DIMPLE} strokeWidth="0.6" fill="none" strokeLinecap="round"
      />
      <path
        d={`M${right[0]} ${right[1]} Q${right[0] + 1} ${right[1] + len * 0.5} ${right[0] + 0.5} ${right[1] + len}`}
        stroke={DIMPLE} strokeWidth="0.6" fill="none" strokeLinecap="round"
      />
    </g>
  );
};

/* ──────────────────────────────────────────────────────────────────────
   SMIRK — Alchemists: asymmetric, one corner raised, confident
   ────────────────────────────────────────────────────────────────────── */
const SmirkMouth = ({ color }: { color?: string }) => {
  const accent = color || LIP_MAIN;
  return (
    <g>
      {/* Philtrum hint */}
      <Philtrum cx={100} top={87.5} bottom={91} />

      {/* Upper lip — asymmetric, left corner flat, right corner rises */}
      <path
        d="M91 93.5 Q95 92 100 92.5 Q105 92 109 91"
        stroke={LIP_UPPER} strokeWidth="1.6" fill="none" strokeLinecap="round"
      />
      {/* Upper lip fill / body */}
      <path
        d="M91 93.5 Q95 92 100 92.5 Q105 92 109 91 Q106 93.5 100 94 Q95 94 91 93.5 Z"
        fill={LIP_UPPER} opacity="0.55"
      />

      {/* Lower lip — softer, slightly thicker on one side */}
      <path
        d="M92 94 Q97 96.5 103 96 Q107 95 109 93"
        stroke={LIP_LOWER} strokeWidth="1.3" fill="none" strokeLinecap="round"
      />
      {/* Lower lip fill */}
      <path
        d="M92 94 Q97 96.5 103 96 Q107 95 109 93 Q106 93.5 100 94 Q95 94 92 94 Z"
        fill={LIP_LOWER} opacity="0.4"
      />

      {/* Right corner upturn — the smirk accent */}
      <path
        d="M108 91.5 Q110 90 111 91"
        stroke={accent} strokeWidth="0.9" fill="none" opacity="0.6" strokeLinecap="round"
      />

      {/* Lip corners */}
      <LipCorners left={[90.5, 93.8]} right={[109.5, 91.5]} />

      {/* Subtle dimple on the raised side */}
      <path
        d="M111 91.5 Q112 93 111.5 94.5"
        stroke={DIMPLE} strokeWidth="0.5" fill="none" opacity="0.18" strokeLinecap="round"
      />
    </g>
  );
};

/* ──────────────────────────────────────────────────────────────────────
   NEUTRAL-PRECISE — Architects: thin, controlled, perfectly horizontal
   ────────────────────────────────────────────────────────────────────── */
const NeutralPreciseMouth = ({ color }: { color?: string }) => (
  <g>
    {/* Philtrum hint */}
    <Philtrum cx={100} top={88} bottom={91.5} />

    {/* Upper lip — thin, precise horizontal with minimal cupid's bow */}
    <path
      d="M90 93 Q95 92.2 100 92.5 Q105 92.2 110 93"
      stroke={LIP_UPPER} strokeWidth="1.2" fill="none" strokeLinecap="round"
    />
    {/* Upper lip subtle fill */}
    <path
      d="M90 93 Q95 92.2 100 92.5 Q105 92.2 110 93 Q105 93.5 100 93.6 Q95 93.5 90 93 Z"
      fill={LIP_UPPER} opacity="0.35"
    />

    {/* Lip seam — the defining horizontal line */}
    <line
      x1="91" y1="93.5" x2="109" y2="93.5"
      stroke={LIP_MAIN} strokeWidth="1.1" strokeLinecap="round"
    />

    {/* Lower lip — very subtle, controlled */}
    <path
      d="M92 94 Q100 95.5 108 94"
      stroke={LIP_LOWER} strokeWidth="0.9" fill="none" strokeLinecap="round"
    />
    {/* Lower lip fill */}
    <path
      d="M92 94 Q100 95.5 108 94 Q104 93.8 100 93.6 Q96 93.8 92 94 Z"
      fill={LIP_LOWER} opacity="0.3"
    />

    {/* Lip corners — precise dots */}
    <LipCorners left={[90, 93.2]} right={[110, 93.2]} />

    {/* Lower lip center highlight */}
    <ellipse cx="100" cy="94.5" rx="4" ry="0.6" fill={LIP_LOWER} opacity="0.15" />
  </g>
);

/* ──────────────────────────────────────────────────────────────────────
   OPEN-SMILE — Explorers: teeth showing, wide, energetic
   ────────────────────────────────────────────────────────────────────── */
const OpenSmileMouth = ({ color }: { color?: string }) => {
  const accent = color || LIP_MAIN;
  return (
    <g>
      {/* Philtrum hint */}
      <Philtrum cx={100} top={87} bottom={90} />

      {/* Upper lip — wide arc, pronounced cupid's bow */}
      <path
        d="M88 92 Q93 90.5 97 91 Q100 89.5 103 91 Q107 90.5 112 92"
        stroke={LIP_UPPER} strokeWidth="1.5" fill="none" strokeLinecap="round"
      />
      {/* Upper lip fill */}
      <path
        d="M88 92 Q93 90.5 97 91 Q100 89.5 103 91 Q107 90.5 112 92 Q106 93 100 93 Q94 93 88 92 Z"
        fill={LIP_UPPER} opacity="0.5"
      />

      {/* Mouth opening — dark interior */}
      <path
        d="M90 93 Q100 100 110 93"
        fill="#1a1018" opacity="0.7"
      />

      {/* Teeth — upper row */}
      <path
        d="M93 93 L93 95 Q100 95.5 107 95 L107 93 Z"
        fill={TEETH} opacity={TEETH_OPACITY}
      />
      {/* Tooth line separations */}
      <g stroke="#e0d8d0" strokeWidth="0.3" opacity="0.35">
        <line x1="96" y1="93" x2="96" y2="95" />
        <line x1="100" y1="93" x2="100" y2="95.2" />
        <line x1="104" y1="93" x2="104" y2="95" />
      </g>

      {/* Lower lip — full, open curve */}
      <path
        d="M89 93 Q94 93.5 100 100 Q106 93.5 111 93"
        stroke={LIP_LOWER} strokeWidth="1.4" fill="none" strokeLinecap="round"
      />
      {/* Lower lip fill — slight highlight */}
      <path
        d="M92 97 Q100 100 108 97 Q104 99 100 99.5 Q96 99 92 97 Z"
        fill={LIP_LOWER} opacity="0.35"
      />

      {/* Lip corners */}
      <LipCorners left={[88, 92.5]} right={[112, 92.5]} />

      {/* Smile lines / dimples */}
      <Dimples left={[87, 92]} right={[113, 92]} />

      {/* Lower lip center shine */}
      <ellipse cx="100" cy="98" rx="3.5" ry="0.8" fill={TEETH} opacity="0.08" />
    </g>
  );
};

/* ──────────────────────────────────────────────────────────────────────
   GENTLE-SMILE — Anchors: soft curve, warm, no teeth, fuller lips
   ────────────────────────────────────────────────────────────────────── */
const GentleSmileMouth = ({ color }: { color?: string }) => {
  const accent = color || LIP_MAIN;
  return (
    <g>
      {/* Philtrum hint */}
      <Philtrum cx={100} top={87.5} bottom={91} />

      {/* Upper lip — soft cupid's bow, fuller shape */}
      <path
        d="M90 93 Q94 91.5 98 92 Q100 91 102 92 Q106 91.5 110 93"
        stroke={LIP_UPPER} strokeWidth="1.4" fill="none" strokeLinecap="round"
      />
      {/* Upper lip fill */}
      <path
        d="M90 93 Q94 91.5 98 92 Q100 91 102 92 Q106 91.5 110 93 Q105 93.8 100 94 Q95 93.8 90 93 Z"
        fill={LIP_UPPER} opacity="0.45"
      />

      {/* Lip seam — gentle upward curve */}
      <path
        d="M90 93.5 Q100 97 110 93.5"
        stroke={LIP_MAIN} strokeWidth="1.2" fill="none" strokeLinecap="round"
      />

      {/* Lower lip — full, warm, rounded */}
      <path
        d="M91 94 Q95 97 100 97.5 Q105 97 109 94"
        stroke={LIP_LOWER} strokeWidth="1.2" fill="none" strokeLinecap="round"
      />
      {/* Lower lip fill */}
      <path
        d="M91 94 Q95 97 100 97.5 Q105 97 109 94 Q106 94 100 94.5 Q94 94 91 94 Z"
        fill={LIP_LOWER} opacity="0.35"
      />

      {/* Lower lip center highlight — warmth */}
      <ellipse cx="100" cy="96" rx="4.5" ry="1" fill={LIP_LOWER} opacity="0.18" />

      {/* Lip corners */}
      <LipCorners left={[89.5, 93.5]} right={[110.5, 93.5]} />

      {/* Soft dimples */}
      <Dimples left={[89, 93]} right={[111, 93]} size="subtle" />

      {/* Warm accent glow behind lower lip */}
      <ellipse cx="100" cy="95.5" rx="7" ry="2" fill={accent} opacity="0.06" />
    </g>
  );
};

/* ──────────────────────────────────────────────────────────────────────
   GRIN — Kineticists: very wide, teeth showing, energetic, dimples
   ────────────────────────────────────────────────────────────────────── */
const GrinMouth = ({ color }: { color?: string }) => {
  const accent = color || LIP_MAIN;
  return (
    <g>
      {/* Philtrum hint */}
      <Philtrum cx={100} top={86.5} bottom={89.5} />

      {/* Upper lip — wide, pronounced cupid's bow */}
      <path
        d="M85 91 Q91 89 96 90 Q100 88.5 104 90 Q109 89 115 91"
        stroke={LIP_UPPER} strokeWidth="1.6" fill="none" strokeLinecap="round"
      />
      {/* Upper lip fill */}
      <path
        d="M85 91 Q91 89 96 90 Q100 88.5 104 90 Q109 89 115 91 Q108 92.5 100 92.5 Q92 92.5 85 91 Z"
        fill={LIP_UPPER} opacity="0.5"
      />

      {/* Mouth opening — wide dark interior */}
      <path
        d="M87 92.5 Q100 103 113 92.5 Z"
        fill="#1a1018" opacity="0.65"
      />

      {/* Teeth — upper row, wide */}
      <path
        d="M90 92.5 L90 95 Q100 96 110 95 L110 92.5 Z"
        fill={TEETH} opacity={TEETH_OPACITY}
      />
      {/* Tooth line separations */}
      <g stroke="#e0d8d0" strokeWidth="0.3" opacity="0.3">
        <line x1="94" y1="92.5" x2="94" y2="95.2" />
        <line x1="97" y1="92.5" x2="97" y2="95.5" />
        <line x1="100" y1="92.5" x2="100" y2="95.7" />
        <line x1="103" y1="92.5" x2="103" y2="95.5" />
        <line x1="106" y1="92.5" x2="106" y2="95.2" />
      </g>

      {/* Lower teeth hint — subtle */}
      <path
        d="M93 99 L93 97.5 Q100 97 107 97.5 L107 99 Z"
        fill={TEETH} opacity="0.3"
      />

      {/* Lower lip — wide, energetic arc */}
      <path
        d="M86 92.5 Q93 93 100 103 Q107 93 114 92.5"
        stroke={LIP_LOWER} strokeWidth="1.5" fill="none" strokeLinecap="round"
      />
      {/* Lower lip fill highlight */}
      <path
        d="M91 99 Q100 103 109 99 Q105 101 100 101.5 Q95 101 91 99 Z"
        fill={LIP_LOWER} opacity="0.35"
      />

      {/* Lip corners */}
      <LipCorners left={[85, 91.5]} right={[115, 91.5]} />

      {/* Prominent dimples */}
      <Dimples left={[84, 91]} right={[116, 91]} />

      {/* Extra crinkle lines at corners for energy */}
      <path
        d="M84 90 Q83 91 83.5 92.5"
        stroke={DIMPLE} strokeWidth="0.45" fill="none" opacity="0.16" strokeLinecap="round"
      />
      <path
        d="M116 90 Q117 91 116.5 92.5"
        stroke={DIMPLE} strokeWidth="0.45" fill="none" opacity="0.16" strokeLinecap="round"
      />
    </g>
  );
};

/* ──────────────────────────────────────────────────────────────────────
   FOCUSED — concentrated, small "o", pursed lips
   ────────────────────────────────────────────────────────────────────── */
const FocusedMouth = ({ color }: { color?: string }) => (
  <g>
    {/* Philtrum hint */}
    <Philtrum cx={100} top={88} bottom={91} />

    {/* Upper lip — pursed, drawn inward */}
    <path
      d="M95 92.5 Q97 91.5 100 91.8 Q103 91.5 105 92.5"
      stroke={LIP_UPPER} strokeWidth="1.3" fill="none" strokeLinecap="round"
    />
    {/* Upper lip fill */}
    <path
      d="M95 92.5 Q97 91.5 100 91.8 Q103 91.5 105 92.5 Q103 93 100 93 Q97 93 95 92.5 Z"
      fill={LIP_UPPER} opacity="0.5"
    />

    {/* Mouth opening — small "o" */}
    <ellipse cx="100" cy="94" rx="3.5" ry="2.2" fill="#1a1018" opacity="0.55" />

    {/* Inner mouth shadow ring */}
    <ellipse cx="100" cy="94" rx="3.5" ry="2.2"
      stroke={LIP_MAIN} strokeWidth="0.4" fill="none" opacity="0.3"
    />

    {/* Lower lip — rounded, slightly protruding */}
    <path
      d="M95 95.5 Q97 97 100 97.2 Q103 97 105 95.5"
      stroke={LIP_LOWER} strokeWidth="1.3" fill="none" strokeLinecap="round"
    />
    {/* Lower lip fill */}
    <path
      d="M95 95.5 Q97 97 100 97.2 Q103 97 105 95.5 Q103 95.2 100 95.2 Q97 95.2 95 95.5 Z"
      fill={LIP_LOWER} opacity="0.4"
    />

    {/* Lower lip center highlight */}
    <ellipse cx="100" cy="96.2" rx="2.5" ry="0.5" fill={LIP_LOWER} opacity="0.2" />

    {/* Lip corners — close together for pursed look */}
    <LipCorners left={[94.5, 93.5]} right={[105.5, 93.5]} />

    {/* Chin tension lines below pursed mouth */}
    <path
      d="M98 97.5 Q100 98.5 102 97.5"
      stroke={DIMPLE} strokeWidth="0.4" fill="none" opacity="0.12" strokeLinecap="round"
    />
  </g>
);

/* ── Component Map & Export ──────────────────────────────────────────── */

const MOUTH_MAP: Record<MouthStyle, React.FC<{ color?: string }>> = {
  smirk: SmirkMouth,
  "neutral-precise": NeutralPreciseMouth,
  "open-smile": OpenSmileMouth,
  "gentle-smile": GentleSmileMouth,
  grin: GrinMouth,
  focused: FocusedMouth,
};

export function MouthPart({ style, color }: { style: MouthStyle; color?: string }) {
  const Component = MOUTH_MAP[style];
  return <Component color={color} />;
}
