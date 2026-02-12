/**
 * shaders.js — All GLSL fragment shaders for the MI Analysis Demo.
 * S³ Musical Intelligence — 7 shader programs.
 *
 * Shared vertex shader + noise library + 6 fragment shaders + 1 transition compositor.
 */

// ═══════════════════════════════════════════════════════════════════════
// VERTEX SHADER (shared by all programs)
// ═══════════════════════════════════════════════════════════════════════

export const VERT = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
    v_uv = a_pos * 0.5 + 0.5;
    gl_Position = vec4(a_pos, 0.0, 1.0);
}`;

// ═══════════════════════════════════════════════════════════════════════
// SHARED GLSL LIBRARY (noise, SDF, color)
// ═══════════════════════════════════════════════════════════════════════

const LIB = `
// ─── Noise ───────────────────────────────────
float hash21(vec2 p) {
    p = fract(p * vec2(123.34, 456.21));
    p += dot(p, p + 45.32);
    return fract(p.x * p.y);
}
float hash11(float p) {
    p = fract(p * 0.1031);
    p *= p + 33.33;
    return fract(p * (p + p));
}
float nse(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    float a = hash21(i), b = hash21(i + vec2(1,0));
    float c = hash21(i + vec2(0,1)), d = hash21(i + vec2(1,1));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(a, b, u.x), mix(c, d, u.x), u.y);
}
float fbm(vec2 p) {
    float v = 0.0, a = 0.5;
    mat2 rot = mat2(0.8, 0.6, -0.6, 0.8);
    for (int i = 0; i < 5; i++) {
        v += a * nse(p);
        p = rot * p * 2.0;
        a *= 0.5;
    }
    return v;
}
float fbm3(vec2 p) {
    float v = 0.0, a = 0.5;
    mat2 rot = mat2(0.8, 0.6, -0.6, 0.8);
    for (int i = 0; i < 3; i++) {
        v += a * nse(p);
        p = rot * p * 2.0;
        a *= 0.5;
    }
    return v;
}

// ─── SDF ─────────────────────────────────────
float sdCircle(vec2 p, float r) { return length(p) - r; }
float sdBox(vec2 p, vec2 b) {
    vec2 d = abs(p) - b;
    return length(max(d, 0.0)) + min(max(d.x, d.y), 0.0);
}

// ─── Color ───────────────────────────────────
vec3 s3Indigo = vec3(0.388, 0.400, 0.945);     // #6366f1
vec3 s3Gold   = vec3(0.976, 0.718, 0.227);      // #f9b73a
vec3 s3Red    = vec3(0.976, 0.243, 0.369);       // #f93e5e
vec3 s3Cyan   = vec3(0.024, 0.714, 0.831);       // #06b6d4
vec3 s3Green  = vec3(0.133, 0.804, 0.467);       // #22cd77

vec3 hsl2rgb(float h, float s, float l) {
    vec3 rgb = clamp(abs(mod(h*6.0+vec3(0,4,2),6.0)-3.0)-1.0, 0.0, 1.0);
    return l + s * (rgb - 0.5) * (1.0 - abs(2.0 * l - 1.0));
}
`;

// ═══════════════════════════════════════════════════════════════════════
// UNIFORM HEADER (shared by all fragment shaders)
// ═══════════════════════════════════════════════════════════════════════

const UNIFORM_HEADER = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 O;

uniform vec2 u_res;
uniform float u_time;
uniform float u_progress;
`;

// ═══════════════════════════════════════════════════════════════════════
// SHADER 0: BACKGROUND — Ambient noise field
// ═══════════════════════════════════════════════════════════════════════

export const BACKGROUND = UNIFORM_HEADER + `
uniform float u_mel[8];
` + LIB + `
void main() {
    vec2 uv = v_uv;
    vec2 p = (gl_FragCoord.xy - u_res * 0.5) / u_res.y;

    // Base: dark field with slow drift
    float n = fbm(p * 3.0 + u_time * 0.05);
    vec3 col = vec3(0.02, 0.02, 0.04);

    // Mel energy breathing — subtle pulse
    float energy = 0.0;
    for (int i = 0; i < 8; i++) energy += u_mel[i];
    energy /= 8.0;

    // Particle field
    float stars = 0.0;
    for (float i = 0.0; i < 40.0; i++) {
        vec2 sp = vec2(hash11(i * 7.13), hash11(i * 3.77));
        sp = fract(sp + u_time * 0.01 * vec2(hash11(i*1.3) - 0.5, -0.1));
        float d = length(p - (sp - 0.5) * 2.0);
        float brightness = smoothstep(0.02, 0.0, d) * (0.3 + 0.7 * energy);
        stars += brightness * hash11(i * 11.7);
    }

    // Indigo glow from center
    float vignette = 1.0 - length(p) * 0.6;
    col += s3Indigo * 0.05 * n * vignette;
    col += vec3(0.6, 0.65, 1.0) * stars * 0.4;

    // Energy-responsive ambient
    col += s3Indigo * 0.02 * energy * (0.5 + 0.5 * sin(u_time * 0.5));

    // Vignette
    float vig = 1.0 - pow(length(p) * 0.7, 2.0);
    col *= max(vig, 0.2);

    O = vec4(col, 1.0);
}`;

