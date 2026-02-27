import React from "react";
import { G, Path, Rect, Ellipse, Circle, Line } from "react-native-svg";
import type { HeadShape } from "../types";

interface HeadProps {
  shape: HeadShape;
  skinColor?: string;
}

const SKIN = "#F0D5B8";
const SKIN_SHADOW = "#D4B08C";

const AngularHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <G>
    <Rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    <Path d="M72 70 Q72 38 100 32 Q128 38 128 70 L124 96 Q116 112 100 116 Q84 112 76 96 Z" fill={skinColor} />
    <Path d="M76 72 Q80 76 82 80" stroke={SKIN_SHADOW} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Path d="M124 72 Q120 76 118 80" stroke={SKIN_SHADOW} strokeWidth="1.5" fill="none" opacity="0.4" />
  </G>
);

const GeometricHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <G>
    <Rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    <Path d="M74 68 Q74 36 100 32 Q126 36 126 68 L126 92 Q122 110 100 114 Q78 110 74 92 Z" fill={skinColor} />
    <Path d="M78 92 L100 108 L122 92" stroke={SKIN_SHADOW} strokeWidth="1" fill="none" opacity="0.25" />
  </G>
);

const FluidHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <G>
    <Rect x="90" y="108" width="20" height="16" rx="4" fill={skinColor} />
    <Path d="M73 72 Q71 38 98 32 Q128 36 129 68 L126 94 Q118 112 100 116 Q82 114 76 96 Z" fill={skinColor} />
  </G>
);

const RoundHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <G>
    <Rect x="90" y="110" width="20" height="14" rx="4" fill={skinColor} />
    <Ellipse cx="100" cy="74" rx="30" ry="34" fill={skinColor} />
    <Circle cx="80" cy="82" r="6" fill="#F4A0A0" opacity="0.2" />
    <Circle cx="120" cy="82" r="6" fill="#F4A0A0" opacity="0.2" />
  </G>
);

const AthleticHead = ({ skinColor = SKIN }: { skinColor?: string }) => (
  <G>
    <Rect x="88" y="108" width="24" height="16" rx="4" fill={skinColor} />
    <Path d="M70 68 Q70 34 100 30 Q130 34 130 68 L130 90 Q126 110 100 114 Q74 110 70 90 Z" fill={skinColor} />
    <Path d="M74 88 Q86 102 100 106 Q114 102 126 88" stroke={SKIN_SHADOW} strokeWidth="1.2" fill="none" opacity="0.3" />
  </G>
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
