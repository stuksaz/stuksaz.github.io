// Drobné efekty webu. Bez JavaScriptu se stránka zobrazí celá, jen bez pohybu.
(function () {
  var reduceMotion = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Rok v patičce
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = String(new Date().getFullYear());
  });

  // Proudnice „stlačeného vzduchu“ v tmavém úvodu
  function airflow(canvas) {
    var ctx = canvas.getContext("2d");
    if (!ctx) return;
    var style = getComputedStyle(canvas);
    var colA = style.getPropertyValue("--flow-a").trim() || "#ff6b45";
    var colB = style.getPropertyValue("--flow-b").trim() || "#5fa8d3";
    var w = 0, h = 0, t = 0, parts = [], running = false, raf = 0;

    function spawn(anywhere) {
      return {
        x: anywhere ? Math.random() * w : -10,
        y: Math.random() * h,
        v: 0.5 + Math.random() * 1.1,
        c: Math.random() < 0.22 ? colA : colB,
        a: 0.18 + Math.random() * 0.45,
        life: 240 + Math.random() * 420
      };
    }

    function resize() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = canvas.clientWidth;
      h = canvas.clientHeight;
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.round(Math.min(170, (w * h) / 8000));
      parts = [];
      for (var i = 0; i < n; i++) parts.push(spawn(true));
    }

    // Úhel proudění v bodě: převládá směr zleva doprava, jemně se vlní.
    function angle(x, y) {
      return Math.sin(y * 0.006 + t * 0.004) * 0.55 + Math.cos(x * 0.004 - t * 0.003) * 0.35;
    }

    function step() {
      t++;
      ctx.globalCompositeOperation = "destination-out";
      ctx.fillStyle = "rgba(0,0,0,0.06)";
      ctx.fillRect(0, 0, w, h);
      ctx.globalCompositeOperation = "source-over";
      ctx.lineWidth = 1.1;
      ctx.lineCap = "round";
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        var ang = angle(p.x, p.y);
        var nx = p.x + Math.cos(ang) * p.v * 1.7;
        var ny = p.y + Math.sin(ang) * p.v * 1.7;
        ctx.globalAlpha = p.a;
        ctx.strokeStyle = p.c;
        ctx.beginPath();
        ctx.moveTo(p.x, p.y);
        ctx.lineTo(nx, ny);
        ctx.stroke();
        p.x = nx;
        p.y = ny;
        p.life--;
        if (p.x > w + 10 || p.y < -10 || p.y > h + 10 || p.life < 0) parts[i] = spawn(Math.random() < 0.3);
      }
      ctx.globalAlpha = 1;
      if (running) raf = requestAnimationFrame(step);
    }

    function start() {
      if (running || reduceMotion) return;
      running = true;
      raf = requestAnimationFrame(step);
    }

    function stop() {
      running = false;
      cancelAnimationFrame(raf);
    }

    resize();
    // Hned na začátku domalujeme stopy, aby scéna nebyla prázdná ani bez pohybu.
    for (var k = 0; k < 160; k++) step();

    if (reduceMotion) return;

    var visible = true;
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        visible = entries[0].isIntersecting;
        if (visible && !document.hidden) start();
        else stop();
      }).observe(canvas);
    } else {
      start();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop();
      else if (visible) start();
    });
    var resizeTimer = 0;
    window.addEventListener("resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        resize();
        for (var k = 0; k < 60; k++) step();
      }, 200);
    });
  }

  document.querySelectorAll("canvas[data-airflow]").forEach(airflow);

  // Světlo pod kurzorem na kartách
  document.querySelectorAll(".card, .project, .cs-module, .app, .feature, .contact").forEach(function (el) {
    el.addEventListener("pointermove", function (e) {
      var r = el.getBoundingClientRect();
      el.style.setProperty("--mx", e.clientX - r.left + "px");
      el.style.setProperty("--my", e.clientY - r.top + "px");
    });
    el.addEventListener("pointerleave", function () {
      el.style.removeProperty("--mx");
      el.style.removeProperty("--my");
    });
  });

  // Živý deník Ventilka na stránce middlewaru (ilustrační události)
  var log = document.getElementById("ventilek-log");
  if (log && !reduceMotion) {
    var udalosti = [
      "Nová objednávka → založena v ABŘE",
      "Platba přijata → stav Placeno, SMS zákazníkovi",
      "Faktura z ABRY → v účtu zákazníka",
      "Překlad DE · EN · PL · SK → zapsán do Shoptetu",
      "Poptávka z e-mailu → návrh nabídky v ABŘE",
      "Balík od dodavatele → na cestě, dorazí zítra",
      "Termín doručení posunut → zákazník informován",
      "Recenze → žádost odeslána zákazníkovi",
      "Změna balení v ABŘE → propsána do ceníků",
      "Nákupní cena → zapsána, bez podezřelého skoku",
      "Odkazy na webu → zkontrolováno, vše v pořádku",
      "Článek poradny → návrh čeká na schválení"
    ];
    var index = 6;
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };

    // Úvodní řádky dostanou časy posledních minut, ať deník působí aktuálně.
    var now = new Date();
    var rows = log.querySelectorAll("time");
    rows.forEach(function (el, i) {
      var d = new Date(now.getTime() - (rows.length - 1 - i) * 3 * 60000);
      el.textContent = pad(d.getHours()) + ":" + pad(d.getMinutes());
    });
    // Nejnovější nahoře
    Array.prototype.slice.call(log.children).reverse().forEach(function (li) { log.appendChild(li); });

    setInterval(function () {
      if (document.hidden) return;
      var d = new Date();
      var li = document.createElement("li");
      li.className = "is-new";
      var time = document.createElement("time");
      time.textContent = pad(d.getHours()) + ":" + pad(d.getMinutes());
      var text = document.createElement("span");
      text.textContent = udalosti[index % udalosti.length];
      var ok = document.createElement("b");
      ok.textContent = "✓";
      li.appendChild(time);
      li.appendChild(text);
      li.appendChild(ok);
      log.insertBefore(li, log.firstChild);
      index++;
      while (log.children.length > 5) log.removeChild(log.lastChild);
    }, 2600);
  }
  // ---------- ilustrace na stránkách projektů ----------

  // Košík: množství jen po celých baleních
  document.querySelectorAll("[data-stepper]").forEach(function (el) {
    if (reduceMotion) return;
    var out = el.querySelector("output");
    var step = Number(el.getAttribute("data-step")) || 1;
    var max = Number(el.getAttribute("data-max")) || step * 5;
    var unit = el.getAttribute("data-unit") || "";
    var value = step;
    setInterval(function () {
      if (document.hidden) return;
      value = value >= max ? step : value + step;
      out.textContent = value + unit;
      out.classList.remove("is-new");
      void out.offsetWidth;
      out.classList.add("is-new");
    }, 2200);
  });

  // Odpočet akční nabídky (ukázkový, po doběhnutí začne znovu)
  document.querySelectorAll("[data-countdown]").forEach(function (el) {
    var hours = Number(el.getAttribute("data-hours")) || 48;
    var end = Date.now() + hours * 3600 * 1000;
    var parts = {
      d: el.querySelector("[data-d]"),
      h: el.querySelector("[data-h]"),
      m: el.querySelector("[data-m]"),
      s: el.querySelector("[data-s]"),
    };
    function pad2(n) { return n < 10 ? "0" + n : String(n); }
    function tick() {
      var left = Math.max(0, end - Date.now());
      if (left === 0) end = Date.now() + hours * 3600 * 1000;
      var sec = Math.floor(left / 1000);
      parts.d.textContent = String(Math.floor(sec / 86400));
      parts.h.textContent = pad2(Math.floor((sec % 86400) / 3600));
      parts.m.textContent = pad2(Math.floor((sec % 3600) / 60));
      parts.s.textContent = pad2(sec % 60);
    }
    tick();
    if (!reduceMotion) setInterval(tick, 1000);
  });

  // Kampaň se sama pozastaví, když nabídka skončí
  document.querySelectorAll("[data-campaign]").forEach(function (el) {
    if (reduceMotion) return;
    var text = el.querySelector("[data-campaign-text]");
    var on = el.getAttribute("data-on");
    var off = el.getAttribute("data-off");
    setInterval(function () {
      if (document.hidden) return;
      var isOff = el.classList.toggle("is-off");
      text.textContent = isOff ? off : on;
    }, 3600);
  });

  // Počítadlo, které se rozběhne, když je vidět
  var counters = document.querySelectorAll("[data-count]");
  if (counters.length && !reduceMotion && "IntersectionObserver" in window) {
    var fmt = function (n) { return Math.round(n).toLocaleString("cs-CZ"); };
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        var el = entry.target;
        var target = Number(el.getAttribute("data-count"));
        var start = performance.now();
        var dur = 1600;
        (function frame(now) {
          var t = Math.min(1, (now - start) / dur);
          var eased = 1 - Math.pow(1 - t, 3);
          el.textContent = fmt(target * eased);
          if (t < 1) requestAnimationFrame(frame);
        })(start);
      });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { io.observe(el); });
  }
})();

