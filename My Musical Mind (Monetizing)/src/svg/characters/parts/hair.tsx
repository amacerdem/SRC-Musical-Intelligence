/* ── Hair Styles (24 unique) — Enhanced with highlights, volume, strands ─
 *  Each persona has a unique hair style with:
 *  - Base mass (main color fill)
 *  - Highlight strands (lighter overlay)
 *  - Shadow depth (darker undertone)
 *  - Volume detail (additional shape layers)
 *  uid prop used for gradient references from SharedDefs
 * ──────────────────────────────────────────────────────────────────── */
import React from "react";
import type { HairStyle } from "../types";

interface HairProps {
  style: HairStyle;
  color: string;
  uid?: string;
}

/** Darken a hex color by mixing with black */
const darken = (hex: string) => hex + "CC";
/** Lighten a hex color for highlights */
const lighten = (hex: string) => hex + "90";

/* ═══════════ ALCHEMIST HAIR (4) ═══════════ */

/** #1 Dopamine Seeker — Flame-shaped, rising upward with inner glow */
const FlamesHair = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Base flame mass */}
    <path d="M72 56 Q68 30 80 18 Q86 28 88 20 Q94 32 100 14 Q106 32 112 20 Q118 28 120 18 Q132 30 128 56 Q128 38 100 32 Q72 38 72 56 Z" fill={color} />
    {/* Inner flame layer — darker */}
    <path d="M78 50 Q84 28 92 22 Q96 34 100 18 Q104 34 108 22 Q116 28 122 50" fill={color} opacity="0.75" />
    {/* Bright core flames */}
    <path d="M90 42 Q94 24 100 16 Q106 24 110 42" fill="white" opacity="0.12" />
    {/* Strand highlights */}
    <path d="M84 36 Q90 22 96 18" stroke="white" strokeWidth="1.5" fill="none" opacity="0.2" strokeLinecap="round" />
    <path d="M104 18 Q110 22 116 36" stroke="white" strokeWidth="1.5" fill="none" opacity="0.15" strokeLinecap="round" />
    {/* Ember tips */}
    <circle cx="80" cy="20" r="1.5" fill={color} opacity="0.6" />
    <circle cx="100" cy="12" r="2" fill="white" opacity="0.15" />
    <circle cx="120" cy="20" r="1.5" fill={color} opacity="0.6" />
    {/* Side wisps */}
    <path d="M72 52 Q68 46 66 38" stroke={color} strokeWidth="2" fill="none" opacity="0.5" strokeLinecap="round" />
    <path d="M128 52 Q132 46 134 38" stroke={color} strokeWidth="2" fill="none" opacity="0.5" strokeLinecap="round" />
  </g>
);

/** #6 Tension Architect — Tall structured spikes with geometric precision */
const SpikesHair = ({ color }: { color: string }) => (
  <g>
    {/* Base mass */}
    <path d="M74 58 Q74 40 100 30 Q126 40 126 58 Q116 46 100 40 Q84 46 74 58 Z" fill={color} opacity="0.8" />
    {/* Individual spikes — each with highlight edge */}
    <path d="M80 42 L80 12 L86 42" fill={color} />
    <path d="M81 38 L80 16" stroke="white" strokeWidth="0.6" fill="none" opacity="0.2" />
    <path d="M88 38 L88 8 L94 40" fill={color} />
    <path d="M89 34 L88 12" stroke="white" strokeWidth="0.6" fill="none" opacity="0.2" />
    <path d="M96 36 L100 4 L104 36" fill={color} />
    <path d="M97 32 L100 8" stroke="white" strokeWidth="0.8" fill="none" opacity="0.25" />
    <path d="M106 38 L112 8 L118 42" fill={color} />
    <path d="M107 34 L112 12" stroke="white" strokeWidth="0.6" fill="none" opacity="0.2" />
    <path d="M114 42 L120 12 L126 42" fill={color} />
    {/* Shadow at base */}
    <path d="M76 56 Q100 46 124 56" fill={color} opacity="0.5" />
  </g>
);

