import React from "react";
import { G, Path, Circle, Line } from "react-native-svg";
import type { HairStyle } from "../types";

interface HairProps { style: HairStyle; color: string; }

const FlamesHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 56 Q68 30 80 18 Q86 28 88 20 Q94 32 100 14 Q106 32 112 20 Q118 28 120 18 Q132 30 128 56 Q128 38 100 32 Q72 38 72 56 Z" fill={color} />
    <Path d="M78 50 Q84 28 92 22 Q96 34 100 18 Q104 34 108 22 Q116 28 122 50" fill={color} opacity="0.7" />
  </G>
);

const SpikesHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 58 L74 42 L80 12 L86 42 L88 8 L94 40 L100 4 L106 40 L112 8 L118 42 L120 12 L126 42 L126 58 Q100 48 74 58 Z" fill={color} />
  </G>
);

const SplitHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q70 32 100 26 L100 58 Q86 48 72 58 Z" fill={color} />
    <Path d="M100 26 Q130 32 128 58 Q114 48 100 58 Z" fill="white" opacity="0.85" />
    <Line x1="100" y1="26" x2="100" y2="58" stroke="#1a1a2e" strokeWidth="1" />
  </G>
);

const DramaticWaveHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M68 62 Q64 30 100 22 Q136 30 132 62 Q128 38 100 32 Q72 38 68 62 Z" fill={color} />
    <Path d="M116 30 Q134 18 148 28 Q142 36 132 38" fill={color} opacity="0.8" />
    <Path d="M120 34 Q138 24 146 30" fill={color} opacity="0.5" />
  </G>
);

const SlickHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 58 Q72 38 100 28 Q128 38 126 58 Q120 44 100 38 Q80 44 74 58 Z" fill={color} />
    <Path d="M84 40 Q92 34 100 32" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    <Path d="M88 44 Q96 38 104 36" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
  </G>
);

const BuzzcutHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M76 60 Q74 42 100 34 Q126 42 124 60 Q120 48 100 42 Q80 48 76 60 Z" fill={color} opacity="0.6" />
    {[82, 90, 100, 110, 118].map((x) => (
      <Circle key={x} cx={x} cy="46" r="0.8" fill={color} opacity="0.4" />
    ))}
  </G>
);

const StructuredHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q70 34 100 24 Q130 34 128 58 Q124 40 100 32 Q76 40 72 58 Z" fill={color} />
    <Line x1="88" y1="28" x2="84" y2="58" stroke="#1a1a2e" strokeWidth="1.5" />
    <Path d="M88 28 Q100 24 128 34" stroke={color} strokeWidth="2" fill="none" opacity="0.6" />
  </G>
);

const AnalyticalHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 58 Q72 34 100 26 Q128 34 126 58 Q122 42 100 36 Q78 42 74 58 Z" fill={color} />
    <Path d="M86 30 L84 56" stroke="#1a1a2e" strokeWidth="0.8" opacity="0.5" />
    <Path d="M86 30 Q94 28 100 28 Q112 28 120 32" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
  </G>
);

const PreciseHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M74 58 Q72 34 100 24 Q128 34 126 58 Q122 40 100 32 Q78 40 74 58 Z" fill={color} />
    <Line x1="100" y1="24" x2="100" y2="56" stroke="#1a1a2e" strokeWidth="1" />
    <Path d="M76 46 Q88 34 100 32 Q112 34 124 46" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
  </G>
);

const WildHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M64 62 Q60 28 100 16 Q140 28 136 62 Q130 36 100 28 Q70 36 64 62 Z" fill={color} />
    <Path d="M70 38 L58 28 L66 36" fill={color} />
    <Path d="M130 38 L142 24 L134 36" fill={color} />
    <Path d="M86 22 L78 8 L84 20" fill={color} />
    <Path d="M114 22 L122 6 L116 20" fill={color} />
    <Path d="M100 16 L100 4 L102 16" fill={color} />
  </G>
);

const WindsweptHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q68 30 100 22 Q132 30 128 58 Q124 38 100 30 Q76 38 72 58 Z" fill={color} />
    <Path d="M120 32 Q140 24 156 30" stroke={color} strokeWidth="3" fill="none" strokeLinecap="round" />
    <Path d="M124 38 Q142 32 152 36" stroke={color} strokeWidth="2.5" fill="none" strokeLinecap="round" opacity="0.7" />
    <Path d="M126 44 Q138 40 148 42" stroke={color} strokeWidth="2" fill="none" strokeLinecap="round" opacity="0.5" />
  </G>
);

const CurlyFreeHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M70 62 Q66 30 100 20 Q134 30 130 62 Q126 38 100 30 Q74 38 70 62 Z" fill={color} />
    <Path d="M72 48 Q66 42 70 36 Q74 30 72 24" stroke={color} strokeWidth="3" fill="none" strokeLinecap="round" />
    <Path d="M128 48 Q134 42 130 36 Q126 30 128 24" stroke={color} strokeWidth="3" fill="none" strokeLinecap="round" />
    <Circle cx="86" cy="22" r="5" fill={color} opacity="0.8" />
    <Circle cx="100" cy="18" r="5" fill={color} />
    <Circle cx="114" cy="22" r="5" fill={color} opacity="0.8" />
  </G>
);

const MohawkHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M76 58 Q76 44 84 40 L84 58 Z" fill={color} opacity="0.2" />
    <Path d="M124 58 Q124 44 116 40 L116 58 Z" fill={color} opacity="0.2" />
    <Path d="M88 58 Q86 20 100 6 Q114 20 112 58 Q106 34 100 28 Q94 34 88 58 Z" fill={color} />
    <Path d="M94 16 L92 4 L98 14" fill={color} />
    <Path d="M100 6 L100 -2 L102 6" fill={color} />
    <Path d="M106 16 L108 4 L102 14" fill={color} />
  </G>
);

const FlowingHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M68 62 Q64 30 100 20 Q136 30 132 62 Q128 38 100 28 Q72 38 68 62 Z" fill={color} />
    <Path d="M68 62 Q64 80 66 100 Q68 108 72 112" stroke={color} strokeWidth="6" fill="none" strokeLinecap="round" />
    <Path d="M132 62 Q136 80 134 100 Q132 108 128 112" stroke={color} strokeWidth="6" fill="none" strokeLinecap="round" />
    <Path d="M66 80 Q62 90 66 100" stroke={color} strokeWidth="3" fill="none" opacity="0.5" strokeLinecap="round" />
    <Path d="M134 80 Q138 90 134 100" stroke={color} strokeWidth="3" fill="none" opacity="0.5" strokeLinecap="round" />
  </G>
);

const WavyWarmHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M70 62 Q68 32 100 22 Q132 32 130 62 Q126 40 100 32 Q74 40 70 62 Z" fill={color} />
    <Path d="M74 48 Q86 40 100 42 Q114 40 126 48" stroke={color} strokeWidth="2" fill="none" opacity="0.5" />
    <Path d="M76 54 Q88 46 100 48 Q112 46 124 54" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
    <Path d="M70 62 Q66 72 68 82" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.6" />
    <Path d="M130 62 Q134 72 132 82" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.6" />
  </G>
);

const SoftLongHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M68 62 Q64 30 100 20 Q136 30 132 62 Q128 38 100 28 Q72 38 68 62 Z" fill={color} />
    <Path d="M68 62 Q64 90 68 120" stroke={color} strokeWidth="8" fill="none" strokeLinecap="round" />
    <Path d="M132 62 Q136 90 132 120" stroke={color} strokeWidth="8" fill="none" strokeLinecap="round" />
    <Path d="M72 70 Q70 90 72 108" stroke={color} strokeWidth="3" fill="none" opacity="0.4" strokeLinecap="round" />
    <Path d="M128 70 Q130 90 128 108" stroke={color} strokeWidth="3" fill="none" opacity="0.4" strokeLinecap="round" />
  </G>
);

const DreamyHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M68 60 Q64 28 100 18 Q136 28 132 60 Q128 36 100 28 Q72 36 68 60 Z" fill={color} />
    <Circle cx="74" cy="42" r="8" fill={color} opacity="0.5" />
    <Circle cx="126" cy="42" r="8" fill={color} opacity="0.5" />
    <Circle cx="84" cy="28" r="7" fill={color} opacity="0.6" />
    <Circle cx="116" cy="28" r="7" fill={color} opacity="0.6" />
    <Circle cx="100" cy="22" r="8" fill={color} opacity="0.7" />
  </G>
);

const NeatBobHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q70 34 100 26 Q130 34 128 58 Q124 42 100 36 Q76 42 72 58 Z" fill={color} />
    <Path d="M72 58 L70 82 Q72 86 76 86" fill={color} />
    <Path d="M128 58 L130 82 Q128 86 124 86" fill={color} />
    <Path d="M78 48 Q88 42 100 44 Q112 42 122 48" fill={color} opacity="0.6" />
  </G>
);

const EtherealHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M66 62 Q62 26 100 16 Q138 26 134 62 Q130 34 100 26 Q70 34 66 62 Z" fill={color} opacity="0.8" />
    <Path d="M66 50 Q56 40 60 30" stroke={color} strokeWidth="2" fill="none" opacity="0.4" strokeLinecap="round" />
    <Path d="M134 50 Q144 40 140 30" stroke={color} strokeWidth="2" fill="none" opacity="0.4" strokeLinecap="round" />
    <Path d="M66 62 Q60 80 64 100" stroke={color} strokeWidth="5" fill="none" opacity="0.3" strokeLinecap="round" />
    <Path d="M134 62 Q140 80 136 100" stroke={color} strokeWidth="5" fill="none" opacity="0.3" strokeLinecap="round" />
    <Circle cx="62" cy="36" r="1.5" fill={color} opacity="0.5" />
    <Circle cx="138" cy="36" r="1.5" fill={color} opacity="0.5" />
  </G>
);

const VintageHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q70 32 100 24 Q130 32 128 58 Q124 40 100 34 Q76 40 72 58 Z" fill={color} />
    <Path d="M80 36 Q86 26 96 28 Q106 26 112 30 Q118 28 122 36" fill={color} opacity="0.7" />
    <Path d="M72 58 Q68 62 66 70 Q64 76 68 78 Q72 76 72 70" fill={color} opacity="0.6" />
    <Path d="M128 58 Q132 62 134 70 Q136 76 132 78 Q128 76 128 70" fill={color} opacity="0.6" />
  </G>
);

const DreadlocksHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 56 Q70 34 100 26 Q130 34 128 56 Q124 40 100 34 Q76 40 72 56 Z" fill={color} />
    <Path d="M76 54 Q72 70 74 90" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <Path d="M84 50 Q80 68 82 88" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <Path d="M92 48 Q90 66 90 82" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    <Path d="M108 48 Q110 66 110 82" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    <Path d="M116 50 Q120 68 118 88" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <Path d="M124 54 Q128 70 126 90" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <Circle cx="74" cy="78" r="2" fill="white" opacity="0.5" />
    <Circle cx="126" cy="78" r="2" fill="white" opacity="0.5" />
  </G>
);

const ElectricHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 56 Q68 28 100 16 Q132 28 128 56 Q124 36 100 28 Q76 36 72 56 Z" fill={color} />
    <Path d="M82 28 L76 6 L84 22" fill={color} />
    <Path d="M92 22 L88 2 L96 18" fill={color} />
    <Path d="M100 16 L100 -4 L104 16" fill={color} />
    <Path d="M108 22 L112 2 L104 18" fill={color} />
    <Path d="M118 28 L124 6 L116 22" fill={color} />
    <Path d="M78 14 L74 10 L82 12" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
    <Path d="M122 14 L126 10 L118 12" stroke={color} strokeWidth="1" fill="none" opacity="0.5" />
  </G>
);

const FadeHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M78 56 Q78 38 100 30 Q122 38 122 56 Q118 44 100 38 Q82 44 78 56 Z" fill={color} />
    <Path d="M74 58 Q74 46 78 42 L78 58 Z" fill={color} opacity="0.4" />
    <Path d="M126 58 Q126 46 122 42 L122 58 Z" fill={color} opacity="0.4" />
    <Path d="M74 62 Q74 56 76 54" fill={color} opacity="0.2" />
    <Path d="M126 62 Q126 56 124 54" fill={color} opacity="0.2" />
    <Path d="M86 36 Q100 30 114 36" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
  </G>
);

const RawSpikesHair = ({ color }: { color: string }) => (
  <G>
    <Path d="M72 58 Q68 30 100 18 Q132 30 128 58 Q124 36 100 28 Q76 36 72 58 Z" fill={color} />
    <Path d="M78 34 L68 14 L82 30" fill={color} />
    <Path d="M88 26 L82 4 L94 22" fill={color} />
    <Path d="M100 18 L96 0 L104 18" fill={color} />
    <Path d="M112 26 L120 8 L108 22" fill={color} />
    <Path d="M122 34 L134 16 L118 30" fill={color} />
    <Path d="M84 38 L78 34" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    <Path d="M116 38 L122 34" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
  </G>
);

const HAIR_MAP: Record<HairStyle, React.FC<{ color: string }>> = {
  flames: FlamesHair, spikes: SpikesHair, split: SplitHair, "dramatic-wave": DramaticWaveHair,
  slick: SlickHair, buzzcut: BuzzcutHair, structured: StructuredHair, analytical: AnalyticalHair, precise: PreciseHair,
  wild: WildHair, windswept: WindsweptHair, "curly-free": CurlyFreeHair, mohawk: MohawkHair, flowing: FlowingHair,
  "wavy-warm": WavyWarmHair, "soft-long": SoftLongHair, dreamy: DreamyHair, "neat-bob": NeatBobHair, ethereal: EtherealHair, vintage: VintageHair,
  dreadlocks: DreadlocksHair, electric: ElectricHair, fade: FadeHair, "raw-spikes": RawSpikesHair,
};

export function HairPart({ style, color }: HairProps) {
  const Component = HAIR_MAP[style];
  return <Component color={color} />;
}
