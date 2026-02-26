/* ── NeuronBrainCanvas — Living Neural Network Visualization ──────
 *  Each song the user listens to spawns a neuron.
 *  Repeated listening strengthens connections (synapses).
 *  The brain grows and evolves as the user listens more.
 *  ──────────────────────────────────────────────────────────────── */

import { useRef, useEffect } from "react";
import { recentTracks, lastWeekDays } from "@/data/mock-listening";

/* ── Genre → Color map ──────────────────────────────────────────── */
const GENRE_COLORS: Record<string, string> = {
  Electronic: "#C084FC",
  "Post-Rock": "#F97316",
  "Neo-Classical": "#38BDF8",
  Ambient: "#84CC16",
  Jazz: "#FBBF24",
};

const DEFAULT_NEURON_COLOR = "#6366F1";

/* ── Types ──────────────────────────────────────────────────────── */
interface Neuron {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  color: string;
  genre: string;
  artist: string;
  strength: number;   // 0-1, how "active" this neuron is
  phase: number;       // animation phase offset
  pulseSpeed: number;
}

interface Synapse {
  from: number;
  to: number;
  strength: number; // 0-1, connection strength
  color: string;
}

/* ── Generate mock neuron data from listening history ───────────── */
function generateNeurons(width: number, height: number): Neuron[] {
  const neurons: Neuron[] = [];
  const cx = width / 2;
  const cy = height / 2;
  const spread = Math.min(width, height) * 0.38;

  // Generate neurons from recent tracks + daily data
  const sources = [
    ...recentTracks.map((t) => ({ genre: t.genre, artist: t.artist, strength: t.rewardIntensity })),
    ...lastWeekDays.map((d) => ({ genre: d.topGenre, artist: "", strength: 0.5 + Math.random() * 0.3 })),
  ];

  // Add extra neurons for density (simulating full listening history)
  const extraGenres = ["Electronic", "Post-Rock", "Neo-Classical", "Ambient", "Jazz"];
  for (let i = 0; i < 35; i++) {
    const g = extraGenres[i % extraGenres.length];
    sources.push({ genre: g, artist: "", strength: 0.3 + Math.random() * 0.5 });
  }

  // Position neurons in a brain-like oval cluster
  sources.forEach((src, i) => {
    const angle = (i / sources.length) * Math.PI * 2 + (Math.random() - 0.5) * 0.8;
    const dist = (0.3 + Math.random() * 0.7) * spread;
    // Slight oval shape (wider than tall, brain-like)
    const x = cx + Math.cos(angle) * dist * 1.15;
    const y = cy + Math.sin(angle) * dist * 0.85;

    neurons.push({
      x,
      y,
      vx: (Math.random() - 0.5) * 0.15,
      vy: (Math.random() - 0.5) * 0.15,
      radius: 1.5 + src.strength * 2.5,
      color: GENRE_COLORS[src.genre] || DEFAULT_NEURON_COLOR,
      genre: src.genre,
      artist: src.artist,
      strength: src.strength,
      phase: Math.random() * Math.PI * 2,
      pulseSpeed: 0.5 + Math.random() * 1.5,
    });
  });

  return neurons;
}

/* ── Build synapses between related neurons ─────────────────────── */
function buildSynapses(neurons: Neuron[]): Synapse[] {
  const synapses: Synapse[] = [];
  const maxDist = 120;

  for (let i = 0; i < neurons.length; i++) {
    for (let j = i + 1; j < neurons.length; j++) {
      const a = neurons[i];
      const b = neurons[j];
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const dist = Math.sqrt(dx * dx + dy * dy);

      if (dist > maxDist) continue;

      // Same genre = stronger connection
      const genreMatch = a.genre === b.genre ? 0.4 : 0;
      // Same artist = even stronger
      const artistMatch = a.artist && a.artist === b.artist ? 0.3 : 0;
      // Proximity bonus
      const proxBonus = (1 - dist / maxDist) * 0.3;

      const strength = genreMatch + artistMatch + proxBonus;
      if (strength < 0.15) continue;

      // Mix colors
      synapses.push({
        from: i,
        to: j,
        strength: Math.min(1, strength),
        color: a.color,
      });
    }
  }

  return synapses;
}

