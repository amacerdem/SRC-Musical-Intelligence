import React from "react";
import { G, Ellipse, Circle, Path, Line } from "react-native-svg";
import type { EyeStyle } from "../types";

interface EyeProps {
  style: EyeStyle;
  color?: string;
}

const IRIS = "#2d2d44";

const IntenseEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="74" rx="7" ry="4" fill="white" />
    <Ellipse cx="89" cy="74" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="90" cy="73" r="1" fill="white" />
    <Ellipse cx="112" cy="74" rx="7" ry="4" fill="white" />
    <Ellipse cx="111" cy="74" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="112" cy="73" r="1" fill="white" />
    <Path d="M80 68 Q88 64 96 67" stroke={IRIS} strokeWidth="1.8" fill="none" />
    <Path d="M104 67 Q112 64 120 68" stroke={IRIS} strokeWidth="1.8" fill="none" />
    {color && <Circle cx="89" cy="74" r="2" fill={color} opacity="0.3" />}
    {color && <Circle cx="111" cy="74" r="2" fill={color} opacity="0.3" />}
  </G>
);

const WideEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="76" rx="8" ry="7" fill="white" />
    <Ellipse cx="88" cy="76" rx="4" ry="4" fill={IRIS} />
    <Circle cx="90" cy="74" r="1.5" fill="white" />
    <Ellipse cx="112" cy="76" rx="8" ry="7" fill="white" />
    <Ellipse cx="112" cy="76" rx="4" ry="4" fill={IRIS} />
    <Circle cx="114" cy="74" r="1.5" fill="white" />
    <Path d="M79 66 Q88 62 97 66" stroke={IRIS} strokeWidth="1.5" fill="none" />
    <Path d="M103 66 Q112 62 121 66" stroke={IRIS} strokeWidth="1.5" fill="none" />
    {color && <Circle cx="88" cy="76" r="2.5" fill={color} opacity="0.2" />}
    {color && <Circle cx="112" cy="76" r="2.5" fill={color} opacity="0.2" />}
  </G>
);

const CalmEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="76" rx="7" ry="5" fill="white" />
    <Ellipse cx="88" cy="76" rx="3" ry="3" fill={IRIS} />
    <Circle cx="89" cy="75" r="1" fill="white" />
    <Ellipse cx="112" cy="76" rx="7" ry="5" fill="white" />
    <Ellipse cx="112" cy="76" rx="3" ry="3" fill={IRIS} />
    <Circle cx="113" cy="75" r="1" fill="white" />
    <Line x1="80" y1="68" x2="96" y2="68" stroke={IRIS} strokeWidth="1.5" strokeLinecap="round" />
    <Line x1="104" y1="68" x2="120" y2="68" stroke={IRIS} strokeWidth="1.5" strokeLinecap="round" />
  </G>
);

const WarmEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="76" rx="7" ry="5.5" fill="white" />
    <Ellipse cx="88" cy="77" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="89" cy="75" r="1.2" fill="white" />
    <Ellipse cx="112" cy="76" rx="7" ry="5.5" fill="white" />
    <Ellipse cx="112" cy="77" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="113" cy="75" r="1.2" fill="white" />
    <Path d="M80 68 Q88 64 96 68" stroke={IRIS} strokeWidth="1.3" fill="none" />
    <Path d="M104 68 Q112 64 120 68" stroke={IRIS} strokeWidth="1.3" fill="none" />
    {color && <Ellipse cx="88" cy="80" rx="5" ry="2" fill={color} opacity="0.1" />}
    {color && <Ellipse cx="112" cy="80" rx="5" ry="2" fill={color} opacity="0.1" />}
  </G>
);

