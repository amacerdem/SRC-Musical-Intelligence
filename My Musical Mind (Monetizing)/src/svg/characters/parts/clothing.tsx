/* ── Clothing Styles — Enhanced Detailed SVG ────────────────────────── *
 *  Each of the 24 ClothingStyle variants rendered with 8-15 SVG elements:
 *  fabric folds, collar/neckline detail, shadow, seam/stitch lines,
 *  buttons/fasteners, pattern overlays, inner lining, hem detail.
 *
 *  Body coordinates: shoulders y≈124, torso y≈124-220, width x≈72-128
 * ──────────────────────────────────────────────────────────────────── */
import React from "react";
import type { ClothingStyle } from "../types";

interface ClothingProps {
  style: ClothingStyle;
  color: string;
  uid?: string;
}

const DARK = "#1a1a2e";
const DARK2 = "#2d2d44";

/** Returns fabric gradient fill if uid available, else solid DARK */
const torsoFill = (uid?: string) => (uid ? `url(#fabric-${uid})` : DARK);

/* ═══════════ ALCHEMIST CLOTHING (4) — Dark / Mysterious ═══════════ */

/** #1 — Cloak + Hoodie combo */
const CloakHoodie = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Hood outline behind head */}
    <path d="M66 62 Q64 44 100 36 Q136 44 134 62 Q130 48 100 42 Q70 48 66 62 Z" fill={DARK} opacity="0.5" />
    {/* Hood inner shadow */}
    <path d="M70 58 Q72 48 100 42 Q128 48 130 58" stroke={DARK2} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Cape flowing behind — left */}
    <path d="M70 130 Q60 180 56 240 Q66 250 80 248 L82 160 Z" fill={torsoFill(uid)} opacity="0.6" />
    {/* Cape flowing behind — right */}
    <path d="M130 130 Q140 180 144 240 Q134 250 120 248 L118 160 Z" fill={torsoFill(uid)} opacity="0.6" />
    {/* Inner lining peek — left */}
    <path d="M72 140 Q68 180 60 230 L68 232 Q72 185 76 140 Z" fill={color} opacity="0.08" />
    {/* Inner lining peek — right */}
    <path d="M128 140 Q132 180 140 230 L132 232 Q128 185 124 140 Z" fill={color} opacity="0.08" />
    {/* Fabric fold — left cape */}
    <path d="M68 170 Q66 190 62 220" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Fabric fold — right cape */}
    <path d="M132 170 Q134 190 138 220" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Collar trim accent */}
    <path d="M82 124 L100 134 L118 124" stroke={color} strokeWidth="2" fill="none" />
    {/* Shadow beneath collar */}
    <ellipse cx="100" cy="136" rx="16" ry="3" fill={DARK} opacity="0.15" />
    {/* Center line accent */}
    <line x1="100" y1="134" x2="100" y2="210" stroke={color} strokeWidth="1" opacity="0.3" />
    {/* Stitch detail on collar */}
    <path d="M84 126 L98 133" stroke={color} strokeWidth="0.5" strokeDasharray="2 3" fill="none" opacity="0.25" />
    <path d="M116 126 L102 133" stroke={color} strokeWidth="0.5" strokeDasharray="2 3" fill="none" opacity="0.25" />
    {/* Clasp at collar point */}
    <circle cx="100" cy="134" r="2.5" fill={color} opacity="0.4" />
    <circle cx="100" cy="134" r="1" fill={color} opacity="0.6" />
  </g>
);

/** #6 — Long cloak, floor-length */
const LongCloak = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Full cloak body */}
    <path d="M66 120 Q56 180 52 260 Q76 270 100 268 Q124 270 148 260 Q144 180 134 120 Z" fill={torsoFill(uid)} opacity="0.5" />
    {/* Left fabric fold */}
    <path d="M62 160 Q58 200 54 248" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.4" />
    {/* Right fabric fold */}
    <path d="M138 160 Q142 200 146 248" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.4" />
    {/* Center drape fold */}
    <path d="M98 150 Q96 190 97 250" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.3" />
    <path d="M102 150 Q104 190 103 250" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.3" />
    {/* Collar */}
    <path d="M80 124 L100 118 L120 124" stroke={color} strokeWidth="2" fill="none" />
    {/* Collar flare — left */}
    <path d="M80 124 L76 134 L84 130" fill={color} opacity="0.3" />
    {/* Collar flare — right */}
    <path d="M120 124 L124 134 L116 130" fill={color} opacity="0.3" />
    {/* Shadow beneath collar */}
    <ellipse cx="100" cy="130" rx="18" ry="3" fill={DARK} opacity="0.15" />
    {/* Mysterious sigil — outer */}
    <circle cx="100" cy="170" r="6" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    {/* Mysterious sigil — inner */}
    <circle cx="100" cy="170" r="2" fill={color} opacity="0.2" />
    {/* Sigil rays */}
    <line x1="100" y1="164" x2="100" y2="162" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="106" y1="170" x2="108" y2="170" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="100" y1="176" x2="100" y2="178" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="94" y1="170" x2="92" y2="170" stroke={color} strokeWidth="0.5" opacity="0.2" />
    {/* Hem stitch line */}
    <path d="M56 256 Q76 264 100 262 Q124 264 144 256" stroke={color} strokeWidth="0.5" strokeDasharray="3 4" fill="none" opacity="0.2" />
  </g>
);

