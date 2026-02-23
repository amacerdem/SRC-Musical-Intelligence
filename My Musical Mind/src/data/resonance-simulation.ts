/* ── Resonance Field — Bipolar Psychological State Engine ────────── */
/*
 * 5 bipolar dimensions, each [-5, +5]:
 *   0  Serene ←→ Intense     (arousal / activation energy)
 *   1  Dark ←→ Luminous      (emotional valence)
 *   2  Diffuse ←→ Focused    (attentional state)
 *   3  Ancient ←→ Novel       (temporal orientation — nostalgia vs novelty)
 *   4  Isolated ←→ Merged     (social boundary dissolution)
 *
 * Continuous evolution at 60 fps via layered sine/noise oscillators.
 * Resonance = 1 − (euclidean distance / max distance).
 */

import { mockUsers } from "./mock-users";
import { personas } from "./personas";

/* ── Dimension Metadata ─────────────────────────────────────────── */

export const DIMENSIONS = [
  { id: "arousal",   negLabel: "Serene",   posLabel: "Intense",  negColor: "#6366F1", posColor: "#EF4444" },
  { id: "valence",   negLabel: "Dark",     posLabel: "Luminous", negColor: "#7C3AED", posColor: "#FBBF24" },
  { id: "focus",     negLabel: "Diffuse",  posLabel: "Focused",  negColor: "#06B6D4", posColor: "#84CC16" },
  { id: "temporal",  negLabel: "Ancient",  posLabel: "Novel",    negColor: "#F97316", posColor: "#EC4899" },
  { id: "social",    negLabel: "Isolated", posLabel: "Merged",   negColor: "#475569", posColor: "#38BDF8" },
] as const;

export type Psi5 = [number, number, number, number, number]; // each [-5, +5]

/* ── Types ──────────────────────────────────────────────────────── */

export interface ResonanceUser {
  id: string;
  displayName: string;
  avatarUrl: string;
  country: string;
  personaId: number;
  psi: Psi5;                   // current state [-5,+5]
  position: [number, number, number];
  velocity: [number, number, number];
  intensity: number;           // absolute magnitude of psi vector
  pulseRate: number;           // derived from arousal
  bio: string;
  currentTrack?: string;
  /** Internal oscillator phases (5 per user, continuous) */
  _phases: [number, number, number, number, number];
  /** Internal oscillator speeds */
  _speeds: [number, number, number, number, number];
  /** Base personality center (what they orbit around) */
  _center: Psi5;
  /** Amplitude of oscillation per dimension */
  _amplitude: [number, number, number, number, number];
}

export interface Connection {
  id: string;
  userA: string;
  userB: string;
  strength: number;       // 0–1 resonance
  dominantDim: number;    // which dimension resonates most
}

export interface ResonanceSignal {
  id: string;
  from: string;
  to: string;
  type: "wave" | "chills" | "vibe" | "fire" | "mind" | "feel" | "sync" | "peak";
  content: string;
  ts: number;
  received: boolean;
}

/* ── Constants ──────────────────────────────────────────────────── */

const MAX_DIST = Math.sqrt(5 * 10 * 10); // max euclidean dist in 5D [-5,+5]

const EXTRA_USERS: { name: string; country: string; bio: string }[] = [
  { name: "Anika S.", country: "IN", bio: "Mumbai — melody is consciousness unfolding in real time." },
  { name: "Tomas R.", country: "CZ", bio: "Prague — digging harmonic layers no one else hears." },
  { name: "Emi W.", country: "KR", bio: "Seoul — riding dynamic shifts at maximum salience." },
  { name: "Dante F.", country: "IT", bio: "Milan — every vibrato is a prediction error." },
  { name: "Isla M.", country: "NZ", bio: "Auckland — drifting through ambient fields of familiarity." },
  { name: "Kofi A.", country: "GH", bio: "Accra — my motor cortex speaks in polyrhythm." },
  { name: "Sven K.", country: "SE", bio: "Stockholm — mapping the edge where consonance dissolves." },
  { name: "Luna Z.", country: "MX", bio: "Mexico City — silence is my loudest instrument." },
];

