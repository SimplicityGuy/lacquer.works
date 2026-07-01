# Lacquer Works Studio Landing Page — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a single static `index.html` holding page for Lacquer Works Studio — the exact design system/structure from the source prompt plus a vinyl-grooves dynamic background behind the hero.

**Architecture:** One self-contained `index.html` (inline `<style>` + `<script>`, no build, no external JS libs). The logo mark is Canvas-rendered via a verbatim `drawMark` function, layered as two stacked canvases so the mark's asymmetric parts orbit while text stays upright. A separate hero-background canvas runs a `requestAnimationFrame` grooves animation. Fonts from Google Fonts; all mark/text-dependent code runs inside `document.fonts.ready`.

**Tech Stack:** HTML5, CSS3 (custom properties), vanilla ES2015+ JS, Canvas 2D API. Verification via local static server + Playwright MCP.

## Global Constraints

- Single file `index.html` at repo root. No frameworks, no build step, no external JS libraries. Must work over `file://`.
- Fonts: `<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Anybody:ital,wght@0,200;1,200&display=swap" rel="stylesheet">`.
- Palette (CSS custom properties, exact): `--bg:#04030a; --bg2:#09071a; --bg3:#0d0b20; --violet:#9d5cff; --purple:#c084fc; --magenta:#f472b6; --mid:#2d1b6e; --faint:#1c1040; --near-white:#f0eaff; --dimmed:#c4b0e8; --url-color:#c084fc;`
- All borders `0.5px` (buttons `0.8px`). `border-radius: 0` everywhere. No box-shadows. No gradients.
- `drawMark` is copied **verbatim** from `lacquer-works-claude-code-prompt.md` / `design/lacquer-works-assets.html` — do not alter its drawing logic.
- All mark/arc-text drawing runs inside `document.fonts.ready.then(...)`.
- Copy is exact: hero copy `// building at the intersection of music, data, and AI`; button `Get in touch →` → `mailto:hello@lacquer.works`; projects discogsography / cronduit / GRUVAX; footer `Lacquer Works Studio · MMXXV`.
- Background: vinyl grooves, **Present** intensity (`intensity = 1.7`), behind the **hero only**.
- Honor `prefers-reduced-motion: reduce` (no animation, static frame) and pause animation when the tab is hidden.
- Breakpoint: 768px.

## File Structure

- **Create `index.html`** (repo root) — the entire deliverable. Internal organization:
  - `<head>`: meta/SEO, fonts, one `<style>` block (tokens, reset, per-section CSS).
  - `<body>`: `nav`, `section.hero` (bg canvas + two-layer mark + wordmark), `section.about`, `section.projects`, `footer`.
  - one `<script>`: `drawMark` (verbatim); grooves background module; mark/favicon setup; boot in `document.fonts.ready`.
- **Create `.gitignore`** — ignore local verification artifacts (`*.png` screenshots, `.playwright-mcp/`).

### Verification harness (used by every task)

Start a server once from repo root:

```bash
cd /Users/Robert/Code/public/lacquer.works && python3 -m http.server 8731 >/tmp/claude-501/lw-index.log 2>&1 &
```

Then use the **Playwright MCP**: `browser_navigate` to `http://localhost:8731/`, `browser_evaluate` for assertions, `browser_take_screenshot` for visual confirmation, `browser_console_messages` (level `error`) to confirm no errors (a missing `favicon.ico` 404 is acceptable until Task 8). Re-navigate after each edit to pick up changes.

---

### Task 1: Scaffold — head, tokens, and empty section skeleton

**Files:**
- Create: `index.html`
- Create: `.gitignore`

**Interfaces:**
- Produces: the `index.html` shell with `<style>` holding the palette tokens + reset, and empty `<nav>`, `<section class="hero">`, `<section class="about">`, `<section class="projects">`, `<footer>` elements that later tasks fill in.

- [ ] **Step 1: Write `.gitignore`**

```gitignore
# local verification artifacts
*.png
.playwright-mcp/
__pycache__/
```

