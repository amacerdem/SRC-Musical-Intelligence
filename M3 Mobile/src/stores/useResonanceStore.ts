/* -- Resonance Field -- Zustand store (ephemeral, no persist) ---------------- */

import { create } from "zustand";
import {
  generateUsers,
  evolve,
  computeConnections,
  generateRandomSignal,
  type ResonanceUser,
  type Connection,
  type ResonanceSignal,
  type Psi5,
} from "../data/resonance-simulation";
import { useUserStore } from "./useUserStore";

/* -- Self track playlist ----------------------------------------------------- */

export const SELF_TRACKS = [
  { title: "Luminous Beings", artist: "Jon Hopkins", duration: 312 },
  { title: "On The Nature of Daylight", artist: "Max Richter", duration: 378 },
  { title: "Nuvole Bianche", artist: "Ludovico Einaudi", duration: 337 },
  { title: "Ageispolis", artist: "Aphex Twin", duration: 298 },
  { title: "Says", artist: "Nils Frahm", duration: 332 },
];

/* -- Types ------------------------------------------------------------------- */

interface ResonanceState {
  users: ResonanceUser[];
  connections: Connection[];
  signals: ResonanceSignal[];
  selfPsi: Psi5;
  selectedUserId: string | null;
  entranceComplete: boolean;
  cameraMode: "self" | "selected" | "free";
  time: number;
  _connectionTimer: number;
  _signalTimer: number;
  /** Self-user oscillator state for dynamic psi evolution */
  _selfCenter: Psi5;
  _selfPhases: Psi5;
  _selfSpeeds: Psi5;
  _selfAmplitude: Psi5;
  /** Playback state */
  isPlaying: boolean;
  selfPlaybackTime: number;
  selfTrackIdx: number;

  initialize: () => void;
  tick: (dt: number) => void;
  selectUser: (id: string | null) => void;
  sendSignal: (to: string, type: ResonanceSignal["type"], content: string) => void;
  completeEntrance: () => void;
  setCameraMode: (mode: "self" | "selected" | "free") => void;
  togglePlay: () => void;
  skipTrack: () => void;
  cleanup: () => void;
}

/* -- Map user axes -> bipolar Psi5 [-5, +5] ---------------------------------- */

function getSelfPsi(): Psi5 {
  const mind = useUserStore.getState().mind;
  if (!mind) return [0, 0, 0, 0, 0];
  const a = mind.axes;
  return [
    (a.tensionAppetite - 0.5) * 10,        // arousal
    (a.resolutionCraving - 0.5) * 10,       // valence
    (a.salienceSensitivity - 0.5) * 10,     // focus
    (1 - a.monotonyTolerance - 0.5) * 10,   // temporal (novelty)
    (a.entropyTolerance - 0.5) * 10,        // social
  ];
}

/* -- Store ------------------------------------------------------------------- */

