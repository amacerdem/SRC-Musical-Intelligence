// PavelFluidSimulation.js
// ES Module — default export
// Fluid physics: klasik 2D GPU (Pavel Dobryakov mantığı), ama GÖRÜNTÜLEME aşamasında
// ekran pikselleri içi boş bir kürenin iç yüzeyine maplenir (spherical view).
// Parçacıklar (Haxiomic tarzı) da aynı kamerayla ekrana projekte edilir.

// Standalone color helpers (no external dependencies)
function _hsvToRgb(h,s,v) {
  let r,g,b,i=Math.floor(h*6),f=h*6-i,p=v*(1-s),q=v*(1-f*s),t=v*(1-(1-f)*s);
  switch(i%6){case 0:r=v;g=t;b=p;break;case 1:r=q;g=v;b=p;break;case 2:r=p;g=v;b=t;break;
    case 3:r=p;g=q;b=v;break;case 4:r=t;g=p;b=v;break;case 5:r=v;g=p;b=q;break;}
  return {r,g,b};
}
let _currentColor = { r: 0.03, g: 0.0, b: 0.015, frequency: 55 };
function getCurrentColor() { return _currentColor; }
function frequencyToColor(freq) {
  const hue = (Math.log2(freq / 20) / Math.log2(4000 / 20)) % 1;
  const c = _hsvToRgb(hue, 1, 0.15);
  _currentColor = { ...c, frequency: freq };
  return _currentColor;
}
function getColorPalette(count) {
  const p = [];
  for (let i = 0; i < count; i++) {
    const f = 20 * Math.pow(4000/20, i/(count-1));
    p.push(frequencyToColor(f));
  }
  return p;
}
function getColorFromYPosition(y01) { return frequencyToColor(20 * Math.pow(4000/20, y01)); }
function stopRealTimeColorUpdates() {}
// Standalone — no external color module needed.

// Import dat.GUI from GUI directory
const dat = window.dat || {};

/* MIT License - (c) Pavel Dobryakov (aslı), bu dosya yeniden düzenleme + eklemeler içerir. */

export default class PavelFluidSimulation {
  constructor(canvas, options = {}) {
    if (!canvas) throw new Error('PavelFluidSimulation: canvas is required');
    this.canvas = canvas;

    // ---- Config ----
    this.config = {
      // fluid
      SIM_RESOLUTION: 512,
      DYE_RESOLUTION: 2048,
      CAPTURE_RESOLUTION: 512,
      DENSITY_DISSIPATION: 1.0,
      VELOCITY_DISSIPATION: 0.2,
      PRESSURE: 0.8,
      PRESSURE_ITERATIONS: 20,
      CURL: 30,
      SPLAT_RADIUS: 0.25,         // yüzde (doku alanına göre)
      SPLAT_FORCE: 6000,
      SHADING: true,
      COLORFUL: false,
      COLOR_UPDATE_SPEED: 10,
      PAUSED: false,
      BACK_COLOR: { r: 0, g: 0, b: 0 },
      TRANSPARENT: false,

      // bloom
      BLOOM: true,
      BLOOM_ITERATIONS: 8,
      BLOOM_RESOLUTION: 256,
      BLOOM_INTENSITY: 0.01,
      BLOOM_THRESHOLD: 3.0,
      BLOOM_SOFT_KNEE: 0.7,

      // sunrays
      SUNRAYS: true,
      SUNRAYS_RESOLUTION: 196,
      SUNRAYS_WEIGHT: 0.75, // Reduced by 25%

      // particles (Haxiomic tarzı)
      PARTICLES_ENABLED: true,
      PARTICLE_RES: 1024,          // 256x256 = 65k particle; performansa göre artır/azalt
      PARTICLE_SIZE: 2.0,
      PARTICLE_ALPHA: 0.75,
      PARTICLE_BRIGHTNESS: 1.0,
      PARTICLE_ADVECTION: 1.0,

      // kamera (spherical view)
      // FOV referansları: 45°=0.785, 60°=1.047, 90°=1.571, 120°=2.094, 150°=2.618, 180°=3.142
      CAMERA_FOV_H: 1.8,          // rad ~ 115° (horizontal)
      CAMERA_FOV_V: 1.8,          // rad ~ 115° (vertical)
      CAMERA_YAW: 0.0,            // rad (will auto-rotate)
      CAMERA_PITCH: 0.0,          // rad (y=0 pozisyonu için)
      CAMERA_AUTO_ROTATE: true,   // Otomatik rotasyon
      CAMERA_ROTATION_PERIOD: 48.0, // 48 saniyede bir tam tur (2π radyan, sağa doğru)

      // --- GridParticles (spherical lat-long lines as static points) ---
      GRID_ENABLED: true,
      GRID_TOTAL: 8192,           // toplam nokta sayısı
      GRID_MERIDIANS: 32,         // boylam çizgisi sayısı (≈ 360/11.25°)
      GRID_PARALLELS: 32,         // enlem çizgisi sayısı
      GRID_EXCLUDE_POLAR_DEG: 0.0, // kutuptan ±0°'yi at (tam küre kapsama)
      GRID_EQ_HIGHLIGHT: true,    // ekvator bandını vurgula
      GRID_WEIGHT_M: 0.50,        // bütçe payı (meridian vs parallel)
      GRID_WEIGHT_P: 0.50,
      GRID_POINT_SIZE_PX: 2.0,   // nokta yarıçapı (GL_POINTS size px)
      GRID_COLOR_ICE: { r: 0, g: 255, b: 255 }, // buz-mavi #D2EBFF
      GRID_COLOR_WHITE: { r: 255, g: 255, b: 255 }, // beyaz #FFFFFF
      GRID_INTENSITY: 15.0,       // baz yoğunluk
      GRID_BLOOM_FACTOR: 0.35,    // bloom'a katkı
      GRID_ALPHA: 1.0,
      GRID_RADIUS: 1.0,           // kürenin iç duvarı (göz merkezde)

      ...options
    };

    // Instrument color for initial splats
    this.instrumentColor = options.instrumentColor || null;
    
    // ✅ Instrument-specific preset system
    this.currentInstrument = options.instrument || null;
    this.instrumentPresets = this._createInstrumentPresets();
    
    // Apply instrument preset if provided
    if (this.currentInstrument && this.instrumentPresets[this.currentInstrument]) {
      this.applyInstrumentPreset(this.currentInstrument);
    }

    // Dahili durum
    this.gl = null;
    this.ext = null;
    this.isWebGL2 = false;

    // Zaman
    this.lastUpdateTime = Date.now();
    this.colorUpdateTimer = 0;
    this.rafId = null;

    // Pointer
    this.pointers = [this.createPointer()];
    this.splatStack = [];

    // FBO & program refs
    this.dye = null;
    this.velocity = null;
    this.divergence = null;
    this.curl = null;
    this.pressure = null;

    this.bloom = null;
    this.bloomFramebuffers = [];
    this.sunrays = null;
    this.sunraysTemp = null;

    this.ditheringTexture = null;

    // Blit quad buffers
    this._quadVBO = null;
    this._quadEBO = null;
    this._quadBound = false;

    // Particles
    this.particleState = null;    // Double FBO (RG pos)
    this.particleRes = 0;
    this.particleVBO = null;
    this.particleCount = 0;

    // GridParticles
    this.gridParticleVBO = null;
    this.gridParticleVAO = null;
    this.gridParticleCount = 0;

    // GUI handle
    this.gui = null;

    // Event handlers
    this.handlers = {
      mousedown: (e) => this.handleMouseDown(e),
      mousemove: (e) => this.handleMouseMove(e),
      mouseup:   ()  => this.handleMouseUp(),
      touchstart: (e) => this.handleTouchStart(e),
      touchmove:  (e) => this.handleTouchMove(e),
      touchend:   (e) => this.handleTouchEnd(e),
      keydown:    (e) => this.handleKeyDown(e),
      resize:     ()  => this.onResize()
    };

    // Başlat
    this.init();
  }

  // ---------- Utils ----------
  isMobile() {
    return typeof navigator !== 'undefined' && /Mobi|Android/i.test(navigator.userAgent);
  }
  createPointer() {
    return {
      id: -1,
      texcoordX: 0, texcoordY: 0,
      prevTexcoordX: 0, prevTexcoordY: 0,
      deltaX: 0, deltaY: 0,
      down: false,
      moved: false,
      color: { r: 0.2, g: 0, b: 0.1 } // Default neutral color - centralized
    };
  }
  gaSend(...args) {
    if (typeof window !== 'undefined' && typeof window.ga === 'function') {
      try { window.ga(...args) } catch(_) {}
    }
  }

  // ---------- Init ----------
  init() {
    // Etkileşim
    this.canvas.style.touchAction = 'none';
    this.canvas.style.pointerEvents = 'auto';

    // GL
    const { gl, ext, isWebGL2 } = this.getWebGLContext(this.canvas);
    if (!gl || !ext) throw new Error('WebGL not supported');
    this.gl = gl;
    this.ext = ext;
    this.isWebGL2 = !!isWebGL2;

    // Mobile/Linear filter
    if (this.isMobile()) this.config.DYE_RESOLUTION = Math.min(this.config.DYE_RESOLUTION, 512);
    if (!ext.supportLinearFiltering) {
      this.config.DYE_RESOLUTION = Math.min(this.config.DYE_RESOLUTION, 512);
      this.config.SHADING = false;
      this.config.BLOOM = false;
      this.config.SUNRAYS = false;
    }

    // Canvas boyut
    this.resizeCanvas();

    // Shaders
    this.initShaders();
    this.updateKeywords();

    // Blit helper
    this.blit = this.createBlitHelper();

    // Dither - Using programmatic dithering instead of external texture
    this.ditheringTexture = this.createDitheringTexture();

    // FBO’lar
    this.initFramebuffers();

    // Particles
    this.initParticles();
    
    // GridParticles
    this.initGridParticles();

    // Random başlangıç (uses instrumentColor if provided)
    this.multipleSplats(parseInt(Math.random() * 20) + 5);
    
    // Clear instrumentColor after initial splats (so later splats use real-time colors)
    this.instrumentColor = null;

    // Centralized Color System Integration
    this.initCentralizedColorSystem();

    // Event
    this.attachEvents();

    // Döngü
    this.update();
  }

  // ---------- CENTRALIZED COLOR SYSTEM ----------
  initCentralizedColorSystem() {
    // ✅ GESTURE-BASED: Colors come from hand position only
    // ❌ NO automatic frequency generation
    // ❌ NO real-time sine wave updates
    
    // Status tracking
    this.currentFrequency = 0; // Will be set by hand gesture
    this.currentColor = null;
    this.colorSource = "gesture-based";
    
    // ✅ FIX: Enable real-time color updates during gesture movement
    this.realTimeColorEnabled = true;
    
    // Color palette for optimization
    this.colorPalette = getColorPalette(256);
    this.paletteIndex = 0;
    
    // ❌ REMOVED: startRealTimeColorUpdates()
    // Real-time auto-generator DISABLED - gesture-based only!
    
    // ✅ Logging disabled by default (performance optimization)
  }

  // CENTRALIZED: Y-position → freqToColor → YtoFreq → Frequency → RGB color sampler
  sampleColorFromY01(y01) {
    // NEW INTEGRATION FLOW: PavelFluidSimulation → freqToColor → YtoFreq → frequency → color
    const colorData = getColorFromYPosition(y01);
    
    // ✅ Logging disabled by default (performance optimization)
    
    return { r: colorData.r, g: colorData.g, b: colorData.b };
  }

  /**
   * CENTRALIZED COLOR CONTROL METHODS
   * 
   * These methods connect to freqToColor.js system.
   * PavelFluidSimulation no longer generates colors locally.
   */

  // Update color based on frequency from YtoFreq.js
  updateColorFromFrequency(frequency) {
    const colorData = frequencyToColor(frequency);
    this.currentFrequency = frequency;
    this.currentColor = colorData;
    
    // ✅ FIX: Update ALL pointers' colors immediately
    if (this.pointers && this.pointers.length > 0) {
      this.pointers.forEach(pointer => {
        pointer.color = {
          r: colorData.r,
          g: colorData.g,
          b: colorData.b
        };
      });
    }
    
    // ✅ ALSO: Update global color state for immediate visual feedback
    if (this.config) {
      this.config.COLORFUL = true;
      this.config.COLOR_UPDATE_SPEED = 10;
    }
    
    // ✅ Logging disabled by default (performance optimization)
    
    return colorData;
  }

  // Legacy compatibility - forwards to centralized system
  setColorWheelEnabled(enabled) {
    // Colors are now centralized - this is informational only
    // ✅ Logging disabled by default (performance optimization)
  }

  // Legacy compatibility - forwards to centralized system  
  setColorFrequencyRange(minFreq, maxFreq) {
    // ✅ Logging disabled by default (performance optimization)
  }