/** #7 — Half contrast (split black/white) */
const HalfContrast = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Left half dark */}
    <path d="M74 124 L72 220 Q86 224 100 224 L100 124 Z" fill={torsoFill(uid)} />
    {/* Right half light */}
    <path d="M100 124 L100 224 Q114 224 128 220 L126 124 Z" fill="#e8e8e8" />
    {/* Left shadow overlay */}
    <path d="M74 124 L72 220 Q78 222 84 223 L86 124 Z" fill={DARK} opacity="0.1" />
    {/* Right shadow overlay */}
    <path d="M114 124 L114 223 Q122 222 128 220 L126 124 Z" fill="#ccc" opacity="0.15" />
    {/* Dividing line */}
    <line x1="100" y1="124" x2="100" y2="224" stroke={color} strokeWidth="1.5" />
    {/* Collar points */}
    <path d="M84 124 L100 136 L116 124" stroke={color} strokeWidth="1.5" fill="none" />
    {/* Shadow beneath collar */}
    <ellipse cx="100" cy="138" rx="14" ry="2.5" fill={DARK} opacity="0.12" />
    {/* Left fabric fold */}
    <path d="M80 150 Q78 180 76 210" stroke={DARK2} strokeWidth="0.6" fill="none" opacity="0.3" />
    {/* Right fabric fold */}
    <path d="M120 150 Q122 180 124 210" stroke="#bbb" strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Stitch along center seam */}
    <line x1="100" y1="140" x2="100" y2="220" stroke={color} strokeWidth="0.4" strokeDasharray="2 3" opacity="0.3" />
    {/* Button at split */}
    <circle cx="100" cy="160" r="2" fill={color} opacity="0.45" />
    <circle cx="100" cy="180" r="2" fill={color} opacity="0.45" />
    {/* Hem detail */}
    <path d="M72 218 Q86 222 100 222 Q114 222 128 218" stroke={color} strokeWidth="0.5" strokeDasharray="2 2" fill="none" opacity="0.2" />
  </g>
);

/** #18 — Theater cloak, dramatic collar */
const TheaterCloak = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* High dramatic collar — left */}
    <path d="M72 110 Q68 90 76 82 L80 124" fill={DARK2} />
    {/* High dramatic collar — right */}
    <path d="M128 110 Q132 90 124 82 L120 124" fill={DARK2} />
    {/* Collar inner edge gradient */}
    <path d="M76 86 Q78 100 80 120" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    <path d="M124 86 Q122 100 120 120" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Cape body */}
    <path d="M68 130 Q56 190 58 260 Q78 268 100 266 Q122 268 142 260 Q144 190 132 130 Z" fill={torsoFill(uid)} opacity="0.6" />
    {/* Inner lining peek — left */}
    <path d="M72 130 Q68 190 70 250 L80 248 Q78 190 80 130 Z" fill={color} opacity="0.15" />
    {/* Inner lining peek — right */}
    <path d="M128 130 Q132 190 130 250 L120 248 Q122 190 120 130 Z" fill={color} opacity="0.15" />
    {/* Left drape fold */}
    <path d="M64 170 Q60 210 60 250" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Right drape fold */}
    <path d="M136 170 Q140 210 140 250" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Center front fold */}
    <path d="M100 140 Q98 190 99 260" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Collar trim — left */}
    <path d="M76 82 L80 100" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    {/* Collar trim — right */}
    <path d="M124 82 L120 100" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    {/* Shadow beneath collar */}
    <ellipse cx="100" cy="130" rx="22" ry="3" fill={DARK} opacity="0.15" />
    {/* Hem detail */}
    <path d="M60 256 Q80 264 100 262 Q120 264 140 256" stroke={color} strokeWidth="0.5" strokeDasharray="3 4" fill="none" opacity="0.2" />
  </g>
);

/* ═══════════ ARCHITECT CLOTHING (5) — Clean / Structured ═══════════ */

/** #2 — Collar + shirt, clean */
const CollarShirt = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Shirt body */}
    <path d="M76 130 L74 218 Q87 222 100 222 Q113 222 126 218 L124 130 Z" fill={torsoFill(uid)} opacity="0.25" />
    {/* Collar wings — left */}
    <path d="M84 124 L78 130 L90 132 Z" fill="white" opacity="0.8" />
    {/* Collar wings — right */}
    <path d="M116 124 L122 130 L110 132 Z" fill="white" opacity="0.8" />
    {/* Collar shadow */}
    <ellipse cx="100" cy="134" rx="12" ry="2" fill={DARK} opacity="0.12" />
    {/* Tie knot */}
    <path d="M97 132 L100 138 L103 132 Z" fill={color} opacity="0.7" />
    {/* Tie body */}
    <path d="M98 138 L100 198 L102 138" fill={color} opacity="0.4" />
    {/* Tie stripe accent */}
    <line x1="99" y1="155" x2="101" y2="160" stroke="white" strokeWidth="0.4" opacity="0.3" />
    <line x1="99" y1="170" x2="101" y2="175" stroke="white" strokeWidth="0.4" opacity="0.3" />
    {/* Button placket seam */}
    <line x1="100" y1="132" x2="100" y2="218" stroke={DARK2} strokeWidth="0.4" opacity="0.2" />
    {/* Buttons */}
    <circle cx="100" cy="148" r="1.2" fill="white" opacity="0.3" />
    <circle cx="100" cy="164" r="1.2" fill="white" opacity="0.3" />
    <circle cx="100" cy="180" r="1.2" fill="white" opacity="0.3" />
    {/* Fabric fold — left */}
    <path d="M82 150 Q80 175 78 200" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Fabric fold — right */}
    <path d="M118 150 Q120 175 122 200" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Collar stitch detail */}
    <path d="M80 129 L88 131" stroke={DARK2} strokeWidth="0.3" strokeDasharray="1 2" fill="none" opacity="0.2" />
    <path d="M120 129 L112 131" stroke={DARK2} strokeWidth="0.3" strokeDasharray="1 2" fill="none" opacity="0.2" />
  </g>
);

/** #4 — Plain tee, minimal */
const PlainTee = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Tee body */}
    <path d="M78 128 L76 216 Q88 220 100 220 Q112 220 124 216 L122 128 Z" fill={torsoFill(uid)} opacity="0.2" />
    {/* Round neckline */}
    <path d="M88 124 Q100 130 112 124" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    {/* Neckline binding/ribbing */}
    <path d="M88 125 Q100 131 112 125" stroke={color} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Shadow beneath neckline */}
    <ellipse cx="100" cy="132" rx="10" ry="2" fill={DARK} opacity="0.1" />
    {/* Sleeve hem — left */}
    <path d="M78 128 Q74 134 72 144" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Sleeve hem — right */}
    <path d="M122 128 Q126 134 128 144" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Center chest crease */}
    <path d="M100 134 Q99 160 100 190" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.15" />
    {/* Side seam — left */}
    <line x1="77" y1="134" x2="76" y2="216" stroke={DARK2} strokeWidth="0.3" strokeDasharray="3 4" opacity="0.15" />
    {/* Side seam — right */}
    <line x1="123" y1="134" x2="124" y2="216" stroke={DARK2} strokeWidth="0.3" strokeDasharray="3 4" opacity="0.15" />
    {/* Hem line */}
    <path d="M76 216 Q88 220 100 220 Q112 220 124 216" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/** #5 — Formal jacket */
