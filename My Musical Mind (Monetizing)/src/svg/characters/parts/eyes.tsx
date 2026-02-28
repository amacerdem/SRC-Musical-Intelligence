/* ── Eye Styles — Detailed SVG Rendering ──────────────────────────────── */
import React from "react";
import type { EyeStyle } from "../types";

const IRIS_DEFAULT = "#2d2d44";
const PUPIL = "#0a0a14";
const SKIN_SHADOW = "#D4B08C";

/* ── Helper: iris fill respects uid-based gradient when available ────── */
const irisFill = (uid?: string) =>
  uid ? `url(#iris-${uid})` : IRIS_DEFAULT;

/* ── Intense — Alchemists: narrow, piercing, lowered upper lids ─────── */
const IntenseEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* Under-eye shadows */}
    <ellipse cx="88" cy="79" rx="7" ry="2.5" fill={SKIN_SHADOW} opacity="0.25" />
    <ellipse cx="112" cy="79" rx="7" ry="2.5" fill={SKIN_SHADOW} opacity="0.25" />

    {/* ── Left eye ── */}
    {/* Eye white — narrow slit */}
    <ellipse cx="88" cy="75" rx="7.5" ry="3.8" fill="white" />
    {/* Iris */}
    <ellipse cx="89" cy="75" rx="3.8" ry="3.6" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="89" cy="75" r="2.4" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.5" />
    {/* Pupil */}
    <circle cx="89" cy="75" r="1.6" fill={PUPIL} />
    {/* Color accent on iris */}
    {color && <circle cx="89" cy="75" r="2.8" fill={color} opacity="0.25" />}
    {/* Primary catch light (top-right) */}
    <ellipse cx="90.5" cy="73.5" rx="1.2" ry="0.9" fill="white" opacity="0.95" />
    {/* Secondary catch light (bottom-left) */}
    <circle cx="87.5" cy="76.5" r="0.5" fill="white" opacity="0.6" />
    {/* Upper eyelid — lowered, narrowing the eye */}
    <path d="M80.5 75 Q84 70 88 70.5 Q92 71 95.5 75" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1.1" />
    <path d="M80.5 75 Q84 71.5 88 72 Q92 72.5 95.5 75" fill="#F0D5B8" opacity="0.6" />
    {/* Lower eyelid hint */}
    <path d="M81 76.5 Q88 80 95 76.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />
    {/* Eyelashes — 3 along upper lid */}
    <line x1="83" y1="71.5" x2="82" y2="69.5" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />
    <line x1="87" y1="70.5" x2="86.5" y2="68.5" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />
    <line x1="91" y1="71" x2="91.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />

    {/* ── Right eye ── */}
    <ellipse cx="112" cy="75" rx="7.5" ry="3.8" fill="white" />
    <ellipse cx="111" cy="75" rx="3.8" ry="3.6" fill={irisFill(uid)} />
    <circle cx="111" cy="75" r="2.4" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.5" />
    <circle cx="111" cy="75" r="1.6" fill={PUPIL} />
    {color && <circle cx="111" cy="75" r="2.8" fill={color} opacity="0.25" />}
    <ellipse cx="112.5" cy="73.5" rx="1.2" ry="0.9" fill="white" opacity="0.95" />
    <circle cx="109.5" cy="76.5" r="0.5" fill="white" opacity="0.6" />
    <path d="M104.5 75 Q108 70 112 70.5 Q116 71 119.5 75" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1.1" />
    <path d="M104.5 75 Q108 71.5 112 72 Q116 72.5 119.5 75" fill="#F0D5B8" opacity="0.6" />
    <path d="M105 76.5 Q112 80 119 76.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />
    <line x1="107" y1="71.5" x2="106" y2="69.5" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />
    <line x1="111" y1="70.5" x2="110.5" y2="68.5" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />
    <line x1="115" y1="71" x2="115.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.7" strokeLinecap="round" />

    {/* Furrowed brows — thick, angled inward */}
    <path d="M79 67 Q84 63 89 64 Q93 64.5 96 66.5"
      stroke={IRIS_DEFAULT} strokeWidth="2.2" fill="none" strokeLinecap="round" />
    <path d="M104 66.5 Q107 64.5 111 64 Q116 63 121 67"
      stroke={IRIS_DEFAULT} strokeWidth="2.2" fill="none" strokeLinecap="round" />
  </g>
);