// ═══════════════════════════════════════════════════════════════════════
// SHADER 1: SPECTRAL LANDSCAPE — Level 1 Primary
// ═══════════════════════════════════════════════════════════════════════

export const SPECTRAL_LANDSCAPE = UNIFORM_HEADER + `
uniform float u_mel[8];
uniform float u_r3[16];

// R³ index mapping:
// [0-2] consonance: roughness, stumpf_fusion, sensory_pleasantness
// [3-5] energy: amplitude, loudness, onset_strength
// [6-9] timbre: warmth, sharpness, tonalness, clarity
// [10-12] change: spectral_flux, distribution_entropy, distribution_flatness
// [13-15] interactions: x_amp_roughness, x_vel_roughness, x_flux_roughness
` + LIB + `
void main() {
    vec2 uv = v_uv;
    vec2 p = (gl_FragCoord.xy - u_res * 0.5) / u_res.y;

    float consonance = u_r3[1];   // stumpf_fusion
    float energy = u_r3[3];       // amplitude
    float loudness = u_r3[4];     // loudness
    float onset = u_r3[5];        // onset_strength
    float warmth = u_r3[6];       // warmth
    float tonalness = u_r3[8];    // tonalness
    float flux = u_r3[10];        // spectral_flux

    // ─── Terrain ─────────────────────────────────
    float scroll = u_time * 0.15;
    vec2 tp = vec2(uv.x * 4.0 - scroll, uv.y * 3.0);

    // Multiple octaves terrain with mel influence
    float terrain = 0.0;
    for (int i = 0; i < 8; i++) {
        float band = u_mel[i];
        float y_pos = float(i) / 7.0;
        float ridge = exp(-pow(uv.y - y_pos, 2.0) * 20.0) * band;
        terrain += ridge;
    }
    terrain *= 0.5 + 0.5 * fbm(tp);

    // ─── Color by R³ groups ──────────────────────
    // Consonance → blue-green, Energy → red-orange, Timbre → purple, Change → yellow
    vec3 consonColor = mix(s3Red * 0.5, s3Cyan, consonance);
    vec3 energyColor = mix(vec3(0.1), vec3(1.0, 0.4, 0.1), energy);
    vec3 timbreColor = mix(vec3(0.1, 0.05, 0.15), vec3(0.6, 0.3, 0.9), warmth);
    vec3 changeColor = vec3(1.0, 0.9, 0.3) * flux;

    vec3 col = vec3(0.02, 0.02, 0.04);

    // Terrain coloring: mix by vertical position
    vec3 terrainColor = mix(
        mix(consonColor, energyColor, uv.y),
        mix(timbreColor, changeColor, uv.y),
        0.5 + 0.5 * sin(uv.y * 6.28)
    );
    col += terrainColor * terrain * 0.8;

    // ─── Energy envelope glow (bottom) ───────────
    float envGlow = exp(-pow(uv.y - 0.1, 2.0) * 40.0) * loudness;
    col += energyColor * envGlow * 0.6;

    // ─── Onset flashes ───────────────────────────
    if (onset > 0.5) {
        float flash = onset * 0.3 * exp(-pow(fract(uv.x * 8.0 + scroll * 4.0) - 0.5, 2.0) * 100.0);
        col += vec3(1.0) * flash;
    }

    // ─── Spectral flux particles ─────────────────
    if (flux > 0.3) {
        for (float i = 0.0; i < 15.0; i++) {
            vec2 sp = vec2(
                fract(hash11(i * 5.7) + u_time * 0.2),
                hash11(i * 3.3 + floor(u_time * 2.0))
            );
            float d = length(uv - sp);
            col += changeColor * flux * smoothstep(0.015, 0.0, d) * 0.5;
        }
    }

    // ─── Consonance bar (top) ────────────────────
    float barY = smoothstep(0.94, 0.96, uv.y) * smoothstep(0.98, 0.96, uv.y);
    col += mix(s3Red, s3Green, consonance) * barY * 0.5;

    // ─── Tonalness aura ──────────────────────────
    col += s3Indigo * tonalness * 0.05 * (0.5 + 0.5 * nse(p * 5.0 + u_time));

    O = vec4(col, 1.0);
}`;