/** #7 Contrast Addict — Split two-tone with sharp divide */
const SplitHair = ({ color }: { color: string }) => (
  <g>
    {/* Left half — persona color */}
    <path d="M72 58 Q70 32 100 26 L100 58 Q86 48 72 58 Z" fill={color} />
    {/* Left highlight */}
    <path d="M78 42 Q88 34 98 30" stroke="white" strokeWidth="1" fill="none" opacity="0.15" />
    {/* Right half — white/silver */}
    <path d="M100 26 Q130 32 128 58 Q114 48 100 58 Z" fill="white" opacity="0.85" />
    {/* Right shadow detail */}
    <path d="M102 30 Q120 36 126 48" stroke="#ccc" strokeWidth="1" fill="none" opacity="0.3" />
    {/* Center part line — sharp */}
    <line x1="100" y1="26" x2="100" y2="58" stroke="#1a1a2e" strokeWidth="1.5" />
    {/* Volume strands */}
    <path d="M76 46 Q82 38 90 34" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" strokeLinecap="round" />
    <path d="M124 46 Q118 38 110 34" stroke="#ddd" strokeWidth="1.5" fill="none" opacity="0.3" strokeLinecap="round" />
    {/* Side tuck */}
    <path d="M72 58 Q70 64 72 68" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" strokeLinecap="round" />
    <path d="M128 58 Q130 64 128 68" stroke="#ddd" strokeWidth="2.5" fill="none" opacity="0.3" strokeLinecap="round" />
  </g>
);

/** #18 Dramatic Arc — Sweeping dramatic wave with theatrical volume */
const DramaticWaveHair = ({ color }: { color: string }) => (
  <g>
    {/* Main mass */}
    <path d="M68 62 Q64 30 100 22 Q136 30 132 62 Q128 38 100 32 Q72 38 68 62 Z" fill={color} />
    {/* Dramatic sweep to the right — larger, more theatrical */}
    <path d="M116 30 Q138 16 154 24 Q148 34 136 38" fill={color} opacity="0.85" />
    <path d="M120 34 Q142 22 152 28" fill={color} opacity="0.6" />
    <path d="M124 38 Q140 30 148 34" fill={color} opacity="0.4" />
    {/* Wave highlight */}
    <path d="M80 36 Q100 26 120 30 Q136 20 148 26" stroke="white" strokeWidth="1.2" fill="none" opacity="0.15" strokeLinecap="round" />
    {/* Volume depth at crown */}
    <ellipse cx="96" cy="32" rx="12" ry="4" fill="white" opacity="0.08" />
    {/* Under-wave shadow */}
    <path d="M70 56 Q86 48 100 46 Q114 48 128 52" stroke={color} strokeWidth="2" fill="none" opacity="0.4" />
  </g>
);

/* ═══════════ ARCHITECT HAIR (5) ═══════════ */

/** #2 Harmonic Purist — Slicked back, clean, precise */
const SlickHair = ({ color }: { color: string }) => (
  <g>
    {/* Base shape */}
    <path d="M74 58 Q72 38 100 28 Q128 38 126 58 Q120 44 100 38 Q80 44 74 58 Z" fill={color} />
    {/* Comb lines — precise, parallel */}
    <path d="M82 42 Q90 34 100 30" stroke="white" strokeWidth="0.8" fill="none" opacity="0.15" />
    <path d="M84 46 Q92 38 102 34" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    <path d="M86 50 Q94 42 104 38" stroke="white" strokeWidth="0.5" fill="none" opacity="0.1" />
    {/* Clean edge definition */}
    <path d="M74 58 Q76 54 80 50" stroke={color} strokeWidth="0.5" fill="none" opacity="0.5" />
    <path d="M126 58 Q124 54 120 50" stroke={color} strokeWidth="0.5" fill="none" opacity="0.5" />
    {/* Subtle gloss */}
    <ellipse cx="96" cy="36" rx="10" ry="4" fill="white" opacity="0.08" />
  </g>
);

/** #4 Minimal Zen — Buzzcut, ultra-clean */
const BuzzcutHair = ({ color }: { color: string }) => (
  <g>
    {/* Very thin hair layer */}
    <path d="M76 60 Q74 42 100 34 Q126 42 124 60 Q120 48 100 42 Q80 48 76 60 Z" fill={color} opacity="0.5" />
    {/* Stubble texture — refined dot pattern */}
    {[80, 86, 92, 98, 104, 110, 116, 120].map((x) => (
      <circle key={x} cx={x} cy={46 + (x % 3)} r="0.6" fill={color} opacity="0.35" />
    ))}
    {[84, 90, 96, 102, 108, 114].map((x) => (
      <circle key={`r2-${x}`} cx={x} cy={42 + (x % 2)} r="0.5" fill={color} opacity="0.25" />
    ))}
    {/* Hairline edge */}
    <path d="M78 56 Q100 48 122 56" stroke={color} strokeWidth="0.5" fill="none" opacity="0.3" />
  </g>
);

