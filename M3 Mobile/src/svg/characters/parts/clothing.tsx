import React from "react";
import { G, Path, Circle, Line, Rect, Ellipse } from "react-native-svg";
import type { ClothingStyle } from "../types";

interface ClothingProps { style: ClothingStyle; color: string; }

const DARK = "#1a1a2e";
const DARK2 = "#2d2d44";

const CloakHoodie = ({ color }: { color: string }) => (
  <G>
    <Path d="M66 62 Q64 44 100 36 Q136 44 134 62 Q130 48 100 42 Q70 48 66 62 Z" fill={DARK} opacity="0.5" />
    <Path d="M70 130 Q60 180 56 240 Q66 250 80 248 L82 160 Z" fill={DARK2} opacity="0.6" />
    <Path d="M130 130 Q140 180 144 240 Q134 250 120 248 L118 160 Z" fill={DARK2} opacity="0.6" />
    <Path d="M82 124 L100 134 L118 124" stroke={color} strokeWidth="2" fill="none" />
    <Line x1="100" y1="134" x2="100" y2="210" stroke={color} strokeWidth="1" opacity="0.3" />
  </G>
);

const LongCloak = ({ color }: { color: string }) => (
  <G>
    <Path d="M66 120 Q56 180 52 260 Q76 270 100 268 Q124 270 148 260 Q144 180 134 120 Z" fill={DARK2} opacity="0.5" />
    <Path d="M80 124 L100 118 L120 124" stroke={color} strokeWidth="2" fill="none" />
    <Path d="M80 124 L76 134 L84 130" fill={color} opacity="0.3" />
    <Path d="M120 124 L124 134 L116 130" fill={color} opacity="0.3" />
    <Circle cx="100" cy="170" r="6" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    <Circle cx="100" cy="170" r="2" fill={color} opacity="0.2" />
  </G>
);

const HalfContrast = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 124 L72 220 Q86 224 100 224 L100 124 Z" fill={DARK} />
    <Path d="M100 124 L100 224 Q114 224 128 220 L126 124 Z" fill="#e8e8e8" />
    <Line x1="100" y1="124" x2="100" y2="224" stroke={color} strokeWidth="1.5" />
    <Path d="M84 124 L100 136 L116 124" stroke={color} strokeWidth="1.5" fill="none" />
  </G>
);

const TheaterCloak = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 110 Q68 90 76 82 L80 124" fill={DARK2} />
    <Path d="M128 110 Q132 90 124 82 L120 124" fill={DARK2} />
    <Path d="M68 130 Q56 190 58 260 Q78 268 100 266 Q122 268 142 260 Q144 190 132 130 Z" fill={DARK2} opacity="0.6" />
    <Path d="M72 130 Q68 190 70 250 L80 248 Q78 190 80 130 Z" fill={color} opacity="0.15" />
    <Path d="M128 130 Q132 190 130 250 L120 248 Q122 190 120 130 Z" fill={color} opacity="0.15" />
    <Path d="M76 82 L80 100" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    <Path d="M124 82 L120 100" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
  </G>
);

const CollarShirt = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 L78 130 L90 132 Z" fill="white" opacity="0.8" />
    <Path d="M116 124 L122 130 L110 132 Z" fill="white" opacity="0.8" />
    <Path d="M97 132 L100 148 L103 132" fill={color} opacity="0.6" />
    <Line x1="100" y1="148" x2="100" y2="200" stroke={color} strokeWidth="1" opacity="0.3" />
  </G>
);

const PlainTee = ({ color }: { color: string }) => (
  <G>
    <Path d="M88 124 Q100 130 112 124" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
  </G>
);

const FormalJacket = ({ color }: { color: string }) => (
  <G>
    <Path d="M82 124 L76 142 L88 140 Z" fill={DARK2} />
    <Path d="M118 124 L124 142 L112 140 Z" fill={DARK2} />
    <Path d="M76 142 L74 210 Q86 218 100 220 Q114 218 126 210 L124 142" stroke={DARK2} strokeWidth="1" fill="none" />
    <Circle cx="100" cy="160" r="2" fill={color} opacity="0.5" />
    <Circle cx="100" cy="176" r="2" fill={color} opacity="0.5" />
    <Path d="M82 148 L86 144 L90 148 L86 150 Z" fill={color} opacity="0.4" />
  </G>
);

const ArgyleSweater = ({ color }: { color: string }) => (
  <G>
    <Path d="M86 124 L100 140 L114 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    <Path d="M84 150 L92 158 L84 166 L76 158 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    <Path d="M100 142 L108 150 L100 158 L92 150 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    <Path d="M116 150 L124 158 L116 166 L108 158 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    <Path d="M100 158 L108 166 L100 174 L92 166 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.15" />
  </G>
);

