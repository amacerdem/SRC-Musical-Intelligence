/* ── Resonance Field — Mock user generation + state evolution ─── */

import { mockUsers } from "./mock-users";
import { personas } from "./personas";

/* ── Types ──────────────────────────────────────────────────────── */

export interface ResonanceUser {
  id: string;
  displayName: string;
  avatarUrl: string;
  country: string;
  personaId: number;
  beliefs: [number, number, number, number, number]; // C/T/S/F/R
  targetBeliefs: [number, number, number, number, number];
  position: [number, number, number];
  velocity: [number, number, number];
  dominantBelief: number;
  intensity: number;
  pulseRate: number;
  bio: string;
  currentTrack?: string;
  /** Internal: seconds until next target shift */
  _nextShift: number;
}

export interface Connection {
  id: string;
  userA: string;
  userB: string;
  strength: number;
  dominantBelief: number;
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

const BELIEF_NAMES = ["consonance", "tempo", "salience", "familiarity", "reward"] as const;

const EXTRA_USERS: { name: string; country: string; bio: string }[] = [
  { name: "Anika S.", country: "IN", bio: "Mumbai. Raga interpreter — melody is consciousness unfolding." },
  { name: "Tomas R.", country: "CZ", bio: "Prague. Harmonic archaeologist digging layers in every chord." },
  { name: "Emi W.", country: "KR", bio: "Seoul. K-wave surfer riding dynamic shifts at 0.95σ salience." },
  { name: "Dante F.", country: "IT", bio: "Milan. Opera neural maximalist — every vibrato is a prediction error." },
  { name: "Isla M.", country: "NZ", bio: "Auckland. Ambient drifter — familiarity is my compass." },
  { name: "Kofi A.", country: "GH", bio: "Accra. Polyrhythm native — my motor cortex speaks in 12/8." },
  { name: "Sven K.", country: "SE", bio: "Stockholm. Noise cartographer mapping the edge of consonance." },
  { name: "Luna Z.", country: "MX", bio: "Mexico City. Tension sculptor — silence is my loudest instrument." },
];

const EMOTE_RESPONSES: ResonanceSignal["type"][] = ["wave", "chills", "vibe", "feel", "sync"];

/* ── Pseudo-random (deterministic per seed) ─────────────────────── */

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 16807 + 0) % 2147483647;
    return (s - 1) / 2147483646;
  };
}

/* ── Simple noise for smooth belief evolution ───────────────────── */

function smoothNoise(t: number, seed: number): number {
  const s = seededRandom(seed + Math.floor(t));
  const a = s() * 2 - 1;
  const b = seededRandom(seed + Math.floor(t) + 1)() * 2 - 1;
  const frac = t - Math.floor(t);
  const smooth = frac * frac * (3 - 2 * frac); // hermite
  return a + (b - a) * smooth;
}

/* ── Derive computed fields ─────────────────────────────────────── */

function computeDerived(user: ResonanceUser) {
  const sum = user.beliefs.reduce((a, b) => a + b, 0);
  user.intensity = sum / 5;
  user.pulseRate = 0.8 + (user.beliefs[4] + user.beliefs[2]) * 0.6; // reward + salience
  let maxIdx = 0;
  let maxVal = 0;
  for (let i = 0; i < 5; i++) {
    if (user.beliefs[i] > maxVal) { maxVal = user.beliefs[i]; maxIdx = i; }
  }
  user.dominantBelief = maxIdx;
}

/* ── Generate initial users ─────────────────────────────────────── */

export function generateUsers(selfBeliefs: [number, number, number, number, number]): ResonanceUser[] {
  const users: ResonanceUser[] = [];
  const rng = seededRandom(42);

  // Seed from existing mockUsers (12)
  for (const mu of mockUsers) {
    const bs = mu.listening?.beliefSnapshot ?? [0.5, 0.5, 0.5, 0.5, 0.5];
    const beliefs: [number, number, number, number, number] = [bs[0], bs[1], bs[2], bs[3], bs[4]];
    const user: ResonanceUser = {
      id: mu.id,
      displayName: mu.displayName,
      avatarUrl: mu.avatarUrl,
      country: mu.country,
      personaId: mu.mind.personaId,
      beliefs,
      targetBeliefs: [...beliefs],
      position: [0, 0, 0],
      velocity: [0, 0, 0],
      dominantBelief: 0,
      intensity: 0,
      pulseRate: 1,
      bio: mu.bio ?? "",
      currentTrack: mu.recentTracks?.[0]?.title
        ? `${mu.recentTracks[0].artist} — ${mu.recentTracks[0].title}`
        : undefined,
      _nextShift: 8 + rng() * 12,
    };
    computeDerived(user);
    users.push(user);
  }

  // Add 8 procedural users
  for (let i = 0; i < EXTRA_USERS.length; i++) {
    const ex = EXTRA_USERS[i];
    const personaIdx = Math.floor(rng() * personas.length);
    const beliefs: [number, number, number, number, number] = [
      0.2 + rng() * 0.6,
      0.2 + rng() * 0.6,
      0.2 + rng() * 0.6,
      0.2 + rng() * 0.6,
      0.2 + rng() * 0.6,
    ];
    const user: ResonanceUser = {
      id: `gen-${i}`,
      displayName: ex.name,
      avatarUrl: `/avatars/photo_gen_${i}.png`,
      country: ex.country,
      personaId: personas[personaIdx].id,
      beliefs,
      targetBeliefs: [...beliefs],
      position: [0, 0, 0],
      velocity: [0, 0, 0],
      dominantBelief: 0,
      intensity: 0,
      pulseRate: 1,
      bio: ex.bio,
      _nextShift: 5 + rng() * 10,
    };
    computeDerived(user);
    users.push(user);
  }

  // Initialize positions using force-directed with selfBeliefs at origin
  initializePositions(users, selfBeliefs);

  return users;
}