- [ ] **Step 2: Write the `index.html` shell**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Lacquer Works Studio — building at the intersection of music, data, and AI.">
<meta property="og:title" content="Lacquer Works Studio">
<meta property="og:description" content="Independent engineering studio. Music + Data + AI.">
<meta property="og:url" content="https://lacquer.works">
<meta name="theme-color" content="#04030a">
<title>Lacquer Works Studio</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Anybody:ital,wght@0,200;1,200&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:#04030a; --bg2:#09071a; --bg3:#0d0b20;
    --violet:#9d5cff; --purple:#c084fc; --magenta:#f472b6;
    --mid:#2d1b6e; --faint:#1c1040;
    --near-white:#f0eaff; --dimmed:#c4b0e8; --url-color:#c084fc;
  }
  html, body { background: var(--bg); color: var(--near-white); }
  body { font-family: 'JetBrains Mono', monospace; -webkit-font-smoothing: antialiased; }
  a { color: inherit; text-decoration: none; }
</style>
</head>
<body>
  <nav></nav>
  <section class="hero"></section>
  <section class="about"></section>
  <section class="projects"></section>
  <footer></footer>
  <script>
  // drawMark + background + boot added in later tasks
  </script>
</body>
</html>
```

- [ ] **Step 3: Start the server** (see Verification harness above). Confirm it responds:

Run: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8731/`
Expected: `200`

- [ ] **Step 4: Verify in browser**

Playwright: `browser_navigate` → `http://localhost:8731/`. Then `browser_evaluate`:

```js
() => ({
  title: document.title,
  bg: getComputedStyle(document.body).backgroundColor,
  sections: ['nav','.hero','.about','.projects','footer'].map(s => !!document.querySelector(s)),
})
```

Expected: `title` = `"Lacquer Works Studio"`, `bg` = `"rgb(4, 3, 10)"`, `sections` all `true`. `browser_console_messages` level `error`: none except possibly `favicon.ico` 404.

- [ ] **Step 5: Commit**

```bash
git add index.html .gitignore
git commit -m "feat: scaffold index.html shell with design tokens"
```

---

### Task 2: Verbatim drawMark + boot + nav

**Files:**
- Modify: `index.html` (`<nav>` markup, nav CSS, `<script>`)

**Interfaces:**
- Produces: global `drawMark(canvasId, opts)` (verbatim); a rendered 48×48 `#nav-mark` canvas; the `document.fonts.ready` boot block that later tasks extend.

- [ ] **Step 1: Add the nav markup** — replace `<nav></nav>` with:

```html
<nav>
  <div class="nav-left">
    <canvas id="nav-mark" width="48" height="48"></canvas>
    <span class="nav-name">Lacquer Works</span>
  </div>
  <span class="nav-url">lacquer.works</span>
</nav>
```

- [ ] **Step 2: Add nav CSS** (inside `<style>`):

```css
  nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 50;
    display: flex; align-items: center; justify-content: space-between;
    padding: 16px 40px;
    background: rgba(4,3,10,0.92); backdrop-filter: blur(12px);
    border-bottom: 0.5px solid var(--faint);
  }
  .nav-left { display: flex; align-items: center; gap: 14px; }
  #nav-mark { display: block; }
  .nav-name { font-size: 10px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--near-white); }
  .nav-url  { font-size: 9px; letter-spacing: 0.2em; color: var(--url-color); }
```

- [ ] **Step 3: Add `drawMark` verbatim + boot** — replace the `<script>` body with the verbatim function from `design/lacquer-works-assets.html` (lines 460–604) followed by:

```js
document.fonts.ready.then(() => {
  drawMark('nav-mark', { showText: false });
});
```

Copy `drawMark` **exactly** — do not modify its drawing logic. (Full source: `design/lacquer-works-assets.html`.)

- [ ] **Step 4: Verify the nav mark renders**

Playwright `browser_navigate` then `browser_evaluate`:

```js
() => {
  const c = document.getElementById('nav-mark');
  const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data;
  let nz = 0; for (let i=0;i<d.length;i+=4) if (d[i]||d[i+1]||d[i+2]) nz++;
  return { nonZeroPixels: nz };
}
```

Expected: `nonZeroPixels` > 100 (mark drew). `browser_console_messages` error level: none (except favicon 404).

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "feat: add verbatim drawMark and nav mark"
```

---

### Task 3: Hero — two-layer rotating mark, wordmark, copy, button, fade-in

**Files:**
- Modify: `index.html` (`.hero` markup, hero CSS, boot block)

**Interfaces:**
- Consumes: `drawMark` from Task 2.
- Produces: `.hero` with a `.hero-mark-wrap` containing `#hero-mark-static` and `#hero-mark-rotor` canvases (320×340), the wordmark lockup, hero copy, and the `Get in touch` button. Boot draws both mark layers.

- [ ] **Step 1: Add hero markup** — replace `<section class="hero"></section>` with:

```html
<section class="hero">
  <div class="hero-inner">
    <div class="hero-mark-wrap">
      <canvas id="hero-mark-static" width="320" height="340"></canvas>
      <canvas id="hero-mark-rotor"  width="320" height="340"></canvas>
    </div>
    <div class="hero-text">
      <div class="wm-lacquer">Lacquer</div>
      <div class="wm-works-row">
        <div class="wm-works">Works</div>
        <div class="wm-studio">STUDIO</div>
      </div>
      <div class="wm-url">lacquer.works</div>
      <div class="hero-copy">// building at the intersection of music, data, and AI</div>
      <div><a class="hero-btn" href="mailto:hello@lacquer.works">Get in touch →</a></div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Add hero CSS** (inside `<style>`):

```css
  .hero { position: relative; min-height: 100vh; overflow: hidden; display: flex; align-items: center; justify-content: center; }
  .hero-inner {
    position: relative; z-index: 1;
    display: flex; align-items: center; gap: 80px; padding: 0 40px; max-width: 1100px;
    animation: heroIn 800ms ease-out both;
  }
  @keyframes heroIn { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: none; } }
  .hero-mark-wrap { position: relative; width: 320px; height: 340px; flex-shrink: 0; }
  .hero-mark-wrap canvas { position: absolute; inset: 0; display: block; }
  #hero-mark-rotor { animation: spin 60s linear infinite; transform-origin: 50% 55%; }
  @keyframes spin { to { transform: rotate(360deg); } }

  .wm-lacquer { font-family:'Anybody',cursive; font-weight:200; font-style:italic; font-size:64px; line-height:1; letter-spacing:-0.5px; color:var(--near-white); }
  .wm-works-row { display:flex; align-items:flex-end; }
  .wm-works  { font-family:'Anybody',cursive; font-weight:200; font-style:italic; font-size:64px; line-height:1; letter-spacing:-0.5px; color:var(--violet); }
  .wm-studio { font-size:12px; letter-spacing:0.22em; color:var(--dimmed); margin-bottom:10px; margin-left:10px; white-space:nowrap; }
  .wm-url    { font-size:9px; letter-spacing:0.2em; color:var(--url-color); text-align:right; margin-top:8px; }
  .hero-copy { margin-top:40px; font-size:13px; font-weight:300; letter-spacing:0.02em; line-height:1.8; color:var(--dimmed); }
  .hero-btn  {
    display:inline-block; margin-top:24px;
    font-size:10px; letter-spacing:0.18em; text-transform:uppercase; color:var(--near-white);
    background:transparent; border:0.8px solid var(--violet); padding:12px 24px; cursor:pointer;
    transition: background .2s, color .2s;
  }
  .hero-btn:hover { background:var(--violet); color:var(--near-white); }
  @media (prefers-reduced-motion: reduce) {
    #hero-mark-rotor { animation: none; }
    .hero-inner { animation: none; }
  }