const LabCoat = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 124 L72 220 Q86 224 100 224 Q114 224 128 220 L126 124 Z" fill="white" opacity="0.15" />
    <Path d="M82 124 L76 140 L86 138 Z" fill="white" opacity="0.2" />
    <Path d="M118 124 L124 140 L114 138 Z" fill="white" opacity="0.2" />
    <Rect x="80" y="170" width="12" height="10" rx="1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Line x1="84" y1="168" x2="84" y2="174" stroke={color} strokeWidth="1" opacity="0.4" />
  </G>
);

const HoodieBackpack = ({ color }: { color: string }) => (
  <G>
    <Path d="M68 62 Q66 48 100 40 Q134 48 132 62 Q128 50 100 44 Q72 50 68 62 Z" fill={DARK2} opacity="0.4" />
    <Line x1="92" y1="128" x2="90" y2="150" stroke={color} strokeWidth="1" opacity="0.4" />
    <Line x1="108" y1="128" x2="110" y2="150" stroke={color} strokeWidth="1" opacity="0.4" />
    <Path d="M82 130 L80 160" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" />
    <Path d="M118 130 L120 160" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" />
    <Path d="M86 180 Q100 188 114 180" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
  </G>
);

const TravelCloak = ({ color }: { color: string }) => (
  <G>
    <Path d="M66 130 Q58 190 64 258 Q82 266 100 264 Q118 266 136 258 Q142 190 134 130 Z" fill={DARK2} opacity="0.4" />
    <Circle cx="100" cy="128" r="4" fill={color} opacity="0.5" />
    <Circle cx="100" cy="128" r="2" fill={color} opacity="0.3" />
    <Path d="M64 240 Q56 248 58 258" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
  </G>
);

const ExplorerJacket = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 L80 132 L88 130 Z" fill={DARK2} />
    <Path d="M116 124 L120 132 L112 130 Z" fill={DARK2} />
    <Line x1="100" y1="130" x2="100" y2="210" stroke={color} strokeWidth="1" opacity="0.3" />
    <Rect x="78" y="168" width="14" height="12" rx="2" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Rect x="108" y="168" width="14" height="12" rx="2" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Line x1="78" y1="172" x2="92" y2="172" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <Line x1="108" y1="172" x2="122" y2="172" stroke={color} strokeWidth="0.5" opacity="0.2" />
  </G>
);

const LeatherJacket = ({ color }: { color: string }) => (
  <G>
    <Path d="M80 124 L72 144 L90 140 Z" fill={DARK2} />
    <Path d="M120 124 L128 144 L110 140 Z" fill={DARK2} />
    <Path d="M90 140 Q96 190 94 210" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Circle cx="82" cy="150" r="1.5" fill={color} opacity="0.3" />
    <Circle cx="82" cy="158" r="1.5" fill={color} opacity="0.3" />
    <Circle cx="82" cy="166" r="1.5" fill={color} opacity="0.3" />
  </G>
);

const LayeredBohemian = ({ color }: { color: string }) => (
  <G>
    <Path d="M80 124 Q100 138 120 124 Q114 130 100 134 Q86 130 80 124 Z" fill={color} opacity="0.3" />
    <Path d="M74 140 L72 220" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    <Path d="M126 140 L128 220" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    <Path d="M80 170 Q90 168 100 170 Q110 168 120 170" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Path d="M80 176 Q90 174 100 176 Q110 174 120 176" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
  </G>
);

const VintageJacket = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 L78 138 L88 136 Z" fill={DARK2} opacity="0.7" />
    <Path d="M116 124 L122 138 L112 136 Z" fill={DARK2} opacity="0.7" />
    <Ellipse cx="62" cy="170" rx="4" ry="6" fill={color} opacity="0.15" />
    <Ellipse cx="138" cy="166" rx="4" ry="6" fill={color} opacity="0.15" />
    <Circle cx="100" cy="155" r="1.8" fill={color} opacity="0.3" />
    <Circle cx="100" cy="170" r="1.8" fill={color} opacity="0.3" />
    <Circle cx="100" cy="185" r="1.8" fill={color} opacity="0.3" />
  </G>
);

const SoftSweater = ({ color }: { color: string }) => (
  <G>
    <Path d="M86 124 Q100 132 114 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Path d="M82 206 Q100 212 118 206" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    <Path d="M82 210 Q100 216 118 210" stroke={color} strokeWidth="1" fill="none" opacity="0.15" />
    <Path d="M86 160 Q94 158 102 160" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
    <Path d="M98 168 Q106 166 114 168" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
  </G>
);

