/* ── SpectralPeaks — WebGL peak-based spectral visualization ─────────
 *  Renders extracted spectral peaks as glowing particles using R3F.
 *  OrthographicCamera pans horizontally for scrolling; all peak data
 *  is pre-computed and uploaded once as static BufferAttributes.
 *
 *  Layout: Piano Roll (Canvas 2D, 52px) | R3F Canvas (WebGL, flex-1)
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useState, useCallback, useMemo } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { EffectComposer, Bloom, Noise } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";
import * as THREE from "three";
import type { MelData, PeakBuffers } from "./peakExtractor";
import { extractPeaks, freqToColor } from "./peakExtractor";

/* ── Constants ───────────────────────────────────────────────────────── */

const PIANO_MIN_HZ = 27.5;
const PIANO_MAX_HZ = 4186.01;
const LOG2_MIN = Math.log2(PIANO_MIN_HZ);
const LOG2_MAX = Math.log2(PIANO_MAX_HZ);
const LOG2_RANGE = LOG2_MAX - LOG2_MIN;

const PIANO_KEYS_W = 44;     // px width of piano keys
const SPECTRUM_BAR_W = 10;   // px width of note-spectrum color bar
const PIANO_ROLL_W = PIANO_KEYS_W + SPECTRUM_BAR_W; // total left strip
const WINDOW_DURATION = 12;  // seconds visible
const PLAYHEAD_ANCHOR = 0.7;  // playhead at 70% from left
const POINT_SCALE_BASE = 18;  // base gl_PointSize multiplier

/* ── Piano key data ──────────────────────────────────────────────────── */

interface PianoKey {
  midi: number;
  name: string;
  octave: number;
  isBlack: boolean;
  freq: number;
}

function buildPianoKeys(): PianoKey[] {
  const NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
  const BLACK = new Set([1, 3, 6, 8, 10]);
  const keys: PianoKey[] = [];
  for (let midi = 21; midi <= 108; midi++) {
    const noteIdx = (midi - 12) % 12;
    const octave = Math.floor((midi - 12) / 12);
    const freq = 440 * Math.pow(2, (midi - 69) / 12);
    keys.push({ midi, name: NOTE_NAMES[noteIdx], octave, isBlack: BLACK.has(noteIdx), freq });
  }
  return keys;
}

const PIANO_KEYS = buildPianoKeys();

/* ── GLSL Shaders ────────────────────────────────────────────────────── */

const vertexShader = `
uniform float uMaxPeaks;
uniform float uPointScale;

attribute float aSize;
attribute float aRank;

varying vec3 vColor;
varying float vAlpha;

void main() {
  // Filter by peak count
  if (aRank >= uMaxPeaks || aSize < 0.01) {
    gl_Position = vec4(0.0, 0.0, -2.0, 1.0);
    gl_PointSize = 0.0;
    vColor = vec3(0.0);
    vAlpha = 0.0;
    return;
  }

  vec4 mvPos = modelViewMatrix * vec4(position, 1.0);
  gl_Position = projectionMatrix * mvPos;

  // Remap amplitude: raw 0-1 → compressed range with visible floor
  // Weakest visible peak (~0.04) → size 0.35, alpha 0.30
  // Strongest peak (1.0) → size 1.0, alpha 1.0
  float sizeRemap = 0.3 + aSize * 0.7;
  gl_PointSize = sizeRemap * uPointScale;

  vColor = color;
  vAlpha = 0.25 + aSize * 0.75;
}
`;

const fragmentShader = `
varying vec3 vColor;
varying float vAlpha;

void main() {
  float d = length(gl_PointCoord - 0.5) * 2.0;
  if (d > 1.0) discard;

  float core = smoothstep(0.3, 0.0, d);
  float glow = smoothstep(1.0, 0.0, d);

  // Preserve note color — only a tiny white highlight at the very center
  vec3 finalColor = mix(vColor, vec3(1.0), core * 0.15);
  float alpha = glow * vAlpha;

  // Moderate HDR for bloom — enough glow without washing out color
  gl_FragColor = vec4(finalColor * (1.0 + core * 1.0), alpha);
}
`;

/* ── PeakScene — inner R3F scene ─────────────────────────────────── */

interface PeakSceneProps {
  peaks: PeakBuffers;
  melDuration: number;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  accentColor: string;
  peakCount: 4 | 8 | 16;
  onSeek: (ratio: number) => void;
  duration: number;
}