// Měření návštěvnosti (Google Analytics 4), jen se souhlasem návštěvníka.
// Bez souhlasu se nic nenačte a žádné cookies nevzniknou.
(function () {
  var GA_ID = "G-2QMREX9VCJ";
  var KEY = "zs-souhlas-mereni";
  var bar = null;

  function read() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function write(v) {
    try { localStorage.setItem(KEY, v); } catch (e) { /* prohlížeč úložiště nepovolil */ }
  }

  function loadGA() {
    if (window.__zsGa) return;
    window.__zsGa = true;
    window["ga-disable-" + GA_ID] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", {
      analytics_storage: "granted",
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied"
    });
    window.gtag("js", new Date());
    window.gtag("config", GA_ID);
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
  }

  function stopGA() {
    window["ga-disable-" + GA_ID] = true;
    if (window.gtag) window.gtag("consent", "update", { analytics_storage: "denied" });
    // smazat cookies Google Analytics (_ga, _ga_…)
    var host = location.hostname;
    var domains = ["", host, "." + host, "." + host.replace(/^www\./, "")];
    document.cookie.split(";").forEach(function (c) {
      var name = c.split("=")[0].trim();
      if (!/^_ga/.test(name)) return;
      domains.forEach(function (d) {
        document.cookie = name + "=; Max-Age=0; path=/" + (d ? "; domain=" + d : "");
      });
    });
  }

  function hide() {
    if (bar) { bar.remove(); bar = null; }
  }

  function decide(v) {
    write(v);
    hide();
    if (v === "ano") loadGA(); else stopGA();
  }

  function show() {
    if (bar) return;
    bar = document.createElement("div");
    bar.className = "consent";
    bar.setAttribute("role", "region");
    bar.setAttribute("aria-label", "Souhlas s měřením návštěvnosti");
    bar.innerHTML =
      '<p class="consent__text">Rád bych věděl, kolik lidí web čte a co je zajímá. ' +
      "S vaším souhlasem k tomu použiju Google Analytics, které ukládá cookies. " +
      "Bez souhlasu se nic neměří.</p>" +
      '<div class="consent__actions">' +
      '<button type="button" class="btn btn--primary" data-consent="ano">Souhlasím</button>' +
      '<button type="button" class="btn btn--ghost" data-consent="ne">Nesouhlasím</button>' +
      "</div>";
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("[data-consent]");
      if (b) decide(b.getAttribute("data-consent"));
    });
    document.body.appendChild(bar);
  }

  // odkaz v patičce: znovu otevře volbu
  document.querySelectorAll("[data-consent-open]").forEach(function (el) {
    el.hidden = false;
    el.addEventListener("click", show);
  });

  // kliknutí na e-mail nebo telefon = poptávka (měří se jen se souhlasem)
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="mailto:"], a[href^="tel:"]');
    if (!a || !window.__zsGa || !window.gtag) return;
    window.gtag("event", "generate_lead", {
      method: a.getAttribute("href").indexOf("tel:") === 0 ? "telefon" : "e-mail"
    });
  });

  var stav = read();
  if (stav === "ano") loadGA();
  else if (stav !== "ne") show();
})();
