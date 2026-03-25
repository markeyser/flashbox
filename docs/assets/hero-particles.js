/*
  WebGL spiral animation for Flashbox hero.
  Inspired by the Zensical Three.js attractor but self-contained,
  using raw WebGL to avoid a 400 KB Three.js dependency.
*/
(function () {
  "use strict";

  const canvas = document.getElementById("fb-canvas");
  if (!canvas) return;

  /* ── Try WebGL first, fall back to 2D canvas ── */
  const gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

  if (!gl) {
    run2D(canvas);
    return;
  }

  /* ────────────────────────────────────────────────
     WebGL spiral attractor (Clifford-style)
     Uses point sprites drawn each frame.
  ──────────────────────────────────────────────── */

  const VS = `
    attribute vec2 a_pos;
    uniform   vec2 u_res;
    uniform   float u_size;
    void main(){
      vec2 p = (a_pos / u_res) * 2.0 - 1.0;
      p.y = -p.y;
      gl_Position  = vec4(p, 0.0, 1.0);
      gl_PointSize = u_size;
    }
  `;
  const FS = `
    precision mediump float;
    uniform vec4 u_color;
    void main(){
      float d = distance(gl_PointCoord, vec2(0.5));
      if(d > 0.5) discard;
      gl_FragColor = u_color * (1.0 - d * 1.8);
    }
  `;

  function makeShader(type, src) {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    return s;
  }

  const prog = gl.createProgram();
  gl.attachShader(prog, makeShader(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, makeShader(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  gl.useProgram(prog);

  const aPos   = gl.getAttribLocation(prog, "a_pos");
  const uRes   = gl.getUniformLocation(prog, "u_res");
  const uSize  = gl.getUniformLocation(prog, "u_size");
  const uColor = gl.getUniformLocation(prog, "u_color");

  const N = 18000; // number of points per arm
  const ARMS = 3;
  const TOTAL = N * ARMS;

  const buf = gl.createBuffer();
  const data = new Float32Array(TOTAL * 2);

  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, data, gl.DYNAMIC_DRAW);
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);

  let W, H, frame = 0;

  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    gl.viewport(0, 0, W, H);
  }
  resize();
  window.addEventListener("resize", resize);

  /* Clifford attractor parameters */
  const CONFIGS = [
    { a: -1.7,  b: 1.8,  c: -1.9, d: -0.4 },
    { a: -1.4,  b: 1.6,  c:  1.0, d:  0.7 },
    { a:  1.5,  b: -1.8, c:  1.6, d:  0.9 },
  ];

  function draw() {
    frame++;
    const t = frame * 0.0012;
    gl.clearColor(0.027, 0.031, 0.059, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    for (let arm = 0; arm < ARMS; arm++) {
      const cfg = CONFIGS[arm];

      /* slowly rotate config values for motion */
      const a = cfg.a + Math.sin(t * 0.3 + arm) * 0.12;
      const b = cfg.b + Math.cos(t * 0.2 + arm) * 0.12;
      const c = cfg.c + Math.sin(t * 0.25 + arm * 1.3) * 0.12;
      const d = cfg.d + Math.cos(t * 0.35 + arm * 0.7) * 0.12;

      let x = 0, y = 0;
      const cx = W * 0.5, cy = H * 0.5;
      const scale = Math.min(W, H) * 0.22;
      const offset = arm * N * 2;

      for (let i = 0; i < N; i++) {
        const nx = Math.sin(a * y) + c * Math.cos(a * x);
        const ny = Math.sin(b * x) + d * Math.cos(b * y);
        x = nx; y = ny;
        data[offset + i * 2]     = cx + x * scale;
        data[offset + i * 2 + 1] = cy + y * scale;
      }

      gl.bindBuffer(gl.ARRAY_BUFFER, buf);
      gl.bufferSubData(gl.ARRAY_BUFFER, offset * 4, data.subarray(offset, offset + N * 2));
      gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, offset * 4);

      /* arm colour: cyan → blue → indigo */
      const hue = arm / ARMS;
      const r = 0.0  + hue * 0.22;
      const g = 0.78 - hue * 0.35;
      const bl = 1.0;
      gl.uniform4f(uColor, r, g, bl, 0.55);
      gl.uniform1f(uSize, 1.4);
      gl.uniform2f(uRes, W, H);
      gl.drawArrays(gl.POINTS, 0, N);
    }

    requestAnimationFrame(draw);
  }

  draw();

  /* ── Fallback 2-D canvas (non-WebGL) ── */
  function run2D(cv) {
    const ctx = cv.getContext("2d");
    let W2, H2, f2 = 0;

    function resize2() {
      W2 = cv.width = cv.offsetWidth;
      H2 = cv.height = cv.offsetHeight;
    }
    resize2();
    window.addEventListener("resize", resize2);

    const PTS = 300;
    const pts = Array.from({ length: PTS }, (_, i) => ({
      t: i / PTS,
      a: (Math.PI * 2 * i) / PTS,
    }));

    function draw2() {
      f2++;
      ctx.clearRect(0, 0, W2, H2);
      const cx = W2 / 2, cy = H2 / 2, R = Math.min(W2, H2) * 0.4;
      pts.forEach((p) => {
        const t2 = (p.t + f2 * 0.001) % 1;
        const angle = p.a + t2 * Math.PI * 6 + f2 * 0.002;
        const r = t2 * R;
        const x = cx + Math.cos(angle) * r;
        const y = cy + Math.sin(angle) * r;
        ctx.beginPath();
        ctx.arc(x, y, 1.5, 0, Math.PI * 2);
        ctx.fillStyle = `hsla(${190 + t2 * 60}, 90%, 70%, ${t2 * 0.8})`;
        ctx.fill();
      });
      requestAnimationFrame(draw2);
    }
    draw2();
  }
})();