const EMOTE_TYPES: ResonanceSignal["type"][] = ["wave", "chills", "vibe", "feel", "sync"];

/* ── Pseudo-random (deterministic per seed) ─────────────────────── */

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 16807 + 0) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

/* ── Derive computed fields ─────────────────────────────────────── */

function computeDerived(user: ResonanceUser) {
  let sumSq = 0;
  for (let i = 0; i < 5; i++) sumSq += user.psi[i] * user.psi[i];
  user.intensity = Math.sqrt(sumSq) / MAX_DIST; // 0–1 normalized magnitude
  user.pulseRate = 0.6 + (Math.abs(user.psi[0]) / 5) * 1.4; // arousal drives pulse 0.6–2.0
}

/* ── Map mockUser axes → initial bipolar psi ────────────────────── */

function axesToPsi(axes: {
  entropyTolerance: number;
  resolutionCraving: number;
  monotonyTolerance: number;
  salienceSensitivity: number;
  tensionAppetite: number;
}): Psi5 {
  return [
    (axes.tensionAppetite - 0.5) * 10,       // arousal
    (axes.resolutionCraving - 0.5) * 10,      // valence
    (axes.salienceSensitivity - 0.5) * 10,    // focus
    (1 - axes.monotonyTolerance - 0.5) * 10,  // temporal (novelty)
    (axes.entropyTolerance - 0.5) * 10,       // social
  ];
}

/* ── Generate users ─────────────────────────────────────────────── */

export function generateUsers(selfPsi: Psi5): ResonanceUser[] {
  const users: ResonanceUser[] = [];
  const rng = seededRandom(42);

  // From mockUsers (12)
  for (const mu of mockUsers) {
    const center = axesToPsi(mu.mind.axes);
    const phases: Psi5 = [rng() * 100, rng() * 100, rng() * 100, rng() * 100, rng() * 100];
    const speeds: Psi5 = [
      0.15 + rng() * 0.25,
      0.1 + rng() * 0.2,
      0.08 + rng() * 0.15,
      0.05 + rng() * 0.12,
      0.12 + rng() * 0.2,
    ];
    const amplitude: Psi5 = [
      1.0 + rng() * 2.5,
      0.8 + rng() * 2.0,
      0.6 + rng() * 1.8,
      0.5 + rng() * 1.5,
      0.8 + rng() * 2.2,
    ];
    const psi: Psi5 = [...center];

    const user: ResonanceUser = {
      id: mu.id,
      displayName: mu.displayName,
      avatarUrl: mu.avatarUrl,
      country: mu.country,
      personaId: mu.mind.personaId,
      psi,
      position: [0, 0, 0],
      velocity: [0, 0, 0],
      intensity: 0,
      pulseRate: 1,
      bio: mu.bio ?? "",
      currentTrack: mu.recentTracks?.[0]?.title
        ? `${mu.recentTracks[0].artist} — ${mu.recentTracks[0].title}`
        : undefined,
      _phases: phases,
      _speeds: speeds,
      _center: center,
      _amplitude: amplitude,
    };
    computeDerived(user);
    users.push(user);
  }

  // 8 procedural users
  for (let i = 0; i < EXTRA_USERS.length; i++) {
    const ex = EXTRA_USERS[i];
    const personaIdx = Math.floor(rng() * personas.length);
    const center: Psi5 = [
      (rng() - 0.5) * 8,
      (rng() - 0.5) * 8,
      (rng() - 0.5) * 8,
      (rng() - 0.5) * 8,
      (rng() - 0.5) * 8,
    ];
    const phases: Psi5 = [rng() * 100, rng() * 100, rng() * 100, rng() * 100, rng() * 100];
    const speeds: Psi5 = [
      0.15 + rng() * 0.3,
      0.1 + rng() * 0.25,
      0.08 + rng() * 0.18,
      0.05 + rng() * 0.15,
      0.12 + rng() * 0.22,
    ];
    const amplitude: Psi5 = [
      1.0 + rng() * 2.5,
      0.8 + rng() * 2.0,
      0.6 + rng() * 1.8,
      0.5 + rng() * 1.5,
      0.8 + rng() * 2.2,
    ];
    const psi: Psi5 = [...center];

    const user: ResonanceUser = {
      id: `gen-${i}`,
      displayName: ex.name,
      avatarUrl: `/avatars/photo_gen_${i}.png`,
      country: ex.country,
      personaId: personas[personaIdx].id,
      psi,
      position: [0, 0, 0],
      velocity: [0, 0, 0],
      intensity: 0,
      pulseRate: 1,
      bio: ex.bio,
      _phases: phases,
      _speeds: speeds,
      _center: center,
      _amplitude: amplitude,
    };
    computeDerived(user);
    users.push(user);
  }

  initializePositions(users, selfPsi);
  return users;
}