const FlowingDress = ({ color }: { color: string }) => (
  <G>
    <Path d="M82 124 Q78 160 68 240 Q84 250 100 248 Q116 250 132 240 Q122 160 118 124 Z" fill={color} opacity="0.15" />
    <Path d="M86 124 Q100 130 114 124" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    <Path d="M78 180 Q82 200 74 230" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    <Path d="M122 180 Q118 200 126 230" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </G>
);

const Cardigan = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 L82 210" stroke={DARK2} strokeWidth="1.5" fill="none" />
    <Path d="M116 124 L118 210" stroke={DARK2} strokeWidth="1.5" fill="none" />
    <Path d="M88 128 Q100 134 112 128" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    <Circle cx="83" cy="160" r="1.5" fill={color} opacity="0.3" />
    <Circle cx="117" cy="160" r="1.5" fill={color} opacity="0.3" />
  </G>
);

const LongSkirt = ({ color }: { color: string }) => (
  <G>
    <Path d="M86 124 Q100 132 114 124" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    <Path d="M80 190 Q74 220 66 260 Q84 268 100 266 Q116 268 134 260 Q126 220 120 190 Z" fill={color} opacity="0.12" />
    <Line x1="78" y1="190" x2="122" y2="190" stroke={color} strokeWidth="1" opacity="0.3" />
  </G>
);

const RetroJacket = ({ color }: { color: string }) => (
  <G>
    <Path d="M80 124 L72 140 L92 138 Z" fill={DARK2} opacity="0.6" />
    <Path d="M120 124 L128 140 L108 138 Z" fill={DARK2} opacity="0.6" />
    <Line x1="78" y1="150" x2="122" y2="150" stroke={color} strokeWidth="1.5" opacity="0.2" />
    <Line x1="78" y1="156" x2="122" y2="156" stroke={color} strokeWidth="1" opacity="0.15" />
    <Line x1="78" y1="160" x2="122" y2="160" stroke={color} strokeWidth="1.5" opacity="0.2" />
  </G>
);

const TankTop = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 Q100 128 116 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Line x1="86" y1="120" x2="86" y2="130" stroke={color} strokeWidth="2" opacity="0.3" />
    <Line x1="114" y1="120" x2="114" y2="130" stroke={color} strokeWidth="2" opacity="0.3" />
    <Path d="M80 200 Q100 208 120 200" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
  </G>
);

const TornTee = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 124 Q90 128 96 126 Q100 130 104 126 Q110 128 116 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Path d="M78 188 L82 184 L80 192 L84 190" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Path d="M120 178 L118 174 L122 180" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Path d="M96 156 L100 148 L104 156 L100 152 Z" fill={color} opacity="0.2" />
  </G>
);

const MechanicApron = ({ color }: { color: string }) => (
  <G>
    <Path d="M84 140 L82 210 Q100 216 118 210 L116 140 Z" fill={DARK2} opacity="0.4" />
    <Path d="M84 140 L88 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Path d="M116 140 L112 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Rect x="88" y="168" width="10" height="14" rx="1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <Rect x="102" y="168" width="10" height="14" rx="1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
  </G>
);

const SleevelessHoodie = ({ color }: { color: string }) => (
  <G>
    <Path d="M70 60 Q68 44 100 38 Q132 44 130 60 Q126 48 100 42 Q74 48 70 60 Z" fill={DARK2} opacity="0.3" />
    <Path d="M80 124 Q78 128 76 136" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
    <Path d="M120 124 Q122 128 124 136" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
    <Line x1="94" y1="128" x2="92" y2="146" stroke={color} strokeWidth="0.8" opacity="0.3" />
    <Line x1="106" y1="128" x2="108" y2="146" stroke={color} strokeWidth="0.8" opacity="0.3" />
  </G>
);

const CLOTHING_MAP: Record<ClothingStyle, React.FC<{ color: string }>> = {
  "cloak-hoodie": CloakHoodie, "long-cloak": LongCloak, "half-contrast": HalfContrast, "theater-cloak": TheaterCloak,
  "collar-shirt": CollarShirt, "plain-tee": PlainTee, "formal-jacket": FormalJacket, "argyle-sweater": ArgyleSweater, "lab-coat": LabCoat,
  "hoodie-backpack": HoodieBackpack, "travel-cloak": TravelCloak, "explorer-jacket": ExplorerJacket, "leather-jacket": LeatherJacket, "layered-bohemian": LayeredBohemian,
  "vintage-jacket": VintageJacket, "soft-sweater": SoftSweater, "flowing-dress": FlowingDress, cardigan: Cardigan, "long-skirt": LongSkirt, "retro-jacket": RetroJacket,
  "tank-top": TankTop, "torn-tee": TornTee, "mechanic-apron": MechanicApron, "sleeveless-hoodie": SleevelessHoodie,
};

export function ClothingPart({ style, color }: ClothingProps) {
  const Component = CLOTHING_MAP[style];
  return <Component color={color} />;
}
