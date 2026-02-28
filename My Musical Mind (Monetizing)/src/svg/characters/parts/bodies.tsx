/* ── Body Shapes ─────────────────────────────────────────────────────── */
import React from "react";
import type { HeadShape } from "../types";

interface BodyProps {
  shape: HeadShape;
  color: string;
  uid?: string;
}

const SKIN = "#F0D5B8";
const SKIN_SHADOW = "#D4B08C";
const CLOTH_MAIN = "#1a1a2e";
const CLOTH_SEC = "#2d2d44";

/* ── Helper: torso fill uses shared fabric gradient when uid present ── */
const torsoFill = (uid?: string) =>
  uid ? `url(#fabric-${uid})` : CLOTH_MAIN;

/* ────────────────────────────────────────────────────────────────────── */
/*  ANGULAR — Alchemists                                                 */
/*  Slim, slight lean, one hand raised, dramatic stance                  */
/* ────────────────────────────────────────────────────────────────────── */
const AngularBody = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* ── Shoulder definition ── */}
    <ellipse cx="100" cy="128" rx="28" ry="6" fill={CLOTH_SEC} opacity="0.7" />
    <ellipse cx="100" cy="128" rx="26" ry="5" fill={torsoFill(uid)} />

    {/* ── Main torso — slim, slight rightward lean ── */}
    <path
      d="M82 124 Q78 126 75 148 L73 178 L72 210
         Q86 218 100 220 Q114 218 128 210
         L127 178 L126 148 Q122 126 118 124 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Collar / neckline accent ── */}
    <path
      d="M88 124 Q94 130 100 131 Q106 130 112 124"
      stroke={color} strokeWidth="2" fill="none" opacity="0.7"
    />
    <path
      d="M92 125 L100 134 L108 125"
      fill={color} opacity="0.15"
    />

    {/* ── Torso fold lines ── */}
    <path d="M88 148 Q96 152 104 148" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.4" />
    <path d="M84 172 Q94 176 108 170" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.35" />
    <path d="M86 196 Q98 200 112 194" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.3" />

    {/* ── LEFT ARM — relaxed, angled down ── */}
    {/* Upper arm */}
    <path
      d="M76 130 Q68 148 62 168 L56 178 Q54 180 58 182 L66 174 Q72 154 78 136 Z"
      fill={SKIN}
    />
    {/* Forearm shadow */}
    <path
      d="M68 156 Q64 168 60 178 L56 178 Q60 166 64 154 Z"
      fill={SKIN_SHADOW} opacity="0.5"
    />
    {/* Left hand — simplified 3-finger */}
    <path
      d="M56 178 Q52 182 50 186 L52 187 L55 183
         Q54 186 53 190 L55 190 L57 185
         Q56 188 56 192 L58 191 L59 184
         L62 182 Z"
      fill={SKIN}
    />
    <path d="M56 178 L58 182" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.5" />

    {/* ── RIGHT ARM — raised dramatically ── */}
    {/* Upper arm */}
    <path
      d="M122 130 Q130 136 138 146 L148 154 Q152 150 148 148 L140 140 Q132 132 124 128 Z"
      fill={SKIN}
    />
    {/* Forearm going upward */}
    <path
      d="M138 146 Q142 142 146 136 L150 128 Q152 126 148 126 L144 132 Q140 140 136 146 Z"
      fill={SKIN}
    />
    {/* Forearm shadow */}
    <path
      d="M140 142 Q144 136 148 128 L146 128 Q142 136 138 142 Z"
      fill={SKIN_SHADOW} opacity="0.4"
    />
    {/* Right hand — raised, fingers spread */}
    <path
      d="M148 128 Q150 122 148 118 L146 118 L147 124
         Q150 120 152 116 L150 116 L148 122
         Q152 118 154 114 L152 114 L149 120
         L148 126 Z"
      fill={SKIN}
    />

    {/* ── LEFT LEG ── */}
    <path
      d="M86 218 Q84 238 82 254 L80 262 Q78 264 76 266
         L72 268 L88 268 L86 264 L84 254
         Q86 236 90 218 Z"
      fill={CLOTH_MAIN}
    />
    {/* Inseam shadow */}
    <path d="M88 220 Q87 240 86 258" stroke={CLOTH_SEC} strokeWidth="1" fill="none" opacity="0.4" />

    {/* ── RIGHT LEG ── */}
    <path
      d="M110 218 Q112 238 114 254 L116 262 Q118 264 120 266
         L124 268 L108 268 L110 264 L112 254
         Q110 236 108 218 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M110 220 Q111 240 112 258" stroke={CLOTH_SEC} strokeWidth="1" fill="none" opacity="0.4" />

    {/* ── LEFT SHOE ── */}
    <path
      d="M72 266 Q68 268 66 270 Q66 274 72 276 L88 276 Q90 274 90 272 Q90 268 88 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="68" y1="274" x2="88" y2="274" stroke="#444" strokeWidth="0.7" opacity="0.5" />
    <circle cx="78" cy="269" r="0.8" fill="#555" opacity="0.4" />
    <circle cx="81" cy="269" r="0.8" fill="#555" opacity="0.4" />

    {/* ── RIGHT SHOE ── */}
    <path
      d="M108 266 Q106 268 106 270 Q106 274 110 276 L126 276 Q130 274 130 270 Q128 268 124 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="110" y1="274" x2="128" y2="274" stroke="#444" strokeWidth="0.7" opacity="0.5" />
    <circle cx="116" cy="269" r="0.8" fill="#555" opacity="0.4" />
    <circle cx="119" cy="269" r="0.8" fill="#555" opacity="0.4" />
  </g>
);

