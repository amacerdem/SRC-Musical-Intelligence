/* ── SpectralPeaks — WebGL peak-based spectral visualization ─────────
 *  Renders extracted spectral peaks as glowing particles using R3F.
 *  OrthographicCamera pans horizontally; dynamic zoom via shared viewport.
 *
 *  Now used as a layer inside LayeredScope (absolute positioned).
 *  Piano roll extracted to PianoStrip.tsx; scroll/zoom to useViewport.ts.
 *  ──────────────────────────────────────────────────────────────────── */

import { useRef, useEffect, useMemo, useCallback } from "react";
import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { EffectComposer, Bloom, Noise } from "@react-three/postprocessing";
import { BlendFunction } from "postprocessing";
import * as THREE from "three";
import type { MelData, PeakBuffers } from "./peakExtractor";
import { extractPeaks } from "./peakExtractor";
import type { ViewportState } from "./useViewport";

/* ── Constants ───────────────────────────────────────────────────────── */

const PIANO_MIN_HZ = 27.5;
const PIANO_MAX_HZ = 4186.01;
const LOG2_MIN = Math.log2(PIANO_MIN_HZ);
const LOG2_MAX = Math.log2(PIANO_MAX_HZ);
const LOG2_RANGE = LOG2_MAX - LOG2_MIN;

const POINT_SCALE_BASE = 18;
const INITIAL_WINDOW = 12;

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

  vec3 finalColor = mix(vColor, vec3(1.0), core * 0.15);
  float alpha = glow * vAlpha;

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
  viewport: ViewportState;
  showPeaks: boolean;
  showBloom: boolean;
  showGrid: boolean;
}

function PeakScene({
  peaks, melDuration, audioRef, isPlaying,
  accentColor, peakCount, onSeek, duration,
  viewport, showPeaks, showBloom, showGrid,
}: PeakSceneProps) {
  const { camera, size: viewportSize } = useThree();
  const orthoCamera = camera as THREE.OrthographicCamera;

  const materialRef = useRef<THREE.ShaderMaterial | null>(null);
  const playheadRef = useRef<THREE.Group>(null);
  const pointsRef = useRef<THREE.Points>(null);

  /* ── Points geometry (static) ──────────────────────────── */
  const geometry = useMemo(() => {
    const geo = new THREE.BufferGeometry();
    geo.setAttribute("position", new THREE.BufferAttribute(peaks.positions, 3));
    geo.setAttribute("color", new THREE.BufferAttribute(peaks.colors, 3));
    geo.setAttribute("aSize", new THREE.BufferAttribute(peaks.sizes, 1));
    geo.setAttribute("aRank", new THREE.BufferAttribute(peaks.ranks, 1));
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
    const maxTime = melDuration + INITIAL_WINDOW;
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
    orthoCamera.right = INITIAL_WINDOW;
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

    // Drive shared viewport (lerp + auto-follow)
    viewport.tick(isPlaying, ct);

    // Read lerped values
    const scroll = viewport.scrollRef.current;
    const window_ = viewport.windowRef.current;

    // Update camera frustum dynamically
    orthoCamera.left = scroll;
    orthoCamera.right = scroll + window_;
    orthoCamera.updateProjectionMatrix();

    // Update playhead position
    if (playheadRef.current) {
      playheadRef.current.position.x = ct;
    }

    // Update uniforms — point size scales with zoom
    if (materialRef.current) {
      materialRef.current.uniforms.uMaxPeaks.value = peakCount;
      const zoomScale = Math.sqrt(INITIAL_WINDOW / Math.max(2, window_));
      materialRef.current.uniforms.uPointScale.value =
        POINT_SCALE_BASE * (viewportSize.height / 600) * zoomScale;
    }

    // Toggle peaks visibility
    if (pointsRef.current) {
      pointsRef.current.visible = showPeaks;
    }
  });

  return (
    <>
      {/* Peak particles */}
      <points
        ref={pointsRef}
        geometry={geometry}
        material={material}
        onUpdate={(self) => { materialRef.current = material; }}
        frustumCulled={false}
      />

      {/* Playhead */}
      <group ref={playheadRef}>
        <primitive object={playheadLine} />
        {/* Playhead glow */}
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
      {showGrid && (
        <group>
          {octaveLines.map((line, i) => (
            <primitive key={`oct-${i}`} object={line} />
          ))}
          {timeLines.map((line, i) => (
            <primitive key={`time-${i}`} object={line} />
          ))}
        </group>
      )}

      {/* Post-processing */}
      {showBloom ? (
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
      ) : (
        <EffectComposer multisampling={0}>
          <Noise
            premultiply
            blendFunction={BlendFunction.SOFT_LIGHT}
            opacity={0.02}
          />
        </EffectComposer>
      )}
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
  viewport: ViewportState;
  showPeaks: boolean;
  showBloom: boolean;
  showGrid: boolean;
}

export function SpectralPeaks({
  melData, audioRef, isPlaying, duration,
  accentColor, peakCount, onSeek,
  viewport, showPeaks, showBloom, showGrid,
}: Props) {
  /* ── Extract peaks (memoized) ───────────────────────── */
  const peaks = useMemo(() => {
    if (!melData) return null;
    return extractPeaks(melData);
  }, [melData]);

  const melDuration = melData ? melData.nFrames / melData.frameRate : 0;

  return (
    <div className="absolute inset-0">
      {peaks && melData ? (
        <Canvas
          orthographic
          camera={{
            position: [0, 0, 1],
            near: -1,
            far: 10,
            left: 0,
            right: INITIAL_WINDOW,
            top: 1,
            bottom: 0,
          }}
          dpr={[1, 2]}
          gl={{
            antialias: false,
            alpha: true,
            powerPreference: "high-performance",
          }}
          style={{ width: "100%", height: "100%", background: "transparent" }}
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
            viewport={viewport}
            showPeaks={showPeaks}
            showBloom={showBloom}
            showGrid={showGrid}
          />
        </Canvas>
      ) : (
        <div className="w-full h-full flex items-center justify-center">
          <span className="text-[10px] font-mono text-slate-600 animate-pulse">
            Loading spectral data...
          </span>
        </div>
      )}
    </div>
  );
}
