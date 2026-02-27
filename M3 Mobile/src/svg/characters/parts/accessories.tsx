import React from "react";
import { G, Path, Circle, Ellipse, Line, Rect } from "react-native-svg";
import type { AccessoryType } from "../types";

interface AccessoryProps { type: AccessoryType; color: string; }

const Lightning = ({ color }: { color: string }) => (
  <G x={140} y={140}>
    <Path d="M0 0 L-4 12 L2 10 L-2 24 L6 10 L0 12 Z" fill={color} opacity="0.7" />
  </G>
);

const TuningFork = ({ color }: { color: string }) => (
  <G x={56} y={170}>
    <Line x1="0" y1="0" x2="0" y2="20" stroke={color} strokeWidth="1.5" opacity="0.6" />
    <Path d="M-3 0 Q-3 -8 0 -10 Q3 -8 3 0" stroke={color} strokeWidth="1.5" fill="none" opacity="0.6" />
  </G>
);

const Compass = ({ color }: { color: string }) => (
  <G x={148} y={150}>
    <Circle cx="0" cy="0" r="7" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
    <Circle cx="0" cy="0" r="1" fill={color} opacity="0.6" />
    <Line x1="0" y1="-5" x2="0" y2="5" stroke={color} strokeWidth="0.8" opacity="0.5" />
    <Line x1="-5" y1="0" x2="5" y2="0" stroke={color} strokeWidth="0.8" opacity="0.5" />
    <Path d="M0 -5 L-2 -2 L2 -2 Z" fill={color} opacity="0.6" />
  </G>
);

const Metronome = ({ color }: { color: string }) => (
  <G x={54} y={164}>
    <Path d="M-5 16 L0 -4 L5 16 Z" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
    <Line x1="0" y1="14" x2="3" y2="0" stroke={color} strokeWidth="1.5" opacity="0.6" />
    <Circle cx="3" cy="-1" r="1.5" fill={color} opacity="0.5" />
  </G>
);

const Blueprint = ({ color }: { color: string }) => (
  <G x={142} y={158}>
    <Rect x="-6" y="-8" width="12" height="16" rx="1" fill={color} opacity="0.15" />
    <Line x1="-4" y1="-4" x2="4" y2="-4" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <Line x1="-4" y1="0" x2="4" y2="0" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <Line x1="-4" y1="4" x2="4" y2="4" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <Line x1="0" y1="-6" x2="0" y2="6" stroke={color} strokeWidth="0.5" opacity="0.3" />
  </G>
);

const YinYang = ({ color }: { color: string }) => (
  <G x={142} y={148}>
    <Circle cx="0" cy="0" r="7" fill={color} opacity="0.2" />
    <Path d="M0 -7 A7 7 0 0 1 0 7 A3.5 3.5 0 0 0 0 0 A3.5 3.5 0 0 1 0 -7 Z" fill={color} opacity="0.5" />
    <Circle cx="0" cy="-3.5" r="1.2" fill={color} opacity="0.2" />
    <Circle cx="0" cy="3.5" r="1.2" fill={color} opacity="0.6" />
  </G>
);

const Rose = ({ color }: { color: string }) => (
  <G x={54} y={162}>
    <Circle cx="0" cy="0" r="4" fill={color} opacity="0.3" />
    <Circle cx="-2" cy="-2" r="3" fill={color} opacity="0.4" />
    <Circle cx="2" cy="-1" r="3" fill={color} opacity="0.35" />
    <Circle cx="0" cy="1" r="2.5" fill={color} opacity="0.5" />
    <Line x1="0" y1="4" x2="-2" y2="16" stroke="#4a7c3f" strokeWidth="1" opacity="0.5" />
  </G>
);

const Magnifier = ({ color }: { color: string }) => (
  <G x={148} y={154}>
    <Circle cx="0" cy="0" r="6" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    <Circle cx="0" cy="0" r="4" fill={color} opacity="0.08" />
    <Line x1="4" y1="4" x2="10" y2="10" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
  </G>
);

