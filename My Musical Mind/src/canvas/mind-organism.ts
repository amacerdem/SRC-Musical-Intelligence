/* ── Mind Organism — Bioluminescent Neural Flow Field ─────────── *
 *  Living, breathing neural organism with:                        *
 *  - 5 rendering variants (hero/ambient/micro/trace/glow)         *
 *  - Belief-colored tendrils (5 belief domain gradients)          *
 *  - Constellation connections between nuclei                     *
 *  - Bloom post-processing (soft glow composite)                  *
 *  - Chromatic aberration on outer edges                          *
 *  - Particle emission from nuclei on interaction                 *
 *  - Flowing tendrils following Perlin noise field                 *
 *  - Pulsating nuclei at junctions                                *
 *  - Organic membrane boundary with mouse warp                    *
 *  - highlightBelief / pulse imperative APIs                      *
 *  - Stage 1→2→3 adds complexity                                  *
 * ──────────────────────────────────────────────────────────────── */

export type OrganismVariant = "hero" | "ambient" | "micro" | "trace" | "glow";

export interface OrganismConfig {
  color: string;
  secondaryColor?: string;
  stage: 1 | 2 | 3;
  intensity: number;        // 0-1
  breathRate: number;       // seconds per breath cycle
  responsive: boolean;
  variant: OrganismVariant;
  beliefWeights?: number[]; // [0-1] x5, per-belief prominence
  constellations?: boolean; // draw lines between nuclei
  frozen?: boolean;         // render single frame, no animation loop
  maxParticles?: number;    // performance cap
  bloomEnabled?: boolean;   // opt-out bloom (default: variant-based)
  chromaticEnabled?: boolean; // opt-out chromatic (default: variant-based)
}

/* ── Belief domain colors for tendril coloring ─────────────── */
const BELIEF_COLORS: RGB[] = [
  { r: 192, g: 132, b: 252 },  // consonance — purple
  { r: 249, g: 115, b: 22 },   // tempo — orange
  { r: 132, g: 204, b: 22 },   // salience — lime
  { r: 56, g: 189, b: 248 },   // familiarity — sky
  { r: 251, g: 191, b: 36 },   // reward — amber
];

export { BELIEF_COLORS };

/* ── Perlin-like noise ────────────────────────────────────── */
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

interface Tendril {
  originAngle: number;
  length: number;
  speed: number;
  width: number;
  phase: number;
  amplitude: number;
  beliefIndex: number;
}

interface Nucleus {
  angle: number;
  dist: number;
  baseSize: number;
  phase: number;
  orbit: number;
  beliefIndex: number;
}

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  size: number;
  color: RGB;
}

const defaults: OrganismConfig = {
  color: "#A855F7",
  stage: 1,
  intensity: 0.7,
  breathRate: 4,
  responsive: true,
  variant: "hero",
};

/* ── Variant feature flags ────────────────────────────────── */
interface VariantFlags {
  tendrils: boolean;
  nuclei: boolean;
  nucleiScale: number;    // 0-1, fraction of default count
  particles: boolean;
  particleCap: number;
  membrane: boolean;
  membraneSimple: boolean; // simplified circle instead of noise
  core: boolean;
  bloom: boolean;
  chromatic: boolean;
  energyRings: boolean;
  constellations: boolean;
  mouse: boolean;
  fpsThrottle: number;    // 1 = every frame, 2 = every other frame
}