const FormalJacket = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Jacket body */}
    <path d="M74 130 L72 216 Q86 222 100 222 Q114 222 128 216 L126 130 Z" fill={torsoFill(uid)} opacity="0.3" />
    {/* Lapels — left */}
    <path d="M82 124 L76 142 L88 140 Z" fill={DARK2} />
    {/* Lapels — right */}
    <path d="M118 124 L124 142 L112 140 Z" fill={DARK2} />
    {/* Lapel shadow — left */}
    <path d="M78 136 L86 138" stroke={DARK} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Lapel shadow — right */}
    <path d="M122 136 L114 138" stroke={DARK} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Shadow beneath lapels */}
    <ellipse cx="100" cy="143" rx="14" ry="2" fill={DARK} opacity="0.12" />
    {/* Inner shirt peek */}
    <path d="M88 140 L100 146 L112 140" stroke="white" strokeWidth="0.5" fill="none" opacity="0.15" />
    {/* Jacket outline */}
    <path d="M76 142 L74 210 Q86 218 100 220 Q114 218 126 210 L124 142" stroke={DARK2} strokeWidth="1" fill="none" />
    {/* Button — upper */}
    <circle cx="100" cy="160" r="2" fill={color} opacity="0.5" />
    {/* Button — lower */}
    <circle cx="100" cy="176" r="2" fill={color} opacity="0.5" />
    {/* Button stitching (cross-hatch) */}
    <path d="M99 159 L101 161 M101 159 L99 161" stroke="white" strokeWidth="0.3" opacity="0.3" />
    <path d="M99 175 L101 177 M101 175 L99 177" stroke="white" strokeWidth="0.3" opacity="0.3" />
    {/* Pocket square accent */}
    <path d="M82 148 L86 144 L90 148 L86 150 Z" fill={color} opacity="0.4" />
    {/* Breast pocket line */}
    <path d="M82 146 L90 146" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.25" />
    {/* Side pocket — left */}
    <path d="M78 186 L92 186" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Side pocket — right */}
    <path d="M108 186 L122 186" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Front seam */}
    <line x1="100" y1="146" x2="100" y2="218" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.2" />
    {/* Cuff line — left */}
    <path d="M62 196 L66 198" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Cuff line — right */}
    <path d="M134 196 L138 198" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/** #9 — Argyle sweater */
const ArgyleSweater = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Sweater body */}
    <path d="M76 130 L74 216 Q88 220 100 220 Q112 220 126 216 L124 130 Z" fill={torsoFill(uid)} opacity="0.2" />
    {/* V-neck */}
    <path d="M86 124 L100 140 L114 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.5" />
    {/* V-neck ribbing double line */}
    <path d="M87 125 L100 141 L113 125" stroke={color} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Shadow beneath V-neck */}
    <ellipse cx="100" cy="142" rx="10" ry="2" fill={DARK} opacity="0.1" />
    {/* Argyle pattern — row 1 */}
    <path d="M84 150 L92 158 L84 166 L76 158 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    <path d="M100 142 L108 150 L100 158 L92 150 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    <path d="M116 150 L124 158 L116 166 L108 158 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    {/* Argyle pattern — row 2 */}
    <path d="M100 158 L108 166 L100 174 L92 166 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.15" />
    <path d="M84 166 L92 174 L84 182 L76 174 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.12" />
    <path d="M116 166 L124 174 L116 182 L108 174 Z" stroke={color} strokeWidth="0.8" fill="none" opacity="0.12" />
    {/* Argyle cross-lines */}
    <line x1="76" y1="150" x2="124" y2="150" stroke={color} strokeWidth="0.3" opacity="0.1" />
    <line x1="76" y1="166" x2="124" y2="166" stroke={color} strokeWidth="0.3" opacity="0.1" />
    {/* Ribbing at hem */}
    <path d="M74 212 Q88 216 100 216 Q112 216 126 212" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    <path d="M74 214 Q88 218 100 218 Q112 218 126 214" stroke={color} strokeWidth="0.6" fill="none" opacity="0.15" />
    {/* Side seam */}
    <line x1="76" y1="134" x2="74" y2="214" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.15" />
    <line x1="124" y1="134" x2="126" y2="214" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.15" />
  </g>
);

/** #20 — Lab coat */
const LabCoat = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* White coat body */}
    <path d="M74 124 L72 220 Q86 224 100 224 Q114 224 128 220 L126 124 Z" fill="white" opacity="0.15" />
    {/* Coat lapels — left */}
    <path d="M82 124 L76 140 L86 138 Z" fill="white" opacity="0.2" />
    {/* Coat lapels — right */}
    <path d="M118 124 L124 140 L114 138 Z" fill="white" opacity="0.2" />
    {/* Lapel shadow */}
    <ellipse cx="100" cy="141" rx="12" ry="2" fill={DARK} opacity="0.08" />
    {/* Inner shirt peek */}
    <path d="M86 138 Q100 144 114 138" stroke={torsoFill(uid)} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Front seam */}
    <line x1="100" y1="140" x2="100" y2="222" stroke={DARK2} strokeWidth="0.3" opacity="0.15" />
    {/* Breast pocket */}
    <rect x="80" y="148" width="12" height="10" rx="1" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Pen in pocket */}
    <line x1="84" y1="146" x2="84" y2="152" stroke={color} strokeWidth="1" opacity="0.4" />
    {/* Pen clip */}
    <line x1="83" y1="147" x2="85" y2="147" stroke={color} strokeWidth="0.5" opacity="0.3" />
    {/* Lower pocket — left */}
    <rect x="78" y="175" width="14" height="12" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Lower pocket — right */}
    <rect x="108" y="175" width="14" height="12" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Coat edge stitch */}
    <path d="M74 128 L72 220" stroke="white" strokeWidth="0.3" strokeDasharray="2 3" fill="none" opacity="0.12" />
    <path d="M126 128 L128 220" stroke="white" strokeWidth="0.3" strokeDasharray="2 3" fill="none" opacity="0.12" />
    {/* Hem line */}
    <path d="M72 218 Q86 222 100 222 Q114 222 128 218" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.15" />
  </g>
);

/* ═══════════ EXPLORER CLOTHING (5) — Rugged / Layered ═══════════ */

