/* ── Resonance Field — Zustand store (ephemeral, no persist) ──── */

import { create } from "zustand";
import {
  generateUsers,
  evolveBeliefsAndPositions,
  computeConnections,
  generateRandomSignal,
  type ResonanceUser,
  type Connection,
  type ResonanceSignal,
} from "@/data/resonance-simulation";
import { useUserStore } from "./useUserStore";

/* ── Types ──────────────────────────────────────────────────────── */

interface ResonanceState {
  users: ResonanceUser[];
  connections: Connection[];
  signals: ResonanceSignal[];
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

/* ── Self beliefs helper ────────────────────────────────────────── */

function getSelfBeliefs(): [number, number, number, number, number] {
  const mind = useUserStore.getState().mind;
  if (!mind) return [0.5, 0.5, 0.5, 0.5, 0.5];
  const a = mind.axes;
  // Map axes to belief-like values
  return [
    1 - a.entropyTolerance,     // consonance (inverse of entropy tolerance)
    a.tensionAppetite,           // tempo (tension maps to rhythmic drive)
    a.salienceSensitivity,       // salience
    a.monotonyTolerance,         // familiarity (monotony tolerance → familiarity seeking)
    a.resolutionCraving,         // reward (resolution craving → reward sensitivity)
  ];
}

/* ── Store ──────────────────────────────────────────────────────── */

export const useResonanceStore = create<ResonanceState>((set, get) => ({
  users: [],
  connections: [],
  signals: [],
  selectedUserId: null,
  entranceComplete: false,
  cameraMode: "self",
  time: 0,
  _connectionTimer: 0,
  _signalTimer: 10 + Math.random() * 10,

  initialize: () => {
    const selfBeliefs = getSelfBeliefs();
    const users = generateUsers(selfBeliefs);
    const connections = computeConnections(users, selfBeliefs);
    set({ users, connections, signals: [], selectedUserId: null, time: 0 });
  },

  tick: (dt: number) => {
    const state = get();
    if (state.users.length === 0) return;

    const selfBeliefs = getSelfBeliefs();
    const newTime = state.time + dt;

    // Evolve beliefs and positions
    evolveBeliefsAndPositions(state.users, selfBeliefs, dt, newTime);

    // Recompute connections every 2s
    let newConnections = state.connections;
    let connTimer = state._connectionTimer + dt;
    if (connTimer >= 2) {
      connTimer = 0;
      newConnections = computeConnections(state.users, selfBeliefs);
    }

    // Random incoming signal
    let newSignals = state.signals;
    let sigTimer = state._signalTimer - dt;
    if (sigTimer <= 0) {
      sigTimer = 15 + Math.random() * 15;
      const sig = generateRandomSignal(state.users);
      if (sig) {
        newSignals = [...state.signals, sig];
      }
    }

    // Expire old signals (> 6s)
    const now = Date.now();
    newSignals = newSignals.filter(s => now - s.ts < 6000);

    set({
      time: newTime,
      connections: newConnections,
      signals: newSignals,
      _connectionTimer: connTimer,
      _signalTimer: sigTimer,
    });
  },

  selectUser: (id) => {
    set({
      selectedUserId: id,
      cameraMode: id ? "selected" : "self",
    });
  },

  sendSignal: (to, type, content) => {
    const signal: ResonanceSignal = {
      id: `sig-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      from: "self",
      to,
      type,
      content,
      ts: Date.now(),
      received: false,
    };
    const state = get();
    set({ signals: [...state.signals, signal] });

    // Simulate response after 2-4s
    setTimeout(() => {
      const respType = (["wave", "chills", "vibe", "feel", "sync"] as const)[
        Math.floor(Math.random() * 5)
      ];
      const response: ResonanceSignal = {
        id: `sig-${Date.now()}-resp`,
        from: to,
        to: "self",
        type: respType,
        content: respType,
        ts: Date.now(),
        received: false,
      };
      const current = get();
      set({ signals: [...current.signals, response] });
    }, 2000 + Math.random() * 2000);
  },

  completeEntrance: () => set({ entranceComplete: true }),

  setCameraMode: (mode) => set({ cameraMode: mode }),

  cleanup: () => set({
    users: [],
    connections: [],
    signals: [],
    selectedUserId: null,
    entranceComplete: false,
    cameraMode: "self",
    time: 0,
  }),
}));