/* ── Wide — Explorers: large open circles, high brows, innocent ─────── */
const WideEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* ── Left eye ── */}
    {/* Eye white — large circle */}
    <ellipse cx="88" cy="76" rx="8.5" ry="7.5" fill="white" />
    {/* Iris */}
    <circle cx="88" cy="76" r="4.5" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="88" cy="76" r="3" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />
    {/* Iris radial detail */}
    <circle cx="88" cy="76" r="4.5" fill="none" stroke="white" strokeWidth="0.2" opacity="0.15" />
    {/* Pupil */}
    <circle cx="88" cy="76" r="2" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="88" cy="76" r="3.5" fill={color} opacity="0.18" />}
    {/* Primary catch light */}
    <ellipse cx="90" cy="73.5" rx="1.8" ry="1.4" fill="white" opacity="0.95" />
    {/* Secondary catch light */}
    <circle cx="86" cy="78.5" r="0.7" fill="white" opacity="0.55" />
    {/* Upper eyelid — thin, high arc (wide open) */}
    <path d="M79.5 76 Q84 68 88 67.5 Q92 68 96.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.8" />
    {/* Lower eyelid hint */}
    <path d="M80 78 Q88 84 96 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* ── Right eye ── */}
    <ellipse cx="112" cy="76" rx="8.5" ry="7.5" fill="white" />
    <circle cx="112" cy="76" r="4.5" fill={irisFill(uid)} />
    <circle cx="112" cy="76" r="3" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />
    <circle cx="112" cy="76" r="4.5" fill="none" stroke="white" strokeWidth="0.2" opacity="0.15" />
    <circle cx="112" cy="76" r="2" fill={PUPIL} />
    {color && <circle cx="112" cy="76" r="3.5" fill={color} opacity="0.18" />}
    <ellipse cx="114" cy="73.5" rx="1.8" ry="1.4" fill="white" opacity="0.95" />
    <circle cx="110" cy="78.5" r="0.7" fill="white" opacity="0.55" />
    <path d="M103.5 76 Q108 68 112 67.5 Q116 68 120.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.8" />
    <path d="M104 78 Q112 84 120 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* High raised brows — thin, surprised arch */}
    <path d="M79 64 Q84 59 88 59 Q92 59 97 64"
      stroke={IRIS_DEFAULT} strokeWidth="1.3" fill="none" strokeLinecap="round" />
    <path d="M103 64 Q108 59 112 59 Q116 59 121 64"
      stroke={IRIS_DEFAULT} strokeWidth="1.3" fill="none" strokeLinecap="round" />
  </g>
);