/** #3 — Hoodie + backpack */
const HoodieBackpack = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Hood behind */}
    <path d="M68 62 Q66 48 100 40 Q134 48 132 62 Q128 50 100 44 Q72 50 68 62 Z" fill={DARK2} opacity="0.4" />
    {/* Hood inner shadow */}
    <path d="M72 58 Q74 50 100 44 Q126 50 128 58" stroke={DARK} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Hoodie body */}
    <path d="M76 128 L74 216 Q88 220 100 220 Q112 220 126 216 L124 128 Z" fill={torsoFill(uid)} opacity="0.25" />
    {/* Hoodie strings — left */}
    <line x1="92" y1="128" x2="90" y2="150" stroke={color} strokeWidth="1" opacity="0.4" />
    {/* String aglet — left */}
    <rect x="89" y="148" width="2" height="4" rx="0.5" fill={color} opacity="0.3" />
    {/* Hoodie strings — right */}
    <line x1="108" y1="128" x2="110" y2="150" stroke={color} strokeWidth="1" opacity="0.4" />
    {/* String aglet — right */}
    <rect x="109" y="148" width="2" height="4" rx="0.5" fill={color} opacity="0.3" />
    {/* Backpack straps — left */}
    <path d="M82 130 L80 160" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" />
    {/* Backpack straps — right */}
    <path d="M118 130 L120 160" stroke={color} strokeWidth="2.5" fill="none" opacity="0.4" />
    {/* Strap stitch detail */}
    <path d="M81 134 L81 156" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 2" fill="none" opacity="0.2" />
    <path d="M119 134 L119 156" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 2" fill="none" opacity="0.2" />
    {/* Kangaroo pocket */}
    <path d="M86 180 Q100 188 114 180" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    {/* Pocket opening slit */}
    <path d="M88 182 Q100 186 112 182" stroke={color} strokeWidth="0.4" fill="none" opacity="0.2" />
    {/* Center seam fold */}
    <path d="M100 130 Q99 165 100 210" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.15" />
    {/* Hem ribbing */}
    <path d="M74 214 Q88 218 100 218 Q112 218 126 214" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/** #10 — Travel cloak */
const TravelCloak = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Flowing travel cape */}
    <path d="M66 130 Q58 190 64 258 Q82 266 100 264 Q118 266 136 258 Q142 190 134 130 Z" fill={torsoFill(uid)} opacity="0.4" />
    {/* Left drape fold */}
    <path d="M70 150 Q66 200 66 250" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Right drape fold */}
    <path d="M130 150 Q134 200 134 250" stroke={DARK2} strokeWidth="0.7" fill="none" opacity="0.35" />
    {/* Center drape fold */}
    <path d="M100 140 Q98 200 99 256" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.25" />
    {/* Brooch — outer ring */}
    <circle cx="100" cy="128" r="4" fill={color} opacity="0.5" />
    {/* Brooch — inner gem */}
    <circle cx="100" cy="128" r="2" fill={color} opacity="0.7" />
    {/* Brooch highlight */}
    <circle cx="99" cy="127" r="0.8" fill="white" opacity="0.3" />
    {/* Shoulder gather — left */}
    <path d="M72 132 Q68 136 66 142" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Shoulder gather — right */}
    <path d="M128 132 Q132 136 134 142" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Travel wear patches */}
    <rect x="78" y="175" width="8" height="6" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
    {/* Wind-blown edge */}
    <path d="M64 240 Q56 248 58 258" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    <path d="M136 240 Q144 248 142 258" stroke={color} strokeWidth="0.8" fill="none" opacity="0.15" />
    {/* Hem stitch */}
    <path d="M64 254 Q82 262 100 260 Q118 262 136 254" stroke={color} strokeWidth="0.4" strokeDasharray="3 3" fill="none" opacity="0.18" />
  </g>
);

/** #19 — Explorer jacket with pockets */
const ExplorerJacket = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Jacket body */}
    <path d="M74 128 L72 216 Q86 220 100 220 Q114 220 128 216 L126 128 Z" fill={torsoFill(uid)} opacity="0.25" />
    {/* Jacket collar — left */}
    <path d="M84 124 L80 132 L88 130 Z" fill={DARK2} />
    {/* Jacket collar — right */}
    <path d="M116 124 L120 132 L112 130 Z" fill={DARK2} />
    {/* Collar shadow */}
    <ellipse cx="100" cy="133" rx="12" ry="2" fill={DARK} opacity="0.1" />
    {/* Zipper line */}
    <line x1="100" y1="130" x2="100" y2="210" stroke={color} strokeWidth="1" opacity="0.3" />
    {/* Zipper teeth detail */}
    <line x1="99" y1="140" x2="101" y2="140" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="99" y1="150" x2="101" y2="150" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="99" y1="160" x2="101" y2="160" stroke={color} strokeWidth="0.5" opacity="0.2" />
    {/* Chest pockets */}
    <rect x="78" y="144" width="14" height="10" rx="2" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    <rect x="108" y="144" width="14" height="10" rx="2" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Chest pocket flaps */}
    <line x1="78" y1="148" x2="92" y2="148" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="108" y1="148" x2="122" y2="148" stroke={color} strokeWidth="0.5" opacity="0.2" />
    {/* Lower pockets */}
    <rect x="78" y="168" width="14" height="12" rx="2" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    <rect x="108" y="168" width="14" height="12" rx="2" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Pocket flaps */}
    <line x1="78" y1="172" x2="92" y2="172" stroke={color} strokeWidth="0.5" opacity="0.2" />
    <line x1="108" y1="172" x2="122" y2="172" stroke={color} strokeWidth="0.5" opacity="0.2" />
    {/* Shoulder epaulette — left */}
    <rect x="74" y="126" width="8" height="3" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Shoulder epaulette — right */}
    <rect x="118" y="126" width="8" height="3" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Hem detail */}
    <path d="M72 214 Q86 218 100 218 Q114 218 128 214" stroke={color} strokeWidth="0.4" strokeDasharray="2 3" fill="none" opacity="0.18" />
  </g>
);

