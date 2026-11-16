/* FINAL pages: decode titles, laps scrub, stamped closing, per-page hover effects. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var G = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+=<>/";
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  var root = document.querySelector("[data-fx]"); if (!root) return;
  var fx = root.getAttribute("data-fx"), hfx = root.getAttribute("data-hfx");

  /* decode titles on load */
  if (fx === "decode" && !reduce) {
    setTimeout(function () {
      root.querySelectorAll("[data-split]").forEach(function (t) {
        var chars = t.querySelectorAll(".sc"), orig = Array.prototype.map.call(chars, function (c) { return c.textContent; }), s = performance.now();
        (function step(now) { var p = (now - s) / 1500; chars.forEach(function (c, k) { c.textContent = p > k / chars.length + .2 ? orig[k] : G[Math.floor(Math.random() * G.length)]; }); if (p < 1.25) requestAnimationFrame(step); else chars.forEach(function (c, k) { c.textContent = orig[k]; }); })(s);
      });
    }, 500);
  }

  /* per-page hover effect on title letters (replaces the default lift) */
  if (fine && !reduce && hfx && hfx !== "lift") {
    root.querySelectorAll("[data-split]").forEach(function (t) {
      var chars = [], orig = [];
      setTimeout(function () { chars = Array.prototype.slice.call(t.querySelectorAll(".sc")); orig = chars.map(function (c) { return c.textContent; }); }, 80);
      t.addEventListener("pointermove", function (e) {
        e.stopImmediatePropagation();
        chars.forEach(function (c, k) {
          var r = c.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), d = Math.sqrt(dx * dx + dy * dy), q = Math.max(0, 1 - d / 130);
          c.classList.toggle("hot", q > .3);
          if (hfx === "glow" || hfx === "neon") c.style.transform = "none";
          else if (hfx === "skew") c.style.transform = q ? "skewX(" + (-q * 16) + "deg)" : "none";
          else if (hfx === "flip") c.style.transform = q > .3 ? "rotateX(" + (q * 360) + "deg)" : "none";
          else if (hfx === "shake") c.style.transform = q > .3 ? "translate(" + ((Math.random() - .5) * 6 * q) + "px," + ((Math.random() - .5) * 6 * q) + "px) rotate(" + ((Math.random() - .5) * 8 * q) + "deg)" : "none";
          else if (hfx === "scramble") { c.style.transform = "none"; c.textContent = q > .45 && Math.random() < .5 ? G[Math.floor(Math.random() * G.length)] : orig[k]; }
        });
      }, true);
      t.addEventListener("pointerleave", function () { chars.forEach(function (c, k) { c.style.transform = "none"; c.classList.remove("hot"); c.textContent = orig[k]; }); });
    });
  }

  /* laps: the car follows the scroll */
  document.querySelectorAll("[data-laps]").forEach(function (s) {
    var laps = s.querySelectorAll("[data-lap]");
    function upd() { var r = s.getBoundingClientRect(), p = clamp((innerHeight * .8 - r.top) / (r.height + innerHeight * .1), 0, 1); s.style.setProperty("--lp", p.toFixed(3)); laps.forEach(function (l) { l.classList.toggle("on", p >= parseFloat(l.getAttribute("data-lap"))); }); }
    addEventListener("scroll", upd, { passive: true }); upd();
  });

  /* stamped closing */
  document.querySelectorAll("[data-stamps]").forEach(function (w) {
    if (!("IntersectionObserver" in window) || reduce) { w.classList.add("on"); return; }
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { w.classList.add("on"); io.disconnect(); } }, { threshold: .5 }); io.observe(w);
  });
})();

/* second set: signature draw, lighthouse beam */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll(".sx-sign").forEach(function (s) {
    if (!("IntersectionObserver" in window) || reduce) { s.classList.add("on"); return; }
    var io = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { s.classList.add("on"); io.disconnect(); } }, { threshold: .5 }); io.observe(s);
  });
  document.querySelectorAll("[data-beam]").forEach(function (s) {
    var lit = s.querySelector(".lh-lit"), a = -40, ta = -40, bx = 50, active = false, t0 = performance.now();
    s.addEventListener("pointermove", function (e) { var r = s.getBoundingClientRect(); active = true; bx = (e.clientX - r.left) / r.width * 100; ta = -14; });
    s.addEventListener("pointerleave", function () { active = false; t0 = performance.now(); });
    (function loop(now) {
      if (!active) { var t = (now - t0) / 1800; bx = 50 + Math.sin(t) * 40; ta = -14; }
      a += (ta - a) * .1; lit.style.setProperty("--bx", bx.toFixed(1) + "%"); lit.style.setProperty("--ba", a.toFixed(1) + "deg");
      if (!reduce) requestAnimationFrame(loop);
    })(performance.now());
  });
})();