function getVariantFlags(variant: OrganismVariant, stage: number): VariantFlags {
  switch (variant) {
    case "hero":
      return {
        tendrils: true, nuclei: true, nucleiScale: 1, particles: true,
        particleCap: 100, membrane: true, membraneSimple: false, core: true,
        bloom: stage >= 2, chromatic: stage === 3, energyRings: stage === 3,
        constellations: true, mouse: true, fpsThrottle: 1,
      };
    case "ambient":
      return {
        tendrils: true, nuclei: true, nucleiScale: 0.5, particles: true,
        particleCap: 30, membrane: true, membraneSimple: false, core: true,
        bloom: stage >= 2, chromatic: false, energyRings: false,
        constellations: true, mouse: false, fpsThrottle: 2,
      };
    case "micro":
      return {
        tendrils: false, nuclei: true, nucleiScale: 0.4, particles: false,
        particleCap: 0, membrane: true, membraneSimple: true, core: true,
        bloom: false, chromatic: false, energyRings: false,
        constellations: false, mouse: false, fpsThrottle: 1,
      };
    case "trace":
      return {
        tendrils: false, nuclei: false, nucleiScale: 0, particles: false,
        particleCap: 0, membrane: false, membraneSimple: false, core: false,
        bloom: false, chromatic: false, energyRings: false,
        constellations: false, mouse: false, fpsThrottle: 2,
      };
    case "glow":
      return {
        tendrils: false, nuclei: false, nucleiScale: 0, particles: false,
        particleCap: 0, membrane: false, membraneSimple: false, core: false,
        bloom: false, chromatic: false, energyRings: false,
        constellations: false, mouse: false, fpsThrottle: 1,
      };
  }
}

export class MindOrganism {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private bloomCanvas: HTMLCanvasElement;
  private bloomCtx: CanvasRenderingContext2D;
  private config: OrganismConfig;
  private flags: VariantFlags;
  private noise: NoiseField;
  private tendrils: Tendril[] = [];
  private nuclei: Nucleus[] = [];
  private particles: Particle[] = [];
  private mouse = { x: -9999, y: -9999, influence: 0 };
  private time = 0;
  private raf = 0;
  private frameCount = 0;

  /* imperative state */
  private highlightedBelief = -1;
  private highlightStrength = 0;
  private pulseTime = -999;
  private pulseStrength = 0;

  private eventCleanup: (() => void) | null = null;

  constructor(canvas: HTMLCanvasElement, config?: Partial<OrganismConfig>) {
    this.canvas = canvas;
    this.ctx = canvas.getContext("2d")!;
    this.config = { ...defaults, ...config };
    this.flags = getVariantFlags(this.config.variant, this.config.stage);
    this.noise = new NoiseField(Math.floor(Math.random() * 9999));

    this.bloomCanvas = document.createElement("canvas");
    this.bloomCtx = this.bloomCanvas.getContext("2d")!;

    this.generate();
    if (this.config.responsive && this.flags.mouse) this.bindEvents();
  }

  private generate() {
    const { stage } = this.config;
    const baseTendrils = stage === 3 ? 24 : stage === 2 ? 16 : 9;
    const baseNuclei = stage === 3 ? 12 : stage === 2 ? 7 : 4;

    const tendrilCount = this.flags.tendrils ? baseTendrils : 0;
    const nucleiCount = this.flags.nuclei
      ? Math.max(3, Math.round(baseNuclei * this.flags.nucleiScale))
      : 0;

    this.tendrils = Array.from({ length: tendrilCount }, (_, i) => ({
      originAngle: (i / tendrilCount) * Math.PI * 2 + (Math.random() - 0.5) * 0.3,
      length: 0.25 + Math.random() * 0.35,
      speed: 0.3 + Math.random() * 0.5,
      width: stage === 3 ? 2 + Math.random() * 3 : 1 + Math.random() * 2,
      phase: Math.random() * Math.PI * 2,
      amplitude: 15 + Math.random() * 25,
      beliefIndex: i % 5,
    }));

    this.nuclei = Array.from({ length: nucleiCount }, (_, i) => ({
      angle: Math.random() * Math.PI * 2,
      dist: 0.15 + Math.random() * 0.4,
      baseSize: stage === 3 ? 4 + Math.random() * 6 : 2 + Math.random() * 4,
      phase: Math.random() * Math.PI * 2,
      orbit: (Math.random() - 0.5) * 0.08,
      beliefIndex: i % 5,
    }));
  }