/** #5 Resolution Junkie — Structured geometric cut with hard part */
const StructuredHair = ({ color }: { color: string }) => (
  <g>
    {/* Main mass */}
    <path d="M72 58 Q70 34 100 24 Q130 34 128 58 Q124 40 100 32 Q76 40 72 58 Z" fill={color} />
    {/* Hard geometric part line */}
    <line x1="88" y1="28" x2="84" y2="58" stroke="#1a1a2e" strokeWidth="1.8" />
    {/* Side sweep — right side elevated */}
    <path d="M88 28 Q100 24 128 34" stroke={color} strokeWidth="2.5" fill="none" opacity="0.6" />
    {/* Volume highlight on swept side */}
    <path d="M92 30 Q108 26 124 34" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" />
    {/* Short side (left of part) */}
    <path d="M76 50 Q80 44 86 38" fill={color} opacity="0.7" />
    {/* Clean edge */}
    <path d="M74 58 Q74 52 76 48" stroke={color} strokeWidth="0.5" fill="none" opacity="0.4" />
  </g>
);

/** #9 Pattern Hunter — Medium, neatly combed, analytical */
const AnalyticalHair = ({ color }: { color: string }) => (
  <g>
    <path d="M74 58 Q72 34 100 26 Q128 34 126 58 Q122 42 100 36 Q78 42 74 58 Z" fill={color} />
    {/* Subtle side part */}
    <path d="M86 30 L84 56" stroke="#1a1a2e" strokeWidth="1" opacity="0.4" />
    {/* Wave detail — neat, controlled */}
    <path d="M86 30 Q94 28 100 28 Q112 28 120 32" stroke={color} strokeWidth="2" fill="none" opacity="0.5" />
    {/* Strand highlights */}
    <path d="M90 32 Q100 28 110 30" stroke="white" strokeWidth="0.7" fill="none" opacity="0.12" />
    <path d="M88 36 Q98 32 108 34" stroke="white" strokeWidth="0.5" fill="none" opacity="0.1" />
    {/* Ear tuck */}
    <path d="M74 58 Q72 62 74 66" stroke={color} strokeWidth="2" fill="none" opacity="0.3" strokeLinecap="round" />
    <path d="M126 58 Q128 62 126 66" stroke={color} strokeWidth="2" fill="none" opacity="0.3" strokeLinecap="round" />
  </g>
);

/** #20 Precision Mind — Perfectly symmetric, center-parted */
const PreciseHair = ({ color }: { color: string }) => (
  <g>
    <path d="M74 58 Q72 34 100 24 Q128 34 126 58 Q122 40 100 32 Q78 40 74 58 Z" fill={color} />
    {/* Perfect center part */}
    <line x1="100" y1="24" x2="100" y2="56" stroke="#1a1a2e" strokeWidth="1.2" />
    {/* Symmetric volume */}
    <path d="M76 46 Q88 34 100 32" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    <path d="M124 46 Q112 34 100 32" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    {/* Precise edge line */}
    <path d="M76 56 Q88 48 100 46 Q112 48 124 56" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Crown highlight */}
    <ellipse cx="100" cy="32" rx="8" ry="3" fill="white" opacity="0.1" />
  </g>
);

/* ═══════════ EXPLORER HAIR (5) ═══════════ */

/** #3 Chaos Explorer — Wild, untamed, strands everywhere */
const WildHair = ({ color }: { color: string }) => (
  <g>
    {/* Big wild mass */}
    <path d="M64 62 Q60 28 100 16 Q140 28 136 62 Q130 36 100 28 Q70 36 64 62 Z" fill={color} />
    {/* Wild strands */}
    <path d="M70 38 L56 26 L66 36" fill={color} />
    <path d="M130 38 L144 22 L134 36" fill={color} />
    <path d="M86 22 L76 6 L84 20" fill={color} />
    <path d="M114 22 L124 4 L116 20" fill={color} />
    <path d="M100 16 L98 2 L102 16" fill={color} />
    {/* Extra wild strands */}
    <path d="M66 48 L52 38 L62 46" fill={color} opacity="0.7" />
    <path d="M134 48 L148 38 L138 46" fill={color} opacity="0.7" />
    {/* Highlight strands */}
    <path d="M78 28 L70 12" stroke="white" strokeWidth="1" fill="none" opacity="0.15" strokeLinecap="round" />
    <path d="M122 28 L130 10" stroke="white" strokeWidth="1" fill="none" opacity="0.15" strokeLinecap="round" />
    <path d="M100 16 L100 6" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" strokeLinecap="round" />
    {/* Volume shadow */}
    <path d="M68 56 Q84 46 100 44 Q116 46 132 56" stroke={color} strokeWidth="2" fill="none" opacity="0.4" />
  </g>
);