/* ────────────────────────────────────────────────────────────────────── */
/*  GEOMETRIC — Architects                                               */
/*  Upright, hands at sides, perfect symmetry, structured                */
/* ────────────────────────────────────────────────────────────────────── */
const GeometricBody = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* ── Shoulder definition — square/structured ── */}
    <rect x="72" y="124" width="56" height="8" rx="3" fill={CLOTH_SEC} opacity="0.6" />
    <rect x="74" y="124" width="52" height="7" rx="2" fill={torsoFill(uid)} />

    {/* ── Main torso — rectangular, perfectly upright ── */}
    <path
      d="M78 124 L76 160 L76 210 Q88 218 100 220 Q112 218 124 210 L124 160 L122 124 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Structured collar — geometric V-neck ── */}
    <path
      d="M86 124 L100 136 L114 124"
      fill={color} opacity="0.12"
    />
    <path
      d="M86 124 L100 136 L114 124"
      stroke={color} strokeWidth="1.5" fill="none" opacity="0.65"
    />

    {/* ── Vertical center seam ── */}
    <line x1="100" y1="136" x2="100" y2="216" stroke={color} strokeWidth="0.5" opacity="0.15" />

    {/* ── Button details along center ── */}
    <circle cx="100" cy="150" r="1.2" fill={color} opacity="0.2" />
    <circle cx="100" cy="166" r="1.2" fill={color} opacity="0.2" />
    <circle cx="100" cy="182" r="1.2" fill={color} opacity="0.2" />

    {/* ── Torso fold lines — minimal, precise ── */}
    <path d="M82 154 L90 156" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.3" />
    <path d="M110 156 L118 154" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.3" />
    <path d="M80 190 L92 192" stroke={CLOTH_SEC} strokeWidth="0.5" fill="none" opacity="0.25" />
    <path d="M108 192 L120 190" stroke={CLOTH_SEC} strokeWidth="0.5" fill="none" opacity="0.25" />

    {/* ── LEFT ARM — straight down at side ── */}
    <path
      d="M76 130 Q72 146 68 164 L64 180 Q62 184 66 186 L70 178 Q74 160 78 138 Z"
      fill={SKIN}
    />
    <path
      d="M72 158 Q70 168 66 180 L64 180 Q68 168 70 156 Z"
      fill={SKIN_SHADOW} opacity="0.45"
    />
    {/* Left hand — 3-finger, at side */}
    <path
      d="M64 180 Q62 184 60 188 L62 189 L64 185
         Q62 188 62 192 L64 192 L65 186
         Q64 190 64 194 L66 193 L66 186
         L68 184 Z"
      fill={SKIN}
    />
    <path d="M64 182 L66 184" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />

    {/* ── RIGHT ARM — mirror of left ── */}
    <path
      d="M124 130 Q128 146 132 164 L136 180 Q138 184 134 186 L130 178 Q126 160 122 138 Z"
      fill={SKIN}
    />
    <path
      d="M128 158 Q130 168 134 180 L136 180 Q132 168 130 156 Z"
      fill={SKIN_SHADOW} opacity="0.45"
    />
    {/* Right hand — 3-finger, at side */}
    <path
      d="M136 180 Q138 184 140 188 L138 189 L136 185
         Q138 188 138 192 L136 192 L135 186
         Q136 190 136 194 L134 193 L134 186
         L132 184 Z"
      fill={SKIN}
    />
    <path d="M136 182 L134 184" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />

    {/* ── LEFT LEG — straight, structured ── */}
    <path
      d="M88 218 L86 240 L86 258 L84 264
         L80 268 L94 268 L92 264 L90 258
         L90 240 L92 218 Z"
      fill={CLOTH_MAIN}
    />
    <line x1="90" y1="220" x2="89" y2="260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.35" />

    {/* ── RIGHT LEG — mirror ── */}
    <path
      d="M108 218 L110 240 L110 258 L112 264
         L116 268 L102 268 L104 264 L106 258
         L106 240 L104 218 Z"
      fill={CLOTH_MAIN}
    />
    <line x1="106" y1="220" x2="107" y2="260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.35" />

    {/* ── LEFT SHOE — structured, angular ── */}
    <path
      d="M80 266 Q76 268 74 270 Q74 274 78 276 L94 276 Q96 274 96 272 Q96 268 94 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="76" y1="274" x2="94" y2="274" stroke="#444" strokeWidth="0.8" opacity="0.5" />
    <line x1="84" y1="267" x2="84" y2="270" stroke="#555" strokeWidth="0.5" opacity="0.3" />
    <circle cx="84" cy="269" r="0.7" fill="#555" opacity="0.35" />

    {/* ── RIGHT SHOE — mirror ── */}
    <path
      d="M102 266 Q100 268 100 270 Q100 274 104 276 L120 276 Q124 274 124 270 Q122 268 116 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="104" y1="274" x2="122" y2="274" stroke="#444" strokeWidth="0.8" opacity="0.5" />
    <line x1="112" y1="267" x2="112" y2="270" stroke="#555" strokeWidth="0.5" opacity="0.3" />
    <circle cx="112" cy="269" r="0.7" fill="#555" opacity="0.35" />
  </g>
);

