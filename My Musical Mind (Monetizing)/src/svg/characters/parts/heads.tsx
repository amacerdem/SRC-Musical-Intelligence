/* ── Head Shapes — Detailed, anatomically refined ──────────────────────
 *  5 family variants with gradient skin, ears, jaw definition, neck
 *  shading, and subtle anatomical landmarks.
 * ──────────────────────────────────────────────────────────────────── */
import React from "react";
import type { HeadShape } from "../types";

interface HeadProps {
  shape: HeadShape;
  uid?: string;
}

const SKIN = "#F0D5B8";
const SKIN_HI = "#F8E4D0";
const SKIN_SHADOW = "#D4B08C";
const EAR_INNER = "#E0BFA0";

/** Angular — Alchemists: sharp jawline, high cheekbones, intensity */
const AngularHead = ({ uid }: { uid?: string }) => (
  <g>
    {/* Neck with shadow */}
    <rect x="89" y="106" width="22" height="18" rx="5" fill={SKIN} />
    <rect x="89" y="106" width="22" height="8" rx="3" fill={SKIN_SHADOW} opacity="0.3" />

    {/* Head — angular jaw tapering to pointed chin */}
    <path
      d="M72 68 Q72 36 100 30 Q128 36 128 68 L125 94 Q118 110 100 115 Q82 110 75 94 Z"
      fill={uid ? `url(#skin-${uid})` : SKIN}
    />

    {/* Forehead highlight */}
    <ellipse cx="100" cy="46" rx="18" ry="8" fill={SKIN_HI} opacity="0.25" />

    {/* Ears */}
    <path d="M72 66 Q66 62 64 72 Q62 82 68 86 Q70 80 72 76" fill={SKIN} />
    <path d="M67 70 Q66 76 68 80" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />
    <path d="M128 66 Q134 62 136 72 Q138 82 132 86 Q130 80 128 76" fill={SKIN} />
    <path d="M133 70 Q134 76 132 80" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />

    {/* Cheekbone accents */}
    <path d="M76 70 Q80 76 83 82" stroke={SKIN_SHADOW} strokeWidth="1.2" fill="none" opacity="0.3" />
    <path d="M124 70 Q120 76 117 82" stroke={SKIN_SHADOW} strokeWidth="1.2" fill="none" opacity="0.3" />

    {/* Jawline definition */}
    <path d="M78 94 Q88 106 100 110" stroke={SKIN_SHADOW} strokeWidth="0.8" fill="none" opacity="0.2" />
    <path d="M122 94 Q112 106 100 110" stroke={SKIN_SHADOW} strokeWidth="0.8" fill="none" opacity="0.2" />

    {/* Temple hollow */}
    <ellipse cx="78" cy="58" rx="3" ry="5" fill={SKIN_SHADOW} opacity="0.1" />
    <ellipse cx="122" cy="58" rx="3" ry="5" fill={SKIN_SHADOW} opacity="0.1" />
  </g>
);

/** Geometric — Architects: square jaw, symmetric, structured */
const GeometricHead = ({ uid }: { uid?: string }) => (
  <g>
    <rect x="89" y="106" width="22" height="18" rx="5" fill={SKIN} />
    <rect x="89" y="106" width="22" height="8" rx="3" fill={SKIN_SHADOW} opacity="0.3" />

    <path
      d="M74 66 Q74 34 100 30 Q126 34 126 66 L126 90 Q122 108 100 113 Q78 108 74 90 Z"
      fill={uid ? `url(#skin-${uid})` : SKIN}
    />

    <ellipse cx="100" cy="44" rx="16" ry="7" fill={SKIN_HI} opacity="0.2" />

    {/* Ears */}
    <path d="M74 64 Q68 60 66 70 Q64 80 70 84 Q72 78 74 74" fill={SKIN} />
    <path d="M69 68 Q68 74 70 78" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />
    <path d="M126 64 Q132 60 134 70 Q136 80 130 84 Q128 78 126 74" fill={SKIN} />
    <path d="M131 68 Q132 74 130 78" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />

    {/* Jaw — strong geometric */}
    <path d="M78 90 Q88 104 100 108 Q112 104 122 90" stroke={SKIN_SHADOW} strokeWidth="1" fill="none" opacity="0.2" />

    {/* Symmetric structure lines */}
    <path d="M80 62 L80 86" stroke={SKIN_SHADOW} strokeWidth="0.4" fill="none" opacity="0.08" />
    <path d="M120 62 L120 86" stroke={SKIN_SHADOW} strokeWidth="0.4" fill="none" opacity="0.08" />
  </g>
);