  private bindEvents() {
    const onMove = (e: MouseEvent) => {
      const rect = this.canvas.getBoundingClientRect();
      this.mouse.x = e.clientX - rect.left;
      this.mouse.y = e.clientY - rect.top;
      this.mouse.influence = 1;
      if (this.config.stage >= 2 && this.flags.particles) {
        this.emitParticles(this.mouse.x, this.mouse.y, 2);
      }
    };
    const onLeave = () => { this.mouse.influence = 0; };
    this.canvas.addEventListener("mousemove", onMove);
    this.canvas.addEventListener("mouseleave", onLeave);
    this.eventCleanup = () => {
      this.canvas.removeEventListener("mousemove", onMove);
      this.canvas.removeEventListener("mouseleave", onLeave);
    };
  }

  private emitParticles(x: number, y: number, count: number) {
    if (!this.flags.particles) return;
    const rgb = hexToRGB(this.config.color);
    const cap = this.config.maxParticles ?? this.flags.particleCap;
    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 0.3 + Math.random() * 1.5;
      this.particles.push({
        x, y,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        life: 1,
        maxLife: 1,
        size: 1 + Math.random() * 2,
        color: Math.random() > 0.5 ? rgb : BELIEF_COLORS[Math.floor(Math.random() * 5)],
      });
    }
    if (this.particles.length > cap) {
      this.particles = this.particles.slice(-Math.floor(cap * 0.8));
    }
  }

  /* ── Public API ──────────────────────────────────────────── */

  start() {
    if (this.config.frozen) {
      this.time = 1.0; // non-zero for noise variation
      this.draw(0.016);
      return;
    }
    let prev = performance.now();
    const loop = (now: number) => {
      const dt = Math.min((now - prev) / 1000, 0.05);
      prev = now;
      this.time += dt;
      this.frameCount++;
      this.mouse.influence *= 0.95;

      // FPS throttle for ambient variant
      if (this.flags.fpsThrottle > 1 && this.frameCount % this.flags.fpsThrottle !== 0) {
        this.raf = requestAnimationFrame(loop);
        return;
      }

      this.draw(dt);
      this.raf = requestAnimationFrame(loop);
    };
    this.raf = requestAnimationFrame(loop);
  }

  stop() {
    cancelAnimationFrame(this.raf);
    this.eventCleanup?.();
  }

  updateConfig(partial: Partial<OrganismConfig>) {
    const stageChanged = partial.stage !== undefined && partial.stage !== this.config.stage;
    const variantChanged = partial.variant !== undefined && partial.variant !== this.config.variant;
    Object.assign(this.config, partial);

    if (stageChanged || variantChanged) {
      this.flags = getVariantFlags(this.config.variant, this.config.stage);
      this.generate();
    }

    if (this.config.frozen) {
      this.draw(0.016);
    }
  }

  /** Highlight a specific belief domain (0-4). Pass -1 to clear. */
  highlightBelief(beliefIndex: number, strength = 1) {
    this.highlightedBelief = beliefIndex;
    this.highlightStrength = Math.max(0, Math.min(1, strength));
  }

  /** Emit a radial pulse wave from the core */
  pulse(strength = 1) {
    this.pulseTime = this.time;
    this.pulseStrength = Math.max(0, Math.min(1, strength));
    this.emitParticles(this.w() / 2, this.h() / 2, Math.floor(strength * 20));
  }

  private w() { return this.canvas.width; }
  private h() { return this.canvas.height; }

  /* ── Main draw loop ─────────────────────────────────────── */

  private draw(_dt: number) {
    const { variant } = this.config;

    if (variant === "trace") {
      this.drawTrace();
      return;
    }
    if (variant === "glow") {
      this.drawGlow();
      return;
    }

    this.drawOrganism();
  }

  /* ── Organism renderer (hero / ambient / micro) ─────────── */

  private drawOrganism() {
    const ctx = this.ctx;
    const w = this.w(), h = this.h();
    if (w === 0 || h === 0) return;
    const cx = w / 2, cy = h / 2;
    const R = Math.min(cx, cy) * 0.7;
    const { color, secondaryColor, stage, breathRate, intensity, variant } = this.config;
    const t = this.time;
    const breath = Math.sin(t * Math.PI * 2 / breathRate) * 0.5 + 0.5;
    const rgb = hexToRGB(color);
    const _rgb2 = secondaryColor ? hexToRGB(secondaryColor) : { r: rgb.r * 0.6, g: rgb.g * 0.6, b: rgb.b * 1.3 };
    const flags = this.flags;

    // Belief weight multipliers
    const bw = this.config.beliefWeights ?? [1, 1, 1, 1, 1];

    // Pulse wave state
    const pulseAge = t - this.pulseTime;
    const pulseActive = pulseAge < 1.0 && this.pulseStrength > 0;
    const pulseWave = pulseActive ? Math.exp(-pulseAge * 3) * this.pulseStrength : 0;

    ctx.clearRect(0, 0, w, h);

    /* ── 1. Deep ambient glow ──────────────────────────────── */
    const ambR = R * (1.2 + breath * 0.15 + pulseWave * 0.3);
    const amb = ctx.createRadialGradient(cx, cy, 0, cx, cy, ambR);
    amb.addColorStop(0, rgba(rgb, 0.06 + breath * 0.03 + pulseWave * 0.05));
    amb.addColorStop(0.5, rgba(rgb, 0.02));
    amb.addColorStop(1, rgba(rgb, 0));
    ctx.fillStyle = amb;
    ctx.fillRect(0, 0, w, h);

    /* ── 2. Membrane ───────────────────────────────────────── */
    if (flags.membrane) {
      ctx.beginPath();

      if (flags.membraneSimple) {
        // Micro variant: simplified circle with slight breathing
        const memR = R * (0.55 + 0.04 * breath + pulseWave * 0.05);
        ctx.arc(cx, cy, memR, 0, Math.PI * 2);
      } else {
        const memPoints = 120;
        for (let i = 0; i <= memPoints; i++) {
          const a = (i / memPoints) * Math.PI * 2;
          const noiseVal = this.noise.noise2D(
            Math.cos(a) * 2 + t * 0.15,
            Math.sin(a) * 2 + t * 0.15
          );
          const r = R * (0.55 + 0.12 * noiseVal + 0.04 * breath + pulseWave * 0.06);

          let warp = 0;
          if (flags.mouse && this.mouse.influence > 0.01) {
            const mx = this.mouse.x - cx, my = this.mouse.y - cy;
            const mAngle = Math.atan2(my, mx);
            const angleDiff = Math.abs(((a - mAngle + Math.PI * 3) % (Math.PI * 2)) - Math.PI);
            if (angleDiff < 0.8) {
              warp = (0.8 - angleDiff) * 20 * this.mouse.influence;
            }
          }

          const px = cx + Math.cos(a) * (r + warp);
          const py = cy + Math.sin(a) * (r + warp);
          i === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }
        ctx.closePath();
      }

      const memGrad = ctx.createRadialGradient(cx, cy, R * 0.1, cx, cy, R * 0.7);
      memGrad.addColorStop(0, rgba(rgb, 0.03 + stage * 0.01));
      memGrad.addColorStop(1, rgba(rgb, 0.005));
      ctx.fillStyle = memGrad;
      ctx.fill();
      ctx.strokeStyle = rgba(rgb, 0.08 + breath * 0.04 + pulseWave * 0.06);
      ctx.lineWidth = stage >= 2 ? 1.5 : 0.8;
      ctx.stroke();
    }

    /* ── 3. Tendrils — belief-colored ──────────────────────── */
    if (flags.tendrils) {
      for (const td of this.tendrils) {
        // Belief highlighting: dim non-highlighted tendrils
        const bWeight = bw[td.beliefIndex] ?? 1;
        let highlightMul = 1;
        if (this.highlightedBelief >= 0) {
          highlightMul = td.beliefIndex === this.highlightedBelief
            ? 1 + this.highlightStrength * 0.8
            : 1 - this.highlightStrength * 0.6;
        }
        const effectiveAlpha = highlightMul * bWeight;
        if (effectiveAlpha < 0.05) continue;

        const ang = td.originAngle + Math.sin(t * td.speed * 0.3 + td.phase) * 0.15;
        const startR = R * 0.08;
        const endR = R * td.length;

        const bColor = stage >= 2
          ? lerpRGB(rgb, BELIEF_COLORS[td.beliefIndex], 0.4)
          : rgb;

        ctx.beginPath();
        const segments = variant === "ambient" ? 30 : 40;
        for (let s = 0; s <= segments; s++) {
          const frac = s / segments;
          const r = startR + (endR - startR) * frac;

          const nx = this.noise.noise2D(
            Math.cos(ang) * frac * 3 + t * td.speed * 0.4,
            Math.sin(ang) * frac * 3 + t * td.speed * 0.4
          );
          const ny = this.noise.noise2D(
            Math.cos(ang) * frac * 3 + 100 + t * td.speed * 0.4,
            Math.sin(ang) * frac * 3 + 100 + t * td.speed * 0.4
          );

          const displace = td.amplitude * frac * intensity;
          const px = cx + Math.cos(ang) * r + nx * displace;
          const py = cy + Math.sin(ang) * r + ny * displace;
          s === 0 ? ctx.moveTo(px, py) : ctx.lineTo(px, py);
        }

        const alpha = (0.15 + breath * 0.1) * intensity * effectiveAlpha;
        ctx.strokeStyle = rgba(bColor, alpha);
        ctx.lineWidth = td.width * (0.8 + breath * 0.3);
        ctx.lineCap = "round";
        ctx.stroke();

        // Glowing tip
        if (stage >= 2) {
          const tipR = startR + (endR - startR);
          const tipNx = this.noise.noise2D(Math.cos(ang) * 3 + t * td.speed * 0.4, Math.sin(ang) * 3 + t * td.speed * 0.4);
          const tipNy = this.noise.noise2D(Math.cos(ang) * 3 + 100 + t * td.speed * 0.4, Math.sin(ang) * 3 + 100 + t * td.speed * 0.4);
          const tipX = cx + Math.cos(ang) * tipR + tipNx * td.amplitude * intensity;
          const tipY = cy + Math.sin(ang) * tipR + tipNy * td.amplitude * intensity;

          const tipGlow = ctx.createRadialGradient(tipX, tipY, 0, tipX, tipY, 8 + stage * 3);
          tipGlow.addColorStop(0, rgba(bColor, 0.4 * breath * effectiveAlpha));
          tipGlow.addColorStop(1, rgba(bColor, 0));
          ctx.fillStyle = tipGlow;
          ctx.beginPath();
          ctx.arc(tipX, tipY, 8 + stage * 3, 0, Math.PI * 2);
          ctx.fill();
        }
      }
    }

    /* ── 4. Nuclei ─────────────────────────────────────────── */
    if (flags.nuclei) {
      for (let ni = 0; ni < this.nuclei.length; ni++) {
        const n = this.nuclei[ni];
        if (!this.config.frozen) n.angle += n.orbit * 0.016;
        const nd = R * n.dist;
        const nx = cx + Math.cos(n.angle) * nd;
        const ny = cy + Math.sin(n.angle) * nd;
        const pulse = 1 + 0.4 * Math.sin(t * 1.5 + n.phase) + pulseWave * 0.5;
        const size = n.baseSize * pulse;

        // Belief highlighting for nuclei
        const bWeight = bw[n.beliefIndex] ?? 1;
        let nHighlight = 1;
        if (this.highlightedBelief >= 0) {
          nHighlight = n.beliefIndex === this.highlightedBelief
            ? 1 + this.highlightStrength * 0.6
            : 1 - this.highlightStrength * 0.4;
        }

        const nColor = stage >= 2 ? lerpRGB(rgb, BELIEF_COLORS[n.beliefIndex], 0.3) : rgb;

        const glowRadius = size * (stage === 3 ? 6 : variant === "micro" ? 3 : 4);
        const glow = ctx.createRadialGradient(nx, ny, 0, nx, ny, glowRadius);
        glow.addColorStop(0, rgba(nColor, 0.25 * intensity * nHighlight * bWeight));
        glow.addColorStop(0.4, rgba(nColor, 0.08 * intensity * nHighlight * bWeight));
        glow.addColorStop(1, rgba(nColor, 0));
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.arc(nx, ny, glowRadius, 0, Math.PI * 2);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(nx, ny, size, 0, Math.PI * 2);
        ctx.fillStyle = rgba(nColor, (0.7 + 0.3 * breath) * nHighlight * bWeight);
        ctx.fill();

        ctx.beginPath();
        ctx.arc(nx, ny, size * 0.4, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255,255,255,${(0.3 + 0.2 * breath) * nHighlight * bWeight})`;
        ctx.fill();

        // Nucleus particle emission (stage 3 only, slow)
        if (stage === 3 && flags.particles && Math.random() < 0.03) {
          this.emitParticles(nx, ny, 1);
        }
      }
    }

    /* ── 4b. Constellation connections (stage 2+) ────────── */
    if (flags.constellations && this.config.constellations && this.nuclei.length > 1) {
      const maxDist = R * 0.6;
      ctx.lineWidth = 0.5;
      for (let i = 0; i < this.nuclei.length; i++) {
        const a = this.nuclei[i];
        const ax = cx + Math.cos(a.angle) * R * a.dist;
        const ay = cy + Math.sin(a.angle) * R * a.dist;
        for (let j = i + 1; j < this.nuclei.length; j++) {
          const b = this.nuclei[j];
          const bx = cx + Math.cos(b.angle) * R * b.dist;
          const by = cy + Math.sin(b.angle) * R * b.dist;
          const dx = ax - bx, dy = ay - by;
          const d = Math.sqrt(dx * dx + dy * dy);
          if (d < maxDist) {
            const lineAlpha = (1 - d / maxDist) * (0.03 + 0.05 * breath) * intensity;
            const lineColor = lerpRGB(
              BELIEF_COLORS[a.beliefIndex],
              BELIEF_COLORS[b.beliefIndex],
              0.5
            );
            ctx.beginPath();
            ctx.moveTo(ax, ay);
            ctx.lineTo(bx, by);
            ctx.strokeStyle = rgba(lineColor, lineAlpha);
            ctx.stroke();
          }
        }
      }
    }

    /* ── 5. Particles ──────────────────────────────────────── */
    if (flags.particles) {
      for (let i = this.particles.length - 1; i >= 0; i--) {
        const p = this.particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vx *= 0.98;
        p.vy *= 0.98;
        p.life -= 0.015;

        if (p.life <= 0) {
          this.particles.splice(i, 1);
          continue;
        }

        const alpha = p.life * 0.6 * intensity;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size * p.life, 0, Math.PI * 2);
        ctx.fillStyle = rgba(p.color, alpha);
        ctx.fill();
      }
    }

    /* ── 6. Central core ───────────────────────────────────── */
    if (flags.core) {
      const coreSize = 5 + stage * 3 + breath * 3 + pulseWave * 6;
      const coreGlow = ctx.createRadialGradient(cx, cy, 0, cx, cy, coreSize * 8);
      coreGlow.addColorStop(0, rgba(rgb, 0.3 + pulseWave * 0.2));
      coreGlow.addColorStop(0.3, rgba(rgb, 0.1));
      coreGlow.addColorStop(1, rgba(rgb, 0));
      ctx.fillStyle = coreGlow;
      ctx.beginPath();
      ctx.arc(cx, cy, coreSize * 8, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.arc(cx, cy, coreSize, 0, Math.PI * 2);
      ctx.fillStyle = rgba(rgb, 0.8);
      ctx.fill();
      ctx.beginPath();
      ctx.arc(cx, cy, coreSize * 0.5, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(255,255,255,${0.5 + pulseWave * 0.3})`;
      ctx.fill();
    }

    /* ── 7. Pulse wave ring (when pulse() is called) ──────── */
    if (pulseActive) {
      const pulseR = R * pulseAge * 1.2;
      const pulseAlpha = pulseWave * 0.15;
      ctx.beginPath();
      ctx.arc(cx, cy, pulseR, 0, Math.PI * 2);
      ctx.strokeStyle = rgba(rgb, pulseAlpha);
      ctx.lineWidth = 2 + pulseWave * 3;
      ctx.stroke();
    }

    /* ── 8. Stage 3: outer energy rings ────────────────────── */
    if (flags.energyRings && stage === 3) {
      for (let ring = 0; ring < 3; ring++) {
        const ringR = R * (0.6 + ring * 0.12) + Math.sin(t * 0.7 + ring * 2) * 8;
        ctx.beginPath();
        ctx.arc(cx, cy, ringR, 0, Math.PI * 2);
        ctx.strokeStyle = rgba(rgb, 0.04 + 0.02 * Math.sin(t + ring));
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }

    /* ── 9. Bloom composite ───────────────────────────────── */
    const doBloom = this.config.bloomEnabled ?? flags.bloom;
    if (doBloom && stage >= 2) {
      this.applyBloom(w, h);
    }

    /* ── 10. Chromatic aberration ──────────────────────────── */
    const doChromatic = this.config.chromaticEnabled ?? flags.chromatic;
    if (doChromatic && stage === 3) {
      this.applyChromaticAberration(w, h);
    }
  }

  /* ── Trace renderer (linear ribbon for progress bars) ──── */

  private drawTrace() {
    const ctx = this.ctx;
    const w = this.w(), h = this.h();
    if (w === 0 || h === 0) return;
    const t = this.time;
    const { color, intensity, breathRate } = this.config;
    const rgb = hexToRGB(color);
    const breath = Math.sin(t * Math.PI * 2 / breathRate) * 0.5 + 0.5;

    ctx.clearRect(0, 0, w, h);

    // Draw belief-colored sinusoidal waves flowing horizontally
    const waveCount = 5;
    for (let wi = 0; wi < waveCount; wi++) {
      const bColor = lerpRGB(rgb, BELIEF_COLORS[wi], 0.5);
      const freq = 0.008 + wi * 0.003;
      const amp = h * (0.15 + wi * 0.03);
      const phase = wi * 1.2 + t * (0.5 + wi * 0.15);

      ctx.beginPath();
      for (let x = 0; x <= w; x += 2) {
        const noiseY = this.noise.noise2D(x * 0.01 + t * 0.2 + wi * 10, wi * 5);
        const y = h / 2
          + Math.sin(x * freq + phase) * amp
          + noiseY * h * 0.05;
        x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.strokeStyle = rgba(bColor, (0.08 + breath * 0.04) * intensity);
      ctx.lineWidth = 1.5;
      ctx.lineCap = "round";
      ctx.stroke();
    }

    // Nucleus dots at intervals
    const dotCount = Math.floor(w / 80);
    for (let i = 0; i < dotCount; i++) {
      const dx = (i + 0.5) / dotCount * w;
      const noiseY = this.noise.noise2D(dx * 0.01 + t * 0.2, 0);
      const dy = h / 2 + noiseY * h * 0.1;
      const dotSize = 2 + breath * 1;
      const bColor = BELIEF_COLORS[i % 5];

      const dotGlow = ctx.createRadialGradient(dx, dy, 0, dx, dy, dotSize * 4);
      dotGlow.addColorStop(0, rgba(bColor, 0.3 * intensity));
      dotGlow.addColorStop(1, rgba(bColor, 0));
      ctx.fillStyle = dotGlow;
      ctx.beginPath();
      ctx.arc(dx, dy, dotSize * 4, 0, Math.PI * 2);
      ctx.fill();

      ctx.beginPath();
      ctx.arc(dx, dy, dotSize, 0, Math.PI * 2);
      ctx.fillStyle = rgba(bColor, 0.7 * intensity);
      ctx.fill();
    }
  }

  /* ── Glow renderer (radial glow only) ──────────────────── */

  private drawGlow() {
    const ctx = this.ctx;
    const w = this.w(), h = this.h();
    if (w === 0 || h === 0) return;
    const cx = w / 2, cy = h / 2;
    const R = Math.min(cx, cy);
    const { color, intensity, breathRate } = this.config;
    const rgb = hexToRGB(color);
    const t = this.time;
    const breath = Math.sin(t * Math.PI * 2 / breathRate) * 0.5 + 0.5;

    ctx.clearRect(0, 0, w, h);

    // Multi-layered radial glow
    for (let layer = 0; layer < 3; layer++) {
      const layerR = R * (0.5 + layer * 0.3) * (1 + breath * 0.1);
      const bColor = lerpRGB(rgb, BELIEF_COLORS[layer % 5], 0.2);
      const glow = ctx.createRadialGradient(cx, cy, 0, cx, cy, layerR);
      glow.addColorStop(0, rgba(bColor, (0.12 - layer * 0.03) * intensity));
      glow.addColorStop(0.5, rgba(bColor, (0.04 - layer * 0.01) * intensity));
      glow.addColorStop(1, rgba(bColor, 0));
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, w, h);
    }
  }

  /* ── Bloom post-processing ─────────────────────────────── */

  private applyBloom(w: number, h: number) {
    this.bloomCanvas.width = w;
    this.bloomCanvas.height = h;
    const bctx = this.bloomCtx;

    bctx.clearRect(0, 0, w, h);
    bctx.filter = "blur(12px) brightness(1.5)";
    bctx.globalAlpha = 0.15;
    bctx.drawImage(this.canvas, 0, 0, w, h);
    bctx.filter = "none";
    bctx.globalAlpha = 1;

    this.ctx.save();
    this.ctx.globalCompositeOperation = "lighter";
    this.ctx.drawImage(this.bloomCanvas, 0, 0);
    this.ctx.restore();
  }

  /* ── Chromatic aberration ──────────────────────────────── */

  private applyChromaticAberration(w: number, h: number) {
    const ctx = this.ctx;
    const imageData = ctx.getImageData(0, 0, w, h);
    const data = imageData.data;
    const cx = w / 2, cy = h / 2;
    const maxDist = Math.sqrt(cx * cx + cy * cy);
    const offset = 2;

    for (let y = 0; y < h; y++) {
      for (let x = 0; x < w; x++) {
        const dx = x - cx, dy = y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy) / maxDist;

        if (dist > 0.7) {
          const strength = (dist - 0.7) / 0.3;
          const ox = Math.round((dx / dist) * offset * strength) || 0;

          const idx = (y * w + x) * 4;
          const rIdx = (y * w + Math.min(w - 1, Math.max(0, x + ox))) * 4;
          const bIdx = (y * w + Math.min(w - 1, Math.max(0, x - ox))) * 4;

          data[idx] = data[rIdx];
          data[idx + 2] = data[bIdx + 2];
        }
      }
    }
    ctx.putImageData(imageData, 0, 0);
  }
}

/* ── Color helpers ─────────────────────────────────────────── */

interface RGB { r: number; g: number; b: number; }

function hexToRGB(hex: string): RGB {
  if (hex.startsWith("hsl")) {
    return { r: 168, g: 85, b: 247 };
  }
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
  return {
    r: a.r + (b.r - a.r) * t,
    g: a.g + (b.g - a.g) * t,
    b: a.b + (b.b - a.b) * t,
  };
}

export { hexToRGB, rgba, lerpRGB };
export type { RGB };
