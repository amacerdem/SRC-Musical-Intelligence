/**
 * gl.js — WebGL2 context, shader compilation, fullscreen quad, FBO management.
 * S³ Musical Intelligence Demo
 */
export class GLContext {
    constructor(canvas) {
        this.canvas = canvas;
        this.gl = canvas.getContext('webgl2', {
            antialias: false,
            alpha: false,
            premultipliedAlpha: false,
            preserveDrawingBuffer: false,
        });
        if (!this.gl) throw new Error('WebGL2 not supported');

        this._setupQuad();
        this._programs = new Map();
        this._fbos = [null, null]; // For transitions
        this._fboTextures = [null, null];
        this._fboSize = [0, 0];
    }

    // ─── Fullscreen Quad ─────────────────────────────
    _setupQuad() {
        const gl = this.gl;
        const verts = new Float32Array([-1,-1, 1,-1, -1,1, -1,1, 1,-1, 1,1]);
        this.vao = gl.createVertexArray();
        gl.bindVertexArray(this.vao);
        const vbo = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
        gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(0);
        gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
        gl.bindVertexArray(null);
    }

    // ─── Shader Compilation ──────────────────────────
    compileShader(type, src) {
        const gl = this.gl;
        const s = gl.createShader(type);
        gl.shaderSource(s, src);
        gl.compileShader(s);
        if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
            const log = gl.getShaderInfoLog(s);
            console.error('Shader compile error:\n' + log);
            const lines = src.split('\n');
            for (let i = 0; i < lines.length; i++) {
                console.log((i+1) + ': ' + lines[i]);
            }
            gl.deleteShader(s);
            return null;
        }
        return s;
    }

    createProgram(vsrc, fsrc, name) {
        const gl = this.gl;
        const vs = this.compileShader(gl.VERTEX_SHADER, vsrc);
        const fs = this.compileShader(gl.FRAGMENT_SHADER, fsrc);
        if (!vs || !fs) return null;

        const p = gl.createProgram();
        gl.attachShader(p, vs);
        gl.attachShader(p, fs);
        gl.bindAttribLocation(p, 0, 'a_pos');
        gl.linkProgram(p);

        if (!gl.getProgramParameter(p, gl.LINK_STATUS)) {
            console.error('Program link error:', gl.getProgramInfoLog(p));
            return null;
        }

        // Cache uniform locations
        const uniforms = {};
        const n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
        for (let i = 0; i < n; i++) {
            const info = gl.getActiveUniform(p, i);
            // Handle arrays: u_mel[0] → u_mel
            const baseName = info.name.replace(/\[0\]$/, '');
            uniforms[baseName] = gl.getUniformLocation(p, info.name);
            // For arrays, also cache individual element locations
            if (info.size > 1) {
                for (let j = 0; j < info.size; j++) {
                    uniforms[baseName + '[' + j + ']'] = gl.getUniformLocation(p, baseName + '[' + j + ']');
                }
            }
        }

        const prog = { program: p, uniforms, name };
        if (name) this._programs.set(name, prog);
        return prog;
    }

    getProgram(name) {
        return this._programs.get(name) || null;
    }

    // ─── Uniform Helpers ─────────────────────────────
    setFloat(prog, name, value) {
        const loc = prog.uniforms[name];
        if (loc != null) this.gl.uniform1f(loc, value);
    }

    setVec2(prog, name, x, y) {
        const loc = prog.uniforms[name];
        if (loc != null) this.gl.uniform2f(loc, x, y);
    }

    setFloatArray(prog, name, arr) {
        const loc = prog.uniforms[name];
        if (loc != null) this.gl.uniform1fv(loc, arr);
    }

    // ─── FBO for Transitions ─────────────────────────
    _ensureFBOs(w, h) {
        if (this._fboSize[0] === w && this._fboSize[1] === h) return;
        const gl = this.gl;

        for (let i = 0; i < 2; i++) {
            if (this._fbos[i]) gl.deleteFramebuffer(this._fbos[i]);
            if (this._fboTextures[i]) gl.deleteTexture(this._fboTextures[i]);

            const tex = gl.createTexture();
            gl.bindTexture(gl.TEXTURE_2D, tex);
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, w, h, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
            gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);

            const fbo = gl.createFramebuffer();
            gl.bindFramebuffer(gl.FRAMEBUFFER, fbo);
            gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);

            this._fbos[i] = fbo;
            this._fboTextures[i] = tex;
        }
        gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        this._fboSize = [w, h];
    }

    renderToFBO(index) {
        const gl = this.gl;
        this._ensureFBOs(this.canvas.width, this.canvas.height);
        gl.bindFramebuffer(gl.FRAMEBUFFER, this._fbos[index]);
        gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    }

    renderToScreen() {
        const gl = this.gl;
        gl.bindFramebuffer(gl.FRAMEBUFFER, null);
        gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    }

    getFBOTexture(index) {
        return this._fboTextures[index];
    }

    // ─── Draw ────────────────────────────────────────
    drawQuad(prog) {
        const gl = this.gl;
        gl.useProgram(prog.program);
        gl.bindVertexArray(this.vao);
        gl.drawArrays(gl.TRIANGLES, 0, 6);
    }

    // ─── Resize ──────────────────────────────────────
    resize() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        const w = Math.floor(this.canvas.clientWidth * dpr);
        const h = Math.floor(this.canvas.clientHeight * dpr);
        if (this.canvas.width !== w || this.canvas.height !== h) {
            this.canvas.width = w;
            this.canvas.height = h;
            this.gl.viewport(0, 0, w, h);
        }
        return [w, h];
    }
}