/* ── Resonance metric (1 = identical, 0 = maximally different) ──── */

export function resonance(a: Psi5, b: Psi5): number {
  let sumSq = 0;
  for (let i = 0; i < 5; i++) {
    const d = a[i] - b[i];
    sumSq += d * d;
  }
  return 1 - Math.sqrt(sumSq) / MAX_DIST;
}

/* ── Per-dimension resonance (how close on single axis, 0–1) ───── */

export function dimResonance(a: number, b: number): number {
  return 1 - Math.abs(a - b) / 10;
}

/* ── Initialize positions ───────────────────────────────────────── */

function initializePositions(users: ResonanceUser[], selfPsi: Psi5) {
  const n = users.length;
  for (let i = 0; i < n; i++) {
    const res = resonance(selfPsi, users[i].psi);
    const dist = 5 + (1 - res) * 16;
    const phi = Math.acos(1 - 2 * (i + 0.5) / n);
    const theta = Math.PI * (1 + Math.sqrt(5)) * i;
    users[i].position = [
      dist * Math.sin(phi) * Math.cos(theta),
      (dist * Math.cos(phi)) * 0.35,
      dist * Math.sin(phi) * Math.sin(theta),
    ];
  }
}

/* ── 60 fps continuous evolution ─────────────────────────────────── */

export function evolve(
  users: ResonanceUser[],
  selfPsi: Psi5,
  dt: number,
  time: number,
) {
  for (let i = 0; i < users.length; i++) {
    const u = users[i];

    // Advance oscillator phases continuously
    for (let d = 0; d < 5; d++) {
      u._phases[d] += u._speeds[d] * dt;

      // Multi-layer oscillation: slow drift + medium wave + fast tremor
      const slow  = Math.sin(u._phases[d] * 0.3) * u._amplitude[d] * 0.6;
      const med   = Math.sin(u._phases[d] * 1.1 + d * 1.7) * u._amplitude[d] * 0.3;
      const fast  = Math.sin(u._phases[d] * 3.7 + i * 0.9) * u._amplitude[d] * 0.1;

      const target = u._center[d] + slow + med + fast;
      // Smooth chase toward target (creates organic lag)
      u.psi[d] += (target - u.psi[d]) * Math.min(2.5 * dt, 0.15);
      // Clamp to [-5, +5]
      u.psi[d] = Math.max(-5, Math.min(5, u.psi[d]));
    }

    computeDerived(u);
  }

  updatePositions(users, selfPsi, dt);
}

/* ── Force-directed layout ──────────────────────────────────────── */

