/* ── MindVisualizerCanvas — 15-Tendril Radial Visualization ──────────
 *  Imperative Canvas 2D engine that renders 15 parameters (5 C³ + 10 R³)
 *  as an organic radial visualization synchronized with audio.
 *
 *  Layout: 15 tendrils arranged radially, alternating C³/R³:
 *    C3→R3→R3→C3→R3→R3→C3→R3→R3→C3→R3→R3→C3→R3→R3
 *
 *  C³ tendrils: thick, colored by beliefColors, connected by cognitive web.
 *  R³ tendrils: thinner, muted, interspersed between C³ ones.
 *  Central breathing core, ambient particles, slow rotation.
 *
 *  Follows mind-organism.ts pattern (class with start/stop/dispose).
 *  ──────────────────────────────────────────────────────────────── */

import type { MindVisualizerParams } from "@/services/AudioAnalyzer";

/* ── Constants ───────────────────────────────────────────────── */

/** C³ colors matching beliefColors from tokens.ts */
const C3_COLORS: RGB[] = [
  { r: 192, g: 132, b: 252 }, // harmonicConsonance — purple
  { r: 56, g: 189, b: 248 },  // rhythmicSync — cyan
  { r: 251, g: 191, b: 36 },  // patternPredictability — amber
  { r: 132, g: 204, b: 22 },  // memoryRecognition — lime
  { r: 236, g: 72, b: 153 },  // wanting — pink
];

const C3_LABELS = [
  "Harmonic Consonance",
  "Rhythmic Sync",
  "Pattern Prediction",
  "Memory Recognition",
  "Wanting",
];

const R3_COLOR: RGB = { r: 148, g: 163, b: 184 }; // slate-400

/** Parameter order — interleaved C3/R3 */
const PARAM_ORDER: { key: keyof MindVisualizerParams; type: "c3" | "r3"; c3Idx?: number }[] = [
  { key: "harmonicConsonance", type: "c3", c3Idx: 0 },
  { key: "roughness", type: "r3" },
  { key: "spectralFlux", type: "r3" },
  { key: "rhythmicSync", type: "c3", c3Idx: 1 },
  { key: "loudness", type: "r3" },
  { key: "keyClarity", type: "r3" },
  { key: "patternPredictability", type: "c3", c3Idx: 2 },
  { key: "onsetStrength", type: "r3" },
  { key: "melodicClarity", type: "r3" },
  { key: "memoryRecognition", type: "c3", c3Idx: 3 },
  { key: "brightness", type: "r3" },
  { key: "tempoStability", type: "r3" },
  { key: "wanting", type: "c3", c3Idx: 4 },
  { key: "tonalness", type: "r3" },
  { key: "grooveStrength", type: "r3" },
];

/* ── Perlin Noise (same as mind-organism.ts) ─────────────────── */

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
}

/* ── Particle ────────────────────────────────────────────────── */

interface Particle {
  x: number; y: number;
  vx: number; vy: number;
  life: number; maxLife: number;
  size: number; color: RGB;
}

/* ── Config ──────────────────────────────────────────────────── */

export interface VisualizerConfig {
  accentColor: string;
  breathRate?: number;
}

/* ── Main Class ──────────────────────────────────────────────── */

export class MindVisualizerEngine {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private noise: NoiseField;
  private time = 0;
  private raf = 0;
  private params: MindVisualizerParams;
  private particles: Particle[] = [];
  private accentRGB: RGB;
  private breathRate: number;
  private rotation = 0;