/** #10 Sonic Nomad — Windswept, flowing in one direction */
const WindsweptHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 58 Q68 30 100 22 Q132 30 128 58 Q124 38 100 30 Q76 38 72 58 Z" fill={color} />
    {/* Wind-blown strands to the right — more layered */}
    <path d="M118 30 Q142 22 160 28" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M122 36 Q144 30 158 34" stroke={color} strokeWidth="3" fill="none" strokeLinecap="round" opacity="0.75" />
    <path d="M124 42 Q142 38 154 40" stroke={color} strokeWidth="2.5" fill="none" strokeLinecap="round" opacity="0.55" />
    <path d="M126 48 Q140 44 150 46" stroke={color} strokeWidth="2" fill="none" strokeLinecap="round" opacity="0.35" />
    {/* Highlight on wind strand */}
    <path d="M120 32 Q138 26 152 30" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" strokeLinecap="round" />
    {/* Root volume */}
    <ellipse cx="98" cy="34" rx="14" ry="4" fill="white" opacity="0.08" />
  </g>
);

/** #19 Curious Wanderer — Curly, free-flowing, bouncy */
const CurlyFreeHair = ({ color }: { color: string }) => (
  <g>
    {/* Base mass */}
    <path d="M70 62 Q66 30 100 20 Q134 30 130 62 Q126 38 100 30 Q74 38 70 62 Z" fill={color} />
    {/* Curly tendrils — more defined */}
    <path d="M72 48 Q66 42 70 36 Q74 30 72 24" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    <path d="M128 48 Q134 42 130 36 Q126 30 128 24" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    {/* Additional curl */}
    <path d="M76 56 Q70 52 72 46 Q74 40 72 36" stroke={color} strokeWidth="2.5" fill="none" strokeLinecap="round" opacity="0.6" />
    <path d="M124 56 Q130 52 128 46 Q126 40 128 36" stroke={color} strokeWidth="2.5" fill="none" strokeLinecap="round" opacity="0.6" />
    {/* Top curls — bouncy circles */}
    <circle cx="84" cy="22" r="6" fill={color} opacity="0.8" />
    <circle cx="100" cy="18" r="6" fill={color} />
    <circle cx="116" cy="22" r="6" fill={color} opacity="0.8" />
    {/* Highlight glints */}
    <circle cx="86" cy="20" r="1.5" fill="white" opacity="0.12" />
    <circle cx="100" cy="16" r="1.5" fill="white" opacity="0.15" />
    <circle cx="114" cy="20" r="1.5" fill="white" opacity="0.12" />
    {/* Shadow depth */}
    <path d="M74 56 Q86 46 100 44 Q114 46 126 56" fill={color} opacity="0.4" />
  </g>
);

/** #23 Edge Runner — Punk mohawk, aggressive and bold */
const MohawkHair = ({ color }: { color: string }) => (
  <g>
    {/* Shaved sides — texture */}
    <path d="M76 58 Q76 44 84 40 L84 58 Z" fill={color} opacity="0.15" />
    <path d="M124 58 Q124 44 116 40 L116 58 Z" fill={color} opacity="0.15" />
    {/* Shaved side stubble */}
    {[78, 80, 82].map((x) => (
      <React.Fragment key={x}>
        <circle cx={x} cy={48} r="0.4" fill={color} opacity="0.2" />
        <circle cx={x} cy={52} r="0.4" fill={color} opacity="0.15" />
      </React.Fragment>
    ))}
    {[118, 120, 122].map((x) => (
      <React.Fragment key={x}>
        <circle cx={x} cy={48} r="0.4" fill={color} opacity="0.2" />
        <circle cx={x} cy={52} r="0.4" fill={color} opacity="0.15" />
      </React.Fragment>
    ))}
    {/* Mohawk strip — tall and proud */}
    <path d="M88 58 Q86 20 100 6 Q114 20 112 58 Q106 34 100 28 Q94 34 88 58 Z" fill={color} />
    {/* Spiky tips */}
    <path d="M94 16 L90 2 L98 14" fill={color} />
    <path d="M100 6 L99 -4 L103 6" fill={color} />
    <path d="M106 16 L110 2 L102 14" fill={color} />
    {/* Center highlight */}
    <path d="M98 22 Q100 10 102 22" stroke="white" strokeWidth="0.8" fill="none" opacity="0.2" />
    {/* Edge glow */}
    <path d="M88 48 Q94 34 100 28 Q106 34 112 48" stroke="white" strokeWidth="0.5" fill="none" opacity="0.1" />
  </g>
);