/* ── Calm — Architects: relaxed oval, hooded upper lid, level brows ── */
const CalmEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* ── Left eye ── */}
    {/* Eye white — horizontal oval */}
    <ellipse cx="88" cy="76" rx="7.5" ry="5" fill="white" />
    {/* Iris */}
    <ellipse cx="88" cy="76" rx="3.4" ry="3.4" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="88" cy="76" r="2.2" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.45" />
    {/* Pupil */}
    <circle cx="88" cy="76" r="1.4" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="88" cy="76" r="2.6" fill={color} opacity="0.15" />}
    {/* Primary catch light */}
    <ellipse cx="89.5" cy="74.5" rx="1.1" ry="0.8" fill="white" opacity="0.9" />
    {/* Secondary catch light */}
    <circle cx="87" cy="77.5" r="0.45" fill="white" opacity="0.5" />
    {/* Hooded upper eyelid — heavy, relaxed droop */}
    <path d="M80.5 76 Q84 72 88 71.5 Q92 72 95.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    <path d="M80.5 76 Q84 73 88 73 Q92 73 95.5 76" fill="#F0D5B8" opacity="0.55" />
    {/* Lower eyelid hint */}
    <path d="M81 77.5 Q88 81 95 77.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* ── Right eye ── */}
    <ellipse cx="112" cy="76" rx="7.5" ry="5" fill="white" />
    <ellipse cx="112" cy="76" rx="3.4" ry="3.4" fill={irisFill(uid)} />
    <circle cx="112" cy="76" r="2.2" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.45" />
    <circle cx="112" cy="76" r="1.4" fill={PUPIL} />
    {color && <circle cx="112" cy="76" r="2.6" fill={color} opacity="0.15" />}
    <ellipse cx="113.5" cy="74.5" rx="1.1" ry="0.8" fill="white" opacity="0.9" />
    <circle cx="111" cy="77.5" r="0.45" fill="white" opacity="0.5" />
    <path d="M104.5 76 Q108 72 112 71.5 Q116 72 119.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    <path d="M104.5 76 Q108 73 112 73 Q116 73 119.5 76" fill="#F0D5B8" opacity="0.55" />
    <path d="M105 77.5 Q112 81 119 77.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* Level straight brows — even thickness */}
    <line x1="80" y1="68" x2="96" y2="68"
      stroke={IRIS_DEFAULT} strokeWidth="1.6" strokeLinecap="round" />
    <line x1="104" y1="68" x2="120" y2="68"
      stroke={IRIS_DEFAULT} strokeWidth="1.6" strokeLinecap="round" />
    {/* Brow thickness taper — subtle */}
    <line x1="80" y1="68" x2="84" y2="68"
      stroke={IRIS_DEFAULT} strokeWidth="2" strokeLinecap="round" opacity="0.3" />
    <line x1="116" y1="68" x2="120" y2="68"
      stroke={IRIS_DEFAULT} strokeWidth="2" strokeLinecap="round" opacity="0.3" />
  </g>
);

/* ── Warm — Anchors: soft, upturned corners (smiling eyes) ──────────── */
const WarmEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* Warm under-eye glow */}
    {color && <ellipse cx="88" cy="81" rx="6" ry="2.5" fill={color} opacity="0.08" />}
    {color && <ellipse cx="112" cy="81" rx="6" ry="2.5" fill={color} opacity="0.08" />}

    {/* ── Left eye ── */}
    {/* Eye white — soft oval, slightly upturned at outer corner */}
    <path d="M80.5 76 Q84 70 88 70 Q92 70 95.5 74 Q93 80 88 81 Q83 80 80.5 76 Z" fill="white" />
    {/* Iris */}
    <ellipse cx="88" cy="75.5" rx="3.8" ry="3.8" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="88" cy="75.5" r="2.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.4" />
    {/* Pupil */}
    <circle cx="88" cy="75.5" r="1.5" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="88" cy="75.5" r="3" fill={color} opacity="0.2" />}
    {/* Primary catch light */}
    <ellipse cx="89.8" cy="73.8" rx="1.3" ry="1" fill="white" opacity="0.9" />
    {/* Secondary catch light */}
    <circle cx="86.5" cy="77.5" r="0.5" fill="white" opacity="0.55" />
    {/* Upper eyelid — gentle curve */}
    <path d="M80.5 76 Q84 70 88 70 Q92 70 95.5 74" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    {/* Lower eyelid — smiling upturn */}
    <path d="M81 77 Q85 80 88 80.5 Q91 80 95 77" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.35" />
    {/* Eyelashes — delicate, warm expression */}
    <line x1="84" y1="71" x2="83" y2="69.5" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    <line x1="87.5" y1="70" x2="87" y2="68.5" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    <line x1="91" y1="70.5" x2="91.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    {/* Smile crease at outer corner */}
    <path d="M95 75 Q96.5 77 96 79" fill="none" stroke={SKIN_SHADOW} strokeWidth="0.5" opacity="0.3" />

    {/* ── Right eye ── */}
    <path d="M104.5 74 Q108 70 112 70 Q116 70 119.5 76 Q117 80 112 81 Q107 80 104.5 74 Z" fill="white" />
    <ellipse cx="112" cy="75.5" rx="3.8" ry="3.8" fill={irisFill(uid)} />
    <circle cx="112" cy="75.5" r="2.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.4" />
    <circle cx="112" cy="75.5" r="1.5" fill={PUPIL} />
    {color && <circle cx="112" cy="75.5" r="3" fill={color} opacity="0.2" />}
    <ellipse cx="113.8" cy="73.8" rx="1.3" ry="1" fill="white" opacity="0.9" />
    <circle cx="110.5" cy="77.5" r="0.5" fill="white" opacity="0.55" />
    <path d="M104.5 74 Q108 70 112 70 Q116 70 119.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    <path d="M105 77 Q109 80 112 80.5 Q115 80 119 77" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.35" />
    <line x1="108" y1="71" x2="107" y2="69.5" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    <line x1="111.5" y1="70" x2="111" y2="68.5" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    <line x1="115" y1="70.5" x2="115.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.5" strokeLinecap="round" />
    <path d="M104 75 Q102.5 77 103 79" fill="none" stroke={SKIN_SHADOW} strokeWidth="0.5" opacity="0.3" />

    {/* Gentle arched brows — soft curve */}
    <path d="M79 68 Q84 63.5 88 63.5 Q92 63.5 97 68"
      stroke={IRIS_DEFAULT} strokeWidth="1.4" fill="none" strokeLinecap="round" />
    <path d="M103 68 Q108 63.5 112 63.5 Q116 63.5 121 68"
      stroke={IRIS_DEFAULT} strokeWidth="1.4" fill="none" strokeLinecap="round" />
  </g>
);