/** Fluid — Explorers: slightly asymmetric, dynamic, expressive */
const FluidHead = ({ uid }: { uid?: string }) => (
  <g>
    <rect x="89" y="106" width="22" height="18" rx="5" fill={SKIN} />
    <rect x="89" y="106" width="22" height="8" rx="3" fill={SKIN_SHADOW} opacity="0.25" />

    <path
      d="M73 70 Q71 36 98 30 Q128 34 129 66 L127 92 Q120 110 100 115 Q80 112 76 94 Z"
      fill={uid ? `url(#skin-${uid})` : SKIN}
    />

    <ellipse cx="98" cy="44" rx="18" ry="8" fill={SKIN_HI} opacity="0.2" transform="rotate(-3 98 44)" />

    {/* Ears */}
    <path d="M73 68 Q67 64 65 74 Q63 84 69 88 Q71 82 73 78" fill={SKIN} />
    <path d="M68 72 Q67 78 69 82" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />
    <path d="M129 64 Q135 60 137 70 Q139 80 133 84 Q131 78 129 74" fill={SKIN} />
    <path d="M134 68 Q135 74 133 78" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />

    {/* Subtle asymmetric cheek warmth */}
    <ellipse cx="82" cy="84" rx="6" ry="4" fill="#F0A8A8" opacity="0.08" />
    <ellipse cx="120" cy="82" rx="5" ry="4" fill="#F0A8A8" opacity="0.06" />
  </g>
);

/** Round — Anchors: full, warm, approachable */
const RoundHead = ({ uid }: { uid?: string }) => (
  <g>
    <rect x="89" y="108" width="22" height="16" rx="5" fill={SKIN} />
    <rect x="89" y="108" width="22" height="6" rx="3" fill={SKIN_SHADOW} opacity="0.25" />

    <ellipse cx="100" cy="72" rx="30" ry="34" fill={uid ? `url(#skin-${uid})` : SKIN} />

    <ellipse cx="100" cy="50" rx="16" ry="10" fill={SKIN_HI} opacity="0.25" />

    {/* Ears — rounder */}
    <ellipse cx="68" cy="74" rx="5" ry="8" fill={SKIN} />
    <ellipse cx="68" cy="74" rx="3" ry="5" fill={EAR_INNER} opacity="0.3" />
    <ellipse cx="132" cy="74" rx="5" ry="8" fill={SKIN} />
    <ellipse cx="132" cy="74" rx="3" ry="5" fill={EAR_INNER} opacity="0.3" />

    {/* Cheek blush */}
    <ellipse cx="80" cy="84" rx="8" ry="5" fill="#F4A0A0" opacity="0.15" />
    <ellipse cx="120" cy="84" rx="8" ry="5" fill="#F4A0A0" opacity="0.15" />

    {/* Chin roundness */}
    <ellipse cx="100" cy="102" rx="6" ry="3" fill={SKIN_HI} opacity="0.12" />
  </g>
);

/** Athletic — Kineticists: strong jaw, wide, powerful */
const AthleticHead = ({ uid }: { uid?: string }) => (
  <g>
    <rect x="87" y="106" width="26" height="18" rx="5" fill={SKIN} />
    <rect x="87" y="106" width="26" height="8" rx="3" fill={SKIN_SHADOW} opacity="0.35" />

    <path
      d="M70 66 Q70 32 100 28 Q130 32 130 66 L130 88 Q126 108 100 113 Q74 108 70 88 Z"
      fill={uid ? `url(#skin-${uid})` : SKIN}
    />

    <ellipse cx="100" cy="42" rx="18" ry="8" fill={SKIN_HI} opacity="0.2" />

    {/* Ears — larger */}
    <path d="M70 64 Q63 60 60 70 Q58 82 64 86 Q67 80 70 74" fill={SKIN} />
    <path d="M64 68 Q63 76 65 80" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />
    <path d="M130 64 Q137 60 140 70 Q142 82 136 86 Q133 80 130 74" fill={SKIN} />
    <path d="M136 68 Q137 76 135 80" stroke={EAR_INNER} strokeWidth="1.2" fill="none" opacity="0.5" />

    {/* Strong jaw */}
    <path d="M74 86 Q86 100 100 106 Q114 100 126 86" stroke={SKIN_SHADOW} strokeWidth="1.2" fill="none" opacity="0.25" />

    {/* Brow ridge */}
    <path d="M78 60 Q100 56 122 60" stroke={SKIN_SHADOW} strokeWidth="1.5" fill="none" opacity="0.12" />

    {/* Neck muscle hint */}
    <path d="M92 112 Q96 118 94 122" stroke={SKIN_SHADOW} strokeWidth="0.6" fill="none" opacity="0.15" />
    <path d="M108 112 Q104 118 106 122" stroke={SKIN_SHADOW} strokeWidth="0.6" fill="none" opacity="0.15" />
  </g>
);

const HEAD_MAP: Record<HeadShape, React.FC<{ uid?: string }>> = {
  angular: AngularHead,
  geometric: GeometricHead,
  fluid: FluidHead,
  round: RoundHead,
  athletic: AthleticHead,
};

export function HeadPart({ shape, uid }: HeadProps) {
  const Component = HEAD_MAP[shape];
  return <Component uid={uid} />;
}
