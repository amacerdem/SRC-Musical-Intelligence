/* ── Duo Organism — Dual-Source Generative Neural Confluence ───────
 *  Two flow fields (emotional + physical) converge in center,
 *  creating a resonance zone. Canvas 2D with:
 *  - Dual Perlin-noise flow fields with distinct motion styles
 *  - Particle systems per stream (warm vs cool palette)
 *  - Resonance zone with additive blend + aurora interference
 *  - Game effect overlays (bursts, ring pulses, XP floats)
 *  - Neural constellation (26 brain regions, data-driven)
 *  - Relay flow particles along neural pathways
 *  - PE-driven disruption events + precision-modulated rendering
 *  - R³ group ambient glow zones + brain wave overlay
 *  - Bloom post-processing
 * ────────────────────────────────────────────────────────────────── */

interface RGB { r: number; g: number; b: number }

/* ── Perlin noise ────────────────────────────────────────────────── */
class NoiseField {
  private perm: number[];
  constructor(seed = 42) {
    this.perm = Array.from({ length: 512 }, (_, i) => i % 256);
    let s = seed;
    for (let i = 255; i > 0; i--) {
      s = (s * 16807 + 0) % 2147483647;
      const j = s % (i + 1);
      [this.perm[i], this.perm[j]] = [this.perm[j], this.perm[i]];
    }
    for (let i = 0; i < 256; i++) this.perm[i + 256] = this.perm[i];
  }
  private fade(t: number) { return t * t * t * (t * (t * 6 - 15) + 10); }
  private lerp(a: number, b: number, t: number) { return a + t * (b - a); }
  private grad(hash: number, x: number, y: number) {
    const h = hash & 3;
    const u = h < 2 ? x : y;
    const v = h < 2 ? y : x;
    return ((h & 1) === 0 ? u : -u) + ((h & 2) === 0 ? v : -v);
  }
  noise2D(x: number, y: number): number {
    const X = Math.floor(x) & 255, Y = Math.floor(y) & 255;
    const xf = x - Math.floor(x), yf = y - Math.floor(y);
    const u = this.fade(xf), v = this.fade(yf);
    const p = this.perm;
    const aa = p[p[X] + Y], ab = p[p[X] + Y + 1];
    const ba = p[p[X + 1] + Y], bb = p[p[X + 1] + Y + 1];
    return this.lerp(
      this.lerp(this.grad(aa, xf, yf), this.grad(ba, xf - 1, yf), u),
      this.lerp(this.grad(ab, xf, yf - 1), this.grad(bb, xf - 1, yf - 1), u),
      v
    );
  }
  fbm(x: number, y: number, octaves = 4): number {
    let val = 0, amp = 0.5, freq = 1;
    for (let i = 0; i < octaves; i++) {
      val += amp * this.noise2D(x * freq, y * freq);
      amp *= 0.5;
      freq *= 2;
    }
    return val;
  }
}

/* ── Color Palettes ───────────────────────────────────────────── */

const EMO_PALETTE: RGB[] = [
  { r: 236, g: 72, b: 153 },   // pink (valence)
  { r: 245, g: 158, b: 11 },   // amber (arousal)
  { r: 139, g: 92, b: 246 },   // purple (depth)
  { r: 56, g: 189, b: 248 },   // sky (nostalgia)
];

const PHYS_PALETTE: RGB[] = [
  { r: 249, g: 115, b: 22 },   // orange (tempo)
  { r: 239, g: 68, b: 68 },    // red (energy)
  { r: 132, g: 204, b: 22 },   // lime (dynamics)
  { r: 6, g: 182, b: 212 },    // cyan (density)
];

const RESONANCE_COLOR: RGB = { r: 251, g: 191, b: 36 };

/* ── Particle ─────────────────────────────────────────────────── */
interface DuoParticle {
  x: number; y: number;
  vx: number; vy: number;
  life: number; maxLife: number;
  size: number;
  color: RGB;
  stream: "A" | "B" | "resonance" | "effect";
  trail?: { x: number; y: number }[];
}

/* ── Game Effect ──────────────────────────────────────────────── */
export interface GameEffect {
  type: "xp" | "ring" | "burst" | "flash" | "text";
  x: number; y: number;
  age: number;
  maxAge: number;
  value?: string;
  color: RGB;
  strength: number;
  particles?: DuoParticle[];
}

/* ── Analysis Frame — full C³ data per frame ──────────────────── */

export interface AnalysisFrame {
  beliefs: { consonance: number; tempo: number; salience: number; familiarity: number; reward: number };
  r3: number[];         // 9 R³ group values [0-1]: A,B,C,D,F,G,H,J,K
  pe: number[];          // 4 prediction errors [0-1]: cons,tempo,sal,fam
  precision: number[];   // 4 precision values [0-1]
  ram: number[];         // 26 RAM region activations [0-1]
  relays: number[];      // 7 relay outputs [0-1]: bch,hmce,snem,mmp,daed_w,daed_l,mpg
}

/* ── Neural Constellation Layout ────────────────────────────────── */
// 26 brain regions, normalized to canvas [0-1] × [0-1]
const RAM_LAYOUT: [number, number][] = [
  // Cortical 12 (upper arc)
  [0.28, 0.14], // 0  A1_HG
  [0.35, 0.11], // 1  STG (hub)
  [0.43, 0.15], // 2  STS
  [0.65, 0.11], // 3  IFG
  [0.74, 0.16], // 4  dlPFC
  [0.58, 0.09], // 5  vmPFC
  [0.50, 0.13], // 6  OFC
  [0.50, 0.06], // 7  ACC
  [0.61, 0.14], // 8  SMA
  [0.71, 0.19], // 9  PMC
  [0.24, 0.18], // 10 AG
  [0.19, 0.22], // 11 TP
  // Subcortical 9 (middle)
  [0.52, 0.39], // 12 VTA
  [0.58, 0.37], // 13 NAcc
  [0.44, 0.37], // 14 caudate
  [0.36, 0.42], // 15 amygdala
  [0.39, 0.47], // 16 hippocampus
  [0.63, 0.41], // 17 putamen
  [0.29, 0.31], // 18 MGB
  [0.50, 0.45], // 19 hypothalamus
  [0.67, 0.35], // 20 insula
  // Brainstem 5 (lower center)
  [0.50, 0.57], // 21 IC
  [0.45, 0.62], // 22 AN
  [0.55, 0.62], // 23 CN
  [0.50, 0.60], // 24 SOC
  [0.50, 0.53], // 25 PAG
];