function updatePositions(users: ResonanceUser[], selfPsi: Psi5, dt: number) {
  const n = users.length;
  const forces: [number, number, number][] = users.map(() => [0, 0, 0]);

  for (let i = 0; i < n; i++) {
    for (let j = i + 1; j < n; j++) {
      const dx = users[j].position[0] - users[i].position[0];
      const dy = users[j].position[1] - users[i].position[1];
      const dz = users[j].position[2] - users[i].position[2];
      const distSq = dx * dx + dy * dy + dz * dz + 0.01;
      const dist = Math.sqrt(distSq);

      const res = resonance(users[i].psi, users[j].psi);

      // Repulsive
      const rep = 2.0 / distSq;
      const rx = (dx / dist) * rep;
      const ry = (dy / dist) * rep;
      const rz = (dz / dist) * rep;
      forces[i][0] -= rx; forces[i][1] -= ry; forces[i][2] -= rz;
      forces[j][0] += rx; forces[j][1] += ry; forces[j][2] += rz;

      // Attractive when resonant
      if (res > 0.5) {
        const ideal = 4 + (1 - res) * 10;
        const att = (dist - ideal) * 0.025 * (res - 0.5);
        const ax = (dx / dist) * att;
        const ay = (dy / dist) * att;
        const az = (dz / dist) * att;
        forces[i][0] += ax; forces[i][1] += ay; forces[i][2] += az;
        forces[j][0] -= ax; forces[j][1] -= ay; forces[j][2] -= az;
      }
    }

    // Pull toward distance from origin based on resonance with self
    const res = resonance(selfPsi, users[i].psi);
    const ideal = 5 + (1 - res) * 16;
    const px = users[i].position[0], py = users[i].position[1], pz = users[i].position[2];
    const cd = Math.sqrt(px * px + py * py + pz * pz) + 0.01;
    const pull = (cd - ideal) * 0.012;
    forces[i][0] -= (px / cd) * pull;
    forces[i][1] -= (py / cd) * pull;
    forces[i][2] -= (pz / cd) * pull;
  }

  const damp = 0.92;
  for (let i = 0; i < n; i++) {
    users[i].velocity[0] = (users[i].velocity[0] + forces[i][0] * dt) * damp;
    users[i].velocity[1] = (users[i].velocity[1] + forces[i][1] * dt) * damp;
    users[i].velocity[2] = (users[i].velocity[2] + forces[i][2] * dt) * damp;
    users[i].position[0] += users[i].velocity[0] * dt;
    users[i].position[1] += users[i].velocity[1] * dt;
    users[i].position[2] += users[i].velocity[2] * dt;
    users[i].position[1] *= 0.98;
    const d = Math.sqrt(users[i].position[0] ** 2 + users[i].position[1] ** 2 + users[i].position[2] ** 2);
    if (d > 25) {
      const s = 25 / d;
      users[i].position[0] *= s; users[i].position[1] *= s; users[i].position[2] *= s;
    }
  }
}

/* ── Compute connections ────────────────────────────────────────── */

export function computeConnections(
  users: ResonanceUser[],
  selfPsi: Psi5,
  threshold = 0.55,
): Connection[] {
  const connections: Connection[] = [];
  const allPsi = [selfPsi, ...users.map(u => u.psi)];
  const allIds = ["self", ...users.map(u => u.id)];

  for (let i = 0; i < allIds.length; i++) {
    for (let j = i + 1; j < allIds.length; j++) {
      const res = resonance(allPsi[i] as Psi5, allPsi[j] as Psi5);
      if (res > threshold) {
        // Find dimension with strongest resonance
        let bestDim = 0, bestDimRes = 0;
        for (let d = 0; d < 5; d++) {
          const dr = dimResonance(allPsi[i][d], allPsi[j][d]);
          if (dr > bestDimRes) { bestDimRes = dr; bestDim = d; }
        }
        connections.push({
          id: `${allIds[i]}-${allIds[j]}`,
          userA: allIds[i],
          userB: allIds[j],
          strength: (res - threshold) / (1 - threshold),
          dominantDim: bestDim,
        });
      }
    }
  }

  connections.sort((a, b) => b.strength - a.strength);
  return connections.slice(0, 25);
}

/* ── Random signal ──────────────────────────────────────────────── */

export function generateRandomSignal(users: ResonanceUser[]): ResonanceSignal | null {
  if (users.length < 2) return null;
  const from = users[Math.floor(Math.random() * users.length)];
  const toSelf = Math.random() < 0.4;
  const toId = toSelf ? "self" : users[Math.floor(Math.random() * users.length)].id;
  const type = EMOTE_TYPES[Math.floor(Math.random() * EMOTE_TYPES.length)];
  return {
    id: `sig-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    from: from.id, to: toId, type, content: type, ts: Date.now(), received: false,
  };
}
