import React from "react";
import { G, Defs, RadialGradient, LinearGradient, Stop, Ellipse, Path, Circle } from "react-native-svg";
import type { PersonaLevel } from "../../../types/m3";

interface AuraProps { color: string; level: PersonaLevel; id: string; }

export function AuraPart({ color, level, id }: AuraProps) {
  const intensity = Math.min(level / 12, 1);
  const radius = 80 + level * 4;
  return (
    <G>
      <Defs>
        <RadialGradient id={`aura-${id}`}>
          <Stop offset="0%" stopColor={color} stopOpacity={0.15 * intensity} />
          <Stop offset="60%" stopColor={color} stopOpacity={0.05 * intensity} />
          <Stop offset="100%" stopColor={color} stopOpacity={0} />
        </RadialGradient>
      </Defs>
      <Ellipse cx="100" cy="140" rx={radius} ry={radius * 1.1} fill={`url(#aura-${id})`} />
    </G>
  );
}

export function CrownPart({ color, id }: { color: string; id: string }) {
  return (
    <G>
      <Defs>
        <LinearGradient id={`crown-${id}`} x1="0" y1="0" x2="0" y2="1">
          <Stop offset="0%" stopColor={color} stopOpacity={0.8} />
          <Stop offset="100%" stopColor={color} stopOpacity={0.2} />
        </LinearGradient>
      </Defs>
      <Path d="M82 24 L86 8 L92 18 L100 2 L108 18 L114 8 L118 24 Z" fill={`url(#crown-${id})`} />
      <Circle cx="100" cy="12" r="2" fill="white" opacity="0.6" />
      <Circle cx="90" cy="16" r="1.5" fill="white" opacity="0.4" />
      <Circle cx="110" cy="16" r="1.5" fill="white" opacity="0.4" />
    </G>
  );
}

export function WingsPart({ color, id }: { color: string; id: string }) {
  return (
    <G>
      <Defs>
        <LinearGradient id={`wing-l-${id}`} x1="1" y1="0" x2="0" y2="0">
          <Stop offset="0%" stopColor={color} stopOpacity={0.4} />
          <Stop offset="100%" stopColor={color} stopOpacity={0.05} />
        </LinearGradient>
        <LinearGradient id={`wing-r-${id}`} x1="0" y1="0" x2="1" y2="0">
          <Stop offset="0%" stopColor={color} stopOpacity={0.4} />
          <Stop offset="100%" stopColor={color} stopOpacity={0.05} />
        </LinearGradient>
      </Defs>
      <Path d="M70 140 Q40 110 20 130 Q30 150 40 160 Q50 170 60 168 Q66 160 70 150 Z" fill={`url(#wing-l-${id})`} />
      <Path d="M60 140 Q44 128 30 138" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
      <Path d="M62 148 Q48 140 36 148" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
      <Path d="M64 156 Q52 150 42 156" stroke={color} strokeWidth="0.5" fill="none" opacity="0.1" />
      <Path d="M130 140 Q160 110 180 130 Q170 150 160 160 Q150 170 140 168 Q134 160 130 150 Z" fill={`url(#wing-r-${id})`} />
      <Path d="M140 140 Q156 128 170 138" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
      <Path d="M138 148 Q152 140 164 148" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
      <Path d="M136 156 Q148 150 158 156" stroke={color} strokeWidth="0.5" fill="none" opacity="0.1" />
    </G>
  );
}