/** #23 — Leather jacket */
const LeatherJacket = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Jacket body */}
    <path d="M74 130 L72 214 Q86 218 100 218 Q114 218 128 214 L126 130 Z" fill={torsoFill(uid)} opacity="0.3" />
    {/* Wide lapels — left */}
    <path d="M80 124 L72 144 L90 140 Z" fill={DARK2} />
    {/* Wide lapels — right */}
    <path d="M120 124 L128 144 L110 140 Z" fill={DARK2} />
    {/* Lapel fold shadow — left */}
    <path d="M76 138 L86 138" stroke={DARK} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Lapel fold shadow — right */}
    <path d="M124 138 L114 138" stroke={DARK} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Shadow beneath lapels */}
    <ellipse cx="100" cy="142" rx="14" ry="2.5" fill={DARK} opacity="0.12" />
    {/* Asymmetric zip */}
    <path d="M90 140 Q96 190 94 210" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    {/* Zip teeth markers */}
    <line x1="89" y1="155" x2="91" y2="155" stroke={color} strokeWidth="0.4" opacity="0.25" />
    <line x1="90" y1="170" x2="92" y2="170" stroke={color} strokeWidth="0.4" opacity="0.25" />
    <line x1="91" y1="185" x2="93" y2="185" stroke={color} strokeWidth="0.4" opacity="0.25" />
    {/* Studs on left */}
    <circle cx="82" cy="150" r="1.5" fill={color} opacity="0.3" />
    <circle cx="82" cy="158" r="1.5" fill={color} opacity="0.3" />
    <circle cx="82" cy="166" r="1.5" fill={color} opacity="0.3" />
    {/* Belt at waist */}
    <path d="M74 192 L126 192" stroke={DARK2} strokeWidth="1.5" fill="none" opacity="0.3" />
    {/* Belt buckle */}
    <rect x="96" y="190" width="8" height="4" rx="1" stroke={color} strokeWidth="0.6" fill="none" opacity="0.3" />
    {/* Leather crease — left */}
    <path d="M80 150 Q78 170 76 196" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Leather crease — right */}
    <path d="M120 150 Q122 170 124 196" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.25" />
  </g>
);

/** #24 — Layered bohemian */
const LayeredBohemian = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Outer layer body */}
    <path d="M72 136 L70 222 Q86 226 100 226 Q114 226 130 222 L128 136 Z" fill={torsoFill(uid)} opacity="0.2" />
    {/* Scarf/wrap */}
    <path d="M80 124 Q100 138 120 124 Q114 130 100 134 Q86 130 80 124 Z" fill={color} opacity="0.3" />
    {/* Scarf drape — left */}
    <path d="M82 130 Q78 150 80 165" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Scarf drape — right */}
    <path d="M118 130 Q122 150 120 165" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Scarf fringe detail */}
    <path d="M78 163 L80 168 M80 163 L82 168 M82 163 L84 168" stroke={color} strokeWidth="0.4" fill="none" opacity="0.2" />
    {/* Outer layer edge — left */}
    <path d="M74 140 L72 220" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    {/* Outer layer edge — right */}
    <path d="M126 140 L128 220" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    {/* Pattern strip — upper */}
    <path d="M80 170 Q90 168 100 170 Q110 168 120 170" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Pattern strip — lower */}
    <path d="M80 176 Q90 174 100 176 Q110 174 120 176" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    {/* Inner layer peek at neckline */}
    <path d="M86 132 Q100 138 114 132" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Fabric fold — left */}
    <path d="M78 155 Q76 185 74 215" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Fabric fold — right */}
    <path d="M122 155 Q124 185 126 215" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Hem fringe */}
    <path d="M72 220 Q86 224 100 224 Q114 224 128 220" stroke={color} strokeWidth="0.5" strokeDasharray="2 2" fill="none" opacity="0.2" />
  </g>
);

/* ═══════════ ANCHOR CLOTHING (6) — Warm / Comfortable ═══════════ */

/** #8 — Vintage jacket */
const VintageJacket = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Jacket body */}
    <path d="M76 130 L74 214 Q87 218 100 218 Q113 218 126 214 L124 130 Z" fill={torsoFill(uid)} opacity="0.25" />
    {/* Soft lapels — left */}
    <path d="M84 124 L78 138 L88 136 Z" fill={DARK2} opacity="0.7" />
    {/* Soft lapels — right */}
    <path d="M116 124 L122 138 L112 136 Z" fill={DARK2} opacity="0.7" />
    {/* Lapel shadow */}
    <ellipse cx="100" cy="139" rx="12" ry="2" fill={DARK} opacity="0.1" />
    {/* Inner shirt peek */}
    <path d="M88 136 Q100 142 112 136" stroke="white" strokeWidth="0.4" fill="none" opacity="0.12" />
    {/* Elbow patches — left */}
    <ellipse cx="62" cy="170" rx="4" ry="6" fill={color} opacity="0.15" />
    {/* Elbow patches — right */}
    <ellipse cx="138" cy="166" rx="4" ry="6" fill={color} opacity="0.15" />
    {/* Elbow patch stitch — left */}
    <ellipse cx="62" cy="170" rx="4" ry="6" stroke={color} strokeWidth="0.3" strokeDasharray="2 2" fill="none" opacity="0.12" />
    {/* Elbow patch stitch — right */}
    <ellipse cx="138" cy="166" rx="4" ry="6" stroke={color} strokeWidth="0.3" strokeDasharray="2 2" fill="none" opacity="0.12" />
    {/* Buttons */}
    <circle cx="100" cy="155" r="1.8" fill={color} opacity="0.3" />
    <circle cx="100" cy="170" r="1.8" fill={color} opacity="0.3" />
    <circle cx="100" cy="185" r="1.8" fill={color} opacity="0.3" />
    {/* Button thread detail */}
    <path d="M99 154 L101 156 M101 154 L99 156" stroke="white" strokeWidth="0.2" opacity="0.2" />
    {/* Front seam */}
    <line x1="100" y1="140" x2="100" y2="216" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.15" />
    {/* Pocket flap — left */}
    <path d="M80 184 L92 184" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Pocket flap — right */}
    <path d="M108 184 L120 184" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Hem detail */}
    <path d="M74 212 Q87 216 100 216 Q113 216 126 212" stroke={color} strokeWidth="0.4" fill="none" opacity="0.18" />
  </g>
);