/* ────────────────────────────────────────────────────────────────────── */
/*  FLUID — Explorers                                                    */
/*  Relaxed, one hand up in gesture, casual asymmetric                   */
/* ────────────────────────────────────────────────────────────────────── */
const FluidBody = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* ── Shoulder definition — soft, slightly asymmetric ── */}
    <ellipse cx="98" cy="128" rx="27" ry="6" fill={CLOTH_SEC} opacity="0.5" />
    <ellipse cx="98" cy="128" rx="25" ry="5" fill={torsoFill(uid)} />

    {/* ── Main torso — relaxed curve, slight leftward lean ── */}
    <path
      d="M80 124 Q76 128 74 150 L72 180 L72 210
         Q86 220 100 222 Q114 220 128 210
         L127 180 L126 150 Q122 128 118 124 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Collar — casual scoop neckline ── */}
    <path
      d="M84 124 Q92 133 100 134 Q108 133 116 124"
      stroke={color} strokeWidth="1.8" fill="none" opacity="0.55"
    />
    <path
      d="M86 124 Q93 132 100 133 Q107 132 114 124 L114 126 Q107 134 100 135 Q93 134 86 126 Z"
      fill={color} opacity="0.1"
    />

    {/* ── Torso fold lines — flowing, organic ── */}
    <path d="M82 150 Q92 156 106 150" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.35" />
    <path d="M78 174 Q90 180 110 172" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.3" />
    <path d="M80 198 Q96 204 114 196" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.25" />
    {/* Diagonal crease */}
    <path d="M84 140 Q90 148 98 152" stroke={CLOTH_SEC} strokeWidth="0.5" fill="none" opacity="0.2" />

    {/* ── LEFT ARM — relaxed, hanging loose ── */}
    <path
      d="M74 130 Q66 150 58 174 L54 188 Q52 192 56 194 L60 186 Q66 162 76 138 Z"
      fill={SKIN}
    />
    <path
      d="M66 160 Q62 174 58 188 L56 186 Q60 172 64 158 Z"
      fill={SKIN_SHADOW} opacity="0.4"
    />
    {/* Left hand — relaxed, fingers loosely curled */}
    <path
      d="M54 188 Q50 192 48 196 L50 197 L53 193
         Q52 196 50 200 L52 200 L54 195
         Q52 198 52 202 L54 201 L55 194
         L58 192 Z"
      fill={SKIN}
    />

    {/* ── RIGHT ARM — raised up, gesturing ── */}
    {/* Upper arm */}
    <path
      d="M124 130 Q132 134 140 140 L150 148 Q154 144 150 142 L142 136 Q134 130 126 128 Z"
      fill={SKIN}
    />
    {/* Forearm angled upward */}
    <path
      d="M140 140 Q146 134 150 126 L154 118 Q156 116 152 116 L148 122 Q144 130 138 138 Z"
      fill={SKIN}
    />
    <path
      d="M142 136 Q148 128 152 118 L150 118 Q146 128 140 136 Z"
      fill={SKIN_SHADOW} opacity="0.35"
    />
    {/* Right hand — open, welcoming gesture */}
    <path
      d="M152 118 Q154 112 152 108 L150 108 L151 114
         Q154 110 156 106 L154 106 L152 112
         Q156 108 158 104 L156 104 L153 110
         L152 116 Z"
      fill={SKIN}
    />
    {/* Finger separation lines */}
    <path d="M151 112 L152 110" stroke={SKIN_SHADOW} strokeWidth="0.4" fill="none" opacity="0.5" />

    {/* ── LEFT LEG — slightly wider stance ── */}
    <path
      d="M84 220 Q80 240 76 256 L74 264
         L70 268 L86 268 L84 264 L82 256
         Q84 238 88 220 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M86 222 Q83 242 80 260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.3" />

    {/* ── RIGHT LEG — casual ── */}
    <path
      d="M112 220 Q116 240 120 256 L122 264
         L126 268 L110 268 L112 264 L114 256
         Q112 238 108 220 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M110 222 Q113 242 116 260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.3" />

    {/* ── LEFT SHOE — casual/sneaker style ── */}
    <path
      d="M70 266 Q66 268 64 270 Q64 275 68 276 L86 276 Q88 274 88 271 Q88 268 86 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="66" y1="274" x2="86" y2="274" stroke="#444" strokeWidth="0.7" opacity="0.4" />
    {/* Lace accent */}
    <path d="M74 267 L76 270 L78 267" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M76 268 L78 271 L80 268" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.35" />

    {/* ── RIGHT SHOE ── */}
    <path
      d="M110 266 Q108 268 108 270 Q108 275 112 276 L130 276 Q134 274 134 270 Q132 268 126 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="112" y1="274" x2="132" y2="274" stroke="#444" strokeWidth="0.7" opacity="0.4" />
    <path d="M118 267 L120 270 L122 267" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M120 268 L122 271 L124 268" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.35" />
  </g>
);

