/* HMG client versions — intro curtain, split text, parallax, pinned horizontal scroll,
   particle typography, magnetic buttons, custom cursor, scroll-scrubbed drawing. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var root = document.documentElement;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function progressOf(el) { var r = el.getBoundingClientRect(); return clamp((window.innerHeight - r.top) / (window.innerHeight + r.height), 0, 1); }

  /* ---------- intro curtain (first view of each page) ---------- */
  var cur = document.querySelector(".v-curtain");
  if (cur) {
    if (reduce) cur.remove();
    else {
      document.body.classList.add("is-intro");
      window.addEventListener("load", function () { setTimeout(function () { cur.classList.add("go"); document.body.classList.remove("is-intro"); document.body.classList.add("is-ready"); }, 450); });
      setTimeout(function () { cur.classList.add("go"); document.body.classList.add("is-ready"); }, 2600);
      cur.addEventListener("animationend", function (e) { if (e.animationName === "curtainUp") cur.remove(); });
    }
  } else document.body.classList.add("is-ready");

  /* ---------- split text into characters (keeps words and nested tags) ---------- */
  document.querySelectorAll("[data-split]").forEach(function (el) {
    var i = 0;
    (function walk(node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (n) {
        if (n.nodeType === 3) {
          var frag = document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) { frag.appendChild(document.createTextNode(" ")); return; }
            var ws = document.createElement("span"); ws.className = "sw";
            w.split("").forEach(function (ch) { var s = document.createElement("span"); s.className = "sc"; s.style.setProperty("--ci", i++); s.textContent = ch; ws.appendChild(s); });
            frag.appendChild(ws);
          });
          n.parentNode.replaceChild(frag, n);
        } else if (n.nodeType === 1 && n.tagName !== "BR") walk(n);
      });
    })(el);
    el.classList.add("is-split");
  });

  /* ---------- pointer parallax inside heroes ---------- */
  var fxRoot = document.querySelector("[data-fx]");
  if (!reduce && fine && (!fxRoot || fxRoot.hasAttribute("data-par"))) {
    document.querySelectorAll(".w-hero, .v2-hero, .v3-hero").forEach(function (hero) {
      var layers = hero.querySelectorAll("[data-depth], .bigstar, .radar, .sun, .phone, .gauge, .clap, .flagstar, .lh, .ast, .monitor, .term, .portrait, .aurora, .floor, .pipes, .topo, .stars, .mount");
      if (!layers.length) return;
      var tx = 0, ty = 0, x = 0, y = 0, raf = null;
      function loop() {
        x += (tx - x) * 0.08; y += (ty - y) * 0.08;
        layers.forEach(function (l) { var d = parseFloat(l.getAttribute("data-depth") || 18); l.style.translate = (x * d).toFixed(2) + "px " + (y * d).toFixed(2) + "px"; });
        raf = Math.abs(tx - x) + Math.abs(ty - y) > 0.001 ? requestAnimationFrame(loop) : null;
      }
      hero.addEventListener("pointermove", function (e) { var r = hero.getBoundingClientRect(); tx = (e.clientX - r.left) / r.width - 0.5; ty = (e.clientY - r.top) / r.height - 0.5; if (!raf) raf = requestAnimationFrame(loop); });
      hero.addEventListener("pointerleave", function () { tx = 0; ty = 0; if (!raf) raf = requestAnimationFrame(loop); });
    });
  }

  /* ---------- scroll-driven effects ---------- */
  var hs = Array.prototype.slice.call(document.querySelectorAll(".v2-hs"));
  var scrubs = Array.prototype.slice.call(document.querySelectorAll("[data-scrub]"));
  var fills = Array.prototype.slice.call(document.querySelectorAll("[data-fill]"));
  var skews = Array.prototype.slice.call(document.querySelectorAll("[data-skew]"));
  var heroes = Array.prototype.slice.call(document.querySelectorAll(".v2-hero, .v3-hero"));
  function sizeHs() {
    hs.forEach(function (s) {
      var track = s.querySelector(".v2-hs-track");
      if (window.innerWidth < 820 || reduce) { s.style.height = ""; track.style.transform = ""; s.classList.add("is-static"); return; }
      s.classList.remove("is-static");
      s.style.height = (track.scrollWidth - window.innerWidth + window.innerHeight) + "px";
    });
    scrubs.forEach(function (p) { var L = p.getTotalLength ? p.getTotalLength() : 1000; p.style.strokeDasharray = L; p.dataset.len = L; });
  }
  var lastY = window.scrollY, vel = 0, ticking = false;
  function frame() {
    ticking = false;
    hs.forEach(function (s) {
      if (s.classList.contains("is-static")) return;
      var track = s.querySelector(".v2-hs-track"), r = s.getBoundingClientRect();
      var max = s.offsetHeight - window.innerHeight, p = clamp(-r.top / (max || 1), 0, 1);
      track.style.transform = "translate3d(" + (-p * (track.scrollWidth - window.innerWidth)) + "px,0,0)";
      var bar = s.querySelector(".v2-hs-bar i"); if (bar) bar.style.transform = "scaleX(" + p + ")";
    });
    scrubs.forEach(function (p) {
      var host = p.closest("[data-scrub-host]") || p.parentNode;
      var r = host.getBoundingClientRect();
      var prog = clamp((window.innerHeight * 0.75 - r.top) / (r.height), 0, 1);
      p.style.strokeDashoffset = (1 - prog) * parseFloat(p.dataset.len || 1000);
      host.querySelectorAll("[data-node]").forEach(function (n) { n.classList.toggle("on", prog >= parseFloat(n.getAttribute("data-node"))); });
    });
    fills.forEach(function (f) { f.style.setProperty("--p", (clamp((progressOf(f) - 0.15) / 0.5, 0, 1) * 100).toFixed(1) + "%"); });
    var y = window.scrollY; vel = vel * 0.85 + (y - lastY) * 0.15; lastY = y;
    skews.forEach(function (s) { s.style.transform = "skewX(" + clamp(-vel * 0.35, -12, 12).toFixed(2) + "deg)"; });
    heroes.forEach(function (h) { var p = clamp(window.scrollY / window.innerHeight, 0, 1); h.style.setProperty("--hp", p.toFixed(3)); });
    if (Math.abs(vel) > 0.1) requestTick();
  }
  function requestTick() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }
  window.addEventListener("scroll", requestTick, { passive: true });
  window.addEventListener("resize", function () { sizeHs(); requestTick(); });
  window.addEventListener("load", function () { sizeHs(); requestTick(); });
  sizeHs(); requestTick();

  /* ---------- compact version switcher appears after the hero ---------- */
  var vmini = document.querySelector(".vmini");
  if (vmini) { var vm = function () { vmini.classList.toggle("show", window.scrollY > window.innerHeight * 0.8); }; window.addEventListener("scroll", vm, { passive: true }); vm(); }

  /* ---------- magnetic buttons ---------- */
  if (fine && !reduce) {
    document.querySelectorAll("[data-magnet]").forEach(function (b) {
      b.addEventListener("pointermove", function (e) { var r = b.getBoundingClientRect(); b.style.translate = ((e.clientX - r.left - r.width / 2) * 0.25).toFixed(1) + "px " + ((e.clientY - r.top - r.height / 2) * 0.35).toFixed(1) + "px"; });
      b.addEventListener("pointerleave", function () { b.style.translate = "0 0"; });
    });
  }

  /* ---------- custom cursor (v3) ---------- */
  var cursor = document.querySelector(".v-cursor");
  if (cursor && fine && !reduce) {
    var cx = innerWidth / 2, cy = innerHeight / 2, px = cx, py = cy;
    document.addEventListener("pointermove", function (e) { cx = e.clientX; cy = e.clientY; cursor.classList.add("on"); });
    document.addEventListener("pointerleave", function () { cursor.classList.remove("on"); });
    document.querySelectorAll("a, button, [data-tilt]").forEach(function (a) {
      a.addEventListener("pointerenter", function () { cursor.classList.add("big"); });
      a.addEventListener("pointerleave", function () { cursor.classList.remove("big"); });
    });
    (function loop() { px += (cx - px) * 0.2; py += (cy - py) * 0.2; cursor.style.transform = "translate3d(" + px + "px," + py + "px,0)"; requestAnimationFrame(loop); })();
  } else if (cursor) cursor.remove();

  /* ---------- particle typography (v3 hero) ---------- */
  document.querySelectorAll("canvas[data-word]").forEach(function (cv) {
    var mode = cv.getAttribute("data-mode") || "dots", inBlock = cv.classList.contains("sx-pt-c"), GL = "01#%&*+=<>/HMG", ctx = cv.getContext("2d"), word = cv.getAttribute("data-word"), cols = (cv.getAttribute("data-colors") || "#ffffff").split(","), font = cv.getAttribute("data-font") || "900 200px sans-serif";
    var dpr = Math.min(window.devicePixelRatio || 1, 2), W, H, parts = [], mouse = { x: -9999, y: -9999 }, running = true;
    function build() {
      W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var off = document.createElement("canvas"), o = off.getContext("2d"); off.width = W; off.height = H;
      var size = inBlock ? Math.min(W * 0.86 / (word.length * 0.62), H * 0.78) : Math.min(W * 0.84 / (word.length * 0.6), H * (W < 820 ? 0.8 : 0.42));
      o.fillStyle = "#fff"; o.textAlign = "center"; o.textBaseline = "middle"; o.font = font.replace(/\d+px/, Math.round(size) + "px");
      o.fillText(word, W * 0.5, inBlock ? H * 0.45 : H * (W < 820 ? 0.52 : 0.36));
      var data = o.getImageData(0, 0, W, H).data, gap = (W < 820 ? 4 : 6) + (mode === 'ascii' ? 4 : 0), next = [];
      for (var y = 0; y < H; y += gap) for (var x = 0; x < W; x += gap) if (data[(y * W + x) * 4 + 3] > 128) next.push({ tx: x, ty: y });
      parts = next.map(function (t, k) {
        var old = parts[k];
        return { x: old ? old.x : Math.random() * W, y: old ? old.y : (mode === 'snow' ? -20 - Math.random() * H : (Math.random() < .5 ? -20 : H + 20) + Math.random() * 40), vx: 0, vy: 0, tx: t.tx, ty: t.ty, c: cols[k % cols.length], s: Math.random() * 1.4 + 1.1, g: GL[k % GL.length] };
      });
      if (reduce) parts.forEach(function (p) { p.x = p.tx; p.y = p.ty; });
    }
    function tick() {
      if (!running) return;
      ctx.clearRect(0, 0, W, H); if (mode === 'ascii') { ctx.font = '700 9px ui-monospace, monospace'; ctx.textBaseline = 'top'; }
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i], dx = p.x - mouse.x, dy = p.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 9000) { var f = (9000 - d2) / 9000 * 6; var d = Math.sqrt(d2) || 1; p.vx += dx / d * f; p.vy += dy / d * f; }
        p.vx += (p.tx - p.x) * 0.045; p.vy += (p.ty - p.y) * 0.045; p.vx *= 0.82; p.vy *= 0.82; p.x += p.vx; p.y += p.vy;
        if (mode === 'ascii') { ctx.fillStyle = p.c; if (Math.random() < .004) p.g = GL[Math.floor(Math.random() * GL.length)]; ctx.fillText(p.g, p.x, p.y); }
        else if (mode === 'lines') { ctx.strokeStyle = p.c; ctx.lineWidth = 1.2; ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - p.vx * 3 - 4, p.y - p.vy * 3); ctx.stroke(); }
        else if (mode === 'snow') { ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 6.3); ctx.fill(); }
        else { ctx.fillStyle = p.c; ctx.fillRect(p.x, p.y, p.s, p.s); }
      }
      requestAnimationFrame(tick);
    }
    build(); if (!reduce) tick(); else { ctx.clearRect(0, 0, W, H); parts.forEach(function (p) { ctx.fillStyle = p.c; ctx.fillRect(p.x, p.y, p.s, p.s); }); }
    var host = cv.parentElement;
    host.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
    host.addEventListener("pointerleave", function () { mouse.x = mouse.y = -9999; });
    var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(build, 200); });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { var vis = es[0].isIntersecting; if (vis && !running && !reduce) { running = true; tick(); } running = vis || reduce; }).observe(cv);
  });

  /* ---------- spotlight that follows the pointer on bento cards ---------- */
  document.querySelectorAll(".bx").forEach(function (b) {
    b.addEventListener("pointermove", function (e) { var r = b.getBoundingClientRect(); b.style.setProperty("--mx", (e.clientX - r.left) + "px"); b.style.setProperty("--my", (e.clientY - r.top) + "px"); });
  });

  /* ---------- accordion rows (v2 playbook) ---------- */
  document.querySelectorAll(".v2-acc button").forEach(function (b) {
    b.addEventListener("click", function () {
      var row = b.closest(".v2-acc-row"), open = row.classList.contains("open");
      row.parentNode.querySelectorAll(".v2-acc-row").forEach(function (r) { r.classList.remove("open"); r.querySelector("button").setAttribute("aria-expanded", "false"); });
      if (!open) { row.classList.add("open"); b.setAttribute("aria-expanded", "true"); }
    });
  });
})();
