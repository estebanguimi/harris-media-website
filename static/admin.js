/* Panel HMG: editor de texto, vistas previas de imágenes, confirmaciones y avisos de carga. */
(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  function busy(msg) {
    var o = document.createElement("div"); o.className = "busy-overlay"; o.innerHTML = "<span></span>";
    o.firstChild.appendChild(document.createTextNode(msg || "Guardando…")); document.body.appendChild(o);
  }

  /* confirmations */
  $$("[data-confirm]").forEach(function (b) {
    b.addEventListener("click", function (e) { if (!confirm(b.getAttribute("data-confirm"))) e.preventDefault(); });
  });

  /* busy messages: publish + forms with uploads */
  $$("form[data-busy]").forEach(function (f) { f.addEventListener("submit", function () { busy(f.getAttribute("data-busy")); }); });
  $$("form[data-busy-upload]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      var btn = e.submitter, hasVideo = $$('input[type=file][name=video]', f).some(function (i) { return i.files.length; });
      busy(btn && btn.getAttribute("data-busy") ? btn.getAttribute("data-busy") : hasVideo ? "Subiendo video… (puede tardar un poco, no cierres la página)" : "Guardando…");
    });
  });

  /* image previews + file names */
  $$("input[type=file][data-preview]").forEach(function (inp) {
    inp.addEventListener("change", function () {
      var box = inp.closest(".img-field").querySelector(".img-prev"), f = inp.files[0];
      if (!f) return;
      box.classList.remove("empty"); box.innerHTML = ""; var img = document.createElement("img"); img.src = URL.createObjectURL(f); box.appendChild(img);
      inp.parentNode.classList.add("has-file");
    });
  });
  $$("input[type=file][data-filename]").forEach(function (inp) {
    inp.addEventListener("change", function () {
      var l = inp.parentNode; if (!inp.files[0]) return;
      l.classList.add("has-file"); l.firstChild.nodeValue = "✓ " + inp.files[0].name + " ";
    });
  });

  /* tabs */
  $$("[data-tabs]").forEach(function (t) {
    var btns = $$("button", t), panes = $$("[data-pane]", t.parentNode);
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.classList.toggle("on", x === b); });
        panes.forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== b.getAttribute("data-tab"); });
      });
    });
  });

  /* rich text editor */
  var toAdmin = function (h) { return h.replace(/(src|href)="media\//g, '$1="/media/'); };
  var toSite = function (h) { return h.replace(/(src|href)="\/media\//g, '$1="media/'); };
  $$(".rte").forEach(function (box, k) {
    var area = box.querySelector(".rte-area"), ta = box.querySelector("textarea"), form = box.closest("form");
    area.innerHTML = toAdmin(ta.value.trim());
    if (!area.textContent.trim() && !area.querySelector("img")) area.innerHTML = "";
    var mark = function () {
      var pane = box.closest("[data-pane]");
      if (!pane) return;
      var tb = document.querySelector('[data-tabs] [data-tab="' + pane.getAttribute("data-pane") + '"]');
      if (tb) tb.classList.toggle("filled", !!area.textContent.trim());
    };
    mark(); area.addEventListener("input", mark);
    document.execCommand("defaultParagraphSeparator", false, "p");
    var cmd = function (c) {
      area.focus();
      if (c === "h2") document.execCommand("formatBlock", false, "h2");
      else if (c === "p") document.execCommand("formatBlock", false, "p");
      else if (c === "bold" || c === "italic") document.execCommand(c);
      else if (c === "ul") document.execCommand("insertUnorderedList");
      else if (c === "ol") document.execCommand("insertOrderedList");
      else if (c === "quote") document.execCommand("formatBlock", false, "blockquote");
      else if (c === "clear") { document.execCommand("removeFormat"); document.execCommand("formatBlock", false, "p"); document.execCommand("unlink"); }
      else if (c === "link") {
        var u = prompt("Pega la dirección del enlace (por ejemplo https://…):", "https://");
        if (u && u !== "https://") document.execCommand("createLink", false, u);
      } else if (c === "image") {
        var sel = window.getSelection(), range = sel.rangeCount ? sel.getRangeAt(0).cloneRange() : null;
        var fi = document.createElement("input"); fi.type = "file"; fi.accept = "image/*";
        fi.onchange = function () {
          if (!fi.files[0]) return;
          var fd = new FormData(); fd.append("archivo", fi.files[0]); fd.append("_csrf", window.CSRF);
          busy("Subiendo imagen…");
          fetch("/admin/subir-imagen", { method: "POST", body: fd, headers: { "X-CSRF": window.CSRF } })
            .then(function (r) { return r.json(); })
            .then(function (j) {
              document.querySelector(".busy-overlay").remove();
              if (j.error) { alert(j.error); return; }
              area.focus(); if (range) { sel.removeAllRanges(); sel.addRange(range); }
              document.execCommand("insertHTML", false, '<figure><img src="/' + j.url + '" alt=""></figure><p><br></p>');
            })
            .catch(function () { document.querySelector(".busy-overlay").remove(); alert("No se pudo subir la imagen."); });
        };
        fi.click();
      }
    };
    $$("[data-cmd]", box).forEach(function (b) { b.addEventListener("mousedown", function (e) { e.preventDefault(); }); b.addEventListener("click", function () { cmd(b.getAttribute("data-cmd")); }); });
    /* paste: keep paragraphs, drop styles */
    area.addEventListener("paste", function (e) {
      var html = e.clipboardData.getData("text/html"), text = e.clipboardData.getData("text/plain");
      e.preventDefault();
      if (html) {
        var d = document.createElement("div"); d.innerHTML = html;
        $$("style,script,meta,link,title", d).forEach(function (n) { n.remove(); });
        $$("*", d).forEach(function (n) { ["style", "class", "id", "width", "height", "face", "color", "size", "align", "dir", "lang"].forEach(function (a) { n.removeAttribute(a); }); });
        $$("span,font", d).forEach(function (n) { while (n.firstChild) n.parentNode.insertBefore(n.firstChild, n); n.remove(); });
        document.execCommand("insertHTML", false, d.innerHTML);
      } else {
        var esc = function (s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
        document.execCommand("insertHTML", false, text.split(/\n\s*\n/).map(function (p) { return "<p>" + esc(p).replace(/\n/g, "<br>") + "</p>"; }).join(""));
      }
    });
    form.addEventListener("submit", function () { ta.value = toSite(area.innerHTML); });
  });
})();

/* Instagram: show only the photo / video (hide Instagram's own header and footer) */
(function () {
  var TOP = 54, BOTTOM = 154;
  function apply(f) {
    var r = f._igr, box = f.parentNode;
    if (!r) return;
    if ((box.getAttribute("data-igfit") || "shape") === "shape") {
      var card = box.closest(".work");
      if (card && r < 0.85) card.classList.add("wide");          /* horizontal video / photo: wide card */
      box.style.aspectRatio = "1 / " + r.toFixed(4);
      f.style.top = -TOP + "px"; f.style.height = "calc(100% + " + (TOP + BOTTOM) + "px)";
    } else {
      var tile = box.closest(".hw-tile");
      if (tile && r < 0.85 && tile.classList.contains("hw-image")) { tile.classList.remove("hw-image"); tile.classList.add("hw-video"); }
      var bw = box.clientWidth, bh = box.clientHeight, mm = r * bw, s = Math.max(bh / mm, 1);
      f.style.width = bw + "px"; f.style.height = (mm + TOP + BOTTOM) + "px"; f.style.transformOrigin = "0 0";
      f.style.transform = "scale(" + s + ")"; f.style.left = (-(bw * s - bw) / 2) + "px"; f.style.top = (-TOP * s - (mm * s - bh) / 2) + "px";
    }
    box.classList.add("ig-ready");
  }
  window.addEventListener("message", function (e) {
    if (e.origin !== "https://www.instagram.com") return;
    var d = e.data;
    try { if (typeof d === "string") d = JSON.parse(d); } catch (x) { return; }
    if (!d || d.type !== "MEASURE" || !d.details || !d.details.height) return;
    var frames = document.querySelectorAll("iframe[data-ig]");
    for (var k = 0; k < frames.length; k++) {
      var f = frames[k];
      if (f.contentWindow !== e.source || !f.offsetWidth) continue;
      var m = d.details.height - TOP - BOTTOM;
      if (m > 40) { f._igr = m / f.offsetWidth; apply(f); }
    }
  });
  var t;
  window.addEventListener("resize", function () {
    clearTimeout(t);
    t = setTimeout(function () { var fr = document.querySelectorAll("iframe[data-ig]"); for (var k = 0; k < fr.length; k++) apply(fr[k]); }, 200);
  });
})();

