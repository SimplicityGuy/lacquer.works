# Lacquer Works Studio — Landing Page Design

**Date:** 2026-06-30
**Status:** Approved
**Source prompt:** `docs/lacquer-works-claude-code-prompt.md`
**Design assets:** `design/lacquer-works-assets.html`
**Background prototype:** `design/bg-prototypes.html`

---

## 1. Purpose

A single-page, atmospheric holding page for **Lacquer Works Studio** at `lacquer.works`.
Establishes identity for an independent engineer / AI practitioner building tools at the
intersection of **music, data, and AI**. Aesthetic reference: *4AD records meets Teenage
Engineering* — dark, precise, restrained, a little mysterious. It should feel like a tool,
not a portfolio.

## 2. Scope

**In scope:** one static `index.html` implementing the exact design system, page structure,
copy, and canvas logo mark defined in the source prompt, plus one dynamic background element.

**Out of scope:** multi-page site, CMS, forms/back-end, analytics, contact form (email link
only), separate favicon image files (favicon is generated at runtime from the mark).

## 3. Constraints (locked — from source prompt, built verbatim)

- **Stack:** plain HTML + CSS + vanilla JS. No frameworks, no build step, no external JS
  libraries. Single file `index.html`. Must work over `file://` and deploy as static HTML.
- **Fonts:** Google Fonts — `JetBrains Mono` (300/400/500) + `Anybody` (200 italic).
- **Palette:** exact tokens from the prompt (`--bg #04030a` … `--url-color #c084fc`).
- **Typography scale, 8px spacing grid, buttons:** exactly as tabulated in the prompt.
- **Borders/surfaces:** all borders `0.5px`; no `border-radius` anywhere (0px); no box
  shadows; no gradients.
- **Logo mark:** the `drawMark(canvasId, opts)` Canvas API function is copied **verbatim**
  from the prompt / asset file. Must be invoked inside `document.fonts.ready.then(...)`
  because the arc text depends on font metrics. Do not use SVG for the mark.
- **When in doubt, remove rather than add.**

## 4. Page structure (locked — from source prompt)

1. **Nav** — fixed top, `rgba(4,3,10,0.92)` + `backdrop-filter: blur(12px)`, bottom border
   `0.5px var(--faint)`. Left: 48×48 canvas mark (`showText:false`) + "LACQUER WORKS"
   (JetBrains Mono 10px uppercase). Right: `lacquer.works` in `--url-color`. No nav links.
2. **Hero** — `min-height:100vh`, two columns on desktop (mark left ~320×340, wordmark
   lockup right), stacked + centered on mobile (mark 220px). Wordmark = Lacquer / Works
   STUDIO / lacquer.works. Below: `// building at the intersection of music, data, and AI`
   (JetBrains Mono Light). Below that: one outline button `Get in touch →` →
   `mailto:hello@lacquer.works`.
3. **About strip** — full-width `var(--bg2)`, three columns with `0.5px var(--faint)`
   dividers: (1) Founder & Principal Engineer, (2) Music + Data + AI, (3) Est. MMXXV.
   Labels 9px uppercase `--url-color`; body 12px JetBrains Mono Light `--dimmed`.
4. **Projects** — label `// projects` (9px uppercase `--url-color`); 3 cards (3-col desktop,
   1-col mobile), `background:var(--bg)`, `border:0.5px var(--faint)`, `padding:24px`.
   Cards: **discogsography** (`python · docker · graph`), **cronduit**
   (`docker · scheduling · open source`), **GRUVAX** (`python · AI · music`). Card fields
   per prompt (PROJECT label, Anybody 22px name, 11px description, bordered tags, `→` link
   to GitHub — `#` placeholder for now).
5. **Footer** — full-width `var(--bg)`, top border `0.5px var(--faint)`. Left: "Lacquer
   Works Studio · MMXXV". Right: `lacquer.works`. Both 9px JetBrains Mono `#4a3880`.
6. **Meta/SEO** — description, `og:title`/`og:description`/`og:url`, `theme-color #04030a`,
   `<title>Lacquer Works Studio</title>` exactly as in the prompt.

## 5. Dynamic background (the one addition)

**Concept:** Vinyl grooves. **Intensity:** Present. **Scope:** behind the **hero only**.

- A `<canvas>` is absolutely positioned to fill the hero (`inset:0`, `z-index:0`); hero
  content sits at `z-index:1`. About/Projects/Footer remain flat (no background canvas).
- **Composition:** concentric record grooves centered behind the hero mark (≈ left third of
  the hero), so the field reads as a turntable halo around the logo.
- **Motion (rotation of concentric circles is visually invisible, so motion comes from):**
  1. An **outward-travelling brightness wave** — per-ring alpha modulated by
     `sin(r·0.045 − t·waveSpeed)`, crest-only, over a low base alpha.
  2. An **orbiting magenta "tonearm" dot** with a faint line to center — echoes the mark's
     terminal dots and provides clearly perceptible rotation.
  3. A slowly **breathing spindle ring** near the center.
- **Colors:** violet `#9d5cff` grooves, magenta `#f472b6` dot, purple `#c084fc` spindle —
  palette only. No gradients.
