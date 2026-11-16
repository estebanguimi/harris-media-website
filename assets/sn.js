/* OUR SERVICES + NEWS versions: one interaction per version. */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var onScroll = [];
  addEventListener("scroll", function () { onScroll.forEach(function (f) { f(); }); }, { passive: true });
  addEventListener("resize", function () { onScroll.forEach(function (f) { f(); }); });

  /* Services V1 — sticky index scroll-spy */
  var chs = $$("[data-spy-target]");
  if (chs.length) {
    var links = $$("[data-spy]"), body = $(".ix-chs");
    var spy = function () {
      var mid = innerHeight * .45, cur = chs[0];
      chs.forEach(function (c) { if (c.getBoundingClientRect().top < mid) cur = c; });
      chs.forEach(function (c) { c.classList.toggle("on", c === cur); });
      links.forEach(function (a) { a.classList.toggle("on", a.getAttribute("data-spy") === cur.id); });
      var r = body.getBoundingClientRect();
      document.documentElement.style.setProperty("--ixp", Math.max(0, Math.min(1, (mid - r.top) / r.height)).toFixed(3));
    };
    onScroll.push(spy); spy();
  }

  /* Services V2 — matrix rows + column focus */
  $$(".mx-row").forEach(function (r) {
    var t = function () { var o = r.classList.toggle("open"); r.setAttribute("aria-expanded", o); };
    r.addEventListener("click", t);
    r.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); t(); } });
  });
  var mx = $(".mx");
  if (mx) {
    mx.addEventListener("mouseover", function (e) {
      var c = e.target.closest("[data-col]"), k = c && c.getAttribute("data-col");
      $$("[data-col]", mx).forEach(function (x) { x.classList.toggle("col-on", k !== null && x.getAttribute("data-col") === k); });
    });
    mx.addEventListener("mouseleave", function () { $$(".col-on", mx).forEach(function (x) { x.classList.remove("col-on"); }); });
  }

  /* Services V3 — program builder */
  var cards = $$(".bd-card");
  if (cards.length) {
    var goals = $$(".bd-goal"), list = $("#bd-list"), count = $("#bd-count"), send = $("#bd-send");
    var render = function () {
      var on = cards.filter(function (c) { return c.getAttribute("aria-pressed") === "true"; }).map(function (c) { return c.getAttribute("data-svc"); });
      count.textContent = (on.length < 10 ? "0" : "") + on.length;
      list.innerHTML = on.length ? on.map(function (n) { return "<li>" + n.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</li>"; }).join("") : '<li class="bd-empty">Choose a goal or a discipline to start.</li>';
      var gs = goals.filter(function (g) { return g.getAttribute("aria-pressed") === "true"; }).map(function (g) { return g.textContent; });
      send.href = "contact.html?service=" + encodeURIComponent(on.join(", ")) + (gs.length ? "&goal=" + encodeURIComponent(gs.join(", ")) : "");
      send.setAttribute("aria-disabled", on.length ? "false" : "true");
    };
    var syncFromGoals = function () {
      var want = {};
      goals.forEach(function (g) { if (g.getAttribute("aria-pressed") === "true") g.getAttribute("data-svcs").split("|").forEach(function (s) { want[s] = 1; }); });
      cards.forEach(function (c) { c.setAttribute("aria-pressed", want[c.getAttribute("data-svc")] ? "true" : "false"); });
    };
    goals.forEach(function (g) { g.addEventListener("click", function () { g.setAttribute("aria-pressed", g.getAttribute("aria-pressed") === "true" ? "false" : "true"); syncFromGoals(); render(); }); });
    cards.forEach(function (c) { c.addEventListener("click", function () { c.setAttribute("aria-pressed", c.getAttribute("aria-pressed") === "true" ? "false" : "true"); render(); }); });
    $("#bd-reset").addEventListener("click", function () { goals.concat(cards).forEach(function (x) { x.setAttribute("aria-pressed", "false"); }); render(); });
    render();
  }

  /* Services V4 — expanding columns */
  var cols = $$(".cl-s");
  cols.forEach(function (c) {
    var open = function () { cols.forEach(function (x) { x.classList.toggle("on", x === c); }); };
    c.addEventListener("click", open);
    c.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(); } });
    if (window.matchMedia("(hover: hover) and (min-width: 901px)").matches) {
      var t; c.addEventListener("mouseenter", function () { t = setTimeout(open, 180); }); c.addEventListener("mouseleave", function () { clearTimeout(t); });
    }
  });
  $$("[data-draw]").forEach(function (tl) {
    var items = $$(".cl-tl-i", tl);
    var f = function () {
      var r = tl.getBoundingClientRect(), p = Math.max(0, Math.min(1, (innerHeight * .7 - r.top) / r.height));
      tl.style.setProperty("--d", p.toFixed(3));
      items.forEach(function (it) { it.classList.toggle("lit", it.getBoundingClientRect().top < innerHeight * .7); });
    };
    onScroll.push(f); f();
  });

  /* News V2 — newswire */
  var wl = $("#wr-list");
  if (wl) {
    var rows = $$(".wr-row", wl), prev = $(".wr-prev");
    var show = function (r) {
      rows.forEach(function (x) { x.classList.toggle("on", x === r); });
      $("#wr-pt").textContent = r.getAttribute("data-t"); $("#wr-pc").textContent = r.getAttribute("data-c");
      $("#wr-pd").textContent = r.getAttribute("data-d"); $("#wr-px").textContent = r.getAttribute("data-x");
      $("#wr-pa").href = r.getAttribute("href");
      prev.classList.remove("swap"); void prev.offsetWidth; prev.classList.add("swap");
    };
    rows.forEach(function (r) { r.addEventListener("mouseenter", function () { show(r); }); r.addEventListener("focus", function () { show(r); }); });
    $$(".wr-tabs button").forEach(function (b) {
      b.addEventListener("click", function () {
        var k = b.getAttribute("data-w");
        $$(".wr-tabs button").forEach(function (x) { x.classList.toggle("on", x === b); });
        var first = null;
        rows.forEach(function (r) { var ok = k === "all" || r.getAttribute("data-w") === k; r.hidden = !ok; if (ok && !first) first = r; });
        if (first) show(first);
      });
    });
    var clock = $("#wr-time");
    var tick = function () { try { clock.textContent = new Date().toLocaleTimeString("en-US", { hour12: false, timeZone: "America/Chicago" }); } catch (e) { clock.textContent = new Date().toLocaleTimeString(); } };
    tick(); setInterval(tick, 1000);
  }

  /* News V3 — floating cover follows the cursor */
  var fl = $(".sp-float");
  if (fl && window.matchMedia("(hover: hover) and (min-width: 861px)").matches) {
    var fc = $$(".sp-card", fl), x = 0, y = 0, tx = 0, ty = 0, raf = 0;
    var loop = function () { x += (tx - x) * (reduce ? 1 : .16); y += (ty - y) * (reduce ? 1 : .16); fl.style.left = x + "px"; fl.style.top = y + "px"; raf = Math.abs(tx - x) + Math.abs(ty - y) > .5 ? requestAnimationFrame(loop) : 0; };
    $$(".sp-row").forEach(function (r) {
      r.addEventListener("mouseenter", function (e) { var k = r.getAttribute("data-k"); fc.forEach(function (c) { c.classList.toggle("on", c.getAttribute("data-k") === k); }); fl.classList.add("on"); if (!x) { x = e.clientX; y = e.clientY; } });
      r.addEventListener("mousemove", function (e) { tx = e.clientX + 200; ty = e.clientY; if (!raf) raf = requestAnimationFrame(loop); });
      r.addEventListener("mouseleave", function () { fl.classList.remove("on"); });
    });
  }

  /* News V4 — searchable archive timeline */
  var tl = $("#ar-tl");
  if (tl) {
    var its = $$(".ar-it", tl), marks = $$("[data-mark]", tl), q = $("#ar-q"), cat = "all";
    var orig = its.map(function (it) { return [$("h3", it).innerHTML, $("p", it).innerHTML]; });
    var esc = function (s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); };
    var apply = function () {
      var term = q.value.trim().toLowerCase(), n = 0, re = term ? new RegExp("(" + esc(term.replace(/&/g, "&amp;")) + ")", "gi") : null;
      its.forEach(function (it, k) {
        var ok = (cat === "all" || it.getAttribute("data-a") === cat) && (!term || it.getAttribute("data-q").indexOf(term) > -1);
        it.hidden = !ok; if (ok) n++;
        $("h3", it).innerHTML = re ? orig[k][0].replace(re, "<mark>$1</mark>") : orig[k][0];
        $("p", it).innerHTML = re ? orig[k][1].replace(re, "<mark>$1</mark>") : orig[k][1];
      });
      marks.forEach(function (m) { var s = m.nextElementSibling, vis = false; while (s && !s.hasAttribute("data-mark")) { if (!s.hidden) vis = true; s = s.nextElementSibling; } m.hidden = !vis; });
      $("#ar-n").textContent = (n < 10 ? "0" : "") + n; $("#ar-none").hidden = n > 0; draw();
    };
    q.addEventListener("input", apply);
    $$(".ar-chips button").forEach(function (b) { b.addEventListener("click", function () { cat = b.getAttribute("data-a"); $$(".ar-chips button").forEach(function (x) { x.classList.toggle("on", x === b); }); apply(); }); });
    var draw = function () { var r = tl.getBoundingClientRect(); tl.style.setProperty("--ap", Math.max(0, Math.min(1, (innerHeight * .6 - r.top) / Math.max(1, r.height))).toFixed(3)); };
    onScroll.push(draw); draw();
  }
})();
