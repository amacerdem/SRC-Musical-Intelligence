import React, { useState, useEffect, useRef, useCallback, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import PavelFluidSimulation from './engine/PavelFluidSimulation.js';
import AudioAnalyzer from './audio/AudioAnalyzer.js';

// ─── Glass Panel ───
function Glass({ children, className = '', style = {} }) {
  return (
    <div className={`rounded-3xl border border-white/[0.08] ${className}`}
      style={{
        background: 'linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01))',
        backdropFilter: 'blur(40px) saturate(1.2)',
        WebkitBackdropFilter: 'blur(40px) saturate(1.2)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05)',
        ...style,
      }}>{children}</div>
  );
}

// ─── Sparkline with past-present-future ───
// Shows a sliding time window: past = solid colored, future = dimmed
// `column` = full Float32Array for this dimension
// `frameIdx` = current playback frame
// `windowFrames` = how many frames to show on each side of "now"
// `min`/`max` = dimension value range for normalization
function Sparkline({
  column, frameIdx, windowFrames = 1700,
  min = 0, max = 1, color = 'rgba(255,255,255,0.5)',
  label = '', bipolar = false, height = 26, width = 180,
}) {
  if (!column || column.length === 0) return null;

  const totalFrames = column.length;
  const startFrame = Math.max(0, frameIdx - windowFrames);
  const endFrame = Math.min(totalFrames - 1, frameIdx + windowFrames);
  const windowSize = endFrame - startFrame;
  if (windowSize <= 0) return null;

  // Downsample to ~90 points for SVG performance
  const points = 90;
  const step = Math.max(1, Math.floor(windowSize / points));
  const range = max - min || 1;

  // Build SVG path data
  const pathPoints = [];
  for (let i = startFrame; i <= endFrame; i += step) {
    const x = ((i - startFrame) / windowSize) * width;
    const normalized = (column[i] - min) / range;
    const y = height - Math.min(1, Math.max(0, normalized)) * height;
    pathPoints.push({ x, y, frame: i });
  }

  // Split into past and future at the "now" position
  const nowX = ((frameIdx - startFrame) / windowSize) * width;
  const nowNorm = (column[frameIdx] - min) / range;
  const nowY = height - Math.min(1, Math.max(0, nowNorm)) * height;
  const currentVal = column[frameIdx];

  // Build past path (up to and including now)
  const pastPts = pathPoints.filter(p => p.frame <= frameIdx);
  pastPts.push({ x: nowX, y: nowY, frame: frameIdx });
  const pastD = pastPts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

  // Build future path (from now onward)
  const futurePts = [{ x: nowX, y: nowY, frame: frameIdx }];
  futurePts.push(...pathPoints.filter(p => p.frame > frameIdx));
  const futureD = futurePts.map((p, i) => `${i === 0 ? 'M' : 'L'}${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ');

  // Format display value
  let displayVal;
  if (bipolar) {
    displayVal = (currentVal >= 0 ? '+' : '') + currentVal.toFixed(2);
  } else {
    displayVal = currentVal.toFixed(2);
  }

  return (
    <div className="flex items-center gap-2 w-full">
      <span className="text-[9px] text-white/30 w-[70px] text-right shrink-0 tracking-wide uppercase">{label}</span>
      <svg width={width} height={height} className="shrink-0" style={{ overflow: 'visible' }}>
        {/* Baseline for bipolar dimensions */}
        {bipolar && (
          <line x1={0} y1={height / 2} x2={width} y2={height / 2}
            stroke="rgba(255,255,255,0.06)" strokeWidth={0.5} />
        )}
        {/* Past — solid */}
        <path d={pastD} fill="none" stroke={color} strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round" />
        {/* Future — dimmed */}
        <path d={futureD} fill="none" stroke={color} strokeWidth={1} strokeLinecap="round" strokeLinejoin="round"
          opacity={0.2} strokeDasharray="3,2" />
        {/* Now dot */}
        <circle cx={nowX} cy={nowY} r={3} fill={color} opacity={0.9}>
          <animate attributeName="r" values="3;4;3" dur="1.5s" repeatCount="indefinite" />
        </circle>
        {/* Now vertical line */}
        <line x1={nowX} y1={0} x2={nowX} y2={height}
          stroke="rgba(255,255,255,0.08)" strokeWidth={0.5} />
      </svg>
      <span className="text-[9px] text-white/20 w-10 shrink-0 text-right tabular-nums">{displayVal}</span>
    </div>
  );
}

// ─── Section Header ───
function SectionHeader({ label }) {
  return (
    <div className="text-[8px] text-white/15 uppercase tracking-[0.2em] mt-3 mb-1.5 first:mt-0">{label}</div>
  );
}

// ─── R³ HUD (left) — perceptual / spectral brain dimensions ───
function R3HUD({ columns, dimMap, frameIdx, windowFrames }) {
  if (!columns || !dimMap) return null;

  // Value ranges from data analysis (for proper normalization)
  const dims = [
    { key: 'arousal',           label: 'Arousal',    color: 'rgba(252,165,165,0.7)', min: 0,    max: 1,    group: 'state' },
    { key: 'tension',           label: 'Tension',    color: 'rgba(253,186,116,0.7)', min: 0,    max: 1,    group: 'state' },
    { key: 'prediction_error',  label: 'Pred Error', color: 'rgba(252,165,165,0.6)', min: -0.8, max: 1,    group: 'prediction', bipolar: true },
    { key: 'prediction_match',  label: 'Pred Match', color: 'rgba(147,197,253,0.6)', min: -1,   max: 1,    group: 'prediction', bipolar: true },
    { key: 'harmonic_context',  label: 'Harmony',    color: 'rgba(167,243,208,0.6)', min: 0.75, max: 0.95, group: 'harmony' },
    { key: 'consonance_valence',label: 'Consonance', color: 'rgba(167,243,208,0.5)', min: 0.15, max: 0.8,  group: 'harmony' },
    { key: 'mode_signal',       label: 'Mode',       color: 'rgba(253,224,71,0.5)',  min: 0.15, max: 0.7,  group: 'harmony' },
    { key: 'emotional_momentum',label: 'Momentum',   color: 'rgba(196,181,253,0.6)', min: -0.8, max: 1,    group: 'dynamics', bipolar: true },
  ];

  let lastGroup = '';

  return (
    <Glass className="p-4 w-[340px]">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">R³</span>
        <span className="text-[9px] text-white/20">Spectral</span>
      </div>
      <div className="space-y-1">
        {dims.map((dim) => {
          const colIdx = dimMap[dim.key];
          if (colIdx === undefined) return null;
          const showHeader = dim.group !== lastGroup;
          lastGroup = dim.group;
          return (
            <React.Fragment key={dim.key}>
              {showHeader && <SectionHeader label={dim.group} />}
              <Sparkline
                column={columns[colIdx]}
                frameIdx={frameIdx}
                windowFrames={windowFrames}
                min={dim.min}
                max={dim.max}
                color={dim.color}
                label={dim.label}
                bipolar={dim.bipolar}
              />
            </React.Fragment>
          );
        })}
      </div>
    </Glass>
  );
}

// ─── C³ HUD (right) — cognitive / reward brain dimensions ───
function C3HUD({ columns, dimMap, frameIdx, windowFrames }) {
  if (!columns || !dimMap) return null;

  const dims = [
    { key: 'pleasure',         label: 'Pleasure',   color: 'rgba(253,224,71,0.7)',  min: 0,    max: 0.8,  group: 'reward' },
    { key: 'wanting',          label: 'Wanting',    color: 'rgba(252,211,77,0.6)',  min: 0,    max: 0.65, group: 'reward' },
    { key: 'liking',           label: 'Liking',     color: 'rgba(253,186,116,0.6)', min: 0.15, max: 0.75, group: 'reward' },
    { key: 'da_nacc',          label: 'DA NAcc',    color: 'rgba(253,224,71,0.5)',  min: 0.18, max: 0.87, group: 'neuro' },
    { key: 'da_caudate',       label: 'DA Caudate', color: 'rgba(252,211,77,0.5)',  min: 0,    max: 0.9,  group: 'neuro' },
    { key: 'opioid_proxy',     label: 'Opioid',     color: 'rgba(196,181,253,0.5)', min: 0.74, max: 0.94, group: 'neuro' },
    { key: 'happy_pathway',    label: 'Happy',      color: 'rgba(253,186,116,0.5)', min: 0.35, max: 0.77, group: 'affect' },
    { key: 'sad_pathway',      label: 'Sad',        color: 'rgba(147,197,253,0.5)', min: 0.27, max: 0.73, group: 'affect' },
    { key: 'beauty',           label: 'Beauty',     color: 'rgba(167,243,208,0.6)', min: 0.13, max: 0.68, group: 'aesthetic' },
    { key: 'chills_intensity', label: 'Chills',     color: 'rgba(253,224,71,0.7)',  min: 0,    max: 0.75, group: 'aesthetic' },
    { key: 'emotional_arc',    label: 'Emo Arc',    color: 'rgba(196,181,253,0.5)', min: 0.2,  max: 0.8,  group: 'aesthetic' },
  ];

  let lastGroup = '';

  return (
    <Glass className="p-4 w-[340px]">
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">C³</span>
        <span className="text-[9px] text-white/20">Brain</span>
      </div>
      <div className="space-y-1">
        {dims.map((dim) => {
          const colIdx = dimMap[dim.key];
          if (colIdx === undefined) return null;
          const showHeader = dim.group !== lastGroup;
          lastGroup = dim.group;
          return (
            <React.Fragment key={dim.key}>
              {showHeader && <SectionHeader label={dim.group} />}
              <Sparkline
                column={columns[colIdx]}
                frameIdx={frameIdx}
                windowFrames={windowFrames}
                min={dim.min}
                max={dim.max}
                color={dim.color}
                label={dim.label}
                bipolar={dim.bipolar}
              />
            </React.Fragment>
          );
        })}
      </div>
    </Glass>
  );
}

// ─── L³ Narration — real-time text from brain data ───
function generateNarration(columns, dimMap, frameIdx) {
  if (!columns || !dimMap || frameIdx == null) return [];

  const v = (key) => {
    const idx = dimMap[key];
    return idx !== undefined ? columns[idx][frameIdx] : 0;
  };

  // Rate of change (compare to 1 second ago ~172 frames)
  const delta = (key, lookback = 172) => {
    const idx = dimMap[key];
    if (idx === undefined) return 0;
    const prev = Math.max(0, frameIdx - lookback);
    return columns[idx][frameIdx] - columns[idx][prev];
  };

  const lines = [];

  // Arousal state
  const arousal = v('arousal');
  if (arousal > 0.85) lines.push({ text: 'High arousal — intense passage', color: 'rgba(252,165,165,0.6)' });
  else if (arousal < 0.15) lines.push({ text: 'Low arousal — calm, restful', color: 'rgba(147,197,253,0.4)' });
  else if (delta('arousal') > 0.15) lines.push({ text: 'Arousal rising rapidly', color: 'rgba(252,165,165,0.5)' });
  else if (delta('arousal') < -0.15) lines.push({ text: 'Arousal subsiding', color: 'rgba(147,197,253,0.4)' });

  // Tension
  const tension = v('tension');
  if (tension > 0.7) lines.push({ text: 'Strong harmonic tension', color: 'rgba(253,186,116,0.6)' });
  else if (tension < 0.15) lines.push({ text: 'Tension resolved', color: 'rgba(167,243,208,0.5)' });
  if (delta('tension') > 0.1) lines.push({ text: 'Tension building...', color: 'rgba(253,186,116,0.5)' });

  // Prediction
  const predErr = v('prediction_error');
  const predMatch = v('prediction_match');
  if (predErr > 0.6) lines.push({ text: 'Musical surprise — unexpected turn', color: 'rgba(252,165,165,0.6)' });
  else if (predErr < -0.4) lines.push({ text: 'Below expectation — anticlimax', color: 'rgba(147,197,253,0.4)' });
  if (predMatch > 0.8) lines.push({ text: 'Expectation confirmed — familiar pattern', color: 'rgba(167,243,208,0.5)' });
  else if (predMatch < -0.5) lines.push({ text: 'Strong deviation from expected', color: 'rgba(253,186,116,0.5)' });

  // Reward / Pleasure
  const pleasure = v('pleasure');
  const wanting = v('wanting');
  if (pleasure > 0.55) lines.push({ text: 'Peak pleasure response', color: 'rgba(253,224,71,0.7)' });
  if (wanting > 0.4 && pleasure < 0.2) lines.push({ text: 'Anticipation without resolution', color: 'rgba(252,211,77,0.5)' });
  if (delta('pleasure') > 0.12) lines.push({ text: 'Pleasure surge detected', color: 'rgba(253,224,71,0.6)' });

  // Dopamine
  const daNacc = v('da_nacc');
  const daCaudate = v('da_caudate');
  if (daCaudate > 0.6 && daNacc > 0.7) lines.push({ text: 'Dopamine surge — reward circuitry active', color: 'rgba(253,224,71,0.5)' });

  // Chills
  const chills = v('chills_intensity');
  if (chills > 0.4) lines.push({ text: 'Chills moment', color: 'rgba(253,224,71,0.8)' });
  else if (chills > 0.2) lines.push({ text: 'Mild frisson sensation', color: 'rgba(253,224,71,0.4)' });

  // Happy / Sad pathway balance
  const happy = v('happy_pathway');
  const sad = v('sad_pathway');
  if (happy > 0.65 && sad < 0.4) lines.push({ text: 'Joyful character — major mode dominance', color: 'rgba(253,186,116,0.5)' });
  else if (sad > 0.65 && happy < 0.4) lines.push({ text: 'Melancholic passage — minor tonality', color: 'rgba(147,197,253,0.5)' });
  else if (Math.abs(happy - sad) < 0.05) lines.push({ text: 'Mixed emotional quality — ambiguity', color: 'rgba(196,181,253,0.5)' });

  // Beauty
  const beauty = v('beauty');
  if (beauty > 0.55) lines.push({ text: 'Aesthetically beautiful moment', color: 'rgba(167,243,208,0.6)' });

  // Emotional momentum
  const momentum = v('emotional_momentum');
  if (momentum > 0.4) lines.push({ text: 'Building toward climax', color: 'rgba(196,181,253,0.6)' });
  else if (momentum < -0.4) lines.push({ text: 'Gradual emotional descent', color: 'rgba(196,181,253,0.4)' });

  // Harmony
  const consonance = v('consonance_valence');
  if (consonance > 0.65) lines.push({ text: 'Rich consonance — harmonic clarity', color: 'rgba(167,243,208,0.5)' });
  else if (consonance < 0.3) lines.push({ text: 'Dissonant harmony — chromatic tension', color: 'rgba(253,186,116,0.4)' });

  // Emotional arc
  const arc = v('emotional_arc');
  if (arc > 0.7) lines.push({ text: 'Narrative peak — emotional climax zone', color: 'rgba(196,181,253,0.6)' });
  else if (arc < 0.3) lines.push({ text: 'Opening / resolution — arc baseline', color: 'rgba(196,181,253,0.4)' });

  // Limit to 4 most relevant lines
  return lines.slice(0, 4);
}

function L3HUD({ columns, dimMap, frameIdx }) {
  // Throttle narration to every ~0.5s (every ~86 frames at 172Hz)
  const lastNarrationFrame = useRef(0);
  const [lines, setLines] = useState([]);

  if (frameIdx - lastNarrationFrame.current > 86 || lines.length === 0) {
    const newLines = generateNarration(columns, dimMap, frameIdx);
    if (newLines.length > 0) {
      lastNarrationFrame.current = frameIdx;
      // Only update state if lines actually changed (avoid unnecessary re-renders)
      const changed = newLines.length !== lines.length ||
        newLines.some((l, i) => !lines[i] || l.text !== lines[i].text);
      if (changed) setLines(newLines);
    }
  }

  if (lines.length === 0) return null;

  return (
    <Glass className="px-5 py-3" style={{ maxWidth: 500 }}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">L³</span>
        <span className="text-[9px] text-white/20">Narration</span>
      </div>
      <div className="space-y-1">
        {lines.map((line, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className="w-1 h-1 rounded-full shrink-0" style={{ background: line.color }} />
            <span className="text-[10px] tracking-wide" style={{ color: line.color }}>{line.text}</span>
          </div>
        ))}
      </div>
    </Glass>
  );
}

// ─── Playback Bar ───
function PlaybackBar({ progress, duration, playing, onToggle }) {
  const fmt = (s) => `${Math.floor(s/60)}:${String(Math.floor(s%60)).padStart(2,'0')}`;
  return (
    <Glass className="px-4 py-2 flex items-center gap-4" style={{ minWidth: 320 }}>
      <button onClick={onToggle} className="text-white/40 hover:text-white/70 transition-colors text-sm w-6 text-center">
        {playing ? '\u23F8' : '\u25B6'}
      </button>
      <div className="flex-1 h-[2px] bg-white/[0.06] rounded-full relative">
        <div className="h-full rounded-full bg-white/20" style={{ width: `${progress * 100}%`, transition: 'width 0.1s' }} />
      </div>
      <span className="text-[10px] text-white/25 w-24 text-right">{fmt(progress * duration)} / {fmt(duration)}</span>
    </Glass>
  );
}

// ─── Main App ───
export default function App() {
  const canvasRef = useRef(null);
  const fluidRef = useRef(null);
  const analyzerRef = useRef(null);
  const brainRef = useRef(null);      // raw brain JSON
  const columnsRef = useRef(null);    // per-dimension columns [Float64Array x 26]
  const hudRafRef = useRef(null);

  const [appState, setAppState] = useState('landing');
  const [dimMap, setDimMap] = useState(null);     // { name: index }
  const [columns, setColumns] = useState(null);   // array of Float64Arrays
  const [frameIdx, setFrameIdx] = useState(0);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playing, setPlaying] = useState(false);

  // ~10 seconds of context at 172.27 Hz
  const windowFrames = 1723;

  const startHudLoop = useCallback(() => {
    const tick = () => {
      const analyzer = analyzerRef.current;
      const brain = brainRef.current;

      if (analyzer && brain) {
        const elapsed = analyzer.elapsed;
        const idx = Math.min(
          brain.brain.shape[0] - 1,
          Math.floor(elapsed * brain.meta.frame_rate)
        );
        setFrameIdx(idx);
        setProgress(Math.min(1, elapsed / brain.meta.duration_s));
      }

      hudRafRef.current = requestAnimationFrame(tick);
    };
    hudRafRef.current = requestAnimationFrame(tick);
  }, []);

  const start = useCallback(async () => {
    setAppState('loading');

    // Fluid simulation
    if (!fluidRef.current && canvasRef.current) {
      fluidRef.current = new PavelFluidSimulation(canvasRef.current, {
        SIM_RESOLUTION: 256, DYE_RESOLUTION: 1024,
        DENSITY_DISSIPATION: 0.97, VELOCITY_DISSIPATION: 0.98,
        CURL: 25, SPLAT_RADIUS: 0.15, SPLAT_FORCE: 4000,
        BLOOM: true, BLOOM_INTENSITY: 0.012, BLOOM_THRESHOLD: 2.5,
        SUNRAYS: true, SUNRAYS_WEIGHT: 0.6,
        PRESSURE: 0.8, PRESSURE_ITERATIONS: 20,
        PARTICLES_ENABLED: true, PARTICLE_BRIGHTNESS: 1.0,
        GRID_ENABLED: true, GRID_INTENSITY: 8.0, GRID_ALPHA: 0.4,
        CAMERA_AUTO_ROTATE: true, CAMERA_ROTATION_PERIOD: 60,
      });
    }

    // Brain data → extract per-dimension columns for sparklines
    const brainRes = await fetch('/audio/swan-lake-brain.json');
    const brain = await brainRes.json();
    brainRef.current = brain;
    setDuration(brain.meta.duration_s);

    const dims = brain.brain.dimensions;
    const map = {};
    dims.forEach((name, i) => { map[name] = i; });
    setDimMap(map);

    // Extract columns: dims × frames → frames[dim] as Float64Array
    const numFrames = brain.brain.shape[0];
    const numDims = brain.brain.shape[1];
    const cols = [];
    for (let d = 0; d < numDims; d++) {
      const col = new Float64Array(numFrames);
      for (let f = 0; f < numFrames; f++) {
        col[f] = brain.brain.values[f][d];
      }
      cols.push(col);
    }
    columnsRef.current = cols;
    setColumns(cols);

    // Audio analyzer (precomputed FFT + playback)
    const analyzer = new AudioAnalyzer(fluidRef.current, {
      splatsPerFrame: 20,
      brightness: 0.05,
    });
    await Promise.all([
      analyzer.loadFFT('/audio/swan-lake-fft.json'),
      analyzer.loadAudio('/audio/swan-lake.wav'),
    ]);
    analyzerRef.current = analyzer;

    setAppState('playing');
    setPlaying(true);
    analyzer.play();
    startHudLoop();
  }, [startHudLoop]);

  const togglePlay = useCallback(() => {
    const analyzer = analyzerRef.current;
    if (!analyzer) return;

    if (playing) {
      analyzer.pause();
      if (hudRafRef.current) cancelAnimationFrame(hudRafRef.current);
    } else {
      analyzer.play();
      startHudLoop();
    }
    setPlaying(!playing);
  }, [playing, startHudLoop]);

  useEffect(() => {
    return () => {
      if (hudRafRef.current) cancelAnimationFrame(hudRafRef.current);
      analyzerRef.current?.destroy();
      fluidRef.current?.cleanup?.();
    };
  }, []);

  return (
    <div className="w-full h-full bg-black relative overflow-hidden">
      {/* Fluid canvas */}
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full"
        style={{ display: appState === 'landing' ? 'none' : 'block' }} />

      {/* Landing */}
      <AnimatePresence>
        {appState === 'landing' && (
          <motion.div className="absolute inset-0 flex flex-col items-center justify-center"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0, scale: 0.97 }} transition={{ duration: 0.6 }}>
            <h1 className="text-[clamp(2rem,5vw,4rem)] font-light tracking-[0.3em] text-white/90 mb-3">
              SRC<sup className="text-[0.5em] relative -top-[0.5em]">9</sup>
            </h1>
            <p className="text-[clamp(0.7rem,1.5vw,0.85rem)] tracking-[0.5em] text-white/25 uppercase mb-16">Studio</p>
            <button onClick={start} className="group">
              <Glass className="px-12 py-6 cursor-pointer transition-all duration-300 hover:border-white/[0.15]">
                <span className="text-[13px] tracking-[0.25em] text-white/50 uppercase group-hover:text-white/70 transition-colors">
                  Swan Lake
                </span>
                <p className="text-[9px] text-white/15 mt-2 tracking-wider">Tchaikovsky &middot; Analyze</p>
              </Glass>
            </button>
            <p className="mt-20 text-[9px] text-white/10 tracking-[0.3em]">v0.1.0</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Loading */}
      <AnimatePresence>
        {appState === 'loading' && (
          <motion.div className="absolute inset-0 flex items-center justify-center z-50"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
            <span className="text-[11px] text-white/30 tracking-[0.3em] uppercase animate-pulse">Loading Swan Lake...</span>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Playing HUD */}
      <AnimatePresence>
        {appState === 'playing' && (
          <>
            {/* Mode badge */}
            <motion.div className="fixed top-5 left-1/2 -translate-x-1/2 z-50"
              initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}>
              <Glass className="px-4 py-1.5 flex items-center gap-3">
                <span className="text-[10px] text-white/30 tracking-[0.15em] uppercase">Analyze</span>
                <div className="w-1 h-1 rounded-full bg-green-400/60" style={{ boxShadow: '0 0 6px rgba(74,222,128,0.4)' }} />
              </Glass>
            </motion.div>

            {/* R³ — left */}
            <motion.div className="fixed left-4 top-1/2 -translate-y-1/2 z-50"
              initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.15 }}>
              <R3HUD columns={columns} dimMap={dimMap} frameIdx={frameIdx} windowFrames={windowFrames} />
            </motion.div>

            {/* C³ — right */}
            <motion.div className="fixed right-4 top-1/2 -translate-y-1/2 z-50"
              initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
              <C3HUD columns={columns} dimMap={dimMap} frameIdx={frameIdx} windowFrames={windowFrames} />
            </motion.div>

            {/* L³ — bottom narration */}
            <motion.div className="fixed bottom-16 left-1/2 -translate-x-1/2 z-50"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.25 }}>
              <L3HUD columns={columns} dimMap={dimMap} frameIdx={frameIdx} />
            </motion.div>

            {/* Playback bar */}
            <motion.div className="fixed bottom-5 left-1/2 -translate-x-1/2 z-50"
              initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
              <PlaybackBar progress={progress} duration={duration} playing={playing} onToggle={togglePlay} />
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
}