function PeakScene({
  peaks, melDuration, audioRef, isPlaying,
  accentColor, peakCount, onSeek, duration,
}: PeakSceneProps) {
  const { camera, size: viewportSize } = useThree();
  const orthoCamera = camera as THREE.OrthographicCamera;

  const materialRef = useRef<THREE.ShaderMaterial | null>(null);
  const playheadRef = useRef<THREE.Group>(null);
  const gridGroupRef = useRef<THREE.Group>(null);

  // Scroll state (mutable refs for useFrame)
  const scrollRef = useRef(0);
  const targetScrollRef = useRef(0);

  /* ── Points geometry (static) ──────────────────────────── */
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(peaks.positions, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(peaks.colors, 3));
    geo.setAttribute("aSize", new THREE.BufferAttribute(peaks.sizes, 1));
    geo.setAttribute("aRank", new THREE.BufferAttribute(peaks.ranks, 1));
    // Bounding sphere for frustum culling — huge sphere so Three.js doesn't cull the whole object
    geo.boundingSphere = new THREE.Sphere(
      new THREE.Vector3(melDuration / 2, 0.5, 0),
      melDuration
    );
    return geo;
  }, [peaks, melDuration]);

  /* ── Shader material ─────────────────────────────────── */
  const material = useMemo(() => {
    return new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      uniforms: {
        uMaxPeaks: { value: peakCount },
        uPointScale: { value: POINT_SCALE_BASE },
      },
      vertexColors: true,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
    });
  }, []);

  /* ── Playhead line (THREE.Line object) ───────────────── */
  const playheadLine = useMemo(() => {
    const geo = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, -0.02, 0.1),
      new THREE.Vector3(0, 1.02, 0.1),
    ]);
    const mat = new THREE.LineBasicMaterial({
      color: new THREE.Color(accentColor),
      transparent: true,
      opacity: 0.9,
    });
    return new THREE.Line(geo, mat);
  }, [accentColor]);

  /* ── Grid line objects ────────────────────────────────── */
  const octaveLines = useMemo(() => {
    const gridMat = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.04,
    });
    const lines: THREE.Line[] = [];
    for (let oct = 1; oct <= 8; oct++) {
      const freq = 16.3516 * Math.pow(2, oct);
      if (freq < PIANO_MIN_HZ || freq > PIANO_MAX_HZ) continue;
      const y = (Math.log2(freq) - LOG2_MIN) / LOG2_RANGE;
      const geo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(-10, y, 0),
        new THREE.Vector3(melDuration + 10, y, 0),
      ]);
      lines.push(new THREE.Line(geo, gridMat));
    }
    return lines;
  }, [melDuration]);

  const timeLines = useMemo(() => {
    const gridMat = new THREE.LineBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.03,
    });
    const lines: THREE.Line[] = [];
    const maxTime = melDuration + WINDOW_DURATION;
    for (let t = 0; t <= maxTime; t += 2) {
      const geo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(t, 0, 0),
        new THREE.Vector3(t, 1, 0),
      ]);
      lines.push(new THREE.Line(geo, gridMat));
    }
    return lines;
  }, [melDuration]);

  /* ── Initialize camera ────────────────────────────── */
  useEffect(() => {
    orthoCamera.left = 0;
    orthoCamera.right = WINDOW_DURATION;
    orthoCamera.bottom = 0;
    orthoCamera.top = 1;
    orthoCamera.near = -1;
    orthoCamera.far = 10;
    orthoCamera.position.set(0, 0, 1);
    orthoCamera.updateProjectionMatrix();
  }, [orthoCamera]);

  /* ── Frame loop ────────────────────────────────────── */
  useFrame(() => {
    const audio = audioRef.current;
    const ct = audio?.currentTime ?? 0;

    // Auto-scroll when playing
    if (isPlaying && audio && !isNaN(audio.duration)) {
      const target = Math.max(0, ct - WINDOW_DURATION * PLAYHEAD_ANCHOR);
      const maxS = Math.max(0, melDuration - WINDOW_DURATION);
      targetScrollRef.current = Math.min(maxS, target);
    }
    scrollRef.current += (targetScrollRef.current - scrollRef.current) * 0.12;

    // Update camera frustum
    const scroll = scrollRef.current;
    orthoCamera.left = scroll;
    orthoCamera.right = scroll + WINDOW_DURATION;
    orthoCamera.updateProjectionMatrix();

    // Update playhead position
    if (playheadRef.current) {
      playheadRef.current.position.x = ct;
    }

    // Update uniforms
    if (materialRef.current) {
      materialRef.current.uniforms.uMaxPeaks.value = peakCount;
      materialRef.current.uniforms.uPointScale.value =
        POINT_SCALE_BASE * (viewportSize.height / 600);
    }

  });

  /* ── Click/wheel handlers ───────────────────────────── */
  const handlePointerDown = useCallback((e: THREE.Event) => {
    // R3F raycasting gives us the point in world space
    // But for a click-to-seek, we need to convert screen X to time
    const threeEvent = e as unknown as { nativeEvent: PointerEvent };
    const nativeEvent = threeEvent.nativeEvent;
    if (!nativeEvent) return;

    const canvas = nativeEvent.target as HTMLCanvasElement;
    const rect = canvas.getBoundingClientRect();
    const xFrac = (nativeEvent.clientX - rect.left) / rect.width;
    const time = scrollRef.current + xFrac * WINDOW_DURATION;
    const ratio = Math.max(0, Math.min(1, time / duration));
    onSeek(ratio);
  }, [duration, onSeek]);

  return (
    <>
      {/* Peak particles */}
      <points
        geometry={geometry}
        material={material}
        ref={(mesh) => {
          if (mesh) materialRef.current = material;
        }}
        frustumCulled={false}
      />

      {/* Playhead */}
      <group ref={playheadRef}>
        <primitive object={playheadLine} />
        {/* Playhead glow — wider translucent plane */}
        <mesh position={[0, 0.5, 0.05]}>
          <planeGeometry args={[0.15, 1.04]} />
          <meshBasicMaterial
            color={new THREE.Color(accentColor)}
            transparent
            opacity={0.06}
            blending={THREE.AdditiveBlending}
          />
        </mesh>
      </group>

      {/* Grid lines */}
      <group ref={gridGroupRef}>
        {octaveLines.map((line, i) => (
          <primitive key={`oct-${i}`} object={line} />
        ))}
        {timeLines.map((line, i) => (
          <primitive key={`time-${i}`} object={line} />
        ))}
      </group>

      {/* Click plane (invisible, for pointer events) */}
      <mesh
        position={[melDuration / 2, 0.5, -0.1]}
        onPointerDown={handlePointerDown}
      >
        <planeGeometry args={[melDuration + 20, 2]} />
        <meshBasicMaterial transparent opacity={0} />
      </mesh>

      {/* Post-processing */}
      <EffectComposer multisampling={0}>
        <Bloom
          luminanceThreshold={0.15}
          luminanceSmoothing={0.9}
          intensity={1.8}
          mipmapBlur
        />
        <Noise
          premultiply
          blendFunction={BlendFunction.SOFT_LIGHT}
          opacity={0.02}
        />
      </EffectComposer>
    </>
  );
}