  // ---------- GL Context ----------
  getWebGLContext(canvas) {
    const params = { alpha:true, depth:false, stencil:false, antialias:false, preserveDrawingBuffer:false };
    let gl = canvas.getContext('webgl2', params);
    const isWebGL2 = !!gl;
    if (!isWebGL2) {
      gl = canvas.getContext('webgl', params) || canvas.getContext('experimental-webgl', params);
    }
    if (!gl) return { gl: null, ext: null };

    let halfFloat, supportLinearFiltering;
    if (isWebGL2) {
      gl.getExtension('EXT_color_buffer_float');
      supportLinearFiltering = gl.getExtension('OES_texture_float_linear');
    } else {
      halfFloat = gl.getExtension('OES_texture_half_float');
      supportLinearFiltering = gl.getExtension('OES_texture_half_float_linear');
    }
    gl.clearColor(0,0,0,1);

    const halfFloatTexType = isWebGL2 ? gl.HALF_FLOAT : halfFloat.HALF_FLOAT_OES;
    let formatRGBA, formatRG, formatR;
    if (isWebGL2) {
      formatRGBA = this.getSupportedFormat(gl, gl.RGBA16F, gl.RGBA, halfFloatTexType);
      formatRG   = this.getSupportedFormat(gl, gl.RG16F,  gl.RG,   halfFloatTexType);
      formatR    = this.getSupportedFormat(gl, gl.R16F,   gl.RED,  halfFloatTexType);
    } else {
      // WebGL1 fallback
      formatRGBA = this.getSupportedFormat(gl, gl.RGBA, gl.RGBA, halfFloatTexType);
      formatRG   = this.getSupportedFormat(gl, gl.RGBA, gl.RGBA, halfFloatTexType);
      formatR    = this.getSupportedFormat(gl, gl.RGBA, gl.RGBA, halfFloatTexType);
    }

    return {
      gl,
      ext: { formatRGBA, formatRG, formatR, halfFloatTexType, supportLinearFiltering },
      isWebGL2
    };
  }
  getSupportedFormat(gl, internalFormat, format, type) {
    if (!this.supportRenderTextureFormat(gl, internalFormat, format, type)) {
      switch (internalFormat) {
        case gl.R16F:  return this.getSupportedFormat(gl, gl.RG16F, gl.RG, type);
        case gl.RG16F: return this.getSupportedFormat(gl, gl.RGBA16F, gl.RGBA, type);
        default: return null;
      }
    }
    return { internalFormat, format };
  }
  supportRenderTextureFormat(gl, internalFormat, format, type) {
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, 4, 4, 0, format, type, null);