/* ── Sharp — Kineticists: diamond/almond shape, angular, heavy brows ─ */
const SharpEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* Under-eye shadow */}
    <path d="M81 79 Q88 82 95 79" fill="none" stroke={SKIN_SHADOW} strokeWidth="1" opacity="0.2" />
    <path d="M105 79 Q112 82 119 79" fill="none" stroke={SKIN_SHADOW} strokeWidth="1" opacity="0.2" />

    {/* ── Left eye ── */}
    {/* Eye white — sharp almond/diamond */}
    <path d="M80 76 Q84 70.5 88 70 Q92 70.5 96 76 Q92 80.5 88 81 Q84 80.5 80 76 Z" fill="white" />
    {/* Iris */}
    <ellipse cx="88" cy="76" rx="3.6" ry="3.6" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="88" cy="76" r="2.3" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.5" />
    {/* Pupil — slightly vertical (predator) */}
    <ellipse cx="88" cy="76" rx="1.3" ry="1.7" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="88" cy="76" r="2.8" fill={color} opacity="0.22" />}
    {/* Primary catch light */}
    <ellipse cx="89.5" cy="74" rx="1.1" ry="0.8" fill="white" opacity="0.9" />
    {/* Secondary catch light */}
    <circle cx="87" cy="78" r="0.4" fill="white" opacity="0.5" />
    {/* Upper eyelid — angular, sharp */}
    <path d="M80 76 Q84 70.5 88 70 Q92 70.5 96 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1.2" />
    {/* Lower eyelid — subtle angular */}
    <path d="M81 77 Q88 80 95 77" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />

    {/* ── Right eye ── */}
    <path d="M104 76 Q108 70.5 112 70 Q116 70.5 120 76 Q116 80.5 112 81 Q108 80.5 104 76 Z" fill="white" />
    <ellipse cx="112" cy="76" rx="3.6" ry="3.6" fill={irisFill(uid)} />
    <circle cx="112" cy="76" r="2.3" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.5" />
    <ellipse cx="112" cy="76" rx="1.3" ry="1.7" fill={PUPIL} />
    {color && <circle cx="112" cy="76" r="2.8" fill={color} opacity="0.22" />}
    <ellipse cx="113.5" cy="74" rx="1.1" ry="0.8" fill="white" opacity="0.9" />
    <circle cx="111" cy="78" r="0.4" fill="white" opacity="0.5" />
    <path d="M104 76 Q108 70.5 112 70 Q116 70.5 120 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1.2" />
    <path d="M105 77 Q112 80 119 77" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.4" />

    {/* Heavy determined brows — angled, thick inner ends */}
    <path d="M78 69 Q83 65 88 66 Q93 67 97 71"
      stroke={IRIS_DEFAULT} strokeWidth="2.5" fill="none" strokeLinecap="round" />
    <path d="M103 71 Q107 67 112 66 Q117 65 122 69"
      stroke={IRIS_DEFAULT} strokeWidth="2.5" fill="none" strokeLinecap="round" />
    {/* Brow inner emphasis */}
    <path d="M78 69 Q80 67 83 66" stroke={IRIS_DEFAULT} strokeWidth="3" fill="none" strokeLinecap="round" opacity="0.4" />
    <path d="M117 66 Q120 67 122 69" stroke={IRIS_DEFAULT} strokeWidth="3" fill="none" strokeLinecap="round" opacity="0.4" />
  </g>
);