const RAM_NODE_COLORS: RGB[] = [
  { r: 59, g: 130, b: 246 },  // A1_HG — auditory
  { r: 96, g: 165, b: 250 },  // STG — auditory hub
  { r: 59, g: 130, b: 246 },  // STS
  { r: 168, g: 85, b: 247 },  // IFG — cognitive
  { r: 168, g: 85, b: 247 },  // dlPFC
  { r: 139, g: 92, b: 246 },  // vmPFC
  { r: 168, g: 85, b: 247 },  // OFC
  { r: 192, g: 132, b: 252 }, // ACC
  { r: 132, g: 204, b: 22 },  // SMA — motor
  { r: 132, g: 204, b: 22 },  // PMC
  { r: 139, g: 92, b: 246 },  // AG
  { r: 168, g: 85, b: 247 },  // TP
  { r: 251, g: 191, b: 36 },  // VTA — reward
  { r: 251, g: 191, b: 36 },  // NAcc
  { r: 220, g: 170, b: 40 },  // caudate
  { r: 236, g: 72, b: 153 },  // amygdala — emotion
  { r: 56, g: 189, b: 248 },  // hippocampus — memory
  { r: 132, g: 204, b: 22 },  // putamen — motor
  { r: 59, g: 130, b: 246 },  // MGB — auditory
  { r: 236, g: 72, b: 153 },  // hypothalamus
  { r: 236, g: 72, b: 153 },  // insula
  { r: 148, g: 163, b: 184 }, // IC
  { r: 120, g: 140, b: 170 }, // AN
  { r: 120, g: 140, b: 170 }, // CN
  { r: 120, g: 140, b: 170 }, // SOC
  { r: 148, g: 163, b: 184 }, // PAG
];

const RAM_CONN_EDGES: [number, number][] = [
  [21, 18], [18, 1], [18, 0],
  [0, 1], [1, 2], [2, 16],
  [1, 8], [8, 17],
  [16, 1], [16, 3],
  [12, 13], [13, 14], [12, 6],
  [1, 3], [3, 9],
  [7, 4], [7, 5], [15, 6],
  [20, 7], [10, 2], [11, 15],
  [19, 15], [6, 5],
];

const RELAY_PATHS: { relayIdx: number; segments: [number, number][]; color: RGB }[] = [
  { relayIdx: 0, segments: [[21, 18], [18, 1]], color: { r: 192, g: 132, b: 252 } },
  { relayIdx: 1, segments: [[0, 1], [1, 2]], color: { r: 249, g: 115, b: 22 } },
  { relayIdx: 2, segments: [[1, 8], [8, 17]], color: { r: 132, g: 204, b: 22 } },
  { relayIdx: 3, segments: [[16, 1], [16, 3]], color: { r: 56, g: 189, b: 248 } },
  { relayIdx: 4, segments: [[12, 13], [13, 14]], color: { r: 251, g: 191, b: 36 } },
  { relayIdx: 5, segments: [[12, 13]], color: { r: 251, g: 221, b: 100 } },
  { relayIdx: 6, segments: [[1, 3], [3, 9]], color: { r: 236, g: 72, b: 153 } },
];

const R3_GLOW_COLORS: RGB[] = [
  { r: 192, g: 132, b: 252 }, // A consonance
  { r: 239, g: 68, b: 68 },   // B energy
  { r: 6, g: 182, b: 212 },   // C timbre
  { r: 249, g: 115, b: 22 },  // D change
  { r: 139, g: 92, b: 246 },  // F pitch
  { r: 132, g: 204, b: 22 },  // G rhythm
  { r: 59, g: 130, b: 246 },  // H harmony
  { r: 236, g: 72, b: 153 },  // J ext_timbre
  { r: 251, g: 191, b: 36 },  // K modulation
];

// PE burst color per belief
const PE_COLORS: RGB[] = [
  { r: 192, g: 132, b: 252 }, // consonance PE
  { r: 249, g: 115, b: 22 },  // tempo PE
  { r: 132, g: 204, b: 22 },  // salience PE
  { r: 56, g: 189, b: 248 },  // familiarity PE
];

interface RelayFlowDot {
  pathIdx: number;
  segIdx: number;
  progress: number;
  speed: number;
}

/* ── DuoOrganism Config ───────────────────────────────────────── */
export interface DuoOrganismConfig {
  width: number;
  height: number;
}

/* ── Main Class ───────────────────────────────────────────────── */
export class DuoOrganism {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private bloomCanvas: HTMLCanvasElement;
  private bloomCtx: CanvasRenderingContext2D;
  private noiseA: NoiseField;
  private noiseB: NoiseField;
  private particles: DuoParticle[] = [];
  private effects: GameEffect[] = [];
  private t = 0;
  private animId = 0;
  private alive = true;

  // Parameters: [0-1] x4 each
  private emoParams = [0.5, 0.5, 0.5, 0.5];
  private physParams = [0.5, 0.5, 0.5, 0.5];

  // Session timeline
  private sessionTime = 0;
  private phase: "emergence" | "exploration" | "contact" | "flow" | "crescendo" | "peak" | "resolution" = "emergence";

  // Performance
  private readonly MAX_PARTICLES = 6000;
  private lastFrame = 0;

  // ── Analysis data integration ──
  private analysisFrame: AnalysisFrame | null = null;
  private dataIntensity: number | null = null;
  private prevPeValues = [0, 0, 0, 0];
  private peCooldown = 0;
  private prevReward = 0;
  private rewardPulseCooldown = 0;
  private relayFlows: RelayFlowDot[] = [];
  private constellationBreath = 0;

