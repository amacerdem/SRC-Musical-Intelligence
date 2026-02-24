import { useRef, useEffect, useCallback, useState, useMemo } from 'react';
import { useNavigationStore } from '../stores/navigationStore';
import { usePipelineStore } from '../stores/pipelineStore';
import { useAudioStore } from '../stores/audioStore';
import { fetchJSON, fetchBinary } from '../api/client';
import { colors, R3_GROUP_COLORS, FRAME_RATE } from '../design/tokens';
import GlassPanel from '../components/layout/GlassPanel';

// ══════════════════════════════════════════════════════════════════════
//  NEURAL OVERVIEW — Interactive Data-Driven System DAG
//  Click to drill deeper into R³, H³, C³, Output layers
// ══════════════════════════════════════════════════════════════════════

interface ClusterNode {
  id: string;
  label: string;
  sublabel: string;
  x: number;
  y: number;
  w: number;
  h: number;
  color: string;
  category: 'source' | 'r3' | 'h3' | 'c3' | 'output';
  navigateTo?: () => void;
  dims?: string;
  detail?: string;
}

interface ClusterEdge {
  from: string;
  to: string;
  color: string;
  width?: number;
  label?: string;
  dashed?: boolean;
}

interface Particle {
  edge: number;
  t: number;
  speed: number;
}

// Layout
const W = 1600;
const H = 900;
const COL_SRC = 60;
const COL_R3 = 280;
const COL_H3 = 560;
const COL_C3 = 860;
const COL_OUT = 1180;

interface AudioFile {
  name: string;
  filename: string;
  duration: number;
  sample_rate: number;
  channels: number;
}