// ═══════════════════════════════════════════════════════════════════════
// SHADER 3: REWARD FLOW — Level 2 Primary
// ═══════════════════════════════════════════════════════════════════════

export const REWARD_FLOW = UNIFORM_HEADER + `
uniform float u_brain[12];
uniform float u_zeta[4];

// u_brain mapping:
// [0] wanting  [1] liking  [2] pleasure  [3] tension
// [4] valence  [5] arousal [6] beauty    [7] emotional_arc
// [8] prediction_error  [9] emotional_momentum
// [10] harmonic_context [11] emotion_certainty
` + LIB + `
void main() {
    vec2 uv = v_uv;
    vec2 p = (gl_FragCoord.xy - u_res * 0.5) / u_res.y;

    float wanting = u_brain[0];
    float liking  = u_brain[1];
    float pleasure = u_brain[2];
    float tension = u_brain[3];
    float valence = u_brain[4];
    float arousal = u_brain[5];
    float beauty  = u_brain[6];
    float arc     = u_brain[7];
    float pe      = u_brain[8];
    float momentum = u_brain[9];

    vec3 col = vec3(0.02, 0.02, 0.04);

    // ─── Wanting Field (left, warm) ──────────────
    {
        vec2 wp = p + vec2(0.4, 0.0);
        float flow = fbm(wp * 3.0 + vec2(-u_time * 0.3, u_time * 0.1));
        float mask = smoothstep(0.8, -0.2, wp.x);
        vec3 wantColor = mix(vec3(0.3, 0.05, 0.0), vec3(1.0, 0.3, 0.05), wanting);
        col += wantColor * flow * mask * wanting * 0.7;
    }

    // ─── Liking Field (right, cool) ──────────────
    {
        vec2 lp = p - vec2(0.4, 0.0);
        float flow = fbm(lp * 3.0 + vec2(u_time * 0.3, -u_time * 0.15));
        float mask = smoothstep(-0.8, 0.2, lp.x);
        vec3 likeColor = mix(vec3(0.0, 0.05, 0.3), vec3(0.1, 0.4, 1.0), liking);
        col += likeColor * flow * mask * liking * 0.7;
    }

    // ─── Pleasure Convergence (center vortex) ────
    {
        float r = length(p);
        float angle = atan(p.y, p.x) + u_time * 0.5 * pleasure;
        float spiral = fbm(vec2(r * 5.0, angle * 2.0));
        float center = exp(-r * r * 8.0) * pleasure;
        vec3 pleaColor = mix(s3Indigo, vec3(0.8, 0.3, 0.9), pleasure);
        col += pleaColor * center * spiral * 1.2;

        // Core glow
        col += pleaColor * exp(-r * r * 30.0) * pleasure * 0.5;
    }

    // ─── Tension turbulence ──────────────────────
    {
        float turb = fbm(p * 6.0 + u_time * 0.4 * tension) - 0.5;
        col += vec3(0.8, 0.2, 0.2) * turb * tension * 0.15;
    }

    // ─── Beauty golden shimmer ───────────────────
    {
        float shimmer = fbm(p * 8.0 + u_time * 0.2);
        float mask = 0.5 + 0.5 * sin(p.x * 10.0 + u_time);
        col += s3Gold * shimmer * mask * beauty * 0.15;
    }

    // ─── Emotional arc background gradient ───────
    {
        float grad = arc * 0.5 + 0.5;
        vec3 arcColor = mix(vec3(0.05, 0.0, 0.15), vec3(0.15, 0.05, 0.0), grad);
        col += arcColor * 0.2;
    }

    // ─── Prediction error sparks ─────────────────
    {
        float absPE = abs(pe);
        if (absPE > 0.3) {
            for (float i = 0.0; i < 8.0; i++) {
                vec2 sp = vec2(hash11(i * 7.1 + floor(u_time * 3.0)),
                               hash11(i * 3.9 + floor(u_time * 3.0))) - 0.5;
                float d = length(p - sp * 1.5);
                col += vec3(1.0, 0.9, 0.5) * absPE * smoothstep(0.02, 0.0, d) * 0.4;
            }
        }
    }

    // ─── Peak flash ──────────────────────────────
    if (pleasure > 0.7) {
        col += vec3(1.0) * (pleasure - 0.7) * 0.5;
    }

    O = vec4(col, 1.0);
}`;