/* ── Cosine similarity between two 5D belief vectors ────────────── */

export function beliefSimilarity(
  a: [number, number, number, number, number],
  b: [number, number, number, number, number],
): number {
  let dot = 0, magA = 0, magB = 0;
  for (let i = 0; i < 5; i++) {
    dot += a[i] * b[i];
    magA += a[i] * a[i];
    magB += b[i] * b[i];
  }
  const denom = Math.sqrt(magA) * Math.sqrt(magB);
  return denom > 0 ? dot / denom : 0;
}

/* ── Initialize positions spread on a sphere, biased by similarity ─ */

function initializePositions(
  users: ResonanceUser[],
  selfBeliefs: [number, number, number, number, number],
) {
  const n = users.length;
  for (let i = 0; i < n; i++) {
    const sim = beliefSimilarity(selfBeliefs, users[i].beliefs);
    // Distance: similar users closer (4-8), dissimilar further (12-20)
    const dist = 6 + (1 - sim) * 14;
    // Spread on sphere using golden angle distribution
    const phi = Math.acos(1 - 2 * (i + 0.5) / n);
    const theta = Math.PI * (1 + Math.sqrt(5)) * i;
    users[i].position = [
      dist * Math.sin(phi) * Math.cos(theta),
      (dist * Math.cos(phi)) * 0.4, // flatten Y
      dist * Math.sin(phi) * Math.sin(theta),
    ];
  }
}

/* ── Evolve beliefs over time ───────────────────────────────────── */

export function evolveBeliefsAndPositions(
  users: ResonanceUser[],
  selfBeliefs: [number, number, number, number, number],
  dt: number,
  time: number,
) {
  for (let i = 0; i < users.length; i++) {
    const u = users[i];

    // Count down to next target shift
    u._nextShift -= dt;
    if (u._nextShift <= 0) {
      u._nextShift = 10 + Math.abs(smoothNoise(time, i * 100 + 77)) * 15;
      // Generate new targets using noise
      for (let b = 0; b < 5; b++) {
        const noise = smoothNoise(time * 0.1, i * 5 + b + 1000);
        u.targetBeliefs[b] = Math.max(0.05, Math.min(0.95, u.beliefs[b] + noise * 0.2));
      }
    }

    // Lerp beliefs toward targets
    for (let b = 0; b < 5; b++) {
      u.beliefs[b] += (u.targetBeliefs[b] - u.beliefs[b]) * 0.3 * dt;
      u.beliefs[b] = Math.max(0.02, Math.min(0.98, u.beliefs[b]));
    }

    computeDerived(u);
  }

  // Force-directed position update
  updatePositions(users, selfBeliefs, dt);
}

/* ── Force-directed layout ──────────────────────────────────────── */