  constructor(canvas: HTMLCanvasElement) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d", { alpha: false })!;
    this.bloomCanvas = document.createElement("canvas");
    this.bloomCtx = this.bloomCanvas.getContext("2d")!;
    this.noiseA = new NoiseField(42);
    this.noiseB = new NoiseField(137);
  }

  /* ── Public API ─────────────────────────────────────────────── */

  start() {
    this.alive = true;
    this.t = 0;
    this.sessionTime = 0;
    this.particles = [];
    this.effects = [];
    this.relayFlows = [];
    this.lastFrame = performance.now();
    this.loop();
  }

  stop() {
    this.alive = false;
    cancelAnimationFrame(this.animId);
  }

  resize(w: number, h: number) {
    const dpr = Math.min(window.devicePixelRatio, 2);
    this.canvas.width = w * dpr;
    this.canvas.height = h * dpr;
    this.bloomCanvas.width = w * dpr;
    this.bloomCanvas.height = h * dpr;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.bloomCtx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }

  updateParams(emotional: number[], physical: number[]) {
    this.emoParams = emotional.map(v => Math.max(0, Math.min(1, v)));
    this.physParams = physical.map(v => Math.max(0, Math.min(1, v)));
  }

  /** Set full analysis frame — drives all data-driven visuals */
  setAnalysisFrame(frame: AnalysisFrame) {
    this.analysisFrame = frame;

    // Derive 8 params from beliefs + r3 + relays
    this.emoParams = [
      frame.beliefs.consonance,     // valence
      frame.beliefs.salience,        // arousal
      frame.beliefs.familiarity,     // depth
      frame.relays[3],               // nostalgia (mmp_familiarity)
    ];
    this.physParams = [
      frame.beliefs.tempo,           // tempo
      frame.r3[1],                   // energy (B_energy)
      frame.r3[3],                   // dynamics (D_change)
      frame.relays[0],               // density (bch)
    ];

    // Data-driven intensity: reward + salience + energy composite
    const reward = frame.beliefs.reward;
    const salience = frame.beliefs.salience;
    const energy = frame.r3[1];
    this.dataIntensity = Math.max(0.15, Math.min(1.0,
      0.2 + reward * 2.5 + salience * 0.6 + energy * 0.3
    ));
  }

  addEffect(effect: GameEffect) {
    this.effects.push(effect);
  }

  pulseRing(color: RGB = RESONANCE_COLOR, strength = 1) {
    const w = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const h = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    this.effects.push({
      type: "ring", x: w / 2, y: h / 2,
      age: 0, maxAge: 0.8, color, strength,
    });
  }

  burst(x: number, y: number, count: number, color: RGB) {
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 40 + Math.random() * 120;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1, maxLife: 0.3 + Math.random() * 0.7,
        size: 2 + Math.random() * 6,
        color,
        stream: "effect",
      });
    }
  }

  flash(color: RGB = { r: 255, g: 255, b: 255 }, strength = 0.3) {
    const w = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const h = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    this.effects.push({
      type: "flash", x: w / 2, y: h / 2,
      age: 0, maxAge: 0.15, color, strength,
    });
  }

  floatXP(x: number, y: number, text: string, color: RGB = RESONANCE_COLOR) {
    this.effects.push({
      type: "xp", x, y,
      age: 0, maxAge: 1.8, value: text, color, strength: 1,
    });
  }

  /* ── Animation Loop ─────────────────────────────────────────── */

  private loop = () => {
    if (!this.alive) return;
    const now = performance.now();
    const dt = Math.min((now - this.lastFrame) / 1000, 0.05);
    this.lastFrame = now;
    this.t += dt;
    this.sessionTime += dt;
    this.constellationBreath += dt;
    this.updatePhase();
    this.handleAnalysisEffects(dt);
    this.updateRelayFlows(dt);
    this.spawnParticles(dt);
    this.updateParticles(dt);
    this.updateEffects(dt);
    this.render();
    this.animId = requestAnimationFrame(this.loop);
  };

  /* ── Phase Management ───────────────────────────────────────── */

  private updatePhase() {
    const s = this.sessionTime;
    if (s < 5) this.phase = "emergence";
    else if (s < 15) this.phase = "exploration";
    else if (s < 30) this.phase = "contact";
    else if (s < 60) this.phase = "flow";
    else if (s < 90) this.phase = "crescendo";
    else if (s < 110) this.phase = "peak";
    else this.phase = "resolution";
  }

  private get phaseIntensity(): number {
    // Data-driven intensity overrides timeline when analysis data is present
    if (this.dataIntensity !== null) return this.dataIntensity;

    switch (this.phase) {
      case "emergence": return this.sessionTime / 5 * 0.3;
      case "exploration": return 0.3 + (this.sessionTime - 5) / 10 * 0.2;
      case "contact": return 0.5 + (this.sessionTime - 15) / 15 * 0.15;
      case "flow": return 0.65 + (this.sessionTime - 30) / 30 * 0.15;
      case "crescendo": return 0.8 + (this.sessionTime - 60) / 30 * 0.15;
      case "peak": return 0.95 + (this.sessionTime - 90) / 20 * 0.05;
      case "resolution": return 1.0 - (this.sessionTime - 110) / 10 * 0.5;
      default: return 0.5;
    }
  }

  /* ── Analysis-Driven Effects ─────────────────────────────────── */

  private handleAnalysisEffects(dt: number) {
    if (!this.analysisFrame) return;

    const W = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const H = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    const af = this.analysisFrame;

    // Cooldowns
    this.peCooldown = Math.max(0, this.peCooldown - dt);
    this.rewardPulseCooldown = Math.max(0, this.rewardPulseCooldown - dt);

    // PE burst detection — spike in prediction error triggers particle burst
    const pe = af.pe;
    for (let i = 0; i < 4; i++) {
      const delta = pe[i] - this.prevPeValues[i];
      if (delta > 0.06 && this.peCooldown <= 0 && pe[i] > 0.15) {
        const burstCount = Math.floor(10 + delta * 100);
        const bx = W * (0.35 + Math.random() * 0.3);
        const by = H * (0.35 + Math.random() * 0.3);
        this.burst(bx, by, burstCount, PE_COLORS[i]);

        // Big PE spikes also create ring pulse
        if (delta > 0.12) {
          this.pulseRing(PE_COLORS[i], 0.6 + delta * 2);
        }
        this.peCooldown = 0.25;
      }
    }
    this.prevPeValues = [...pe];

    // Reward pulse — positive reward surge triggers gold ring
    const reward = af.beliefs.reward;
    const rewardDelta = reward - this.prevReward;
    if (rewardDelta > 0.015 && this.rewardPulseCooldown <= 0 && reward > 0.1) {
      this.pulseRing(RESONANCE_COLOR, 0.4 + reward * 2);
      if (rewardDelta > 0.03) {
        this.flash(RESONANCE_COLOR, 0.08 + rewardDelta * 2);
      }
      this.rewardPulseCooldown = 0.5;
    }
    this.prevReward = reward;

    // Spawn relay flow particles based on relay output magnitudes
    for (const rp of RELAY_PATHS) {
      const relayVal = af.relays[rp.relayIdx] ?? 0;
      if (relayVal > 0.05 && Math.random() < relayVal * dt * 8) {
        const segIdx = Math.floor(Math.random() * rp.segments.length);
        this.relayFlows.push({
          pathIdx: RELAY_PATHS.indexOf(rp),
          segIdx,
          progress: 0,
          speed: 0.3 + relayVal * 1.5,
        });
      }
    }
  }

  /* ── Relay Flow Particle Update ──────────────────────────────── */

  private updateRelayFlows(dt: number) {
    for (let i = this.relayFlows.length - 1; i >= 0; i--) {
      const f = this.relayFlows[i];
      f.progress += f.speed * dt;
      if (f.progress >= 1.0) {
        // Move to next segment or remove
        const path = RELAY_PATHS[f.pathIdx];
        if (f.segIdx < path.segments.length - 1) {
          f.segIdx++;
          f.progress = 0;
        } else {
          this.relayFlows.splice(i, 1);
        }
      }
    }
    // Cap relay flow particles
    if (this.relayFlows.length > 200) {
      this.relayFlows.splice(0, this.relayFlows.length - 200);
    }
  }

  /* ── Particle Spawning ──────────────────────────────────────── */

  private spawnParticles(dt: number) {
    if (this.particles.length >= this.MAX_PARTICLES) return;

    const W = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const H = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    const intensity = this.phaseIntensity;
    const af = this.analysisFrame;

    // R³ color modulation: weight palette by R3 group activity
    const r3Warmth = af ? (af.r3[0] * 0.3 + af.r3[1] * 0.3 + af.r3[3] * 0.4) : 0.5;
    const r3Richness = af ? (af.r3[2] * 0.4 + af.r3[7] * 0.3 + af.r3[4] * 0.3) : 0.5;

    // Stream A — emotional (from bottom-right)
    const emoRate = (8 + this.emoParams[1] * 30) * intensity;
    const emoCount = Math.floor(emoRate * dt + (Math.random() < (emoRate * dt % 1) ? 1 : 0));
    for (let i = 0; i < emoCount; i++) {
      const angle = Math.PI + Math.random() * Math.PI / 2;
      const speed = 15 + this.emoParams[1] * 60;
      const colorIdx = Math.floor(Math.random() * 4);
      const baseColor = EMO_PALETTE[colorIdx];
      const val = this.emoParams[0];
      const color = {
        r: Math.round(baseColor.r * (0.5 + val * 0.5) * (0.7 + r3Warmth * 0.6)),
        g: Math.round(Math.min(255, baseColor.g * (0.3 + val * 0.7))),
        b: Math.round(Math.min(255, baseColor.b * (1.3 - val * 0.5) * (0.7 + r3Richness * 0.6))),
      };
      const depth = this.emoParams[2];
      const nostalgia = this.emoParams[3];
      this.particles.push({
        x: W * (0.7 + Math.random() * 0.3),
        y: H * (0.7 + Math.random() * 0.3),
        vx: Math.cos(angle) * speed * (0.5 + Math.random()),
        vy: Math.sin(angle) * speed * (0.5 + Math.random()),
        life: 1,
        maxLife: 3 + depth * 5 + Math.random() * 2,
        size: 1.5 + depth * 4 + Math.random() * 2,
        color,
        stream: "A",
        trail: nostalgia > 0.3 ? [] : undefined,
      });
    }

    // Stream B — physical (from top-left)
    const physRate = (8 + this.physParams[3] * 30) * intensity;
    const physCount = Math.floor(physRate * dt + (Math.random() < (physRate * dt % 1) ? 1 : 0));
    for (let i = 0; i < physCount; i++) {
      const angle = Math.random() * Math.PI / 2;
      const tempo = this.physParams[0];
      const speed = 20 + tempo * 80;
      const colorIdx = Math.floor(Math.random() * 4);
      const baseColor = PHYS_PALETTE[colorIdx];
      const energy = this.physParams[1];
      const color = {
        r: Math.round(Math.min(255, baseColor.r * (0.6 + energy * 0.4) * (0.8 + r3Warmth * 0.4))),
        g: Math.round(Math.min(255, baseColor.g * (0.6 + energy * 0.4))),
        b: Math.round(Math.min(255, baseColor.b * (0.6 + energy * 0.4) * (0.8 + r3Richness * 0.4))),
      };
      const dynamics = this.physParams[2];
      this.particles.push({
        x: W * (Math.random() * 0.3),
        y: H * (Math.random() * 0.3),
        vx: Math.cos(angle) * speed * (0.5 + Math.random()),
        vy: Math.sin(angle) * speed * (0.5 + Math.random()),
        life: 1,
        maxLife: 1 + (1 - tempo) * 3 + Math.random(),
        size: 1 + dynamics * 3 + Math.random(),
        color,
        stream: "B",
      });
    }

    // Resonance sparks — center zone, gated by phase or data intensity
    const canResonance = this.dataIntensity !== null ? this.dataIntensity > 0.3 : (this.phase !== "emergence" && this.phase !== "exploration");
    if (canResonance) {
      const resonanceStrength = this.getResonanceStrength();
      // Reward amplifies resonance
      const rewardBoost = af ? 1 + af.beliefs.reward * 3 : 1;
      const sparkRate = resonanceStrength * 15 * intensity * rewardBoost;
      const sparkCount = Math.floor(sparkRate * dt + (Math.random() < (sparkRate * dt % 1) ? 1 : 0));
      for (let i = 0; i < sparkCount; i++) {
        const cx = W / 2 + (Math.random() - 0.5) * W * 0.3;
        const cy = H / 2 + (Math.random() - 0.5) * H * 0.3;
        const angle = Math.random() * Math.PI * 2;
        this.particles.push({
          x: cx, y: cy,
          vx: Math.cos(angle) * (10 + Math.random() * 30),
          vy: Math.sin(angle) * (10 + Math.random() * 30),
          life: 1,
          maxLife: 0.5 + Math.random() * 1.5,
          size: 1 + Math.random() * 3,
          color: { ...RESONANCE_COLOR },
          stream: "resonance",
        });
      }
    }
  }

  getResonanceStrength(): number {
    let sync = 0;
    for (let i = 0; i < 4; i++) {
      sync += 1 - Math.abs(this.emoParams[i] - this.physParams[i]);
    }
    return (sync / 4) * this.phaseIntensity;
  }

  /* ── Particle Physics ───────────────────────────────────────── */

  private updateParticles(dt: number) {
    const W = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const H = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    const cx = W / 2, cy = H / 2;

    // PE-driven turbulence: high PE → more chaotic flow
    const peTurb = this.analysisFrame
      ? (this.analysisFrame.pe[0] + this.analysisFrame.pe[1] + this.analysisFrame.pe[2] + this.analysisFrame.pe[3]) / 4
      : 0;

    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.life -= dt / p.maxLife;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      if (p.trail) {
        p.trail.push({ x: p.x, y: p.y });
        if (p.trail.length > 16) p.trail.shift(); // longer trails with nostalgia
      }

      if (p.stream === "effect") {
        p.vx *= 0.95;
        p.vy *= 0.95;
        p.x += p.vx * dt;
        p.y += p.vy * dt;
        continue;
      }

      const noiseScale = 0.003;
      const noiseTime = this.t * 0.3;
      let nx: number, ny: number;

      if (p.stream === "A") {
        const n = this.noiseA.fbm(p.x * noiseScale, p.y * noiseScale + noiseTime, 3);
        const angle = n * Math.PI * (4 + peTurb * 4); // PE increases turbulence
        nx = Math.cos(angle) * (40 + peTurb * 30);
        ny = Math.sin(angle) * (40 + peTurb * 30);
        const dx = cx - p.x, dy = cy - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy) + 1;
        nx += (dx / dist) * 8 * this.phaseIntensity;
        ny += (dy / dist) * 8 * this.phaseIntensity;
      } else if (p.stream === "B") {
        const n = this.noiseB.noise2D(p.x * noiseScale * 2, p.y * noiseScale * 2 + noiseTime * 0.5);
        const tempo = this.physParams[0];
        const pulsePhase = Math.sin(this.t * (1 + tempo * 4));
        nx = n * (30 + peTurb * 20) + pulsePhase * 15;
        ny = n * (30 + peTurb * 20) + Math.cos(this.t * 0.7) * 10;
        const dx = cx - p.x, dy = cy - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy) + 1;
        nx += (dx / dist) * 10 * this.phaseIntensity;
        ny += (dy / dist) * 10 * this.phaseIntensity;
      } else {
        nx = (Math.random() - 0.5) * 20;
        ny = (Math.random() - 0.5) * 20;
      }

      p.vx = p.vx * 0.92 + nx * dt;
      p.vy = p.vy * 0.92 + ny * dt;
      p.x += p.vx * dt;
      p.y += p.vy * dt;

      if (p.x < -20 || p.x > W + 20 || p.y < -20 || p.y > H + 20) {
        p.life = 0;
      }
    }
  }

  /* ── Effects Update ─────────────────────────────────────────── */

  private updateEffects(dt: number) {
    for (let i = this.effects.length - 1; i >= 0; i--) {
      const e = this.effects[i];
      e.age += dt;
      if (e.age >= e.maxAge) {
        this.effects.splice(i, 1);
      }
    }
  }

  /* ── Render ─────────────────────────────────────────────────── */

  private render() {
    const W = this.canvas.width / (Math.min(window.devicePixelRatio, 2));
    const H = this.canvas.height / (Math.min(window.devicePixelRatio, 2));
    const ctx = this.ctx;

    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, W, H);

    // L0: Ambient glow (R³-modulated if data present)
    this.renderAmbientGlow(ctx, W, H);

    // L0.5: Neural constellation (26 brain regions + edges)
    if (this.analysisFrame) {
      this.renderConstellation(ctx, W, H);
    }

    // L1: Brain wave overlay (precision-modulated)
    if (this.analysisFrame) {
      this.renderBrainWaves(ctx, W, H);
    }

    // L2-L3: Particles (all streams)
    this.renderParticles(ctx, W, H);

    // L3.5: Relay flow particles
    if (this.analysisFrame && this.relayFlows.length > 0) {
      this.renderRelayFlows(ctx, W, H);
    }

    // L4: Resonance aurora (reward-modulated)
    const canAurora = this.dataIntensity !== null ? this.dataIntensity > 0.2 : (this.phase !== "emergence");
    if (canAurora) {
      this.renderResonanceAurora(ctx, W, H);
    }

    // L5: Game effects
    this.renderEffects(ctx, W, H);

    // L6: Bloom post-process (precision-driven)
    this.renderBloom(W, H);
  }

  /* ── L0: Ambient Glow ───────────────────────────────────────── */

  private renderAmbientGlow(ctx: CanvasRenderingContext2D, W: number, H: number) {
    const intensity = this.phaseIntensity;
    const breath = 0.5 + 0.5 * Math.sin(this.t * Math.PI * 2 / 4);
    const af = this.analysisFrame;

    if (af) {
      // R³-modulated multi-zone ambient glow — 9 radial sectors
      const cx = W / 2, cy = H / 2;
      const maxR = W * 0.6;
      for (let g = 0; g < 9; g++) {
        const val = af.r3[g];
        if (val < 0.05) continue;

        const angle = (g / 9) * Math.PI * 2 - Math.PI / 2;
        const gx = cx + Math.cos(angle) * maxR * 0.3;
        const gy = cy + Math.sin(angle) * maxR * 0.3;
        const glowR = maxR * (0.3 + val * 0.4);
        const c = R3_GLOW_COLORS[g];
        const alpha = (0.02 + val * 0.04 + breath * 0.01) * intensity;

        const grad = ctx.createRadialGradient(gx, gy, 0, gx, gy, glowR);
        grad.addColorStop(0, `rgba(${c.r},${c.g},${c.b},${alpha})`);
        grad.addColorStop(0.6, `rgba(${c.r},${c.g},${c.b},${alpha * 0.3})`);
        grad.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, W, H);
      }

      // Reward aurora glow — center, modulated by reward
      const reward = af.beliefs.reward;
      if (reward > 0.05) {
        const resAlpha = reward * 0.15 * intensity;
        const resGrad = ctx.createRadialGradient(cx, cy, 0, cx, cy, W * 0.4);
        resGrad.addColorStop(0, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},${resAlpha})`);
        resGrad.addColorStop(0.5, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},${resAlpha * 0.4})`);
        resGrad.addColorStop(1, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},0)`);
        ctx.fillStyle = resGrad;
        ctx.fillRect(0, 0, W, H);
      }
    } else {
      // Fallback: original 2-zone glow
      const emoAlpha = (0.06 + breath * 0.04) * intensity;
      const emoGrad = ctx.createRadialGradient(W * 0.75, H * 0.75, 0, W * 0.75, H * 0.75, W * 0.5);
      const ec = EMO_PALETTE[0];
      emoGrad.addColorStop(0, `rgba(${ec.r},${ec.g},${ec.b},${emoAlpha})`);
      emoGrad.addColorStop(1, `rgba(${ec.r},${ec.g},${ec.b},0)`);
      ctx.fillStyle = emoGrad;
      ctx.fillRect(0, 0, W, H);

      const physAlpha = (0.05 + breath * 0.03) * intensity;
      const physGrad = ctx.createRadialGradient(W * 0.25, H * 0.25, 0, W * 0.25, H * 0.25, W * 0.5);
      const pc = PHYS_PALETTE[2];
      physGrad.addColorStop(0, `rgba(${pc.r},${pc.g},${pc.b},${physAlpha})`);
      physGrad.addColorStop(1, `rgba(${pc.r},${pc.g},${pc.b},0)`);
      ctx.fillStyle = physGrad;
      ctx.fillRect(0, 0, W, H);

      const res = this.getResonanceStrength();
      if (res > 0.2) {
        const resAlpha = (res - 0.2) * 0.12 * intensity;
        const resGrad = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.35);
        resGrad.addColorStop(0, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},${resAlpha})`);
        resGrad.addColorStop(1, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},0)`);
        ctx.fillStyle = resGrad;
        ctx.fillRect(0, 0, W, H);
      }
    }
  }

  /* ── L0.5: Neural Constellation ──────────────────────────────── */

  private renderConstellation(ctx: CanvasRenderingContext2D, W: number, H: number) {
    const af = this.analysisFrame!;
    const ram = af.ram;
    const breathPhase = Math.sin(this.constellationBreath * 1.5) * 0.5 + 0.5;

    ctx.save();

    // Draw edges first (behind nodes)
    for (const [a, b] of RAM_CONN_EDGES) {
      const actA = ram[a] ?? 0;
      const actB = ram[b] ?? 0;
      const avgAct = (actA + actB) / 2;
      if (avgAct < 0.05) continue;

      const ax = RAM_LAYOUT[a][0] * W, ay = RAM_LAYOUT[a][1] * H;
      const bx = RAM_LAYOUT[b][0] * W, by = RAM_LAYOUT[b][1] * H;

      // Blend colors of connected nodes
      const cA = RAM_NODE_COLORS[a], cB = RAM_NODE_COLORS[b];
      const alpha = avgAct * 0.15 * this.phaseIntensity;

      ctx.beginPath();
      ctx.moveTo(ax, ay);
      ctx.lineTo(bx, by);
      ctx.strokeStyle = `rgba(${(cA.r + cB.r) >> 1},${(cA.g + cB.g) >> 1},${(cA.b + cB.b) >> 1},${alpha})`;
      ctx.lineWidth = 0.5 + avgAct * 1.0;
      ctx.stroke();
    }

    // Draw nodes
    for (let i = 0; i < 26; i++) {
      const act = ram[i] ?? 0;
      if (act < 0.02) continue;

      const x = RAM_LAYOUT[i][0] * W;
      const y = RAM_LAYOUT[i][1] * H;
      const c = RAM_NODE_COLORS[i];
      const pulseMod = 0.8 + 0.2 * Math.sin(this.constellationBreath * 2 + i * 0.7);

      // Node glow
      const glowR = 4 + act * 12;
      const glowAlpha = act * 0.3 * pulseMod * this.phaseIntensity;
      const glow = ctx.createRadialGradient(x, y, 0, x, y, glowR);
      glow.addColorStop(0, `rgba(${c.r},${c.g},${c.b},${glowAlpha})`);
      glow.addColorStop(0.5, `rgba(${c.r},${c.g},${c.b},${glowAlpha * 0.4})`);
      glow.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
      ctx.fillStyle = glow;
      ctx.fillRect(x - glowR, y - glowR, glowR * 2, glowR * 2);

      // Node core
      const coreR = 1 + act * 2.5;
      ctx.beginPath();
      ctx.arc(x, y, coreR, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${c.r},${c.g},${c.b},${(0.3 + act * 0.7) * pulseMod})`;
      ctx.fill();

      // Bright center for high activation
      if (act > 0.5) {
        ctx.beginPath();
        ctx.arc(x, y, coreR * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${(act - 0.5) * breathPhase * 0.8})`;
        ctx.fill();
      }
    }

    ctx.restore();
  }

  /* ── L1: Brain Waves (precision-modulated) ───────────────────── */

  private renderBrainWaves(ctx: CanvasRenderingContext2D, W: number, H: number) {
    const af = this.analysisFrame!;
    const avgPrecision = (af.precision[0] + af.precision[1] + af.precision[2] + af.precision[3]) / 4;
    if (avgPrecision < 0.1) return;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    // 4 wave bands, one per belief precision
    const beliefs = ["consonance", "tempo", "salience", "familiarity"] as const;
    const waveColors: RGB[] = [
      { r: 192, g: 132, b: 252 },
      { r: 249, g: 115, b: 22 },
      { r: 132, g: 204, b: 22 },
      { r: 56, g: 189, b: 248 },
    ];

    for (let b = 0; b < 4; b++) {
      const prec = af.precision[b];
      if (prec < 0.15) continue;

      const c = waveColors[b];
      const yBase = H * (0.25 + b * 0.15);
      const alpha = prec * 0.04 * this.phaseIntensity;
      const freq = 2 + b * 0.5;
      const amp = 3 + prec * 8;

      ctx.beginPath();
      for (let x = 0; x < W; x += 2) {
        const wave = Math.sin(x * freq / W * Math.PI * 2 + this.t * (0.8 + b * 0.3)) * amp;
        const harmonic = Math.sin(x * freq * 2.3 / W * Math.PI * 2 + this.t * 1.1) * amp * 0.3;
        const y = yBase + wave + harmonic;
        if (x === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = `rgba(${c.r},${c.g},${c.b},${alpha})`;
      ctx.lineWidth = 1 + prec * 2;
      ctx.stroke();
    }

    ctx.restore();
  }

  /* ── L2-L3: Particles ───────────────────────────────────────── */

  private renderParticles(ctx: CanvasRenderingContext2D, _W: number, _H: number) {
    ctx.save();
    const dynamics = this.physParams[2];

    // Precision-driven rendering: high precision = sharp, low = diffuse
    const avgPrecision = this.analysisFrame
      ? (this.analysisFrame.precision[0] + this.analysisFrame.precision[1] +
         this.analysisFrame.precision[2] + this.analysisFrame.precision[3]) / 4
      : 0.5;
    const sharpness = 0.3 + avgPrecision * 0.7; // 0.3–1.0
    const glowSpread = 2 + (1 - avgPrecision) * 3; // inverse: low prec = more spread

    for (const p of this.particles) {
      const alpha = p.life * (p.stream === "effect" ? 0.9 : 0.7);
      if (alpha <= 0) continue;

      const { r, g, b } = p.color;

      // Trail rendering
      if (p.trail && p.trail.length > 1) {
        ctx.beginPath();
        ctx.moveTo(p.trail[0].x, p.trail[0].y);
        for (let j = 1; j < p.trail.length; j++) {
          ctx.lineTo(p.trail[j].x, p.trail[j].y);
        }
        ctx.lineTo(p.x, p.y);
        ctx.strokeStyle = `rgba(${r},${g},${b},${alpha * 0.3})`;
        ctx.lineWidth = p.size * 0.5;
        ctx.stroke();
      }

      const sz = p.size * (p.stream === "effect" ? p.life : 1);

      // Outer glow — spread modulated by precision
      if (sz > 1.5) {
        const glowR = sz * glowSpread;
        const glow = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, glowR);
        glow.addColorStop(0, `rgba(${r},${g},${b},${alpha * 0.25 * (1.2 - sharpness * 0.4)})`);
        glow.addColorStop(1, `rgba(${r},${g},${b},0)`);
        ctx.fillStyle = glow;
        ctx.fillRect(p.x - glowR, p.y - glowR, glowR * 2, glowR * 2);
      }

      // Core — opacity modulated by precision (high prec = brighter core)
      ctx.beginPath();
      ctx.arc(p.x, p.y, sz * sharpness, 0, Math.PI * 2);
      const coreAlpha = p.stream === "B"
        ? alpha * (0.6 + dynamics * 0.4) * sharpness
        : alpha * 0.6 * sharpness;
      ctx.fillStyle = `rgba(${r},${g},${b},${coreAlpha})`;
      ctx.fill();

      // Specular highlight (resonance + high precision)
      if (p.stream === "resonance" && sz > 1) {
        ctx.beginPath();
        ctx.arc(p.x - sz * 0.2, p.y - sz * 0.2, sz * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${alpha * 0.4 * sharpness})`;
        ctx.fill();
      }
    }
    ctx.restore();
  }

  /* ── L3.5: Relay Flow Particles ──────────────────────────────── */

  private renderRelayFlows(ctx: CanvasRenderingContext2D, W: number, H: number) {
    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    for (const f of this.relayFlows) {
      const path = RELAY_PATHS[f.pathIdx];
      const seg = path.segments[f.segIdx];
      if (!seg) continue;

      const ax = RAM_LAYOUT[seg[0]][0] * W;
      const ay = RAM_LAYOUT[seg[0]][1] * H;
      const bx = RAM_LAYOUT[seg[1]][0] * W;
      const by = RAM_LAYOUT[seg[1]][1] * H;

      const x = ax + (bx - ax) * f.progress;
      const y = ay + (by - ay) * f.progress;
      const c = path.color;

      // Flow dot with glow
      const dotR = 2 + (this.analysisFrame?.relays[path.relayIdx] ?? 0) * 3;
      const alpha = 0.6 * (1 - Math.abs(f.progress - 0.5) * 0.6);

      const glow = ctx.createRadialGradient(x, y, 0, x, y, dotR * 3);
      glow.addColorStop(0, `rgba(${c.r},${c.g},${c.b},${alpha * 0.5})`);
      glow.addColorStop(1, `rgba(${c.r},${c.g},${c.b},0)`);
      ctx.fillStyle = glow;
      ctx.fillRect(x - dotR * 3, y - dotR * 3, dotR * 6, dotR * 6);

      ctx.beginPath();
      ctx.arc(x, y, dotR * 0.6, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(${c.r},${c.g},${c.b},${alpha})`;
      ctx.fill();

      // Bright center
      ctx.beginPath();
      ctx.arc(x, y, dotR * 0.2, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${alpha * 0.7})`;
      ctx.fill();
    }

    ctx.restore();
  }

  /* ── L4: Resonance Aurora ───────────────────────────────────── */

  private renderResonanceAurora(ctx: CanvasRenderingContext2D, W: number, H: number) {
    const res = this.getResonanceStrength();
    // Reward amplifies aurora when analysis data present
    const rewardBoost = this.analysisFrame ? 1 + this.analysisFrame.beliefs.reward * 4 : 1;
    const effectiveRes = Math.min(1, res * rewardBoost);
    if (effectiveRes < 0.1) return;

    ctx.save();
    ctx.globalCompositeOperation = "lighter";

    const bandCount = 3 + Math.floor(effectiveRes * 5);
    for (let i = 0; i < bandCount; i++) {
      const yBase = H * 0.35 + (H * 0.3) * (i / bandCount);
      const wave = Math.sin(this.t * 0.8 + i * 1.5) * H * 0.04;
      const y = yBase + wave;
      const bandH = 2 + effectiveRes * 10;
      const alpha = (0.03 + effectiveRes * 0.07) * (1 - Math.abs(i - bandCount / 2) / (bandCount / 2));

      const grad = ctx.createLinearGradient(W * 0.15, y, W * 0.85, y);
      const ec = EMO_PALETTE[i % 4];
      const pc = PHYS_PALETTE[i % 4];
      grad.addColorStop(0, `rgba(${ec.r},${ec.g},${ec.b},0)`);
      grad.addColorStop(0.25, `rgba(${ec.r},${ec.g},${ec.b},${alpha})`);
      grad.addColorStop(0.5, `rgba(${RESONANCE_COLOR.r},${RESONANCE_COLOR.g},${RESONANCE_COLOR.b},${alpha * 1.5})`);
      grad.addColorStop(0.75, `rgba(${pc.r},${pc.g},${pc.b},${alpha})`);
      grad.addColorStop(1, `rgba(${pc.r},${pc.g},${pc.b},0)`);

      ctx.fillStyle = grad;
      ctx.fillRect(0, y - bandH / 2, W, bandH);
    }

    ctx.restore();
  }

  /* ── L5: Game Effects ───────────────────────────────────────── */

  private renderEffects(ctx: CanvasRenderingContext2D, W: number, H: number) {
    for (const e of this.effects) {
      const progress = e.age / e.maxAge;
      const { r, g, b } = e.color;

      switch (e.type) {
        case "ring": {
          const radius = W * 0.4 * progress;
          const alpha = (1 - progress) * e.strength * 0.5;
          ctx.save();
          ctx.globalCompositeOperation = "lighter";
          ctx.beginPath();
          ctx.arc(e.x, e.y, radius, 0, Math.PI * 2);
          ctx.strokeStyle = `rgba(${r},${g},${b},${alpha})`;
          ctx.lineWidth = 2 + (1 - progress) * 4;
          ctx.stroke();
          const glow = ctx.createRadialGradient(e.x, e.y, radius * 0.9, e.x, e.y, radius * 1.1);
          glow.addColorStop(0, `rgba(${r},${g},${b},0)`);
          glow.addColorStop(0.5, `rgba(${r},${g},${b},${alpha * 0.3})`);
          glow.addColorStop(1, `rgba(${r},${g},${b},0)`);
          ctx.fillStyle = glow;
          ctx.fillRect(0, 0, W, H);
          ctx.restore();
          break;
        }

        case "flash": {
          const alpha = (1 - progress) * e.strength;
          ctx.save();
          ctx.globalCompositeOperation = "lighter";
          ctx.fillStyle = `rgba(${r},${g},${b},${alpha})`;
          ctx.fillRect(0, 0, W, H);
          ctx.restore();
          break;
        }

        case "xp": {
          const alpha = progress < 0.2 ? progress / 0.2 : 1 - (progress - 0.2) / 0.8;
          const y = e.y - progress * 40;
          ctx.save();
          ctx.font = "bold 12px 'Space Grotesk', monospace";
          ctx.textAlign = "center";
          ctx.fillStyle = `rgba(${r},${g},${b},${alpha * 0.9})`;
          ctx.shadowColor = `rgba(${r},${g},${b},0.5)`;
          ctx.shadowBlur = 8;
          ctx.fillText(e.value ?? "+XP", e.x, y);
          ctx.restore();
          break;
        }
      }
    }
  }

  /* ── L6: Bloom Post-Process ─────────────────────────────────── */

  private renderBloom(W: number, H: number) {
    const bloomCtx = this.bloomCtx;
    bloomCtx.clearRect(0, 0, W, H);
    bloomCtx.drawImage(this.canvas, 0, 0, W, H);

    // Precision modulates bloom: low precision = more blur, high = sharper
    const precBlur = this.analysisFrame
      ? Math.round(6 + (1 - (this.analysisFrame.precision[0] + this.analysisFrame.precision[1]) / 2) * 6)
      : 8;
    const precBright = this.analysisFrame
      ? 1.1 + this.analysisFrame.beliefs.reward * 0.6
      : 1.3;

    bloomCtx.filter = `blur(${precBlur}px) brightness(${precBright.toFixed(2)})`;
    bloomCtx.drawImage(this.bloomCanvas, 0, 0, W, H);
    bloomCtx.filter = "none";

    this.ctx.save();
    this.ctx.globalCompositeOperation = "lighter";
    this.ctx.globalAlpha = 0.12 + this.phaseIntensity * 0.08;
    this.ctx.drawImage(this.bloomCanvas, 0, 0, W, H);
    this.ctx.restore();
  }
}