// ═══════════════════════════════════════════════════════════════════════
// SHADER 5: NEURAL PULSE — Level 3 Primary
// ═══════════════════════════════════════════════════════════════════════

export const NEURAL_PULSE = UNIFORM_HEADER + `
uniform float u_beta[14];
uniform float u_autonomic[6];

// u_beta: [0] nacc [1] caudate [2] vta [3] sn
//         [4] stg  [5] ifg     [6] amygdala [7] hippocampus
//         [8] dopamine [9] opioid [10] da_opioid_interact
//         [11] anticipation_circuit [12] consummation_circuit [13] learning_circuit
// u_autonomic: [0] scr [1] hr [2] respr [3] chills [4] ans [5] da_opioid
` + LIB + `

// Brain region positions (sagittal view, normalized)
const vec2 POS_STG  = vec2( 0.35,  0.15);   // Superior temporal gyrus
const vec2 POS_CAU  = vec2( 0.0,   0.25);   // Caudate
const vec2 POS_NAC  = vec2( 0.0,   0.0);    // Nucleus accumbens
const vec2 POS_VTA  = vec2( 0.0,  -0.2);    // Ventral tegmental area
const vec2 POS_HIP  = vec2( 0.25, -0.1);    // Hippocampus
const vec2 POS_AMG  = vec2( 0.2,  -0.05);   // Amygdala
const vec2 POS_IFG  = vec2(-0.3,   0.3);    // Inferior frontal gyrus
const vec2 POS_OFC  = vec2(-0.2,   0.15);   // Orbitofrontal cortex

float brainRegion(vec2 p, vec2 center, float activation, float baseR) {
    float r = baseR * (1.0 + 0.15 * activation);
    float d = sdCircle(p - center, r);
    float glow = exp(-d * d * 200.0) * (0.2 + 0.8 * activation);
    float pulse = 0.5 + 0.5 * sin(u_time * 3.0 * activation + length(center) * 10.0);
    return glow * (0.7 + 0.3 * pulse);
}

float fiberPath(vec2 p, vec2 a, vec2 b, float width) {
    vec2 ab = b - a;
    float t = clamp(dot(p - a, ab) / dot(ab, ab), 0.0, 1.0);
    float d = length(p - a - ab * t);
    return smoothstep(width, 0.0, d);
}

float particleOnPath(vec2 p, vec2 a, vec2 b, float speed, float idx) {
    vec2 ab = b - a;
    float t = fract(u_time * speed + idx * 0.37);
    vec2 pos = a + ab * t;
    return smoothstep(0.015, 0.0, length(p - pos));
}

void main() {
    vec2 p = (gl_FragCoord.xy - u_res * 0.5) / u_res.y;

    // Extract activations
    float nacc = u_beta[0];
    float caudate = u_beta[1];
    float vta = u_beta[2];
    float stg = u_beta[4];
    float ifg = u_beta[5];
    float amygdala = u_beta[6];
    float hippocampus = u_beta[7];
    float dopamine = u_beta[8];
    float opioid = u_beta[9];
    float antic = u_beta[11];   // anticipation circuit
    float consum = u_beta[12];  // consummation circuit
    float learning = u_beta[13]; // learning circuit

    float scr = u_autonomic[0];
    float hr = u_autonomic[1];
    float chills = u_autonomic[3];

    vec3 col = vec3(0.02, 0.02, 0.04);

    // ─── Brain outline (soft sagittal silhouette) ─
    float brainShape = 1.0 - smoothstep(0.35, 0.45, length(p * vec2(1.0, 1.2)));
    col += vec3(0.04, 0.04, 0.08) * brainShape;

    // ─── Fiber pathways (background glow) ────────
    float fiber_vta_nac = fiberPath(p, POS_VTA, POS_NAC, 0.015);
    float fiber_vta_cau = fiberPath(p, POS_VTA, POS_CAU, 0.015);
    float fiber_stg_nac = fiberPath(p, POS_STG, POS_NAC, 0.012);
    float fiber_ifg_cau = fiberPath(p, POS_IFG, POS_CAU, 0.012);
    float fiber_amg_nac = fiberPath(p, POS_AMG, POS_NAC, 0.012);

    col += s3Green * fiber_vta_nac * consum * 0.15;
    col += vec3(1.0, 0.6, 0.1) * fiber_vta_cau * antic * 0.15;
    col += vec3(0.6, 0.3, 0.9) * fiber_stg_nac * stg * 0.12;
    col += s3Indigo * fiber_ifg_cau * ifg * 0.12;
    col += vec3(0.9, 0.3, 0.5) * fiber_amg_nac * amygdala * 0.12;

    // ─── Dopamine particles along pathways ───────
    for (float i = 0.0; i < 6.0; i++) {
        // VTA → NAcc (green, consummatory)
        float part = particleOnPath(p, POS_VTA, POS_NAC, 0.4 + consum * 0.3, i);
        col += s3Green * part * consum * 0.8;

        // VTA → Caudate (orange, anticipatory)
        part = particleOnPath(p, POS_VTA, POS_CAU, 0.35 + antic * 0.25, i + 10.0);
        col += vec3(1.0, 0.6, 0.1) * part * antic * 0.8;

        // STG → NAcc (violet)
        if (i < 4.0) {
            part = particleOnPath(p, POS_STG, POS_NAC, 0.3, i + 20.0);
            col += vec3(0.6, 0.3, 0.9) * part * stg * nacc * 0.6;
        }
    }

    // ─── Brain regions ───────────────────────────
    float ofc_act = 0.5 * (nacc + caudate); // OFC tracks value
    col += s3Cyan * brainRegion(p, POS_STG, stg, 0.04);
    col += vec3(1.0, 0.6, 0.1) * brainRegion(p, POS_CAU, caudate, 0.035);
    col += s3Green * brainRegion(p, POS_NAC, nacc, 0.04);
    col += vec3(0.8, 0.3, 0.1) * brainRegion(p, POS_VTA, vta, 0.03);
    col += vec3(0.4, 0.7, 0.9) * brainRegion(p, POS_HIP, hippocampus, 0.03);
    col += vec3(0.9, 0.3, 0.5) * brainRegion(p, POS_AMG, amygdala, 0.035);
    col += s3Indigo * brainRegion(p, POS_IFG, ifg, 0.035);
    col += s3Gold * brainRegion(p, POS_OFC, ofc_act, 0.03);

    // ─── Opioid golden ambient ───────────────────
    col += s3Gold * opioid * 0.06 * brainShape;

    // ─── Autonomic border effects ────────────────
    float edge = max(abs(p.x), abs(p.y));
    float border = smoothstep(0.42, 0.45, edge);

    // SCR: pulsing glow
    float scrPulse = 0.5 + 0.5 * sin(u_time * 4.0 * scr);
    col += vec3(0.3, 0.8, 0.3) * border * scr * scrPulse * 0.3;

    // Chills: cold blue wave
    if (chills > 0.4) {
        float wave = sin(p.y * 20.0 + u_time * 5.0) * 0.5 + 0.5;
        col += vec3(0.3, 0.5, 1.0) * border * chills * wave * 0.4;
    }

    // HR: rhythmic flash at "heart" position
    float hrBeat = pow(0.5 + 0.5 * sin(u_time * 6.28 * (0.5 + hr)), 8.0);
    float hrPos = smoothstep(0.04, 0.0, length(p - vec2(-0.4, -0.35)));
    col += s3Red * hrBeat * hrPos * 0.6;

    O = vec4(col, 1.0);
}`;

// ═══════════════════════════════════════════════════════════════════════
// SHADER 6: TRANSITION — Dual-FBO cross-fade compositor
// ═══════════════════════════════════════════════════════════════════════

export const TRANSITION = `#version 300 es
precision highp float;
in vec2 v_uv;
out vec4 O;

uniform sampler2D u_tex_old;
uniform sampler2D u_tex_new;
uniform float u_mix;

void main() {
    vec4 old = texture(u_tex_old, v_uv);
    vec4 new_ = texture(u_tex_new, v_uv);
    float t = smoothstep(0.0, 1.0, u_mix);
    O = mix(old, new_, t);

    // Indigo edge glow during transition
    float edge = max(abs(v_uv.x - 0.5), abs(v_uv.y - 0.5)) * 2.0;
    float glow = exp(-pow(edge - 0.95, 2.0) * 200.0) * (1.0 - abs(2.0 * t - 1.0));
    O.rgb += vec3(0.388, 0.400, 0.945) * glow * 0.3;
}`;