/* ── SpectralPeaks — outer container ──────────────────────────────── */

interface Props {
  melData: MelData | null;
  audioRef: React.RefObject<HTMLAudioElement | null>;
  isPlaying: boolean;
  duration: number;
  accentColor: string;
  peakCount: 4 | 8 | 16;
  onSeek: (ratio: number) => void;
}

export function SpectralPeaks({
  melData, audioRef, isPlaying, duration,
  accentColor, peakCount, onSeek,
}: Props) {
  const pianoCanvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [containerHeight, setContainerHeight] = useState(400);
  const dpr = typeof window !== "undefined" ? Math.min(window.devicePixelRatio || 1, 2) : 1;

  /* ── Extract peaks (memoized) ───────────────────────── */
  const peaks = useMemo(() => {
    if (!melData) return null;
    return extractPeaks(melData);
  }, [melData]);

  const melDuration = melData ? melData.nFrames / melData.frameRate : 0;

  /* ── ResizeObserver ─────────────────────────────────── */
  useEffect(() => {
    const el = containerRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      const { height } = entries[0].contentRect;
      setContainerHeight(Math.round(height));
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  /* ── Piano roll canvas ──────────────────────────────── */
  useEffect(() => {
    const canvas = pianoCanvasRef.current;
    if (!canvas) return;
    const H = containerHeight;
    canvas.width = PIANO_ROLL_W * dpr;
    canvas.height = H * dpr;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, PIANO_ROLL_W, H);

    ctx.fillStyle = "rgba(6,6,14,0.95)";
    ctx.fillRect(0, 0, PIANO_ROLL_W, H);

    const freqToY = (hz: number) => {
      const frac = (Math.log2(hz) - LOG2_MIN) / LOG2_RANGE;
      return H * (1 - frac);
    };

    // ── Piano keys (left PIANO_KEYS_W region) ────────────
    // White keys
    for (const key of PIANO_KEYS) {
      if (key.isBlack) continue;
      const nextSemitone = key.freq * Math.pow(2, 1 / 12);
      const prevSemitone = key.freq / Math.pow(2, 1 / 12);
      const y1 = freqToY(Math.min(nextSemitone, PIANO_MAX_HZ));
      const y2 = freqToY(Math.max(prevSemitone, PIANO_MIN_HZ));
      const kh = Math.max(1, y2 - y1);

      ctx.fillStyle = "rgba(200,200,210,0.85)";
      ctx.fillRect(0, y1, PIANO_KEYS_W - 1, kh);
      ctx.strokeStyle = "rgba(0,0,0,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, PIANO_KEYS_W - 1, kh);

      if (key.name === "C") {
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.font = "bold 7px 'JetBrains Mono', monospace";
        ctx.textAlign = "left";
        ctx.textBaseline = "middle";
        ctx.fillText(`C${key.octave}`, 2, y1 + kh / 2);
      }
    }

    // Black keys
    for (const key of PIANO_KEYS) {
      if (!key.isBlack) continue;
      const halfSemitone = Math.pow(2, 0.5 / 12);
      const y1 = freqToY(key.freq * halfSemitone);
      const y2 = freqToY(key.freq / halfSemitone);
      const kh = Math.max(1, y2 - y1);
      const kw = PIANO_KEYS_W * 0.6;

      ctx.fillStyle = "rgba(20,20,30,0.95)";
      ctx.fillRect(0, y1, kw, kh);
      ctx.strokeStyle = "rgba(80,80,100,0.3)";
      ctx.lineWidth = 0.5;
      ctx.strokeRect(0, y1, kw, kh);
    }

    // ── Note-spectrum color bar (right SPECTRUM_BAR_W strip) ─────────
    // Continuous gradient: each pixel row gets its frequency's note color
    const barX = PIANO_KEYS_W;
    for (let py = 0; py < H; py++) {
      const frac = 1 - py / (H - 1); // py=0 → top → high freq
      const log2Freq = LOG2_MIN + frac * LOG2_RANGE;
      const freq = Math.pow(2, log2Freq);
      const [r, g, b] = freqToColor(freq);
      ctx.fillStyle = `rgb(${Math.round(r * 255)},${Math.round(g * 255)},${Math.round(b * 255)})`;
      ctx.fillRect(barX, py, SPECTRUM_BAR_W, 1);
    }

    // Subtle separator between keys and spectrum bar
    ctx.strokeStyle = "rgba(0,0,0,0.4)";
    ctx.lineWidth = 0.5;
    ctx.beginPath();
    ctx.moveTo(barX, 0);
    ctx.lineTo(barX, H);
    ctx.stroke();

    // Right border
    ctx.strokeStyle = "rgba(255,255,255,0.06)";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(PIANO_ROLL_W - 0.5, 0);
    ctx.lineTo(PIANO_ROLL_W - 0.5, H);
    ctx.stroke();
  }, [containerHeight, dpr]);

  /* ── Wheel handler on container ──────────────────────── */
  const scrollRef = useRef({ target: 0 });

  const handleWheel = useCallback((e: React.WheelEvent) => {
    e.stopPropagation();
    const maxS = Math.max(0, duration - WINDOW_DURATION);
    const delta = (e.deltaX || e.deltaY) * 0.04;
    scrollRef.current.target = Math.max(0, Math.min(maxS, scrollRef.current.target + delta));
  }, [duration]);

  return (
    <div ref={containerRef} className="relative w-full h-full flex" onWheel={handleWheel}>
      {/* Piano roll (Canvas 2D) */}
      <canvas
        ref={pianoCanvasRef}
        style={{ width: PIANO_ROLL_W, height: "100%", flexShrink: 0 }}
      />

      {/* R3F WebGL Canvas */}
      {peaks && melData ? (
        <Canvas
          orthographic
          camera={{
            position: [0, 0, 1],
            near: -1,
            far: 10,
            left: 0,
            right: WINDOW_DURATION,
            top: 1,
            bottom: 0,
          }}
          dpr={[1, 2]}
          gl={{
            antialias: false,
            alpha: true,
            powerPreference: "high-performance",
          }}
          style={{ flex: 1, height: "100%", cursor: "pointer", background: "transparent" }}
        >
          <PeakScene
            peaks={peaks}
            melDuration={melDuration}
            audioRef={audioRef}
            isPlaying={isPlaying}
            accentColor={accentColor}
            peakCount={peakCount}
            onSeek={onSeek}
            duration={duration}
          />
        </Canvas>
      ) : (
        <div className="flex-1 flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-600 animate-pulse">
            Loading spectral data...
          </span>
        </div>
      )}
    </div>
  );
}