```

- [ ] **Step 3: Add the two-layer mark draw to the boot block** — inside the existing `document.fonts.ready.then(() => { ... })`, add:

```js
  const TRANSPARENT = 'rgba(0,0,0,0)';
  // Static layer: rings + interior + waveform bars + arc text (glyphs/dots hidden)
  drawMark('hero-mark-static', {
    glyphAColor: TRANSPARENT, glyphBColor: TRANSPARENT,
    dot1Color: TRANSPARENT, dot2Color: TRANSPARENT,
  });
  // Rotating layer: only the asymmetric glyph arcs + terminal dots (everything else hidden)
  drawMark('hero-mark-rotor', {
    bg: TRANSPARENT, showText: false,
    outerColor: TRANSPARENT, grooveColor: TRANSPARENT,
    bar1Color: TRANSPARENT, bar2Color: TRANSPARENT, bar3Color: TRANSPARENT,
  });
```

- [ ] **Step 4: Verify mark layers + rotation**

Playwright `browser_navigate` then `browser_evaluate`:

```js
() => {
  const px = id => { const c=document.getElementById(id); const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data; let n=0; for(let i=0;i<d.length;i+=4) if(d[i]||d[i+1]||d[i+2]||d[i+3]) n++; return n; };
  return {
    staticPx: px('hero-mark-static'),
    rotorPx: px('hero-mark-rotor'),
    rotorAnim: getComputedStyle(document.getElementById('hero-mark-rotor')).animationName,
    lacquer: document.querySelector('.wm-lacquer').textContent,
    btnHref: document.querySelector('.hero-btn').getAttribute('href'),
  };
}
```

Expected: `staticPx` > 1000, `rotorPx` > 100 (glyphs+dots drew) and much smaller than staticPx, `rotorAnim` = `"spin"`, `lacquer` = `"Lacquer"`, `btnHref` = `"mailto:hello@lacquer.works"`.

- [ ] **Step 5: Visual check** — `browser_take_screenshot`. Confirm: complete mark (rings, waveform bars, arc text "LACQUER"/"WORKS" upright), wordmark lockup to the right, copy + button below.

- [ ] **Step 6: Commit**

```bash
git add index.html
git commit -m "feat: hero with two-layer rotating mark, wordmark, and CTA"
```

---

### Task 4: Vinyl-grooves background behind the hero

**Files:**
- Modify: `index.html` (add `#bg-canvas` to `.hero`, CSS, background module in `<script>`)

**Interfaces:**
- Consumes: `.hero` element (Task 3).
- Produces: `#bg-canvas` filling the hero at `z-index:0`; a self-running grooves animation with `intensity = 1.7`, `prefers-reduced-motion` and `visibilitychange` guards.

- [ ] **Step 1: Add the canvas** — as the first child of `.hero` (before `.hero-inner`):

```html
  <canvas id="bg-canvas"></canvas>
```

- [ ] **Step 2: Add CSS** (inside `<style>`):

```css
  #bg-canvas { position: absolute; inset: 0; width: 100%; height: 100%; z-index: 0; display: block; }
```

- [ ] **Step 3: Add the background module** — inside the `<script>`, before the `document.fonts.ready` block:

```js
// ── Vinyl-grooves hero background (Present intensity) ──
(function(){
  const cv = document.getElementById('bg-canvas');
  if (!cv) return;
  const cx = cv.getContext('2d');
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const DPR = Math.min(window.devicePixelRatio || 1, 2);
  const intensity = 1.7;                 // "Present"
  let W = 0, H = 0, running = false;

  function resize(){
    const r = cv.getBoundingClientRect();
    W = r.width; H = r.height;
    cv.width = Math.max(1, Math.round(W*DPR));
    cv.height = Math.max(1, Math.round(H*DPR));
    cx.setTransform(DPR,0,0,DPR,0,0);
  }

  function drawGrooves(t){
    cx.clearRect(0,0,W,H);
    const ccx = W*0.30, ccy = H*0.52;
    const maxR = Math.hypot(Math.max(ccx, W-ccx), Math.max(ccy, H-ccy)) + 40;
    const gap = 15;
    const waveSpeed = 0.0011 * intensity;
    cx.save();
    cx.translate(ccx, ccy);
    for (let r=gap; r<maxR; r+=gap){
      const crest = Math.max(0, Math.sin(r*0.045 - t*waveSpeed));
      const alpha = (0.045 + crest*0.16*intensity) * (1 - r/maxR*0.32);
      cx.beginPath(); cx.arc(0,0,r,0,Math.PI*2);
      cx.strokeStyle = `rgba(157,92,255,${alpha.toFixed(4)})`; cx.lineWidth = 1; cx.stroke();
    }
    cx.beginPath(); cx.arc(0,0, 58 + Math.sin(t*0.0006)*7, 0, Math.PI*2);
    cx.strokeStyle = `rgba(192,132,252,${(0.10*intensity).toFixed(4)})`; cx.lineWidth = 1; cx.stroke();
    const orbitR = Math.min(W,H)*0.20;
    const ang = -t*0.00026 * intensity;
    const dx = orbitR*Math.cos(ang), dy = orbitR*Math.sin(ang);
    cx.beginPath(); cx.moveTo(0,0); cx.lineTo(dx,dy);
    cx.strokeStyle = `rgba(157,92,255,${(0.05*intensity).toFixed(4)})`; cx.lineWidth = 0.5; cx.stroke();
    cx.beginPath(); cx.arc(dx,dy, 2.2, 0, Math.PI*2);
    cx.fillStyle = `rgba(244,114,182,${Math.min(0.85,0.55*intensity).toFixed(4)})`; cx.fill();
    cx.restore();
  }

  function frame(t){ if (!running) return; drawGrooves(t); requestAnimationFrame(frame); }
  function start(){ if (running) return; running = true; requestAnimationFrame(frame); }
  function stop(){ running = false; }

  window.addEventListener('resize', () => { resize(); if (reduceMotion) drawGrooves(0); });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop(); else if (!reduceMotion) start();
  });

  resize();
  if (reduceMotion) drawGrooves(0); else start();
})();
```

- [ ] **Step 4: Verify it animates (Present intensity)**

Playwright `browser_navigate` then `browser_evaluate`:

```js
async () => {
  const cv = document.getElementById('bg-canvas');
  const ctx = cv.getContext('2d');
  const sample = () => { const d=ctx.getImageData(0,0,cv.width,cv.height).data; let s=0,nz=0; for(let i=0;i<d.length;i+=40){ if(d[i]||d[i+1]||d[i+2]) nz++; s=(s+d[i]+d[i+1]*2+d[i+2]*3)%1e9; } return {s,nz}; };
  const a = sample(); await new Promise(r=>setTimeout(r,1200)); const b = sample();
  return { changed: a.s !== b.s, visiblePixels: a.nz, reduce: matchMedia('(prefers-reduced-motion: reduce)').matches };
}
```

Expected (normal motion): `changed` = `true`, `visiblePixels` in the tens-of-thousands (grooves fill the hero), `reduce` = `false`.

- [ ] **Step 5: Verify reduced-motion is honored** — Playwright `browser_run_code_unsafe`:

```js
async (page) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('http://localhost:8731/');
  const cv = 'document.getElementById("bg-canvas")';
  const t0 = await page.evaluate(`(()=>{const c=${cv};const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let s=0;for(let i=0;i<d.length;i+=40)s=(s+d[i])%1e9;return s;})()`);
  await page.waitForTimeout(1200);
  const t1 = await page.evaluate(`(()=>{const c=${cv};const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let s=0;for(let i=0;i<d.length;i+=40)s=(s+d[i])%1e9;return s;})()`);
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  return { staticFrame: t0 === t1, drew: t0 !== 0 };
}
```

Expected: `staticFrame` = `true` (no animation), `drew` = `true` (one frame rendered).

- [ ] **Step 6: Visual check** — reset media (Step 5 already did), `browser_navigate`, `browser_take_screenshot`. Confirm grooves halo behind the mark with the magenta orbiting dot; hero text remains fully legible above it.