/** #11 — Soft sweater */
const SoftSweater = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Sweater body */}
    <path d="M76 128 L74 216 Q88 220 100 220 Q112 220 126 216 L124 128 Z" fill={torsoFill(uid)} opacity="0.18" />
    {/* Round neckline */}
    <path d="M86 124 Q100 132 114 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    {/* Neckline ribbing */}
    <path d="M87 125 Q100 133 113 125" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Collar shadow */}
    <ellipse cx="100" cy="134" rx="12" ry="2" fill={DARK} opacity="0.08" />
    {/* Cozy knit texture hints — scattered */}
    <path d="M86 148 Q90 146 94 148" stroke={color} strokeWidth="0.4" fill="none" opacity="0.12" />
    <path d="M106 156 Q110 154 114 156" stroke={color} strokeWidth="0.4" fill="none" opacity="0.12" />
    <path d="M90 168 Q94 166 98 168" stroke={color} strokeWidth="0.4" fill="none" opacity="0.1" />
    <path d="M102 178 Q106 176 110 178" stroke={color} strokeWidth="0.4" fill="none" opacity="0.1" />
    {/* Side seam — left */}
    <line x1="76" y1="132" x2="74" y2="214" stroke={DARK2} strokeWidth="0.3" strokeDasharray="3 4" opacity="0.12" />
    {/* Side seam — right */}
    <line x1="124" y1="132" x2="126" y2="214" stroke={DARK2} strokeWidth="0.3" strokeDasharray="3 4" opacity="0.12" />
    {/* Soft ribbing at hem — upper */}
    <path d="M74 208 Q88 214 100 214 Q112 214 126 208" stroke={color} strokeWidth="0.8" fill="none" opacity="0.2" />
    {/* Soft ribbing at hem — lower */}
    <path d="M74 212 Q88 218 100 218 Q112 218 126 212" stroke={color} strokeWidth="0.8" fill="none" opacity="0.15" />
    {/* Subtle center fold */}
    <path d="M100 136 Q99 170 100 210" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.1" />
  </g>
);

/** #13 — Flowing dress */
const FlowingDress = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Dress silhouette — flows outward */}
    <path d="M82 124 Q78 160 68 240 Q84 250 100 248 Q116 250 132 240 Q122 160 118 124 Z" fill={color} opacity="0.15" />
    {/* Bodice overlay */}
    <path d="M82 124 Q80 145 80 160 L120 160 Q120 145 118 124 Z" fill={torsoFill(uid)} opacity="0.12" />
    {/* Neckline */}
    <path d="M86 124 Q100 130 114 124" stroke={color} strokeWidth="1" fill="none" opacity="0.4" />
    {/* Neckline shadow */}
    <ellipse cx="100" cy="132" rx="12" ry="2" fill={DARK} opacity="0.08" />
    {/* Waistline gather */}
    <path d="M80 160 Q100 164 120 160" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Flow lines — left */}
    <path d="M78 170 Q76 200 70 235" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Flow lines — right */}
    <path d="M122 170 Q124 200 130 235" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Inner flow fold */}
    <path d="M92 165 Q90 200 86 240" stroke={color} strokeWidth="0.3" fill="none" opacity="0.15" />
    <path d="M108 165 Q110 200 114 240" stroke={color} strokeWidth="0.3" fill="none" opacity="0.15" />
    {/* Center drape */}
    <path d="M100 164 Q98 205 100 244" stroke={color} strokeWidth="0.4" fill="none" opacity="0.12" />
    {/* Hem detail */}
    <path d="M68 238 Q84 246 100 244 Q116 246 132 238" stroke={color} strokeWidth="0.5" strokeDasharray="3 3" fill="none" opacity="0.2" />
    {/* Small decorative element at bodice */}
    <circle cx="100" cy="140" r="1.5" fill={color} opacity="0.2" />
  </g>
);

/** #15 — Cardigan */
const Cardigan = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Cardigan body */}
    <path d="M74 128 L72 214 Q86 218 100 218 Q114 218 128 214 L126 128 Z" fill={torsoFill(uid)} opacity="0.18" />
    {/* Open front — left edge */}
    <path d="M84 124 L82 210" stroke={DARK2} strokeWidth="1.5" fill="none" />
    {/* Open front — right edge */}
    <path d="M116 124 L118 210" stroke={DARK2} strokeWidth="1.5" fill="none" />
    {/* Inner shirt peek */}
    <path d="M88 128 Q100 134 112 128" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    {/* Inner shirt V peek */}
    <path d="M90 130 L100 140 L110 130" stroke="white" strokeWidth="0.3" fill="none" opacity="0.1" />
    {/* Button — left */}
    <circle cx="83" cy="150" r="1.5" fill={color} opacity="0.3" />
    {/* Button — center-left */}
    <circle cx="83" cy="165" r="1.5" fill={color} opacity="0.3" />
    {/* Button — lower-left */}
    <circle cx="83" cy="180" r="1.5" fill={color} opacity="0.25" />
    {/* Buttonhole — right side */}
    <line x1="116" y1="149" x2="118" y2="151" stroke={DARK2} strokeWidth="0.4" opacity="0.2" />
    <line x1="116" y1="164" x2="118" y2="166" stroke={DARK2} strokeWidth="0.4" opacity="0.2" />
    <line x1="116" y1="179" x2="118" y2="181" stroke={DARK2} strokeWidth="0.4" opacity="0.2" />
    {/* Fabric fold */}
    <path d="M90 145 Q88 170 86 200" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.15" />
    <path d="M110 145 Q112 170 114 200" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.15" />
    {/* Ribbing at hem */}
    <path d="M72 210 Q86 214 100 214 Q114 214 128 210" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    <path d="M72 212 Q86 216 100 216 Q114 216 128 212" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
  </g>
);

