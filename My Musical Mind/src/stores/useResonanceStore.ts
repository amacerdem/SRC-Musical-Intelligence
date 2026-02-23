/* ── Resonance Field — Zustand store (ephemeral, no persist) ──── */

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
} from "@/data/resonance-simulation";
import { useUserStore } from "./useUserStore";

/* ── Types ──────────────────────────────────────────────────────── */

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

  initialize: () => void;
  tick: (dt: number) => void;
  selectUser: (id: string | null) => void;
  sendSignal: (to: string, type: ResonanceSignal["type"], content: string) => void;
  completeEntrance: () => void;
  setCameraMode: (mode: "self" | "selected" | "free") => void;
  cleanup: () => void;
}

/* ── Map user axes → bipolar Psi5 [-5, +5] ──────────────────────── */

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

/* ── Store ──────────────────────────────────────────────────────── */

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

  initialize: () => {
    const selfPsi = getSelfPsi();
    const users = generateUsers(selfPsi);
    const connections = computeConnections(users, selfPsi);
    set({ users, connections, selfPsi, signals: [], selectedUserId: null, time: 0 });
  },

  tick: (dt: number) => {
    const state = get();
    if (state.users.length === 0) return;

    const selfPsi = getSelfPsi();
    const newTime = state.time + dt;

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

  cleanup: () => set({
    users: [], connections: [], signals: [],
    selfPsi: [0, 0, 0, 0, 0],
    selectedUserId: null, entranceComplete: false,
    cameraMode: "self", time: 0,
  }),
}));
