/* Last five finals: hover modes, pipeline valves, summit climb, edit-bay playhead, film leader. */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function prog(el, a, b) { var r = el.getBoundingClientRect(); return clamp((innerHeight * (a || .8) - r.top) / (r.height + innerHeight * (b || .2)), 0, 1); }
  var root = document.querySelector("[data-fx]");
  var hfx = root && root.getAttribute("data-hfx");

  /* hover modes owned by these pages */
  if (root && fine && !reduce && /^(beat|heat|gild|frost|rec)$/.test(hfx)) {
    root.querySelectorAll("[data-split]").forEach(function (t) {
      var chars = []; setTimeout(function () { chars = Array.prototype.slice.call(t.querySelectorAll(".sc")); }, 80);
      t.addEventListener("pointermove", function (e) {
        e.stopImmediatePropagation();
        chars.forEach(function (c, k) {
          var r = c.getBoundingClientRect(), dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2), q = Math.max(0, 1 - Math.sqrt(dx * dx + dy * dy) / 130);
          c.classList.toggle("hot", q > .3);
          if (hfx === "beat") c.style.transform = q > .3 ? "scale(" + (1 + .18 * Math.abs(Math.sin(performance.now() / 120 + k))) + ")" : "none";
          else if (hfx === "heat") c.style.transform = q > .3 ? "translateY(" + (Math.sin(performance.now() / 60 + k) * 2) + "px) skewX(" + (Math.sin(performance.now() / 90 + k) * 4) + "deg)" : "none";
          else if (hfx === "frost") c.style.transform = q > .3 ? "translateY(" + (-q * 6) + "px)" : "none";
          else if (hfx === "rec") c.style.transform = q > .3 ? "translateX(" + ((Math.random() - .5) * 3) + "px)" : "none";
          else c.style.transform = "none";
        });
      }, true);
      t.addEventListener("pointerleave", function () { chars.forEach(function (c) { c.style.transform = "none"; c.classList.remove("hot"); }); });
    });
  }

  var scrollers = [];
  addEventListener("scroll", function () { scrollers.forEach(function (f) { f(); }); }, { passive: true });

  /* pipeline: flow advances and valves open */
  document.querySelectorAll("[data-pipe]").forEach(function (s) {
    var v = s.querySelectorAll("[data-valve]");
    var f = function () { var p = prog(s, .85, .1); s.style.setProperty("--pp", p.toFixed(3)); v.forEach(function (x) { x.classList.toggle("open", p >= parseFloat(x.getAttribute("data-valve"))); }); };
    scrollers.push(f); f();
  });

  /* summit climb: a marker walks the ridge */
  document.querySelectorAll("[data-summits]").forEach(function (s) {
    var path = s.querySelector(".sm-ridge"), me = s.querySelector(".sm-me"), flags = s.querySelectorAll(".sm-f"), cards = s.querySelectorAll("[data-peak]");
    var pts = [[0, 360], [80, 300], [190, 330], [300, 220], [410, 260], [520, 140], [630, 190], [740, 60]];
    var f = function () {
      var p = prog(s, .8, .2) * (pts.length - 1), i = Math.min(pts.length - 2, Math.floor(p)), t = p - i;
      me.setAttribute("cx", pts[i][0] + (pts[i + 1][0] - pts[i][0]) * t); me.setAttribute("cy", pts[i][1] + (pts[i + 1][1] - pts[i][1]) * t);
      var q = p / (pts.length - 1);
      flags.forEach(function (fl, k) { fl.classList.toggle("on", q >= (k * 2 + 1) / 7); });
      cards.forEach(function (c) { c.classList.toggle("on", q >= parseFloat(c.getAttribute("data-peak"))); });
    };
    scrollers.push(f); f();
  });

  /* edit bay: playhead follows the scroll */
  document.querySelectorAll("[data-nle]").forEach(function (s) {
    var notes = s.querySelectorAll("[data-clip]");
    var f = function () { var p = prog(s, .8, .1); s.style.setProperty("--ph", p.toFixed(3)); notes.forEach(function (n) { n.classList.toggle("on", p >= parseFloat(n.getAttribute("data-clip"))); }); };
    scrollers.push(f); f();
  });

  /* film leader countdown */
  document.querySelectorAll("[data-leader]").forEach(function (s) {
    var n = s.querySelector(".ld-n"), sw = s.querySelector(".ld-sweep");
    if (reduce || !("IntersectionObserver" in window)) { s.classList.add("done"); n.textContent = ""; return; }
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var start = performance.now();
      (function loop(now) {
        var t = (now - start) / 1000, k = Math.floor(t);
        if (k < 3) { n.textContent = 3 - k; sw.style.setProperty("--sw", ((t - k) * 360) + "deg"); requestAnimationFrame(loop); }
        else { n.textContent = ""; sw.style.setProperty("--sw", "0deg"); s.classList.add("done"); }
      })(start);
    }, { threshold: .5 });
    io.observe(s);
  });
})();
