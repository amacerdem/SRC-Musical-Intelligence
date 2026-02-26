/* ── Head Shapes ─────────────────────────────────────────────────────── */
import React from "react";
import type { HeadShape } from "../types";

interface HeadProps {
  shape: HeadShape;
  skinColor?: string;
}

/* Skin base = warm neutral */
const SKIN = "#F0D5B8";
const SKIN_SHADOW = "#D4B08C";

/** Angular — Alchemists: pointed chin, high cheekbones */
const AngularHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <g>
    {/* Neck */}
    <rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    {/* Head shape — angular jaw tapering to pointed chin */}
    <path
      d="M72 70 Q72 38 100 32 Q128 38 128 70 L124 96 Q116 112 100 116 Q84 112 76 96 Z"
      fill={skinColor}
    />
    {/* Cheekbone accents */}
    <path d="M76 72 Q80 76 82 80" stroke={SKIN_SHADOW} strokeWidth="1.5" fill="none" opacity="0.4" />
    <path d="M124 72 Q120 76 118 80" stroke={SKIN_SHADOW} strokeWidth="1.5" fill="none" opacity="0.4" />
  </g>
);

/** Geometric — Architects: square jaw, symmetric, structured */
const GeometricHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <g>
    <rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    <path
      d="M74 68 Q74 36 100 32 Q126 36 126 68 L126 92 Q122 110 100 114 Q78 110 74 92 Z"
      fill={skinColor}
    />
    {/* Jaw line accent */}
    <path d="M78 92 L100 108 L122 92" stroke={SKIN_SHADOW} strokeWidth="1" fill="none" opacity="0.25" />
  </g>
);

/** Fluid — Explorers: slightly asymmetric, dynamic */
const FluidHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <g>
    <rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    <path
      d="M73 72 Q71 38 98 32 Q128 36 129 68 L126 94 Q118 112 100 116 Q82 114 76 96 Z"
      fill={skinColor}
    />
  </g>
);

/** Round — Anchors: full circle, warm, approachable */
const RoundHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <g>
    <rect x="90" y="110" width="20" height="14" rx="4" fill={skinColor} />
    <ellipse cx="100" cy="74" rx="30" ry="34" fill={skinColor} />
    {/* Soft cheek blush */}
    <circle cx="80" cy="82" r="6" fill="#F4A0A0" opacity="0.2" />
    <circle cx="120" cy="82" r="6" fill="#F4A0A0" opacity="0.2" />
  </g>
);

/** Athletic — Kineticists: strong jaw, wide, powerful */
const AthleticHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <g>
    <rect x="88" y="108" width="24" height="16" rx="4" fill={skinColor} />
    <path
      d="M70 68 Q70 34 100 30 Q130 34 130 68 L130 90 Q126 110 100 114 Q74 110 70 90 Z"
      fill={skinColor}
    />
    {/* Strong jaw accents */}
    <path d="M74 88 Q86 102 100 106 Q114 102 126 88" stroke={SKIN_SHADOW} strokeWidth="1.2" fill="none" opacity="0.3" />
  </g>
);

const HEAD_MAP: Record<HeadShape, React.FC<{ skinColor?: string }>> = {
  angular: AngularHead,
  geometric: GeometricHead,
  fluid: FluidHead,
  round: RoundHead,
  athletic: AthleticHead,
};

export function HeadPart({ shape, skinColor }: HeadProps) {
  const Component = HEAD_MAP[shape];
  return <Component skinColor={skinColor} />;
}
