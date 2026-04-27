/* ============================================================
   animations.js  —  plug-and-play animation toolkit
   Usage: <script src="animations.js"></script>
   Then call any function below, or use data-attributes.
   ============================================================ */


/* ============================================================
   1.  TYPING EFFECT
   ============================================================
   QUICK START (auto-init via HTML attribute):
     <h1 data-type='["Hello!", "Welcome.", "Let'\''s build."]'></h1>

   OR call manually:
     typewriter({
       el:        document.getElementById("my-heading"),
       phrases:   ["Hello!", "Welcome.", "Let's build."],
       typeSpeed: 80,       // ms per character when typing
       eraseSpeed: 40,      // ms per character when erasing
       pauseAfter: 1800,    // ms to wait before erasing
       pauseBefore: 400,    // ms to wait before typing next phrase
       loop:      true,     // false = stop after all phrases typed once
       cursor:    true,     // show blinking cursor
       cursorChar: "|",     // cursor character  e.g. "|", "_", "▋"
     });
   ============================================================ */

function typewriter(opts = {}) {
  const cfg = {
    el:          opts.el          || document.querySelector("[data-type]"),
    phrases:     opts.phrases     || ["Change me!"],
    typeSpeed:   opts.typeSpeed   || 80,
    eraseSpeed:  opts.eraseSpeed  || 40,
    pauseAfter:  opts.pauseAfter  || 1800,
    pauseBefore: opts.pauseBefore || 400,
    loop:        opts.loop        !== false,
    cursor:      opts.cursor      !== false,
    cursorChar:  opts.cursorChar  || "|",
  };

  if (!cfg.el) return;

  // inject cursor span once
  let cursorEl = null;
  if (cfg.cursor) {
    cursorEl = document.createElement("span");
    cursorEl.className = "tw-cursor";
    cursorEl.textContent = cfg.cursorChar;
    cursorEl.style.cssText = "animation:tw-blink 1s step-end infinite; margin-left:2px;";
    cfg.el.after(cursorEl);
    if (!document.getElementById("tw-style")) {
      const s = document.createElement("style");
      s.id = "tw-style";
      s.textContent = "@keyframes tw-blink{0%,100%{opacity:1}50%{opacity:0}}";
      document.head.appendChild(s);
    }
  }

  let pIdx = 0, cIdx = 0;

  function type() {
    const phrase = cfg.phrases[pIdx];
    cfg.el.textContent = phrase.slice(0, cIdx + 1);
    cIdx++;
    if (cIdx < phrase.length) {
      setTimeout(type, cfg.typeSpeed);
    } else {
      if (cfg.loop || pIdx < cfg.phrases.length - 1) {
        setTimeout(erase, cfg.pauseAfter);
      }
    }
  }

  function erase() {
    cfg.el.textContent = cfg.el.textContent.slice(0, -1);
    if (cfg.el.textContent.length > 0) {
      setTimeout(erase, cfg.eraseSpeed);
    } else {
      pIdx = (pIdx + 1) % cfg.phrases.length;
      cIdx = 0;
      setTimeout(type, cfg.pauseBefore);
    }
  }

  type();
}

// auto-init any [data-type] elements on page load
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-type]").forEach(el => {
    try {
      const phrases = JSON.parse(el.getAttribute("data-type"));
      typewriter({ el, phrases });
    } catch (e) {
      console.warn("animations.js: invalid JSON in data-type on", el);
    }
  });
});


/* ============================================================
   2.  SCROLL REVEAL
   ============================================================
   QUICK START (auto-init via HTML class):
     <div class="reveal">I fade in on scroll</div>
     <div class="reveal-left">I slide from the left</div>
     <div class="reveal-right">I slide from the right</div>
     <div class="reveal-pop">I pop in</div>
     <div class="reveal" data-delay="200">I fade in with 200ms delay</div>

   OR call manually:
     scrollReveal({
       selector:  ".my-class",     // CSS selector to watch
       animation: "fade",          // "fade" | "left" | "right" | "pop" | "zoom"
       threshold: 0.15,            // 0–1, how much of element must be visible
       duration:  600,             // ms for the transition
       distance:  "28px",          // how far elements travel (fade/slide)
       once:      true,            // false = re-animate every time it enters view
     });
   ============================================================ */