export default function NeuralOverview() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<ClusterNode | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });
  const [camera, setCamera] = useState({ x: 30, y: 30, zoom: 0.85 });
  const isDragging = useRef(false);
  const dragStart = useRef({ x: 0, y: 0, cx: 0, cy: 0 });
  const particlesRef = useRef<Particle[]>([]);
  const timeRef = useRef(0);

  const { navigateIn } = useNavigationStore();
  const { r3Features, r3Frames, rewardData, ramData, currentExperimentId } = usePipelineStore();
  const { currentFrame } = useAudioStore();

  // Audio library
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [showAudioPicker, setShowAudioPicker] = useState(false);

  useEffect(() => {
    fetchJSON<AudioFile[]>('/audio/list').then(setAudioFiles).catch(() => {});
  }, []);

  const hasData = r3Features !== null && r3Frames > 0;

  // Real-time data values at current frame
  const liveData = useMemo(() => {
    if (!hasData || currentFrame >= r3Frames) return null;
    // R3 group energies
    const groups: Record<string, number> = {};
    const ranges: [string, number, number][] = [
      ['A', 0, 7], ['B', 7, 12], ['C', 12, 21], ['D', 21, 25],
      ['F', 25, 41], ['G', 41, 51], ['H', 51, 63], ['J', 63, 83], ['K', 83, 97],
    ];
    let totalR3 = 0;
    for (const [key, start, end] of ranges) {
      let sum = 0;
      for (let i = start; i < end; i++) {
        sum += r3Features![currentFrame * 97 + i];
      }
      groups[key] = sum / (end - start);
      totalR3 += groups[key];
    }
    totalR3 /= 9;

    const reward = rewardData ? rewardData[currentFrame] || 0 : 0;

    // RAM mean
    let ramMean = 0;
    if (ramData) {
      for (let i = 0; i < 26; i++) {
        ramMean += ramData[currentFrame * 26 + i];
      }
      ramMean /= 26;
    }

    return { groups, totalR3, reward, ramMean };
  }, [hasData, r3Features, rewardData, ramData, currentFrame, r3Frames]);

  // Build cluster nodes
  const nodes: ClusterNode[] = useMemo(() => [
    // Source
    { id: 'audio', label: 'Audio', sublabel: 'WAV \u00B7 44.1kHz', x: COL_SRC, y: 200, w: 150, h: 55, color: '#ffffff', category: 'source', dims: '(1, N)', detail: 'Raw audio waveform' },
    { id: 'mel', label: 'Mel Spectrogram', sublabel: '128 bands \u00B7 log1p', x: COL_SRC, y: 340, w: 150, h: 55, color: '#64748b', category: 'source', dims: '(1, 128, T)', detail: 'Frame rate: 172.27 Hz' },

    // R3 — single cluster with sub-dots
    { id: 'r3', label: 'R\u00B3 Perception', sublabel: '97D \u00B7 9 groups \u00B7 Frozen', x: COL_R3, y: 130, w: 200, h: 340, color: colors.r3, category: 'r3',
      navigateTo: () => navigateIn({ type: 'r3' }), dims: '(B, T, 97)', detail: 'Deterministic per-frame spectral features' },

    // H3
    { id: 'h3', label: 'H\u00B3 Temporal', sublabel: '32 horizons \u00B7 24 morphs \u00B7 3 laws', x: COL_H3, y: 130, w: 200, h: 340, color: colors.h3, category: 'h3',
      navigateTo: () => navigateIn({ type: 'h3' }), dims: '131 tuples', detail: 'Demand-driven multi-scale temporal morphology' },

    // C3
    { id: 'c3', label: 'C\u00B3 Cognition', sublabel: '9 relays \u00B7 131 beliefs', x: COL_C3, y: 130, w: 200, h: 340, color: colors.c3, category: 'c3',
      navigateTo: () => navigateIn({ type: 'c3' }), dims: '131 beliefs', detail: 'Bayesian cognitive architecture\n9 functions \u00B7 3 meta-layers' },

    // Outputs
    { id: 'reward', label: 'Reward', sublabel: 'R = sal \u00D7 w \u00D7 fam \u00D7 DA', x: COL_OUT, y: 130, w: 180, h: 65, color: colors.reward, category: 'output',
      navigateTo: () => navigateIn({ type: 'reward' }), dims: '(B, T)', detail: 'Composite musical pleasure signal' },
    { id: 'neuro', label: 'Neuro', sublabel: 'DA \u00B7 NE \u00B7 OPI \u00B7 5HT', x: COL_OUT, y: 230, w: 180, h: 65, color: '#ef4444', category: 'output',
      navigateTo: () => navigateIn({ type: 'neuro' }), dims: '(B, T, 4)', detail: '4 neurochemical channels' },
    { id: 'ram', label: 'RAM', sublabel: '26 brain regions', x: COL_OUT, y: 330, w: 180, h: 65, color: colors.c3, category: 'output',
      navigateTo: () => navigateIn({ type: 'ram' }), dims: '(B, T, 26)', detail: 'Region Activation Map\nSTG convergence hub' },
    { id: 'psi', label: '\u03A8\u00B3', sublabel: 'Cognitive State \u00B7 28D', x: COL_OUT, y: 430, w: 180, h: 65, color: '#8b5cf6', category: 'output',
      dims: '6 domains', detail: 'affect \u00B7 emotion \u00B7 aesthetic\nbodily \u00B7 cognitive \u00B7 temporal' },
  ], [navigateIn]);

  const edges: ClusterEdge[] = useMemo(() => [
    { from: 'audio', to: 'mel', color: '#ffffff20', width: 2 },
    { from: 'mel', to: 'r3', color: colors.r3 + '40', width: 3, label: '128 mels' },
    { from: 'r3', to: 'h3', color: colors.r3 + '50', width: 3, label: '97D' },
    { from: 'h3', to: 'c3', color: colors.h3 + '50', width: 3, label: '131 tuples' },
    { from: 'r3', to: 'c3', color: colors.r3 + '20', dashed: true, label: 'direct' },
    { from: 'c3', to: 'reward', color: colors.reward + '40', width: 2 },
    { from: 'c3', to: 'neuro', color: '#ef444430' },
    { from: 'c3', to: 'ram', color: colors.c3 + '30' },
    { from: 'c3', to: 'psi', color: '#8b5cf625', dashed: true },
    { from: 'reward', to: 'psi', color: '#8b5cf620' },
    { from: 'neuro', to: 'psi', color: '#8b5cf618' },
  ], []);

  // Initialize particles
  useEffect(() => {
    const particles: Particle[] = [];
    for (let i = 0; i < edges.length; i++) {
      const edge = edges[i];
      const count = (edge.width && edge.width >= 3) ? 4 : 2;
      for (let j = 0; j < count; j++) {
        particles.push({ edge: i, t: Math.random(), speed: 0.001 + Math.random() * 0.002 });
      }
    }
    particlesRef.current = particles;
  }, [edges]);

  const getNodeById = useCallback((id: string) => nodes.find(n => n.id === id), [nodes]);

  // Draw
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const dpr = window.devicePixelRatio || 1;
    const cw = container.clientWidth;
    const ch = container.clientHeight;
    canvas.width = cw * dpr;
    canvas.height = ch * dpr;
    canvas.style.width = `${cw}px`;
    canvas.style.height = `${ch}px`;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    ctx.scale(dpr, dpr);

    const { x: cx, y: cy, zoom } = camera;
    timeRef.current += 1;

    // Clear
    ctx.fillStyle = '#0a0a0f';
    ctx.fillRect(0, 0, cw, ch);

    ctx.save();
    ctx.translate(cx, cy);
    ctx.scale(zoom, zoom);

    // Subtle grid
    ctx.strokeStyle = 'rgba(255,255,255,0.012)';
    ctx.lineWidth = 0.5;
    for (let gx = 0; gx < W; gx += 80) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, H); ctx.stroke();
    }
    for (let gy = 0; gy < H; gy += 80) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(W, gy); ctx.stroke();
    }

    // Section labels
    const sections = [
      { x: COL_SRC + 75, y: 160, label: 'SOURCE', color: '#ffffff20' },
      { x: COL_R3 + 100, y: 100, label: 'R\u00B3 PERCEPTION', color: colors.r3 + '50' },
      { x: COL_H3 + 100, y: 100, label: 'H\u00B3 TEMPORAL', color: colors.h3 + '50' },
      { x: COL_C3 + 100, y: 100, label: 'C\u00B3 COGNITION', color: colors.c3 + '50' },
      { x: COL_OUT + 90, y: 100, label: 'OUTPUT', color: colors.reward + '50' },
    ];
    for (const sl of sections) {
      ctx.font = '600 9px Inter, sans-serif';
      ctx.fillStyle = sl.color;
      ctx.textAlign = 'center';
      ctx.fillText(sl.label.toUpperCase(), sl.x, sl.y);
    }

    // Edges
    for (const edge of edges) {
      const from = getNodeById(edge.from);
      const to = getNodeById(edge.to);
      if (!from || !to) continue;

      const x1 = from.x + from.w;
      const y1 = from.y + from.h / 2;
      const x2 = to.x;
      const y2 = to.y + to.h / 2;

      ctx.strokeStyle = edge.color;
      ctx.lineWidth = edge.width || 1;
      ctx.setLineDash(edge.dashed ? [4, 4] : []);

      const cpx = (x1 + x2) / 2;
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.bezierCurveTo(cpx, y1, cpx, y2, x2, y2);
      ctx.stroke();

      if (edge.label) {
        ctx.font = '8px JetBrains Mono, monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.15)';
        ctx.textAlign = 'center';
        ctx.fillText(edge.label, (x1 + x2) / 2, (y1 + y2) / 2 - 6);
      }
    }
    ctx.setLineDash([]);

    // Particles — speed driven by data
    const dataSpeedMul = hasData ? 1.5 : 0.5;
    for (const particle of particlesRef.current) {
      particle.t += particle.speed * dataSpeedMul;
      if (particle.t > 1) particle.t -= 1;

      const edge = edges[particle.edge];
      const from = getNodeById(edge.from);
      const to = getNodeById(edge.to);
      if (!from || !to) continue;

      const x1 = from.x + from.w, y1 = from.y + from.h / 2;
      const x2 = to.x, y2 = to.y + to.h / 2;
      const cpx = (x1 + x2) / 2;
      const t = particle.t, mt = 1 - t;
      const px = mt*mt*mt*x1 + 3*mt*mt*t*cpx + 3*mt*t*t*cpx + t*t*t*x2;
      const py = mt*mt*mt*y1 + 3*mt*mt*t*y1 + 3*mt*t*t*y2 + t*t*t*y2;

      const pColor = edge.color.substring(0, 7);
      const alpha = hasData ? 'cc' : '40';
      ctx.fillStyle = pColor + alpha;
      ctx.beginPath();
      ctx.arc(px, py, hasData ? 2.5 : 1.5, 0, Math.PI * 2);
      ctx.fill();

      if (hasData) {
        ctx.fillStyle = pColor + '25';
        ctx.beginPath();
        ctx.arc(px, py, 7, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Hovered connections
    const hoveredConnections = new Set<string>();
    if (hoveredNode) {
      for (const edge of edges) {
        if (edge.from === hoveredNode.id || edge.to === hoveredNode.id) {
          hoveredConnections.add(edge.from);
          hoveredConnections.add(edge.to);
        }
      }
    }

    // Nodes
    for (const node of nodes) {
      const hovered = hoveredNode?.id === node.id;
      const connected = hoveredNode ? hoveredConnections.has(node.id) : false;
      const dimmed = hoveredNode && !connected && !hovered;
      const isClickable = !!node.navigateTo;

      // Data-driven glow
      let glowIntensity = 0;
      if (hasData && liveData) {
        if (node.id === 'r3') glowIntensity = liveData.totalR3;
        else if (node.id === 'reward') glowIntensity = Math.max(0, liveData.reward * 3);
        else if (node.id === 'ram') glowIntensity = liveData.ramMean;
        else if (node.id === 'c3') glowIntensity = 0.5;
        else if (node.id === 'h3') glowIntensity = 0.5;
      }

      // Background
      ctx.fillStyle = dimmed
        ? 'rgba(255,255,255,0.012)'
        : hovered
          ? 'rgba(255,255,255,0.10)'
          : 'rgba(255,255,255,0.035)';
      ctx.strokeStyle = dimmed
        ? 'rgba(255,255,255,0.025)'
        : hovered
          ? node.color
          : connected
            ? node.color + '50'
            : 'rgba(255,255,255,0.05)';
      ctx.lineWidth = hovered ? 1.5 : 0.8;

      // Rounded rect
      const r = 14;
      ctx.beginPath();
      ctx.moveTo(node.x + r, node.y);
      ctx.lineTo(node.x + node.w - r, node.y);
      ctx.quadraticCurveTo(node.x + node.w, node.y, node.x + node.w, node.y + r);
      ctx.lineTo(node.x + node.w, node.y + node.h - r);
      ctx.quadraticCurveTo(node.x + node.w, node.y + node.h, node.x + node.w - r, node.y + node.h);
      ctx.lineTo(node.x + r, node.y + node.h);
      ctx.quadraticCurveTo(node.x, node.y + node.h, node.x, node.y + node.h - r);
      ctx.lineTo(node.x, node.y + r);
      ctx.quadraticCurveTo(node.x, node.y, node.x + r, node.y);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();

      // Data-driven glow
      if ((hovered || glowIntensity > 0.1) && !dimmed) {
        ctx.shadowColor = node.color;
        ctx.shadowBlur = hovered ? 25 : glowIntensity * 20;
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // R3 sub-dots (mini group indicators inside the R3 cluster)
      if (node.id === 'r3') {
        const groupKeys = ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'J', 'K'];
        const cols = 3, rows = 3;
        const dotR = 10;
        const padX = 35, padY = 60;
        const gapX = (node.w - padX * 2) / (cols - 1);
        const gapY = (node.h - padY - 30) / (rows - 1);

        for (let gi = 0; gi < 9; gi++) {
          const col = gi % cols, row = Math.floor(gi / cols);
          const dx = node.x + padX + col * gapX;
          const dy = node.y + padY + row * gapY;
          const gColor = R3_GROUP_COLORS[groupKeys[gi]];
          const energy = liveData?.groups[groupKeys[gi]] || 0;

          // Glow from data
          if (hasData && energy > 0.15) {
            ctx.fillStyle = gColor + '18';
            ctx.beginPath();
            ctx.arc(dx, dy, dotR + energy * 12, 0, Math.PI * 2);
            ctx.fill();
          }

          ctx.fillStyle = dimmed ? gColor + '15' : gColor + (hasData ? '80' : '40');
          ctx.beginPath();
          ctx.arc(dx, dy, dotR, 0, Math.PI * 2);
          ctx.fill();

          if (!dimmed) {
            ctx.font = '600 7px Inter, sans-serif';
            ctx.fillStyle = gColor + (dimmed ? '40' : 'cc');
            ctx.textAlign = 'center';
            ctx.fillText(groupKeys[gi], dx, dy + 3);
          }
        }
      }

      // H3 horizon bars
      if (node.id === 'h3') {
        const bands = [
          { label: 'Micro', color: '#60a5fa', range: 'H0-H7' },
          { label: 'Meso', color: '#a78bfa', range: 'H8-H15' },
          { label: 'Macro', color: '#f59e0b', range: 'H16-H23' },
          { label: 'Ultra', color: '#ef4444', range: 'H24-H31' },
        ];
        const barH = 20, gap = 8, startY = node.y + 55;
        for (let bi = 0; bi < bands.length; bi++) {
          const by = startY + bi * (barH + gap);
          const bw = node.w - 30;
          ctx.fillStyle = dimmed ? bands[bi].color + '08' : bands[bi].color + '15';
          ctx.beginPath();
          ctx.roundRect(node.x + 15, by, bw, barH, 6);
          ctx.fill();
          if (!dimmed) {
            ctx.font = '500 8px Inter, sans-serif';
            ctx.fillStyle = bands[bi].color + '90';
            ctx.textAlign = 'left';
            ctx.fillText(bands[bi].label, node.x + 22, by + 13);
            ctx.font = '400 7px JetBrains Mono, monospace';
            ctx.fillStyle = 'rgba(255,255,255,0.2)';
            ctx.textAlign = 'right';
            ctx.fillText(bands[bi].range, node.x + 15 + bw - 5, by + 13);
          }
        }
      }

      // C3 relay dots
      if (node.id === 'c3') {
        const relays = [
          { label: 'BCH', color: '#60a5fa' }, { label: 'HMCE', color: '#a78bfa' },
          { label: 'SNEM', color: '#f97316' }, { label: 'MEAMN', color: '#14b8a6' },
          { label: 'DAED', color: '#eab308' }, { label: 'MPG', color: '#22c55e' },
          { label: 'SRP', color: '#ef4444' }, { label: 'PEOM', color: '#ec4899' },
          { label: 'HTP', color: '#6366f1' },
        ];
        const dotR = 8;
        const padX = 30, padY = 55;
        const cols = 3, rows = 3;
        const gapX = (node.w - padX * 2) / (cols - 1);
        const gapY = (node.h - padY - 50) / (rows - 1);

        for (let ri = 0; ri < 9; ri++) {
          const col = ri % cols, row = Math.floor(ri / cols);
          const rx = node.x + padX + col * gapX;
          const ry = node.y + padY + row * gapY;

          ctx.fillStyle = dimmed ? relays[ri].color + '15' : relays[ri].color + '60';
          ctx.beginPath();
          ctx.arc(rx, ry, dotR, 0, Math.PI * 2);
          ctx.fill();

          if (!dimmed) {
            ctx.font = '500 6px Inter, sans-serif';
            ctx.fillStyle = relays[ri].color + 'aa';
            ctx.textAlign = 'center';
            ctx.fillText(relays[ri].label, rx, ry + 3);
          }
        }

        // Belief count label
        if (!dimmed) {
          ctx.font = '400 8px JetBrains Mono, monospace';
          ctx.fillStyle = 'rgba(255,255,255,0.25)';
          ctx.textAlign = 'center';
          ctx.fillText('131 beliefs', node.x + node.w / 2, node.y + node.h - 20);
          ctx.fillText('36C + 65A + 30N', node.x + node.w / 2, node.y + node.h - 10);
        }
      }

      // Label
      const alpha = dimmed ? '30' : 'e0';
      ctx.font = '600 12px Inter, sans-serif';
      ctx.fillStyle = node.color + alpha;
      ctx.textAlign = 'left';
      ctx.fillText(node.label, node.x + 12, node.y + 20);

      // Sublabel
      if (node.sublabel) {
        ctx.font = '400 9px Inter, sans-serif';
        ctx.fillStyle = dimmed ? 'rgba(255,255,255,0.12)' : 'rgba(255,255,255,0.35)';
        ctx.fillText(node.sublabel, node.x + 12, node.y + 34);
      }

      // Dims badge
      if (node.dims && !dimmed) {
        ctx.font = '400 8px JetBrains Mono, monospace';
        ctx.fillStyle = 'rgba(255,255,255,0.2)';
        ctx.textAlign = 'right';
        ctx.fillText(node.dims, node.x + node.w - 10, node.y + 20);
      }

      // Click indicator
      if (isClickable && !dimmed) {
        ctx.font = '400 10px Inter, sans-serif';
        ctx.fillStyle = 'rgba(255,255,255,0.15)';
        ctx.textAlign = 'right';
        ctx.fillText('\u203A', node.x + node.w - 8, node.y + node.h - 8);
      }
    }

    // Highlighted edges for hovered node
    if (hoveredNode) {
      for (const edge of edges) {
        if (edge.from !== hoveredNode.id && edge.to !== hoveredNode.id) continue;
        const from = getNodeById(edge.from);
        const to = getNodeById(edge.to);
        if (!from || !to) continue;

        const x1 = from.x + from.w, y1 = from.y + from.h / 2;
        const x2 = to.x, y2 = to.y + to.h / 2;
        const hColor = edge.from === hoveredNode.id
          ? hoveredNode.color + '80'
          : (getNodeById(edge.from)?.color || '#fff') + '80';

        ctx.strokeStyle = hColor;
        ctx.lineWidth = 2.5;
        ctx.setLineDash(edge.dashed ? [6, 4] : []);

        const cpx = (x1 + x2) / 2;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.bezierCurveTo(cpx, y1, cpx, y2, x2, y2);
        ctx.stroke();

        // Arrow
        const angle = Math.atan2(y2 - (y1 + y2) / 2, x2 - cpx);
        ctx.fillStyle = hColor;
        ctx.beginPath();
        ctx.moveTo(x2, y2);
        ctx.lineTo(x2 - 6 * Math.cos(angle - 0.4), y2 - 6 * Math.sin(angle - 0.4));
        ctx.lineTo(x2 - 6 * Math.cos(angle + 0.4), y2 - 6 * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fill();
      }
      ctx.setLineDash([]);
    }

    ctx.restore();

    // Summary cards (DOM overlay drawn outside canvas transform)
    // These are rendered as React overlays

  }, [camera, hoveredNode, getNodeById, nodes, edges, hasData, liveData]);

  // Animation loop
  useEffect(() => {
    let raf: number;
    const loop = () => { draw(); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [draw]);

  // Hit test
  const hitTest = useCallback((mx: number, my: number): ClusterNode | null => {
    const { x: cx, y: cy, zoom } = camera;
    const wx = (mx - cx) / zoom;
    const wy = (my - cy) / zoom;
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      if (wx >= n.x && wx <= n.x + n.w && wy >= n.y && wy <= n.y + n.h) {
        return n;
      }
    }
    return null;
  }, [camera, nodes]);

  // Mouse events
  const handleMouseMove = useCallback((e: React.MouseEvent) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;

    if (isDragging.current) {
      setCamera(prev => ({
        ...prev,
        x: dragStart.current.cx + (e.clientX - dragStart.current.x),
        y: dragStart.current.cy + (e.clientY - dragStart.current.y),
      }));
      return;
    }

    const node = hitTest(mx, my);
    setHoveredNode(node);
    setTooltipPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
  }, [hitTest]);

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    isDragging.current = true;
    dragStart.current = { x: e.clientX, y: e.clientY, cx: camera.x, cy: camera.y };
  }, [camera]);

  const handleMouseUp = useCallback((e: React.MouseEvent) => {
    if (!isDragging.current) return;
    const dx = Math.abs(e.clientX - dragStart.current.x);
    const dy = Math.abs(e.clientY - dragStart.current.y);
    isDragging.current = false;

    // If minimal movement, treat as click
    if (dx < 4 && dy < 4) {
      const rect = e.currentTarget.getBoundingClientRect();
      const mx = e.clientX - rect.left;
      const my = e.clientY - rect.top;
      const node = hitTest(mx, my);
      if (node?.navigateTo) {
        node.navigateTo();
      }
    }
  }, [hitTest]);

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.preventDefault();
    const rect = e.currentTarget.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    const factor = e.deltaY > 0 ? 0.92 : 1.08;
    setCamera(prev => {
      const newZoom = Math.max(0.3, Math.min(2, prev.zoom * factor));
      const wx = (mx - prev.x) / prev.zoom;
      const wy = (my - prev.y) / prev.zoom;
      return { zoom: newZoom, x: mx - wx * newZoom, y: my - wy * newZoom };
    });
  }, []);

  return (
    <div className="flex flex-col h-full overflow-hidden" style={{ background: '#0a0a0f' }}>
      {/* Canvas */}
      <div
        ref={containerRef}
        className="flex-1 relative"
        style={{ cursor: hoveredNode?.navigateTo ? 'pointer' : isDragging.current ? 'grabbing' : 'grab' }}
        onMouseMove={handleMouseMove}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseLeave={() => { isDragging.current = false; setHoveredNode(null); }}
        onWheel={handleWheel}
      >
        <canvas ref={canvasRef} className="absolute inset-0" />

        {/* Empty state overlay */}
        {!hasData && (
          <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
            <div className="text-center blueprint-pulse">
              <div className="text-sm font-medium mb-2" style={{ color: 'var(--text-secondary)' }}>
                Neural network awaiting data
              </div>
              <div className="text-xs" style={{ color: 'var(--text-muted)' }}>
                Run a pipeline to activate the network
              </div>
            </div>
          </div>
        )}

        {/* Summary cards */}
        {hasData && liveData && (
          <div className="absolute top-3 right-3 flex flex-col gap-2 pointer-events-none">
            <div className="glass-panel-sm px-3 py-2">
              <div className="text-[10px]" style={{ color: 'var(--text-muted)' }}>Reward</div>
              <div className="font-data text-sm" style={{ color: liveData.reward > 0 ? colors.c3 : colors.danger }}>
                {liveData.reward > 0 ? '+' : ''}{liveData.reward.toFixed(4)}
              </div>
            </div>
            <div className="glass-panel-sm px-3 py-2">
              <div className="text-[10px]" style={{ color: 'var(--text-muted)' }}>R\u00B3 Energy</div>
              <div className="font-data text-sm" style={{ color: colors.r3 }}>
                {liveData.totalR3.toFixed(3)}
              </div>
            </div>
            {ramData && (
              <div className="glass-panel-sm px-3 py-2">
                <div className="text-[10px]" style={{ color: 'var(--text-muted)' }}>RAM</div>
                <div className="font-data text-sm" style={{ color: colors.c3 }}>
                  {liveData.ramMean.toFixed(3)}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tooltip */}
        {hoveredNode && (
          <div
            className="glass-panel-sm absolute pointer-events-none p-3"
            style={{
              left: Math.min(tooltipPos.x + 16, (containerRef.current?.clientWidth || 800) - 260),
              top: Math.min(tooltipPos.y + 16, (containerRef.current?.clientHeight || 600) - 180),
              maxWidth: 240,
              zIndex: 100,
              borderColor: hoveredNode.color + '40',
            }}
          >
            <div className="flex items-center gap-2 mb-1">
              <span className="w-2 h-2 rounded-sm" style={{ background: hoveredNode.color }} />
              <span className="text-sm font-semibold" style={{ color: hoveredNode.color }}>
                {hoveredNode.label}
              </span>
              {hoveredNode.dims && (
                <span className="font-data text-xs ml-auto" style={{ color: 'var(--text-muted)' }}>
                  {hoveredNode.dims}
                </span>
              )}
            </div>
            {hoveredNode.detail && (
              <pre className="text-xs font-data whitespace-pre-wrap mt-1" style={{ color: 'var(--text-muted)', lineHeight: 1.4 }}>
                {hoveredNode.detail}
              </pre>
            )}
            {hoveredNode.navigateTo && (
              <div className="text-xs mt-2 pt-1" style={{ borderTop: '1px solid rgba(255,255,255,0.06)', color: hoveredNode.color }}>
                Click to explore \u203A
              </div>
            )}
          </div>
        )}
      </div>

      {/* Bottom status */}
      <div className="flex items-center justify-between px-4 py-1.5" style={{ background: 'rgba(255,255,255,0.015)' }}>
        <div className="flex items-center gap-3">
          {[
            { label: 'R\u00B3', color: colors.r3 },
            { label: 'H\u00B3', color: colors.h3 },
            { label: 'C\u00B3', color: colors.c3 },
            { label: 'Reward', color: colors.reward },
          ].map(l => (
            <span key={l.label} className="flex items-center gap-1 text-xs">
              <span className="w-1.5 h-1.5 rounded-sm" style={{ background: l.color }} />
              <span style={{ color: l.color + '90' }}>{l.label}</span>
            </span>
          ))}
        </div>
        <span className="font-data text-[10px]" style={{ color: 'var(--text-muted)' }}>
          {Math.round(camera.zoom * 100)}% \u00B7 Pan: drag \u00B7 Zoom: scroll \u00B7 Click: explore
        </span>
      </div>
    </div>
  );
}
