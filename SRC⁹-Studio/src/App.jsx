import React, { useState, useEffect, useRef, useCallback } from 'react';
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

// ─── Arc Gauge ───
function ArcGauge({ value = 0, size = 48, color = '#fff', label = '' }) {
  const sw = 2.5, r = (size - sw * 2) / 2, circ = 2 * Math.PI * r;
  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth={sw} />
        <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={sw}
          strokeDasharray={circ} strokeDashoffset={circ * (1 - Math.min(1, Math.max(0, value)))}
          strokeLinecap="round" style={{ transition: 'stroke-dashoffset 0.12s ease-out' }} />
      </svg>
      <span className="text-[9px] text-white/40 tracking-wider uppercase">{label}</span>
    </div>
  );
}

// ─── Horizontal Bar ───
function HBar({ value = 0, color = '#fff', label = '' }) {
  return (
    <div className="flex items-center gap-3 w-full">
      <span className="text-[10px] text-white/35 w-20 text-right tracking-wide uppercase shrink-0">{label}</span>
      <div className="flex-1 h-[3px] rounded-full bg-white/[0.06] overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${Math.min(100, value * 100)}%`, background: color, transition: 'width 0.12s ease-out' }} />
      </div>
      <span className="text-[9px] text-white/20 w-7 shrink-0">{(value * 100).toFixed(0)}</span>
    </div>
  );
}

// ─── Dot Indicator ───
function Dot({ value = 0, color = '#fff', label = '' }) {
  return (
    <div className="flex items-center gap-2">
      <div className="w-2 h-2 rounded-full" style={{ background: color, opacity: 0.15 + value * 0.85, boxShadow: value > 0.5 ? `0 0 ${value*12}px ${color}` : 'none', transition: 'all 0.12s' }} />
      <span className="text-[10px] text-white/30">{label}</span>
      <span className="text-[10px] text-white/15 ml-auto">{(value * 100).toFixed(0)}</span>
    </div>
  );
}

// ─── Polarity Axis ───
function Polarity({ value = 0.5, left = '', right = '', color = 'rgba(255,255,255,0.3)' }) {
  return (
    <div className="flex items-center gap-2 w-full">
      <span className="text-[9px] text-white/25 w-14 text-right shrink-0">{left}</span>
      <div className="flex-1 h-[2px] bg-white/[0.06] rounded-full relative">
        <div className="absolute top-1/2 w-2 h-2 rounded-full" style={{ left: `${value*100}%`, transform: 'translate(-50%,-50%)', background: color, boxShadow: `0 0 8px ${color}`, transition: 'left 0.2s' }} />
      </div>
      <span className="text-[9px] text-white/25 w-14 shrink-0">{right}</span>
    </div>
  );
}

// ─── C³ Brain HUD (right side) ───
function BrainHUD({ frame, dims }) {
  if (!frame || !dims) return null;
  const v = {};
  dims.forEach((name, i) => { v[name] = frame[i] || 0; });

  return (
    <Glass className="p-5 w-64">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">C³</span>
        <span className="text-[9px] text-white/20">Brain</span>
      </div>

      <div className="text-[8px] text-white/20 uppercase tracking-widest mb-2">Reward</div>
      <div className="flex justify-between mb-4">
        <ArcGauge value={v.pleasure || 0} size={48} color="rgba(253,224,71,0.7)" label="Plsr" />
        <ArcGauge value={v.wanting || 0} size={48} color="rgba(252,211,77,0.7)" label="Want" />
        <ArcGauge value={v.liking || 0} size={48} color="rgba(253,186,116,0.7)" label="Like" />
      </div>
      <div className="space-y-1.5 mb-3">
        <Dot value={v.da_nacc || 0} color="rgba(253,224,71,0.7)" label="DA NAcc" />
        <Dot value={v.da_caudate || 0} color="rgba(252,211,77,0.6)" label="DA Caudate" />
        <Dot value={v.opioid_proxy || 0} color="rgba(196,181,253,0.7)" label="Opioid" />
      </div>

      <div className="text-[8px] text-white/20 uppercase tracking-widest mb-2 mt-3">Affect</div>
      <div className="space-y-2">
        <HBar value={v.f03_valence || 0} color="rgba(147,197,253,0.5)" label="Valence" />
        <HBar value={v.happy_pathway || 0} color="rgba(253,186,116,0.5)" label="Happy" />
        <HBar value={v.sad_pathway || 0} color="rgba(147,197,253,0.5)" label="Sad" />
        <HBar value={v.tension || 0} color="rgba(252,165,165,0.5)" label="Tension" />
      </div>

      <div className="mt-3 pt-3 border-t border-white/[0.04] flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px]" style={{ opacity: 0.3 + (v.hr || 0) * 0.7 }}>&#9825;</span>
          <span className="text-[10px] text-white/25">HR {((v.hr || 0) * 100).toFixed(0)}</span>
        </div>
        {(v.chills_intensity || 0) > 0.1 && (
          <div className="flex items-center gap-1">
            <span className="text-[10px] text-amber-300" style={{ opacity: 0.4 + v.chills_intensity * 0.6 }}>&#9889;</span>
            <span className="text-[9px] text-white/30">chills</span>
          </div>
        )}
      </div>
    </Glass>
  );
}