const SharpEyes = ({ color }: { color?: string }) => (
  <G>
    <Path d="M81 78 Q88 70 95 78 Q88 82 81 78 Z" fill="white" />
    <Circle cx="88" cy="76" r="3" fill={IRIS} />
    <Circle cx="89" cy="75" r="1" fill="white" />
    <Path d="M105 78 Q112 70 119 78 Q112 82 105 78 Z" fill="white" />
    <Circle cx="112" cy="76" r="3" fill={IRIS} />
    <Circle cx="113" cy="75" r="1" fill="white" />
    <Path d="M79 68 Q88 66 96 70" stroke={IRIS} strokeWidth="2" fill="none" />
    <Path d="M104 70 Q112 66 121 68" stroke={IRIS} strokeWidth="2" fill="none" />
    {color && <Circle cx="88" cy="76" r="2" fill={color} opacity="0.25" />}
    {color && <Circle cx="112" cy="76" r="2" fill={color} opacity="0.25" />}
  </G>
);

const DreamyEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="78" rx="7" ry="3.5" fill="white" />
    <Ellipse cx="88" cy="78" rx="3" ry="3" fill={IRIS} />
    <Circle cx="89" cy="77" r="1" fill="white" />
    <Ellipse cx="112" cy="78" rx="7" ry="3.5" fill="white" />
    <Ellipse cx="112" cy="78" rx="3" ry="3" fill={IRIS} />
    <Circle cx="113" cy="77" r="1" fill="white" />
    <Path d="M80 70 Q88 68 96 70" stroke={IRIS} strokeWidth="1.2" fill="none" />
    <Path d="M104 70 Q112 68 120 70" stroke={IRIS} strokeWidth="1.2" fill="none" />
    {color && <Ellipse cx="100" cy="78" rx="20" ry="6" fill={color} opacity="0.06" />}
  </G>
);

const DeterminedEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="88" cy="76" rx="7" ry="4.5" fill="white" />
    <Ellipse cx="89" cy="76" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="90" cy="75" r="1" fill="white" />
    <Ellipse cx="112" cy="76" rx="7" ry="4.5" fill="white" />
    <Ellipse cx="111" cy="76" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="112" cy="75" r="1" fill="white" />
    <Line x1="79" y1="67" x2="96" y2="66" stroke={IRIS} strokeWidth="1.8" strokeLinecap="round" />
    <Line x1="104" y1="66" x2="121" y2="67" stroke={IRIS} strokeWidth="1.8" strokeLinecap="round" />
  </G>
);

const CuriousEyes = ({ color }: { color?: string }) => (
  <G>
    <Ellipse cx="87" cy="76" rx="8" ry="6.5" fill="white" />
    <Ellipse cx="87" cy="76" rx="4" ry="4" fill={IRIS} />
    <Circle cx="89" cy="74" r="1.5" fill="white" />
    <Circle cx="86" cy="78" r="0.8" fill="white" />
    <Ellipse cx="113" cy="74" rx="7.5" ry="6" fill="white" />
    <Ellipse cx="113" cy="74" rx="3.5" ry="3.5" fill={IRIS} />
    <Circle cx="115" cy="72" r="1.5" fill="white" />
    <Path d="M78 66 Q87 62 96 66" stroke={IRIS} strokeWidth="1.5" fill="none" />
    <Path d="M104 64 Q113 60 122 64" stroke={IRIS} strokeWidth="1.5" fill="none" />
    {color && <Circle cx="87" cy="76" r="2.5" fill={color} opacity="0.15" />}
    {color && <Circle cx="113" cy="74" r="2.5" fill={color} opacity="0.15" />}
  </G>
);

const EYE_MAP: Record<EyeStyle, React.FC<{ color?: string }>> = {
  intense: IntenseEyes,
  wide: WideEyes,
  calm: CalmEyes,
  warm: WarmEyes,
  sharp: SharpEyes,
  dreamy: DreamyEyes,
  determined: DeterminedEyes,
  curious: CuriousEyes,
};

export function EyesPart({ style, color }: EyeProps) {
  const Component = EYE_MAP[style];
  return <Component color={color} />;
}
