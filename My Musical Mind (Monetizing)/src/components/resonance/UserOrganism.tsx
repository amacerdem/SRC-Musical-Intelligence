/* ── UserOrganism — 3D bioluminescent organism per user ─────────── */

import { useRef, useMemo, useState, useCallback } from "react";
import { useFrame, useThree } from "@react-three/fiber";
import { Html, Billboard, useTexture } from "@react-three/drei";
import * as THREE from "three";
import { useResonanceStore } from "@/stores/useResonanceStore";
import { DIMENSIONS, resonance as computeResonance, type ResonanceUser, type Psi5 } from "@/data/resonance-simulation";

/* ── Dimension colors as vec3 (neg + pos per dimension) ───────── */

const NEG_COLORS_RGB = DIMENSIONS.map(d => {
  const c = new THREE.Color(d.negColor);
  return [c.r, c.g, c.b] as [number, number, number];
});

const POS_COLORS_RGB = DIMENSIONS.map(d => {
  const c = new THREE.Color(d.posColor);
  return [c.r, c.g, c.b] as [number, number, number];
});

/** Find dominant dimension (highest |psi|) and its polarity color */
function getDominantColor(psi: number[]): string {
  let maxAbs = 0, maxIdx = 0;
  for (let i = 0; i < 5; i++) {
    const a = Math.abs(psi[i]);
    if (a > maxAbs) { maxAbs = a; maxIdx = i; }
  }
  return psi[maxIdx] >= 0 ? DIMENSIONS[maxIdx].posColor : DIMENSIONS[maxIdx].negColor;
}

/* ── Vertex shader ──────────────────────────────────────────────── */

const vertexShader = `
uniform float uTime;
uniform float uPulseRate;
uniform float uIntensity;
uniform float uSelected;

varying vec3 vNormal;
varying vec3 vViewPos;
varying float vFresnel;
varying vec3 vLocalPos;

// Simplex 3D noise
vec4 permute(vec4 x){return mod(((x*34.0)+1.0)*x, 289.0);}
vec4 taylorInvSqrt(vec4 r){return 1.79284291400159 - 0.85373472095314 * r;}

float snoise(vec3 v){
  const vec2 C = vec2(1.0/6.0, 1.0/3.0);
  const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
  vec3 i  = floor(v + dot(v, C.yyy));
  vec3 x0 = v - i + dot(i, C.xxx);
  vec3 g = step(x0.yzx, x0.xyz);
  vec3 l = 1.0 - g;
  vec3 i1 = min(g.xyz, l.zxy);
  vec3 i2 = max(g.xyz, l.zxy);
  vec3 x1 = x0 - i1 + C.xxx;
  vec3 x2 = x0 - i2 + C.yyy;
  vec3 x3 = x0 - D.yyy;
  i = mod(i, 289.0);
  vec4 p = permute(permute(permute(
    i.z + vec4(0.0, i1.z, i2.z, 1.0))
  + i.y + vec4(0.0, i1.y, i2.y, 1.0))
  + i.x + vec4(0.0, i1.x, i2.x, 1.0));
  float n_ = 1.0/7.0;
  vec3 ns = n_ * D.wyz - D.xzx;
  vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
  vec4 x_ = floor(j * ns.z);
  vec4 y_ = floor(j - 7.0 * x_);
  vec4 x = x_ * ns.x + ns.yyyy;
  vec4 y = y_ * ns.x + ns.yyyy;
  vec4 h = 1.0 - abs(x) - abs(y);
  vec4 b0 = vec4(x.xy, y.xy);
  vec4 b1 = vec4(x.zw, y.zw);
  vec4 s0 = floor(b0)*2.0 + 1.0;
  vec4 s1 = floor(b1)*2.0 + 1.0;
  vec4 sh = -step(h, vec4(0.0));
  vec4 a0 = b0.xzyw + s0.xzyw*sh.xxyy;
  vec4 a1 = b1.xzyw + s1.xzyw*sh.zzww;
  vec3 p0 = vec3(a0.xy,h.x);
  vec3 p1 = vec3(a0.zw,h.y);
  vec3 p2 = vec3(a1.xy,h.z);
  vec3 p3 = vec3(a1.zw,h.w);
  vec4 norm = taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
  vec4 m = max(0.6 - vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)), 0.0);
  m = m * m;
  return 42.0 * dot(m*m, vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}

void main() {
  vec3 pos = position;

  // Breathing displacement
  float breath = sin(uTime * uPulseRate) * 0.1 * uIntensity;
  float noise = snoise(pos * 2.5 + uTime * 0.4) * 0.06 * uIntensity;
  pos += normal * (breath + noise);

  // Selection pulse
  float selPulse = uSelected * sin(uTime * 3.0) * 0.04;
  pos += normal * selPulse;

  vLocalPos = pos;
  vNormal = normalize(normalMatrix * normal);
  vec4 mvPos = modelViewMatrix * vec4(pos, 1.0);
  vViewPos = mvPos.xyz;

  // Fresnel
  vec3 viewDir = normalize(-mvPos.xyz);
  vFresnel = 1.0 - max(dot(viewDir, vNormal), 0.0);

  gl_Position = projectionMatrix * mvPos;
}
`;