/* ── Dreamy — half-closed, heavy upper lid, relaxed brows ───────────── */
const DreamyEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* Ambient dreamy glow */}
    {color && <ellipse cx="100" cy="78" rx="22" ry="8" fill={color} opacity="0.05" />}

    {/* ── Left eye ── */}
    {/* Eye white — narrow horizontal, half-closed */}
    <ellipse cx="88" cy="78" rx="7.5" ry="3.2" fill="white" />
    {/* Iris — mostly hidden by upper lid, bottom peeking */}
    <ellipse cx="88" cy="78" rx="3.5" ry="3" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="88" cy="78" r="2" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.3" opacity="0.4" />
    {/* Pupil */}
    <circle cx="88" cy="78" r="1.3" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="88" cy="78" r="2.5" fill={color} opacity="0.2" />}
    {/* Primary catch light — soft */}
    <ellipse cx="89.5" cy="77" rx="1" ry="0.6" fill="white" opacity="0.8" />
    {/* Secondary catch light */}
    <circle cx="87" cy="79" r="0.35" fill="white" opacity="0.45" />
    {/* Heavy upper eyelid — drooping, covers upper iris */}
    <path d="M80.5 78 Q84 72 88 71.5 Q92 72 95.5 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    <path d="M80.5 78 Q84 74 88 73.5 Q92 74 95.5 78" fill="#F0D5B8" opacity="0.7" />
    {/* Extra lid weight line */}
    <path d="M82 75 Q88 73.5 94 75" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.35" opacity="0.3" />
    {/* Lower eyelid hint */}
    <path d="M81 79 Q88 81.5 95 79" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.25" />
    {/* Eyelashes — soft, dreamy wisps */}
    <line x1="83.5" y1="73.5" x2="82.5" y2="71.5" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="87" y1="72" x2="86.5" y2="70" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="90.5" y1="72.5" x2="91" y2="70.5" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="93.5" y1="74" x2="94.5" y2="72" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />

    {/* ── Right eye ── */}
    <ellipse cx="112" cy="78" rx="7.5" ry="3.2" fill="white" />
    <ellipse cx="112" cy="78" rx="3.5" ry="3" fill={irisFill(uid)} />
    <circle cx="112" cy="78" r="2" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.3" opacity="0.4" />
    <circle cx="112" cy="78" r="1.3" fill={PUPIL} />
    {color && <circle cx="112" cy="78" r="2.5" fill={color} opacity="0.2" />}
    <ellipse cx="113.5" cy="77" rx="1" ry="0.6" fill="white" opacity="0.8" />
    <circle cx="111" cy="79" r="0.35" fill="white" opacity="0.45" />
    <path d="M104.5 78 Q108 72 112 71.5 Q116 72 119.5 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.9" />
    <path d="M104.5 78 Q108 74 112 73.5 Q116 74 119.5 78" fill="#F0D5B8" opacity="0.7" />
    <path d="M106 75 Q112 73.5 118 75" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.35" opacity="0.3" />
    <path d="M105 79 Q112 81.5 119 79" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.25" />
    <line x1="107.5" y1="73.5" x2="106.5" y2="71.5" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="111" y1="72" x2="110.5" y2="70" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="114.5" y1="72.5" x2="115" y2="70.5" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />
    <line x1="117.5" y1="74" x2="118.5" y2="72" stroke={IRIS_DEFAULT} strokeWidth="0.45" strokeLinecap="round" />

    {/* Relaxed brows — barely arched, soft */}
    <path d="M80 71 Q84 69 88 69 Q92 69 96 71"
      stroke={IRIS_DEFAULT} strokeWidth="1.1" fill="none" strokeLinecap="round" />
    <path d="M104 71 Q108 69 112 69 Q116 69 120 71"
      stroke={IRIS_DEFAULT} strokeWidth="1.1" fill="none" strokeLinecap="round" />
  </g>
);