  constructor(canvas: HTMLCanvasElement, config: VisualizerConfig) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d")!;
    this.noise = new NoiseField(Math.floor(Math.random() * 9999));
    this.accentRGB = hexToRGB(config.accentColor);
    this.breathRate = config.breathRate ?? 5;
    this.params = {
      roughness: 0, spectralFlux: 0, loudness: 0, keyClarity: 0,
      onsetStrength: 0, melodicClarity: 0, brightness: 0,
      tempoStability: 0, tonalness: 0, grooveStrength: 0,
      harmonicConsonance: 0, rhythmicSync: 0, patternPredictability: 0,
      memoryRecognition: 0, wanting: 0,
    };
  }

  /* ── Public API ────────────────────────────── */

  start() {
    let prev = performance.now();
    const loop = (now: number) => {
      const dt = Math.min((now - prev) / 1000, 0.05);
      prev = now;
      this.time += dt;
      this.rotation += dt * 0.055; // ~0.5 RPM
      this.draw(dt);
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  stop() {
    cancelAnimationFrame(this.raf);
  }

  updateParams(params: MindVisualizerParams) {
    this.params = params;
  }

  updateAccentColor(hex: string) {
    this.accentRGB = hexToRGB(hex);
  }

  dispose() {
    this.stop();
    this.particles = [];
  }

  /* ── Drawing ───────────────────────────────── */

  private draw(_dt: number) {
    const ctx = this.ctx;
    const w = this.canvas.width;
    const h = this.canvas.height;
    if (w === 0 || h === 0) return;

    const cx = w / 2;
    const cy = h / 2;
    const R = Math.min(cx, cy) * 0.82;
    const t = this.time;
    const breath = Math.sin(t * Math.PI * 2 / this.breathRate) * 0.5 + 0.5;
    const p = this.params;

    // Overall energy from loudness
    const energy = p.loudness;

    ctx.clearRect(0, 0, w, h);

    // ── 1. Deep ambient glow ───────────────────
    const ambR = R * (1.1 + breath * 0.1 + energy * 0.15);
    const amb = ctx.createRadialGradient(cx, cy, 0, cx, cy, ambR);
    amb.addColorStop(0, rgba(this.accentRGB, 0.05 + energy * 0.04));
    amb.addColorStop(0.5, rgba(this.accentRGB, 0.015));
    amb.addColorStop(1, rgba(this.accentRGB, 0));
    ctx.fillStyle = amb;
    ctx.fillRect(0, 0, w, h);

    // ── 2. Outer boundary ring ─────────────────
    ctx.beginPath();
    for (let i = 0; i <= 120; i++) {
      const a = (i / 120) * Math.PI * 2 + this.rotation;
      const noiseVal = this.noise.noise2D(Math.cos(a) * 2 + t * 0.1, Math.sin(a) * 2 + t * 0.1);
      const r = R * (0.92 + noiseVal * 0.04 + breath * 0.02 + energy * 0.03);
      const px = cx + Math.cos(a) * r;
      const py = cy + Math.sin(a) * r;
      i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
    }
    ctx.closePath();
    ctx.strokeStyle = rgba(this.accentRGB, 0.04 + breath * 0.02);
    ctx.lineWidth = 1;
    ctx.stroke();

    // ── 3. Tendrils — 15 parameter beams ───────
    for (let i = 0; i < PARAM_ORDER.length; i++) {
      const def = PARAM_ORDER[i];
      const value = p[def.key];
      const angle = (i / PARAM_ORDER.length) * Math.PI * 2 + this.rotation;
      const isC3 = def.type === "c3";

      const maxLength = R * (isC3 ? 0.85 : 0.65);
      const length = maxLength * Math.max(0.08, value);
      const baseWidth = isC3 ? 3.5 + energy * 2 : 1.5 + energy * 0.8;

      const color = isC3 ? C3_COLORS[def.c3Idx!] : lerpRGB(R3_COLOR, this.accentRGB, 0.3);
      const alpha = isC3
        ? 0.35 + value * 0.4 + breath * 0.1
        : 0.12 + value * 0.25 + breath * 0.05;

      // Draw tendril as bezier curve with noise displacement
      ctx.beginPath();
      const segments = 30;
      for (let s = 0; s <= segments; s++) {
        const frac = s / segments;
        const r = R * 0.06 + (length - R * 0.06) * frac;

        const nx = this.noise.noise2D(
          Math.cos(angle) * frac * 2.5 + t * 0.3 + i * 10,
          Math.sin(angle) * frac * 2.5 + t * 0.3
        );
        const ny = this.noise.noise2D(
          Math.cos(angle) * frac * 2.5 + 100 + t * 0.3 + i * 10,
          Math.sin(angle) * frac * 2.5 + 100 + t * 0.3
        );

        const displace = (isC3 ? 18 : 10) * frac * (0.5 + energy * 0.5);
        const px = cx + Math.cos(angle) * r + nx * displace;
        const py = cy + Math.sin(angle) * r + ny * displace;
        s === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
      }

      // Width tapers with distance
      ctx.strokeStyle = rgba(color, alpha);
      ctx.lineWidth = baseWidth * (0.8 + breath * 0.2);
      ctx.lineCap = "round";
      ctx.stroke();

      // Glowing tip
      const tipR = R * 0.06 + (length - R * 0.06);
      const tipNx = this.noise.noise2D(Math.cos(angle) * 2.5 + t * 0.3 + i * 10, Math.sin(angle) * 2.5 + t * 0.3);
      const tipNy = this.noise.noise2D(Math.cos(angle) * 2.5 + 100 + t * 0.3 + i * 10, Math.sin(angle) * 2.5 + 100 + t * 0.3);
      const tipDisplace = (isC3 ? 18 : 10) * (0.5 + energy * 0.5);
      const tipX = cx + Math.cos(angle) * tipR + tipNx * tipDisplace;
      const tipY = cy + Math.sin(angle) * tipR + tipNy * tipDisplace;

      const tipSize = isC3 ? 8 + value * 8 + energy * 4 : 4 + value * 4 + energy * 2;
      const tipGlow = ctx.createRadialGradient(tipX, tipY, 0, tipX, tipY, tipSize);
      tipGlow.addColorStop(0, rgba(color, (isC3 ? 0.5 : 0.25) * value * (0.5 + breath * 0.5)));
      tipGlow.addColorStop(1, rgba(color, 0));
      ctx.fillStyle = tipGlow;
      ctx.beginPath();
      ctx.arc(tipX, tipY, tipSize, 0, Math.PI * 2);
      ctx.fill();

      // C³ — tip dot
      if (isC3 && value > 0.05) {
        ctx.beginPath();
        ctx.arc(tipX, tipY, 2 + value * 2, 0, Math.PI * 2);
        ctx.fillStyle = rgba(color, 0.7 + breath * 0.3);
        ctx.fill();
      }
    }

    // ── 4. Cognitive web — connect C³ tips ─────
    const c3Tips: { x: number; y: number; color: RGB; value: number }[] = [];
    for (let i = 0; i < PARAM_ORDER.length; i++) {
      const def = PARAM_ORDER[i];
      if (def.type !== "c3") continue;
      const value = p[def.key];
      const angle = (i / PARAM_ORDER.length) * Math.PI * 2 + this.rotation;
      const maxLength = R * 0.85;
      const length = maxLength * Math.max(0.08, value);
      const tipR = R * 0.06 + (length - R * 0.06);
      const tipNx = this.noise.noise2D(Math.cos(angle) * 2.5 + t * 0.3 + i * 10, Math.sin(angle) * 2.5 + t * 0.3);
      const tipNy = this.noise.noise2D(Math.cos(angle) * 2.5 + 100 + t * 0.3 + i * 10, Math.sin(angle) * 2.5 + 100 + t * 0.3);
      const tipDisplace = 18 * (0.5 + energy * 0.5);
      c3Tips.push({
        x: cx + Math.cos(angle) * tipR + tipNx * tipDisplace,
        y: cy + Math.sin(angle) * tipR + tipNy * tipDisplace,
        color: C3_COLORS[def.c3Idx!],
        value,
      });
    }

    // Draw web lines between adjacent C³ nodes
    ctx.lineWidth = 0.8;
    for (let i = 0; i < c3Tips.length; i++) {
      const a = c3Tips[i];
      const b = c3Tips[(i + 1) % c3Tips.length];
      const avgValue = (a.value + b.value) / 2;
      const webColor = lerpRGB(a.color, b.color, 0.5);
      ctx.beginPath();
      // Curved connection through center-ish point
      const midX = (a.x + b.x) / 2 + (cx - (a.x + b.x) / 2) * 0.2;
      const midY = (a.y + b.y) / 2 + (cy - (a.y + b.y) / 2) * 0.2;
      ctx.moveTo(a.x, a.y);
      ctx.quadraticCurveTo(midX, midY, b.x, b.y);
      ctx.strokeStyle = rgba(webColor, 0.04 + avgValue * 0.06 + breath * 0.02);
      ctx.stroke();
    }

    // ── 5. Particles — emitted from high-energy tips ──
    // Emit from C³ tips proportional to their value
    for (const tip of c3Tips) {
      if (Math.random() < tip.value * 0.06 + energy * 0.02) {
        const angle = Math.random() * Math.PI * 2;
        const speed = 0.2 + Math.random() * 0.8;
        this.particles.push({
          x: tip.x, y: tip.y,
          vx: Math.cos(angle) * speed,
          vy: Math.sin(angle) * speed,
          life: 1, maxLife: 1,
          size: 1 + Math.random() * 1.5,
          color: tip.color,
        });
      }
    }

    // Update and draw particles
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const pt = this.particles[i];
      pt.x += pt.vx;
      pt.y += pt.vy;
      pt.vx *= 0.985;
      pt.vy *= 0.985;
      pt.life -= 0.012;

      if (pt.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      ctx.beginPath();
      ctx.arc(pt.x, pt.y, pt.size * pt.life, 0, Math.PI * 2);
      ctx.fillStyle = rgba(pt.color, pt.life * 0.4);
      ctx.fill();
    }

    // Cap particles
    if (this.particles.length > 80) {
      this.particles = this.particles.slice(-60);
    }

    // ── 6. Central core — breathing nucleus ────
    const coreSize = 6 + breath * 3 + energy * 5;
    const coreGlow = ctx.createRadialGradient(cx, cy, 0, cx, cy, coreSize * 6);
    coreGlow.addColorStop(0, rgba(this.accentRGB, 0.2 + energy * 0.15));
    coreGlow.addColorStop(0.3, rgba(this.accentRGB, 0.06));
    coreGlow.addColorStop(1, rgba(this.accentRGB, 0));
    ctx.fillStyle = coreGlow;
    ctx.beginPath();
    ctx.arc(cx, cy, coreSize * 6, 0, Math.PI * 2);
    ctx.fill();

    // Core dot
    ctx.beginPath();
    ctx.arc(cx, cy, coreSize, 0, Math.PI * 2);
    ctx.fillStyle = rgba(this.accentRGB, 0.6 + breath * 0.2);
    ctx.fill();

    // White highlight
    ctx.beginPath();
    ctx.arc(cx, cy, coreSize * 0.4, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(255,255,255,${0.3 + breath * 0.2})`;
    ctx.fill();

    // ── 7. Energy pulse rings ──────────────────
    if (energy > 0.15) {
      const pulseR = R * 0.15 + R * energy * 0.4 * ((t * 2) % 1);
      const pulseAlpha = 0.03 * energy * (1 - (t * 2) % 1);
      ctx.beginPath();
      ctx.arc(cx, cy, pulseR, 0, Math.PI * 2);
      ctx.strokeStyle = rgba(this.accentRGB, pulseAlpha);
      ctx.lineWidth = 1.5;
      ctx.stroke();
    }

    // ── 8. Bloom composite (soft glow) ─────────
    this.applyBloom(w, h);
  }

  private applyBloom(w: number, h: number) {
    const ctx = this.ctx;
    ctx.save();
    ctx.globalCompositeOperation = "lighter";
    ctx.filter = "blur(8px)";
    ctx.globalAlpha = 0.08;
    ctx.drawImage(this.canvas, 0, 0, w, h);
    ctx.restore();
  }
}

/* ── Color helpers ───────────────────────────────────────────── */

interface RGB { r: number; g: number; b: number }

function hexToRGB(hex: string): RGB {
  if (hex.startsWith("hsl")) return { r: 168, g: 85, b: 247 };
  return {
    r: parseInt(hex.slice(1, 3), 16),
    g: parseInt(hex.slice(3, 5), 16),
    b: parseInt(hex.slice(5, 7), 16),
  };
}

function rgba(c: RGB, a: number): string {
  return `rgba(${Math.round(c.r)},${Math.round(c.g)},${Math.round(c.b)},${Math.max(0, Math.min(1, a))})`;
}

function lerpRGB(a: RGB, b: RGB, t: number): RGB {
  return { r: a.r + (b.r - a.r) * t, g: a.g + (b.g - a.g) * t, b: a.b + (b.b - a.b) * t };
}

export { C3_COLORS, C3_LABELS, PARAM_ORDER };