/** #24 Renaissance Mind — Long, flowing, elegant with artistic flair */
const FlowingHair = ({ color }: { color: string }) => (
  <g>
    {/* Crown mass */}
    <path d="M68 62 Q64 30 100 20 Q136 30 132 62 Q128 38 100 28 Q72 38 68 62 Z" fill={color} />
    {/* Long flowing sides */}
    <path d="M68 62 Q64 80 66 100 Q68 110 72 116" stroke={color} strokeWidth="7" fill="none" strokeLinecap="round" />
    <path d="M132 62 Q136 80 134 100 Q132 110 128 116" stroke={color} strokeWidth="7" fill="none" strokeLinecap="round" />
    {/* Inner wave detail */}
    <path d="M70 72 Q68 88 70 104" stroke={color} strokeWidth="3.5" fill="none" opacity="0.5" strokeLinecap="round" />
    <path d="M130 72 Q132 88 130 104" stroke={color} strokeWidth="3.5" fill="none" opacity="0.5" strokeLinecap="round" />
    {/* Elegant wave highlights */}
    <path d="M66 76 Q62 88 66 100" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" strokeLinecap="round" />
    <path d="M134 76 Q138 88 134 100" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" strokeLinecap="round" />
    {/* Crown highlight */}
    <ellipse cx="100" cy="30" rx="14" ry="4" fill="white" opacity="0.1" />
    {/* Strand detail */}
    <path d="M78 38 Q88 30 100 26" stroke="white" strokeWidth="0.6" fill="none" opacity="0.1" />
    <path d="M122 38 Q112 30 100 26" stroke="white" strokeWidth="0.6" fill="none" opacity="0.1" />
  </g>
);

/* ═══════════ ANCHOR HAIR (6) ═══════════ */

/** #8 Structural Romantic — Warm waves, full and soft */
const WavyWarmHair = ({ color }: { color: string }) => (
  <g>
    <path d="M70 62 Q68 32 100 22 Q132 32 130 62 Q126 40 100 32 Q74 40 70 62 Z" fill={color} />
    {/* Gentle wave layers — multiple tiers */}
    <path d="M74 48 Q86 40 100 42 Q114 40 126 48" stroke={color} strokeWidth="2.5" fill="none" opacity="0.5" />
    <path d="M76 54 Q88 46 100 48 Q112 46 124 54" stroke={color} strokeWidth="2" fill="none" opacity="0.35" />
    {/* Soft side volume */}
    <path d="M70 62 Q66 72 68 84" stroke={color} strokeWidth="5" fill="none" strokeLinecap="round" opacity="0.6" />
    <path d="M130 62 Q134 72 132 84" stroke={color} strokeWidth="5" fill="none" strokeLinecap="round" opacity="0.6" />
    {/* Wave highlights */}
    <path d="M78 44 Q90 36 100 38" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" />
    <path d="M122 44 Q110 36 100 38" stroke="white" strokeWidth="0.8" fill="none" opacity="0.12" />
    {/* Crown shine */}
    <ellipse cx="100" cy="32" rx="10" ry="3" fill="white" opacity="0.08" />
  </g>
);

/** #11 Emotional Anchor — Soft, long, flowing down with warmth */
const SoftLongHair = ({ color }: { color: string }) => (
  <g>
    <path d="M68 62 Q64 30 100 20 Q136 30 132 62 Q128 38 100 28 Q72 38 68 62 Z" fill={color} />
    {/* Flowing down both sides — thick, soft */}
    <path d="M68 62 Q64 90 68 122" stroke={color} strokeWidth="9" fill="none" strokeLinecap="round" />
    <path d="M132 62 Q136 90 132 122" stroke={color} strokeWidth="9" fill="none" strokeLinecap="round" />
    {/* Inner strand layers */}
    <path d="M72 70 Q70 92 72 112" stroke={color} strokeWidth="4" fill="none" opacity="0.45" strokeLinecap="round" />
    <path d="M128 70 Q130 92 128 112" stroke={color} strokeWidth="4" fill="none" opacity="0.45" strokeLinecap="round" />
    {/* Highlight strands */}
    <path d="M66 72 Q64 88 66 104" stroke="white" strokeWidth="0.8" fill="none" opacity="0.1" strokeLinecap="round" />
    <path d="M134 72 Q136 88 134 104" stroke="white" strokeWidth="0.8" fill="none" opacity="0.1" strokeLinecap="round" />
    {/* Soft ends */}
    <circle cx="68" cy="122" r="3" fill={color} opacity="0.5" />
    <circle cx="132" cy="122" r="3" fill={color} opacity="0.5" />
  </g>
);

