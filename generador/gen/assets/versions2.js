/* HMG per-version effects: broadcast clock, 3D tiles, lens, spotlight, kinetic type,
   image-in-type, scramble/decode, blobs, scroll-lit words, odometers, hover letters. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function onView(el, fn, th) {
    if (!("IntersectionObserver" in window)) return fn();
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { io.disconnect(); fn(); } }); }, { threshold: th || 0.25 });
    io.observe(el);
  }
  var GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+=<>/\\";

  /* ---------- broadcast clock + timecode ---------- */
  document.querySelectorAll("[data-clock]").forEach(function (el) {
    (function t() { var d = new Date(); el.textContent = d.toTimeString().slice(0, 8) + " ET"; setTimeout(t, 1000); })();
  });
  document.querySelectorAll("[data-timecode]").forEach(function (el) {
    var f = 0; if (reduce) return;
    setInterval(function () { f++; var s = Math.floor(f / 25), pad = function (n) { return String(n).padStart(2, "0"); };
      el.textContent = pad(Math.floor(s / 3600)) + ":" + pad(Math.floor(s / 60) % 60) + ":" + pad(s % 60) + ":" + pad(f % 25); }, 40);
  });

  /* ---------- 3D photo tiles ---------- */
  document.querySelectorAll("[data-tiles]").forEach(function (box) {
    var dims = box.getAttribute("data-tiles").split("x"), cols = +dims[0], rows = +dims[1];
    box.style.gridTemplateColumns = "repeat(" + cols + ",1fr)"; box.style.gridTemplateRows = "repeat(" + rows + ",1fr)";
    var tiles = [];
    for (var r = 0; r < rows; r++) for (var c = 0; c < cols; c++) {
      var t = document.createElement("div"); t.className = "tile";
      t.style.setProperty("--bs", (cols * 100) + "% " + (rows * 100) + "%");
      t.style.setProperty("--bp", (c / (cols - 1) * 100) + "% " + (r / (rows - 1) * 100) + "%");
      t.style.setProperty("--d", (r + c) * 2 + Math.random() * 6);
      box.appendChild(t); tiles.push({ el: t, c: c, r: r });
    }
    onView(box, function () { box.classList.add("go"); setTimeout(function () { box.classList.add("live"); }, 1800); }, 0.1);
    if (!fine || reduce) return;
    box.addEventListener("pointermove", function (e) {
      var rc = box.getBoundingClientRect(), mx = (e.clientX - rc.left) / rc.width * cols, my = (e.clientY - rc.top) / rc.height * rows;
      tiles.forEach(function (t) {
        var dx = t.c + .5 - mx, dy = t.r + .5 - my, d = Math.sqrt(dx * dx + dy * dy), k = Math.max(0, 1 - d / 3);
        t.el.style.transform = k ? "translateZ(" + (k * 60) + "px) rotateY(" + (-dx * k * 14) + "deg) rotateX(" + (dy * k * 14) + "deg)" : "";
        t.el.style.filter = k ? "brightness(" + (1 + k * .35) + ")" : "";
      });
    });
    box.addEventListener("pointerleave", function () { tiles.forEach(function (t) { t.el.style.transform = ""; t.el.style.filter = ""; }); });
  });

  /* ---------- magnifying lens over the title ---------- */
  document.querySelectorAll("[data-lens]").forEach(function (st) {
    var R = Math.min(170, window.innerWidth * .16), x = st.clientWidth * .3, y = st.clientHeight * .5, tx = x, ty = y, active = false, t0 = performance.now();
    st.style.setProperty("--lr", R + "px");
    function loop(now) {
      if (!active && !reduce) { var a = (now - t0) / 2200; tx = st.clientWidth * (.5 + Math.sin(a) * .32); ty = st.clientHeight * (.5 + Math.sin(a * 1.7) * .18); }
      x += (tx - x) * .12; y += (ty - y) * .12;
      st.style.setProperty("--lx", x + "px"); st.style.setProperty("--ly", y + "px");
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
    st.addEventListener("pointermove", function (e) { var r = st.getBoundingClientRect(); active = true; tx = e.clientX - r.left; ty = e.clientY - r.top; });
    st.addEventListener("pointerleave", function () { active = false; t0 = performance.now(); });
  });

  /* ---------- spotlight ---------- */
  document.querySelectorAll("[data-spot]").forEach(function (h) {
    var x = innerWidth * .65, y = innerHeight * .4, tx = x, ty = y, active = false, t0 = performance.now();
    h.style.setProperty("--sr", Math.max(170, innerWidth * .17) + "px");
    function loop(now) {
      if (!active && !reduce) { var a = (now - t0) / 2600; tx = h.clientWidth * (.55 + Math.cos(a) * .25); ty = h.clientHeight * (.42 + Math.sin(a * 1.3) * .15); }
      x += (tx - x) * .1; y += (ty - y) * .1;
      h.style.setProperty("--sx", x + "px"); h.style.setProperty("--sy", y + "px");
      requestAnimationFrame(loop);
    }
    requestAnimationFrame(loop);
    h.addEventListener("pointermove", function (e) { var r = h.getBoundingClientRect(); active = true; tx = e.clientX - r.left; ty = e.clientY - r.top; });
    h.addEventListener("pointerleave", function () { active = false; t0 = performance.now(); });
  });

  /* ---------- kinetic rows: drift + scroll velocity ---------- */
  var rows = Array.prototype.slice.call(document.querySelectorAll(".kn-row"));
  if (rows.length && !reduce) {
    var off = rows.map(function () { return Math.random() * -400; }), lastY = scrollY, boost = 0;
    (function loop() {
      var y = scrollY; boost = boost * .9 + (y - lastY) * .4; lastY = y;
      rows.forEach(function (r, k) {
        var dir = +r.getAttribute("data-dir"), inner = r.firstElementChild, w = inner.scrollWidth / 6;
        off[k] += dir * (0.6 + Math.abs(boost) * .15);
        if (off[k] < -w) off[k] += w; if (off[k] > 0) off[k] -= w;
        inner.style.transform = "translate3d(" + off[k] + "px,0,0)";
      });
      requestAnimationFrame(loop);
    })();
  }

  /* ---------- image inside type: pan with pointer ---------- */
  document.querySelectorAll("[data-pan]").forEach(function (w) {
    var host = w.closest(".hx"), px = 50, py = 30, tx = 50, ty = 30;
    host.addEventListener("pointermove", function (e) { var r = host.getBoundingClientRect(); tx = 20 + (e.clientX - r.left) / r.width * 60; ty = 10 + (e.clientY - r.top) / r.height * 60; });
    (function loop(now) {
      if (!fine) { tx = 50 + Math.sin(now / 3000) * 25; }
      px += (tx - px) * .06; py += (ty - py) * .06;
      w.style.setProperty("--px", px + "%"); w.style.setProperty("--py", py + "%");
      if (!reduce) requestAnimationFrame(loop);
    })(0);
  });

  /* ---------- scramble / decode titles ---------- */
  function scramble(el, dur) {
    var chars = el.querySelectorAll(".sc"); if (!chars.length || reduce) return;
    var orig = Array.prototype.map.call(chars, function (c) { return c.textContent; }), start = performance.now();
    (function step(now) {
      var p = (now - start) / dur;
      chars.forEach(function (c, k) { var at = k / chars.length; c.textContent = p > at + .25 ? orig[k] : GLYPHS[Math.floor(Math.random() * GLYPHS.length)]; });
      if (p < 1.3) requestAnimationFrame(step); else chars.forEach(function (c, k) { c.textContent = orig[k]; });
    })(start);
  }
  document.querySelectorAll(".sc-title").forEach(function (t) {
    setTimeout(function () { scramble(t, 1400); }, 700);
    t.addEventListener("pointerenter", function () { scramble(t, 700); });
  });
  document.querySelectorAll("[data-type]").forEach(function (pre) {
    var lines = JSON.parse(pre.getAttribute("data-type")), txt = "";
    if (reduce) { pre.textContent = lines.join("\n"); return; }
    onView(pre, function () {
      var li = 0, ci = 0;
      (function tick() {
        if (li >= lines.length) { pre.innerHTML = txt.replace(/[<&]/g, "") + '<span class="cur"></span>'; return; }
        var line = lines[li];
        if (ci <= line.length) { pre.innerHTML = (txt + line.slice(0, ci)).replace(/[<&]/g, "") + '<span class="cur"></span>'; ci++; setTimeout(tick, 16); }
        else { txt += line + "\n"; li++; ci = 0; setTimeout(tick, 180); }
      })();
    }, 0.1);
  });
  document.querySelectorAll("[data-glitch]").forEach(function (g) {
    g.addEventListener("pointerenter", function () { g.classList.add("glitch"); });
    g.addEventListener("pointerleave", function () { g.classList.remove("glitch"); });
    if (!fine && !reduce) setInterval(function () { g.classList.add("glitch"); setTimeout(function () { g.classList.remove("glitch"); }, 380); }, 3500);
  });

  /* ---------- soft blobs ---------- */
  document.querySelectorAll("canvas[data-blob]").forEach(function (cv) {
    var ctx = cv.getContext("2d"), cols = cv.getAttribute("data-blob").split(","), W, H, m = { x: .7, y: .4 }, t = 0;
    var blobs = cols.concat(cols[0]).map(function (c, k) { return { c: c, x: Math.random(), y: Math.random(), r: .22 + Math.random() * .18, s: .0006 + k * .00025, p: Math.random() * 6 }; });
    function size() { W = cv.width = cv.clientWidth / 2; H = cv.height = cv.clientHeight / 2; }
    size(); addEventListener("resize", size);
    cv.parentElement.addEventListener("pointermove", function (e) { var r = cv.getBoundingClientRect(); m.x = (e.clientX - r.left) / r.width; m.y = (e.clientY - r.top) / r.height; });
    (function loop() {
      t += 16; ctx.clearRect(0, 0, W, H); ctx.globalCompositeOperation = "lighter";
      blobs.forEach(function (b, k) {
        var x = (k === blobs.length - 1 ? m.x : .5 + Math.sin(t * b.s + b.p) * .38) * W, y = (k === blobs.length - 1 ? m.y : .5 + Math.cos(t * b.s * 1.3 + b.p) * .34) * H, r = b.r * Math.max(W, H);
        var g = ctx.createRadialGradient(x, y, 0, x, y, r); g.addColorStop(0, b.c); g.addColorStop(1, "transparent");
        ctx.globalAlpha = .55; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.3); ctx.fill();
      });
      if (!reduce) requestAnimationFrame(loop);
    })();
  });

  /* ---------- words that light up as you scroll ---------- */
  var wordBlocks = [];
  document.querySelectorAll("[data-words]").forEach(function (p) {
    var ws = p.textContent.trim().split(/\s+/);
    p.innerHTML = ws.map(function (w) { return '<span class="ww">' + w.replace(/[<&]/g, "") + "</span>"; }).join(" ");
    wordBlocks.push({ el: p, words: p.querySelectorAll(".ww") });
  });
  function lightWords() {
    wordBlocks.forEach(function (b) {
      var r = b.el.getBoundingClientRect(), p = clamp((innerHeight * .85 - r.top) / (r.height + innerHeight * .35), 0, 1), n = Math.round(p * b.words.length);
      b.words.forEach(function (w, k) { w.classList.toggle("on", k < n); w.classList.toggle("now", k >= n - 3 && k < n); });
    });
  }
  if (wordBlocks.length) { addEventListener("scroll", lightWords, { passive: true }); lightWords(); if (reduce) wordBlocks.forEach(function (b) { b.words.forEach(function (w) { w.classList.add("on"); }); }); }

  /* ---------- odometers ---------- */
  document.querySelectorAll("[data-odo]").forEach(function (el) {
    var v = el.getAttribute("data-odo");
    el.innerHTML = v.split("").map(function (ch, k) {
      if (!/\d/.test(ch)) return "<span>" + ch + "</span>";
      var col = ""; for (var i = 0; i <= 10; i++) col += "<span>" + ((+ch + i) % 10) + "</span>";
      return '<span class="dg" style="--k:' + k + ';transform:translateY(-' + 10 + 'em)">' + col + "</span>";
    }).join("");
    onView(el, function () { el.querySelectorAll(".dg").forEach(function (d) { d.style.transform = "translateY(0)"; }); });
  });

  /* ---------- services list: image follows pointer ---------- */
  document.querySelectorAll(".sx-svc").forEach(function (list) {
    var fl = list.parentNode.parentNode.querySelector(".svc-float"); if (!fl || !fine) return;
    var img = fl.querySelector("img"), x = 0, y = 0, tx = 0, ty = 0, raf = null;
    function loop() { x += (tx - x) * .2; y += (ty - y) * .2; fl.style.left = x + "px"; fl.style.top = y + "px"; raf = requestAnimationFrame(loop); }
    list.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("pointerenter", function (e) { img.src = a.getAttribute("data-img"); tx = x = e.clientX + 160; ty = y = e.clientY; fl.classList.add("on"); if (!raf) loop(); });
      a.addEventListener("pointermove", function (e) { tx = e.clientX + 160; ty = e.clientY; });
      a.addEventListener("pointerleave", function () { fl.classList.remove("on"); cancelAnimationFrame(raf); raf = null; });
    });
  });

  /* ---------- hover letters: characters near the cursor lift and light up ---------- */
  if (fine && !reduce) {
    document.querySelectorAll("[data-hovertext], .w-hero [data-split]").forEach(function (t) {
      var chars = [];
      setTimeout(function () { chars = Array.prototype.slice.call(t.querySelectorAll(".sc")); }, 50);
      t.addEventListener("pointermove", function (e) {
        chars.forEach(function (c) {
          var r = c.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), d = Math.sqrt(dx * dx + dy * dy), k = Math.max(0, 1 - d / 140);
          c.style.transform = k ? "translateY(" + (-k * 18) + "%) scale(" + (1 + k * .12) + ")" : "none";
          c.classList.toggle("hot", k > .35);
        });
      });
      t.addEventListener("pointerleave", function () { chars.forEach(function (c) { c.style.transform = "none"; c.classList.remove("hot"); }); });
    });
  }
})();