/* ── Determined — slightly narrowed, focused forward, flat brows ───── */
const DeterminedEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* Under-eye shadow — mature focus */}
    <ellipse cx="88" cy="80" rx="6" ry="1.8" fill={SKIN_SHADOW} opacity="0.18" />
    <ellipse cx="112" cy="80" rx="6" ry="1.8" fill={SKIN_SHADOW} opacity="0.18" />

    {/* ── Left eye ── */}
    {/* Eye white — slightly narrowed oval */}
    <ellipse cx="88" cy="76" rx="7.5" ry="4.5" fill="white" />
    {/* Iris */}
    <ellipse cx="89" cy="76" rx="3.8" ry="3.8" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="89" cy="76" r="2.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.45" opacity="0.5" />
    {/* Pupil — focused, slightly larger */}
    <circle cx="89" cy="76" r="1.7" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="89" cy="76" r="2.8" fill={color} opacity="0.18" />}
    {/* Primary catch light */}
    <ellipse cx="90.5" cy="74.5" rx="1.2" ry="0.85" fill="white" opacity="0.9" />
    {/* Secondary catch light */}
    <circle cx="87.5" cy="77.5" r="0.45" fill="white" opacity="0.5" />
    {/* Upper eyelid — slightly lowered, focused */}
    <path d="M80.5 76 Q84 71.5 88 71 Q92 71.5 95.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1" />
    <path d="M80.5 76 Q84 72.5 88 72.5 Q92 72.5 95.5 76" fill="#F0D5B8" opacity="0.45" />
    {/* Lower eyelid */}
    <path d="M81 78 Q88 81 95 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.45" opacity="0.3" />

    {/* ── Right eye ── */}
    <ellipse cx="112" cy="76" rx="7.5" ry="4.5" fill="white" />
    <ellipse cx="111" cy="76" rx="3.8" ry="3.8" fill={irisFill(uid)} />
    <circle cx="111" cy="76" r="2.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.45" opacity="0.5" />
    <circle cx="111" cy="76" r="1.7" fill={PUPIL} />
    {color && <circle cx="111" cy="76" r="2.8" fill={color} opacity="0.18" />}
    <ellipse cx="112.5" cy="74.5" rx="1.2" ry="0.85" fill="white" opacity="0.9" />
    <circle cx="109.5" cy="77.5" r="0.45" fill="white" opacity="0.5" />
    <path d="M104.5 76 Q108 71.5 112 71 Q116 71.5 119.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="1" />
    <path d="M104.5 76 Q108 72.5 112 72.5 Q116 72.5 119.5 76" fill="#F0D5B8" opacity="0.45" />
    <path d="M105 78 Q112 81 119 78" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.45" opacity="0.3" />

    {/* Flat straight brows — determined, no arch, slight inner tension */}
    <path d="M79 66.5 Q83 65.5 88 66 Q93 66.5 97 67"
      stroke={IRIS_DEFAULT} strokeWidth="2" fill="none" strokeLinecap="round" />
    <path d="M103 67 Q107 66.5 112 66 Q117 65.5 121 66.5"
      stroke={IRIS_DEFAULT} strokeWidth="2" fill="none" strokeLinecap="round" />
    {/* Brow furrow crease between brows */}
    <line x1="99" y1="65" x2="99.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.25" strokeLinecap="round" />
    <line x1="101" y1="65" x2="100.5" y2="69" stroke={IRIS_DEFAULT} strokeWidth="0.5" opacity="0.25" strokeLinecap="round" />
  </g>
);

