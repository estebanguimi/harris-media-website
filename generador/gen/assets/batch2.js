/* BATCH 2 effects: underdog meter, scratch card, month grid, racetrack, photo finish, split-flap,
   hit counter, Iowa counties, book, envelope, marquee bulbs, curtain light, drag-scroll gallery. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function prog(el, start, span) { var r = el.getBoundingClientRect(); return clamp((innerHeight * (start || .9) - r.top) / (r.height + innerHeight * (span || .4)), 0, 1); }
  function onView(el, fn, th) {
    if (!("IntersectionObserver" in window)) return fn();
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { io.disconnect(); fn(); } }); }, { threshold: th || 0.35 });
    io.observe(el);
  }
  var scrollers = [];
  function onScroll(fn) { scrollers.push(fn); fn(); }
  addEventListener("scroll", function () { scrollers.forEach(function (f) { f(); }); }, { passive: true });

  /* underdog meter */
  document.querySelectorAll("[data-meter]").forEach(function (m) {
    var rd = m.querySelector("[data-meter-read]");
    onScroll(function () { var p = prog(m, .95, .3); m.style.setProperty("--deg", (-80 + p * 160) + "deg"); rd.textContent = p < .34 ? "UNDERDOG" : p < .7 ? "CONTENDER" : "WINNER"; });
  });

  /* scratch card */
  document.querySelectorAll("canvas[data-scratch]").forEach(function (cv) {
    var cols = cv.getAttribute("data-scratch").split(","), card = cv.parentElement, ctx = cv.getContext("2d"), down = false, done = false;
    function paint() {
      var d = Math.min(devicePixelRatio || 1, 2); cv.width = cv.clientWidth * d; cv.height = cv.clientHeight * d; ctx.setTransform(d, 0, 0, d, 0, 0);
      var W = cv.clientWidth, H = cv.clientHeight, g = ctx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, "#C8CDD3"); g.addColorStop(.5, "#EEF1F4"); g.addColorStop(1, "#AEB4BB");
      ctx.globalCompositeOperation = "source-over"; ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
      ctx.fillStyle = cols[0]; ctx.font = "400 " + Math.round(W / 6) + "px Anton, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.globalAlpha = .9; ctx.fillText("THE", W / 2, H * .36); ctx.fillText("RESULT", W / 2, H * .55); ctx.globalAlpha = .35;
      for (var k = 0; k < 40; k++) { ctx.fillStyle = cols[1]; ctx.fillText("★", Math.random() * W, Math.random() * H); }
      ctx.globalAlpha = 1;
    }
    paint(); addEventListener("resize", paint);
    function scratch(e) {
      var r = cv.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
      ctx.globalCompositeOperation = "destination-out"; ctx.beginPath(); ctx.arc(x, y, 34, 0, 6.3); ctx.fill();
      if (!done && Math.random() < .08) {
        var d = ctx.getImageData(0, 0, cv.width, cv.height).data, clear = 0; for (var i = 3; i < d.length; i += 160) if (d[i] === 0) clear++;
        if (clear / (d.length / 160) > .45) { done = true; card.classList.add("done"); cv.style.transition = "opacity .8s"; cv.style.opacity = 0; }
      }
    }
    cv.addEventListener("pointerdown", function (e) { down = true; cv.setPointerCapture(e.pointerId); scratch(e); });
    cv.addEventListener("pointermove", function (e) { if (down || e.pointerType === "mouse") scratch(e); });
    cv.addEventListener("pointerup", function () { down = false; });
    if (reduce) { cv.style.opacity = 0; card.classList.add("done"); }
  });

  /* 36 months */
  document.querySelectorAll("[data-months]").forEach(function (g) {
    var cells = g.querySelectorAll("i");
    onScroll(function () { var n = Math.round(prog(g, .9, .5) * cells.length); cells.forEach(function (c, k) { c.classList.toggle("on", k < n); }); });
  });

  /* racetrack */
  document.querySelectorAll("canvas[data-race]").forEach(function (cv) {
    var ctx, W, H, flash = cv.parentElement.querySelector(".tk-flash"), cs = getComputedStyle(cv);
    var acc = cs.getPropertyValue("--a").trim() || "#FF6B35", fg = cs.getPropertyValue("--fg").trim() || "#12343B";
    var horses = [{ l: 0, sp: .0036, c: fg, r: 7 }, { l: .02, sp: .0035, c: fg, r: 7 }, { l: -.03, sp: .00345, c: fg, r: 7 }, { l: -.06, sp: .0032, c: acc, r: 10, us: true }];
    function size() { var d = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * d; cv.height = H * d; ctx = cv.getContext("2d"); ctx.setTransform(d, 0, 0, d, 0, 0); }
    size(); addEventListener("resize", size);
    var lap = 0;
    (function loop() {
      ctx.clearRect(0, 0, W, H);
      horses.forEach(function (h, k) {
        var p = (h.l % 1 + 1) % 1, late = p > .55;
        h.l += h.us ? (late ? .0049 : .0031) : h.sp;
        var a = -Math.PI / 2 + p * Math.PI * 2, rx = W * (.4 + k * .006), ry = H * (.317 + k * .006);
        var x = W / 2 + Math.cos(a) * rx, y = H / 2 + Math.sin(a) * ry;
        ctx.fillStyle = h.c; ctx.globalAlpha = h.us ? 1 : .55; ctx.beginPath(); ctx.arc(x, y, h.r, 0, 6.3); ctx.fill();
        if (h.us) { ctx.globalAlpha = .25; ctx.beginPath(); ctx.arc(x, y, h.r * 2.2, 0, 6.3); ctx.fill(); }
      });
      ctx.globalAlpha = 1;
      var us = horses[3]; if (Math.floor(us.l) > lap) { lap = Math.floor(us.l); flash.classList.remove("on"); void flash.offsetWidth; flash.classList.add("on"); horses.forEach(function (h) { h.l = Math.floor(us.l) + (h.us ? -.06 : (Math.random() * .05)); }); }
      if (!reduce) requestAnimationFrame(loop);
    })();
  });

  /* photo finish */
  document.querySelectorAll("[data-finish]").forEach(function (f) {
    var inp = f.querySelector("input"), line = f.querySelector(".pf-line"), res = document.querySelector("[data-finish-res]");
    function upd() { var v = +inp.value; line.style.setProperty("--fx", v + "%"); res.textContent = v >= 76.5 && v <= 79 ? "By a nose — the dark horse wins." : v > 79 ? "The dark horse crossed first." : "Still racing… drag to the line."; }
    inp.addEventListener("input", upd); upd();
  });

  /* split-flap board */
  var CH = " ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  document.querySelectorAll("[data-flap]").forEach(function (row, ri) {
    var target = row.getAttribute("data-flap").padEnd(20).slice(0, 20), cells = row.querySelectorAll(".fb-c");
    onView(row, function () {
      cells.forEach(function (c, k) {
        var goal = target[k], n = reduce ? 0 : 6 + Math.floor(Math.random() * 10) + k;
        (function flip(left) {
          c.textContent = left > 0 ? CH[Math.floor(Math.random() * CH.length)] : goal;
          c.classList.remove("flip"); void c.offsetWidth; c.classList.add("flip");
          if (left > 0) setTimeout(function () { flip(left - 1); }, 55);
        })(n);
      });
    }, .1);
  });

  /* hit counter */
  document.querySelectorAll("[data-hits]").forEach(function (h) {
    var n = 4210; if (reduce) { h.textContent = "004210"; return; }
    setInterval(function () { n += Math.floor(Math.random() * 3); h.textContent = String(n).padStart(6, "0"); }, 700);
  });

  /* Iowa counties: asterisk → #1 */
  document.querySelectorAll("[data-counties]").forEach(function (g) {
    var cells = g.querySelectorAll("i"), stage = g.parentElement, read = stage.querySelector("[data-county-read]"), order = Array.prototype.map.call(cells, function (_, k) { return k; }).sort(function () { return Math.random() - .5; }), t0 = performance.now();
    (function loop(now) {
      var p = reduce ? 1 : clamp((now - t0 - 900) / 5200, 0, 1), n = Math.round(p * cells.length);
      order.forEach(function (k, j) { cells[k].classList.toggle("on", j < n); });
      stage.style.setProperty("--ap", clamp((p - .55) / .45, 0, 1).toFixed(3));
      read.textContent = p < .35 ? "AN ASTERISK IN THE POLLS" : p < .99 ? "GAINING, COUNTY BY COUNTY" : "IOWA CAUCUS WINNER";
      if (p < 1) requestAnimationFrame(loop);
    })(t0);
  });
  document.querySelectorAll("[data-book]").forEach(function (b) { onView(b, function () { b.classList.add("open"); }, .5); });
  document.querySelectorAll("[data-env]").forEach(function (b) { onView(b, function () { b.classList.add("is-in"); }, .5); });

  /* marquee bulbs placed around the frame + stage light follows pointer */
  document.querySelectorAll(".ct-marquee").forEach(function (m) {
    var bulbs = m.querySelectorAll(".ct-bulbs i");
    function place() {
      var W = m.offsetWidth, H = m.offsetHeight, P = 2 * (W + H), step = P / bulbs.length;
      bulbs.forEach(function (b, k) {
        var d = k * step, x, y;
        if (d < W) { x = d; y = 0; } else if (d < W + H) { x = W; y = d - W; } else if (d < 2 * W + H) { x = W - (d - W - H); y = H; } else { x = 0; y = H - (d - 2 * W - H); }
        b.style.left = (x - 5) + "px"; b.style.top = (y - 5) + "px";
      });
    }
    place(); addEventListener("resize", place); setTimeout(place, 600);
  });
  document.querySelectorAll("[data-stage]").forEach(function (s) {
    s.addEventListener("pointermove", function (e) { var r = s.getBoundingClientRect(); s.style.setProperty("--lx", ((e.clientX - r.left) / r.width * 100) + "%"); s.style.setProperty("--ly", ((e.clientY - r.top) / r.height * 100) + "%"); });
  });

  /* drag-to-scroll gallery */
  document.querySelectorAll("[data-dragscroll]").forEach(function (el) {
    var down = false, sx, sl;
    el.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; sx = e.clientX; sl = el.scrollLeft; el.classList.add("drag"); });
    addEventListener("pointerup", function () { down = false; el.classList.remove("drag"); });
    el.addEventListener("pointermove", function (e) { if (!down) return; el.scrollLeft = sl - (e.clientX - sx); });
  });
})();