function scrollReveal(opts = {}) {
  const cfg = {
    selector:  opts.selector  || ".reveal",
    animation: opts.animation || "fade",
    threshold: opts.threshold || 0.15,
    duration:  opts.duration  || 600,
    distance:  opts.distance  || "28px",
    once:      opts.once      !== false,
  };

  const transforms = {
    fade:  `translateY(${cfg.distance})`,
    left:  `translateX(-${cfg.distance})`,
    right: `translateX(${cfg.distance})`,
    pop:   "scale(0.88)",
    zoom:  "scale(0.75)",
  };

  const hidden = transforms[cfg.animation] || transforms.fade;

  const styleId = "sr-style-" + cfg.animation;
  if (!document.getElementById(styleId)) {
    const s = document.createElement("style");
    s.id = styleId;
    s.textContent = `
      .sr-hidden-${cfg.animation} {
        opacity: 0;
        transform: ${hidden};
        transition: opacity ${cfg.duration}ms ease, transform ${cfg.duration}ms cubic-bezier(0.22,1,0.36,1);
      }
      .sr-visible-${cfg.animation} {
        opacity: 1 !important;
        transform: none !important;
      }
    `;
    document.head.appendChild(s);
  }

  const els = document.querySelectorAll(cfg.selector);
  els.forEach((el, i) => {
    el.classList.add(`sr-hidden-${cfg.animation}`);
    const delay = el.dataset.delay || 0;
    if (delay) el.style.transitionDelay = delay + "ms";
  });

  const obs = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add(`sr-visible-${cfg.animation}`);
        if (cfg.once) obs.unobserve(entry.target);
      } else if (!cfg.once) {
        entry.target.classList.remove(`sr-visible-${cfg.animation}`);
      }
    });
  }, { threshold: cfg.threshold });

  els.forEach(el => obs.observe(el));
}

// auto-init common classes
document.addEventListener("DOMContentLoaded", () => {
  const presets = [
    { selector: ".reveal",       animation: "fade"  },
    { selector: ".reveal-left",  animation: "left"  },
    { selector: ".reveal-right", animation: "right" },
    { selector: ".reveal-pop",   animation: "pop"   },
    { selector: ".reveal-zoom",  animation: "zoom"  },
  ];
  presets.forEach(p => {
    if (document.querySelector(p.selector)) scrollReveal(p);
  });
});


/* ============================================================
   3.  SCROLL-LINKED BACKGROUND
   ============================================================
   QUICK START:
     scrollBackground({
       target: document.body,      // element whose bg changes
       colors: ["#e8f4ff", "#fff0e8", "#f0ffe8"],  // colors to shift through
       property: "background",     // CSS property to change
     });

   Or for parallax (element moves slower than scroll):
     parallax({
       el: document.getElementById("hero-img"),
       speed: 0.4,    // 0 = no move, 1 = normal scroll, 0.5 = half speed
     });
   ============================================================ */

function scrollBackground(opts = {}) {
  const cfg = {
    target:   opts.target   || document.body,
    colors:   opts.colors   || ["#ffffff", "#e8f4ff", "#f0fff4"],
    property: opts.property || "background",
  };

  function hexToRgb(hex) {
    const r = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return r ? [parseInt(r[1],16), parseInt(r[2],16), parseInt(r[3],16)] : [255,255,255];
  }

  function lerp(a, b, t) {
    const ca = hexToRgb(a), cb = hexToRgb(b);
    return `rgb(${Math.round(ca[0]+(cb[0]-ca[0])*t)},${Math.round(ca[1]+(cb[1]-ca[1])*t)},${Math.round(ca[2]+(cb[2]-ca[2])*t)})`;
  }

  function update() {
    const scrolled = window.scrollY;
    const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
    const progress = maxScroll > 0 ? Math.min(scrolled / maxScroll, 1) : 0;

    const segments = cfg.colors.length - 1;
    const scaled   = progress * segments;
    const segIdx   = Math.min(Math.floor(scaled), segments - 1);
    const t        = scaled - segIdx;

    cfg.target.style[cfg.property] = lerp(cfg.colors[segIdx], cfg.colors[segIdx + 1], t);
  }

  window.addEventListener("scroll", update, { passive: true });
  update(); // set initial color
}

