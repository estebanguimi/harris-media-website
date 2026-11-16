/* BATCH 1 effects: waving flag, star fill, network graph, topo readout, scope, draggable windows,
   trophy ring, confetti, poster rays, pamphlet unfold, army crowd. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function onView(el, fn, th) {
    if (!("IntersectionObserver" in window)) return fn();
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { io.disconnect(); fn(); } }); }, { threshold: th || 0.3 });
    io.observe(el);
  }
  function fitCanvas(cv, scale) { var d = Math.min(window.devicePixelRatio || 1, 2) * (scale || 1); cv.width = cv.clientWidth * d; cv.height = cv.clientHeight * d; var x = cv.getContext("2d"); x.setTransform(d, 0, 0, d, 0, 0); return x; }
  function visibleLoop(el, draw) {
    var on = true, raf;
    function f(t) { draw(t); if (on && !reduce) raf = requestAnimationFrame(f); }
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { var v = es[0].isIntersecting; if (v && !on) { on = true; raf = requestAnimationFrame(f); } on = v; }).observe(el);
    raf = requestAnimationFrame(f);
  }

  /* ---------- waving flag ---------- */
  document.querySelectorAll("canvas[data-flag]").forEach(function (cv) {
    var cols = cv.getAttribute("data-flag").split(","), ctx = fitCanvas(cv), wind = .6, tw = .6;
    addEventListener("resize", function () { ctx = fitCanvas(cv); });
    cv.parentElement.addEventListener("pointermove", function (e) { tw = .3 + e.clientX / innerWidth * 1.6; });
    visibleLoop(cv, function (t) {
      var W = cv.clientWidth, H = cv.clientHeight, stripes = 13, sh = H * .9 / stripes, x0 = W * .04;
      wind += (tw - wind) * .03; ctx.clearRect(0, 0, W, H);
      for (var s = 0; s < stripes; s++) {
        ctx.beginPath();
        for (var x = 0; x <= W; x += 16) {
          var y = H * .05 + s * sh + Math.sin(x * .006 - t * .0016 * wind + s * .15) * 26 * wind * (x / W) + Math.sin(x * .013 - t * .002) * 8;
          if (x === 0) ctx.moveTo(x0 + x, y); else ctx.lineTo(x0 + x, y);
        }
        for (x = W; x >= 0; x -= 16) {
          var y2 = H * .05 + (s + 1) * sh + Math.sin(x * .006 - t * .0016 * wind + (s + 1) * .15) * 26 * wind * (x / W) + Math.sin(x * .013 - t * .002) * 8;
          ctx.lineTo(x0 + x, y2);
        }
        ctx.closePath(); ctx.globalAlpha = s % 2 ? .1 : .36; ctx.fillStyle = s % 2 ? cols[1] : cols[0]; ctx.fill();
      }
      ctx.globalAlpha = .55; ctx.fillStyle = cols[1];
      for (var r = 0; r < 9; r++) for (var c = 0; c < (r % 2 ? 5 : 6); c++) {
        var sx = x0 + 30 + c * 44 + (r % 2 ? 22 : 0), sy = H * .08 + r * 32 + Math.sin(sx * .006 - t * .0016 * wind) * 10 * wind * (sx / W);
        ctx.beginPath(); ctx.arc(sx, sy, 2.4, 0, 6.3); ctx.fill();
      }
      ctx.globalAlpha = 1;
    });
  });
  document.querySelectorAll("[data-starfill]").forEach(function (g) {
    var stars = g.querySelectorAll("i");
    function upd() { var r = g.getBoundingClientRect(), p = clamp((innerHeight * .9 - r.top) / (r.height + innerHeight * .4), 0, 1), n = Math.round(p * stars.length); stars.forEach(function (s, k) { s.classList.toggle("on", k < n); }); }
    addEventListener("scroll", upd, { passive: true }); upd();
  });

  /* ---------- network graph ---------- */
  document.querySelectorAll("canvas[data-net]").forEach(function (cv) {
    var cols = cv.getAttribute("data-net").split(","), ctx = fitCanvas(cv), nodes = [], packets = [], m = { x: -999, y: -999 };
    function build() {
      ctx = fitCanvas(cv); var W = cv.clientWidth, H = cv.clientHeight; nodes = [];
      var N = W < 820 ? 130 : 320;
      for (var k = 0; k < N; k++) { var a = Math.random() * 6.28, r = (.08 + Math.pow(Math.random(), .7) * .55) * Math.min(W, H) * .95; nodes.push({ x: W * .66 + Math.cos(a) * r * 1.3, y: H * .42 + Math.sin(a) * r * .75, vx: 0, vy: 0, c: k % 2 ? cols[0] : cols[1], s: 1.5 + Math.random() * 2 }); }
    }
    build(); addEventListener("resize", build);
    cv.parentElement.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); m.x = e.clientX - r.left; m.y = e.clientY - r.top; });
    visibleLoop(cv, function (t) {
      var W = cv.clientWidth, H = cv.clientHeight, hx = W * .66, hy = H * .42; ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = .6;
      nodes.forEach(function (n, k) {
        var dx = n.x - m.x, dy = n.y - m.y, d2 = dx * dx + dy * dy;
        if (d2 < 14000) { n.vx += dx / 900; n.vy += dy / 900; }
        n.vx *= .9; n.vy *= .9; n.x += n.vx + Math.sin(t * .0008 + k) * .15; n.y += n.vy + Math.cos(t * .0007 + k) * .15;
        if (k % 2 === 0) { ctx.strokeStyle = n.c; ctx.globalAlpha = .22; ctx.beginPath(); ctx.moveTo(n.x, n.y); ctx.lineTo(hx, hy); ctx.stroke(); }
        ctx.globalAlpha = .9; ctx.fillStyle = n.c; ctx.beginPath(); ctx.arc(n.x, n.y, n.s, 0, 6.3); ctx.fill();
      });
      if (Math.random() < .5) { var src = nodes[Math.floor(Math.random() * nodes.length)]; packets.push({ n: src, p: 0 }); }
      packets = packets.filter(function (pk) {
        pk.p += .018; var x = pk.n.x + (hx - pk.n.x) * pk.p, y = pk.n.y + (hy - pk.n.y) * pk.p;
        ctx.globalAlpha = 1; ctx.fillStyle = pk.n.c; ctx.beginPath(); ctx.arc(x, y, 2.2, 0, 6.3); ctx.fill(); return pk.p < 1;
      });
      var pulse = 18 + Math.sin(t * .004) * 4;
      ctx.globalAlpha = .25; ctx.fillStyle = cols[2]; ctx.beginPath(); ctx.arc(hx, hy, pulse * 2.2, 0, 6.3); ctx.fill();
      ctx.globalAlpha = 1; ctx.beginPath(); ctx.arc(hx, hy, pulse, 0, 6.3); ctx.fill();
      ctx.fillStyle = "#030915"; ctx.font = "700 13px ui-monospace, monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("AI", hx, hy);
    });
  });

  /* ---------- topo cursor readout ---------- */
  document.querySelectorAll("[data-topo]").forEach(function (h) {
    var rd = h.querySelector(".tp-read");
    h.addEventListener("pointermove", function (e) {
      var r = h.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
      var lat = (43.9 - y / r.height * 1.4).toFixed(4), lon = (72.4 - x / r.width * 1.6).toFixed(4);
      rd.textContent = lat + "° N · " + lon + "° W"; rd.style.transform = "translate(" + (x + 18) + "px," + (y + 18) + "px)";
    });
    h.addEventListener("pointerleave", function () { rd.style.transform = "translate(-300px,-300px)"; });
  });

  /* ---------- scope ---------- */
  document.querySelectorAll("[data-scope]").forEach(function (h) {
    var view = h.querySelector(".scp-view"), rng = h.querySelector(".scp-rng"), words = [], x = innerWidth * .7, y = innerHeight * .45, tx = x, ty = y, active = false, t0 = performance.now();
    setTimeout(function () { words = Array.prototype.slice.call(h.querySelectorAll(".scp-copy h1 .sw")); }, 100);
    var img = new Image(); var src = getComputedStyle(h).getPropertyValue("--img").replace(/^url\(['"]?|['"]?\)$/g, "").trim(); img.src = src;
    h.addEventListener("pointermove", function (e) { var r = h.getBoundingClientRect(); active = true; tx = e.clientX - r.left; ty = e.clientY - r.top; });
    h.addEventListener("pointerleave", function () { active = false; t0 = performance.now(); });
    (function loop(now) {
      var W = h.clientWidth, H = h.clientHeight;
      if (!active && !reduce) { var a = (now - t0) / 2400; tx = W * (.6 + Math.cos(a) * .22); ty = H * (.42 + Math.sin(a * 1.4) * .14); }
      x += (tx - x) * .12; y += (ty - y) * .12;
      h.style.setProperty("--rx", x + "px"); h.style.setProperty("--ry", y + "px");
      if (view.classList.contains("vec")) {
        var z = 1.9; view.style.setProperty("--mw", W + "px"); view.style.setProperty("--mh", H + "px"); view.style.setProperty("--z", z);
        view.style.setProperty("--tx", (150 - x * z) + "px"); view.style.setProperty("--ty", (150 - y * z) + "px");
      } else {
      var iw = img.naturalWidth || 16, ihh = img.naturalHeight || 9, s = Math.max(W / iw, H / ihh), bw0 = iw * s, bh0 = ihh * s, ox = (W - bw0) / 2, oy = (H - bh0) / 2, zoom = 1.8;
      view.style.setProperty("--bw", (bw0 * zoom) + "px");
      view.style.setProperty("--bx", (150 - (x - ox) * zoom) + "px"); view.style.setProperty("--by", (150 - (y - oy) * zoom) + "px");
      }
      if (rng) rng.textContent = "RNG " + String(Math.round(400 + y)).padStart(4, "0") + " · " + String(Math.round(x)).padStart(4, "0");
      words.forEach(function (w) { var r = w.getBoundingClientRect(), hr = h.getBoundingClientRect(); var cx = x + hr.left, cy = y + hr.top; w.classList.toggle("locked", cx > r.left - 30 && cx < r.right + 30 && cy > r.top - 30 && cy < r.bottom + 30); });
      if (!reduce) requestAnimationFrame(loop);
    })(performance.now());
  });

  /* ---------- plaque shine ---------- */
  document.querySelectorAll(".pq").forEach(function (p) {
    p.addEventListener("pointermove", function (e) { var r = p.getBoundingClientRect(); p.style.setProperty("--shine", (((e.clientX - r.left) / r.width) * 120 - 60) + "%"); });
  });

  /* ---------- draggable windows ---------- */
  var z = 10;
  document.querySelectorAll("[data-drag]").forEach(function (w) {
    var bar = w.querySelector(".os-bar"), sx, sy, ox, oy, drag = false;
    w.addEventListener("pointerdown", function () { w.style.zIndex = ++z; });
    bar.addEventListener("pointerdown", function (e) {
      if (window.innerWidth < 900) return;
      drag = true; sx = e.clientX; sy = e.clientY; ox = w.offsetLeft; oy = w.offsetTop; bar.setPointerCapture(e.pointerId);
    });
    bar.addEventListener("pointermove", function (e) { if (!drag) return; w.style.left = (ox + e.clientX - sx) + "px"; w.style.top = (oy + e.clientY - sy) + "px"; });
    bar.addEventListener("pointerup", function () { drag = false; });
  });

  /* ---------- trophy ring ---------- */
  document.querySelectorAll("[data-ring]").forEach(function (st) {
    var spin = 0, speed = .25, tilt = 14, tt = 14;
    st.parentElement.parentElement.addEventListener("pointermove", function (e) { speed = .1 + e.clientX / innerWidth * .8; tt = 4 + e.clientY / innerHeight * 24; });
    (function loop() { spin += speed; tilt += (tt - tilt) * .05; st.style.setProperty("--spin", spin + "deg"); st.style.setProperty("--tilt", tilt + "deg"); if (!reduce) requestAnimationFrame(loop); })();
  });

  /* ---------- confetti ---------- */
  document.querySelectorAll("canvas[data-confetti]").forEach(function (cv) {
    var cols = cv.getAttribute("data-confetti").split(","), ctx = fitCanvas(cv), bits = [], running = false;
    function burst() {
      ctx = fitCanvas(cv); var W = cv.clientWidth, H = cv.clientHeight;
      for (var k = 0; k < 220; k++) bits.push({ x: W / 2, y: H * .55, vx: (Math.random() - .5) * 18, vy: -Math.random() * 18 - 6, r: Math.random() * 6.3, vr: (Math.random() - .5) * .4, w: 6 + Math.random() * 8, h: 4 + Math.random() * 6, c: cols[k % cols.length] });
      if (!running && !reduce) { running = true; requestAnimationFrame(step); }
    }
    function step() {
      var W = cv.clientWidth, H = cv.clientHeight; ctx.clearRect(0, 0, W, H);
      bits = bits.filter(function (b) { b.vy += .45; b.vx *= .99; b.x += b.vx; b.y += b.vy; b.r += b.vr; ctx.save(); ctx.translate(b.x, b.y); ctx.rotate(b.r); ctx.fillStyle = b.c; ctx.fillRect(-b.w / 2, -b.h / 2, b.w, b.h); ctx.restore(); return b.y < H + 40; });
      if (bits.length) requestAnimationFrame(step); else running = false;
    }
    var btn = cv.parentElement.querySelector("[data-burst]"); if (btn) btn.addEventListener("click", burst);
    onView(cv.parentElement, burst, .5);
  });

  /* ---------- poster rays follow pointer ---------- */
  document.querySelectorAll("[data-rays]").forEach(function (h) {
    var rays = h.querySelector(".ps-rays");
    h.addEventListener("pointermove", function (e) { var r = h.getBoundingClientRect(); rays.style.setProperty("--cx", (55 + (e.clientX - r.left) / r.width * 25) + "%"); rays.style.setProperty("--cy", (40 + (e.clientY - r.top) / r.height * 20) + "%"); });
  });
  document.querySelectorAll("[data-unfold]").forEach(function (p) { onView(p, function () { p.classList.add("open"); }, .25); });

  /* ---------- army crowd ---------- */
  document.querySelectorAll("canvas[data-army]").forEach(function (cv) {
    var cols = cv.getAttribute("data-army").split(","), ctx = fitCanvas(cv), dots = [], total = 0, m = { x: -999, y: -999 }, counter = document.querySelector("[data-armycount]");
    function build() {
      ctx = fitCanvas(cv); var W = cv.clientWidth, H = cv.clientHeight, gap = W < 820 ? 14 : 16; dots = [];
      for (var y = 150; y < H - 20; y += gap) for (var x = W * .35; x < W - 10; x += gap) dots.push({ x: x + (Math.random() - .5) * 6, y: y + (Math.random() - .5) * 6, born: Math.random() * 7000 * (1 - (x - W * .35) / (W * .65)) + Math.random() * 1500, c: cols[Math.random() < .15 ? 1 : (Math.random() < .5 ? 0 : 2)] });
      total = dots.length;
    }
    build(); addEventListener("resize", build);
    cv.parentElement.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); m.x = e.clientX - r.left; m.y = e.clientY - r.top; });
    var start = performance.now();
    visibleLoop(cv, function (t) {
      var W = cv.clientWidth, H = cv.clientHeight, el = reduce ? 99999 : t - start, alive = 0; ctx.clearRect(0, 0, W, H);
      dots.forEach(function (d) {
        if (el < d.born) return; alive++;
        var a = Math.min(1, (el - d.born) / 400), dx = d.x - m.x, dy = d.y - m.y, dist = Math.sqrt(dx * dx + dy * dy), lift = dist < 110 ? (110 - dist) / 110 : 0;
        ctx.globalAlpha = a * (.35 + lift * .65); ctx.fillStyle = lift > .2 ? cols[1] : d.c;
        ctx.beginPath(); ctx.arc(d.x, d.y - lift * 10, 2.2 + lift * 2.5, 0, 6.3); ctx.fill();
        ctx.beginPath(); ctx.arc(d.x, d.y - lift * 10 - 5 - lift * 3, 1.6 + lift * 1.4, 0, 6.3); ctx.fill();
      });
      ctx.globalAlpha = 1;
      if (counter) counter.textContent = String(alive).padStart(4, "0");
    });
  });
})();