/* ── Fragment shader ────────────────────────────────────────────── */

const fragmentShader = `
uniform float uTime;
uniform vec3 uNegColors[5];
uniform vec3 uPosColors[5];
uniform float uPsi[5];
uniform float uIntensity;
uniform float uSelected;
uniform float uHovered;

varying vec3 vNormal;
varying vec3 vViewPos;
varying float vFresnel;
varying vec3 vLocalPos;

void main() {
  // Weighted blend of bipolar dimension colors
  // For each dimension: mix(negColor, posColor, t) where t = (psi+5)/10
  // Weight by |psi|/5 — neutral dims contribute less
  vec3 col = vec3(0.0);
  float totalWeight = 0.0;
  for (int i = 0; i < 5; i++) {
    float t = clamp((uPsi[i] + 5.0) / 10.0, 0.0, 1.0);
    vec3 dimCol = mix(uNegColors[i], uPosColors[i], t);
    float w = abs(uPsi[i]) / 5.0;
    w = w * w; // Square for more contrast
    col += dimCol * w;
    totalWeight += w;
  }
  col /= max(totalWeight, 0.001);

  // Core brightness (center bright, edge transparent)
  float core = smoothstep(0.85, 0.0, vFresnel) * 0.9;

  // Fresnel edge glow
  float edge = pow(vFresnel, 2.5) * 0.7 * uIntensity;

  // Inner noise pattern
  float pattern = sin(vLocalPos.x * 8.0 + uTime * 0.5) *
                  sin(vLocalPos.y * 8.0 + uTime * 0.3) *
                  sin(vLocalPos.z * 8.0 + uTime * 0.4);
  pattern = pattern * 0.1 + 0.9;

  // Selection + hover highlights
  float sel = uSelected * (0.35 + 0.15 * sin(uTime * 2.5));
  float hov = uHovered * 0.2;

  float alpha = (core + edge + sel + hov) * uIntensity * pattern;
  vec3 finalCol = col * (1.0 + edge * 0.8 + sel * 0.5 + hov * 0.3);

  // Slight emission boost at center
  finalCol += col * core * 0.3;

  gl_FragColor = vec4(finalCol, clamp(alpha, 0.0, 1.0));
}
`;

/* ── Circular avatar billboard shaders ──────────────────────────── */

const avatarVertexShader = `
varying vec2 vUv;
void main() {
  vUv = uv;
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const avatarFragmentShader = `
uniform sampler2D uTexture;
uniform vec3 uBorderColor;
uniform float uOpacity;
varying vec2 vUv;