- [ ] **Step 7: Commit**

```bash
git add index.html
git commit -m "feat: vinyl-grooves hero background with reduced-motion + visibility guards"
```

---

### Task 5: About strip

**Files:**
- Modify: `index.html` (`.about` markup + CSS)

**Interfaces:**
- Produces: `.about` full-width section with three bordered columns.

- [ ] **Step 1: Add markup** — replace `<section class="about"></section>` with:

```html
<section class="about">
  <div class="about-col">
    <div class="about-label">Founder &amp; Principal Engineer</div>
    <div class="about-body">VP-level engineering depth, AI practitioner, independent builder.</div>
  </div>
  <div class="about-col">
    <div class="about-label">Music + Data + AI</div>
    <div class="about-body">Tools for exploring, managing, and understanding music collections.</div>
  </div>
  <div class="about-col">
    <div class="about-label">Est. MMXXV</div>
    <div class="about-body">Lacquer Works Studio. Seattle. Open source where possible.</div>
  </div>
</section>
```

- [ ] **Step 2: Add CSS**:

```css
  .about { background: var(--bg2); display: grid; grid-template-columns: repeat(3, 1fr); border-top: 0.5px solid var(--faint); border-bottom: 0.5px solid var(--faint); }
  .about-col { padding: 40px; border-left: 0.5px solid var(--faint); }
  .about-col:first-child { border-left: none; }
  .about-label { font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--url-color); margin-bottom: 16px; }
  .about-body  { font-size: 12px; font-weight: 300; line-height: 1.8; color: var(--dimmed); }
```

- [ ] **Step 3: Verify** — `browser_navigate` then `browser_evaluate`:

```js
() => ({
  cols: document.querySelectorAll('.about-col').length,
  labels: [...document.querySelectorAll('.about-label')].map(e => e.textContent),
})
```

Expected: `cols` = `3`; `labels` = `["Founder & Principal Engineer","Music + Data + AI","Est. MMXXV"]`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: about strip"
```

---

### Task 6: Projects section

**Files:**
- Modify: `index.html` (`.projects` markup + CSS)

**Interfaces:**
- Produces: `.projects` section with `// projects` label and three project cards.

- [ ] **Step 1: Add markup** — replace `<section class="projects"></section>` with:

```html
<section class="projects">
  <div class="section-label">// projects</div>
  <div class="project-grid">
    <a class="project-card" href="#">
      <div class="project-kicker">Project</div>
      <div class="project-name">discogsography</div>
      <div class="project-desc">Vinyl collection graph. Neo4j + PostgreSQL + Discogs API.</div>
      <div class="project-tags"><span>python</span><span>docker</span><span>graph</span></div>
      <div class="project-arrow">→</div>
    </a>
    <a class="project-card" href="#">
      <div class="project-kicker">Project</div>
      <div class="project-name">cronduit</div>
      <div class="project-desc">Docker-native cron scheduler.</div>
      <div class="project-tags"><span>docker</span><span>scheduling</span><span>open source</span></div>
      <div class="project-arrow">→</div>
    </a>
    <a class="project-card" href="#">
      <div class="project-kicker">Project</div>
      <div class="project-name">GRUVAX</div>
      <div class="project-desc">AI music file organiser. Anthropic Batch API + prompt caching.</div>
      <div class="project-tags"><span>python</span><span>AI</span><span>music</span></div>
      <div class="project-arrow">→</div>
    </a>
  </div>
</section>
```

- [ ] **Step 2: Add CSS**:

```css
  .projects { padding: 96px 40px; max-width: 1100px; margin: 0 auto; }
  .section-label { font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase; color: var(--url-color); margin-bottom: 24px; }
  .project-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px; }
  .project-card { background: var(--bg); border: 0.5px solid var(--faint); padding: 24px; display: flex; flex-direction: column; transition: border-color .2s; }
  .project-card:hover { border-color: var(--mid); }
  .project-kicker { font-size: 8px; letter-spacing: 0.18em; text-transform: uppercase; color: #4a3880; margin-bottom: 12px; }
  .project-name { font-family:'Anybody',cursive; font-weight:200; font-style:italic; font-size:22px; color: var(--purple); margin-bottom: 8px; }
  .project-desc { font-size: 11px; font-weight: 300; line-height: 1.7; color: var(--dimmed); margin-bottom: 16px; }
  .project-tags { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
  .project-tags span { font-size: 8px; letter-spacing: 0.12em; text-transform: uppercase; color: var(--purple); border: 0.5px solid var(--mid); padding: 4px 10px; }
  .project-arrow { margin-top: auto; color: var(--violet); font-size: 14px; }
```

- [ ] **Step 3: Verify** — `browser_navigate` then `browser_evaluate`:

```js
() => ({
  cards: document.querySelectorAll('.project-card').length,
  names: [...document.querySelectorAll('.project-name')].map(e => e.textContent),
  tagsFirst: [...document.querySelectorAll('.project-card:first-child .project-tags span')].map(e => e.textContent),
})
```

Expected: `cards` = `3`; `names` = `["discogsography","cronduit","GRUVAX"]`; `tagsFirst` = `["python","docker","graph"]`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: projects section with three cards"
```

---

### Task 7: Footer

**Files:**
- Modify: `index.html` (`footer` markup + CSS)

**Interfaces:**
- Produces: minimal `footer` with studio line and URL.

- [ ] **Step 1: Add markup** — replace `<footer></footer>` with:

```html
<footer>
  <span>Lacquer Works Studio · MMXXV</span>
  <span>lacquer.works</span>