/* ────────────────────────────────────────────────────────────────────── */
/*  ROUND — Anchors                                                      */
/*  Comfortable, arms slightly open/welcoming, warm                      */
/* ────────────────────────────────────────────────────────────────────── */
const RoundBody = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* ── Shoulder definition — soft, rounded ── */}
    <ellipse cx="100" cy="128" rx="30" ry="7" fill={CLOTH_SEC} opacity="0.5" />
    <ellipse cx="100" cy="128" rx="28" ry="6" fill={torsoFill(uid)} />

    {/* ── Main torso — wider, comfortable ── */}
    <path
      d="M78 124 Q74 130 72 155 L70 180 L70 210
         Q84 222 100 224 Q116 222 130 210
         L130 180 L128 155 Q126 130 122 124 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Collar — soft round neckline ── */}
    <path
      d="M86 124 Q93 132 100 133 Q107 132 114 124"
      stroke={color} strokeWidth="1.5" fill="none" opacity="0.5"
    />
    <path
      d="M88 124 Q94 131 100 132 Q106 131 112 124 L112 126 Q106 133 100 134 Q94 133 88 126 Z"
      fill={color} opacity="0.1"
    />

    {/* ── Torso fold lines — soft curves ── */}
    <path d="M82 152 Q96 158 118 152" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.3" />
    <path d="M78 178 Q98 186 122 178" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.25" />
    <path d="M76 200 Q98 208 124 200" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.2" />

    {/* ── LEFT ARM — open/welcoming, angled outward ── */}
    <path
      d="M72 132 Q62 148 56 168 L52 180 Q50 184 54 186 L58 176 Q64 156 74 138 Z"
      fill={SKIN}
    />
    <path
      d="M62 156 Q58 168 54 180 L52 180 Q56 166 60 154 Z"
      fill={SKIN_SHADOW} opacity="0.4"
    />
    {/* Left hand — open, welcoming */}
    <path
      d="M52 180 Q48 184 46 188 L48 189 L51 185
         Q48 188 48 192 L50 192 L52 186
         Q50 190 50 194 L52 193 L53 186
         L56 184 Z"
      fill={SKIN}
    />
    <path d="M50 184 L52 186" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />

    {/* ── RIGHT ARM — mirrored open/welcoming ── */}
    <path
      d="M128 132 Q138 148 144 168 L148 180 Q150 184 146 186 L142 176 Q136 156 126 138 Z"
      fill={SKIN}
    />
    <path
      d="M138 156 Q142 168 146 180 L148 180 Q144 166 140 154 Z"
      fill={SKIN_SHADOW} opacity="0.4"
    />
    {/* Right hand — open, welcoming */}
    <path
      d="M148 180 Q152 184 154 188 L152 189 L149 185
         Q152 188 152 192 L150 192 L148 186
         Q150 190 150 194 L148 193 L147 186
         L144 184 Z"
      fill={SKIN}
    />
    <path d="M150 184 L148 186" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />

    {/* ── LEFT LEG ── */}
    <path
      d="M88 222 Q84 240 82 256 L80 264
         L76 268 L92 268 L90 264 L88 256
         Q90 238 94 222 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M92 224 Q88 244 86 260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.3" />

    {/* ── RIGHT LEG ── */}
    <path
      d="M106 222 Q110 240 112 256 L114 264
         L118 268 L102 268 L104 264 L106 256
         Q104 238 102 222 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M104 224 Q108 244 110 260" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.3" />

    {/* ── LEFT SHOE — rounded, comfortable ── */}
    <path
      d="M76 266 Q72 268 70 271 Q70 275 74 277 L92 277 Q94 275 94 272 Q94 268 92 266 Z"
      fill={CLOTH_SEC}
    />
    <path
      d="M72 275 Q82 276 92 275"
      stroke="#444" strokeWidth="0.7" fill="none" opacity="0.45"
    />
    <circle cx="82" cy="268" r="0.7" fill="#555" opacity="0.3" />
    <circle cx="85" cy="268" r="0.7" fill="#555" opacity="0.3" />

    {/* ── RIGHT SHOE — rounded, comfortable ── */}
    <path
      d="M102 266 Q100 268 100 271 Q100 275 104 277 L122 277 Q126 275 126 271 Q124 268 118 266 Z"
      fill={CLOTH_SEC}
    />
    <path
      d="M102 275 Q112 276 122 275"
      stroke="#444" strokeWidth="0.7" fill="none" opacity="0.45"
    />
    <circle cx="110" cy="268" r="0.7" fill="#555" opacity="0.3" />
    <circle cx="113" cy="268" r="0.7" fill="#555" opacity="0.3" />
  </g>
);