// ─── R³ Spectral HUD (left side) ───
function SpectralHUD({ summary }) {
  if (!summary) return null;
  return (
    <Glass className="p-5 w-64">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">R³</span>
        <span className="text-[9px] text-white/20">Spectral</span>
      </div>
      <div className="flex justify-between mb-5">
        <ArcGauge value={summary.rms} size={52} color="rgba(252,211,77,0.7)" label="RMS" />
        <ArcGauge value={summary.brightness} size={52} color="rgba(253,186,116,0.7)" label="Bri" />
        <ArcGauge value={summary.peakAmplitude} size={52} color="rgba(252,165,165,0.7)" label="Peak" />
      </div>
      <div className="space-y-2.5">
        <HBar value={summary.lowEnergy} color="rgba(252,165,165,0.5)" label="Low 20-250" />
        <HBar value={summary.midEnergy} color="rgba(253,224,71,0.5)" label="Mid 250-2k" />
        <HBar value={summary.highEnergy} color="rgba(147,197,253,0.5)" label="High 2k-4k" />
      </div>
      <div className="mt-3 text-[9px] text-white/15">
        Centroid {summary.centroid.toFixed(0)} Hz
      </div>
    </Glass>
  );
}

// ─── L³ Integration HUD (bottom) ───
function IntegrationHUD({ frame, dims }) {
  if (!frame || !dims) return null;
  const v = {};
  dims.forEach((name, i) => { v[name] = frame[i] || 0; });

  return (
    <Glass className="px-6 py-4" style={{ maxWidth: 520 }}>
      <div className="flex items-center gap-2 mb-3">
        <span className="text-[11px] font-semibold tracking-[0.2em] text-white/50 uppercase">L³</span>
        <span className="text-[9px] text-white/20">Integration</span>
      </div>
      <div className="space-y-2.5">
        <Polarity value={v.arousal || 0} left="calm" right="aroused" color="rgba(252,165,165,0.5)" />
        <Polarity value={v.f03_valence || 0} left="negative" right="positive" color="rgba(253,224,71,0.5)" />
        <Polarity value={v.tension || 0} left="relaxed" right="tense" color="rgba(253,186,116,0.5)" />
        <Polarity value={v.beauty || 0} left="ordinary" right="beautiful" color="rgba(167,243,208,0.5)" />
      </div>
      <div className="mt-3 pt-3 border-t border-white/[0.04]">
        <div className="flex items-center justify-between mb-1">
          <span className="text-[8px] text-white/20 uppercase tracking-wider">Emotional Arc</span>
          <span className="text-[9px] text-white/15">{((v.emotional_arc || 0) * 100).toFixed(0)}%</span>
        </div>
        <div className="h-[2px] rounded-full bg-white/[0.04] relative">
          <div className="absolute top-1/2 w-6 h-[2px] rounded-full bg-white/20"
            style={{ left: `${(v.emotional_arc || 0) * 100}%`, transform: 'translate(-50%,-50%)', transition: 'left 0.2s' }} />
        </div>
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
        {playing ? '⏸' : '▶'}
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
  const brainDataRef = useRef(null);
  const hudRafRef = useRef(null);
  const startTimeRef = useRef(0);

  const [appState, setAppState] = useState('landing');
  const [brainFrame, setBrainFrame] = useState(null);
  const [brainDims, setBrainDims] = useState(null);
  const [spectralSummary, setSpectralSummary] = useState(null);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [playing, setPlaying] = useState(false);

  const startHudLoop = useCallback(() => {
    const tick = () => {
      const elapsed = (performance.now() - startTimeRef.current) / 1000;
      const brain = brainDataRef.current;
      if (brain) {
        const idx = Math.min(brain.brain.shape[0] - 1, Math.floor(elapsed * brain.meta.frame_rate));
        setBrainFrame(brain.brain.values[idx]);
        setProgress(Math.min(1, elapsed / brain.meta.duration_s));
      }
      if (analyzerRef.current) setSpectralSummary(analyzerRef.current.getSummary());
      hudRafRef.current = requestAnimationFrame(tick);
    };
    hudRafRef.current = requestAnimationFrame(tick);
  }, []);

  const start = useCallback(async () => {
    setAppState('loading');

    // Fluid
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

    // Brain data
    const res = await fetch('/audio/swan-lake-brain.json');
    const brain = await res.json();
    brainDataRef.current = brain;
    setBrainDims(brain.brain.dimensions);
    setDuration(brain.meta.duration_s);

    // Audio
    const analyzer = new AudioAnalyzer(fluidRef.current, {
      fftSize: 4096, minFreq: 20, maxFreq: 4000, splatsPerFrame: 24,
    });
    await analyzer.load('/audio/swan-lake.wav');
    analyzerRef.current = analyzer;

    setAppState('playing');
    setPlaying(true);
    analyzer.play();
    startTimeRef.current = performance.now();
    startHudLoop();
  }, [startHudLoop]);

  const togglePlay = useCallback(() => {
    if (!analyzerRef.current) return;
    if (playing) {
      analyzerRef.current.pause();
      if (hudRafRef.current) cancelAnimationFrame(hudRafRef.current);
    } else {
      analyzerRef.current.play();
      startTimeRef.current = performance.now() - progress * duration * 1000;
      startHudLoop();
    }
    setPlaying(!playing);
  }, [playing, progress, duration, startHudLoop]);

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

            {/* R³ left */}
            <motion.div className="fixed left-5 top-1/2 -translate-y-1/2 z-50"
              initial={{ opacity: 0, x: -30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.15 }}>
              <SpectralHUD summary={spectralSummary} />
            </motion.div>

            {/* C³ right */}
            <motion.div className="fixed right-5 top-1/2 -translate-y-1/2 z-50"
              initial={{ opacity: 0, x: 30 }} animate={{ opacity: 1, x: 0 }} transition={{ duration: 0.5, delay: 0.2 }}>
              <BrainHUD frame={brainFrame} dims={brainDims} />
            </motion.div>

            {/* L³ bottom */}
            <motion.div className="fixed bottom-16 left-1/2 -translate-x-1/2 z-50"
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5, delay: 0.25 }}>
              <IntegrationHUD frame={brainFrame} dims={brainDims} />
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