    const fbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0);
    const status = gl.checkFramebufferStatus(gl.FRAMEBUFFER);

    gl.deleteFramebuffer(fbo);
    gl.deleteTexture(texture);
    return status === gl.FRAMEBUFFER_COMPLETE;
  }

  // ---------- Shader helpers ----------
  addKeywords(source, keywords) {
    if (!keywords || !keywords.length) return source;
    return keywords.map(k => `#define ${k}\n`).join('') + source;
  }
  compileShader(type, source, keywords = null) {
    const gl = this.gl;
    source = this.addKeywords(source, keywords);
    const sh = gl.createShader(type);
    gl.shaderSource(sh, source);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) {
      console.trace(gl.getShaderInfoLog(sh));
    }
    return sh;
  }
  createProgram(vs, fs) {
    const gl = this.gl;
    const prog = gl.createProgram();
    gl.attachShader(prog, vs);
    gl.attachShader(prog, fs);
    gl.bindAttribLocation(prog, 0, 'aPosition');
    gl.linkProgram(prog);
    if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
      console.trace(gl.getProgramInfoLog(prog));
    }
    return prog;
  }
  getUniforms(program) {
    const gl = this.gl;
    const uniforms = [];
    const n = gl.getProgramParameter(program, gl.ACTIVE_UNIFORMS);
    for (let i = 0; i < n; i++) {
      const name = gl.getActiveUniform(program, i).name;
      uniforms[name] = gl.getUniformLocation(program, name);
    }
    return uniforms;
  }
  createProgramInstance(vs, fs) {
    const program = this.createProgram(vs, fs);
    const uniforms = this.getUniforms(program);
    return { program, uniforms, bind: () => this.gl.useProgram(program) };
  }
  createMaterialInstance(vertexShader, fragmentShaderSource) {
    const programs = [];
    let activeProgram = null;
    let uniforms = [];
    const setKeywords = (keys) => {
      let hash = 0;
      for (let i = 0; i < keys.length; i++) hash = (hash * 31 + this.hashCode(keys[i])) | 0;
      let prog = programs[hash];
      if (!prog) {
        const fs = this.compileShader(this.gl.FRAGMENT_SHADER, fragmentShaderSource, keys);
        prog = this.createProgram(vertexShader, fs);
        programs[hash] = prog;
      }
      if (prog === activeProgram) return;
      uniforms = this.getUniforms(prog);
      activeProgram = prog;
    };
    const bind = () => this.gl.useProgram(activeProgram);
    return { setKeywords, bind, get uniforms() { return uniforms; } };
  }
  hashCode(s) {
    if (!s) return 0;
    let h = 0;
    for (let i = 0; i < s.length; i++) { h = (h << 5) - h + s.charCodeAt(i); h |= 0; }
    return h;
  }

  // ---------- Shaders ----------
  initShaders() {
    const gl = this.gl;

    // Vertex: tam (vUv + komşular)
    this.baseVertexShader = this.compileShader(gl.VERTEX_SHADER, `
      precision highp float;
      attribute vec2 aPosition;
      varying vec2 vUv;
      varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform vec2 texelSize; // bazı fragment'lar için gerekli
      void main () {
        vUv = aPosition * 0.5 + 0.5;
        vL = vUv - vec2(texelSize.x, 0.0);
        vR = vUv + vec2(texelSize.x, 0.0);
        vT = vUv + vec2(0.0, texelSize.y);
        vB = vUv - vec2(0.0, texelSize.y);
        gl_Position = vec4(aPosition, 0.0, 1.0);
      }
    `);

    // Vertex: yatay/dikey blur için minimal
    this.blurVertexShader = this.compileShader(gl.VERTEX_SHADER, `
      precision highp float;
      attribute vec2 aPosition;
      varying vec2 vUv;
      varying vec2 vL; varying vec2 vR;
      uniform vec2 texelSize;
      void main () {
        vUv = aPosition * 0.5 + 0.5;
        float offset = 1.33333333;
        vL = vUv - texelSize * offset;
        vR = vUv + texelSize * offset;
        gl_Position = vec4(aPosition, 0.0, 1.0);
      }
    `);

    // ---- Fragment setleri (orijinal akış) ----
    this.copyShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; uniform sampler2D uTexture;
      void main () { gl_FragColor = texture2D(uTexture, vUv); }
    `);
    this.clearShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; uniform sampler2D uTexture; uniform float value;
      void main(){ gl_FragColor = value * texture2D(uTexture, vUv); }
    `);
    this.colorShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; uniform vec4 color;
      void main(){ gl_FragColor = color; }
    `);
    this.checkerboardShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv; uniform float aspectRatio;
      #define SCALE 25.0
      void main(){
        vec2 uv = floor(vUv * SCALE * vec2(aspectRatio, 1.0));
        float v = mod(uv.x + uv.y, 2.0); v = v * 0.1 + 0.8;
        gl_FragColor = vec4(vec3(v), 1.0);
      }
    `);

    // ---- DISPLAY (Spherical) ----
    // Not: Bloom ve Sunrays da sUV (küresel UV) ile örneklenir ki boya ile hizalı olsun.
    const displayFrag = `
      precision highp float;
      precision highp sampler2D;
      varying vec2 vUv;

      uniform sampler2D uTexture;    // dye
      uniform sampler2D uBloom;
      uniform sampler2D uSunrays;
      uniform sampler2D uDithering;

      uniform float uFovH;           // radians (horizontal)
      uniform float uFovV;           // radians (vertical)
      uniform float uAspect;         // width/height
      uniform float uYaw;            // radians
      uniform float uPitch;          // radians
      uniform vec2  uDyeTexel;       // 1/dyeSize

      uniform vec2 ditherScale;

      // --- COLORWHEEL UNIFORMS ---
      uniform sampler2D uColorLUT;     // Frequency-to-color lookup texture
      uniform bool  uColorWheelEnabled;
      uniform float uMinFreq;          // 55 Hz
      uniform float uMaxFreq;          // 137.5 Hz

      // --- GRID UNIFORMS ---
      uniform bool  uGridEnabled;
      uniform vec3  uGridColorA;
      uniform vec3  uGridColorB;
      uniform float uGridThickness;
      uniform float uGridFade;
      uniform float uGridEqBand;     // total band width around v=0.5
      uniform int   uGridMeridians;
      uniform int   uGridParallels;
      uniform int   uGridEqDivs;

      // rotate around Y (yaw)
      vec3 rotY(vec3 v, float a){
        float ca=cos(a), sa=sin(a);
        return vec3(ca*v.x + sa*v.z, v.y, -sa*v.x + ca*v.z);
      }
      // rotate around X (pitch)
      vec3 rotX(vec3 v, float a){
        float ca=cos(a), sa=sin(a);
        return vec3(v.x, ca*v.y - sa*v.z, sa*v.y + ca*v.z);
      }

      vec3 screenRay(vec2 uv){
        // uv in [0,1]
        vec2 ndc = uv * 2.0 - 1.0;
        float tH = tan(uFovH * 0.5);
        float tV = tan(uFovV * 0.5);
        // Create proper perspective ray with correct aspect ratio
        vec3 dirCam = vec3(ndc.x * tH, -ndc.y * tV, -1.0);
        dirCam = normalize(dirCam);
        // camera -> world
        vec3 d = rotY(rotX(dirCam, uPitch), uYaw);
        return d;
      }

      vec2 sphereUV(vec3 d){
        // d: direction from center (inside sphere)
        // Normalize direction to ensure proper spherical mapping
        d = normalize(d);
        float u = atan(d.z, d.x) / (2.0*3.141592653589793) + 0.5;
        float v = acos(clamp(d.y, -1.0, 1.0)) / 3.141592653589793;
        return vec2(u, v);
      }

      vec3 linearToGamma(vec3 color){
        color = max(color, vec3(0.0));
        return max(1.055*pow(color, vec3(0.416666667)) - 0.055, vec3(0.0));
      }

      // --- Izgara yardımcıları (AA: uDyeTexel ile yaklaşım) ---
      float aaSmooth(float d, float w){
        // d: çizgiye uzaklık (0 çizgi üstü), w: yarı kalınlık
        // Küçük fakat sabit bir geçiş; texel boyutuyla ilişkili
        float a = max(uDyeTexel.x, uDyeTexel.y) * 0.75;
        return 1.0 - smoothstep(w, w + a, d);
      }

      float meridianMask(vec2 sUV, int count, float thickness){
        if (count <= 0) return 0.0;
        float u = fract(sUV.x);
        float k = float(count) * u;
        float f = abs(k - floor(k + 0.5));  // en yakın tam çizgiye uzaklık (0..0.5)
        float d = f / float(count);         // 0 çizgi, büyüdükçe uzak
        return aaSmooth(d, thickness);
      }

      float parallelMask(vec2 sUV, int count, float thickness){
        if (count <= 0) return 0.0;
        float phi = sUV.y * 3.141592653589793;        // [0,π]
        float spacing = 3.141592653589793 / float(count);
        float d = abs(mod(phi + 0.5*spacing, spacing) - 0.5*spacing) / 3.141592653589793;
        // Kutuplarda aşırı yoğunluk yerine genişletme: sin(phi) ile ölçekle
        float scale = max(0.2, sin(phi));
        return aaSmooth(d*scale, thickness);
      }

      float equatorBandMask(vec2 sUV, float halfBand, float thickness){
        float d = abs(sUV.y - 0.5);                      // ekvatora uzaklık
        // band sınırları daha yumuşak, çizgi kalınlığını biraz büyüt
        return 1.0 - smoothstep(halfBand - thickness, halfBand + thickness, d);
      }

      float equatorDivMask(vec2 sUV, int divs, float thickness, float halfBand){
        if (divs <= 0) return 0.0;
        float band = smoothstep(halfBand, 0.0, abs(sUV.y - 0.5));  // band içinde 1
        float u = fract(sUV.x);
        float k = float(divs) * u;
        float f = abs(k - floor(k + 0.5));
        float d = f / float(divs);
        return band * aaSmooth(d, thickness);
      }

      void main(){
        vec3 dir = screenRay(vUv);
        vec2 sUV = sphereUV(dir);

        // temel renk
        vec3 c = texture2D(uTexture, vec2(fract(sUV.x), sUV.y)).rgb;

        #ifdef SHADING
          // komşular: küresel UV alanında küçük offset ile örnekle
          vec3 lc = texture2D(uTexture, vec2(fract(sUV.x - uDyeTexel.x), sUV.y)).rgb;
          vec3 rc = texture2D(uTexture, vec2(fract(sUV.x + uDyeTexel.x), sUV.y)).rgb;
          vec3 tc = texture2D(uTexture, vec2(fract(sUV.x), clamp(sUV.y + uDyeTexel.y, 0.0, 1.0))).rgb;
          vec3 bc = texture2D(uTexture, vec2(fract(sUV.x), clamp(sUV.y - uDyeTexel.y, 0.0, 1.0))).rgb;
          float dx = length(rc) - length(lc);
          float dy = length(tc) - length(bc);
          vec3  n  = normalize(vec3(dx, dy, length(uDyeTexel)));
          vec3  l  = vec3(0.0, 0.0, 1.0);
          float diffuse = clamp(dot(n, l) + 0.7, 0.7, 1.0);
          c *= diffuse;
        #endif

        #ifdef BLOOM
          vec3 bloom = texture2D(uBloom, vec2(fract(sUV.x), sUV.y)).rgb;
        #endif

        #ifdef SUNRAYS
          float sunr = texture2D(uSunrays, vec2(fract(sUV.x), sUV.y)).r;
          c *= sunr;
          #ifdef BLOOM
            bloom *= sunr;
          #endif
        #endif

        #ifdef BLOOM
          float noise = texture2D(uDithering, vUv * ditherScale).r;
          noise = noise * 2.0 - 1.0;
          bloom += noise / 255.0;
          bloom = linearToGamma(bloom);
          c += bloom;
        #endif

        // --- ColorWheel Frequency-to-Color Mapping ---
        if (uColorWheelEnabled){
          // Convert sphere UV to frequency based on VERTICAL position
          // bottom = 55 Hz (A1 MAVİ), top = 137.5 Hz (C#2 KIŞMIZI)
          float freqT = sUV.y;  // 0 to 1 (inverted if needed)
          
          // Logarithmic mapping
          float logMinFreq = log(uMinFreq);
          float logMaxFreq = log(uMaxFreq);
          float logFreq = mix(logMinFreq, logMaxFreq, freqT);
          float frequency = exp(logFreq);
          
          // Sample color from ColorLUT (invert Y if needed: bottom=A1, top=C#2)
          vec3 freqColor = texture2D(uColorLUT, vec2(freqT, 0.5)).rgb;
          
          // Mix frequency color with dye color
          // Stronger colorwheel influence in brighter dye areas
          float brightness = length(c);
          float mixFactor = brightness * brightness * 0.8;  // Quadratic falloff
          c = mix(c, freqColor * brightness, mixFactor);
        }

        // --- Spherical Grid Overlay ---
        if (uGridEnabled){
          float px = uGridThickness * 0.5 * max(uDyeTexel.x, uDyeTexel.y);  // ~yarı kalınlık
          float mer = meridianMask(sUV, uGridMeridians, px);
          float par = parallelMask(sUV, uGridParallels, px);
          float eqb = equatorBandMask(sUV, uGridEqBand * 0.5, px * 1.5);
          float eqd = equatorDivMask(sUV, uGridEqDivs, px, uGridEqBand * 0.5);

          float gridA = clamp(max(mer, par) + max(eqb, eqd), 0.0, 1.0);

          // kutuplara doğru isteğe bağlı solma
          float fade = mix(1.0, sin(sUV.y * 3.141592653589793), uGridFade);

          vec3 gridCol = mix(uGridColorA, uGridColorB, 0.6);
          c = mix(gridCol, c, 1.0 - gridA * fade);
        }

        float a = max(c.r, max(c.g, c.b));
        gl_FragColor = vec4(c, a);
      }
    `;
    this.displayMaterial = this.createMaterialInstance(this.baseVertexShader, displayFrag);

    // ---- Bloom ----
    this.bloomPrefilterShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; uniform sampler2D uTexture;
      uniform vec3 curve; uniform float threshold;
      void main(){
        vec3 c = texture2D(uTexture, vUv).rgb;
        float br = max(c.r, max(c.g, c.b));
        float rq = clamp(br - curve.x, 0.0, curve.y);
        rq = curve.z * rq * rq;
        c *= max(rq, br - threshold) / max(br, 0.0001);
        gl_FragColor = vec4(c, 0.0);
      }
    `);
    this.bloomBlurShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uTexture;
      void main(){
        vec4 s = vec4(0.0);
        s += texture2D(uTexture, vL);
        s += texture2D(uTexture, vR);
        s += texture2D(uTexture, vT);
        s += texture2D(uTexture, vB);
        gl_FragColor = 0.25 * s;
      }
    `);
    this.bloomFinalShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uTexture; uniform float intensity;
      void main(){
        vec4 s = vec4(0.0);
        s += texture2D(uTexture, vL);
        s += texture2D(uTexture, vR);
        s += texture2D(uTexture, vT);
        s += texture2D(uTexture, vB);
        gl_FragColor = 0.25 * s * intensity;
      }
    `);

    // ---- Sunrays ----
    this.sunraysMaskShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv; uniform sampler2D uTexture;
      void main(){
        vec4 c = texture2D(uTexture, vUv);
        float br = max(c.r, max(c.g, c.b));
        c.a = 1.0 - min(max(br * 20.0, 0.0), 0.8);
        gl_FragColor = c;
      }
    `);
    this.sunraysShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv; uniform sampler2D uTexture; uniform float weight;
      #define ITERATIONS 16
      void main(){
        float Density = 0.3, Decay = 0.95, Exposure = 0.7;
        vec2 coord = vUv;
        vec2 dir = vUv - 0.5;
        dir *= 1.0 / float(ITERATIONS) * Density;
        float illuminationDecay = 1.0;
        float col = texture2D(uTexture, vUv).a;
        for (int i = 0; i < ITERATIONS; i++) {
          coord -= dir;
          float c = texture2D(uTexture, coord).a;
          col += c * illuminationDecay * weight;
          illuminationDecay *= Decay;
        }
        gl_FragColor = vec4(col * Exposure, 0.0, 0.0, 1.0);
      }
    `);

    // ---- Fluid core ----
    this.splatShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv;
      uniform sampler2D uTarget;
      uniform float aspectRatio;
      uniform vec3 color; uniform vec2 point; uniform float radius;
      void main(){
        vec2 p = vUv - point;
        p.x *= aspectRatio;
        vec3 splat = exp(-dot(p,p)/radius) * color;
        vec3 base = texture2D(uTarget, vUv).xyz;
        gl_FragColor = vec4(base + splat, 1.0);
      }
    `);
    this.advectionShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv;
      uniform sampler2D uVelocity; uniform sampler2D uSource;
      uniform vec2 texelSize; uniform vec2 dyeTexelSize;
      uniform float dt; uniform float dissipation;
      vec4 bilerp (sampler2D sam, vec2 uv, vec2 tsize){
        vec2 st = uv / tsize - 0.5;
        vec2 iuv = floor(st);
        vec2 fuv = fract(st);
        vec4 a = texture2D(sam, (iuv + vec2(0.5, 0.5)) * tsize);
        vec4 b = texture2D(sam, (iuv + vec2(1.5, 0.5)) * tsize);
        vec4 c = texture2D(sam, (iuv + vec2(0.5, 1.5)) * tsize);
        vec4 d = texture2D(sam, (iuv + vec2(1.5, 1.5)) * tsize);
        return mix(mix(a, b, fuv.x), mix(c, d, fuv.x), fuv.y);
      }
      void main(){
        #ifdef MANUAL_FILTERING
          vec2 coord = vUv - dt * bilerp(uVelocity, vUv, texelSize).xy * texelSize;
          vec4 result = bilerp(uSource, coord, dyeTexelSize);
        #else
          vec2 coord = vUv - dt * texture2D(uVelocity, vUv).xy * texelSize;
          vec4 result = texture2D(uSource, coord);
        #endif
        float decay = 1.0 + dissipation * dt;
        gl_FragColor = result / decay;
      }
    `, this.ext.supportLinearFiltering ? null : ['MANUAL_FILTERING']);
    this.divergenceShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uVelocity;
      void main(){
        float L = texture2D(uVelocity, vL).x;
        float R = texture2D(uVelocity, vR).x;
        float T = texture2D(uVelocity, vT).y;
        float B = texture2D(uVelocity, vB).y;
        vec2  C = texture2D(uVelocity, vUv).xy;
        if (vL.x < 0.0) L = -C.x;
        if (vR.x > 1.0) R = -C.x;
        if (vT.y > 1.0) T = -C.y;
        if (vB.y < 0.0) B = -C.y;
        float div = 0.5 * (R - L + T - B);
        gl_FragColor = vec4(div, 0.0, 0.0, 1.0);
      }
    `);
    this.curlShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uVelocity;
      void main(){
        float L = texture2D(uVelocity, vL).y;
        float R = texture2D(uVelocity, vR).y;
        float T = texture2D(uVelocity, vT).x;
        float B = texture2D(uVelocity, vB).x;
        float vort = R - L - T + B;
        gl_FragColor = vec4(0.5 * vort, 0.0, 0.0, 1.0);
      }
    `);
    this.vorticityShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uVelocity; uniform sampler2D uCurl;
      uniform float curl; uniform float dt;
      void main(){
        float L = texture2D(uCurl, vL).x;
        float R = texture2D(uCurl, vR).x;
        float T = texture2D(uCurl, vT).x;
        float B = texture2D(uCurl, vB).x;
        float C = texture2D(uCurl, vUv).x;
        vec2 force = 0.5 * vec2(abs(T)-abs(B), abs(R)-abs(L));
        force /= length(force) + 0.0001;
        force *= curl * C;
        force.y *= -1.0;
        vec2 vel = texture2D(uVelocity, vUv).xy;
        vel += force * dt;
        vel = clamp(vel, -1000.0, 1000.0);
        gl_FragColor = vec4(vel, 0.0, 1.0);
      }
    `);
    this.pressureShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uPressure; uniform sampler2D uDivergence;
      void main(){
        float L = texture2D(uPressure, vL).x;
        float R = texture2D(uPressure, vR).x;
        float T = texture2D(uPressure, vT).x;
        float B = texture2D(uPressure, vB).x;
        float divergence = texture2D(uDivergence, vUv).x;
        float pressure = (L + R + B + T - divergence) * 0.25;
        gl_FragColor = vec4(pressure, 0.0, 0.0, 1.0);
      }
    `);
    this.gradientSubtractShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR; varying vec2 vT; varying vec2 vB;
      uniform sampler2D uPressure; uniform sampler2D uVelocity;
      void main(){
        float L = texture2D(uPressure, vL).x;
        float R = texture2D(uPressure, vR).x;
        float T = texture2D(uPressure, vT).x;
        float B = texture2D(uPressure, vB).x;
        vec2 vel = texture2D(uVelocity, vUv).xy;
        vel -= vec2(R - L, T - B);
        gl_FragColor = vec4(vel, 0.0, 1.0);
      }
    `);

    // Programlar (doğru VS ile!)
    this.copyProgram             = this.createProgramInstance(this.baseVertexShader, this.copyShader);
    this.clearProgram            = this.createProgramInstance(this.baseVertexShader, this.clearShader);
    this.colorProgram            = this.createProgramInstance(this.baseVertexShader, this.colorShader);
    this.checkerboardProgram     = this.createProgramInstance(this.baseVertexShader, this.checkerboardShader);

    // Bloom: vT/vB isteyenler baseVertex ile linklenir
    this.bloomPrefilterProgram   = this.createProgramInstance(this.baseVertexShader, this.bloomPrefilterShader);
    this.bloomBlurProgram        = this.createProgramInstance(this.baseVertexShader, this.bloomBlurShader);
    this.bloomFinalProgram       = this.createProgramInstance(this.baseVertexShader, this.bloomFinalShader);

    // Sunrays
    this.sunraysMaskProgram      = this.createProgramInstance(this.baseVertexShader, this.sunraysMaskShader);
    this.sunraysProgram          = this.createProgramInstance(this.baseVertexShader, this.sunraysShader);

    // Fluid
    this.splatProgram            = this.createProgramInstance(this.baseVertexShader, this.splatShader);
    this.advectionProgram        = this.createProgramInstance(this.baseVertexShader, this.advectionShader);
    this.divergenceProgram       = this.createProgramInstance(this.baseVertexShader, this.divergenceShader);
    this.curlProgram             = this.createProgramInstance(this.baseVertexShader, this.curlShader);
    this.vorticityProgram        = this.createProgramInstance(this.baseVertexShader, this.vorticityShader);
    this.pressureProgram         = this.createProgramInstance(this.baseVertexShader, this.pressureShader);
    this.gradientSubtractProgram = this.createProgramInstance(this.baseVertexShader, this.gradientSubtractShader);

    // Display material keywords (ilk kurulum)
    this.updateKeywords();

    // --- Parçacık shader’ları ---
    this.initParticleShaders();
    this.initGridParticleShaders();
  }

  updateKeywords() {
    if (!this.displayMaterial) return;
    const keys = [];
    if (this.config.SHADING)  keys.push('SHADING');
    if (this.config.BLOOM)    keys.push('BLOOM');
    if (this.config.SUNRAYS)  keys.push('SUNRAYS');
    this.displayMaterial.setKeywords(keys);
  }

  // ---------- Particles ----------
  initParticleShaders() {
    const gl = this.gl;

    // Seed (random fill)
    this.particleSeedShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; varying vec2 vUv;
      float rand(vec2 c){ return fract(sin(dot(c, vec2(12.9898,78.233))) * 43758.5453); }
      void main(){
        vec2 r = vec2(rand(vUv+0.11), rand(vUv+0.73));
        vec2 pos = fract(vUv + r * 0.123);
        gl_FragColor = vec4(pos, 0.0, 1.0);
      }
    `);
    this.particleUpdateShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUv;
      uniform sampler2D uPositions; uniform sampler2D uVelocity;
      uniform vec2 velTexelSize; uniform float dt; uniform float advection;
      void main(){
        vec2 pos = texture2D(uPositions, vUv).xy;
        vec2 vel = texture2D(uVelocity, pos).xy;
        pos += dt * vel * velTexelSize * advection;
        pos = fract(pos);
        gl_FragColor = vec4(pos, 0.0, 1.0);
      }
    `);

    // Draw (küre projeksiyonu ile ekran)
    this.particleDrawVertexShader = this.compileShader(gl.VERTEX_SHADER, `
      precision highp float;
      attribute vec2 aPosition;        // UV in state texture
      uniform sampler2D uPositions;    // RG (u,v)
      uniform float uPointSize;
      uniform float uFovH; uniform float uFovV; uniform float uAspect; uniform float uYaw; uniform float uPitch;

      varying vec2 vParticleUV;        // dye sampling için

      vec3 rotY(vec3 v, float a){ float c=cos(a), s=sin(a); return vec3(c*v.x + s*v.z, v.y, -s*v.x + c*v.z); }
      vec3 rotX(vec3 v, float a){ float c=cos(a), s=sin(a); return vec3(v.x, c*v.y - s*v.z, s*v.y + c*v.z); }

      // sphere uv -> direction
      vec3 fromSphereUV(vec2 uv){
        float theta = uv.x * 6.283185307179586;   // 2*pi
        float phi   = uv.y * 3.141592653589793;   // pi
        float sinf = sin(phi), cosf = cos(phi);
        return normalize(vec3(cos(theta)*sinf, cosf, sin(theta)*sinf));
      }

      // world dir -> screen ndc
      vec2 dirToNDC(vec3 dirWorld, float fovH, float fovV, float aspect, float yaw, float pitch){
        // world -> camera (display ile ters sırada ve ters açıyla)
        vec3 dirCam = rotX(rotY(dirWorld, -yaw), -pitch);

        // z = -1 düzlemiyle kesiştir (display'deki screenRay ile birebir tutarlılık)
        float s = -1.0 / dirCam.z;
        vec2 pos = vec2(dirCam.x, dirCam.y) * s;

        float tH = tan(fovH * 0.5);
        float tV = tan(fovV * 0.5);
        // Display shader'da -ndc.y kullanılıyor, burada da aynı dönüşüm
        float ndcX =  pos.x / tH;
        float ndcY =  pos.y / tV;

        return vec2(ndcX, ndcY);
      }

      void main(){
        vec2 posUV = texture2D(uPositions, aPosition).xy;
        vParticleUV = posUV;

        vec3 dirW = fromSphereUV(posUV);
        vec2 ndc  = dirToNDC(dirW, uFovH, uFovV, uAspect, uYaw, uPitch);

        gl_Position = vec4(ndc, 0.0, 1.0);
        gl_PointSize = uPointSize;
      }
    `);
    this.particleDrawFragmentShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vParticleUV;
      uniform sampler2D uDye; uniform float uAlpha; uniform float uBrightness;
      void main(){
        vec2 d = gl_PointCoord - 0.5;
        if (dot(d,d) > 0.25) discard;
        vec3 col = texture2D(uDye, vParticleUV).rgb * uBrightness;
        gl_FragColor = vec4(col, uAlpha);
      }
    `);

    // Programlar
    this.particleSeedProgram   = this.createProgramInstance(this.baseVertexShader, this.particleSeedShader);
    this.particleUpdateProgram = this.createProgramInstance(this.baseVertexShader, this.particleUpdateShader);
    this.particleDrawProgram   = this.createProgramInstance(this.particleDrawVertexShader, this.particleDrawFragmentShader);
  }
  
  // ---------- GridParticles Shaders ----------
  initGridParticleShaders() {
    const gl = this.gl;
    
    // GridParticle Vertex Shader
    this.gridParticleVertexShader = this.compileShader(gl.VERTEX_SHADER, `
      precision highp float;
      attribute vec3 aPosition;        // 3D world position
      attribute float aParticleId;     // unique particle ID
      uniform float uPointSize;
      uniform float uFovH; uniform float uFovV; uniform float uAspect; 
      uniform float uYaw; uniform float uPitch;
      uniform float uRadius;
      uniform float uTime;  // float efekti için zaman
      
      varying vec2 vUV;                // spherical UV for dye sampling
      varying vec3 vN;                 // surface normal (inward)
      varying vec3 vView;              // view direction
      
      vec3 rotY(vec3 v, float a){ float c=cos(a), s=sin(a); return vec3(c*v.x + s*v.z, v.y, -s*v.x + c*v.z); }
      vec3 rotX(vec3 v, float a){ float c=cos(a), s=sin(a); return vec3(v.x, c*v.y - s*v.z, s*v.y + c*v.z); }
      
      // world dir -> screen ndc
      vec2 dirToNDC(vec3 dirWorld, float fovH, float fovV, float aspect, float yaw, float pitch){
        // world -> camera (display ile ters sırada ve ters açıyla)
        vec3 dirCam = rotX(rotY(dirWorld, -yaw), -pitch);
        
        // z = -1 düzlemiyle kesiştir
        float s = -1.0 / dirCam.z;
        vec2 pos = vec2(dirCam.x, dirCam.y) * s;
        
        float tH = tan(fovH * 0.5);
        float tV = tan(fovV * 0.5);
        return vec2(pos.x / tH, -pos.y / tV);
      }
      
      void main(){
        vec3 pos = aPosition;
        
        // Spherical UV hesapla (dye sampling için)
        float theta = atan(pos.z, pos.x) / 6.283185307179586 + 0.5; // [0,1]
        float phi = acos(pos.y / uRadius) / 3.141592653589793;       // [0,1]
        vUV = vec2(theta, phi);
        
        // Her particle için bağımsız float efekti - grid pozisyonu etrafında
        float seed1 = fract(sin(aParticleId * 12.9898) * 43758.5453);
        float seed2 = fract(sin(aParticleId * 78.233) * 43758.5453);
        float seed3 = fract(sin(aParticleId * 93.9898) * 43758.5453);
        
        // X, Y, Z eksenlerinde ayrı ayrı hareket - çok büyük genlik
        float offsetX = sin(uTime * 1.0 + aParticleId * 0.1) * 1.0;
        float offsetY = sin(uTime * 1.2 + aParticleId * 0.15) * 1.0;
        float offsetZ = sin(uTime * 0.8 + aParticleId * 0.12) * 1.0;
        
        pos += vec3(offsetX, offsetY, offsetZ);
        
        // Normal ve view direction
        vN = -normalize(pos);  // inward normal
        vView = -pos;          // view direction (eye at origin)
        
        // Screen projection
        vec2 ndc = dirToNDC(normalize(pos), uFovH, uFovV, uAspect, uYaw, uPitch);
        
        gl_Position = vec4(ndc, 0.1, 1.0);  // behind fluid (z=0.0)
        
        // Point size with polar compensation
        float latCompensation = mix(1.0, 0.85, abs(vUV.y - 0.5) * 2.0);
        gl_PointSize = uPointSize * latCompensation;
      }
    `);
    
    // GridParticle Fragment Shader
    this.gridParticleFragmentShader = this.compileShader(gl.FRAGMENT_SHADER, `
      precision highp float; precision highp sampler2D;
      varying vec2 vUV;
      varying vec3 vN;
      varying vec3 vView;
      
      uniform sampler2D uTexture;      // dye texture
      uniform sampler2D uBloom;        // bloom texture
      uniform sampler2D uSunrays;      // sunrays texture
      uniform vec3 uIce;               // ice color
      uniform vec3 uWhite;             // white color
      uniform float uIntensity;
      uniform float uAlpha;
      uniform float uBloomFactor;
      uniform bool uEqHighlight;
      
      void main(){
        // Point sprite disk mask with AA
        vec2 d = gl_PointCoord - 0.5;
        float dist = length(d);
        float alpha = 1.0 - smoothstep(0.4, 0.5, dist);
        if (alpha < 0.01) discard;
        
        // Dye-aware toning
        vec3 dye = texture2D(uTexture, vUV).rgb;
        float luma = dot(dye, vec3(0.299, 0.587, 0.114));
        vec3 baseColor = mix(uIce, uWhite, 0.6);
        vec3 color = baseColor * (uIntensity * (0.75 + 0.25 * luma));
        
        // Sunrays contribution
        color *= texture2D(uSunrays, vUV).r;
        
        // Pseudo-Fresnel (edge highlight)
        vec3 N = normalize(vN);
        vec3 V = normalize(vView);
        float fresnel = pow(1.0 - clamp(dot(N, V), 0.0, 1.0), 3.0);
        color = mix(color, color * 1.25, 0.15 * fresnel);
        
        // Equator highlight
        if (uEqHighlight) {
          float eqBand = 0.1; // 10% of sphere height
          float eqDist = abs(vUV.y - 0.5);
          float eqMask = 1.0 - smoothstep(0.0, eqBand, eqDist);
          color = mix(color, uWhite, 0.25 * eqMask);
        }
        
        gl_FragColor = vec4(color, uAlpha * alpha);
      }
    `);
    
    // Program
    this.gridParticleProgram = this.createProgramInstance(this.gridParticleVertexShader, this.gridParticleFragmentShader);
  }

  // ---------- GUI ----------
  startGUI() {
    if (!dat || !dat.GUI) { console.warn('dat.GUI not available'); return; }
    if (this.gui) { console.log('GUI already exists'); return; }

    // 1) Var olan TÜM dat.GUI panellerini temizle (HMR / tekrar init)
    document.querySelectorAll('.dg').forEach(el => {
      try { el.remove(); } catch (_) {}
    });

    // 2) Global bir önceki örnek varsa destroy
    if (window.__PAVEL_FLUID_GUI && typeof window.__PAVEL_FLUID_GUI.destroy === 'function') {
      try { window.__PAVEL_FLUID_GUI.destroy(); } catch (_) {}
      window.__PAVEL_FLUID_GUI = null;
    }

    // 3) Host hazırla ve GUI'yi autoPlace kapalı şekilde oluştur
    const host = this.ensureGuiHost();
    const gui = new dat.GUI({ autoPlace: false, width: 320, hideable: false });
    host.appendChild(gui.domElement);

    this.gui = gui;
    window.__PAVEL_FLUID_GUI = gui; // global tekil koruma

    // === ANA KONTROLLER ===
    gui.add(this.config, 'DYE_RESOLUTION', { '1024': 1024, '512': 512, '256': 256, '128': 128 })
      .name('Quality').onFinishChange(() => this.initFramebuffers());
    gui.add(this.config, 'SIM_RESOLUTION', { '32': 32, '64': 64, '128': 128, '256': 256 })
      .name('Sim Resolution').onFinishChange(() => this.initFramebuffers());
    gui.add(this.config, 'DENSITY_DISSIPATION', 0, 4).name('Density Diffusion');
    gui.add(this.config, 'VELOCITY_DISSIPATION', 0, 4).name('Velocity Diffusion');
    gui.add(this.config, 'PRESSURE', 0, 1).name('Pressure');
    gui.add(this.config, 'CURL', 0, 50).name('Vorticity').step(1);
    gui.add(this.config, 'SPLAT_RADIUS', 0.01, 1.0).name('Splat Radius');
    gui.add(this.config, 'SHADING').name('Shading').onFinishChange(() => this.updateKeywords());
    gui.add(this.config, 'COLORFUL').name('Colorful');
    gui.add(this.config, 'PAUSED').name('Paused'); // .listen() bazı build'lerde yok
    gui.add({ splats: () => this.splatStack.push((Math.random()*20|0)+5) }, 'splats').name('Random Splats');

    // === BLOOM ===
    const bloomFolder = gui.addFolder('Bloom');
    bloomFolder.add(this.config, 'BLOOM').name('Enabled').onFinishChange(() => this.updateKeywords());
    bloomFolder.add(this.config, 'BLOOM_INTENSITY', 0.1, 2.0).name('Intensity');
    bloomFolder.add(this.config, 'BLOOM_THRESHOLD', 0.0, 1.0).name('Threshold');

    // === SUNRAYS ===
    const sunFolder = gui.addFolder('Sunrays');
    sunFolder.add(this.config, 'SUNRAYS').name('Enabled').onFinishChange(() => this.updateKeywords());
    sunFolder.add(this.config, 'SUNRAYS_WEIGHT', 0.3, 1.0).name('Weight');

    // === CAMERA ===
    const camFolder = gui.addFolder('Camera');
    camFolder.add(this.config, 'CAMERA_FOV_H', 0.4, 2.2).name('FOV H (rad)');
    camFolder.add(this.config, 'CAMERA_FOV_V', 0.4, 2.2).name('FOV V (rad)');
    camFolder.add(this.config, 'CAMERA_AUTO_ROTATE').name('Auto Rotate');
    camFolder.add(this.config, 'CAMERA_ROTATION_PERIOD', 5, 120, 1).name('Period (sec)');
    camFolder.add(this.config, 'CAMERA_YAW', -Math.PI, Math.PI).name('Yaw (manual)');
    camFolder.add(this.config, 'CAMERA_PITCH', -1.3, 1.3).name('Pitch');

    // === GRID PARTICLES ===
    const grid = gui.addFolder('Grid Particles');
    grid.add(this.config, 'GRID_ENABLED').name('Enabled');
    grid.add(this.config, 'GRID_TOTAL', 512, 4096, 1).name('Total Points').listen();
    grid.add(this.config, 'GRID_MERIDIANS', 8, 64, 1).name('Meridians');
    grid.add(this.config, 'GRID_PARALLELS', 8, 64, 1).name('Parallels');
    grid.add(this.config, 'GRID_EXCLUDE_POLAR_DEG', 0, 15, 0.5).name('Polar Cut (deg)');
    grid.add(this.config, 'GRID_EQ_HIGHLIGHT').name('Equator Highlight');
    grid.add(this.config, 'GRID_WEIGHT_M', 0.0, 1.0, 0.01).name('Meridian Weight');
    grid.add(this.config, 'GRID_WEIGHT_P', 0.0, 1.0, 0.01).name('Parallel Weight');
    grid.add(this.config, 'GRID_POINT_SIZE_PX', 1.0, 5.0, 0.1).name('Point Size (px)');
    grid.addColor(this.config, 'GRID_COLOR_ICE').name('Ice Color');
    grid.addColor(this.config, 'GRID_COLOR_WHITE').name('White Color');
    grid.add(this.config, 'GRID_INTENSITY', 0.0, 2.0, 0.01).name('Intensity');
    grid.add(this.config, 'GRID_ALPHA', 0.0, 1.0, 0.01).name('Alpha');
    grid.add(this.config, 'GRID_BLOOM_FACTOR', 0.0, 1.0, 0.01).name('Bloom Factor');
    grid.add(this.config, 'GRID_RADIUS', 1.0, 10.0, 0.1).name('Sphere Radius');

    // === CAPTURE ===
    const cap = gui.addFolder('Capture');
    cap.addColor(this.config, 'BACK_COLOR').name('Background');
    cap.add(this.config, 'TRANSPARENT').name('Transparent');
    cap.add({ shot: () => this.captureScreenshot() }, 'shot').name('Screenshot');

    if (this.isMobile()) gui.close();
  }

  ensureGuiHost() {
    let host = document.getElementById('pavel-gui-host');
    if (!host) {
      host = document.createElement('div');
      host.id = 'pavel-gui-host';
      Object.assign(host.style, {
        position: 'fixed',
        top: '12px',   // İsterseniz 'bottom:12px,left:12px' yapıp konumu değiştirin
        right: '12px',
        zIndex: 10000,
        pointerEvents: 'auto'
      });
      document.body.appendChild(host);
    }
    return host;
  }

  // ---------- Screenshot ----------
  captureScreenshot() {
    const res = this.getResolution(this.config.CAPTURE_RESOLUTION);
    const target = this.createFBO(res.width, res.height, this.ext.formatRGBA.internalFormat, this.ext.formatRGBA.format, this.ext.halfFloatTexType, this.gl.NEAREST);
    this.render(target);
    let texture = this.framebufferToTexture(target);
    texture = this.normalizeTexture(texture, target.width, target.height);
    const capCanvas = this.textureToCanvas(texture, target.width, target.height);
    const datauri = capCanvas.toDataURL();
    this.downloadURI('fluid.png', datauri);
    URL.revokeObjectURL(datauri);
  }
  framebufferToTexture(target){
    const gl = this.gl;
    gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
    const len = target.width * target.height * 4;
    const tex = new Float32Array(len);
    gl.readPixels(0,0,target.width,target.height, gl.RGBA, gl.FLOAT, tex);
    return tex;
  }
  normalizeTexture(texture, w, h){
    const out = new Uint8Array(texture.length);
    let id=0;
    for (let i=h-1; i>=0; i--) {
      for (let j=0;j<w;j++){
        const nid = i*w*4 + j*4;
        out[nid+0] = this.clamp01(texture[id+0]) * 255;
        out[nid+1] = this.clamp01(texture[id+1]) * 255;
        out[nid+2] = this.clamp01(texture[id+2]) * 255;
        out[nid+3] = this.clamp01(texture[id+3]) * 255;
        id += 4;
      }
    }
    return out;
  }
  textureToCanvas(texture, w, h){
    const cvs = document.createElement('canvas');
    const ctx = cvs.getContext('2d');
    cvs.width=w; cvs.height=h;
    const img = ctx.createImageData(w,h);
    img.data.set(texture);
    ctx.putImageData(img,0,0);
    return cvs;
  }
  downloadURI(filename, uri){
    const a = document.createElement('a');
    a.download = filename; a.href = uri; document.body.appendChild(a); a.click(); document.body.removeChild(a);
  }
  clamp01(x){ return Math.min(Math.max(x,0),1); }

  // ---------- FBO helpers ----------
  createFBO(w,h, internalFormat, format, type, param){
    const gl = this.gl;
    gl.activeTexture(gl.TEXTURE0);
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, param);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, param);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.texImage2D(gl.TEXTURE_2D, 0, internalFormat, w, h, 0, format, type, null);
    const fbo = gl.createFramebuffer();
    gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, texture, 0);
    gl.viewport(0,0,w,h); gl.clear(gl.COLOR_BUFFER_BIT);
    return {
      texture, fbo, width:w, height:h,
      texelSizeX: 1.0/w, texelSizeY: 1.0/h,
      attach: (id)=>{ gl.activeTexture(gl.TEXTURE0+id); gl.bindTexture(gl.TEXTURE_2D, texture); return id; }
    };
  }
  createDoubleFBO(w,h, internalFormat, format, type, param){
    let fbo1 = this.createFBO(w,h, internalFormat, format, type, param);
    let fbo2 = this.createFBO(w,h, internalFormat, format, type, param);
    return {
      width:w, height:h, texelSizeX:fbo1.texelSizeX, texelSizeY:fbo1.texelSizeY,
      get read(){ return fbo1; }, set read(v){ fbo1=v; },
      get write(){ return fbo2; }, set write(v){ fbo2=v; },
      swap(){ const t=fbo1; fbo1=fbo2; fbo2=t; }
    };
  }
  resizeFBO(target, w,h, internalFormat, format, type, param){
    const newFBO = this.createFBO(w,h, internalFormat, format, type, param);
    this.copyProgram.bind();
    this.gl.uniform1i(this.copyProgram.uniforms.uTexture, target.attach(0));
    this.blit(newFBO);
    return newFBO;
  }
  resizeDoubleFBO(target, w,h, internalFormat, format, type, param){
    if (target.width === w && target.height === h) return target;
    target.read = this.resizeFBO(target.read, w,h, internalFormat, format, type, param);
    target.write = this.createFBO(w,h, internalFormat, format, type, param);
    target.width=w; target.height=h;
    target.texelSizeX = 1.0/w; target.texelSizeY = 1.0/h;
    return target;
  }
  createTextureAsync(url){
    const gl = this.gl;
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    gl.texImage2D(gl.TEXTURE_2D,0, gl.RGB, 1,1,0, gl.RGB, gl.UNSIGNED_BYTE, new Uint8Array([255,255,255]));
    const obj = {
      texture, width:1, height:1,
      attach:(id)=>{ gl.activeTexture(gl.TEXTURE0+id); gl.bindTexture(gl.TEXTURE_2D, texture); return id; }
    };
    const img = new Image();
    img.onload = ()=>{
      obj.width = img.width; obj.height = img.height;
      gl.bindTexture(gl.TEXTURE_2D, texture);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
    };
    img.src = url;
    return obj;
  }

  createDitheringTexture(){
    const gl = this.gl;
    const texture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.REPEAT);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.REPEAT);
    
    // Create a simple 4x4 dithering pattern
    const size = 4;
    const data = new Uint8Array(size * size * 3);
    for (let i = 0; i < size * size; i++) {
      const x = i % size;
      const y = Math.floor(i / size);
      const value = (x + y) % 2 === 0 ? 255 : 0;
      data[i * 3] = value;     // R
      data[i * 3 + 1] = value; // G
      data[i * 3 + 2] = value; // B
    }
    
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, size, size, 0, gl.RGB, gl.UNSIGNED_BYTE, data);
    
    return {
      texture, width: size, height: size,
      attach: (id) => { gl.activeTexture(gl.TEXTURE0 + id); gl.bindTexture(gl.TEXTURE_2D, texture); return id; }
    };
  }

  // ---------- Blit helper ----------
  createBlitHelper(){
    const gl = this.gl;
    this._quadVBO = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this._quadVBO);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, -1,1, 1,1, 1,-1]), gl.STATIC_DRAW);

    this._quadEBO = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this._quadEBO);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array([0,1,2, 0,2,3]), gl.STATIC_DRAW);

    gl.vertexAttribPointer(0,2, gl.FLOAT, false, 0,0);
    gl.enableVertexAttribArray(0);
    this._quadBound = true;

    const bindQuad = ()=>{
      if (this._quadBound) return;
      gl.bindBuffer(gl.ARRAY_BUFFER, this._quadVBO);
      gl.vertexAttribPointer(0,2, gl.FLOAT, false, 0,0);
      gl.enableVertexAttribArray(0);
      gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this._quadEBO);
      this._quadBound = true;
    };

    return (target, clear=false)=>{
      bindQuad();
      if (target == null) {
        gl.viewport(0,0, gl.drawingBufferWidth, gl.drawingBufferHeight);
        gl.bindFramebuffer(gl.FRAMEBUFFER, null);
      } else {
        gl.viewport(0,0, target.width, target.height);
        gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
      }
      if (clear){ gl.clearColor(0,0,0,1); gl.clear(gl.COLOR_BUFFER_BIT); }
      gl.drawElements(gl.TRIANGLES, 6, gl.UNSIGNED_SHORT, 0);
    };
  }

  // ---------- Framebuffers ----------
  initFramebuffers(){
    const gl = this.gl;
    const simRes = this.getResolution(this.config.SIM_RESOLUTION);
    const dyeRes = this.getResolution(this.config.DYE_RESOLUTION);

    const texType = this.ext.halfFloatTexType;
    const rgba = this.ext.formatRGBA;
    const rg   = this.ext.formatRG;
    const r    = this.ext.formatR;
    const filtering = this.ext.supportLinearFiltering ? gl.LINEAR : gl.NEAREST;

    gl.disable(gl.BLEND);

    if (!this.dye)  this.dye  = this.createDoubleFBO(dyeRes.width, dyeRes.height, rgba.internalFormat, rgba.format, texType, filtering);
    else            this.dye  = this.resizeDoubleFBO(this.dye, dyeRes.width, dyeRes.height, rgba.internalFormat, rgba.format, texType, filtering);

    if (!this.velocity) this.velocity = this.createDoubleFBO(simRes.width, simRes.height, rg.internalFormat, rg.format, texType, filtering);
    else                this.velocity = this.resizeDoubleFBO(this.velocity, simRes.width, simRes.height, rg.internalFormat, rg.format, texType, filtering);

    this.divergence = this.createFBO(simRes.width, simRes.height, r.internalFormat, r.format, texType, gl.NEAREST);
    this.curl       = this.createFBO(simRes.width, simRes.height, r.internalFormat, r.format, texType, gl.NEAREST);
    this.pressure   = this.createDoubleFBO(simRes.width, simRes.height, r.internalFormat, r.format, texType, gl.NEAREST);

    this.initBloomFramebuffers();
    this.initSunraysFramebuffers();
  }
  initBloomFramebuffers(){
    const res = this.getResolution(this.config.BLOOM_RESOLUTION);
    const rgba = this.ext.formatRGBA;
    const type = this.ext.halfFloatTexType;
    const filtering = this.ext.supportLinearFiltering ? this.gl.LINEAR : this.gl.NEAREST;

    this.bloom = this.createFBO(res.width, res.height, rgba.internalFormat, rgba.format, type, filtering);
    this.bloomFramebuffers.length = 0;
    for (let i=0; i<this.config.BLOOM_ITERATIONS; i++){
      const w = res.width >> (i+1), h = res.height >> (i+1);
      if (w < 2 || h < 2) break;
      this.bloomFramebuffers.push(this.createFBO(w,h, rgba.internalFormat, rgba.format, type, filtering));
    }
  }
  initSunraysFramebuffers(){
    const res = this.getResolution(this.config.SUNRAYS_RESOLUTION);
    const r = this.ext.formatR;
    const type = this.ext.halfFloatTexType;
    const filtering = this.ext.supportLinearFiltering ? this.gl.LINEAR : this.gl.NEAREST;
    this.sunrays     = this.createFBO(res.width, res.height, r.internalFormat, r.format, type, filtering);
    this.sunraysTemp = this.createFBO(res.width, res.height, r.internalFormat, r.format, type, filtering);
  }

  // ---------- Particles init/update/draw ----------
  initParticles(){
    const gl = this.gl;
    const rg = this.ext.formatRG;
    const type = this.ext.halfFloatTexType;
    const filtering = gl.NEAREST;

    const res = Math.max(2, Math.floor(this.config.PARTICLE_RES));
    this.particleRes = res;
    this.particleCount = res * res;

    this.particleState = this.createDoubleFBO(res, res, rg.internalFormat, rg.format, type, filtering);
    this.seedParticles();

    // aPosition: her parçacığa (texel UV)
    if (this.particleVBO) gl.deleteBuffer(this.particleVBO);
    const uv = new Float32Array(this.particleCount * 2);
    let id=0;
    for (let y=0; y<res; y++){
      for (let x=0; x<res; x++){
        uv[id++] = (x+0.5)/res; uv[id++] = (y+0.5)/res;
      }
    }
    this.particleVBO = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.particleVBO);
    gl.bufferData(gl.ARRAY_BUFFER, uv, gl.STATIC_DRAW);
  }
  seedParticles(){
    this.particleSeedProgram.bind();
    this.blit(this.particleState.write, true);
    this.particleState.swap();
  }
  resetParticles(){ this.seedParticles(); }
  
  // ---------- GridParticles ----------
  initGridParticles(){
    if (!this.config.GRID_ENABLED) return;
    
    const gl = this.gl;
    
    // Grid noktalarını oluştur
    const gridData = this.buildGridParticles();
    this.gridParticleCount = gridData.length / 4; // x,y,z,id
    
    // VBO oluştur
    if (this.gridParticleVBO) gl.deleteBuffer(this.gridParticleVBO);
    this.gridParticleVBO = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, this.gridParticleVBO);
    gl.bufferData(gl.ARRAY_BUFFER, gridData, gl.STATIC_DRAW);
    
    // VAO oluştur
    if (this.gridParticleVAO) gl.deleteVertexArray(this.gridParticleVAO);
    this.gridParticleVAO = gl.createVertexArray();
    gl.bindVertexArray(this.gridParticleVAO);
    
    // Attribute bağla
    gl.bindBuffer(gl.ARRAY_BUFFER, this.gridParticleVBO);
    gl.enableVertexAttribArray(0); // aPosition
    gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 16, 0); // stride 16, offset 0
    gl.enableVertexAttribArray(1); // aParticleId
    gl.vertexAttribPointer(1, 1, gl.FLOAT, false, 16, 12); // stride 16, offset 12
    
    gl.bindVertexArray(null);
    
    console.log('GridParticles initialized:', this.gridParticleCount, 'points');
  }
  
  buildGridParticles(){
    const total = this.config.GRID_TOTAL;
    const meridians = this.config.GRID_MERIDIANS;
    const parallels = this.config.GRID_PARALLELS;
    const weightM = this.config.GRID_WEIGHT_M;
    const weightP = this.config.GRID_WEIGHT_P;
    const polarCut = this.config.GRID_EXCLUDE_POLAR_DEG * Math.PI / 180;
    const radius = this.config.GRID_RADIUS;
    
    // Bütçeyi böl
    const P_m = Math.round(total * weightM);
    const P_p = total - P_m;
    
    // Line başına örnekleme
    const S_m = Math.max(8, Math.floor(P_m / meridians));
    const S_p = Math.max(8, Math.floor(P_p / parallels));
    
    const points = [];
    let particleId = 0;
    
    // Meridian çizgileri (sabit θ, φ boyunca örnekleme)
    for (let m = 0; m < meridians; m++) {
      const theta = m * 2 * Math.PI / meridians;
      const phiMin = 0.0;  // tam kutup
      const phiMax = Math.PI;  // tam kutup
      
      for (let s = 0; s < S_m; s++) {
        const phi = phiMin + (phiMax - phiMin) * s / (S_m - 1);
        
        // Küresel koordinatlardan Kartezyen'e
        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.cos(phi);
        const z = radius * Math.sin(phi) * Math.sin(theta);
        
        points.push(x, y, z, particleId++); // x,y,z,id
      }
    }
    
    // Parallel çizgileri (sabit φ, θ boyunca örnekleme, 0.5 faz offset)
    for (let p = 0; p < parallels; p++) {
      const phi = Math.PI * (p + 0.5) / parallels;  // tam küre kapsama
      
      for (let s = 0; s < S_p; s++) {
        const theta = ((s + 0.5) / S_p) * 2 * Math.PI; // 0.5 faz offset
        
        // Küresel koordinatlardan Kartezyen'e
        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.cos(phi);
        const z = radius * Math.sin(phi) * Math.sin(theta);
        
        points.push(x, y, z, particleId++); // x,y,z,id
      }
    }
    
    return new Float32Array(points);
  }
  updateParticles(dt){
    if (!this.config.PARTICLES_ENABLED) return;
    const gl = this.gl;
    this.particleUpdateProgram.bind();
    gl.uniform1i(this.particleUpdateProgram.uniforms.uPositions, this.particleState.read.attach(0));
    gl.uniform1i(this.particleUpdateProgram.uniforms.uVelocity,  this.velocity.read.attach(1));
    gl.uniform2f(this.particleUpdateProgram.uniforms.velTexelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1f(this.particleUpdateProgram.uniforms.dt, dt);
    gl.uniform1f(this.particleUpdateProgram.uniforms.advection, this.config.PARTICLE_ADVECTION);
    this.blit(this.particleState.write);
    this.particleState.swap();
  }
  drawParticles(target){
    if (!this.config.PARTICLES_ENABLED) return;
    const gl = this.gl;
    const w = (target==null) ? gl.drawingBufferWidth : target.width;
    const h = (target==null) ? gl.drawingBufferHeight : target.height;

    // Blend additive
    gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA, gl.ONE);

    this.particleDrawProgram.bind();

    // attrib 0 → aPosition
    gl.bindBuffer(gl.ARRAY_BUFFER, this.particleVBO);
    gl.vertexAttribPointer(0,2, gl.FLOAT, false, 0,0);
    gl.enableVertexAttribArray(0);
    this._quadBound = false;

    gl.uniform1i(this.particleDrawProgram.uniforms.uPositions, this.particleState.read.attach(0));
    gl.uniform1i(this.particleDrawProgram.uniforms.uDye,       this.dye.read.attach(1));
    gl.uniform1f(this.particleDrawProgram.uniforms.uPointSize, this.config.PARTICLE_SIZE * (window.devicePixelRatio || 1));
    gl.uniform1f(this.particleDrawProgram.uniforms.uAlpha, this.config.PARTICLE_ALPHA);
    gl.uniform1f(this.particleDrawProgram.uniforms.uBrightness, this.config.PARTICLE_BRIGHTNESS);
    gl.uniform1f(this.particleDrawProgram.uniforms.uFovH, this.config.CAMERA_FOV_H);
    gl.uniform1f(this.particleDrawProgram.uniforms.uFovV, this.config.CAMERA_FOV_V);
    gl.uniform1f(this.particleDrawProgram.uniforms.uAspect, w / h);
    gl.uniform1f(this.particleDrawProgram.uniforms.uYaw, this.config.CAMERA_YAW);
    gl.uniform1f(this.particleDrawProgram.uniforms.uPitch, this.config.CAMERA_PITCH);

    if (target == null) {
      gl.viewport(0,0, gl.drawingBufferWidth, gl.drawingBufferHeight);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    } else {
      gl.viewport(0,0, target.width, target.height);
      gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
    }

    gl.drawArrays(gl.POINTS, 0, this.particleCount);
    gl.disable(gl.BLEND);
  }
  
  drawGridParticles(target){
    if (!this.config.GRID_ENABLED || this.gridParticleCount === 0) return;
    
    const gl = this.gl;
    const w = (target==null) ? gl.drawingBufferWidth : target.width;
    const h = (target==null) ? gl.drawingBufferHeight : target.height;
    
    // Enable depth test for proper ordering
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    
    // Blend mode
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    
    this.gridParticleProgram.bind();
    
    // Bind VAO
    gl.bindVertexArray(this.gridParticleVAO);
    
    // Uniforms
    gl.uniform1f(this.gridParticleProgram.uniforms.uPointSize, this.config.GRID_POINT_SIZE_PX * (window.devicePixelRatio || 1));
    gl.uniform1f(this.gridParticleProgram.uniforms.uFovH, this.config.CAMERA_FOV_H);
    gl.uniform1f(this.gridParticleProgram.uniforms.uFovV, this.config.CAMERA_FOV_V);
    gl.uniform1f(this.gridParticleProgram.uniforms.uAspect, w / h);
    gl.uniform1f(this.gridParticleProgram.uniforms.uYaw, this.config.CAMERA_YAW);
    gl.uniform1f(this.gridParticleProgram.uniforms.uPitch, this.config.CAMERA_PITCH);
    gl.uniform1f(this.gridParticleProgram.uniforms.uRadius, this.config.GRID_RADIUS);
    gl.uniform1f(this.gridParticleProgram.uniforms.uTime, Date.now() * 0.001); // zaman uniform'u
    
    // Textures
    gl.uniform1i(this.gridParticleProgram.uniforms.uTexture, this.dye.read.attach(0));
    if (this.bloom && this.bloom.read) {
      gl.uniform1i(this.gridParticleProgram.uniforms.uBloom, this.bloom.read.attach(1));
    }
    if (this.sunrays && this.sunrays.read) {
      gl.uniform1i(this.gridParticleProgram.uniforms.uSunrays, this.sunrays.read.attach(2));
    }
    
    // Colors
    const iceColor = this.normalizeColor(this.config.GRID_COLOR_ICE);
    const whiteColor = this.normalizeColor(this.config.GRID_COLOR_WHITE);
    gl.uniform3f(this.gridParticleProgram.uniforms.uIce, iceColor.r, iceColor.g, iceColor.b);
    gl.uniform3f(this.gridParticleProgram.uniforms.uWhite, whiteColor.r, whiteColor.g, whiteColor.b);
    
    // Parameters
    gl.uniform1f(this.gridParticleProgram.uniforms.uIntensity, this.config.GRID_INTENSITY);
    gl.uniform1f(this.gridParticleProgram.uniforms.uAlpha, this.config.GRID_ALPHA);
    gl.uniform1f(this.gridParticleProgram.uniforms.uBloomFactor, this.config.GRID_BLOOM_FACTOR);
    gl.uniform1i(this.gridParticleProgram.uniforms.uEqHighlight, this.config.GRID_EQ_HIGHLIGHT ? 1 : 0);
    
    // Viewport
    if (target == null) {
      gl.viewport(0,0, gl.drawingBufferWidth, gl.drawingBufferHeight);
      gl.bindFramebuffer(gl.FRAMEBUFFER, null);
    } else {
      gl.viewport(0,0, target.width, target.height);
      gl.bindFramebuffer(gl.FRAMEBUFFER, target.fbo);
    }
    
    // Draw
    gl.drawArrays(gl.POINTS, 0, this.gridParticleCount);
    
    // Cleanup
    gl.disable(gl.BLEND);
    gl.disable(gl.DEPTH_TEST);
    gl.bindVertexArray(null);
  }

  // ---------- Main loop ----------
  update(){
    const dt = this.calcDeltaTime();
    if (this.resizeCanvas()) this.initFramebuffers();
    this.updateColors(dt);
    this.applyInputs();
    
    // Auto-rotate camera (48 saniyede bir tur, sağa doğru)
    if (this.config.CAMERA_AUTO_ROTATE) {
      const angularVelocity = (2 * Math.PI) / this.config.CAMERA_ROTATION_PERIOD; // rad/s
      this.config.CAMERA_YAW -= angularVelocity * dt;  // Negatif = sağa doğru dönüş
      
      // Wrap around 2π (performans için)
      if (this.config.CAMERA_YAW < -2 * Math.PI) {
        this.config.CAMERA_YAW += 2 * Math.PI;
      }
    }
    
    if (!this.config.PAUSED){
      this.step(dt);
      this.updateParticles(dt);
    }
    this.render(null);
    this.rafId = requestAnimationFrame(() => this.update());
  }
  
  // ---------- Resize handler ----------
  onResize() {
    // Canvas resize is handled in update() loop
    // This method exists for compatibility
  }
  calcDeltaTime(){
    const now = Date.now();
    let dt = (now - this.lastUpdateTime)/1000;
    dt = Math.min(dt, 0.016666);
    this.lastUpdateTime = now;
    return dt;
  }

  // ---------- Simulation step ----------
  step(dt){
    const gl = this.gl;
    gl.disable(gl.BLEND);

    this.curlProgram.bind();
    gl.uniform2f(this.curlProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1i(this.curlProgram.uniforms.uVelocity, this.velocity.read.attach(0));
    this.blit(this.curl);

    this.vorticityProgram.bind();
    gl.uniform2f(this.vorticityProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1i(this.vorticityProgram.uniforms.uVelocity, this.velocity.read.attach(0));
    gl.uniform1i(this.vorticityProgram.uniforms.uCurl, this.curl.attach(1));
    gl.uniform1f(this.vorticityProgram.uniforms.curl, this.config.CURL);
    gl.uniform1f(this.vorticityProgram.uniforms.dt, dt);
    this.blit(this.velocity.write); this.velocity.swap();

    this.divergenceProgram.bind();
    gl.uniform2f(this.divergenceProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1i(this.divergenceProgram.uniforms.uVelocity, this.velocity.read.attach(0));
    this.blit(this.divergence);

    this.clearProgram.bind();
    gl.uniform1i(this.clearProgram.uniforms.uTexture, this.pressure.read.attach(0));
    gl.uniform1f(this.clearProgram.uniforms.value, this.config.PRESSURE);
    this.blit(this.pressure.write); this.pressure.swap();

    this.pressureProgram.bind();
    gl.uniform2f(this.pressureProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1i(this.pressureProgram.uniforms.uDivergence, this.divergence.attach(0));
    for (let i=0; i<this.config.PRESSURE_ITERATIONS; i++){
      gl.uniform1i(this.pressureProgram.uniforms.uPressure, this.pressure.read.attach(1));
      this.blit(this.pressure.write); this.pressure.swap();
    }

    this.gradientSubtractProgram.bind();
    gl.uniform2f(this.gradientSubtractProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    gl.uniform1i(this.gradientSubtractProgram.uniforms.uPressure, this.pressure.read.attach(0));
    gl.uniform1i(this.gradientSubtractProgram.uniforms.uVelocity, this.velocity.read.attach(1));
    this.blit(this.velocity.write); this.velocity.swap();

    this.advectionProgram.bind();
    gl.uniform2f(this.advectionProgram.uniforms.texelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    if (!this.ext.supportLinearFiltering)
      gl.uniform2f(this.advectionProgram.uniforms.dyeTexelSize, this.velocity.texelSizeX, this.velocity.texelSizeY);
    const vId = this.velocity.read.attach(0);
    gl.uniform1i(this.advectionProgram.uniforms.uVelocity, vId);
    gl.uniform1i(this.advectionProgram.uniforms.uSource,   vId);
    gl.uniform1f(this.advectionProgram.uniforms.dt, dt);
    gl.uniform1f(this.advectionProgram.uniforms.dissipation, this.config.VELOCITY_DISSIPATION);
    this.blit(this.velocity.write); this.velocity.swap();

    if (!this.ext.supportLinearFiltering)
      gl.uniform2f(this.advectionProgram.uniforms.dyeTexelSize, this.dye.texelSizeX, this.dye.texelSizeY);
    gl.uniform1i(this.advectionProgram.uniforms.uVelocity, this.velocity.read.attach(0));
    gl.uniform1i(this.advectionProgram.uniforms.uSource,   this.dye.read.attach(1));
    gl.uniform1f(this.advectionProgram.uniforms.dissipation, this.config.DENSITY_DISSIPATION);
    this.blit(this.dye.write); this.dye.swap();
  }

  // ---------- Render ----------
  render(target){
    if (this.config.BLOOM) this.applyBloom(this.dye.read, this.bloom);
    if (this.config.SUNRAYS){
      this.applySunrays(this.dye.read, this.dye.write, this.sunrays);
      this.blur(this.sunrays, this.sunraysTemp, 1);
    }

    if (target == null || !this.config.TRANSPARENT) {
      this.gl.blendFunc(this.gl.ONE, this.gl.ONE_MINUS_SRC_ALPHA);
      this.gl.enable(this.gl.BLEND);
    } else {
      this.gl.disable(this.gl.BLEND);
    }

    if (!this.config.TRANSPARENT) this.drawColor(target, this.normalizeColor(this.config.BACK_COLOR));
    if (target == null && this.config.TRANSPARENT) this.drawCheckerboard(target);

    // Display (spherical)
    this.drawDisplay(target);

    // GridParticles (arkada, fluid'in altında)
    this.drawGridParticles(target);

    // Particles üstte
    this.drawParticles(target);
  }
  drawDisplay(target){
    const gl = this.gl;
    const w = (target==null) ? gl.drawingBufferWidth : target.width;
    const h = (target==null) ? gl.drawingBufferHeight : target.height;

    this.displayMaterial.bind();
    gl.uniform1i(this.displayMaterial.uniforms.uTexture, this.dye.read.attach(0));
    gl.uniform1f(this.displayMaterial.uniforms.uFovH, this.config.CAMERA_FOV_H);
    gl.uniform1f(this.displayMaterial.uniforms.uFovV, this.config.CAMERA_FOV_V);
    gl.uniform1f(this.displayMaterial.uniforms.uAspect, w / h);
    gl.uniform1f(this.displayMaterial.uniforms.uYaw, this.config.CAMERA_YAW);
    gl.uniform1f(this.displayMaterial.uniforms.uPitch, this.config.CAMERA_PITCH);
    gl.uniform2f(this.displayMaterial.uniforms.uDyeTexel, this.dye.texelSizeX, this.dye.texelSizeY);

    if (this.config.BLOOM) {
      gl.uniform1i(this.displayMaterial.uniforms.uBloom, this.bloom.attach(1));
      gl.uniform1i(this.displayMaterial.uniforms.uDithering, this.ditheringTexture.attach(2));
      const scale = this.getTextureScale(this.ditheringTexture, w, h);
      gl.uniform2f(this.displayMaterial.uniforms.ditherScale, scale.x, scale.y);
    }
    if (this.config.SUNRAYS) gl.uniform1i(this.displayMaterial.uniforms.uSunrays, this.sunrays.attach(3));

    // ColorWheel uniforms
    if (this.displayMaterial.uniforms.uColorLUT) {
      gl.uniform1i(this.displayMaterial.uniforms.uColorLUT, this.colorLUTTexture?.attach(4) || 0);
      gl.uniform1i(this.displayMaterial.uniforms.uColorWheelEnabled, this.colorWheelEnabled);
      gl.uniform1f(this.displayMaterial.uniforms.uMinFreq, this.colorMinFreq);
      gl.uniform1f(this.displayMaterial.uniforms.uMaxFreq, this.colorMaxFreq);
    }

    // GridParticles are now handled separately in drawGridParticles()

    this.blit(target);
  }
  applyBloom(source, destination){
    if (this.bloomFramebuffers.length < 2) return;

    const gl = this.gl;
    let last = destination;

    gl.disable(gl.BLEND);
    this.bloomPrefilterProgram.bind();
    const knee = this.config.BLOOM_THRESHOLD * this.config.BLOOM_SOFT_KNEE + 0.0001;
    gl.uniform3f(this.bloomPrefilterProgram.uniforms.curve,
      this.config.BLOOM_THRESHOLD - knee, knee * 2.0, 0.25 / knee);
    gl.uniform1f(this.bloomPrefilterProgram.uniforms.threshold, this.config.BLOOM_THRESHOLD);
    gl.uniform1i(this.bloomPrefilterProgram.uniforms.uTexture, source.attach(0));
    this.blit(last);

    this.bloomBlurProgram.bind();
    for (let i=0; i<this.bloomFramebuffers.length; i++){
      const dest = this.bloomFramebuffers[i];
      gl.uniform2f(this.bloomBlurProgram.uniforms.texelSize, last.texelSizeX, last.texelSizeY);
      gl.uniform1i(this.bloomBlurProgram.uniforms.uTexture, last.attach(0));
      this.blit(dest);
      last = dest;
    }

    gl.blendFunc(gl.ONE, gl.ONE);
    gl.enable(gl.BLEND);
    for (let i=this.bloomFramebuffers.length - 2; i>=0; i--){
      const baseTex = this.bloomFramebuffers[i];
      gl.uniform2f(this.bloomBlurProgram.uniforms.texelSize, last.texelSizeX, last.texelSizeY);
      gl.uniform1i(this.bloomBlurProgram.uniforms.uTexture, last.attach(0));
      gl.viewport(0,0, baseTex.width, baseTex.height);
      this.blit(baseTex);
      last = baseTex;
    }

    gl.disable(gl.BLEND);
    this.bloomFinalProgram.bind();
    gl.uniform2f(this.bloomFinalProgram.uniforms.texelSize, last.texelSizeX, last.texelSizeY);
    gl.uniform1i(this.bloomFinalProgram.uniforms.uTexture, last.attach(0));
    gl.uniform1f(this.bloomFinalProgram.uniforms.intensity, this.config.BLOOM_INTENSITY);
    this.blit(destination);
  }
  applySunrays(source, mask, destination){
    const gl = this.gl;
    gl.disable(gl.BLEND);
    this.sunraysMaskProgram.bind();
    gl.uniform1i(this.sunraysMaskProgram.uniforms.uTexture, source.attach(0));
    this.blit(mask);

    this.sunraysProgram.bind();
    gl.uniform1f(this.sunraysProgram.uniforms.weight, this.config.SUNRAYS_WEIGHT);
    gl.uniform1i(this.sunraysProgram.uniforms.uTexture, mask.attach(0));
    this.blit(destination);
  }
  blur(target, temp, iterations){
    const gl = this.gl;
    // basit 2-pass blur (yatay/dikey)
    const blurFrag = this.compileShader(gl.FRAGMENT_SHADER, `
      precision mediump float; precision mediump sampler2D;
      varying vec2 vUv; varying vec2 vL; varying vec2 vR;
      uniform sampler2D uTexture;
      void main(){
        vec4 sum = texture2D(uTexture, vUv) * 0.29411764;
        sum += texture2D(uTexture, vL) * 0.35294117;
        sum += texture2D(uTexture, vR) * 0.35294117;
        gl_FragColor = sum;
      }
    `);
    const blurProg = this.createProgramInstance(this.blurVertexShader, blurFrag);

    for (let i=0; i<iterations; i++){
      blurProg.bind();
      this.gl.uniform2f(blurProg.uniforms.texelSize, target.texelSizeX, 0.0);
      this.gl.uniform1i(blurProg.uniforms.uTexture, target.attach(0));
      this.blit(temp);
      this.gl.uniform2f(blurProg.uniforms.texelSize, 0.0, target.texelSizeY);
      this.gl.uniform1i(blurProg.uniforms.uTexture, temp.attach(0));
      this.blit(target);
    }
  }

  drawColor(target, color){
    this.colorProgram.bind();
    this.gl.uniform4f(this.colorProgram.uniforms.color, color.r, color.g, color.b, 1);
    this.blit(target);
  }
  drawCheckerboard(target){
    this.checkerboardProgram.bind();
    this.gl.uniform1f(this.checkerboardProgram.uniforms.aspectRatio, this.canvas.width / this.canvas.height);
    this.blit(target);
  }

  // ---------- Input (spherical mapping) ----------
  screenToSphereUV(pixelX, pixelY){
    // canvas pixel coords (0..canvas.width/height)
    const w = this.canvas.width, h = this.canvas.height;
    const ndcX = (pixelX / w) * 2 - 1;
    const ndcY = (pixelY / h) * 2 - 1;
    const tH = Math.tan(this.config.CAMERA_FOV_H * 0.5);
    const tV = Math.tan(this.config.CAMERA_FOV_V * 0.5);
    const aspect = w / h;
    // camera dir
    let x = ndcX * tH;
    let y = -ndcY * tV;
    let z = -1.0;
    // normalize
    const len = Math.hypot(x,y,z); x/=len; y/=len; z/=len;
    // apply yaw/pitch (cam -> world)
    const cy = Math.cos(this.config.CAMERA_YAW), sy = Math.sin(this.config.CAMERA_YAW);
    const cp = Math.cos(this.config.CAMERA_PITCH), sp = Math.sin(this.config.CAMERA_PITCH);
    // rotX(pitch) then rotY(yaw)
    let rx = x, ry = cp*y - sp*z, rz = sp*y + cp*z;
    let wx = cy*rx + sy*rz, wy = ry, wz = -sy*rx + cy*rz;
    // sphere UV
    const u = Math.atan2(wz, wx) / (2*Math.PI) + 0.5;
    const v = Math.acos(Math.max(-1, Math.min(1, wy))) / Math.PI;
    return { u, v };
  }

  attachEvents(){
    // ✅ GESTURE-ONLY MODE: Only synthetic mouse events from VisualController
    // Real mouse/touchpad interactions are filtered out in handlers
    const c = this.canvas;
    c.addEventListener('mousedown', this.handlers.mousedown);
    c.addEventListener('mousemove', this.handlers.mousemove);
    window.addEventListener('mouseup', this.handlers.mouseup);
    
    // ❌ Touch events disabled - touchpad triggers nothing
    // c.addEventListener('touchstart', this.handlers.touchstart, { passive:false });
    // c.addEventListener('touchmove',  this.handlers.touchmove,  { passive:false });
    // window.addEventListener('touchend', this.handlers.touchend);
    
    window.addEventListener('keydown',  this.handlers.keydown);
    window.addEventListener('resize',   this.handlers.resize);
  }
  detachEvents(){
    const c = this.canvas;
    c.removeEventListener('mousedown', this.handlers.mousedown);
    c.removeEventListener('mousemove', this.handlers.mousemove);
    window.removeEventListener('mouseup', this.handlers.mouseup);
    // c.removeEventListener('touchstart', this.handlers.touchstart);
    // c.removeEventListener('touchmove', this.handlers.touchmove);
    // window.removeEventListener('touchend', this.handlers.touchend);
    window.removeEventListener('keydown', this.handlers.keydown);
    window.removeEventListener('resize', this.handlers.resize);
  }

  handleMouseDown(e){
    // ✅ MOBILE MODE: Allow real mouse clicks (for Chrome DevTools testing)
    // ✅ DESKTOP GESTURE MODE: Accept ONLY synthetic events from VisualController
    const isMobileMode = this.config.ENABLE_MOBILE_MOUSE || 
                          window.location.search.includes('mobile=true') ||
                          window.innerWidth < 768;
    
    if (e.isTrusted && !isMobileMode) {
      // Real mouse click - IGNORE for visual trigger (desktop gesture-only mode)
      return;
    }
    
    const rect = this.canvas.getBoundingClientRect();
    const x = this.scaleByPixelRatio(e.clientX - rect.left);
    const y = this.scaleByPixelRatio(e.clientY - rect.top);
    let p = this.pointers.find(pp => pp.id === -1);
    if (!p) p = this.createPointer();
    this.updatePointerDownData(p, -1, x, y);
  }
  handleMouseMove(e){
    // ✅ MOBILE MODE: Allow real mouse move (for Chrome DevTools testing)
    // ✅ DESKTOP GESTURE MODE: Accept ONLY synthetic events from VisualController
    const isMobileMode = this.config.ENABLE_MOBILE_MOUSE || 
                          window.location.search.includes('mobile=true') ||
                          window.innerWidth < 768;
    
    if (e.isTrusted && !isMobileMode) {
      // Real mouse move - IGNORE for visual trigger (desktop gesture-only mode)
      return;
    }
    
    const p = this.pointers[0];
    if (!p.down) return;
    const rect = this.canvas.getBoundingClientRect();
    const x = this.scaleByPixelRatio(e.clientX - rect.left);
    const y = this.scaleByPixelRatio(e.clientY - rect.top);
    this.updatePointerMoveData(p, x, y);
  }
  handleMouseUp(e){ 
    // ✅ MOBILE MODE: Allow real mouse up (for Chrome DevTools testing)
    // ✅ DESKTOP GESTURE MODE: Accept ONLY synthetic events from VisualController
    const isMobileMode = this.config.ENABLE_MOBILE_MOUSE || 
                          window.location.search.includes('mobile=true') ||
                          window.innerWidth < 768;
    
    if (e && e.isTrusted && !isMobileMode) {
      // Real mouse up - IGNORE for visual trigger (desktop gesture-only mode)
      return;
    }
    
    this.updatePointerUpData(this.pointers[0]); 
  }

  handleTouchStart(e){
    e.preventDefault();
    const touches = e.targetTouches;
    while (touches.length >= this.pointers.length) this.pointers.push(this.createPointer());
    const rect = this.canvas.getBoundingClientRect();
    for (let i=0; i<touches.length; i++){
      const x = this.scaleByPixelRatio(touches[i].clientX - rect.left);
      const y = this.scaleByPixelRatio(touches[i].clientY - rect.top);
      this.updatePointerDownData(this.pointers[i+1], touches[i].identifier, x, y);
    }
  }
  handleTouchMove(e){
    e.preventDefault();
    const touches = e.targetTouches;
    const rect = this.canvas.getBoundingClientRect();
    for (let i=0; i<touches.length; i++){
      const p = this.pointers[i+1]; if (!p.down) continue;
      const x = this.scaleByPixelRatio(touches[i].clientX - rect.left);
      const y = this.scaleByPixelRatio(touches[i].clientY - rect.top);
      this.updatePointerMoveData(p, x, y);
    }
  }
  handleTouchEnd(e){
    const touches = e.changedTouches;
    for (let i=0; i<touches.length; i++){
      const p = this.pointers.find(pp => pp.id === touches[i].identifier);
      if (p) this.updatePointerUpData(p);
    }
  }
  handleKeyDown(e){
    if (e.code === 'KeyP') this.config.PAUSED = !this.config.PAUSED;
    if (e.key === ' ') this.splatStack.push(parseInt(Math.random()*20) + 5);
  }

  updatePointerDownData(pointer, id, pixelX, pixelY){
    pointer.id = id; pointer.down = true; pointer.moved = false;

    const { u, v } = this.screenToSphereUV(pixelX, pixelY);
    pointer.texcoordX = u; pointer.texcoordY = 1.0 - v;
    pointer.prevTexcoordX = pointer.texcoordX;
    pointer.prevTexcoordY = pointer.texcoordY;
    pointer.deltaX = 0; pointer.deltaY = 0;
    
    // INITIAL COLOR: Set starting color based on Y position
    if (this._colorLUTBytes && typeof this.sampleColorFromY01 === 'function') {
      pointer.color = this.sampleColorFromY01(pointer.texcoordY);
    } else {
      // Fallback to random color if LUT not available
      pointer.color = this.generateColor();
    }
  }
  updatePointerMoveData(pointer, pixelX, pixelY){
    pointer.prevTexcoordX = pointer.texcoordX;
    pointer.prevTexcoordY = pointer.texcoordY;

    const { u, v } = this.screenToSphereUV(pixelX, pixelY);
    pointer.texcoordX = u; pointer.texcoordY = 1.0 - v;

    pointer.deltaX = this.correctDeltaX(pointer.texcoordX - pointer.prevTexcoordX);
    pointer.deltaY = this.correctDeltaY(pointer.texcoordY - pointer.prevTexcoordY);
    pointer.moved = (Math.abs(pointer.deltaX) > 0 || Math.abs(pointer.deltaY) > 0);
    
    // REAL-TIME DYNAMIC COLOR: Update color based on current real-time color (60 FPS refresh)
    if (this.realTimeColorEnabled) {
      const prevY = pointer.prevTexcoordY;
      const currY = pointer.texcoordY;
      
      // Use real-time color for dynamic updates during interaction
      const realTimeColor = getCurrentColor();
      const prevColor = pointer.color;
      
      pointer.color = {
        r: realTimeColor.r,
        g: realTimeColor.g,
        b: realTimeColor.b
      };
      
      // ✅ Logging disabled by default (performance optimization)
    } else {
      console.warn("⚠️ realTimeColorEnabled is FALSE - colors won't update!");
    }
  }
  updatePointerUpData(pointer){ pointer.down = false; }

  correctDeltaX(delta){
    const aspect = this.canvas.width / this.canvas.height;
    if (aspect < 1) delta *= aspect;
    return delta;
  }
  correctDeltaY(delta){
    const aspect = this.canvas.width / this.canvas.height;
    if (aspect > 1) delta /= aspect;
    return delta;
  }

  applyInputs(){
    if (this.splatStack.length > 0) this.multipleSplats(this.splatStack.pop());
    this.pointers.forEach(p => {
      if (p.moved){ p.moved = false; this.splatPointer(p); }
    });
  }
  splatPointer(p){
    const dx = p.deltaX * this.config.SPLAT_FORCE;
    const dy = p.deltaY * this.config.SPLAT_FORCE;
    this.splat(p.texcoordX, p.texcoordY, dx, dy, p.color);
  }
  multipleSplats(amount){
    for (let i=0; i<amount; i++){
      // Use instrument color if provided (initial splats), otherwise generate color
      let color;
      if (this.instrumentColor) {
        color = { ...this.instrumentColor };
      } else {
        color = this.generateColor();
      }
      color.r *= 10; color.g *= 10; color.b *= 10;
      const x = Math.random(), y = Math.random();
      const dx = 1000 * (Math.random()-0.5), dy = 1000 * (Math.random()-0.5);
      this.splat(x,y, dx,dy, color);
    }
  }
  splat(x,y, dx,dy, color){
    // ✅ MAIN SPLAT
    // velocity
    this.splatProgram.bind();
    this.gl.uniform1i(this.splatProgram.uniforms.uTarget, this.velocity.read.attach(0));
    // ÖNEMLİ: aspect = dye aspect (canvas değil)
    this.gl.uniform1f(this.splatProgram.uniforms.aspectRatio, this.dye.width / this.dye.height);
    this.gl.uniform2f(this.splatProgram.uniforms.point, x, y);
    this.gl.uniform3f(this.splatProgram.uniforms.color, dx, dy, 0.0);
    this.gl.uniform1f(this.splatProgram.uniforms.radius, this.correctRadius(this.config.SPLAT_RADIUS / 100.0));
    this.blit(this.velocity.write); this.velocity.swap();

    // dye
    this.gl.uniform1i(this.splatProgram.uniforms.uTarget, this.dye.read.attach(0));
    this.gl.uniform3f(this.splatProgram.uniforms.color, color.r, color.g, color.b);
    this.blit(this.dye.write); this.dye.swap();
    
    // ✅ EXTRA PARTICLE BURST (zengin görüntü için)
    // Her splat için 3-5 ekstra küçük splat oluştur
    const burstCount = 3 + Math.floor(Math.random() * 3); // 3-5 arası
    const baseRadius = this.config.SPLAT_RADIUS / 100.0;
    
    for (let i = 0; i < burstCount; i++) {
      // Rastgele offset (ana splat etrafında)
      const angle = Math.random() * Math.PI * 2;
      const distance = (0.01 + Math.random() * 0.03) * baseRadius; // Radius'a göre ölçekli
      const offsetX = Math.cos(angle) * distance;
      const offsetY = Math.sin(angle) * distance;
      
      // Küçük velocity (ana velocity'nin %30-60'ı)
      const velocityScale = 0.3 + Math.random() * 0.3;
      const burstDx = dx * velocityScale;
      const burstDy = dy * velocityScale;
      
      // Daha küçük radius (%20-40 boyut)
      const burstRadius = baseRadius * (0.2 + Math.random() * 0.2);
      
      // velocity burst
      this.gl.uniform2f(this.splatProgram.uniforms.point, x + offsetX, y + offsetY);
      this.gl.uniform3f(this.splatProgram.uniforms.color, burstDx, burstDy, 0.0);
      this.gl.uniform1f(this.splatProgram.uniforms.radius, this.correctRadius(burstRadius));
      this.gl.uniform1i(this.splatProgram.uniforms.uTarget, this.velocity.read.attach(0));
      this.blit(this.velocity.write); this.velocity.swap();
      
      // dye burst (hafif renk varyasyonu)
      const colorVariation = 0.9 + Math.random() * 0.2; // %90-110 parlaklık
      this.gl.uniform3f(this.splatProgram.uniforms.color, 
        color.r * colorVariation, 
        color.g * colorVariation, 
        color.b * colorVariation);
      this.gl.uniform1i(this.splatProgram.uniforms.uTarget, this.dye.read.attach(0));
      this.blit(this.dye.write); this.dye.swap();
    }
  }
  correctRadius(r){
    const aspect = this.dye.width / this.dye.height;
    if (aspect > 1.0) r *= aspect;
    return r;
  }

  // ---------- Misc ----------
  resizeCanvas(){
    const w = this.scaleByPixelRatio(this.canvas.clientWidth);
    const h = this.scaleByPixelRatio(this.canvas.clientHeight);
    if (this.canvas.width !== w || this.canvas.height !== h){
      this.canvas.width = w; this.canvas.height = h;
      return true;
    }
    return false;
  }
  scaleByPixelRatio(x){
    const pr = (typeof window!=='undefined') ? (window.devicePixelRatio||1) : 1;
    return Math.floor(x*pr);
  }
  getResolution(res){
    let aspect = this.gl.drawingBufferWidth / this.gl.drawingBufferHeight;
    if (aspect < 1) aspect = 1.0/aspect;
    const min = Math.round(res), max = Math.round(res*aspect);
    if (this.gl.drawingBufferWidth > this.gl.drawingBufferHeight)
      return { width:max, height:min };
    else
      return { width:min, height:max };
  }
  getTextureScale(texture, w,h){ return { x: w/texture.width, y: h/texture.height }; }
  updateColors(dt){
    if (!this.config.COLORFUL) return;
    this.colorUpdateTimer += dt * this.config.COLOR_UPDATE_SPEED;
    if (this.colorUpdateTimer >= 1){
      this.colorUpdateTimer = this.wrap(this.colorUpdateTimer, 0,1);
      this.pointers.forEach(p => p.color = this.generateColor());
    }
  }
  wrap(v,min,max){ const range = max-min; if (range===0) return min; return (v-min)%range + min; }
  generateColor(){
    // REAL-TIME CENTRALIZED: Use current real-time color
    const colorData = getCurrentColor();
    
    // Update current color tracking
    this.currentColor = colorData;
    this.currentFrequency = colorData.frequency;
    
    // ✅ Logging disabled by default (performance optimization)
    
    return {
      r: colorData.r,
      g: colorData.g, 
      b: colorData.b
    };
  }
  HSVtoRGB(h,s,v){
    let r,g,b,i=Math.floor(h*6), f=h*6-i, p=v*(1-s), q=v*(1-f*s), t=v*(1-(1-f)*s);
    switch(i%6){ case 0: r=v; g=t; b=p; break; case 1: r=q; g=v; b=p; break; case 2: r=p; g=v; b=t; break;
      case 3: r=p; g=q; b=v; break; case 4: r=t; g=p; b=v; break; case 5: r=v; g=p; b=q; break; }
    return { r,g,b };
  }
  normalizeColor(input){ return { r: input.r/255, g: input.g/255, b: input.b/255 }; }

  // ---------- Instrument-Specific Presets ----------
  /**
   * Create instrument-specific fluid behavior presets
   * Each instrument has unique physics characteristics
   */
  _createInstrumentPresets() {
    return {
      // Morpheus: Atmospheric, dreamy, slow-moving
      // Character: Warm, ethereal, persistent trails
      morpheus: {
        VELOCITY_DISSIPATION: 0.1,      // Slow decay (long, dreamy trails)
        DENSITY_DISSIPATION: 0.5,        // Persistent color (atmospheric)
        CURL: 15,                        // Low vorticity (smooth, flowing)
        PRESSURE: 0.6,                   // Low pressure (gentle movement)
        PRESSURE_ITERATIONS: 15,         // Fewer iterations (softer)
        SPLAT_RADIUS: 0.3,               // Larger initial splats
        SPLAT_FORCE: 4000,               // Gentler force
        PARTICLE_ADVECTION: 0.8,         // Slow particle movement
        PARTICLE_SIZE: 2.5,              // Larger particles (atmospheric)
        PARTICLE_ALPHA: 0.85,            // More visible particles
        BLOOM_INTENSITY: 0.02,           // Strong bloom (ethereal glow)
        BLOOM_THRESHOLD: 2.5,            // Lower threshold (more bloom)
        SUNRAYS_WEIGHT: 0.9,              // Strong sunrays (dreamy)
        GRID_INTENSITY: 20.0,            // More visible grid (atmospheric)
        GRID_ALPHA: 0.9,                 // Stronger grid
        CAMERA_ROTATION_PERIOD: 60.0,    // Slower rotation (dreamy)
        SHADING: true,                   // Soft shading
        COLORFUL: true                   // Colorful mode
      },
      
      // Neo: Sharp, dynamic, energetic
      // Character: Cool, geometric, fast-moving
      neo: {
        VELOCITY_DISSIPATION: 0.3,       // Fast decay (sharp, defined trails)
        DENSITY_DISSIPATION: 1.5,        // Quick color fade (dynamic)
        CURL: 50,                        // High vorticity (turbulent, energetic)
        PRESSURE: 1.0,                   // High pressure (dynamic movement)
        PRESSURE_ITERATIONS: 25,         // More iterations (sharper)
        SPLAT_RADIUS: 0.2,               // Smaller, focused splats
        SPLAT_FORCE: 8000,               // Stronger force (energetic)
        PARTICLE_ADVECTION: 1.2,         // Fast particle movement
        PARTICLE_SIZE: 1.5,              // Smaller particles (sharp)
        PARTICLE_ALPHA: 0.7,              // Less visible (subtle)
        BLOOM_INTENSITY: 0.005,          // Subtle bloom (sharp edges)
        BLOOM_THRESHOLD: 3.5,            // Higher threshold (less bloom)
        SUNRAYS_WEIGHT: 0.5,             // Moderate sunrays (focused)
        GRID_INTENSITY: 10.0,            // Less visible grid (clean)
        GRID_ALPHA: 0.6,                 // Subtle grid
        CAMERA_ROTATION_PERIOD: 30.0,     // Faster rotation (dynamic)
        SHADING: true,                   // Sharp shading
        COLORFUL: true                   // Colorful mode
      },
      
      // Piano: Balanced, classical, elegant
      // Character: Neutral, refined, musical
      piano: {
        VELOCITY_DISSIPATION: 0.2,       // Balanced decay
        DENSITY_DISSIPATION: 1.0,        // Standard color fade
        CURL: 30,                        // Moderate vorticity (balanced)
        PRESSURE: 0.8,                   // Standard pressure
        PRESSURE_ITERATIONS: 20,         // Standard iterations
        SPLAT_RADIUS: 0.25,              // Standard splat size
        SPLAT_FORCE: 6000,               // Standard force
        PARTICLE_ADVECTION: 1.0,          // Standard particle movement
        PARTICLE_SIZE: 2.0,              // Standard particle size
        PARTICLE_ALPHA: 0.75,            // Standard alpha
        BLOOM_INTENSITY: 0.01,           // Balanced bloom
        BLOOM_THRESHOLD: 3.0,            // Standard threshold
        SUNRAYS_WEIGHT: 0.75,            // Standard sunrays
        GRID_INTENSITY: 15.0,            // Standard grid
        GRID_ALPHA: 1.0,                 // Full grid visibility
        CAMERA_ROTATION_PERIOD: 48.0,     // Standard rotation
        SHADING: true,                   // Standard shading
        COLORFUL: false                  // Less colorful (classical)
      }
    };
  }

  /**
   * Apply instrument-specific preset
   * @param {string} instrumentName - 'morpheus' | 'neo' | 'piano'
   */
  applyInstrumentPreset(instrumentName) {
    const preset = this.instrumentPresets[instrumentName];
    if (!preset) {
      console.warn(`⚠️ Unknown instrument preset: ${instrumentName}`);
      return;
    }

    // Apply preset values
    Object.assign(this.config, preset);
    
    // Update shader keywords (SHADING, BLOOM, SUNRAYS, COLORFUL)
    this.updateKeywords();
    
    // Update current instrument
    this.currentInstrument = instrumentName;
    
    console.log(`✅ Applied ${instrumentName} preset:`, {
      velocityDissipation: this.config.VELOCITY_DISSIPATION,
      curl: this.config.CURL,
      bloomIntensity: this.config.BLOOM_INTENSITY,
      sunraysWeight: this.config.SUNRAYS_WEIGHT
    });
  }

  // ---------- Start/Stop/Cleanup (React uyum) ----------
  start(){ if (!this.rafId) this.update(); }
  stop(){ if (this.rafId){ cancelAnimationFrame(this.rafId); this.rafId=null; } }
  cleanup(){
    try{
      this.stop();
      this.detachEvents();

      if (this.gui && typeof this.gui.destroy === 'function') {
        try { this.gui.destroy(); } catch (_) {}
        this.gui = null;
      }
      if (window.__PAVEL_FLUID_GUI === this.gui) {
        window.__PAVEL_FLUID_GUI = null;
      }
      const host = document.getElementById('pavel-gui-host');
      if (host && host.childElementCount === 0) {
        host.remove();
      }

      const gl = this.gl;
      if (this._quadVBO) gl.deleteBuffer(this._quadVBO);
      if (this._quadEBO) gl.deleteBuffer(this._quadEBO);
      if (this.particleVBO) gl.deleteBuffer(this.particleVBO);
      if (this.particleState){
        gl.deleteFramebuffer(this.particleState.read.fbo);
        gl.deleteTexture(this.particleState.read.texture);
        gl.deleteFramebuffer(this.particleState.write.fbo);
        gl.deleteTexture(this.particleState.write.texture);
      }
    } catch(_) {}
    
    // Real-time Color System cleanup
    stopRealTimeColorUpdates();
    // ✅ Logging disabled by default (performance optimization)
  }

  // REMOVED: Old ColorWheel methods replaced by centralized system
  // All color functionality now handled by freqToColor.js

} // end class