/** #17 — Long skirt / flowing bottom */
const LongSkirt = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Top: simple fitted */}
    <path d="M80 124 L78 188 L122 188 L120 124 Z" fill={torsoFill(uid)} opacity="0.15" />
    {/* Neckline */}
    <path d="M86 124 Q100 132 114 124" stroke={color} strokeWidth="1" fill="none" opacity="0.3" />
    {/* Neckline shadow */}
    <ellipse cx="100" cy="133" rx="10" ry="2" fill={DARK} opacity="0.08" />
    {/* Flowing skirt from waist */}
    <path d="M80 190 Q74 220 66 260 Q84 268 100 266 Q116 268 134 260 Q126 220 120 190 Z" fill={color} opacity="0.12" />
    {/* Waist belt */}
    <line x1="78" y1="190" x2="122" y2="190" stroke={color} strokeWidth="1" opacity="0.3" />
    {/* Belt buckle */}
    <rect x="96" y="188" width="8" height="4" rx="1" stroke={color} strokeWidth="0.5" fill="none" opacity="0.25" />
    {/* Skirt flow lines */}
    <path d="M82 194 Q78 225 72 256" stroke={color} strokeWidth="0.4" fill="none" opacity="0.18" />
    <path d="M100 192 Q99 225 100 260" stroke={color} strokeWidth="0.3" fill="none" opacity="0.12" />
    <path d="M118 194 Q122 225 128 256" stroke={color} strokeWidth="0.4" fill="none" opacity="0.18" />
    {/* Top fabric fold */}
    <path d="M86 140 Q84 160 82 184" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.12" />
    {/* Skirt hem */}
    <path d="M66 258 Q84 266 100 264 Q116 266 134 258" stroke={color} strokeWidth="0.5" strokeDasharray="2 3" fill="none" opacity="0.2" />
  </g>
);

/** #22 — Retro jacket */
const RetroJacket = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Jacket body */}
    <path d="M76 130 L74 214 Q87 218 100 218 Q113 218 126 214 L124 130 Z" fill={torsoFill(uid)} opacity="0.25" />
    {/* Wide collar — left */}
    <path d="M80 124 L72 140 L92 138 Z" fill={DARK2} opacity="0.6" />
    {/* Wide collar — right */}
    <path d="M120 124 L128 140 L108 138 Z" fill={DARK2} opacity="0.6" />
    {/* Collar edge highlight */}
    <path d="M74 138 L90 136" stroke={color} strokeWidth="0.4" fill="none" opacity="0.15" />
    <path d="M126 138 L110 136" stroke={color} strokeWidth="0.4" fill="none" opacity="0.15" />
    {/* Collar shadow */}
    <ellipse cx="100" cy="140" rx="14" ry="2" fill={DARK} opacity="0.1" />
    {/* Retro stripes — triple band */}
    <line x1="78" y1="150" x2="122" y2="150" stroke={color} strokeWidth="1.5" opacity="0.2" />
    <line x1="78" y1="156" x2="122" y2="156" stroke={color} strokeWidth="1" opacity="0.15" />
    <line x1="78" y1="160" x2="122" y2="160" stroke={color} strokeWidth="1.5" opacity="0.2" />
    {/* Front zipper */}
    <line x1="100" y1="138" x2="100" y2="214" stroke={DARK2} strokeWidth="0.4" opacity="0.2" />
    {/* Side pocket welts */}
    <path d="M80 180 L92 180" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    <path d="M108 180 L120 180" stroke={DARK2} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Cuff stripes — left */}
    <line x1="62" y1="194" x2="68" y2="194" stroke={color} strokeWidth="0.5" opacity="0.15" />
    <line x1="62" y1="196" x2="68" y2="196" stroke={color} strokeWidth="0.5" opacity="0.15" />
    {/* Cuff stripes — right */}
    <line x1="132" y1="194" x2="138" y2="194" stroke={color} strokeWidth="0.5" opacity="0.15" />
    <line x1="132" y1="196" x2="138" y2="196" stroke={color} strokeWidth="0.5" opacity="0.15" />
    {/* Hem detail */}
    <path d="M74 212 Q87 216 100 216 Q113 216 126 212" stroke={color} strokeWidth="0.4" fill="none" opacity="0.18" />
  </g>
);

/* ═══════════ KINETICIST CLOTHING (4) — Raw / Functional ═══════════ */

/** #12 — Tank top */
const TankTop = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Tank body */}
    <path d="M82 128 L80 210 Q90 214 100 214 Q110 214 120 210 L118 128 Z" fill={torsoFill(uid)} opacity="0.2" />
    {/* Wide neckline */}
    <path d="M84 124 Q100 128 116 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    {/* Neckline binding */}
    <path d="M85 125 Q100 129 115 125" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Neckline shadow */}
    <ellipse cx="100" cy="130" rx="14" ry="2" fill={DARK} opacity="0.08" />
    {/* Tank straps — left */}
    <line x1="86" y1="120" x2="86" y2="130" stroke={color} strokeWidth="2" opacity="0.3" />
    {/* Tank straps — right */}
    <line x1="114" y1="120" x2="114" y2="130" stroke={color} strokeWidth="2" opacity="0.3" />
    {/* Armhole curve — left */}
    <path d="M82 128 Q78 132 76 140" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Armhole curve — right */}
    <path d="M118 128 Q122 132 124 140" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Center chest crease */}
    <path d="M100 130 Q99 165 100 200" stroke={DARK2} strokeWidth="0.4" fill="none" opacity="0.12" />
    {/* Loose bottom */}
    <path d="M80 208 Q90 212 100 212 Q110 212 120 208" stroke={color} strokeWidth="1" fill="none" opacity="0.2" />
    {/* Side seams */}
    <line x1="82" y1="130" x2="80" y2="210" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.12" />
    <line x1="118" y1="130" x2="120" y2="210" stroke={DARK2} strokeWidth="0.3" strokeDasharray="2 3" opacity="0.12" />
  </g>
);

/** #14 — Torn tee, raw */
const TornTee = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Tee body */}
    <path d="M78 126 L76 214 Q88 218 100 218 Q112 218 124 214 L122 126 Z" fill={torsoFill(uid)} opacity="0.18" />
    {/* Ragged neckline */}
    <path d="M84 124 Q90 128 96 126 Q100 130 104 126 Q110 128 116 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    {/* Neckline shadow */}
    <ellipse cx="100" cy="130" rx="12" ry="2" fill={DARK} opacity="0.08" />
    {/* Tear marks — left side */}
    <path d="M78 188 L82 184 L80 192 L84 190" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Tear marks — right side */}
    <path d="M120 178 L118 174 L122 180" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Small rip near hem */}
    <path d="M90 206 L92 202 L94 208" stroke={color} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Graphic symbol on chest */}
    <path d="M96 156 L100 148 L104 156 L100 152 Z" fill={color} opacity="0.2" />
    {/* Faded print effect around graphic */}
    <circle cx="100" cy="152" r="8" stroke={color} strokeWidth="0.3" fill="none" opacity="0.08" />
    {/* Wrinkle texture — scattered */}
    <path d="M86 140 Q88 138 90 140" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.15" />
    <path d="M110 164 Q112 162 114 164" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.15" />
    <path d="M88 194 Q90 192 92 194" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.12" />
    {/* Ragged hem */}
    <path d="M76 212 Q82 216 88 212 Q94 218 100 214 Q106 218 112 212 Q118 216 124 212" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/** #16 — Mechanic apron */