</footer>
```

- [ ] **Step 2: Add CSS**:

```css
  footer { display: flex; align-items: center; justify-content: space-between; padding: 24px 40px; background: var(--bg); border-top: 0.5px solid var(--faint); font-size: 9px; letter-spacing: 0.12em; color: #4a3880; }
```

- [ ] **Step 3: Verify** — `browser_evaluate`:

```js
() => [...document.querySelectorAll('footer span')].map(e => e.textContent)
```

Expected: `["Lacquer Works Studio · MMXXV","lacquer.works"]`.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: footer"
```

---

### Task 8: Favicon generated from the mark

**Files:**
- Modify: `index.html` (`<head>` link, boot block)

**Interfaces:**
- Consumes: `drawMark` (Task 2).
- Produces: a runtime-generated `<link rel="icon">` whose data URL is the mark drawn on a 64×64 offscreen canvas.

- [ ] **Step 1: Add an icon link to `<head>`** (after the `<title>`):

```html
<link id="favicon" rel="icon" type="image/png" href="data:,">
```

- [ ] **Step 2: Generate it in the boot block** — inside `document.fonts.ready.then(...)`, after the mark draws, add:

```js
  const fav = document.createElement('canvas');
  fav.id = 'favicon-src'; fav.width = 64; fav.height = 64;
  fav.style.display = 'none'; document.body.appendChild(fav);
  drawMark('favicon-src', {});
  document.getElementById('favicon').href = fav.toDataURL('image/png');
```

- [ ] **Step 3: Verify** — `browser_navigate` then `browser_evaluate`:

```js
() => { const h = document.getElementById('favicon').href; return { isPng: h.startsWith('data:image/png;base64,'), len: h.length }; }
```

Expected: `isPng` = `true`, `len` > 500.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: generate favicon from the logo mark"
```

---

### Task 9: Responsive (≤768px)

**Files:**
- Modify: `index.html` (append a media query to `<style>`)

**Interfaces:**
- Produces: single-column layouts and mobile-sized mark at ≤768px.

- [ ] **Step 1: Add the media query** (end of `<style>`):

```css
  @media (max-width: 768px) {
    nav { padding: 14px 20px; }
    .nav-url { display: none; }
    .hero-inner { flex-direction: column; gap: 32px; text-align: center; padding: 100px 20px 60px; }
    .hero-mark-wrap { width: 220px; height: 234px; }
    #hero-mark-static, #hero-mark-rotor { width: 220px; height: 234px; }
    .wm-lacquer, .wm-works { font-size: 44px; }
    .wm-url { text-align: center; }
    .about { grid-template-columns: 1fr; }
    .about-col { border-left: none; border-top: 0.5px solid var(--faint); }
    .about-col:first-child { border-top: none; }
    .projects { padding: 64px 20px; }
    .project-grid { grid-template-columns: 1fr; }
    footer { padding: 20px; }
  }
```

Note: the mark canvases keep their 320×340 backing resolution; the media query scales their CSS display size to 220px so the Canvas art stays crisp.

- [ ] **Step 2: Verify at mobile width** — Playwright `browser_resize` to `375 × 800`, `browser_navigate`, then `browser_evaluate`:

```js
() => ({
  heroDir: getComputedStyle(document.querySelector('.hero-inner')).flexDirection,
  aboutCols: getComputedStyle(document.querySelector('.about')).gridTemplateColumns.split(' ').length,
  projCols: getComputedStyle(document.querySelector('.project-grid')).gridTemplateColumns.split(' ').length,
  navUrl: getComputedStyle(document.querySelector('.nav-url')).display,
})
```

Expected: `heroDir` = `"column"`, `aboutCols` = `1`, `projCols` = `1`, `navUrl` = `"none"`.

- [ ] **Step 3: Visual check** — `browser_take_screenshot` at 375px (confirm stacked, centered) and after `browser_resize` back to `1440 × 900` (confirm desktop intact).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: responsive layout at 768px breakpoint"
```

---

### Task 10: Full-page verification pass

**Files:**
- No code changes unless a defect is found.

- [ ] **Step 1: Console-clean at desktop** — `browser_resize` `1440×900`, `browser_navigate`, `browser_console_messages` level `error`. Expected: **zero** errors (the generated favicon removes the earlier 404).

- [ ] **Step 2: Full-page screenshot** — `browser_take_screenshot` with `fullPage: true`. Confirm all five sections present, spacing correct, palette consistent, no rounded corners / shadows / gradients.

- [ ] **Step 3: `file://` smoke test** — open `index.html` directly (no server) in a browser and confirm it renders (fonts may differ offline; layout/mark must still work). Note result.

- [ ] **Step 4: Spec cross-check** — re-read `docs/superpowers/specs/2026-06-30-lacquer-works-landing-design.md` §§4–8 and confirm each requirement is present in the page. Fix any gap (new commit).

- [ ] **Step 5: Final commit (if any fixes)**

```bash
git add index.html
git commit -m "fix: address verification findings"
```

---

## Self-Review

**Spec coverage:**
- §3 constraints → Task 1 (tokens, fonts, no-radius reset) + Global Constraints.
- §4 structure: nav → Task 2; hero → Task 3; about → Task 5; projects → Task 6; footer → Task 7; meta/SEO → Task 1.
- §5 grooves background (Present, behind hero) → Task 4.
- §6.1 rotation (glyphs+dots orbit, text/rings static) → Task 3 (two-layer) ; §6.2 reduced-motion → Tasks 3 (CSS) + 4 (JS) ; §6.3 favicon → Task 8 ; §6.4 visibility pause → Task 4.
- §7 architecture (single file, focused units) → all tasks. §8 responsive → Task 9. §9 verification → per-task steps + Task 10.

**Placeholder scan:** project card links use `#` — intentional per spec (GitHub links not yet available), not a plan placeholder. No TBD/TODO; all steps carry concrete code/commands.

**Type/name consistency:** canvas IDs consistent across tasks — `nav-mark` (T2), `hero-mark-static` / `hero-mark-rotor` (T3), `bg-canvas` (T4), `favicon-src` + `favicon` link (T8). `drawMark(canvasId, opts)` signature used identically everywhere. `intensity = 1.7` matches spec §5 "Present". `transform-origin: 50% 55%` matches the mark's `cy = H/2 + H*0.05`.