function updatePositions(
  users: ResonanceUser[],
  selfBeliefs: [number, number, number, number, number],
  dt: number,
) {
  const n = users.length;
  const forces: [number, number, number][] = users.map(() => [0, 0, 0]);

  for (let i = 0; i < n; i++) {
    // Attraction/repulsion between all pairs
    for (let j = i + 1; j < n; j++) {
      const dx = users[j].position[0] - users[i].position[0];
      const dy = users[j].position[1] - users[i].position[1];
      const dz = users[j].position[2] - users[i].position[2];
      const distSq = dx * dx + dy * dy + dz * dz + 0.01;
      const dist = Math.sqrt(distSq);

      const sim = beliefSimilarity(users[i].beliefs, users[j].beliefs);

      // Repulsive force (always)
      const repulsion = 2.0 / distSq;
      const rx = (dx / dist) * repulsion;
      const ry = (dy / dist) * repulsion;
      const rz = (dz / dist) * repulsion;
      forces[i][0] -= rx; forces[i][1] -= ry; forces[i][2] -= rz;
      forces[j][0] += rx; forces[j][1] += ry; forces[j][2] += rz;

      // Attractive force (when similar)
      if (sim > 0.7) {
        const idealDist = 5 + (1 - sim) * 8;
        const attraction = (dist - idealDist) * 0.02 * (sim - 0.7);
        const ax = (dx / dist) * attraction;
        const ay = (dy / dist) * attraction;
        const az = (dz / dist) * attraction;
        forces[i][0] += ax; forces[i][1] += ay; forces[i][2] += az;
        forces[j][0] -= ax; forces[j][1] -= ay; forces[j][2] -= az;
      }
    }

    // Pull toward appropriate distance from origin (self)
    const sim = beliefSimilarity(selfBeliefs, users[i].beliefs);
    const idealDist = 6 + (1 - sim) * 14;
    const px = users[i].position[0];
    const py = users[i].position[1];
    const pz = users[i].position[2];
    const currentDist = Math.sqrt(px * px + py * py + pz * pz) + 0.01;
    const pull = (currentDist - idealDist) * 0.01;
    forces[i][0] -= (px / currentDist) * pull;
    forces[i][1] -= (py / currentDist) * pull;
    forces[i][2] -= (pz / currentDist) * pull;
  }

  // Apply forces with damping
  const damping = 0.92;
  for (let i = 0; i < n; i++) {
    users[i].velocity[0] = (users[i].velocity[0] + forces[i][0] * dt) * damping;
    users[i].velocity[1] = (users[i].velocity[1] + forces[i][1] * dt) * damping;
    users[i].velocity[2] = (users[i].velocity[2] + forces[i][2] * dt) * damping;

    users[i].position[0] += users[i].velocity[0] * dt;
    users[i].position[1] += users[i].velocity[1] * dt;
    users[i].position[2] += users[i].velocity[2] * dt;

    // Flatten Y
    users[i].position[1] *= 0.98;

    // Soft boundary (sphere r=25)
    const d = Math.sqrt(
      users[i].position[0] ** 2 + users[i].position[1] ** 2 + users[i].position[2] ** 2,
    );
    if (d > 25) {
      const s = 25 / d;
      users[i].position[0] *= s;
      users[i].position[1] *= s;
      users[i].position[2] *= s;
    }
  }
}

/* ── Compute connections ────────────────────────────────────────── */

export function computeConnections(
  users: ResonanceUser[],
  selfBeliefs: [number, number, number, number, number],
  threshold = 0.6,
): Connection[] {
  const connections: Connection[] = [];
  const allBeliefs = [selfBeliefs, ...users.map(u => u.beliefs)];
  const allIds = ["self", ...users.map(u => u.id)];

  for (let i = 0; i < allIds.length; i++) {
    for (let j = i + 1; j < allIds.length; j++) {
      const sim = beliefSimilarity(
        allBeliefs[i] as [number, number, number, number, number],
        allBeliefs[j] as [number, number, number, number, number],
      );
      if (sim > threshold) {
        // Find dominant shared belief
        let maxShared = 0, domBelief = 0;
        for (let b = 0; b < 5; b++) {
          const shared = Math.min(allBeliefs[i][b], allBeliefs[j][b]);
          if (shared > maxShared) { maxShared = shared; domBelief = b; }
        }
        connections.push({
          id: `${allIds[i]}-${allIds[j]}`,
          userA: allIds[i],
          userB: allIds[j],
          strength: (sim - threshold) / (1 - threshold),
          dominantBelief: domBelief,
        });
      }
    }
  }

  // Limit to 25 strongest
  connections.sort((a, b) => b.strength - a.strength);
  return connections.slice(0, 25);
}

/* ── Generate random incoming signal ────────────────────────────── */

export function generateRandomSignal(users: ResonanceUser[]): ResonanceSignal | null {
  if (users.length < 2) return null;
  const fromIdx = Math.floor(Math.random() * users.length);
  // 40% chance to target "self", 60% another user
  const toSelf = Math.random() < 0.4;
  const toId = toSelf
    ? "self"
    : users[Math.floor(Math.random() * users.length)].id;
  const type = EMOTE_RESPONSES[Math.floor(Math.random() * EMOTE_RESPONSES.length)];

  return {
    id: `sig-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    from: users[fromIdx].id,
    to: toId,
    type,
    content: type,
    ts: Date.now(),
    received: false,
  };
}

export { BELIEF_NAMES };