/** #13 Tonal Dreamer — Ethereal, cloud-like puffs */
const DreamyHair = ({ color }: { color: string }) => (
  <g>
    <path d="M68 60 Q64 28 100 18 Q136 28 132 60 Q128 36 100 28 Q72 36 68 60 Z" fill={color} />
    {/* Soft cloud-like puffs — more layered */}
    <circle cx="74" cy="42" r="9" fill={color} opacity="0.5" />
    <circle cx="126" cy="42" r="9" fill={color} opacity="0.5" />
    <circle cx="82" cy="28" r="8" fill={color} opacity="0.6" />
    <circle cx="118" cy="28" r="8" fill={color} opacity="0.6" />
    <circle cx="100" cy="22" r="9" fill={color} opacity="0.7" />
    {/* Inner glow puffs */}
    <circle cx="90" cy="32" r="5" fill="white" opacity="0.06" />
    <circle cx="110" cy="32" r="5" fill="white" opacity="0.06" />
    {/* Sparkle highlights */}
    <circle cx="84" cy="24" r="1" fill="white" opacity="0.2" />
    <circle cx="100" cy="18" r="1.2" fill="white" opacity="0.2" />
    <circle cx="116" cy="24" r="1" fill="white" opacity="0.2" />
    {/* Flowing wisps */}
    <path d="M68 56 Q62 50 58 56" stroke={color} strokeWidth="2" fill="none" opacity="0.3" strokeLinecap="round" />
    <path d="M132 56 Q138 50 142 56" stroke={color} strokeWidth="2" fill="none" opacity="0.3" strokeLinecap="round" />
  </g>
);

/** #15 Quiet Observer — Neat bob cut, composed */
const NeatBobHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 58 Q70 34 100 26 Q130 34 128 58 Q124 42 100 36 Q76 42 72 58 Z" fill={color} />
    {/* Clean bob sides */}
    <path d="M72 58 L70 82 Q72 86 76 86" fill={color} />
    <path d="M128 58 L130 82 Q128 86 124 86" fill={color} />
    {/* Fringe/bangs — layered */}
    <path d="M78 48 Q88 42 100 44 Q112 42 122 48" fill={color} opacity="0.65" />
    <path d="M80 52 Q90 46 100 47 Q110 46 120 52" fill={color} opacity="0.4" />
    {/* Highlight strand */}
    <path d="M82 40 Q92 34 100 34" stroke="white" strokeWidth="0.7" fill="none" opacity="0.12" />
    {/* Clean edge line */}
    <path d="M70 76 Q72 82 76 86" stroke={color} strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M130 76 Q128 82 124 86" stroke={color} strokeWidth="0.5" fill="none" opacity="0.4" />
  </g>
);

/** #17 Ambient Flow — Ethereal, misty, floating wisps */
const EtherealHair = ({ color }: { color: string }) => (
  <g>
    <path d="M66 62 Q62 26 100 16 Q138 26 134 62 Q130 34 100 26 Q70 34 66 62 Z" fill={color} opacity="0.8" />
    {/* Floating ethereal wisps — delicate */}
    <path d="M66 50 Q56 40 60 30" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" strokeLinecap="round" />
    <path d="M134 50 Q144 40 140 30" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" strokeLinecap="round" />
    {/* Additional floating wisps */}
    <path d="M62 42 Q52 36 54 26" stroke={color} strokeWidth="1.5" fill="none" opacity="0.25" strokeLinecap="round" />
    <path d="M138 42 Q148 36 146 26" stroke={color} strokeWidth="1.5" fill="none" opacity="0.25" strokeLinecap="round" />
    {/* Misty flowing sides */}
    <path d="M66 62 Q60 80 64 102" stroke={color} strokeWidth="5.5" fill="none" opacity="0.35" strokeLinecap="round" />
    <path d="M134 62 Q140 80 136 102" stroke={color} strokeWidth="5.5" fill="none" opacity="0.35" strokeLinecap="round" />
    {/* Sparkle dots — like floating particles */}
    <circle cx="58" cy="34" r="1.5" fill={color} opacity="0.5" />
    <circle cx="142" cy="34" r="1.5" fill={color} opacity="0.5" />
    <circle cx="54" cy="44" r="1" fill={color} opacity="0.3" />
    <circle cx="146" cy="44" r="1" fill={color} opacity="0.3" />
    {/* Inner glow */}
    <ellipse cx="100" cy="28" rx="16" ry="5" fill="white" opacity="0.06" />
  </g>
);

