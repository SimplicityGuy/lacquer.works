# Lacquer Works Studio — Landing Page
## Claude Code Prompt

---

## Brief

Build a single-page placeholder / holding page for **Lacquer Works Studio** at `lacquer.works`. This is the holding company for an independent engineer and AI practitioner who builds tools at the intersection of **music, data, and AI**. The page is not a full product site — it is a considered, atmospheric landing page that establishes identity and signals what the studio is about. Think: 4AD records meets Teenage Engineering. Dark, precise, a little mysterious.

---

## Tech Stack

- **Plain HTML + CSS + Vanilla JS** — no frameworks, no build step
- **Single file**: `index.html`
- Fonts loaded from Google Fonts (already specified below)
- Canvas API for the logo mark (code provided below — copy exactly)
- No external JS libraries
- Must work without a server (file://) and deploy as static HTML to any host

---

## Design System

### Palette
```css
--bg:         #04030a;   /* page ground */
--bg2:        #09071a;   /* card / section surface */
--bg3:        #0d0b20;   /* raised surface */
--violet:     #9d5cff;   /* primary accent */
--purple:     #c084fc;   /* secondary accent */
--magenta:    #f472b6;   /* highlight / terminal dot */
--mid:        #2d1b6e;   /* groove ring / subtle border */
--faint:      #1c1040;   /* hairline borders */
--near-white: #f0eaff;   /* primary text */
--dimmed:     #c4b0e8;   /* secondary text / STUDIO label */
--url-color:  #c084fc;   /* URLs, labels, utility text */
```

### Typography
Load from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500&family=Anybody:ital,wght@0,200;1,200&display=swap" rel="stylesheet">
```

| Role | Font | Size | Weight | Style | Tracking |
|---|---|---|---|---|---|
| Display name | Anybody | 64–80px | 200 | italic | −0.5px |
| Section heading | Anybody | 28–36px | 200 | italic | 0 |
| Project name | Anybody | 22px | 200 | italic | 0 |
| Nav / label | JetBrains Mono | 9px | 400 | normal | 0.18em + uppercase |
| Body | JetBrains Mono | 12–13px | 300 | normal | 0.02em · line-height 1.8 |
| URL / utility | JetBrains Mono | 9px | 400 | normal | 0.2em |
| STUDIO descriptor | JetBrains Mono | 12px | 400 | normal | 0.22em |

### Spacing (8px base grid)
```
xs:  4px   sm:  8px   md: 16px   lg: 24px
xl: 40px  2xl: 64px  3xl: 96px  4xl: 128px
```

### Borders & Surfaces
- All borders: `0.5px solid` — never 1px
- Card border: `var(--faint)` (`#1c1040`)
- Raised border: `var(--mid)` (`#2d1b6e`)
- No border-radius anywhere — all corners are sharp (0px)
- No box shadows

### Buttons
```css
/* Primary outline */
border: 0.8px solid var(--violet);
color: var(--near-white);
background: transparent;
font-family: 'JetBrains Mono', monospace;
font-size: 10px;
letter-spacing: 0.18em;
text-transform: uppercase;
padding: 12px 24px;

/* On hover */
background: var(--violet);
color: var(--near-white);
```

---

## Logo Mark — Canvas API

The mark is drawn with JavaScript on a `<canvas>` element. **Copy this function exactly** — it is the production-locked version of the Lacquer Works mark.

```javascript
function drawMark(canvasId, opts) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width;
  const H = canvas.height;
  const bg = opts.bg || '#04030a';

  const o = Object.assign({
    cx: W / 2,
    cy: H / 2 + H * 0.05,
    rOuter:  W * 0.36,
    rGroove: W * 0.29,
    rFill:   W * 0.26,
    rGlyphA: W * 0.21,
    rGlyphB: W * 0.14,
    rText:   W * 0.325,
    barW:    W * 0.15,
    barOff:  W * 0.046,
    dotA:    W * 0.019,
    dotB:    W * 0.015,
    fontSize:    Math.max(6, Math.round(W * 0.032)),
    showText:    W >= 80,
    outerColor:  '#9d5cff',
    grooveColor: '#2d1b6e',
    glyphAColor: '#c084fc',
    glyphBColor: '#2d1b6e',
    bar1Color:   '#c084fc',
    bar2Color:   '#f472b6',
    bar3Color:   '#c084fc',
    dot1Color:   '#f472b6',
    dot2Color:   '#9d5cff',
    textTopColor:'#c084fc',
    textBotColor:'#9d5cff',
  }, opts);

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  // outer ring
  ctx.beginPath();
  ctx.arc(o.cx, o.cy, o.rOuter, 0, Math.PI * 2);
  ctx.strokeStyle = o.outerColor;
  ctx.lineWidth = Math.max(0.8, W * 0.009);
  ctx.stroke();

  // groove ring
  ctx.beginPath();
  ctx.arc(o.cx, o.cy, o.rGroove, 0, Math.PI * 2);
  ctx.strokeStyle = o.grooveColor;
  ctx.lineWidth = Math.max(0.5, W * 0.004);
  ctx.stroke();

  // interior fill
  ctx.beginPath();
  ctx.arc(o.cx, o.cy, o.rFill, 0, Math.PI * 2);
  ctx.fillStyle = bg;
  ctx.fill();

  // outer glyph arc (310deg, gap at bottom-right ~50deg)
  const gapStart = Math.PI * 50 / 180;
  ctx.beginPath();
  ctx.arc(o.cx, o.cy, o.rGlyphA, gapStart, 0, false);
  ctx.strokeStyle = o.glyphAColor;
  ctx.lineWidth = Math.max(0.8, W * 0.009);
  ctx.lineCap = 'round';
  ctx.stroke();

  // inner glyph arc (280deg)
  ctx.beginPath();
  ctx.arc(o.cx, o.cy, o.rGlyphB, Math.PI * 65/180, Math.PI * 345/180, false);
  ctx.strokeStyle = o.glyphBColor;
  ctx.lineWidth = Math.max(0.5, W * 0.005);
  ctx.lineCap = 'round';
  ctx.stroke();

  // waveform bars
  const bx = o.cx - o.barW * 0.35;
  const by = o.cy;
  const lw = Math.max(0.8, W * 0.01);
  ctx.lineCap = 'round';

  ctx.beginPath(); ctx.moveTo(bx, by - o.barOff); ctx.lineTo(bx + o.barW, by - o.barOff);
  ctx.strokeStyle = o.bar1Color; ctx.lineWidth = lw; ctx.stroke();

  ctx.beginPath(); ctx.moveTo(bx + o.barW * 0.18, by); ctx.lineTo(bx + o.barW * 1.18, by);
  ctx.strokeStyle = o.bar2Color; ctx.lineWidth = lw; ctx.stroke();

  ctx.beginPath(); ctx.moveTo(bx, by + o.barOff); ctx.lineTo(bx + o.barW * 0.82, by + o.barOff);
  ctx.strokeStyle = o.bar3Color; ctx.lineWidth = lw; ctx.stroke();

  // terminal dots
  ctx.beginPath();
  ctx.arc(o.cx + o.rGlyphA, o.cy, o.dotA, 0, Math.PI * 2);
  ctx.fillStyle = o.dot1Color; ctx.fill();

  ctx.beginPath();
  ctx.arc(
    o.cx + o.rGlyphA * Math.cos(gapStart),
    o.cy + o.rGlyphA * Math.sin(gapStart),
    o.dotB, 0, Math.PI * 2
  );
  ctx.fillStyle = o.dot2Color; ctx.fill();

  // arc text — letter by letter
  if (!o.showText) return;
  const fs = o.fontSize;
  ctx.font = `${fs}px 'JetBrains Mono', monospace`;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  function arcText(text, radius, startAngle, direction, color, spacing) {
    const letters = text.split('');
    const letterAngles = letters.map(l => (ctx.measureText(l).width + spacing) / radius);
    const totalAngle = letterAngles.reduce((a, b) => a + b, 0);
    let angle = startAngle - (totalAngle / 2) * direction;
    ctx.fillStyle = color;
    letters.forEach((letter) => {
      const a = letterAngles.shift();
      const drawAngle = angle + (a / 2) * direction;
      ctx.save();
      ctx.translate(
        o.cx + radius * Math.cos(drawAngle),
        o.cy + radius * Math.sin(drawAngle)
      );
      ctx.rotate(drawAngle + (direction > 0 ? Math.PI / 2 : -Math.PI / 2));
      ctx.fillText(letter, 0, 0);
      ctx.restore();
      angle += a * direction;
    });
  }

  arcText('LACQUER', o.rText, -Math.PI / 2,  1, o.textTopColor, fs * 0.9);
  arcText('WORKS',   o.rText,  Math.PI / 2, -1, o.textBotColor, fs * 1.1);
}

// Call after fonts are loaded:
document.fonts.ready.then(() => {
  drawMark('hero-mark', {});
  drawMark('nav-mark',  { showText: false });
});
```

### Wordmark HTML Structure
```html
<div class="wordmark">
  <div class="wm-lacquer">Lacquer</div>
  <div class="wm-works-row">
    <div class="wm-works">Works</div>
    <div class="wm-studio">STUDIO</div>
  </div>
  <div class="wm-url">lacquer.works</div>
</div>
```

```css
.wm-lacquer {
  font-family: 'Anybody', cursive;
  font-weight: 200; font-style: italic;
  font-size: 64px; line-height: 1; letter-spacing: -0.5px;
  color: #f0eaff;
}
.wm-works-row { display: flex; align-items: flex-end; }
.wm-works {
  font-family: 'Anybody', cursive;
  font-weight: 200; font-style: italic;
  font-size: 64px; line-height: 1; letter-spacing: -0.5px;
  color: #9d5cff;
}
.wm-studio {
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px; letter-spacing: 0.22em;
  color: #c4b0e8;
  margin-bottom: 10px; margin-left: 10px;
  white-space: nowrap;
}
.wm-url {
  font-family: 'JetBrains Mono', monospace;
  font-size: 9px; letter-spacing: 0.2em;
  color: #c084fc; text-align: right; margin-top: 8px;
}
```

---

## Page Structure

### Nav
- Fixed top, full width, `background: rgba(4,3,10,0.92)`, `backdrop-filter: blur(12px)`
- Left: small canvas mark (48×48, `showText: false`) + "LACQUER WORKS" in JetBrains Mono 10px uppercase
- Right: `lacquer.works` as a quiet label in `var(--url-color)`
- Border-bottom: `0.5px solid var(--faint)`
- No nav links needed — it's a holding page

### Hero
- Full viewport height (`min-height: 100vh`)
- Two-column layout on desktop (mark left, wordmark right), stacked on mobile
- Left: large canvas mark, ~320×340px
- Right: full wordmark lockup (Lacquer / Works STUDIO / lacquer.works)
- Below wordmark: single line of body copy in JetBrains Mono Light:
  > `// building at the intersection of music, data, and AI`
- Below that: one outline button — `Get in touch →` linking to `mailto:hello@lacquer.works`
- Subtle animated element: the outer ring of the mark very slowly rotates (CSS animation, 60s linear infinite, only the ring — not the whole canvas)

### About strip
- Full-width dark section (`var(--bg2)`)
- Three columns, each a short statement:
  1. `Founder & Principal Engineer` — "VP-level engineering depth, AI practitioner, independent builder."
  2. `Music + Data + AI` — "Tools for exploring, managing, and understanding music collections."
  3. `Est. MMXXV` — "Lacquer Works Studio. Seattle. Open source where possible."
- Column labels in 9px uppercase JetBrains Mono `var(--url-color)`
- Column body in 12px JetBrains Mono Light `var(--dimmed)`
- Thin `0.5px solid var(--faint)` dividers between columns

### Projects
- Section label: `// projects` in 9px uppercase `var(--url-color)`
- Three project cards in a grid (3-col desktop, 1-col mobile)
- Each card: `background: var(--bg)`, `border: 0.5px solid var(--faint)`, `padding: 24px`
- Card structure:
  - Label: `PROJECT` in 8px uppercase `#4a3880`
  - Name in Anybody 200i 22px `var(--purple)`
  - One-line description in JetBrains Mono Light 11px `var(--dimmed)`
  - Tags in 8px uppercase, `border: 0.5px solid var(--mid)`, `color: var(--purple)`
  - `→` link in `var(--violet)` pointing to GitHub (use `#` for now)
- Projects to include:
  - **discogsography** — Vinyl collection graph. Neo4j + PostgreSQL + Discogs API. `python · docker · graph`
  - **cronduit** — Docker-native cron scheduler. `docker · scheduling · open source`
  - **GRUVAX** — AI music file organiser. Anthropic Batch API + prompt caching. `python · AI · music`

### Footer
- Full width, `var(--bg)`, `border-top: 0.5px solid var(--faint)`
- Left: "Lacquer Works Studio · MMXXV"
- Right: `lacquer.works`
- Both in 9px JetBrains Mono `#4a3880`
- Minimal, no extra content

---

## Animation

- Hero mark: a very slow, barely-perceptible rotation on the canvas wrapper — `transform: rotate(360deg)`, duration `90s`, `linear`, `infinite`. Only rotate the entire canvas, not individual elements.
- On page load: fade in the hero section over 800ms with a subtle upward drift (`opacity: 0 → 1`, `translateY: 16px → 0`)
- No other animations — restraint is the aesthetic

---

## Responsive

- Breakpoint: 768px
- Below 768px: hero becomes single column (mark centered above wordmark), about strip becomes single column, projects become single column
- Nav: mark + studio name only, no URL label
- Canvas mark in hero: 220px on mobile

---

## Meta / SEO

```html
<meta name="description" content="Lacquer Works Studio — building at the intersection of music, data, and AI.">
<meta property="og:title" content="Lacquer Works Studio">
<meta property="og:description" content="Independent engineering studio. Music + Data + AI.">
<meta property="og:url" content="https://lacquer.works">
<meta name="theme-color" content="#04030a">
<title>Lacquer Works Studio</title>
```

---

## Constraints & Notes

- No gradients anywhere
- No rounded corners anywhere (`border-radius: 0` globally)
- No box shadows
- All borders `0.5px` — never `1px`
- The `drawMark` function must be called inside `document.fonts.ready.then(...)` — the arc text depends on font metrics being available
- Do not use SVG for the mark — Canvas API only
- The page should feel like a tool, not a portfolio. Spare. Precise. Atmospheric.
- When in doubt, remove rather than add.

