/* ── Body Shapes ─────────────────────────────────────────────────────── */
import React from "react";
import type { HeadShape } from "../types";

interface BodyProps {
  shape: HeadShape;
  color: string;
}

const SKIN = "#F0D5B8";

/** Alchemists: Slim, elongated, dynamic pose — slight lean */
const AngularBody = ({ color }: { color: string }) => (
  <g>
    {/* Torso */}
    <path
      d="M82 124 Q78 126 74 160 L72 210 Q86 218 100 220 Q114 218 128 210 L126 160 Q122 126 118 124 Z"
      fill="#1a1a2e"
    />
    {/* Accent trim */}
    <path d="M82 124 L100 130 L118 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.6" />
    {/* Arms */}
    <path d="M74 134 L58 180 L62 182" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    <path d="M126 134 L142 176 L138 178" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    {/* Legs */}
    <path d="M88 220 L84 264 L80 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <path d="M112 220 L116 264 L120 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    {/* Shoes */}
    <ellipse cx="78" cy="270" rx="10" ry="4" fill="#2d2d44" />
    <ellipse cx="122" cy="270" rx="10" ry="4" fill="#2d2d44" />
  </g>
);

/** Architects: Upright, structured, straight posture */
const GeometricBody = ({ color }: { color: string }) => (
  <g>
    <path
      d="M80 124 L76 160 L76 210 Q88 218 100 220 Q112 218 124 210 L124 160 L120 124 Z"
      fill="#1a1a2e"
    />
    {/* Structured collar line */}
    <path d="M84 124 L100 128 L116 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.6" />
    {/* Vertical center line */}
    <line x1="100" y1="130" x2="100" y2="210" stroke={color} strokeWidth="0.5" opacity="0.2" />
    {/* Arms */}
    <path d="M76 134 L62 178 L66 180" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    <path d="M124 134 L138 178 L134 180" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    {/* Legs */}
    <path d="M90 220 L88 264 L84 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <path d="M110 220 L112 264 L116 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <ellipse cx="82" cy="270" rx="10" ry="4" fill="#2d2d44" />
    <ellipse cx="118" cy="270" rx="10" ry="4" fill="#2d2d44" />
  </g>
);

/** Explorers: Relaxed, one arm raised, movement implied */
const FluidBody = ({ color }: { color: string }) => (
  <g>
    <path
      d="M80 124 Q76 128 74 160 L72 210 Q86 220 100 222 Q114 220 128 210 L126 160 Q122 128 118 124 Z"
      fill="#1a1a2e"
    />
    <path d="M82 124 Q100 132 118 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    {/* Left arm relaxed, right arm up */}
    <path d="M74 134 L56 184 L60 186" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    <path d="M126 134 L148 154 L152 148" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    {/* Legs — wider casual stance */}
    <path d="M86 222 L78 264 L74 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <path d="M114 222 L122 264 L126 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <ellipse cx="72" cy="270" rx="10" ry="4" fill="#2d2d44" />
    <ellipse cx="128" cy="270" rx="10" ry="4" fill="#2d2d44" />
  </g>
);

/** Anchors: Warm, relaxed, comfortable stance */
const RoundBody = ({ color }: { color: string }) => (
  <g>
    <path
      d="M78 124 Q74 130 72 160 L72 210 Q86 220 100 222 Q114 220 128 210 L128 160 Q126 130 122 124 Z"
      fill="#1a1a2e"
    />
    <path d="M82 124 Q100 132 118 124" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    {/* Arms — hands together / warm pose */}
    <path d="M72 134 L58 174 L66 186" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    <path d="M128 134 L142 174 L134 186" stroke={SKIN} strokeWidth="6" strokeLinecap="round" fill="none" />
    {/* Legs */}
    <path d="M90 222 L86 264 L82 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <path d="M110 222 L114 264 L118 268" stroke="#1a1a2e" strokeWidth="8" strokeLinecap="round" fill="none" />
    <ellipse cx="80" cy="270" rx="10" ry="4" fill="#2d2d44" />
    <ellipse cx="120" cy="270" rx="10" ry="4" fill="#2d2d44" />
  </g>
);

/** Kineticists: Wide shoulders, athletic, motion lines */
const AthleticBody = ({ color }: { color: string }) => (
  <g>
    {/* Wide-shoulder torso */}
    <path
      d="M76 124 Q70 128 68 160 L70 210 Q86 222 100 224 Q114 222 130 210 L132 160 Q130 128 124 124 Z"
      fill="#1a1a2e"
    />
    {/* Shoulder accent */}
    <path d="M76 124 L100 130 L124 124" stroke={color} strokeWidth="2" fill="none" opacity="0.6" />
    {/* Arms — one flexed */}
    <path d="M68 134 L50 170 L54 172" stroke={SKIN} strokeWidth="7" strokeLinecap="round" fill="none" />
    <path d="M132 134 L148 158 L144 148" stroke={SKIN} strokeWidth="7" strokeLinecap="round" fill="none" />
    {/* Legs — strong stance */}
    <path d="M86 224 L80 264 L76 268" stroke="#1a1a2e" strokeWidth="9" strokeLinecap="round" fill="none" />
    <path d="M114 224 L120 264 L124 268" stroke="#1a1a2e" strokeWidth="9" strokeLinecap="round" fill="none" />
    {/* Motion lines */}
    <line x1="46" y1="164" x2="38" y2="160" stroke={color} strokeWidth="1" opacity="0.3" />
    <line x1="44" y1="170" x2="36" y2="168" stroke={color} strokeWidth="1" opacity="0.2" />
    <ellipse cx="74" cy="270" rx="11" ry="4" fill="#2d2d44" />
    <ellipse cx="126" cy="270" rx="11" ry="4" fill="#2d2d44" />
  </g>
);

const BODY_MAP: Record<HeadShape, React.FC<{ color: string }>> = {
  angular: AngularBody,
  geometric: GeometricBody,
  fluid: FluidBody,
  round: RoundBody,
  athletic: AthleticBody,
};

export function BodyPart({ shape, color }: BodyProps) {
  const Component = BODY_MAP[shape];
  return <Component color={color} />;
}
