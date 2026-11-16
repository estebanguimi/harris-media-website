/* HARRIS MEDIA GROUP — shared subpage behaviour */
(function () {
  "use strict";
  var root = document.documentElement;
  root.classList.remove("no-js");

  /* ---------- theme (dark default, remembered per visitor) ---------- */
  var LOGO_DARK = "https://www.harrismediallc.com/wp-content/uploads/2024/12/logo-DARK.png";
  var LOGO_LIGHT = "https://lh3.googleusercontent.com/aida-public/AB6AXuAwf6tJZtbggvDrVc-2AsC5sjOzFC7LjccKTHxA_U7vQ46AdFvOXV1WrAjhT4BhFai1UxajXESA8NO9LBN0HWFtOTy0sS0mJo-KbIrkkmRo31d8c8pmIT-tfj55PFQ_TpTeQLQiFmTq96dN4SJ9kQc4abydURpxWsEakNREiycH24MoG6I5RKU3PAiTw7tpxRC4MoxGaoLNnbKyJcTjf9RyQAnEaIrpAmkOaNj15LKqsVNv785c7mycbw";
  var SUN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>';
  var MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
  function store(k, v) { try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function applyTheme(dark) {
    root.classList.toggle("dark", dark);
    document.querySelectorAll("[data-logo]").forEach(function (img) { img.src = dark ? LOGO_DARK : LOGO_LIGHT; });
    var b = document.getElementById("theme-btn");
    if (b) { b.innerHTML = dark ? MOON : SUN; b.setAttribute("aria-label", dark ? "Switch to light mode" : "Switch to dark mode"); }
  }
  applyTheme(store("hmg-theme") !== "light");
  var tb = document.getElementById("theme-btn");
  if (tb) tb.addEventListener("click", function () {
    var dark = !root.classList.contains("dark");
    applyTheme(dark); store("hmg-theme", dark ? "dark" : "light");
  });

  /* ---------- mobile menu ---------- */
  var header = document.querySelector(".site-header");
  var menuBtn = document.getElementById("menu-btn");
  if (menuBtn && header) {
    menuBtn.addEventListener("click", function () {
      var open = header.classList.toggle("menu-open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    header.querySelectorAll(".main-nav a").forEach(function (a) {
      a.addEventListener("click", function () { header.classList.remove("menu-open"); menuBtn.setAttribute("aria-expanded", "false"); });
    });
  }

  /* ---------- scroll progress rail ---------- */
  var prog = document.getElementById("hmg-progress");
  function onScroll() {
    if (!prog) return;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    prog.style.transform = "scaleX(" + (h > 0 ? Math.min(1, window.scrollY / h) : 0) + ")";
  }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();

  /* ---------- reveal on scroll (auto-stagger siblings) ---------- */
  var groups = new Map();
  document.querySelectorAll("[data-reveal]").forEach(function (el) {
    var p = el.parentElement, n = groups.get(p) || 0;
    if (!el.style.getPropertyValue("--i")) el.style.setProperty("--i", Math.min(n, 8));
    groups.set(p, n + 1);
  });
  var counted = new WeakSet();
  function countUp(el) {
    if (counted.has(el)) return; counted.add(el);
    var end = parseFloat(el.getAttribute("data-count")), suf = el.getAttribute("data-suffix") || "", pad = el.getAttribute("data-pad");
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var fmt = function (v) { var s = Math.round(v).toLocaleString("en-US"); if (pad) s = s.padStart(+pad, "0"); return s + suf; };
    if (reduce) { el.textContent = fmt(end); return; }
    var t0 = null, dur = 1600;
    function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur); el.textContent = fmt(end * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add("is-in");
        e.target.querySelectorAll("[data-count]").forEach(countUp);
        if (e.target.hasAttribute("data-count")) countUp(e.target);
        io.unobserve(e.target);
      });
    }, { threshold: 0, rootMargin: "0px 0px -8% 0px" });
    document.querySelectorAll("[data-reveal], [data-count]").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll("[data-reveal]").forEach(function (el) { el.classList.add("is-in"); });
    document.querySelectorAll("[data-count]").forEach(countUp);
  }

  /* ---------- ticker: duplicate content for seamless loop ---------- */
  document.querySelectorAll(".ticker .track").forEach(function (t) { t.innerHTML += t.innerHTML; });

  /* ---------- filters ---------- */
  document.querySelectorAll("[data-filters]").forEach(function (bar) {
    var target = document.querySelector(bar.getAttribute("data-filters"));
    var counter = document.querySelector(bar.getAttribute("data-counter") || "#none");
    var items = target ? Array.prototype.slice.call(target.querySelectorAll("[data-cat]")) : [];
    function update(f) {
      var shown = 0;
      items.forEach(function (it) {
        var ok = f === "all" || (" " + it.getAttribute("data-cat") + " ").indexOf(" " + f + " ") > -1;
        it.classList.toggle("is-hidden", !ok); if (ok) { shown++; it.classList.add("is-in"); }
      });
      if (counter) counter.textContent = String(shown).padStart(2, "0");
    }
    bar.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        bar.querySelectorAll("button").forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); });
        update(b.getAttribute("data-f"));
      });
    });
    update("all");
  });

  /* ---------- tabs (multi-language bios) ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (wrap) {
    var btns = wrap.querySelectorAll(".tabs button"), panes = wrap.querySelectorAll("[data-pane]");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.toggle("on", x === b); x.setAttribute("aria-selected", x === b); });
        panes.forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== b.getAttribute("data-tab"); });
      });
    });
  });

  /* ---------- works: official players embedded in the cards ---------- */
  document.querySelectorAll("iframe[data-embed-src]").forEach(function (f) {
    var src = f.getAttribute("data-embed-src");
    if (/facebook\.com\/plugins\//.test(src)) {
      var w = Math.round(f.getBoundingClientRect().width) || 500;
      src += "&width=" + Math.max(350, Math.min(750, w));
    }
    f.addEventListener("load", function () { f.parentNode.classList.add("embed-ready"); });
    f.src = src;
  });

  /* Instagram: show only the photo / video (hide Instagram's own header and footer) */
  (function () {
    var TOP = 54, BOTTOM = 154;
    function fit(f, H) {
      var box = f.parentNode, m = H - TOP - BOTTOM;
      if (m < 40) return;
      if ((box.getAttribute("data-igfit") || "shape") === "shape") {
        var W = box.clientWidth;
        box.style.aspectRatio = W + " / " + m;
        f.style.top = -TOP + "px"; f.style.height = H + "px";
      } else {
        var bw = box.clientWidth, bh = box.clientHeight, s = Math.max(bh / m, 1);
        f.style.width = bw + "px"; f.style.height = H + "px"; f.style.transformOrigin = "0 0";
        f.style.transform = "scale(" + s + ")"; f.style.left = (-(bw * s - bw) / 2) + "px"; f.style.top = (-TOP * s - (m * s - bh) / 2) + "px";
      }
      box.classList.add("ig-ready");
    }
    window.addEventListener("message", function (e) {
      if (e.origin !== "https://www.instagram.com") return;
      var d = e.data;
      try { if (typeof d === "string") d = JSON.parse(d); } catch (x) { return; }
      if (!d || d.type !== "MEASURE" || !d.details || !d.details.height) return;
      var frames = document.querySelectorAll("iframe[data-ig]");
      for (var k = 0; k < frames.length; k++) if (frames[k].contentWindow === e.source) fit(frames[k], d.details.height);
    });
  })();

  /* ---------- works: Facebook / Instagram official embeds ---------- */
  var sdkCards = Array.prototype.slice.call(document.querySelectorAll(".work.embed-sdk"));
  if (sdkCards.length) {
    var fit = function () {
      sdkCards.forEach(function (card) {
        var f = card.querySelector("iframe");
        if (!f || !f.offsetWidth || f.offsetHeight < 60) return;
        card.querySelector(".photo").classList.add("embed-ready");
        if (card.getAttribute("data-sized") || !card.classList.contains("embed-facebook")) return;
        card.setAttribute("data-sized", "1");
        var box = card.querySelector(".fb-video");
        /* horizontal video in a narrow card: widen the card and let Facebook redraw it at the new size */
        if (box && f.offsetHeight < f.offsetWidth * 0.9 && !card.classList.contains("wide")) {
          card.classList.add("wide");
          if (window.FB && FB.XFBML) {
            box.removeAttribute("fb-xfbml-state"); box.removeAttribute("fb-iframe-plugin-query"); box.innerHTML = "";
            FB.XFBML.parse(card);
          }
        }
      });
    };
    var prevInit = window.fbAsyncInit;
    window.fbAsyncInit = function () {
      if (prevInit) prevInit();
      if (window.FB && FB.Event) FB.Event.subscribe("xfbml.render", function () { setTimeout(fit, 400); });
    };
    var tries = 0, poll = setInterval(function () { fit(); if (++tries > 40) clearInterval(poll); }, 500);
  }

  /* ---------- lightbox (works) ---------- */
  var lb = document.getElementById("lightbox");
  if (lb) {
    var media = lb.querySelector(".media"), cap = lb.querySelector(".cap-t"), cat = lb.querySelector(".cap-c");
    var list = [], idx = 0, lastFocus = null;
    function visible() { return Array.prototype.slice.call(document.querySelectorAll("[data-work]:not(.is-hidden)")); }
    function show() {
      var w = list[idx], vid = w.getAttribute("data-video"), emb = w.getAttribute("data-embed"), img = w.querySelector("img");
      media.innerHTML = "";
      if (emb) {
        var f = document.createElement("iframe"); f.src = emb; f.title = w.getAttribute("data-title") || "Video";
        f.setAttribute("allow", "autoplay; fullscreen; picture-in-picture"); f.setAttribute("allowfullscreen", "");
        var kind = w.getAttribute("data-embed-kind") || "video";
        f.style.cssText = kind === "post" ? "width:min(92vw,500px);height:min(82vh,760px);border:0;display:block;background:#fff;border-radius:6px"
          : kind === "vertical" ? "height:min(82vh,780px);aspect-ratio:9/16;max-width:92vw;border:0;display:block;background:#000"
          : "width:min(90vw,1100px);aspect-ratio:16/9;border:0;display:block;background:#000";
        media.appendChild(f);
      } else if (vid) {
        var v = document.createElement("video"); v.src = vid; v.controls = true; v.autoplay = true; v.playsInline = true;
        if (img) v.poster = img.src;
        v.onerror = function () { media.innerHTML = ""; if (img) { var i = document.createElement("img"); i.src = img.src; i.alt = img.alt; media.appendChild(i); } };
        media.appendChild(v);
      } else if (img) { var i = document.createElement("img"); i.src = img.src; i.alt = img.alt; media.appendChild(i); }
      cap.textContent = w.getAttribute("data-title") || ""; cat.textContent = w.getAttribute("data-label") || "";
    }
    function open(w) { list = visible(); idx = list.indexOf(w); lastFocus = document.activeElement; show(); lb.classList.add("open"); lb.querySelector(".x").focus(); }
    function close() { lb.classList.remove("open"); media.innerHTML = ""; if (lastFocus) lastFocus.focus(); }
    function step(d) { idx = (idx + d + list.length) % list.length; show(); }
    document.querySelectorAll("[data-work]").forEach(function (w) {
      w.setAttribute("tabindex", "0"); w.setAttribute("role", "button");
      w.addEventListener("click", function () { open(w); });
      w.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); open(w); } });
    });
    lb.querySelector(".x").addEventListener("click", close);
    lb.querySelector(".prev").addEventListener("click", function () { step(-1); });
    lb.querySelector(".next").addEventListener("click", function () { step(1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close(); if (e.key === "ArrowLeft") step(-1); if (e.key === "ArrowRight") step(1);
    });
  }

  /* ---------- contact form ---------- */
  var form = document.getElementById("contact-form");
  if (form) {
    // Set data-endpoint on the <form> to a form service URL (Formspree, Netlify, your CRM...).
    // Without one, the message opens in the visitor's email app addressed to data-mailto.
    var params = new URLSearchParams(location.search);
    var pre = params.get("service"); if (pre) { var sel = form.querySelector("[name=service]"); if (sel) sel.value = pre; }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var ok = true;
      form.querySelectorAll("[required]").forEach(function (f) {
        var bad = !f.value.trim() || (f.type === "email" && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(f.value));
        f.closest(".field").classList.toggle("invalid", bad); if (bad) ok = false;
      });
      if (!ok) { var first = form.querySelector(".invalid input, .invalid select, .invalid textarea"); if (first) first.focus(); return; }
      var data = new FormData(form), endpoint = form.getAttribute("data-endpoint");
      var done = function () { form.hidden = true; document.getElementById("form-ok").classList.add("show"); };
      if (endpoint) {
        fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } }).then(done).catch(function () { alert("Something went wrong. Please call 512-900-9439."); });
      } else {
        var body = []; data.forEach(function (v, k) { if (k !== "website") body.push(k.toUpperCase() + ": " + v); });
        location.href = "mailto:" + form.getAttribute("data-mailto") + "?subject=" + encodeURIComponent("New project inquiry — " + (data.get("service") || "HMG")) + "&body=" + encodeURIComponent(body.join("\n"));
        done();
      }
    });
    form.querySelectorAll("input, select, textarea").forEach(function (f) {
      f.addEventListener("input", function () { var fl = f.closest(".field"); if (fl) fl.classList.remove("invalid"); });
    });
  }


  /* ---------- team: face strip autoplay, view toggle, unit shortcuts ---------- */
  var strip = document.getElementById("facestrip");
  if (strip) {
    var sl = Array.prototype.slice.call(strip.querySelectorAll(".fs-slice:not(.fs-you)")), cur = 0, paused = false;
    var reduceM = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function setOn(i) { sl.forEach(function (s, k) { s.classList.toggle("is-on", k === i); }); }
    setOn(0);
    strip.addEventListener("mouseenter", function () { paused = true; });
    strip.addEventListener("mouseleave", function () { paused = false; });
    if (!reduceM && window.matchMedia("(min-width: 761px)").matches) {
      setInterval(function () { if (!paused && !document.hidden) { cur = (cur + 1) % sl.length; setOn(cur); } }, 2600);
    }
  }
  var grid = document.getElementById("roster-grid"), idx = document.getElementById("roster-index");
  if (grid && idx) {
    document.querySelectorAll(".viewtog button").forEach(function (b) {
      b.addEventListener("click", function () {
        document.querySelectorAll(".viewtog button").forEach(function (x) { x.classList.toggle("on", x === b); });
        var isIdx = b.getAttribute("data-view") === "index";
        grid.classList.toggle("is-hidden", isIdx); idx.classList.toggle("is-hidden", !isIdx);
      });
    });
    document.querySelectorAll("#team-filters button").forEach(function (b) {
      b.addEventListener("click", function () {
        var f = b.getAttribute("data-f");
        idx.querySelectorAll("li").forEach(function (li) { li.classList.toggle("is-hidden", f !== "all" && li.getAttribute("data-cat") !== f); });
      });
    });
    document.querySelectorAll(".unit-go").forEach(function (u) {
      u.addEventListener("click", function () {
        var btn = document.querySelector('#team-filters button[data-f="' + u.getAttribute("data-unit") + '"]');
        if (btn) btn.click();
        document.getElementById("roster-sec").scrollIntoView({ behavior: "smooth" });
      });
    });
  }

  var y = document.getElementById("year"); if (y) y.textContent = new Date().getFullYear();
})();
