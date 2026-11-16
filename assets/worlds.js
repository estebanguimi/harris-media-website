/* HMG client worlds — per-world interactions */
(function () {
  "use strict";
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function onView(el, fn) {
    if (!("IntersectionObserver" in window)) return fn();
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { io.disconnect(); fn(); } }); }, { threshold: 0.2 });
    io.observe(el);
  }

  /* chat interface: messages appear one after another */
  document.querySelectorAll("[data-chat]").forEach(function (box) {
    var msgs = Array.prototype.slice.call(box.querySelectorAll(".msg"));
    var typing = box.querySelector(".typing");
    if (reduce) { msgs.forEach(function (m) { m.classList.add("in"); }); if (typing) typing.remove(); return; }
    onView(box, function () {
      var i = 0;
      (function next() {
        if (i >= msgs.length) { if (typing) typing.style.display = "none"; return; }
        var m = msgs[i++];
        if (typing) { typing.style.display = m.classList.contains("bot") ? "inline-flex" : "none"; m.parentNode.insertBefore(typing, m); }
        setTimeout(function () { m.classList.add("in"); setTimeout(next, 650); }, m.classList.contains("bot") ? 1100 : 500);
      })();
    });
  });

  /* terminal typing */
  document.querySelectorAll("[data-term]").forEach(function (t) {
    var lines = JSON.parse(t.getAttribute("data-term"));
    var out = t.querySelector(".out"), cur = '<span class="cur"></span>';
    if (reduce) { out.textContent = lines.join("\n"); return; }
    onView(t, function () {
      var li = 0, ci = 0, txt = "";
      (function tick() {
        if (li >= lines.length) { out.innerHTML = esc(txt) + cur; return; }
        var line = lines[li];
        if (ci <= line.length) { out.innerHTML = esc(txt + line.slice(0, ci)) + cur; ci++; setTimeout(tick, line.charAt(0) === ">" ? 28 : 8); }
        else { txt += line + "\n"; li++; ci = 0; setTimeout(tick, 260); }
      })();
    });
  });
  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]; }); }


  /* split statements into words that rise in one by one */
  document.querySelectorAll(".x-words").forEach(function (el) {
    var words = el.textContent.trim().split(/\s+/);
    el.innerHTML = words.map(function (w, i) { return '<span class="wd" style="--w:' + i + '">' + esc(w) + '</span>'; }).join(" ");
    if (reduce) { el.classList.add("on"); return; }
    onView(el, function () { el.classList.add("on"); });
  });

  /* scroll parallax for giant outlined words */
  var px = Array.prototype.slice.call(document.querySelectorAll("[data-px]"));
  if (px.length && !reduce) {
    var ticking = false;
    function upd() {
      px.forEach(function (el) {
        var r = el.parentElement.getBoundingClientRect();
        var prog = (window.innerHeight - r.top) / (window.innerHeight + r.height);
        el.style.transform = "translate(" + ((prog - 0.5) * parseFloat(el.getAttribute("data-px")) * 100) + "vw, -50%)";
      });
      ticking = false;
    }
    window.addEventListener("scroll", function () { if (!ticking) { ticking = true; requestAnimationFrame(upd); } }, { passive: true });
    upd();
  }

  /* subtle 3D tilt on cards */
  if (!reduce && window.matchMedia("(hover: hover)").matches) {
    document.querySelectorAll("[data-tilt]").forEach(function (el) {
      el.addEventListener("mousemove", function (e) {
        var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - 0.5, y = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform = "perspective(800px) rotateY(" + (x * 10) + "deg) rotateX(" + (-y * 10) + "deg) translateY(-4px)";
      });
      el.addEventListener("mouseleave", function () { el.style.transform = ""; });
    });
  }

  /* clients hub: floating preview that follows the cursor */
  var pv = document.getElementById("hub-preview");
  if (pv) {
    var img = pv.querySelector("img"), cap = pv.querySelector(".cap"), x = 0, y = 0, tx = 0, ty = 0, raf = null;
    function loop() { x += (tx - x) * 0.18; y += (ty - y) * 0.18; pv.style.left = x + "px"; pv.style.top = y + "px"; raf = requestAnimationFrame(loop); }
    document.querySelectorAll(".roster a").forEach(function (a) {
      a.addEventListener("mouseenter", function (e) {
        img.src = a.getAttribute("data-img"); cap.textContent = a.getAttribute("data-world");
        pv.style.setProperty("--c", a.style.getPropertyValue("--c")); pv.style.setProperty("--ink", a.style.getPropertyValue("--ink"));
        tx = x = e.clientX + 170; ty = y = e.clientY; pv.classList.add("on"); if (!raf) loop();
      });
      a.addEventListener("mousemove", function (e) { tx = e.clientX + 170; ty = e.clientY; });
      a.addEventListener("mouseleave", function () { pv.classList.remove("on"); cancelAnimationFrame(raf); raf = null; });
    });
  }
})();