/* ────────────────────────────────────────────────────────────────────── */
/*  ATHLETIC — Kineticists                                               */
/*  Wide shoulders, one arm flexed, power stance, motion lines           */
/* ────────────────────────────────────────────────────────────────────── */
const AthleticBody = ({ color, uid }: { color: string; uid?: string }) => (
  <g>
    {/* ── Shoulder definition — broad, powerful ── */}
    <path
      d="M66 126 Q80 120 100 122 Q120 120 134 126 Q136 130 134 132 Q120 128 100 128 Q80 128 66 132 Q64 130 66 126 Z"
      fill={CLOTH_SEC} opacity="0.7"
    />
    <path
      d="M68 127 Q82 122 100 123 Q118 122 132 127 Q134 130 132 131 Q118 128 100 128 Q82 128 68 131 Q66 130 68 127 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Main torso — V-taper, wide shoulders to narrow waist ── */}
    <path
      d="M74 124 Q68 128 66 150 L68 180 L70 210
         Q86 222 100 224 Q114 222 130 210
         L132 180 L134 150 Q132 128 126 124 Z"
      fill={torsoFill(uid)}
    />

    {/* ── Collar — athletic crew neck ── */}
    <path
      d="M86 124 L100 130 L114 124"
      stroke={color} strokeWidth="2.5" fill="none" opacity="0.7"
    />
    <path
      d="M88 124 L100 129 L112 124 L112 126 L100 131 L88 126 Z"
      fill={color} opacity="0.15"
    />

    {/* ── Chest muscle contour lines ── */}
    <path d="M82 136 Q90 142 98 138" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.4" />
    <path d="M102 138 Q110 142 118 136" stroke={CLOTH_SEC} strokeWidth="0.8" fill="none" opacity="0.4" />

    {/* ── Torso fold lines ── */}
    <path d="M78 162 Q88 166 100 164" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.3" />
    <path d="M100 164 Q112 166 122 162" stroke={CLOTH_SEC} strokeWidth="0.7" fill="none" opacity="0.3" />
    <path d="M76 190 Q92 196 108 190" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.25" />

    {/* ── LEFT ARM — hanging with fist ── */}
    <path
      d="M68 130 Q58 148 50 168 L46 180 Q44 184 48 186 L52 176 Q58 156 70 138 Z"
      fill={SKIN}
    />
    {/* Upper arm muscle contour */}
    <path
      d="M64 142 Q60 154 54 170 L50 170 Q56 152 60 140 Z"
      fill={SKIN_SHADOW} opacity="0.45"
    />
    {/* Left hand — fist shape */}
    <path
      d="M46 180 Q42 182 42 186 Q42 190 46 192 L52 192 Q56 190 56 186 Q56 182 52 180 Z"
      fill={SKIN}
    />
    <path d="M44 184 L54 184" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M44 187 L54 187" stroke={SKIN_SHADOW} strokeWidth="0.4" fill="none" opacity="0.35" />

    {/* ── RIGHT ARM — flexed bicep ── */}
    {/* Upper arm going out and up */}
    <path
      d="M130 130 Q140 134 148 144 L154 154 Q150 148 146 140 Q138 130 132 128 Z"
      fill={SKIN}
    />
    {/* Forearm curling up (flexing) */}
    <path
      d="M148 144 Q154 148 156 156 L156 154 Q156 146 152 140 Z"
      fill={SKIN}
    />
    <path
      d="M148 144 Q142 138 140 130 L136 124 Q134 122 136 120 L140 126 Q142 134 150 142 Z"
      fill={SKIN}
    />
    {/* Bicep bulge */}
    <path
      d="M146 138 Q150 134 148 128 L146 128 Q148 132 144 138 Z"
      fill={SKIN_SHADOW} opacity="0.5"
    />
    {/* Right fist — clenched at top of flex */}
    <path
      d="M136 120 Q132 118 132 122 Q132 126 136 128 L140 128 Q144 126 144 122 Q144 118 140 118 Z"
      fill={SKIN}
    />
    <path d="M134 121 L142 121" stroke={SKIN_SHADOW} strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M134 124 L142 124" stroke={SKIN_SHADOW} strokeWidth="0.4" fill="none" opacity="0.35" />

    {/* ── Motion lines — energy radiating from flex ── */}
    <line x1="152" y1="118" x2="160" y2="114" stroke={color} strokeWidth="1.2" opacity="0.4" />
    <line x1="154" y1="124" x2="164" y2="122" stroke={color} strokeWidth="1" opacity="0.3" />
    <line x1="154" y1="130" x2="162" y2="130" stroke={color} strokeWidth="0.8" opacity="0.25" />
    {/* Left side ambient motion */}
    <line x1="40" y1="170" x2="32" y2="166" stroke={color} strokeWidth="1" opacity="0.25" />
    <line x1="38" y1="178" x2="30" y2="176" stroke={color} strokeWidth="0.8" opacity="0.2" />

    {/* ── LEFT LEG — wide power stance ── */}
    <path
      d="M84 222 Q78 240 74 256 L72 264
         L68 268 L84 268 L82 264 L80 256
         Q82 238 86 222 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M84 224 Q80 244 76 260" stroke={CLOTH_SEC} strokeWidth="0.9" fill="none" opacity="0.35" />
    {/* Quad muscle hint */}
    <path d="M84 228 Q82 236 80 244" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.2" />

    {/* ── RIGHT LEG — wide power stance ── */}
    <path
      d="M114 222 Q120 240 124 256 L126 264
         L130 268 L114 268 L116 264 L118 256
         Q116 238 112 222 Z"
      fill={CLOTH_MAIN}
    />
    <path d="M114 224 Q118 244 122 260" stroke={CLOTH_SEC} strokeWidth="0.9" fill="none" opacity="0.35" />
    <path d="M114 228 Q116 236 118 244" stroke={CLOTH_SEC} strokeWidth="0.6" fill="none" opacity="0.2" />

    {/* ── LEFT SHOE — athletic/sneaker, boxy ── */}
    <path
      d="M68 266 Q64 268 62 271 Q62 275 66 277 L84 277 Q86 275 86 272 Q86 268 84 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="64" y1="275" x2="84" y2="275" stroke="#444" strokeWidth="0.8" opacity="0.5" />
    {/* Sole accent */}
    <path d="M64 275 Q74 277 84 275" stroke={color} strokeWidth="0.6" fill="none" opacity="0.3" />
    {/* Laces */}
    <path d="M72 267 L74 270 L76 267" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M74 268 L76 271 L78 268" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.35" />

    {/* ── RIGHT SHOE — athletic/sneaker, boxy ── */}
    <path
      d="M114 266 Q112 268 112 271 Q112 275 116 277 L134 277 Q138 275 138 271 Q136 268 130 266 Z"
      fill={CLOTH_SEC}
    />
    <line x1="116" y1="275" x2="136" y2="275" stroke="#444" strokeWidth="0.8" opacity="0.5" />
    <path d="M116 275 Q126 277 136 275" stroke={color} strokeWidth="0.6" fill="none" opacity="0.3" />
    <path d="M120 267 L122 270 L124 267" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.4" />
    <path d="M122 268 L124 271 L126 268" stroke="#555" strokeWidth="0.5" fill="none" opacity="0.35" />
  </g>
);

/* ── Dispatch map ─────────────────────────────────────────────────────── */

const BODY_MAP: Record<HeadShape, React.FC<{ color: string; uid?: string }>> = {
  angular: AngularBody,
  geometric: GeometricBody,
  fluid: FluidBody,
  round: RoundBody,
  athletic: AthleticBody,
};

export function BodyPart({ shape, color, uid }: BodyProps) {
  const Component = BODY_MAP[shape];
  return <Component color={color} uid={uid} />;
}