- **Parameters** carried over from the approved prototype (`drawGrooves` at intensity 1.7 =
  "Present"): `gap 15px`, `waveSpeed 0.0011·I`, base alpha `0.045`, swing `0.16·I`, orbit
  radius `min(W,H)·0.20`, orbit angular speed `−t·0.00026·I`.
- **Rendering:** single `requestAnimationFrame` loop; canvas sized to element rect ×
  `devicePixelRatio` (capped at 2); redraws fully each frame; re-initialises on resize.

### Rationale
Grooves tie most directly to the logo mark and studio identity (record/turntable). The
prototype exposed that a naive "whisper" tuning fell below the perceptual threshold; "Present"
intensity was chosen by the user after live comparison of all four candidates
(grooves / dust / lattice / waveform).

## 6. Resolved decisions (approved)

1. **Hero-mark rotation — resolved contradiction + a subtlety.** The prompt's Hero section
   says "only the ring rotates (60s), not the whole canvas"; the Animation section says
   "rotate the entire canvas (90s)." **Important:** the outer ring is a perfect circle, so
   rotating *only* the ring is visually imperceptible — same trap as the grooves background.
   The intent (a slow turntable-like rotation with the "LACQUER / WORKS" arc text staying
   upright) is achieved by rotating the mark's **asymmetric** elements instead.

   **Chosen approach — two stacked canvases, `drawMark` used verbatim on both:**
   - **Static layer (bottom):** the outer ring, groove ring, interior fill, waveform bars,
     and arc text. Rotationally-symmetric parts + the text live here and never move.
   - **Rotating layer (top, transparent bg):** the two glyph arcs + the two terminal dots
     (the asymmetric parts). This layer's wrapper is rotated via CSS `transform:rotate` over
     60s linear infinite, producing a gentle, clearly-visible orbit while text stays upright.

   The split is achieved purely through `drawMark`'s existing per-element color options — each
   layer sets the colors it should *not* draw to fully transparent (`rgba(0,0,0,0)`), and the
   rotating layer additionally uses a transparent `bg` so it composites over the static layer.
   No drawing logic is duplicated or altered. (This is a refinement of the literal "ring
   rotates" wording; confirmed acceptable because it delivers the approved outcome — visible
   slow rotation, upright text.)
2. **Accessibility — honor `prefers-reduced-motion: reduce`.** When set: do not start the
   background rAF loop (render one static grooves frame) and do not apply the ring rotation
   (static mark). The static frame must still look intentional.
3. **Favicon — generate from the mark at load.** Draw the mark to an offscreen 64×64 canvas
   and set `<link rel="icon">` to its data URL. No separate image files.
4. **Battery/perf.** Pause the background rAF loop when the document is hidden
   (`visibilitychange`) and resume when visible.

## 7. Architecture

Single `index.html`:

- **`<head>`** — meta/SEO, fonts, all CSS in one `<style>` block using the palette custom
  properties. No external CSS.
- **`<body>`** — semantic sections (nav, hero, about, projects, footer) exactly per §4, with
  the hero containing the background `<canvas>` + the two-canvas mark stack.
- **`<script>`** (one block, plain JS), organised into small, single-purpose units:
  - `drawMark(canvasId, opts)` — verbatim from prompt (the only large function).
  - Background module — `initGrooves()`, `drawGrooves(t)`, `resize()`, rAF loop, reduced-
    motion + visibility guards.
  - Mark setup — draws nav mark, the static hero-mark layer, and the rotating-ring layer.
  - Favicon generator.
  - Boot — everything mark/text-dependent runs inside `document.fonts.ready.then(...)`.

Each unit has one clear responsibility and communicates through explicit arguments, so it can
be reasoned about and adjusted independently (e.g. background tuning never touches the mark).

## 8. Responsive

- Breakpoint **768px**. Below it: hero single-column (mark centered above wordmark, mark
  220px); about strip single-column; projects single-column; nav shows mark + name only (no
  URL label). Background canvas still fills the (taller) hero.

## 9. Verification

- **Renders with no console errors** (allowing the benign missing-`favicon.ico` before the
  generated favicon is wired — which this design removes by generating one).
- **Fonts-ready gate:** arc text on the mark is correctly laid out (proves
  `document.fonts.ready` path).
- **Background is perceptibly animating** at Present intensity — verified by sampling canvas
  pixels over time (checksum changes; visible-pixel/luminance thresholds met), the method used
  to diagnose the original subtlety bug.
- **Mark rotation:** the glyph arcs + terminal dots orbit slowly while the arc text and the
  concentric rings stay upright/static.
- **`prefers-reduced-motion`:** with the media feature emulated on, no animation runs and a
  static frame is shown.
- **Responsive:** layout collapses correctly at ≤768px (checked at ~375px and ~1440px).
- **Static/offline:** opens correctly (fonts aside) without a server.

## 10. Non-goals / YAGNI

No theme switching, no light-mode page (light mark variant exists in assets but the page is
dark-only), no additional animations beyond the hero background + ring rotation + the prompt's
800ms hero fade-in-with-upward-drift on load, no build tooling, no analytics.