void main() {
  vec2 centered = vUv - 0.5;
  float dist = length(centered);

  // Hard circular clip (crisp edge)
  if (dist > 0.48) discard;

  // Thin glowing border ring at the edge
  float ring = smoothstep(0.38, 0.44, dist);

  vec4 tex = texture2D(uTexture, vUv);
  vec3 col = mix(tex.rgb, uBorderColor * 1.2, ring * 0.8);

  gl_FragColor = vec4(col, uOpacity);
}
`;

/** Check if the user has a real avatar image */
function hasRealAvatar(avatarUrl: string): boolean {
  return avatarUrl.includes("/avatars/photo_");
}

/** Billboard avatar that always faces the camera */
function AvatarBillboard({ avatarUrl, borderColor, opacity }: {
  avatarUrl: string;
  borderColor: string;
  opacity: number;
}) {
  const texture = useTexture(avatarUrl);

  // Sharp texture filtering
  useMemo(() => {
    texture.minFilter = THREE.LinearFilter;
    texture.magFilter = THREE.LinearFilter;
    texture.generateMipmaps = false;
  }, [texture]);

  const borderColorObj = useMemo(() => new THREE.Color(borderColor), [borderColor]);

  const uniforms = useMemo(() => ({
    uTexture: { value: texture },
    uBorderColor: { value: borderColorObj },
    uOpacity: { value: opacity },
  }), [texture, borderColorObj, opacity]);

  return (
    <mesh>
      <planeGeometry args={[0.7, 0.7]} />
      <shaderMaterial
        vertexShader={avatarVertexShader}
        fragmentShader={avatarFragmentShader}
        uniforms={uniforms}
        transparent
        depthWrite={false}
        side={THREE.DoubleSide}
      />
    </mesh>
  );
}

/* ── Component ──────────────────────────────────────────────────── */

interface Props {
  user: ResonanceUser;
  isSelected: boolean;
}

export function UserOrganism({ user, isSelected }: Props) {
  const groupRef = useRef<THREE.Group>(null);
  const matRef = useRef<THREE.ShaderMaterial>(null);
  const [hovered, setHovered] = useState(false);
  const selectUser = useResonanceStore(s => s.selectUser);
  const displayScale = useRef(1);

  // Base radius for geometry (fixed); visual size controlled by group scale
  const radius = 0.5;

  const uniforms = useMemo(() => ({
    uTime: { value: 0 },
    uPulseRate: { value: user.pulseRate },
    uIntensity: { value: user.intensity },
    uSelected: { value: 0 },
    uHovered: { value: 0 },
    uNegColors: { value: NEG_COLORS_RGB.map(c => new THREE.Vector3(c[0], c[1], c[2])) },
    uPosColors: { value: POS_COLORS_RGB.map(c => new THREE.Vector3(c[0], c[1], c[2])) },
    uPsi: { value: [...user.psi] },
  }), []);

  const targetPos = useMemo(() => new THREE.Vector3(), []);

  useFrame((_, delta) => {
    if (!groupRef.current || !matRef.current) return;
    const u = matRef.current.uniforms;

    // Update time
    u.uTime.value += delta;

    // Smooth lerp position
    targetPos.set(user.position[0], user.position[1], user.position[2]);
    groupRef.current.position.lerp(targetPos, 0.04);

    // Update psi values (smooth interpolation)
    for (let i = 0; i < 5; i++) {
      u.uPsi.value[i] += (user.psi[i] - u.uPsi.value[i]) * 0.1;
    }

    // Update derived
    u.uIntensity.value += (user.intensity - u.uIntensity.value) * 0.1;
    u.uPulseRate.value += (user.pulseRate - u.uPulseRate.value) * 0.1;

    // Selection / hover
    const selTarget = isSelected ? 1 : 0;
    u.uSelected.value += (selTarget - u.uSelected.value) * 0.1;
    const hovTarget = hovered ? 1 : 0;
    u.uHovered.value += (hovTarget - u.uHovered.value) * 0.15;

    // Resonance-based sizing — read selfPsi directly (no re-render)
    const selfPsi = useResonanceStore.getState().selfPsi;
    const res = computeResonance(selfPsi as Psi5, user.psi);
    const targetScale = 0.5 + res * 1.2; // 0.5 (divergent) to 1.7 (deep sync)
    displayScale.current += (targetScale - displayScale.current) * 0.05;
    groupRef.current.scale.setScalar(displayScale.current);
  });

  const handleClick = useCallback(() => {
    selectUser(isSelected ? null : user.id);
  }, [isSelected, user.id, selectUser]);

  const domColor = getDominantColor(user.psi);

  // Distance check for label
  const dist = useMemo(() => {
    const p = new THREE.Vector3(user.position[0], user.position[1], user.position[2]);
    return p.length();
  }, [user.position]);

  return (
    <group
      ref={groupRef}
      position={[user.position[0], user.position[1], user.position[2]]}
    >
      {/* Core organism sphere */}
      <mesh
        onPointerDown={handleClick}
        onPointerEnter={() => { setHovered(true); document.body.style.cursor = "pointer"; }}
        onPointerLeave={() => { setHovered(false); document.body.style.cursor = "auto"; }}
      >
        <sphereGeometry args={[radius, 24, 18]} />
        <shaderMaterial
          ref={matRef}
          vertexShader={vertexShader}
          fragmentShader={fragmentShader}
          uniforms={uniforms}
          transparent
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </mesh>

      {/* Outer glow halo */}
      <mesh>
        <sphereGeometry args={[radius * 2.2, 16, 12]} />
        <meshBasicMaterial
          color={domColor}
          transparent
          opacity={0.04 * user.intensity}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
          side={THREE.BackSide}
        />
      </mesh>

      {/* Selection ring */}
      {isSelected && (
        <mesh rotation={[Math.PI / 2, 0, 0]}>
          <torusGeometry args={[radius * 1.8, 0.02, 8, 48]} />
          <meshBasicMaterial
            color={domColor}
            transparent
            opacity={0.6}
            blending={THREE.AdditiveBlending}
          />
        </mesh>
      )}

      {/* Billboard avatar — centered on sphere */}
      {hasRealAvatar(user.avatarUrl) && (
        <Billboard position={[0, 0, 0]} follow lockX={false} lockY={false} lockZ={false}>
          <AvatarBillboard
            avatarUrl={user.avatarUrl}
            borderColor={domColor}
            opacity={isSelected ? 1.0 : hovered ? 0.95 : 0.8}
          />
        </Billboard>
      )}

      {/* Name label */}
      {(hovered || isSelected || dist < 15) && (
        <Html
          position={[0, radius + 0.5, 0]}
          center
          style={{
            pointerEvents: "none",
            userSelect: "none",
            whiteSpace: "nowrap",
          }}
        >
          <div className="flex flex-col items-center gap-0.5">
            <span
              className="text-[9px] font-display font-medium uppercase tracking-[0.2em]"
              style={{ color: domColor, textShadow: `0 0 8px ${domColor}60` }}
            >
              {user.displayName}
            </span>
            {user.currentTrack && (hovered || isSelected) && (
              <span className="text-[7px] font-mono text-slate-600 max-w-[120px] truncate">
                {user.currentTrack}
              </span>
            )}
          </div>
        </Html>
      )}
    </group>
  );
}