const MechanicApron = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Undershirt */}
    <path d="M78 124 L76 216 Q88 220 100 220 Q112 220 124 216 L122 124 Z" fill={torsoFill(uid)} opacity="0.15" />
    {/* Undershirt neckline */}
    <path d="M86 124 Q100 130 114 124" stroke={DARK2} strokeWidth="0.6" fill="none" opacity="0.2" />
    {/* Apron bib over shirt */}
    <path d="M84 140 L82 210 Q100 216 118 210 L116 140 Z" fill={DARK2} opacity="0.4" />
    {/* Apron strap — left */}
    <path d="M84 140 L88 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    {/* Apron strap — right */}
    <path d="M116 140 L112 124" stroke={color} strokeWidth="1.5" fill="none" opacity="0.4" />
    {/* Strap buckle/hardware — left */}
    <rect x="85" y="130" width="4" height="3" rx="0.5" fill={color} opacity="0.3" />
    {/* Strap buckle/hardware — right */}
    <rect x="111" y="130" width="4" height="3" rx="0.5" fill={color} opacity="0.3" />
    {/* Top stitch on bib */}
    <path d="M86 142 L86 206" stroke={color} strokeWidth="0.3" strokeDasharray="2 3" fill="none" opacity="0.15" />
    <path d="M114 142 L114 206" stroke={color} strokeWidth="0.3" strokeDasharray="2 3" fill="none" opacity="0.15" />
    {/* Tool pocket — left */}
    <rect x="88" y="168" width="10" height="14" rx="1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Tool pocket — right */}
    <rect x="102" y="168" width="10" height="14" rx="1" stroke={color} strokeWidth="0.8" fill="none" opacity="0.3" />
    {/* Tool peeking out */}
    <line x1="92" y1="166" x2="93" y2="172" stroke={color} strokeWidth="0.8" opacity="0.25" />
    <line x1="106" y1="166" x2="107" y2="171" stroke={color} strokeWidth="0.8" opacity="0.25" />
    {/* Apron hem */}
    <path d="M82 208 Q100 214 118 208" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/** #21 — Sleeveless hoodie */
const SleevelessHoodie = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* Hood behind */}
    <path d="M70 60 Q68 44 100 38 Q132 44 130 60 Q126 48 100 42 Q74 48 70 60 Z" fill={DARK2} opacity="0.3" />
    {/* Hood inner shadow */}
    <path d="M74 56 Q76 48 100 42 Q124 48 126 56" stroke={DARK} strokeWidth="0.5" fill="none" opacity="0.2" />
    {/* Hoodie body */}
    <path d="M80 126 L78 214 Q89 218 100 218 Q111 218 122 214 L120 126 Z" fill={torsoFill(uid)} opacity="0.22" />
    {/* Sleeveless cutout edges — left */}
    <path d="M80 124 Q78 128 76 136" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
    {/* Sleeveless cutout edges — right */}
    <path d="M120 124 Q122 128 124 136" stroke={color} strokeWidth="1.5" fill="none" opacity="0.3" />
    {/* Armhole binding — left */}
    <path d="M80 125 Q78 129 76 137" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
    {/* Armhole binding — right */}
    <path d="M120 125 Q122 129 124 137" stroke={color} strokeWidth="0.5" fill="none" opacity="0.15" />
    {/* Hoodie string — left */}
    <line x1="94" y1="128" x2="92" y2="146" stroke={color} strokeWidth="0.8" opacity="0.3" />
    {/* String aglet — left */}
    <rect x="91" y="144" width="2" height="3" rx="0.5" fill={color} opacity="0.25" />
    {/* Hoodie string — right */}
    <line x1="106" y1="128" x2="108" y2="146" stroke={color} strokeWidth="0.8" opacity="0.3" />
    {/* String aglet — right */}
    <rect x="107" y="144" width="2" height="3" rx="0.5" fill={color} opacity="0.25" />
    {/* Center kangaroo pocket */}
    <path d="M88 178 Q100 184 112 178" stroke={color} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Pocket opening */}
    <path d="M90 180 Q100 182 110 180" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.15" />
    {/* Fabric fold */}
    <path d="M100 132 Q99 170 100 210" stroke={DARK2} strokeWidth="0.3" fill="none" opacity="0.1" />
    {/* Hem ribbing */}
    <path d="M78 212 Q89 216 100 216 Q111 216 122 212" stroke={color} strokeWidth="0.5" fill="none" opacity="0.2" />
  </g>
);

/* ═══════════ CLOTHING MAP ═══════════ */

const CLOTHING_MAP: Record<ClothingStyle, React.FC<{ color: string; uid?: string }>> = {
  "cloak-hoodie": CloakHoodie,
  "long-cloak": LongCloak,
  "half-contrast": HalfContrast,
  "theater-cloak": TheaterCloak,
  "collar-shirt": CollarShirt,
  "plain-tee": PlainTee,
  "formal-jacket": FormalJacket,
  "argyle-sweater": ArgyleSweater,
  "lab-coat": LabCoat,
  "hoodie-backpack": HoodieBackpack,
  "travel-cloak": TravelCloak,
  "explorer-jacket": ExplorerJacket,
  "leather-jacket": LeatherJacket,
  "layered-bohemian": LayeredBohemian,
  "vintage-jacket": VintageJacket,
  "soft-sweater": SoftSweater,
  "flowing-dress": FlowingDress,
  cardigan: Cardigan,
  "long-skirt": LongSkirt,
  "retro-jacket": RetroJacket,
  "tank-top": TankTop,
  "torn-tee": TornTee,
  "mechanic-apron": MechanicApron,
  "sleeveless-hoodie": SleevelessHoodie,
};

export function ClothingPart({ style, color, uid }: ClothingProps) {
  const Component = CLOTHING_MAP[style];
  return <Component color={color} uid={uid} />;
}