/* ── Hex to RGBA helper ─────────────────────────────────────────── */
function hexToRgba(hex: string, alpha: number): string {
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

/* ── Component ──────────────────────────────────────────────────── */
interface Props {
  color: string;
  className?: string;
  neuronCount?: number;
}

export function NeuronBrainCanvas({ color, className = "" }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const neuronsRef = useRef<Neuron[]>([]);
  const synapsesRef = useRef<Synapse[]>([]);
  const timeRef = useRef(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Size canvas to container
    const resize = () => {
      const rect = canvas.parentElement?.getBoundingClientRect();
      if (!rect) return;
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
      ctx.scale(dpr, dpr);

      // Regenerate neurons on resize
      neuronsRef.current = generateNeurons(rect.width, rect.height);
      synapsesRef.current = buildSynapses(neuronsRef.current);
    };

    resize();
    window.addEventListener("resize", resize);

    // Animation loop
    const animate = () => {
      const rect = canvas.parentElement?.getBoundingClientRect();
      if (!rect) return;
      const w = rect.width;
      const h = rect.height;

      timeRef.current += 0.016; // ~60fps
      const t = timeRef.current;

      ctx.clearRect(0, 0, w, h);

      const neurons = neuronsRef.current;
      const synapses = synapsesRef.current;

      // Gentle drift
      for (const n of neurons) {
        n.x += n.vx;
        n.y += n.vy;

        // Soft boundary (pull back toward center)
        const cx = w / 2;
        const cy = h / 2;
        const dx = n.x - cx;
        const dy = n.y - cy;
        const dist = Math.sqrt(dx * dx + dy * dy);
        const maxR = Math.min(w, h) * 0.42;
        if (dist > maxR) {
          n.vx -= dx * 0.0005;
          n.vy -= dy * 0.0005;
        }

        // Damping
        n.vx *= 0.998;
        n.vy *= 0.998;
      }

      // Draw synapses
      for (const syn of synapses) {
        const a = neurons[syn.from];
        const b = neurons[syn.to];
        const pulse = 0.3 + 0.7 * (0.5 + 0.5 * Math.sin(t * 0.8 + syn.from * 0.3));
        const alpha = syn.strength * pulse * 0.25;

        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = hexToRgba(syn.color, alpha);
        ctx.lineWidth = syn.strength * 1.2;
        ctx.stroke();
      }

      // Draw neurons
      for (const n of neurons) {
        const pulse = 0.6 + 0.4 * Math.sin(t * n.pulseSpeed + n.phase);
        const r = n.radius * (0.8 + pulse * 0.4);

        // Glow
        const grd = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, r * 4);
        grd.addColorStop(0, hexToRgba(n.color, 0.3 * pulse * n.strength));
        grd.addColorStop(0.5, hexToRgba(n.color, 0.08 * pulse));
        grd.addColorStop(1, hexToRgba(n.color, 0));
        ctx.beginPath();
        ctx.arc(n.x, n.y, r * 4, 0, Math.PI * 2);
        ctx.fillStyle = grd;
        ctx.fill();

        // Core
        ctx.beginPath();
        ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
        ctx.fillStyle = hexToRgba(n.color, 0.7 + 0.3 * pulse);
        ctx.fill();
      }

      // Subtle brain-shaped outer glow
      const bgGrd = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, Math.min(w, h) * 0.5);
      bgGrd.addColorStop(0, hexToRgba(color, 0.02));
      bgGrd.addColorStop(0.7, hexToRgba(color, 0.01));
      bgGrd.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = bgGrd;
      ctx.fillRect(0, 0, w, h);

      animRef.current = requestAnimationFrame(animate);
    };

    animRef.current = requestAnimationFrame(animate);

    return () => {
      cancelAnimationFrame(animRef.current);
      window.removeEventListener("resize", resize);
    };
  }, [color]);

  return (
    <div className={`relative w-full h-full ${className}`}>
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full"
      />
      {/* Neuron count overlay */}
      <div className="absolute bottom-2 left-3 flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full animate-pulse" style={{ background: color }} />
        <span className="text-[10px] font-mono text-slate-600">
          {neuronsRef.current?.length || 47} neurons
        </span>
      </div>
    </div>
  );
}