export const useResonanceStore = create<ResonanceState>((set, get) => ({
  users: [],
  connections: [],
  signals: [],
  selfPsi: [0, 0, 0, 0, 0],
  selectedUserId: null,
  entranceComplete: false,
  cameraMode: "self",
  time: 0,
  _connectionTimer: 0,
  _signalTimer: 10 + Math.random() * 10,
  _selfCenter: [0, 0, 0, 0, 0],
  _selfPhases: [0, 0, 0, 0, 0],
  _selfSpeeds: [0.12, 0.09, 0.07, 0.05, 0.10],
  _selfAmplitude: [0.8, 0.6, 0.5, 0.4, 0.7],
  isPlaying: true,
  selfPlaybackTime: 0,
  selfTrackIdx: 0,

  initialize: () => {
    const selfCenter = getSelfPsi();
    const selfPsi: Psi5 = [...selfCenter];
    const users = generateUsers(selfPsi);
    const connections = computeConnections(users, selfPsi);
    set({
      users, connections, selfPsi, signals: [],
      selectedUserId: null, time: 0,
      isPlaying: true, selfPlaybackTime: 0, selfTrackIdx: 0,
      _selfCenter: selfCenter,
      _selfPhases: [
        Math.random() * 100, Math.random() * 100, Math.random() * 100,
        Math.random() * 100, Math.random() * 100,
      ] as Psi5,
    });
  },

  tick: (dt: number) => {
    const state = get();
    if (state.users.length === 0) return;

    const newTime = state.time + dt;

    // Advance self playback
    let newPlaybackTime = state.selfPlaybackTime;
    let newTrackIdx = state.selfTrackIdx;
    let energyFactor = 1.0;

    if (state.isPlaying) {
      newPlaybackTime += dt;
      if (newPlaybackTime >= SELF_TRACKS[newTrackIdx].duration) {
        newTrackIdx = (newTrackIdx + 1) % SELF_TRACKS.length;
        newPlaybackTime = 0;
      }
      // Music energy curve -- peaks at verse/chorus transitions
      const progress = newPlaybackTime / SELF_TRACKS[newTrackIdx].duration;
      const energy = 0.5 + 0.3 * Math.sin(progress * Math.PI) + 0.2 * Math.sin(progress * 3 * Math.PI);
      energyFactor = 0.7 + 0.6 * energy;
    }

    // Evolve self psi with gentle oscillators (modulated by track energy)
    const selfPsi: Psi5 = [...state.selfPsi];
    const phases = state._selfPhases;
    for (let d = 0; d < 5; d++) {
      phases[d] += state._selfSpeeds[d] * dt;
      const slow = Math.sin(phases[d] * 0.3) * state._selfAmplitude[d] * 0.6;
      const med  = Math.sin(phases[d] * 1.1 + d * 1.7) * state._selfAmplitude[d] * 0.3;
      const fast = Math.sin(phases[d] * 3.7) * state._selfAmplitude[d] * 0.1;
      const target = state._selfCenter[d] + (slow + med + fast) * energyFactor;
      selfPsi[d] += (target - selfPsi[d]) * Math.min(2.5 * dt, 0.15);
      selfPsi[d] = Math.max(-5, Math.min(5, selfPsi[d]));
    }

    // Continuous 60fps evolution
    evolve(state.users, selfPsi, dt, newTime);

    // Recompute connections every 1.5s (more responsive)
    let newConnections = state.connections;
    let connTimer = state._connectionTimer + dt;
    if (connTimer >= 1.5) {
      connTimer = 0;
      newConnections = computeConnections(state.users, selfPsi);
    }

    // Random incoming signals
    let newSignals = state.signals;
    let sigTimer = state._signalTimer - dt;
    if (sigTimer <= 0) {
      sigTimer = 12 + Math.random() * 18;
      const sig = generateRandomSignal(state.users);
      if (sig) newSignals = [...state.signals, sig];
    }

    // Expire old signals (> 6s)
    const now = Date.now();
    newSignals = newSignals.filter(s => now - s.ts < 6000);

    set({
      time: newTime,
      selfPsi,
      connections: newConnections,
      signals: newSignals,
      _connectionTimer: connTimer,
      _signalTimer: sigTimer,
      selfPlaybackTime: newPlaybackTime,
      selfTrackIdx: newTrackIdx,
    });
  },

  selectUser: (id) => set({
    selectedUserId: id,
    cameraMode: id ? "selected" : "self",
  }),

  sendSignal: (to, type, content) => {
    const signal: ResonanceSignal = {
      id: `sig-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      from: "self", to, type, content, ts: Date.now(), received: false,
    };
    set(s => ({ signals: [...s.signals, signal] }));

    // Simulated response 2-4s later
    setTimeout(() => {
      const respType = (["wave", "chills", "vibe", "feel", "sync"] as const)[
        Math.floor(Math.random() * 5)
      ];
      const response: ResonanceSignal = {
        id: `sig-${Date.now()}-resp`,
        from: to, to: "self", type: respType, content: respType,
        ts: Date.now(), received: false,
      };
      set(s => ({ signals: [...s.signals, response] }));
    }, 2000 + Math.random() * 2000);
  },

  completeEntrance: () => set({ entranceComplete: true }),
  setCameraMode: (mode) => set({ cameraMode: mode }),
  togglePlay: () => set(s => ({ isPlaying: !s.isPlaying })),
  skipTrack: () => set(s => ({
    selfTrackIdx: (s.selfTrackIdx + 1) % SELF_TRACKS.length,
    selfPlaybackTime: 0,
  })),

  cleanup: () => set({
    users: [], connections: [], signals: [],
    selfPsi: [0, 0, 0, 0, 0],
    selectedUserId: null, entranceComplete: false,
    cameraMode: "self", time: 0,
    _selfCenter: [0, 0, 0, 0, 0],
    _selfPhases: [0, 0, 0, 0, 0],
    isPlaying: true, selfPlaybackTime: 0, selfTrackIdx: 0,
  }),
}));