/** #22 Nostalgic Soul — Retro/vintage style with rolls */
const VintageHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 58 Q70 32 100 24 Q130 32 128 58 Q124 40 100 34 Q76 40 72 58 Z" fill={color} />
    {/* Retro wave on top — pronounced */}
    <path d="M80 36 Q86 26 96 28 Q106 26 112 30 Q118 28 122 36" fill={color} opacity="0.7" />
    <path d="M82 40 Q90 30 100 32 Q110 30 118 36" fill={color} opacity="0.5" />
    {/* Side rolls — more defined */}
    <path d="M72 58 Q68 62 66 70 Q64 76 68 78 Q72 76 72 70" fill={color} opacity="0.65" />
    <path d="M128 58 Q132 62 134 70 Q136 76 132 78 Q128 76 128 70" fill={color} opacity="0.65" />
    {/* Roll highlights */}
    <path d="M66 68 Q66 72 68 76" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    <path d="M134 68 Q134 72 132 76" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    {/* Crown wave highlight */}
    <path d="M84 30 Q96 24 108 28" stroke="white" strokeWidth="0.7" fill="none" opacity="0.1" />
  </g>
);

/* ═══════════ KINETICIST HAIR (4) ═══════════ */

/** #12 Rhythmic Pulse — Dreadlocks with beads */
const DreadlocksHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 56 Q70 34 100 26 Q130 34 128 56 Q124 40 100 34 Q76 40 72 56 Z" fill={color} />
    {/* Dreadlock strands — thicker, more defined */}
    <path d="M76 52 Q72 68 74 92" stroke={color} strokeWidth="4.5" fill="none" strokeLinecap="round" />
    <path d="M84 48 Q80 66 82 90" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M92 46 Q90 64 90 84" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    <path d="M108 46 Q110 64 110 84" stroke={color} strokeWidth="3.5" fill="none" strokeLinecap="round" />
    <path d="M116 48 Q120 66 118 90" stroke={color} strokeWidth="4" fill="none" strokeLinecap="round" />
    <path d="M124 52 Q128 68 126 92" stroke={color} strokeWidth="4.5" fill="none" strokeLinecap="round" />
    {/* Bead accents — more prominent */}
    <circle cx="74" cy="76" r="2.5" fill="white" opacity="0.5" />
    <circle cx="74" cy="82" r="2" fill={color} opacity="0.8" stroke="white" strokeWidth="0.5" />
    <circle cx="126" cy="76" r="2.5" fill="white" opacity="0.5" />
    <circle cx="118" cy="80" r="2" fill="gold" opacity="0.4" />
    {/* Strand highlights */}
    <path d="M78 56 Q76 68 78 80" stroke="white" strokeWidth="0.5" fill="none" opacity="0.1" />
    <path d="M122 56 Q124 68 122 80" stroke="white" strokeWidth="0.5" fill="none" opacity="0.1" />
  </g>
);

/** #14 Dynamic Storm — Electric, standing up with crackling energy */
const ElectricHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 56 Q68 28 100 16 Q132 28 128 56 Q124 36 100 28 Q76 36 72 56 Z" fill={color} />
    {/* Electric strands rising up */}
    <path d="M82 28 L76 6 L84 22" fill={color} />
    <path d="M92 22 L88 2 L96 18" fill={color} />
    <path d="M100 16 L100 -4 L104 16" fill={color} />
    <path d="M108 22 L112 2 L104 18" fill={color} />
    <path d="M118 28 L124 6 L116 22" fill={color} />
    {/* Electric sparkles — more prominent */}
    <path d="M76 10 L72 6 L80 8 L76 4" stroke="white" strokeWidth="0.8" fill="none" opacity="0.3" />
    <path d="M124 10 L128 6 L120 8 L124 4" stroke="white" strokeWidth="0.8" fill="none" opacity="0.3" />
    <path d="M100 -2 L96 -6 L104 -4" stroke="white" strokeWidth="0.8" fill="none" opacity="0.25" />
    {/* Energy glow at tips */}
    <circle cx="76" cy="6" r="2" fill="white" opacity="0.15" />
    <circle cx="100" cy="-2" r="2.5" fill="white" opacity="0.15" />
    <circle cx="124" cy="6" r="2" fill="white" opacity="0.15" />
    {/* Base crackle */}
    <path d="M80 50 L76 46 L82 48" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <path d="M120 50 L124 46 L118 48" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
  </g>
);