function parallax(opts = {}) {
  const cfg = {
    el:    opts.el    || null,
    speed: opts.speed || 0.4,   // 0–1
  };
  if (!cfg.el) return;

  window.addEventListener("scroll", () => {
    const offset = window.scrollY * (1 - cfg.speed);
    cfg.el.style.transform = `translateY(${offset}px)`;
  }, { passive: true });
}


/* ============================================================
   4.  PAGE TRANSITION
   ============================================================
   Wrap each "page" in a container and call pageTransition()
   to fade/slide between them.

   QUICK START:
     HTML:
       <div id="page-a" class="page active">...content A...</div>
       <div id="page-b" class="page">...content B...</div>
       <button onclick="showPage('page-b')">Go to B</button>

     JS:
       pageTransition();   // call once to set up styles

       // then use:
       showPage("page-b");          // default: "fade"
       showPage("page-b", "slide"); // options: "fade" | "slide" | "zoom"

   ============================================================ */

function pageTransition(opts = {}) {
  const cfg = {
    duration: opts.duration || 350,  // ms
  };

  if (!document.getElementById("pt-style")) {
    const s = document.createElement("style");
    s.id = "pt-style";
    s.textContent = `
      .page { display: none; }
      .page.active { display: block; }

      @keyframes pt-fade-in  { from{opacity:0} to{opacity:1} }
      @keyframes pt-fade-out { from{opacity:1} to{opacity:0} }

      @keyframes pt-slide-in  { from{opacity:0;transform:translateX(40px)} to{opacity:1;transform:none} }
      @keyframes pt-slide-out { from{opacity:1;transform:none} to{opacity:0;transform:translateX(-40px)} }

      @keyframes pt-zoom-in  { from{opacity:0;transform:scale(0.93)} to{opacity:1;transform:none} }
      @keyframes pt-zoom-out { from{opacity:1;transform:none} to{opacity:0;transform:scale(1.05)} }
    `;
    document.head.appendChild(s);
  }

  window._ptDuration = cfg.duration;
}

function showPage(targetId, effect = "fade") {
  const duration = window._ptDuration || 350;
  const current  = document.querySelector(".page.active");
  const next     = document.getElementById(targetId);
  if (!next || current === next) return;

  current.style.animation = `pt-${effect}-out ${duration}ms ease forwards`;

  setTimeout(() => {
    current.classList.remove("active");
    current.style.animation = "";
    next.classList.add("active");
    next.style.animation = `pt-${effect}-in ${duration}ms ease forwards`;
    setTimeout(() => next.style.animation = "", duration);
  }, duration);
}


/* ============================================================
   5.  STAGGER CHILDREN  (bonus)
   ============================================================
   Animate a list of children one by one on scroll.

   QUICK START:
     <ul data-stagger>
       <li>Item one</li>
       <li>Item two</li>
       <li>Item three</li>
     </ul>

   OR manually:
     staggerReveal({
       parent:    document.getElementById("my-list"),
       staggerMs: 80,       // delay between each child
       animation: "fade",   // same options as scrollReveal
     });
   ============================================================ */

function staggerReveal(opts = {}) {
  const cfg = {
    parent:    opts.parent    || null,
    staggerMs: opts.staggerMs || 80,
    animation: opts.animation || "fade",
    threshold: opts.threshold || 0.1,
    duration:  opts.duration  || 500,
    distance:  opts.distance  || "20px",
  };
  if (!cfg.parent) return;

  Array.from(cfg.parent.children).forEach((child, i) => {
    child.dataset.delay = i * cfg.staggerMs;
  });

  // reuse scrollReveal — give each child a unique temp class
  const uid = "sg-" + Math.random().toString(36).slice(2, 7);
  cfg.parent.querySelectorAll(":scope > *").forEach(c => c.classList.add(uid));
  scrollReveal({ ...cfg, selector: "." + uid });
}

// auto-init [data-stagger]
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-stagger]").forEach(parent => {
    staggerReveal({ parent });
  });
});