const MapAccessory = ({ color }: { color: string }) => (
  <G x={146} y={158}>
    <Rect x="-7" y="-5" width="14" height="10" rx="1" fill={color} opacity="0.15" />
    <Line x1="-2" y1="-5" x2="-2" y2="5" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <Line x1="3" y1="-5" x2="3" y2="5" stroke={color} strokeWidth="0.5" opacity="0.3" />
    <Path d="M-5 0 Q-2 -3 1 0 Q3 2 6 -1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.4" />
    <Circle cx="5" cy="-2" r="1" fill={color} opacity="0.5" />
  </G>
);

const Heart = ({ color }: { color: string }) => (
  <G x={140} y={144}>
    <Path d="M0 4 Q-6 -2 -6 -5 Q-6 -8 -3 -8 Q0 -8 0 -5 Q0 -8 3 -8 Q6 -8 6 -5 Q6 -2 0 4 Z" fill={color} opacity="0.5" />
  </G>
);

const Drumstick = ({ color }: { color: string }) => (
  <G x={148} y={150}>
    <Line x1="0" y1="0" x2="-10" y2="18" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
    <Circle cx="0" cy="-1" r="2.5" fill={color} opacity="0.4" />
  </G>
);

const Cloud = ({ color }: { color: string }) => (
  <G x={144} y={140}>
    <Circle cx="0" cy="0" r="5" fill={color} opacity="0.15" />
    <Circle cx="-4" cy="2" r="4" fill={color} opacity="0.12" />
    <Circle cx="4" cy="1" r="4.5" fill={color} opacity="0.12" />
    <Circle cx="0" cy="3" r="3.5" fill={color} opacity="0.1" />
  </G>
);

const LightningPair = ({ color }: { color: string }) => (
  <G>
    <G x={46} y={148}>
      <Path d="M0 0 L-3 10 L2 8 L-1 20 L5 8 L0 10 Z" fill={color} opacity="0.6" />
    </G>
    <G x={150} y={142}>
      <Path d="M0 0 L-3 10 L2 8 L-1 20 L5 8 L0 10 Z" fill={color} opacity="0.6" />
    </G>
  </G>
);

const Headphones = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 56 Q72 30 100 26 Q128 30 128 56" stroke={color} strokeWidth="2.5" fill="none" opacity="0.5" />
    <Ellipse cx="70" cy="62" rx="5" ry="7" fill={color} opacity="0.4" />
    <Ellipse cx="130" cy="62" rx="5" ry="7" fill={color} opacity="0.4" />
    <Ellipse cx="70" cy="62" rx="3" ry="5" fill={color} opacity="0.2" />
    <Ellipse cx="130" cy="62" rx="3" ry="5" fill={color} opacity="0.2" />
  </G>
);

const Wrench = ({ color }: { color: string }) => (
  <G x={148} y={156}>
    <Line x1="0" y1="0" x2="-8" y2="16" stroke={color} strokeWidth="2" strokeLinecap="round" opacity="0.5" />
    <Path d="M-3 -2 Q0 -6 3 -2 L2 2 L-2 2 Z" fill={color} opacity="0.4" />
  </G>
);

const Wind = ({ color }: { color: string }) => (
  <G>
    <Path d="M140 80 Q152 78 158 82" stroke={color} strokeWidth="1" fill="none" opacity="0.3" strokeLinecap="round" />
    <Path d="M142 88 Q156 86 164 90" stroke={color} strokeWidth="1.5" fill="none" opacity="0.25" strokeLinecap="round" />
    <Path d="M140 96 Q150 94 156 98" stroke={color} strokeWidth="1" fill="none" opacity="0.2" strokeLinecap="round" />
  </G>
);