/** #16 Groove Mechanic — Clean fade with precision */
const FadeHair = ({ color }: { color: string }) => (
  <g>
    {/* Top — full color, shaped */}
    <path d="M78 56 Q78 38 100 30 Q122 38 122 56 Q118 44 100 38 Q82 44 78 56 Z" fill={color} />
    {/* Fade gradient — three opacity tiers */}
    <path d="M74 58 Q74 46 78 42 L78 58 Z" fill={color} opacity="0.4" />
    <path d="M126 58 Q126 46 122 42 L122 58 Z" fill={color} opacity="0.4" />
    <path d="M74 62 Q74 56 76 52" fill={color} opacity="0.2" />
    <path d="M126 62 Q126 56 124 52" fill={color} opacity="0.2" />
    {/* Skin-show fade line */}
    <path d="M76 58 Q76 54 78 50" stroke="#D4B08C" strokeWidth="0.4" fill="none" opacity="0.2" />
    <path d="M124 58 Q124 54 122 50" stroke="#D4B08C" strokeWidth="0.4" fill="none" opacity="0.2" />
    {/* Clean line detail on top */}
    <path d="M84 36 Q100 30 116 36" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    {/* Top highlight */}
    <path d="M88 34 Q100 30 112 34" stroke="white" strokeWidth="0.6" fill="none" opacity="0.12" />
    {/* Edge definition */}
    <path d="M78 56 Q100 48 122 56" stroke={color} strokeWidth="0.8" fill="none" opacity="0.4" />
  </g>
);

/** #21 Raw Energy — Raw, messy, explosive spikes */
const RawSpikesHair = ({ color }: { color: string }) => (
  <g>
    <path d="M72 58 Q68 30 100 18 Q132 30 128 58 Q124 36 100 28 Q76 36 72 58 Z" fill={color} />
    {/* Rough, asymmetric spikes — bolder */}
    <path d="M78 34 L66 12 L82 30" fill={color} />
    <path d="M88 26 L80 2 L94 22" fill={color} />
    <path d="M100 18 L96 -2 L104 18" fill={color} />
    <path d="M112 26 L122 6 L108 22" fill={color} />
    <path d="M122 34 L136 14 L118 30" fill={color} />
    {/* Extra asymmetric spike */}
    <path d="M74 40 L60 22 L76 36" fill={color} opacity="0.7" />
    {/* Messy texture strokes */}
    <path d="M84 38 L78 34" stroke={color} strokeWidth="2" fill="none" opacity="0.4" />
    <path d="M116 38 L122 34" stroke={color} strokeWidth="2" fill="none" opacity="0.4" />
    {/* Energy highlights at tips */}
    <circle cx="66" cy="12" r="2" fill="white" opacity="0.12" />
    <circle cx="80" cy="2" r="2" fill="white" opacity="0.12" />
    <circle cx="136" cy="14" r="2" fill="white" opacity="0.12" />
    {/* Base shadow */}
    <path d="M76 54 Q100 46 124 54" fill={color} opacity="0.3" />
  </g>
);

/* ═══════════ HAIR MAP ═══════════ */

const HAIR_MAP: Record<HairStyle, React.FC<{ color: string; uid?: string }>> = {
  flames: FlamesHair,
  spikes: SpikesHair,
  split: SplitHair,
  "dramatic-wave": DramaticWaveHair,
  slick: SlickHair,
  buzzcut: BuzzcutHair,
  structured: StructuredHair,
  analytical: AnalyticalHair,
  precise: PreciseHair,
  wild: WildHair,
  windswept: WindsweptHair,
  "curly-free": CurlyFreeHair,
  mohawk: MohawkHair,
  flowing: FlowingHair,
  "wavy-warm": WavyWarmHair,
  "soft-long": SoftLongHair,
  dreamy: DreamyHair,
  "neat-bob": NeatBobHair,
  ethereal: EtherealHair,
  vintage: VintageHair,
  dreadlocks: DreadlocksHair,
  electric: ElectricHair,
  fade: FadeHair,
  "raw-spikes": RawSpikesHair,
};

export function HairPart({ style, color, uid }: HairProps) {
  const Component = HAIR_MAP[style];
  return <Component color={color} uid={uid} />;
}
