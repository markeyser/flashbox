(function () {
  "use strict";

  const canvas = document.getElementById("fb-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");

  let W, H, cx, cy, frame = 0;
  const ARMS = 6;
  const PARTICLES_PER_ARM = 180;
  const MAX_R = 0.42; // fraction of min(W,H)

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    cx = W / 2;
    cy = H / 2;
  }
  resize();
  window.addEventListener("resize", resize);

  // Build particle pool once
  const particles = [];
  for (let arm = 0; arm < ARMS; arm++) {
    for (let i = 0; i < PARTICLES_PER_ARM; i++) {
      const t = i / PARTICLES_PER_ARM; // 0..1 along arm
      particles.push({
        arm,
        t,
        speed: 0.00018 + Math.random() * 0.00012,
        size: 0.6 + Math.random() * 1.4,
        opacity: 0.35 + Math.random() * 0.65,
        phase: Math.random() * Math.PI * 2,
      });
    }
  }

  function draw() {
    frame++;
    ctx.clearRect(0, 0, W, H);

    // Subtle radial background glow
    const grd = ctx.createRadialGradient(cx, cy, 0, cx, cy, Math.min(W, H) * 0.5);
    grd.addColorStop(0, "rgba(0,200,255,0.06)");
    grd.addColorStop(1, "rgba(0,0,0,0)");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, W, H);

    const R = Math.min(W, H) * MAX_R;
    const time = frame * 0.001;

    particles.forEach((p) => {
      // Animate t forward, wrap at 1
      p.t = (p.t + p.speed) % 1;

      const armAngle = (p.arm / ARMS) * Math.PI * 2;
      const spiral = p.t * Math.PI * 7; // total wind of each arm
      const angle = armAngle + spiral + time * 0.12;
      const r = p.t * R;

      const x = cx + Math.cos(angle) * r;
      const y = cy + Math.sin(angle) * r;

      // Colour: cyan → indigo based on arm + t
      const hue = 185 + p.arm * 25 + p.t * 40;
      const alpha = p.opacity * (0.4 + 0.6 * p.t); // fade in from centre

      ctx.beginPath();
      ctx.arc(x, y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = `hsla(${hue}, 100%, 72%, ${alpha})`;
      ctx.fill();

      // Tiny trailing line for the outer particles
      if (p.t > 0.55) {
        const prevAngle = angle - 0.08;
        const prevR = r - 3;
        ctx.beginPath();
        ctx.moveTo(cx + Math.cos(prevAngle) * prevR, cy + Math.sin(prevAngle) * prevR);
        ctx.lineTo(x, y);
        ctx.strokeStyle = `hsla(${hue}, 100%, 72%, ${alpha * 0.3})`;
        ctx.lineWidth = p.size * 0.5;
        ctx.stroke();
      }
    });

    requestAnimationFrame(draw);
  }

  draw();
})();
