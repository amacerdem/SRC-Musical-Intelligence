/* ── Duo Game Engine — Score, Combo, Tasks, Achievements ──────── */

import { ACHIEVEMENTS, TASK_POOL, type Achievement, type DuoTask } from "./duo-achievements";

/* ── Types ─────────────────────────────────────────────────────── */

export interface ActiveTask {
  task: DuoTask;
  startTime: number;
  progress: number; // 0-1
  completed: boolean;
}

export interface GameEvent {
  type: "achievement" | "task_complete" | "task_new" | "combo_up" | "score";
  achievement?: Achievement;
  task?: DuoTask;
  xp?: number;
  combo?: number;
  timestamp: number;
}

export interface GameState {
  score: number;
  combo: number;
  comboTimer: number;  // seconds of sustained resonance
  achievements: Set<string>;
  activeTask: ActiveTask | null;
  completedTasks: string[];
  events: GameEvent[]; // recent events for UI consumption
  sessionTime: number;
  resonanceStreak: number; // seconds of continuous high resonance
  paramHistory: { emo: number[]; phys: number[] }[]; // last 60 frames
}

/* ── Engine ────────────────────────────────────────────────────── */

export class DuoGameEngine {
  private state: GameState;
  private nextTaskTime = 8; // first task at 8s
  private usedTasks = new Set<string>();

  constructor() {
    this.state = {
      score: 0,
      combo: 1,
      comboTimer: 0,
      achievements: new Set(),
      activeTask: null,
      completedTasks: [],
      events: [],
      sessionTime: 0,
      resonanceStreak: 0,
      paramHistory: [],
    };
  }

  getState(): Readonly<GameState> {
    return this.state;
  }

  /** Call every frame with current params and resonance */
  tick(dt: number, emo: number[], phys: number[], resonance: number): GameEvent[] {
    const events: GameEvent[] = [];
    this.state.sessionTime += dt;
    const t = this.state.sessionTime;

    // Record param history (keep last 60 entries ≈ 1s at 60fps)
    this.state.paramHistory.push({ emo: [...emo], phys: [...phys] });
    if (this.state.paramHistory.length > 60) this.state.paramHistory.shift();

    // ── Combo system: sustained resonance builds multiplier ──
    if (resonance > 0.5) {
      this.state.comboTimer += dt;
      if (this.state.comboTimer >= 3) {
        const newCombo = Math.min(1 + Math.floor(this.state.comboTimer / 3) * 0.4, 5);
        if (newCombo > this.state.combo) {
          this.state.combo = Math.round(newCombo * 10) / 10;
          events.push({ type: "combo_up", combo: this.state.combo, timestamp: t });
        }
      }
    } else {
      this.state.comboTimer = Math.max(0, this.state.comboTimer - dt * 2);
      if (this.state.comboTimer <= 0) this.state.combo = 1;
    }

    // ── Base score from resonance ──
    const basePoints = resonance * 2 * dt;
    this.state.score += basePoints * this.state.combo;

    // ── Resonance streak tracking ──
    if (resonance > 0.6) {
      this.state.resonanceStreak += dt;
    } else {
      this.state.resonanceStreak = Math.max(0, this.state.resonanceStreak - dt * 3);
    }

    // ── Achievement checks ──
    events.push(...this.checkAchievements(emo, phys, resonance));

    // ── Task management ──
    events.push(...this.manageTasks(dt, emo, phys));

    this.state.events.push(...events);
    // Keep only last 20 events
    if (this.state.events.length > 20) {
      this.state.events = this.state.events.slice(-20);
    }

    return events;
  }

  /* ── Achievement Checks ─────────────────────────────────────── */

  private checkAchievements(emo: number[], phys: number[], resonance: number): GameEvent[] {
    const events: GameEvent[] = [];
    const t = this.state.sessionTime;
    const unlock = (id: string) => {
      if (this.state.achievements.has(id)) return;
      const ach = ACHIEVEMENTS.find(a => a.id === id);
      if (!ach) return;
      this.state.achievements.add(id);
      this.state.score += ach.xp * this.state.combo;
      events.push({ type: "achievement", achievement: ach, xp: Math.round(ach.xp * this.state.combo), timestamp: t });
    };

    // First Resonance: resonance > 0.5 for the first time after 10s
    if (t > 10 && resonance > 0.5) unlock("first_resonance");

    // Flow Master: 15s continuous high resonance
    if (this.state.resonanceStreak >= 15) unlock("flow_master");

    // Chaos Alchemist: arousal > 0.85 AND energy > 0.85
    if (emo[1] > 0.85 && phys[1] > 0.85) unlock("chaos_alchemist");

    // Whisper: all params < 0.2
    if ([...emo, ...phys].every(v => v < 0.2)) unlock("whisper");

    // Perfect Sync: all 8 params within 10%
    if (emo.every((v, i) => Math.abs(v - phys[i]) < 0.1)) unlock("perfect_sync");

    // Crescendo Rider: peak at 90s mark (within 85-95s window)
    if (t >= 85 && t <= 95) {
      const avgAll = [...emo, ...phys].reduce((a, b) => a + b, 0) / 8;
      if (avgAll > 0.75) unlock("crescendo_rider");
    }

    // Genre Bender: detect rapid parameter changes in history
    if (this.state.paramHistory.length >= 30) {
      const recent = this.state.paramHistory.slice(-30);
      let totalDelta = 0;
      for (let i = 1; i < recent.length; i++) {
        for (let j = 0; j < 4; j++) {
          totalDelta += Math.abs(recent[i].emo[j] - recent[i - 1].emo[j]);
          totalDelta += Math.abs(recent[i].phys[j] - recent[i - 1].phys[j]);
        }
      }
      if (totalDelta > 15) unlock("genre_bender");
    }

    // Neural Link: 30s unbroken resonance
    if (this.state.resonanceStreak >= 30) unlock("neural_link");

    // Finale: completed 2 minutes
    if (t >= 120) unlock("finale");

    return events;
  }

  /* ── Task Management ────────────────────────────────────────── */

  private manageTasks(dt: number, emo: number[], phys: number[]): GameEvent[] {
    const events: GameEvent[] = [];
    const t = this.state.sessionTime;

    // Spawn new task
    if (!this.state.activeTask && t >= this.nextTaskTime && t < 110) {
      const available = TASK_POOL.filter(tk => !this.usedTasks.has(tk.id));
      if (available.length > 0) {
        const task = available[Math.floor(Math.random() * available.length)];
        this.usedTasks.add(task.id);
        this.state.activeTask = { task, startTime: t, progress: 0, completed: false };
        events.push({ type: "task_new", task, timestamp: t });
      }
    }

    // Update active task
    if (this.state.activeTask && !this.state.activeTask.completed) {
      const at = this.state.activeTask;
      const elapsed = t - at.startTime;
      at.progress = Math.max(0, Math.min(1, at.task.evaluate(emo, phys)));

      // Check completion (progress > 0.85 for at least a moment)
      if (at.progress >= 0.85) {
        at.completed = true;
        const xp = Math.round(at.task.xp * this.state.combo);
        this.state.score += xp;
        this.state.completedTasks.push(at.task.id);
        events.push({ type: "task_complete", task: at.task, xp, timestamp: t });
        this.state.activeTask = null;
        this.nextTaskTime = t + 8 + Math.random() * 12; // next task in 8-20s
      }
      // Timeout
      else if (elapsed >= at.task.durationSec) {
        this.state.activeTask = null;
        this.nextTaskTime = t + 5 + Math.random() * 8;
      }
    }

    return events;
  }
}