const Mask = ({ color }: { color: string }) => (
  <G x={146} y={152}>
    <Path d="M-6 -4 Q-6 -8 0 -8 Q6 -8 6 -4 Q6 2 0 4 Q-6 2 -6 -4 Z" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Circle cx="-2" cy="-4" r="1" fill={color} opacity="0.4" />
    <Circle cx="2" cy="-4" r="1" fill={color} opacity="0.4" />
    <Path d="M-2 -1 Q0 2 2 -1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.4" />
  </G>
);

const Binoculars = ({ color }: { color: string }) => (
  <G x={148} y={156}>
    <Circle cx="-3" cy="0" r="4" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Circle cx="3" cy="0" r="4" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Rect x="-1.5" y="-2" width="3" height="4" fill={color} opacity="0.2" />
  </G>
);

const Ruler = ({ color }: { color: string }) => (
  <G x={148} y={158}>
    <Rect x="-3" y="-12" width="6" height="24" rx="1" fill={color} opacity="0.15" />
    {[-10, -6, -2, 2, 6, 10].map((y) => (
      <Line key={y} x1="-3" y1={y} x2="-1" y2={y} stroke={color} strokeWidth="0.5" opacity="0.3" />
    ))}
  </G>
);

const Fire = ({ color }: { color: string }) => (
  <G x={148} y={148}>
    <Path d="M0 8 Q-4 2 -3 -2 Q-2 2 0 -6 Q2 2 3 -2 Q4 2 0 8 Z" fill={color} opacity="0.5" />
    <Path d="M0 6 Q-2 2 0 -2 Q2 2 0 6 Z" fill={color} opacity="0.3" />
  </G>
);

const Cassette = ({ color }: { color: string }) => (
  <G x={146} y={160}>
    <Rect x="-8" y="-5" width="16" height="10" rx="1.5" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Circle cx="-3" cy="0" r="2.5" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Circle cx="3" cy="0" r="2.5" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Circle cx="-3" cy="0" r="0.8" fill={color} opacity="0.3" />
    <Circle cx="3" cy="0" r="0.8" fill={color} opacity="0.3" />
    <Rect x="-5" y="2.5" width="10" height="2" rx="0.5" fill={color} opacity="0.1" />
  </G>
);

const Thorns = ({ color }: { color: string }) => (
  <G>
    <Path d="M56 178 L52 174 L58 176" fill={color} opacity="0.4" />
    <Path d="M60 180 L56 176 L62 178" fill={color} opacity="0.4" />
    <Path d="M58 184 L54 180 L60 182" fill={color} opacity="0.4" />
  </G>
);

const Palette = ({ color }: { color: string }) => (
  <G x={150} y={148}>
    <Ellipse cx="0" cy="0" rx="8" ry="6" fill={color} opacity="0.15" />
    <Circle cx="-3" cy="2" r="2" fill="#1a1a2e" />
    <Circle cx="-2" cy="-3" r="1.5" fill="#E040FB" opacity="0.5" />
    <Circle cx="2" cy="-2" r="1.5" fill="#38BDF8" opacity="0.5" />
    <Circle cx="4" cy="1" r="1.5" fill="#84CC16" opacity="0.5" />
    <Circle cx="1" cy="3" r="1.5" fill="#FBBF24" opacity="0.5" />
  </G>
);

const NoAccessory = () => null;

const ACCESSORY_MAP: Record<AccessoryType, React.FC<{ color: string }>> = {
  lightning: Lightning, "tuning-fork": TuningFork, compass: Compass, metronome: Metronome,
  blueprint: Blueprint, "yin-yang": YinYang, rose: Rose, magnifier: Magnifier,
  map: MapAccessory, heart: Heart, drumstick: Drumstick, cloud: Cloud,
  "lightning-pair": LightningPair, headphones: Headphones, wrench: Wrench, wind: Wind,
  mask: Mask, binoculars: Binoculars, ruler: Ruler, fire: Fire,
  cassette: Cassette, thorns: Thorns, palette: Palette,
  none: NoAccessory as React.FC<{ color: string }>,
};

export function AccessoryPart({ type, color }: AccessoryProps) {
  const Component = ACCESSORY_MAP[type];
  return <Component color={color} />;
}
