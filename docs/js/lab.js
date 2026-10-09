/**
 * Single-page lab guide behaviour.
 *
 * - TREE rail: highlights the section in view, expands its module, fills
 *   the ░░░ progress bar as the page scrolls, and "loads" the pixel avatar
 *   row by row in step with that progress.
 * - Tasks: every heading with a data-task attribute (set in index.md) gets a
 *   "Mark complete" button at the end of its section. Ticks show in the rail
 *   and are stored in localStorage.
 * - J / K jump to the next / previous section.
 * - Notes: a small scratchpad (bottom-right) saved in localStorage and
 *   shared by all parts.
 * - Report an issue: a short form that posts to the feedback-api Vercel
 *   function, which files a GitHub issue. Hidden until FEEDBACK_ENDPOINT is set.
 */
(function () {
  // Task ticks are stored per part (several parts have a "1a"); notes are shared.
  var partMatch = window.location.pathname.match(/\/part-(\d+)(\/|$)/);
  var DONE_KEY = partMatch ? "ltrcol2011:done:part-" + partMatch[1] : "ltrcol2011:done";
  var NOTES_KEY = "ltrcol2011:notes";
  var BAR_CHARS = 26;
  // URL of the deployed feedback-api function, e.g. https://<project>.vercel.app/api/report
  var FEEDBACK_ENDPOINT = "https://aibydesignforcollab.vercel.app/api/report";
  var activeId = null;   // section currently in view, kept by setupScroll

  var store = {
    get: function (key, fallback) {
      try {
        var raw = localStorage.getItem(key);
        return raw === null ? fallback : JSON.parse(raw);
      } catch (e) { return fallback; }
    },
    set: function (key, value) {
      try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
    }
  };

  function init() {
    var article = document.querySelector(".lab .prose");
    var tree = document.getElementById("tree");
    if (!article || !tree || tree.dataset.ready) return;
    tree.dataset.ready = "1";

    var links = Array.prototype.slice.call(tree.querySelectorAll("a[data-id]"));
    var linkById = {};
    var heads = [];
    links.forEach(function (a) {
      var h = document.getElementById(a.dataset.id);
      if (h) { linkById[a.dataset.id] = a; heads.push(h); }
    });

    setupTasks(article, linkById);
    setupScroll(heads, linkById);
    setupKeys(heads);
    setupRailTitle();
    setupNotes();
    setupReport(links);
  }

  // ── Active section + progress ────────────────────────────────────────
  function setupScroll(heads, linkById) {
    var bar = document.querySelector("#prog b");
    var rest = document.querySelector("#prog i");
    var pct = document.querySelector("#prog .pct");
    var line = document.getElementById("scrollLine");
    var art = document.getElementById("railArt");
    var artCap = art && art.querySelector(".rail-art__cap");
    var current = null;
    var ticking = false;

    function update() {
      ticking = false;
      var doc = document.documentElement;
      var max = doc.scrollHeight - window.innerHeight;
      var p = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 1;
      var filled = Math.round(p * BAR_CHARS);
      if (bar) bar.textContent = new Array(filled + 1).join("▓");
      if (rest) rest.textContent = new Array(BAR_CHARS - filled + 1).join("░");
      var whole = Math.round(p * 100);
      if (pct) pct.textContent = (whole >= 100 ? "100" : ("0" + whole).slice(-2)) + "%";
      if (line) line.style.width = (p * 100).toFixed(1) + "%";
      if (art) {
        // reveal the 64x48 pixel scene one pixel row at a time
        var rows = Math.round(p * 48);
        art.style.setProperty("--reveal", (rows / 48 * 100).toFixed(3) + "%");
        art.classList.toggle("empty", rows === 0);
        var isDone = rows >= 48;
        if (isDone !== art.classList.contains("done")) {
          art.classList.toggle("done", isDone);
          artCap.innerHTML = isDone ? "AVATAR LOADED ✓" : 'LOADING AVATAR<span class="dots">…</span>';
        }
      }

      var mark = window.innerHeight * 0.3;
      var active = heads[0];
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top - mark <= 0) active = heads[i];
        else break;
      }
      if (p >= 0.999) active = heads[heads.length - 1];
      if (active && active !== current) {
        current = active;
        activeId = active.id;
        Object.keys(linkById).forEach(function (id) {
          linkById[id].classList.toggle("on", id === active.id);
        });
        var link = linkById[active.id];
        var group = link && link.closest(".tree-group");
        document.querySelectorAll("#tree .tree-group").forEach(function (g) {
          g.classList.toggle("open", g === group);
        });
        keepInView(link);
      }
    }

    window.addEventListener("scroll", function () {
      if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    window.addEventListener("resize", update);
    update();
  }

  // When the TREE has to scroll (short screens), keep the active entry visible
  // without moving the page itself.
  function keepInView(link) {
    var tree = document.getElementById("tree");
    if (!tree || !link || tree.scrollHeight <= tree.clientHeight) return;
    setTimeout(function () {             // wait for the module group to expand
      var t = tree.getBoundingClientRect();
      var r = link.getBoundingClientRect();
      if (r.top < t.top + 8) tree.scrollTop -= (t.top + 8 - r.top);
      else if (r.bottom > t.bottom - 8) tree.scrollTop += (r.bottom - t.bottom + 8);
    }, 420);
  }

  // ── J / K section jumps ──────────────────────────────────────────────
  function setupKeys(heads) {
    document.addEventListener("keydown", function (e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      var t = e.target;
      if (t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.tagName))) return;
      var key = e.key.toLowerCase();
      if (key !== "j" && key !== "k") return;
      var mark = window.innerHeight * 0.3;
      var idx = -1;
      for (var i = 0; i < heads.length; i++) {
        if (heads[i].getBoundingClientRect().top - mark <= 1) idx = i;
      }
      var next = key === "j" ? idx + 1 : idx - 1;
      if (key === "k" && idx >= 0 && heads[idx].getBoundingClientRect().top < -10) next = idx;
      if (next < 0) { window.scrollTo({ top: 0, behavior: "smooth" }); return; }
      if (next >= heads.length) return;
      e.preventDefault();
      heads[next].scrollIntoView({ behavior: "smooth", block: "start" });
    });
  }

  // ── Rail title fades in once the hero title has scrolled away ────────
  function setupRailTitle() {
    var title = document.getElementById("railTitle");
    var h1 = document.querySelector(".hero h1");
    if (!title || !h1 || !("IntersectionObserver" in window)) return;
    new IntersectionObserver(function (entries) {
      title.classList.toggle("on", !entries[0].isIntersecting);
    }, { rootMargin: "-60px 0px 0px 0px" }).observe(h1);
  }

  // ── Tasks ────────────────────────────────────────────────────────────
  function setupTasks(article, linkById) {
    var done = store.get(DONE_KEY, {});
    var taskHeads = Array.prototype.slice.call(article.querySelectorAll("[data-task]"));
    var counter = document.querySelector("#tasks");

    function sectionEnd(h) {
      var level = h.tagName === "H2" ? 2 : 3;
      var el = h.nextElementSibling;
      while (el) {
        var isEyebrow = el.classList && el.classList.contains("eyebrow");
        if (isEyebrow || el.tagName === "H2" || (level === 3 && el.tagName === "H3")) return el;
        el = el.nextElementSibling;
      }
      return null;
    }

    function paint(id, h, btn) {
      var isDone = !!done[id];
      btn.setAttribute("aria-pressed", String(isDone));
      btn.querySelector(".box").textContent = isDone ? "☑" : "☐";
      btn.querySelector(".tx").textContent = isDone ? "Completed · " + id.toUpperCase() : "Mark " + id.toUpperCase() + " complete";
      var link = linkById[h.id];
      if (link) {
        link.classList.toggle("done", isDone);
        var br = link.querySelector(".br");
        if (br) br.textContent = isDone ? "✓" : (link.classList.contains("lvl-3") ? "├" : "└");
      }
    }

    function count() {
      if (!counter) return;
      var n = taskHeads.filter(function (h) { return done[h.dataset.task]; }).length;
      var pad = function (x) { return ("0" + x).slice(-2); };
      counter.querySelector(".n").textContent = pad(n) + "/" + pad(taskHeads.length);
      counter.classList.toggle("all", n === taskHeads.length && n > 0);
    }

    taskHeads.forEach(function (h) {
      var id = h.dataset.task;
      var wrap = document.createElement("div");
      wrap.className = "task-done";
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "task-done-btn";
      btn.innerHTML = '<span class="box" aria-hidden="true"></span><span class="tx"></span>';
      btn.addEventListener("click", function () {
        if (done[id]) delete done[id]; else done[id] = true;
        store.set(DONE_KEY, done);
        paint(id, h, btn);
        count();
      });
      wrap.appendChild(btn);
      var end = sectionEnd(h);
      if (end) article.insertBefore(wrap, end); else article.appendChild(wrap);
      paint(id, h, btn);
    });
    count();
  }

  // ── Notes ────────────────────────────────────────────────────────────
  function setupNotes() {
    if (document.querySelector(".notes-fab")) return;

    var fab = document.createElement("button");
    fab.type = "button";
    fab.className = "notes-fab";
    fab.setAttribute("aria-label", "Open lab notes");
    fab.innerHTML = '<span aria-hidden="true">✎</span> NOTES <span class="dot" aria-hidden="true"></span>';

    var panel = document.createElement("section");
    panel.className = "notes-panel";
    panel.hidden = true;
    panel.setAttribute("aria-label", "Lab notes");
    panel.innerHTML =
      '<header><span>LAB NOTES</span><button type="button" data-act="close" aria-label="Close notes">CLOSE ✕</button></header>' +
      '<textarea spellcheck="false" placeholder="Pod domain, Control Hub login, Charles / Anita phone numbers…"></textarea>' +
      '<footer><span class="st">SAVED IN THIS BROWSER ONLY</span><button type="button" data-act="clear">CLEAR</button></footer>';

    document.body.appendChild(fab);
    document.body.appendChild(panel);

    var area = panel.querySelector("textarea");
    var status = panel.querySelector(".st");
    var clearBtn = panel.querySelector('[data-act="clear"]');
    var armed = false;
    var saveTimer = null;

    area.value = store.get(NOTES_KEY, "");
    fab.classList.toggle("has-notes", !!area.value.trim());

    function open() { panel.hidden = false; fab.hidden = true; area.focus(); }
    function close() { panel.hidden = true; fab.hidden = false; disarm(); }
    function disarm() { armed = false; clearBtn.textContent = "CLEAR"; clearBtn.classList.remove("warn"); }

    fab.addEventListener("click", open);
    panel.querySelector('[data-act="close"]').addEventListener("click", close);
    area.addEventListener("input", function () {
      clearTimeout(saveTimer);
      status.textContent = "SAVING…";
      saveTimer = setTimeout(function () {
        store.set(NOTES_KEY, area.value);
        status.textContent = "SAVED IN THIS BROWSER ONLY";
        fab.classList.toggle("has-notes", !!area.value.trim());
      }, 300);
    });
    clearBtn.addEventListener("click", function () {
      if (!armed) {
        armed = true;
        clearBtn.textContent = "CLICK AGAIN TO CLEAR";
        clearBtn.classList.add("warn");
        setTimeout(disarm, 3000);
        return;
      }
      area.value = "";
      store.set(NOTES_KEY, "");
      fab.classList.remove("has-notes");
      disarm();
      area.focus();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) close();
    });
  }

  // ── Report an issue ──────────────────────────────────────────────────
  function setupReport(links) {
    if (!FEEDBACK_ENDPOINT || document.querySelector(".report-fab")) return;

    var fab = document.createElement("button");
    fab.type = "button";
    fab.className = "report-fab";
    fab.setAttribute("aria-label", "Report an issue with this lab");
    fab.title = "Report an issue with this lab";
    fab.innerHTML = '<span aria-hidden="true">⚑</span> REPORT';

    var options = links.map(function (a) {
      var lb = a.querySelector(".lb");
      var text = (lb ? lb.textContent : a.textContent).trim();
      return '<option value="' + a.dataset.id + '">' + text.replace(/</g, "&lt;") + "</option>";
    }).join("");

    var panel = document.createElement("section");
    panel.className = "notes-panel report-panel";
    panel.hidden = true;
    panel.setAttribute("aria-label", "Report an issue");
    panel.innerHTML =
      '<header><span>REPORT AN ISSUE</span><button type="button" data-act="close" aria-label="Close report form">CLOSE ✕</button></header>' +
      '<form novalidate>' +
        '<label>SECTION<select name="section">' + options + '<option value="">Other / not sure</option></select></label>' +
        '<label>WHAT HAPPENED?<textarea name="message" required minlength="10" maxlength="4000" placeholder="Which step, what you expected, and what you saw instead…"></textarea></label>' +
        '<label><span>YOUR NAME OR EMAIL <em>(optional)</em></span><input name="contact" maxlength="200" autocomplete="email"></label>' +
        '<label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>' +
        '<footer><span class="st">GOES TO THE LAB AUTHOR · PUBLIC ON GITHUB</span><button type="submit">SEND</button></footer>' +
      '</form>';

    document.body.appendChild(fab);
    document.body.appendChild(panel);

    // Stack directly above NOTES with the same width, so the pair reads as one.
    var notesFab = document.querySelector(".notes-fab");
    function dock() {
      if (!notesFab || notesFab.hidden) return;
      fab.style.width = notesFab.style.width = "";
      var w = Math.max(fab.offsetWidth, notesFab.offsetWidth);
      fab.style.width = notesFab.style.width = w + "px";
      fab.style.bottom = (window.innerHeight - notesFab.getBoundingClientRect().top + 8) + "px";
    }
    dock();
    window.addEventListener("resize", dock);

    var form = panel.querySelector("form");
    var select = form.elements.section;
    var status = panel.querySelector(".st");
    var send = form.querySelector('[type="submit"]');
    var idle = status.textContent;

    function open() {
      if (activeId && select.querySelector('option[value="' + activeId + '"]')) select.value = activeId;
      panel.hidden = false; fab.hidden = true;
      form.elements.message.focus();
    }
    function close() { panel.hidden = true; fab.hidden = false; }

    fab.addEventListener("click", open);
    panel.querySelector('[data-act="close"]').addEventListener("click", close);
    form.elements.message.addEventListener("input", function () {
      if (!send.disabled) status.textContent = idle;
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hidden) close();
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var message = form.elements.message.value.trim();
      if (message.length < 10) {
        status.textContent = "PLEASE ADD A LITTLE MORE DETAIL";
        form.elements.message.focus();
        return;
      }
      var opt = select.options[select.selectedIndex];
      var base = window.location.href.split("#")[0];
      send.disabled = true;
      status.textContent = "SENDING…";
      fetch(FEEDBACK_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          section: select.value ? opt.textContent : "Other / not sure",
          page: document.title,
          url: select.value ? base + "#" + select.value : base,
          contact: form.elements.contact.value,
          message: message,
          website: form.elements.website.value
        })
      }).then(function (r) {
        return r.json().catch(function () { return {}; }).then(function (data) {
          if (!r.ok) throw new Error(data.error || "Something went wrong");
          return data;
        });
      }).then(function (data) {
        form.elements.message.value = "";
        status.textContent = data.number ? "THANKS · FILED AS #" + data.number : "THANKS · REPORT SENT";
        setTimeout(function () { status.textContent = idle; close(); }, 2500);
      }).catch(function (err) {
        status.textContent = String(err.message || err).toUpperCase();
      }).then(function () { send.disabled = false; });
    });
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(init);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
