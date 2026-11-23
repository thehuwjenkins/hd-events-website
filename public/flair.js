/* HD Events signature motion for the home page:
   - the particle sculpture that flows into the HD Events sound wave (over the hero photo)
   - the scroll aurora that paints light down the page
   Both adapted from the original app.js. The sound ribbons between sections come from ribbons.js.
   Respects "reduce motion" and the Pause motion button. */
(() => {
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let paused = reduce;
  const smooth = x => { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); };
  const mix = (a, b, t) => a + (b - a) * t;
  const TAU = Math.PI * 2;

  /* ---------- Hero particle sculpture (transparent, over the photo) ---------- */
  const canvas = document.getElementById('heroWave');
  const hero = document.querySelector('.hire-hero');
  const ctx = canvas.getContext('2d');
  let w, h, dpr, time = 0, elapsed = 0, heroVisible = true;
  const pointer = { x: 0, y: 0 }, target = { x: 0, y: 0 };
  const mobile = innerWidth < 800;
  const COUNT = mobile ? 9000 : 22000;
  const points = Array.from({ length: COUNT }, (_, i) => ({
    u: ((i % 320) + Math.random() * .8) / 320 * TAU,
    v: (Math.floor(i / 320) + Math.random() * .8) / Math.ceil(COUNT / 320) * TAU,
    r: Math.random(), s: Math.random(),
  }));
  const colors = Array.from({ length: 12 }, (_, i) => { const p = i / 11; return `rgb(${Math.round(10 + 155 * p)},${Math.round(235 - 173 * p)},${Math.round(231 + 24 * p)})`; });

  function resize() {
    w = canvas.clientWidth; h = canvas.clientHeight;
    dpr = Math.min(devicePixelRatio || 1, 1.6);
    canvas.width = Math.floor(w * dpr); canvas.height = Math.floor(h * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  resize(); addEventListener('resize', resize);
  hero.addEventListener('pointermove', e => { target.x = (e.clientX / w - .5) * 2; target.y = (e.clientY / h - .5) * 2; });
  hero.addEventListener('pointerleave', () => { target.x = target.y = 0; });

  function draw() {
    pointer.x += (target.x - pointer.x) * .04; pointer.y += (target.y - pointer.y) * .04;
    ctx.clearRect(0, 0, w, h);
    // Torus, then orbital ribbons, then liquid folds, settling into the flowing HD Events sound wave.
    const t = reduce ? 16 : Math.min(elapsed, 16);
    const saturn = smooth((t - 3) / 1.1) * (1 - smooth((t - 8) / 1.2));
    const vortex = smooth((t - 8) / 1.2) * (1 - smooth((t - 13) / 1.2));
    const wave = smooth((t - 13) / 1.3);
    const scale = Math.min(w * (mobile ? .55 : .30), h * .42);
    const cx = w * (mobile ? .55 : .70), cy = h * (mobile ? .40 : .46);
    const rot = time * .74 + pointer.x * .3, tilt = .45 + Math.sin(time * .57) * .65 + pointer.y * .2;
    const buckets = Array.from({ length: 36 }, () => []);
    for (let i = 0; i < points.length; i++) {
      const p = points[i], u = p.u, v = p.v;
      const major = .64 + .11 * Math.sin(u * 3 + time * 1.15) + .04 * Math.cos(v + time), minor = .20 + .075 * Math.cos(u * 3 - time * 1.3 + v * .5);
      let x = (major + minor * Math.cos(v)) * Math.cos(u), y = (major + minor * Math.cos(v)) * Math.sin(u), z = minor * Math.sin(v);
      const radius = .62 + (v / TAU) * .48 + .035 * Math.sin(u * 3 + time * 1.3), angle = u + time * 1.65;
      x = mix(x, radius * Math.cos(angle), saturn); y = mix(y, .045 * Math.sin(v * 3 + u * 2 + time), saturn); z = mix(z, radius * Math.sin(angle), saturn);
      const fluidAngle = u + .28 * Math.sin(v + time * .8), fluidRadius = .72 + .20 * Math.cos(v + u * 2 - time);
      x = mix(x, fluidRadius * Math.cos(fluidAngle), vortex); y = mix(y, .30 * Math.sin(u * 2 + time * 1.1) + .18 * Math.sin(v + u), vortex); z = mix(z, .57 * Math.sin(fluidAngle) + .23 * Math.cos(v + u * 2 + time), vortex);
      let yy = y * Math.cos(tilt) - z * Math.sin(tilt); z = y * Math.sin(tilt) + z * Math.cos(tilt); y = yy;
      let xx = x * Math.cos(rot) + z * Math.sin(rot); z = -x * Math.sin(rot) + z * Math.cos(rot); x = xx;
      const wx = (u / TAU - .5) * 3.2, wy = Math.sin(u * 1.6 - time * 1.25 + v * .15) * .3 + Math.cos(v) * .13, wz = Math.sin(v) * .25 + Math.sin(u * 2 - time * .6) * .2;
      x = mix(x, wx, wave); y = mix(y, wy, wave); z = mix(z, wz, wave);
      const perspective = 3 / (3 - z);
      const px = cx + x * scale * perspective, py = cy + y * scale * perspective;
      const depth = Math.max(0, Math.min(2, Math.floor((z + .6) * 2)));
      const col = Math.round(((Math.sin(u + v * .22 + time * .4) + 1) / 2) * 11);
      buckets[depth * 12 + col].push(px, py, (mobile ? .38 : .40) + perspective * .22 + p.r * .23);
    }
    for (let d = 0; d < 3; d++) for (let c = 0; c < 12; c++) {
      const b = buckets[d * 12 + c]; if (!b.length) continue;
      ctx.fillStyle = colors[c]; ctx.globalAlpha = Math.min(1, .78 + d * .1);
      ctx.beginPath();
      for (let k = 0; k < b.length; k += 3) { const size = b[k + 2] * 1.8; ctx.rect(b[k], b[k + 1], size, size); }
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }
  new IntersectionObserver(es => heroVisible = es[0].isIntersecting, { threshold: 0 }).observe(hero);

  /* ---------- Scroll aurora (from the original app.js) ---------- */
  const aurora = document.getElementById('aurora'), ac = aurora.getContext('2d');
  let aw, ah, previousScroll = scrollY, auroraPhase = 0, hasScrolled = false, headPage = scrollY + innerHeight * .48, stretch = 0, scrollEnergy = .4, direction = 1, trailClock = 0;
  const smoke = [];
  function sizeAurora() { aw = innerWidth; ah = innerHeight; aurora.width = Math.round(aw * .6); aurora.height = Math.round(ah * .6); ac.setTransform(.6, 0, 0, .6, 0, 0); }
  sizeAurora(); addEventListener('resize', sizeAurora);
  function paintRibbon(base, phase, extension, opacity, smoky = false) {
    if (opacity < .002 || base + Math.abs(extension) < -ah || base - Math.abs(extension) > ah * 2) return;
    for (let strand = 0; strand < (smoky ? 6 : 14); strand++) {
      const n = smoky ? 6 : 14, spread = (strand / n - .5) * (smoky ? ah * .12 : ah * .055);
      const gradient = ac.createLinearGradient(0, base - ah * .3, aw, base + ah * .4);
      gradient.addColorStop(0, 'rgba(0,240,170,0)'); gradient.addColorStop(.22, `rgba(0,235,163,${opacity * .060})`);
      gradient.addColorStop(.5, `rgba(0,201,232,${opacity * .085})`); gradient.addColorStop(.79, `rgba(145,51,248,${opacity * .085})`);
      gradient.addColorStop(1, 'rgba(123,30,246,0)');
      ac.strokeStyle = gradient; ac.lineWidth = smoky ? ah * .085 : 12 + strand * 1.8; ac.beginPath();
      for (let k = 0; k <= 64; k++) {
        const x = k / 64 * aw, curve = Math.sin(k / 64 * 5 + phase);
        const y = base + curve * ah * .18 + Math.sin(k / 64 * 9 - phase * .6) * ah * .055 + spread + extension * Math.pow((curve + 1) * .5, 1.5);
        if (k === 0) ac.moveTo(x, y); else ac.lineTo(x, y);
      }
      ac.stroke();
    }
  }
  function drawAurora(dt = .033) {
    const delta = scrollY - previousScroll; previousScroll = scrollY; const moving = Math.abs(delta) > .15;
    ac.clearRect(0, 0, aw, ah); ac.globalCompositeOperation = 'lighter';
    if (moving) {
      hasScrolled = true; direction = Math.sign(delta); auroraPhase += delta * .002;
      headPage = scrollY + ah * (direction > 0 ? .60 : .36);
      stretch = mix(stretch, direction * Math.min(ah * .65, Math.abs(delta) * 8), .35);
      scrollEnergy = Math.min(1, scrollEnergy + Math.abs(delta) * .02); trailClock += dt;
      if (trailClock > .045) { smoke.push({ page: headPage, phase: auroraPhase, stretch, age: 0, strength: scrollEnergy }); trailClock = 0; if (smoke.length > 28) smoke.shift(); }
    } else { scrollEnergy *= Math.exp(-dt * 1.8); if (!hasScrolled) { auroraPhase += dt * .10; scrollEnergy = .45; } }
    for (let i = smoke.length - 1; i >= 0; i--) {
      const puff = smoke[i]; puff.age += dt; if (puff.age > 2.8) { smoke.splice(i, 1); continue; }
      paintRibbon(puff.page - scrollY, puff.phase, puff.stretch, Math.pow(1 - puff.age / 2.8, 2) * puff.strength * .60, true);
    }
    paintRibbon(headPage - scrollY, auroraPhase, stretch, hasScrolled ? scrollEnergy : .55);
    if (!hasScrolled) paintRibbon(ah * .82, auroraPhase + 2.1, -ah * .2, .25);
    ac.globalCompositeOperation = 'source-over';
  }

  /* ---------- One clock for both ---------- */
  let last = 0, lastPaint = 0;
  function frame(now) {
    if (!last) last = now;
    const delta = Math.min((now - last) / 1000, .1);
    if (!paused) {
      time += delta; elapsed += delta;
      if (now - lastPaint > 30) { if (heroVisible) draw(); drawAurora(Math.min(.1, (now - lastPaint) / 1000)); lastPaint = now; }
    }
    last = now; requestAnimationFrame(frame);
  }
  draw(); drawAurora(); requestAnimationFrame(frame);
  addEventListener('scroll', () => { if (paused) drawAurora(); }, { passive: true });

  /* ---------- Pause motion ---------- */
  const toggle = document.getElementById('motion');
  function setMotion() {
    toggle.setAttribute('aria-pressed', String(paused));
    toggle.innerHTML = paused ? '▶ <span>PLAY MOTION</span>' : 'Ⅱ <span>PAUSE MOTION</span>';
    toggle.setAttribute('aria-label', paused ? 'Play animation' : 'Pause animation');
    document.body.classList.toggle('paused', paused);
  }
  setMotion();
  toggle.addEventListener('click', () => { paused = !paused; setMotion(); if (paused) draw(); });
})();