/* ── Curious — different sizes, one brow higher, sparkle dots ────────── */
const CuriousEyes = ({ color, uid }: { color?: string; uid?: string }) => (
  <g>
    {/* ── Left eye (slightly bigger) ── */}
    {/* Eye white — larger */}
    <ellipse cx="87" cy="76" rx="8.5" ry="7" fill="white" />
    {/* Iris */}
    <circle cx="87" cy="76" r="4.2" fill={irisFill(uid)} />
    {/* Iris inner ring */}
    <circle cx="87" cy="76" r="2.8" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.45" />
    {/* Iris radial streaks (curiosity detail) */}
    <circle cx="87" cy="76" r="3.5" fill="none" stroke="white" strokeWidth="0.15" opacity="0.2"
      strokeDasharray="0.8 1.5" />
    {/* Pupil */}
    <circle cx="87" cy="76" r="1.8" fill={PUPIL} />
    {/* Color accent */}
    {color && <circle cx="87" cy="76" r="3.2" fill={color} opacity="0.18" />}
    {/* Primary catch light */}
    <ellipse cx="89" cy="73.8" rx="1.6" ry="1.2" fill="white" opacity="0.95" />
    {/* Secondary catch light */}
    <circle cx="85.5" cy="78" r="0.6" fill="white" opacity="0.55" />
    {/* Sparkle dots — curiosity twinkle */}
    <circle cx="90.5" cy="73" r="0.4" fill="white" opacity="0.8" />
    <circle cx="84" cy="74" r="0.3" fill="white" opacity="0.6" />
    {/* Upper eyelid — open, slight upturn */}
    <path d="M78.5 76 Q83 69 87 68.5 Q91 69 95.5 76" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.8" />
    {/* Lower eyelid hint */}
    <path d="M79 78.5 Q87 83 95 78.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* ── Right eye (slightly smaller, higher) ── */}
    <ellipse cx="113" cy="74.5" rx="7.5" ry="6" fill="white" />
    <circle cx="113" cy="74.5" r="3.8" fill={irisFill(uid)} />
    <circle cx="113" cy="74.5" r="2.4" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.45" />
    <circle cx="113" cy="74.5" r="3.2" fill="none" stroke="white" strokeWidth="0.15" opacity="0.2"
      strokeDasharray="0.8 1.5" />
    <circle cx="113" cy="74.5" r="1.6" fill={PUPIL} />
    {color && <circle cx="113" cy="74.5" r="2.8" fill={color} opacity="0.18" />}
    <ellipse cx="115" cy="72.5" rx="1.4" ry="1" fill="white" opacity="0.95" />
    <circle cx="111.5" cy="76.5" r="0.5" fill="white" opacity="0.55" />
    {/* Sparkle dots */}
    <circle cx="116" cy="71.5" r="0.35" fill="white" opacity="0.75" />
    <circle cx="110" cy="72.5" r="0.25" fill="white" opacity="0.55" />
    <path d="M105.5 74.5 Q109 68 113 67.5 Q117 68 120.5 74.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.8" />
    <path d="M106 76.5 Q113 81 120 76.5" fill="none" stroke={IRIS_DEFAULT} strokeWidth="0.4" opacity="0.3" />

    {/* Asymmetric brows — left lower, right raised higher (curious tilt) */}
    <path d="M78 66 Q83 63 87 63 Q91 63 96 66"
      stroke={IRIS_DEFAULT} strokeWidth="1.5" fill="none" strokeLinecap="round" />
    <path d="M104 63 Q109 59 113 58.5 Q117 59 122 63"
      stroke={IRIS_DEFAULT} strokeWidth="1.5" fill="none" strokeLinecap="round" />
  </g>
);

/* ── Style → Component Map ──────────────────────────────────────────── */
const EYE_MAP: Record<EyeStyle, React.FC<{ color?: string; uid?: string }>> = {
  intense: IntenseEyes,
  wide: WideEyes,
  calm: CalmEyes,
  warm: WarmEyes,
  sharp: SharpEyes,
  dreamy: DreamyEyes,
  determined: DeterminedEyes,
  curious: CuriousEyes,
};

export function EyesPart({ style, color, uid }: { style: EyeStyle; color: string; uid?: string }) {
  const Component = EYE_MAP[style];
  return <Component color={color} uid={uid} />;
}
